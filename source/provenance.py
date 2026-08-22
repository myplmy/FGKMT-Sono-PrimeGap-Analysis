"""Immutable acquisition and provenance helpers for the upstream dataset."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_URL = "https://github.com/primegap-list-project/prime-gap-list.git"
REPOSITORY_WEB_URL = "https://github.com/primegap-list-project/prime-gap-list"
DEFAULT_BRANCH = "master"
RAW_FILE_NAME = "allgaps.sql"
SCHEMA_FILE_NAME = "schema.sql"
PINNED_SOURCE_FILES = (RAW_FILE_NAME, SCHEMA_FILE_NAME)
APPROVAL_TOKEN = "USER_APPROVED_EXPERIMENT"


class ApprovalRequiredError(PermissionError):
    """Raised before any network or experiment write when approval is absent."""


def require_experiment_approval(token: str | None) -> None:
    if token != APPROVAL_TOKEN:
        raise ApprovalRequiredError(
            "actual dataset acquisition/validation/analysis requires explicit user approval; "
            f"pass the exact approval token {APPROVAL_TOKEN!r} only after approval"
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_remote_head(
    repository_url: str = REPOSITORY_URL,
    branch: str = DEFAULT_BRANCH,
) -> str:
    """Resolve a branch to a full Git SHA without cloning the repository."""

    result = subprocess.run(
        ["git", "ls-remote", repository_url, f"refs/heads/{branch}"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
    )
    fields = result.stdout.strip().split()
    if len(fields) != 2 or fields[1] != f"refs/heads/{branch}":
        raise RuntimeError(f"unexpected git ls-remote output: {result.stdout!r}")
    commit = fields[0].lower()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError(f"invalid remote commit SHA: {commit!r}")
    return commit


def pinned_raw_url(commit: str, file_name: str = RAW_FILE_NAME) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("commit must be a lowercase 40-character Git SHA")
    if file_name not in PINNED_SOURCE_FILES:
        raise ValueError(f"unsupported upstream source file: {file_name!r}")
    return (
        "https://raw.githubusercontent.com/primegap-list-project/"
        f"prime-gap-list/{commit}/{file_name}"
    )


def _download_to_temp(url: str, target_directory: Path, *, file_name: str) -> Path:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "FGKMT-Sono-PrimeGap-Analysis/1.0"},
    )
    temporary_path: Path | None = None
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=f"{Path(file_name).stem}_",
                suffix=".part",
                dir=target_directory,
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    temporary.write(chunk)
                temporary.flush()
                os.fsync(temporary.fileno())
        assert temporary_path is not None
        return temporary_path
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def acquire_dataset(
    workspace_root: Path,
    *,
    approval_token: str | None,
    commit: str | None = None,
    branch: str = DEFAULT_BRANCH,
) -> tuple[Path, Path, dict[str, object]]:
    """Download a commit-pinned raw dataset without overwriting prior input."""

    require_experiment_approval(approval_token)
    commit_resolution = (
        "user_supplied_full_sha"
        if commit is not None
        else f"git_ls_remote_refs_heads_{branch}"
    )
    resolved_commit = commit.lower() if commit is not None else resolve_remote_head(branch=branch)
    if not re.fullmatch(r"[0-9a-f]{40}", resolved_commit):
        raise ValueError("commit must be a lowercase 40-character Git SHA")

    raw_directory = (
        workspace_root
        / "datas"
        / "raw"
        / "prime-gap-list-project"
        / resolved_commit
    )
    raw_directory.mkdir(parents=True, exist_ok=True)
    raw_path = raw_directory / RAW_FILE_NAME
    schema_path = raw_directory / SCHEMA_FILE_NAME
    metadata_path = raw_directory / "metadata.json"
    source_paths = {
        RAW_FILE_NAME: raw_path,
        SCHEMA_FILE_NAME: schema_path,
    }
    existing_paths = [path for path in source_paths.values() if path.exists()]

    if existing_paths or metadata_path.exists():
        if len(existing_paths) != len(source_paths) or not metadata_path.exists():
            raise FileExistsError(
                "partial immutable source directory exists; manual provenance review required"
            )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("commit") != resolved_commit:
            raise RuntimeError("existing metadata commit disagrees with directory commit")
        file_metadata = metadata.get("files")
        if not isinstance(file_metadata, dict):
            raise RuntimeError("existing metadata lacks per-file provenance")
        for file_name, path in source_paths.items():
            details = file_metadata.get(file_name)
            if not isinstance(details, dict):
                raise RuntimeError(f"existing metadata lacks {file_name} provenance")
            if details.get("sha256") != sha256_file(path):
                raise RuntimeError(f"existing {file_name} hash disagrees with metadata")
        return raw_path, metadata_path, metadata

    temporary_paths: dict[str, Path] = {}
    try:
        for file_name in PINNED_SOURCE_FILES:
            url = pinned_raw_url(resolved_commit, file_name)
            temporary_path = _download_to_temp(
                url,
                raw_directory,
                file_name=file_name,
            )
            if temporary_path.stat().st_size == 0:
                raise RuntimeError(f"downloaded {file_name} is empty")
            temporary_paths[file_name] = temporary_path

        file_manifest: dict[str, dict[str, object]] = {}
        for file_name, temporary_path in temporary_paths.items():
            file_manifest[file_name] = {
                "raw_url": pinned_raw_url(resolved_commit, file_name),
                "byte_count": temporary_path.stat().st_size,
                "sha256": sha256_file(temporary_path),
            }
        for file_name, temporary_path in temporary_paths.items():
            temporary_path.replace(source_paths[file_name])
    finally:
        for temporary_path in temporary_paths.values():
            temporary_path.unlink(missing_ok=True)

    metadata: dict[str, object] = {
        "source_id": "prime-gap-list-project/prime-gap-list:allgaps.sql",
        "repository_url": REPOSITORY_WEB_URL,
        "repository_git_url": REPOSITORY_URL,
        "branch_resolved": branch,
        "commit_resolution": commit_resolution,
        "commit": resolved_commit,
        "raw_url": file_manifest[RAW_FILE_NAME]["raw_url"],
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "file_name": RAW_FILE_NAME,
        "byte_count": file_manifest[RAW_FILE_NAME]["byte_count"],
        "sha256": file_manifest[RAW_FILE_NAME]["sha256"],
        "files": file_manifest,
        "raw_immutable": True,
    }
    serialized = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with metadata_path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
    except Exception:
        # A raw file without its manifest is not silently accepted on retry.
        raise

    return raw_path, metadata_path, metadata


__all__ = [
    "APPROVAL_TOKEN",
    "ApprovalRequiredError",
    "DEFAULT_BRANCH",
    "PINNED_SOURCE_FILES",
    "RAW_FILE_NAME",
    "SCHEMA_FILE_NAME",
    "REPOSITORY_URL",
    "acquire_dataset",
    "pinned_raw_url",
    "require_experiment_approval",
    "resolve_remote_head",
    "sha256_file",
]
