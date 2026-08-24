# 실행 완료 BAT 보존 폴더

이 폴더는 사용자가 실제로 실행했다고 확인한 BAT의 당시 원본을 보존한다.

규칙:

- 파일명 끝에 `-done.bat`를 붙인다.
- 보존된 파일은 당시 실행과 로그를 연결하는 provenance 자료이므로 수정하거나 다시 실행하지 않는다.
- 재시도가 필요하면 루트에 교정된 새 활성 BAT를 만든다.
- 루트의 활성 BAT가 성공 또는 실패로 실제 실행됐다고 사용자가 확인하면 그 버전도 새 `-done` 이름으로 이관한다. 이름이 충돌하면 run UTC 또는 revision을 추가한다.
- 실제 성공 여부는 BAT 존재가 아니라 로그의 종료 marker와 필수 산출물로 판정한다.

## 2026-08-23 실행 원본

| 보존 파일 | SHA-256 | 연결 로그 | 판정 |
|---|---|---|---|
| `run_P006_plateau_recurrence_pilot-done.bat` | `473DDA69C89DEAEA60D30F863F0B6DAF59BCA1911ED9E39411B1B69CC6401FA0` | `run_20260823T161227Z_p006_pilot1e8.log`, `run_20260823T173021Z_p006_pilot1e8.log` | 둘 다 실제 분석 전 runner 실패 |
| `run_P007_finite_gap_certificate_pilot-done.bat` | `459E5363566EFC04CB82783C12607135A05BD5F05F090A62C21A4180B9A90C71` | `run_20260823T173316Z_p007_pilot.log` | certificate audit 전 runner 실패 |
| `run_P006_plateau_recurrence_pilot-20260823T190035Z-done.bat` | `6527806481AAB168D1143EA37FAF59815D19BECD07CB04BDD365FA3CAF0F5FDE` | `run_20260823T190035Z_p006_pilot1e8.log` | `[2,10^8]` exact pilot·saved verification PASS, 사용자 figure QA PASS |
| `run_P007_finite_gap_certificate_pilot-20260823T185624Z-done.bat` | `7BC4524C945C4081EA93F1D50BB8E8FD3D8457F30F32703609F3504BA5A952EC` | `run_20260823T185624Z_p007_pilot.log` | supplied certificate exact audit·saved verification PASS |

성공한 P006/P007 교정판 pilot BAT는 timestamp suffix로 보존했고 루트 활성본은 제거했다. 재실행이 필요해지면 새 revision을 루트에 만들어야 한다. 아래 2026-08-24 full 실행 전까지는 full BAT가 루트에 있었으며, 실제 실행 확인 뒤 같은 규칙으로 이관했다.

## 2026-08-24 실행 원본

| 보존 파일 | SHA-256 | 연결 로그 | 판정 |
|---|---|---|---|
| `run_P008_local_residue_certificate_pilot-20260824T053954Z-done.bat` | `A04EF785C2E2E6871CC5A80ACE96BAB3778762383E319FDAAC9E1F76FFF8EF49` | `run_20260824T053954Z_p008_pilot.log` | toy feasibility·saved verification PASS |
| `run_P008_local_residue_certificate_full-20260824T064748Z-done.bat` | `AEDF970EE992B99665D096183EABA53BB63DE0C0CDAEC5F0DDD97D40EF4CA831` | `run_20260824T064748Z_p008_full.log` | phase-A full PASS; actual certified zero 0, direct acceleration false |
| `run_P006_plateau_recurrence_full-20260824T065339Z-done.bat` | `C7C8CF2F866B27BAC297D5CF9DB4BC07B2E7B98963F1CE1BC7575496AF05B448` | `run_20260824T065339Z_p006_full_1000000000.log` | `[2,10^9]` numeric/saved verification PASS; figure user QA 대기 |
| `run_P007_finite_gap_certificate_full-20260824T090010Z-done.bat` | `A242B5B9101C13ACBB37B17A8F6368F3FCCA1C5CF9ADFDCFB40F2FDCDB9479A6` | `run_20260824T090010Z_p007_full.log` | modulus 30/210/2310 exact comparison PASS |

위 네 활성 BAT는 실행 시점 원본을 timestamp suffix로 보존한 뒤 루트에서 제거했다. P005 CPU calibration과 P008 prime-count 준비는 WSL `.sh` 진입점이므로 BAT 이관 대상이 아니다.
