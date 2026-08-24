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

성공한 P006/P007 교정판 pilot BAT는 timestamp suffix로 보존했고 루트 활성본은 제거했다. 재실행이 필요해지면 새 revision을 루트에 만들어야 한다. full BAT는 아직 실행 이력이 없어 루트에 유지한다.
