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

2026-08-24에 루트에 다시 만든 P006/P007 pilot BAT는 로깅 교정판이며 아직 사용자 실제 실행으로 확인되지 않은 활성 실행기다.
