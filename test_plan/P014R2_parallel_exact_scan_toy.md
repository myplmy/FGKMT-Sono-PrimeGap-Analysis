# P014-R2 — source-row 병렬 exact certificate scan toy

## 1. 상태

`COMPLETED` — small-modulus negative-control과 synthetic modulus-30030 full-state toy 검증을
완료했다. modulus 510510 actual과 기존 P014 runner 연결은 승인 범위 밖이다.

## 2. 연구 질문과 비목적

P014 exact integer constraint scan을 source-state row block으로 나누어도 serial 정본과 같은
constraint coverage·violation·minimum slack·top-k를 얻는지 확인한다.

비목적은 floating candidate 발견, count bound 개선, search acceleration 증명, actual wall-time
예측이다.

## 3. 수학 정의

serial `scan_exact_certificate_constraints`와 같은 두 constraint family와 동일한 signed integer
slack을 계산한다. `int64` overflow upper bound가 안전할 때만 vectorized arithmetic을 허용한다.

## 4. 입력·원천·완전성

- 외부 dataset 없음
- modulus 210 feasible/infeasible nonzero-potential toy `RationalCertificate`
- modulus 30030·threshold 1856 synthetic nonzero-potential feasible certificate
- serial exact scanner를 oracle로 사용
- P010A/P014 actual certificate는 읽지 않음

## 5. 분할·복원 규칙

1. source-state index `[0,phi(M))`를 겹치지 않는 row block으로 분할한다.
2. 각 block은 모든 target state와 small/large 두 family를 빠짐없이 검사한다.
3. scanned/violation count는 합산, minimum slack은 최솟값으로 합친다.
4. top-k는 전역 exact tuple 정렬로 다시 선택한다.

## 6. 사전검증·중단 조건

- certificate shape·denominator·lambda·`t_num` guard가 serial 계약과 다르면 중단
- overflow guard가 `int64`를 넘으면 중단
- 전체 scanned constraint 수가 exact resource estimate와 다르면 중단
- feasible/infeasible toy 중 하나라도 serial과 다르면 FAIL
- worker 1·2·4·8 결과가 다르면 FAIL

## 7. 실행 명령

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_finite_gap_parallel_exact_scan -v
```

## 8. 산출물

- 별도 parallel exact-scan 모듈
- feasible/infeasible exact-equivalence 단위시험
- 로컬검증 보고서
- actual certificate·bound·그래프는 생성하지 않음

## 9. 판정 기준과 한계

serial exact core fields와 worker-count invariance가 모두 PASS할 때 toy revision만
`LOCALLY_VERIFIED`다. CPU 8개 포화나 actual 속도향상은 별도 calibration 전에는 주장하지 않는다.

## 10. 후속 작업

modulus 210/2310 중간 calibration, worker 4/8 비교, peak RAM 측정과 fail-fast memory gate가
필요하다.

## 완료 증거

- targeted P014-R2 tests: 3/3 PASS
- feasible/infeasible certificate, worker 1/2/4/8, repeated top-k tie PASS
- 통합 toy synthetic modulus 30030: 5,760 states·35,224,647 constraints,
  worker process 8개 관측
- worker별 immutable certificate array 1회 초기화·native thread=1·8-worker participation
  fail-closed PASS
- serial exact core fields equality PASS
- 정본: `test_result/202608290552_P013_P014_parallel_toy_local_validation.md`
- modulus 510510 actual·actual runner: NOT RUN / NOT PROMOTED
