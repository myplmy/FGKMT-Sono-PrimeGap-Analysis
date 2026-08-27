# P010A G4 — modulus-30030 memory-bounded cutting-plane 11시간 실험

## 1. 상태

`EXPERIMENT_PASS / EXACT_CERTIFICATE_PASS / STRICT_BOUND_IMPROVEMENT / SEARCH_ACCELERATION_NOT_PROVED`

사용자가 조건부 P010A/P010B 코드·runner 준비와 현재 약 12시간 CPU 사용을 승인했다.
P010B full scan과 P010A exact lift가 실제 PASS했으므로, 3,522만 행 전체를 저장하지 않는
working-set LP를 다음 count-upper-bound 실험으로 진행한다.

## 2. 연구 질문과 비목적

연구 질문:

1. modulus 30030의 추가 residue 자유도를 이용해 P007/P010A의 exact total upper bound
   `439161464927854179`를 strict하게 낮출 수 있는가?
2. full transition scan이 아니라 반복 sparse LP solve가 실제 병목인가?
3. 11시간·32 GB 미만·decimal 50 GB 안에서 exact certificate까지 닫을 수 있는가?

비목적:

- `[10^20,10^21)` prime을 직접 탐색하지 않는다.
- Rank 85→86 exhaustive coverage를 주장하지 않는다.
- count upper bound 개선을 search acceleration으로 부르지 않는다.
- GPU를 사용하지 않는다.
- 35,224,647-row sparse/dense matrix 전체를 만들지 않는다.

## 3. 수학 계약

변수는 `lambda >= 0`, `mu`, 5,760개 potential `phi_i`, `t >= |phi_i|`다. transition
constraint는 P007과 같은

```text
weight <= lambda * gap + mu + phi_i - phi_j
```

를 사용한다. LP floating candidate는 발견 도구일 뿐이다. 각 iteration candidate는
denominator `10^15` 정수로 반올림한 뒤 모든 35,224,647 constraints를 exact int64
streaming한다. 가장 작은 exact slack이 음수이면 공통 `mu`에 정확히 그 절댓값을 더해
보정한다. 최종 저장 certificate는 다시 full exact scan해 위반 0일 때만 PASS다.

## 4. 고정 입력과 provenance

- exact-lift run: `test_result/run_20260826T144450Z_p010a_mod30030_exact_lift`
- manifest SHA-256: `d859cc6ad9f94b9b15f6db3b72f302e3704c14257d86c3be63145b74e81a8bfe`
- input modulus-2310 certificate SHA-256:
  `725a2dcd4fd04b870a7f42edb85e6d9c029290fba861c592348a54d370c88ae5`
- lifted modulus-30030 certificate SHA-256:
  `3983025e2092a3e435f4d40dcc2be89baef1ca36496171a2eccdc680c06368d0`
- threshold: `gap >= 1856`에서 equality 포함
- baseline total bound: `439161464927854179`
- Python: `W:\miniforge3\envs\FGKMT\python.exe`

## 5. 알고리즘

1. baseline certificate에서 slack이 가장 작은 20,000 constraints를 deterministic seed로 선택
2. seed working set만 HiGHS sparse LP로 solve
3. candidate로 35,224,647 constraints 전체를 streaming scan
4. 가장 위반된 새 constraints 최대 10,000개를 추가
5. candidate를 exact integer로 반올림·공통-mu 보정·full exact scan
6. exact objective가 더 작은 certificate를 checkpoint와 별도로 best로 유지
7. 수렴, working-set cap, wall limit, solver no-candidate 중 하나에서 종료

working-set constraint는 최대 250,000개다. full matrix는 만들지 않는다. iteration마다
`checkpoints/iteration_NNNN.json`을 새 파일로 남겨 중단 뒤 어느 단계까지 갔는지 확인한다.

## 6. 자원과 중단 기준

- CPU only, GPU 금지
- total wall hard cap: 39,600초(11시간)
- 한 번의 HiGHS solve hard option: 1,800초(30분)
- maximum iterations: 100
- maximum working constraints: 250,000
- output disk cap: 50,000,000,000 bytes
- RAM 목표: 32 GB 미만; full matrix 금지와 working-set cap으로 구조적으로 제한

즉시 중단 또는 controlled 종료:

- exact-lift manifest/hash/saved verification 불일치
- exact final constraint violation 1개 이상
- 11시간 도달
- working set 250,000개 도달
- output 50 GB 초과
- solver가 candidate를 반환하지 않음
- signed-int64 overflow guard 불통과

RAM은 OS job-object hard limit이 아니라 working-set 구조 제한이다. 250,000-row sparse LP가
실측에서 과도한 메모리를 사용하면 사용자가 작업 관리자에서 종료하고 로그·마지막
checkpoint를 회신한다.

## 7. 성공 판정

실행 성공:

- terminal PASS
- saved artifact hash issue 0
- best certificate 35,224,647 exact constraints 위반 0
- iteration·중단 이유·elapsed·working-set 크기 저장

과학적 결과는 별도 분류한다.

- `strict_bound_improvement=true`: P010A count 상한 개선 성공
- `false`: 계산·검증은 PASS지만 이 설정에서는 개선 음성
- 어느 경우도 P010B search acceleration 성공이 아니다.

## 8. 예상시간과 이번 12시간 창의 사용 판단

full scan은 실제 약 0.77초였지만 5,763-variable sparse LP 시간은 아직 실측하지 않았다.
따라서 정직한 예상 범위는 약 30분–11시간이다. 빠른 수렴이나 early negative 결과면 더
일찍 끝난다. 시간을 채우기 위해 불필요한 반복을 강제하지 않는다.

P009 추가 block은 internal-zero 공급법이 없고, P012는 사용자 설계 답변 전이므로 이번
창에는 별도 queue로 섞지 않는다. 현재는 이 한 실험이 가장 장시간 계산 가치가 높다.

## 9. 사용자 실행 절차

아래 명령은 2026-08-26 완료 실행의 provenance다. 실행기는 `test_done/`으로 이관하므로
재실행하지 않는다. 새 sensitivity가 필요하면 별도 revision 계획과 runner를 만든다.

실행 환경은 **Windows FGKMT Conda Prompt 또는 Windows PowerShell**이었다. WSL에서 직접
실행하지 않았다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p010a\run_p010a_mod30030_cutting_plane_11h.ps1 -ConfirmP010AG4
```

실행 중 `[CUT]` 줄이 seed 및 iteration checkpoint를 표시한다. 중간 `[FAIL]`이 나오면 같은
명령을 즉시 재실행하지 않는다. 완료 또는 실패 뒤 다음을 회신한다.

1. 마지막 `[PASS]` 또는 첫 `[FAIL]` 줄
2. `test_result/logs/run_<UTC>_p010a_mod30030_cutting_plane_11h.log`
3. result directory
4. `summary.json`이 있으면 `outcome`, `best_total_upper_bound`,
   `strict_bound_improvement`
5. 비정상 종료면 마지막 `checkpoints/iteration_NNNN.json`

## 10. 예상 산출물

- `seed_scan_report.json`
- `checkpoints/iteration_NNNN.json`
- `iteration_history.json`
- `best_certificate_mod30030.txt`
- `exact_best_report.json`
- `summary.json`, `manifest.json`, `saved_verification_report.json`
- stdout/stderr 전체 log

## 11. 실제 결과

- run: `test_result/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h`
- log: `test_result/logs/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h.log`
- core elapsed: 20.919초
- solver runs: 4, final working constraints: 20,123
- exact full scan: 35,224,647 constraints, violation 0, minimum integer slack 0
- baseline total bound: `439161464927854179`
- best exact total bound: `436001550591586306`
- 감소: `3159914336267873`, 약 0.7195336%
- outcome: `FULL_FLOATING_CONVERGENCE`
- direct search acceleration: false

11시간은 hard cap이었고 네 번째 candidate가 full scan 위반 0으로 정상 수렴해 일찍
종료했다. 상세 정본은
`test_result/202608271208_P010A_G4_mod30030_cutting_plane_result_analysis.md`다.
