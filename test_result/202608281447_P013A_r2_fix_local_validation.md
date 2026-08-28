# P013-A r2 대규모 hypergeometric 교정 로컬검증

## 판정

`IMPLEMENTED / LOCALLY_VERIFIED / ACTUAL_NOT_RUN`

P013-A r1의 NumPy large-parameter 제한을 exact sequential symmetry sampler로 교정하고,
sufficient-statistics checkpoint와 Windows 물리 4코어·논리 8프로세서 자원 정책을 추가했다.
P013-A r2, P013-B, P014/P015 actual은 이 검증에서 실행하지 않았다.

## 수학·재현성 gate

- target law: exact finite-population hypergeometric
- binomial approximation: false
- NumPy safe path: raw `Generator.hypergeometric` 10,000 draws와 bit-for-bit 동일
- large path: 네 symmetry support·mean 검사 PASS
- small exact PMF: 300,000 draws의 각 outcome 빈도가 exact combinatorial PMF의 6 sigma 안
- NumPy category limit 경계: `10^9` 이상에서 corrected backend 선택
- reviewed sequential draw cap: component당 `2,000,000`, 초과 시 fail closed
- P013 frozen range/bin/cohort/seed/replications/alpha: 변경 없음
- checkpoint canonical hash·plateau identity·N/M/C·scheme별 exposure 합 검증: PASS

## CPU resource gate

| 항목 | 확인값 |
|---|---:|
| CPU | AMD Ryzen 7 9700X |
| detected physical cores | 8 |
| detected logical processors | 16 |
| requested physical/logical | 4 / 8 |
| selected affinity mask | `0xff` |
| selected logical bits | 8 |
| 실제 child-process affinity smoke | PASS |
| thread-pool ceiling | OMP/OpenBLAS/MKL/NumExpr/BLIS 각 8 |

P013 sieve/통계 component loop와 P014 exact scan은 single Python stream이다. affinity 8은 사용
가능 상한이지 8-way 병렬화 주장이 아니다. P014의 HiGHS 내부 병렬 구간은 process affinity 안에서
최대 8 logical processor를 사용할 수 있다.

## 실행기·preflight gate

- affected Python `py_compile`: PASS
- active PowerShell parser: 11 files, issue 0
- root BAT approval-denial: P013-A r2/P013-B/P014/P015 4/4 PASS
- P013-A resource/input preflight: PASS, actual=false
- P013-B resource/input preflight: PASS, actual=false
- P014 G4/resource/overflow preflight: PASS, actual=false
- affected unittest: 23/23 PASS
- full unittest: 148/148 PASS
- sandbox 내부 기존 temp cleanup tests: 알려진 `WinError 5` 재현
- 같은 affected/full tests의 sandbox 밖 고정 FGKMT Python 재실행: PASS

## 실행 이력 보존

- r1 BAT SHA-256 `1923DFCDE1214C9C831A8567A5F88092698D9BABB90315559F882590C0ED20D5`
- r1 PS1 SHA-256 `3C49161D7D8B0C85E6C2A65DB4B746F138888C1ECFBD30FAA7FB9774840720A4`
- 두 파일은 hash 불변으로 `test_done/*20260827T163052Z-failed-done.*`에 이관
- r2 활성 BAT: `run_P013A_recurrence_extension_1e11_r2.bat`
- P015 child path도 r2로 교정

## 남은 gate

사용자가 P013-A r2 actual을 실행해 terminal PASS, result directory, log를 회신해야 한다. Codex는
manifest·checkpoint binding·large sampler provenance·두 번째 full recomputation·figure 자동 QA를
감사하고, 사용자가 figure를 시각 확인한 뒤에만 `EXPERIMENT_PASS`를 부여한다.
