# P013 segment·P014 exact-scan 병렬 toy 로컬검증 보고서

검증 시각: 2026-08-29 05:52 KST

## 판정

`LOCALLY_VERIFIED_TOY_ONLY / ACTUAL_NOT_RUN / ACTUAL_RUNNER_NOT_PROMOTED`

P013 segment sufficient-statistics와 P014 source-row exact constraint scan을 각각 별도 process
병렬 모듈로 구현했다. serial 정본과 worker `1/2/4/8` 결과가 exact하게 일치했고, 통합 toy에서
affinity `0xff` 아래 worker process 8개가 실제 관측됐다. 계산 정밀도 축소, prime/gap/constraint
생략, floating 대체는 없었다.

## 사용자 질문에 대한 판단

P013 recurrence를 같은 형태로 계속 큰 decade에 반복할 과학적 필요는 LOW_INFORMATION 때문에
자동으로 인정할 수 없다. 그러나 segmented-prime sufficient-statistics 엔진은 후속 holdout,
민감도, 독립 saved recomputation에서 재사용될 가능성이 높다. P014 exact scan은 한 actual에서도
여러 번 반복되므로 별도 병렬 revision의 재사용 가능성이 높다.

## 구현 격리

- P013 toy: `source/parallel_segment_statistics.py`
- P014-R2 toy: `source/finite_gap_parallel_exact_scan.py`
- 통합 toy 검증기: `source/parallel_toy_validation_cli.py`
- P013 tests: `tests/test_parallel_segment_statistics.py`
- P014 tests: `tests/test_finite_gap_parallel_exact_scan.py`

기존 `source/recurrence_sequential_extension.py`, serial exact scanner, P013/P014 actual runner는
교체하지 않았다.

## P013 exact completeness 검증

검증한 불변식:

1. `[L,U)`를 겹침·누락 없는 정수 segment로 분할
2. 각 segment에서 첫 `q>=b`까지 포함해 마지막 crossing gap을 닫음
3. 인접 segment마다 `left.boundary_prime == right.first_prime`
4. worker local `prime_count == gap_count + 1`
5. worker local `gap_count == segment 안 prime/gap-start 수`
6. prime 배열은 process 사이에 전달하지 않고 integer sufficient statistics만 전달
7. populations, gap counts, exposure counts, equal-exposure counts 전체를 serial과 대조
8. downstream plateau와 component table도 serial과 동일
9. worker 수 `1/2/4/8` 및 13개 비균등 segment에서 동일

통합 toy 결과:

| 항목 | 값 |
|---|---:|
| 범위 | `[100000,1000003)` |
| exact gap starts | 68,906 |
| segment | 32 |
| 요청 worker | 8 |
| 관측 worker process | 8 |
| serial/parallel exact equality | PASS |

## P014-R2 exact completeness 검증

검증한 불변식:

1. source-state row `[0,phi(M))` 전체를 겹침·누락 없이 분할
2. 각 source-target 쌍의 small/large 두 constraint family를 모두 검사
3. signed `int64` overflow upper bound를 serial과 동일하게 적용
4. scanned/violation count는 exact integer 합산
5. minimum slack은 exact global minimum
6. top-k는 `(slack,source,target,gap,weight)` 전역 정렬로 worker 완료 순서와 무관
7. feasible와 deliberately infeasible modulus-210 certificate 모두 serial과 동일
8. worker 수 `1/2/4/8`에서 동일하고 top-k tie repeat도 동일

통합 toy 결과:

| 항목 | 값 |
|---|---:|
| modulus | 30,030 (synthetic certificate) |
| states | 5,760 |
| threshold | 1,856 |
| exact scanned constraints | 35,224,647 |
| 요청 worker | 8 |
| 관측 worker process | 8 |
| serial/parallel exact equality | PASS |

통합 검증의 modulus·state·constraint 규모는 P010A와 같지만 입력은 실제 P014 certificate가
아니라 nonzero periodic potential과 nonzero lambda를 가진 합성 feasible certificate다. 따라서
대규모 분할·산술·merge 경로는 시험하되 기존 count bound를 다시 계산하거나 변경하지 않는다.

## 중첩 thread 방지

부모 프로세스는 물리 4코어·논리 8프로세서, affinity `0xff`를 적용했다. 각 worker initializer는
`OMP/OPENBLAS/MKL/NUMEXPR/VECLIB/BLIS` thread 상한을 `1`로 다시 설정했다. 통합 toy에서 모든
worker가 이 값을 실제 보고했다. 따라서 8 process가 각각 8 native thread를 만드는 64-thread
oversubscription은 막았다.

P014 worker는 immutable certificate·residue·potential 배열을 process 초기화 때 한 번만 만들고,
row block마다 다시 전송하거나 복제하지 않는다. 시작 barrier 뒤 요청한 8개 worker 모두 적어도
한 block을 처리하지 않으면 fail-closed한다.

## 실행 증거

Python:

```text
W:\miniforge3\envs\FGKMT\python.exe
```

초기 sandbox 실행은 Windows multiprocessing Pipe 생성에서 `PermissionError: [WinError 5]`로
차단됐다. 이는 계산 불일치가 아니라 sandbox process-IPC 제한이었다. 승인된 sandbox 외부에서
동일 명령을 다시 실행했다.

Targeted:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest `
  tests.test_parallel_segment_statistics `
  tests.test_finite_gap_parallel_exact_scan -v
```

결과: `7 tests`, `17.099s`, `OK`.

통합 toy:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B `
  -m source.parallel_toy_validation_cli --workers 8
```

결과: terminal `status=PASS`, P013/P014 각각 worker 8개 관측, 정밀도 축소·누락 false.

전체 회귀시험:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
```

결과: `158 tests`, `24.422s`, `OK`.

`py_compile`도 새 source/test 5개에서 exit 0이었다.

## 아직 검증하지 않은 것

- P013 actual decade의 속도향상·peak RAM·crash recovery
- P014 modulus 510510의 속도향상·메모리 대역폭·peak RAM
- worker 4개와 8개 중 어느 쪽이 wall time이 더 짧은지
- 병렬 engine을 actual manifest/saved verifier에 연결하는 schema revision
- P013 Monte Carlo 자체의 병렬화

따라서 이 결과는 **누락 없는 병렬 분할·exact merge의 toy 타당성**만 확정한다. actual runner에
연결하려면 중간범위 calibration과 별도 사용자 승인이 필요하다.
