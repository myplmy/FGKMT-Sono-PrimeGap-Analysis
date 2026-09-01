"""Auditable CPU affinity planning for user-run CPU-only experiments."""

from __future__ import annotations

import ctypes
import os
import struct
from dataclasses import asdict, dataclass


_PROCESS_JOB_HANDLE: int | None = None
_PROCESS_JOB_LIMIT_BYTES: int | None = None


DEFAULT_PHYSICAL_CORES = 4
DEFAULT_LOGICAL_PROCESSORS = 8
THREAD_ENVIRONMENT_VARIABLES = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
)


class CpuResourceError(RuntimeError):
    """Raised when the requested CPU-only resource contract cannot be applied."""


class MemoryResourceError(RuntimeError):
    """Raised when a process-tree memory ceiling cannot be applied."""


@dataclass(frozen=True, slots=True)
class CpuResourcePlan:
    platform: str
    requested_physical_cores: int
    requested_logical_processors: int
    detected_physical_cores: int
    detected_logical_processors: int
    selected_logical_processors: int
    affinity_mask_hex: str
    topology_mapping: str

    def as_dict(self) -> dict[str, int | str | bool]:
        return asdict(self)


def _windows_core_masks() -> tuple[int, ...]:
    """Return one group-0 logical-processor mask per physical Windows core."""

    if os.name != "nt":
        raise CpuResourceError("Windows processor topology was requested off Windows")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    function = kernel32.GetLogicalProcessorInformationEx
    function.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong))
    function.restype = ctypes.c_int
    length = ctypes.c_ulong(0)
    relation_processor_core = 0
    function(relation_processor_core, None, ctypes.byref(length))
    if length.value == 0:
        raise CpuResourceError("Windows did not report processor topology size")
    buffer = ctypes.create_string_buffer(length.value)
    if not function(relation_processor_core, buffer, ctypes.byref(length)):
        raise CpuResourceError(
            f"GetLogicalProcessorInformationEx failed: {ctypes.get_last_error()}"
        )

    raw = buffer.raw
    offset = 0
    pointer_bytes = ctypes.sizeof(ctypes.c_void_p)
    group_affinity_bytes = pointer_bytes + 8
    masks: list[int] = []
    while offset < length.value:
        relationship, size = struct.unpack_from("II", raw, offset)
        if size <= 0 or offset + size > length.value:
            raise CpuResourceError("Windows processor topology buffer is malformed")
        if relationship == relation_processor_core:
            group_count = struct.unpack_from("H", raw, offset + 30)[0]
            selected = 0
            for group_index in range(group_count):
                base = offset + 32 + group_index * group_affinity_bytes
                mask = int.from_bytes(raw[base : base + pointer_bytes], "little")
                group = struct.unpack_from("H", raw, base + pointer_bytes)[0]
                if group == 0:
                    selected |= mask
            if selected:
                masks.append(selected)
        offset += size
    if not masks:
        raise CpuResourceError("Windows reported no group-0 physical cores")
    return tuple(masks)


def plan_cpu_resources(
    *,
    physical_cores: int = DEFAULT_PHYSICAL_CORES,
    logical_processors: int = DEFAULT_LOGICAL_PROCESSORS,
) -> CpuResourcePlan:
    if physical_cores < 1 or logical_processors < physical_cores:
        raise CpuResourceError("invalid physical/logical CPU budget")
    if os.name != "nt":
        available = sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else list(range(os.cpu_count() or 1))
        if len(available) < logical_processors:
            raise CpuResourceError("requested logical CPU budget is unavailable")
        mask = sum(1 << index for index in available[:logical_processors])
        return CpuResourcePlan(
            os.name,
            physical_cores,
            logical_processors,
            0,
            len(available),
            logical_processors,
            hex(mask),
            "logical-only-non-windows",
        )

    core_masks = _windows_core_masks()
    detected_logical = sum(mask.bit_count() for mask in core_masks)
    if len(core_masks) < physical_cores:
        raise CpuResourceError("requested physical CPU budget is unavailable")
    selected_masks = core_masks[:physical_cores]
    selected_mask = 0
    for mask in selected_masks:
        selected_mask |= mask
    selected_logical = selected_mask.bit_count()
    if selected_logical != logical_processors:
        raise CpuResourceError(
            "selected physical cores do not expose the requested logical count: "
            f"{selected_logical} != {logical_processors}"
        )
    return CpuResourcePlan(
        "windows",
        physical_cores,
        logical_processors,
        len(core_masks),
        detected_logical,
        selected_logical,
        hex(selected_mask),
        "windows-physical-core-topology",
    )


def configure_cpu_resources(
    *,
    physical_cores: int = DEFAULT_PHYSICAL_CORES,
    logical_processors: int = DEFAULT_LOGICAL_PROCESSORS,
) -> dict[str, int | str | bool | dict[str, str]]:
    """Apply the reviewed process affinity and thread-pool ceiling."""

    plan = plan_cpu_resources(
        physical_cores=physical_cores,
        logical_processors=logical_processors,
    )
    for name in THREAD_ENVIRONMENT_VARIABLES:
        os.environ[name] = str(logical_processors)
    mask = int(plan.affinity_mask_hex, 16)
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        get_current_process = kernel32.GetCurrentProcess
        get_current_process.argtypes = ()
        get_current_process.restype = ctypes.c_void_p
        set_affinity = kernel32.SetProcessAffinityMask
        set_affinity.argtypes = (ctypes.c_void_p, ctypes.c_size_t)
        set_affinity.restype = ctypes.c_int
        current = get_current_process()
        if not set_affinity(current, ctypes.c_size_t(mask)):
            raise CpuResourceError(f"SetProcessAffinityMask failed: {ctypes.get_last_error()}")
    elif hasattr(os, "sched_setaffinity"):
        selected = {index for index in range(mask.bit_length()) if mask & (1 << index)}
        os.sched_setaffinity(0, selected)
    else:
        raise CpuResourceError("this platform cannot apply process affinity")
    payload = plan.as_dict()
    payload.update(
        {
            "affinity_applied": True,
            "thread_pool_limits": {
                name: os.environ[name] for name in THREAD_ENVIRONMENT_VARIABLES
            },
        }
    )
    return payload


def configure_process_tree_memory_limit(*, limit_bytes: int) -> dict[str, int | str | bool]:
    """Apply a Windows Job Object limit inherited by spawned worker processes."""

    global _PROCESS_JOB_HANDLE, _PROCESS_JOB_LIMIT_BYTES
    if not 1_000_000_000 <= limit_bytes < 32_000_000_000:
        raise MemoryResourceError(
            "process-tree memory limit must be in [1 GB, 32 GB)"
        )
    if os.name != "nt":
        raise MemoryResourceError(
            "the P018 process-tree memory ceiling is implemented for Windows"
        )
    if _PROCESS_JOB_HANDLE is not None:
        if _PROCESS_JOB_LIMIT_BYTES != limit_bytes:
            raise MemoryResourceError("a different process-tree memory limit is active")
        return {
            "platform": "windows_job_object",
            "limit_bytes": limit_bytes,
            "applied": True,
            "inherited_by_child_processes": True,
            "already_active": True,
        }

    from ctypes import wintypes

    class JobObjectBasicLimitInformation(ctypes.Structure):
        _fields_ = (
            ("PerProcessUserTimeLimit", ctypes.c_int64),
            ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        )

    class IoCounters(ctypes.Structure):
        _fields_ = (
            ("ReadOperationCount", ctypes.c_uint64),
            ("WriteOperationCount", ctypes.c_uint64),
            ("OtherOperationCount", ctypes.c_uint64),
            ("ReadTransferCount", ctypes.c_uint64),
            ("WriteTransferCount", ctypes.c_uint64),
            ("OtherTransferCount", ctypes.c_uint64),
        )

    class JobObjectExtendedLimitInformation(ctypes.Structure):
        _fields_ = (
            ("BasicLimitInformation", JobObjectBasicLimitInformation),
            ("IoInfo", IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        )

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_job = kernel32.CreateJobObjectW
    create_job.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    create_job.restype = wintypes.HANDLE
    set_information = kernel32.SetInformationJobObject
    set_information.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    set_information.restype = wintypes.BOOL
    assign_process = kernel32.AssignProcessToJobObject
    assign_process.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    assign_process.restype = wintypes.BOOL
    get_current_process = kernel32.GetCurrentProcess
    get_current_process.argtypes = ()
    get_current_process.restype = wintypes.HANDLE
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = (wintypes.HANDLE,)
    close_handle.restype = wintypes.BOOL

    handle = create_job(None, None)
    if not handle:
        raise MemoryResourceError(
            f"CreateJobObjectW failed: {ctypes.get_last_error()}"
        )
    job_memory_limit = 0x00000200
    kill_on_job_close = 0x00002000
    information = JobObjectExtendedLimitInformation()
    information.BasicLimitInformation.LimitFlags = (
        job_memory_limit | kill_on_job_close
    )
    information.JobMemoryLimit = limit_bytes
    if not set_information(
        handle,
        9,
        ctypes.byref(information),
        ctypes.sizeof(information),
    ):
        error = ctypes.get_last_error()
        close_handle(handle)
        raise MemoryResourceError(f"SetInformationJobObject failed: {error}")
    if not assign_process(handle, get_current_process()):
        error = ctypes.get_last_error()
        close_handle(handle)
        raise MemoryResourceError(f"AssignProcessToJobObject failed: {error}")
    _PROCESS_JOB_HANDLE = int(handle)
    _PROCESS_JOB_LIMIT_BYTES = limit_bytes
    return {
        "platform": "windows_job_object",
        "limit_bytes": limit_bytes,
        "applied": True,
        "inherited_by_child_processes": True,
        "already_active": False,
    }


__all__ = [
    "CpuResourceError",
    "CpuResourcePlan",
    "MemoryResourceError",
    "DEFAULT_LOGICAL_PROCESSORS",
    "DEFAULT_PHYSICAL_CORES",
    "THREAD_ENVIRONMENT_VARIABLES",
    "configure_cpu_resources",
    "configure_process_tree_memory_limit",
    "plan_cpu_resources",
]
