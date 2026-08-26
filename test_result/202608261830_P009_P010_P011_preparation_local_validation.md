# P009/P010/P011 구현 준비 로컬검증

## 판정

`LOCALLY_VERIFIED / ACTUAL_FOLLOW_UP_NOT_RUN`

P009 single-block production adapter, P010A modulus-2310 replay, P010B
modulus-30030 one-candidate scan, P011 recurrence null-model의 코드·실행기를 준비했다.
정적·toy 검증은 PASS했지만 P009 actual, P010A/B actual, P011 pilot은 실행하지 않았다.

## 검증 증거

| 항목 | 결과 |
|---|---|
| fixed Python py_compile | PASS |
| 전체 unittest | 100 tests, 4.827 s, PASS |
| 새 targeted tests | 13 tests, PASS |
| manifest-binding 보정 후 targeted 재검증 | 16 tests, PASS |
| PowerShell parser | 17 files, issue 0 |
| archived PARI helper `bash -n` | PASS |
| P010A certificate preflight | modulus 2310, pinned SHA-256 일치, PASS |
| P011 input preflight | 29 complete plateaus, 130 distinct gaps, 50,847,533 total gaps, PASS |
| 실제 GP boundary serialization smoke | `[100,120)`, `p=113`, `q=127`, factor rows 6, PASS |
| `git diff --check` | whitespace error 0; line-ending warning만 존재 |

전체 unittest는 반복로그 금지 호출 감사, end-bounded interval, P006/P007/P008 기존
검증, P009 ECPP 형식, P010 approval gate, P011 fixed-seed toy까지 포함한다.

## fool-proof 보정

P010A `manifest.json`의 `status=PASS`만 downstream 조건으로 쓰지 않는다.
`saved_verification_report.json`이 다음을 모두 만족해야 P009/P010B가 시작된다.

- `status=PASS`
- `exact_recomputed=true`
- report의 `manifest_sha256`가 실제 manifest hash와 일치

따라서 계산 산출물만 작성한 뒤 saved verification에서 실패하거나 중단된 run은 다음
실험의 선행조건으로 사용할 수 없다.

## 준비된 실행기

- P010A:
  `scripts/experiments/p010a/run_p010a_mod2310_replay.ps1`
- P011:
  `scripts/experiments/p011/run_p011_recurrence_null_pilot.ps1`
- P009 actual, P010A PASS 뒤:
  `scripts/experiments/p009/run_p009_single_block_actual.ps1`
- P010B scan, P010A PASS 뒤:
  `scripts/experiments/p010b/run_p010b_mod30030_one_candidate_scan.ps1`

모든 active runner는 fixed FGKMT Python, 확인 flag, non-overwrite run directory,
stdout/stderr full logging과 stage failure를 사용한다.

## 아직 주장할 수 없는 것

- P009 actual block `CERTIFIED_ZERO`
- modulus-30030 exact certificate 또는 더 작은 count upper bound
- P010B direct search acceleration
- P011 recurrence의 통계적 결과 또는 수론적 구조
- `[10^20,10^21)` exhaustive coverage
