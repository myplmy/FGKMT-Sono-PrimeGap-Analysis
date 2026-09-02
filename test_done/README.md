# 실행 완료 진입점·실험 전용 보조파일 보존 폴더

이 폴더는 사용자가 실제로 실행했다고 확인했거나 사용자 승인 범위에서 완료된
BAT·PowerShell·WSL 진입점과, 해당 완료 실험에만 쓰인 보조파일의 당시 원본을 보존한다.

규칙:

- 파일명은 확장자 앞에 `-done`을 붙이고, 가능하면 연결 run UTC도 넣는다.
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
| `run_P006_plateau_recurrence_full-20260824T065339Z-done.bat` | `C7C8CF2F866B27BAC297D5CF9DB4BC07B2E7B98963F1CE1BC7575496AF05B448` | `run_20260824T065339Z_p006_full_1000000000.log` | `[2,10^9]` numeric/saved verification PASS; 2026-08-26 figure 3개 사용자 시각 QA PASS |
| `run_P007_finite_gap_certificate_full-20260824T090010Z-done.bat` | `A242B5B9101C13ACBB37B17A8F6368F3FCCA1C5CF9ADFDCFB40F2FDCDB9479A6` | `run_20260824T090010Z_p007_full.log` | modulus 30/210/2310 exact comparison PASS |

위 네 활성 BAT는 실행 시점 원본을 timestamp suffix로 보존한 뒤 루트에서 제거했다.

## 2026-08-26 PowerShell·WSL 완료본 정리

| 보존 파일 | SHA-256 | 연결 로그·역할 | 판정 |
|---|---|---|---|
| `run_pilot-20260822T181837Z-done.ps1` | `E379530DEB708FDC0B835EB6D22F6ACFE5E1DBE40A85FC372497BDC156F245FF` | `run_20260822T181837Z_pilot5.log` | P002 PASS 당시 원본 |
| `run_full_analysis-20260822T195906Z-done.ps1` | `AB91294CD4DD1539D98F67B1A10BA9DDE0570E16DB167C9B0EE41C52D78FA8FC` | P003의 3회 로그, 정본 `run_20260822T195906Z_full1e20.log` | P003 PASS 당시 원본 |
| `run_sensitivity_analysis-20260823T075238Z-done.ps1` | `87A4B0C301B2D98B361FD8FF65860D3E360D568ACAD618AF67F356A0AF66932A` | `run_20260823T075238Z_p004_sensitivity.log` | P004 PASS 당시 원본 |
| `run_plateau_recurrence-20260824T065339Z-done.ps1` | `CF25E9102B4E3B4696E977C77439F69D379568419543BDE9CF47EC3F13980DE3` | P006 pilot·full 로그 | P006 완료 공통 runner 원본 |
| `run_finite_gap_certificate-20260824T090010Z-done.ps1` | `B30E25E88AC4728BADAF4A8C755684A94BB0A72CF26718058C5CC400612F6E7E` | P007 pilot·full 로그 | P007 완료 공통 runner 원본 |
| `run_local_residue_certificate-20260824T064748Z-done.ps1` | `398322A17FC3AE59BA0BDB88CF91DD25E59A1BE046C197F2F432EE75FDC35585` | P008 pilot·full 로그 | P008 완료 공통 runner 원본 |
| `prepare_P008_local_primecounts-20260824T054725Z-done.sh` | `AC9D7F2DB462A23A6C3A5176A0457DBDE5E3A66F00DCB459A4F100FA3D3A03FB` | `run_20260824T054725Z_p008_primecount_prepare.log` | P008 exact-count 입력 준비 PASS |
| `run_P005_prime_gap_cpu_calibration-20260824T054203Z-done.sh` | `5B709D2DC66A4D847F637B2F8E8D5F3BE19A0B2F101C4B51A1F4F8394D667A52` | `run_20260824T054203Z_p005_prime_gap_cpu_calibration.log` | P005 WSL 진입점 PASS |
| `run_prime_gap_cpu_calibration-helper-20260824T054203Z-done.sh` | `9B05A79E34C357A62AEB030795F09BF9848F6440AB4FD1B7D5024C925789A25E` | 위 P005 run 내부 helper | P005 전용, 재사용하지 않음 |
| `test_prime_gap_reference_db-p005-done.sh` | `037B9BA48A407D379B153CB9E2A53B9B483299EB7F12511B5757D449DE424815` | P005 DB fixture 검사 | P005 전용, 재사용하지 않음 |
| `test_prime_gap_sqlite_schema-p005-done.sh` | `6D17770C0BD46A26C4E7FF9FE7D5E4385050766D397C3EA9A074CE509F0A1508` | P005 SQLite schema 검사 | P005 전용, 재사용하지 않음 |
| `run_experiment-legacy-20260826-done.ps1` | `B39568E193579B88477FC68EAEECD1DBA81E6189314CBA7F2C2039046BE0D6F5` | 초기 P001 승인 gate | 완료 run 원본이 아니라 새 공통 runner로 대체된 legacy 진입점 |
| `install_pari_gp_wsl-20260826T084156Z-done.sh` | `4DE35165CDA2E84FAB1D55A1DE4ACB9B5E01C16075005FCE8D139DC2F900B3B0` | `tmp/setup/install_pari_gp_20260826T084156Z.log` | PARI/GP 2.15.4 설치·`primecertisvalid` smoke test PASS |
| `run_p009_pari_adapter_validation-20260826T090950Z-done.ps1` | `FB89EB038B2C41F163ABCDAFC58F49EC469B2AC0EAC9E88B9505B08C82B2394B` | `test_result/logs/run_20260826T090950Z_p009_pari_adapter_validation.log` | small integer·중간 ECPP·wrong-subject 음성대조·saved verification PASS |
| `run_p010a_mod2310_replay-20260826T100715Z-done.ps1` | `3DC6245720B2E8BB76F211C4C38B1800995AA85BE00FFC847302F54E4EBCB402` | `test_result/logs/run_20260826T100715Z_p010a_mod2310_replay.log` | 두 exact builder·chunk oracle·saved verification PASS; 상한 동일 |
| `run_p011_recurrence_null_pilot-20260826T100938Z-done.ps1` | `9091AA1ACDB1F73D9514CFC9BEBD428615EE7C43C894D9F19151832D4E121C2E` | `test_result/logs/run_20260826T100938Z_p011_recurrence_null_pilot.log` | stationary-null 실행 PASS; enrichment 미지지·null 부적합 진단, 사용자 figure QA PASS |
| `run_p009_p010_bounded_queue-20260826T144439Z-done.ps1` | `E2885AE8123BFEB5480E600BFD1807D23AEFF28C0523A8E4E8DE5D199356AE97` | `test_result/logs/run_20260826T144439Z_p009_p010_bounded_queue.log` | P010B scan·P010A exact lift·P009 single-block을 orchestration, aggregate PASS |
| `run_p010b_mod30030_one_candidate_scan-20260826T144440Z-done.ps1` | `CAAAE0250757DD9152F85CA60A3CAA428808A0890022DD6A070A5050DEEB640D` | `test_result/logs/run_20260826T144440Z_p010b_mod30030_candidate_scan.log` | 35,224,647 floating constraints scan PASS, violation 0; LP·acceleration 미증명 |
| `run_p010a_mod30030_exact_lift-20260826T144450Z-done.ps1` | `2AE15C9E5C2E539059EB3BC6560F75F3C3DB260347930FAAFDFB7D51BE262171` | `test_result/logs/run_20260826T144450Z_p010a_mod30030_exact_lift.log` | 35,224,647 exact constraints PASS, 상한 불변 |
| `run_p009_single_block_actual-20260826T144500Z-done.ps1` | `9A242D2AD1D05E06B3B59B992F9178EF9E9E7A2825C0525F17D87B2356E24266` | `test_result/logs/run_20260826T144500Z_p009_single_block_actual.log` | `[10^20,10^20+1000)` exact certified zero 1 block, acceleration 미증명 |
| `run_p010a_mod30030_cutting_plane_11h-20260826T155918Z-done.ps1` | `6DCE831B8E29D72D4A0EF2BA62FF0120C679A6BB93C1789A37F8EC98AFFAA8C2` | `test_result/logs/run_20260826T155918Z_p010a_mod30030_cutting_plane_11h.log` | 4 solves·exact 35,224,647 constraints PASS, total bound 약 0.7195% 개선; acceleration 미증명 |

## 2026-08-27 PowerShell 실행 실패본

| 보존 파일 | SHA-256 | 연결 로그·역할 | 판정 |
|---|---|---|---|
| `run_p012_stratified_null_development-20260827T032233Z-failed-done.ps1` | `61FF041F32813D377D9414E700638DAC359961CD29699778AE0969B40404A9F3` | `test_result/logs/run_20260827T032233Z_p012a_stratified_null_development.log` | preflight·targeted tests PASS 뒤 zero-variance `z=None` 시각화의 `float(None)` 결함으로 USER_RUN_FAILED |
| `run_p012_stratified_null_development_r2-20260827T054007Z-done.ps1` | `0AF40C63E02B962C2C1716D868C15A8DABC4A52302E2B87E9E9BE36201AB8E28` | `test_result/logs/run_20260827T054007Z_p012a_stratified_null_development_r2.log` | P012-A r2 terminal·saved full recomputation PASS; 통계 artifact는 r1과 동일, figure visual QA는 사용자 대기 |
| `run_P013A_recurrence_extension_1e11-20260827T163052Z-failed-done.bat` | `1923DFCDE1214C9C831A8567A5F88092698D9BABB90315559F882590C0ED20D5` | `test_result/logs/run_20260827T163052Z_p013a_recurrence_extension_1e11.log` | exact range sweep 완료 뒤 NumPy large-hypergeometric parameter limit로 USER_RUN_FAILED |
| `run_p013a_recurrence_extension_1e11-20260827T163052Z-failed-done.ps1` | `3C49161D7D8B0C85E6C2A65DB4B746F138888C1ECFBD30FAA7FB9774840720A4` | 위 P013-A r1 실패 run의 실험 전용 PowerShell entrypoint | r2로 교체되어 재실행 금지 |

재사용 기능은 다음으로 분리했다.

- 공통 로깅: `scripts/common/powershell_stage_logging.ps1`
- 일반 FGKMT pipeline: `scripts/runners/run_fgkmt_pipeline.ps1`
- 공통 self-test: `scripts/tests/`
- 신규 실험별 toy 진입점: `scripts/experiments/<experiment>/`

## 2026-09-01 P018-A 실행 원본

| 보존 파일 | SHA-256 | 연결 로그·역할 | 판정 |
|---|---|---|---|
| `run_P018A_prefix_information_probe-20260901T125849Z-done.bat` | `3402F68C47E396D42C67C5A64D156F45E60C1725F1EFD559FC739E1FC1DFD437` | `test_result/logs/run_20260901T125849Z_p018a_prefix_information_probe.log`의 사용자 entrypoint | terminal·launcher PASS; `HOLD_PREFIX_INFORMATION` |
| `run_p018a_prefix_information_probe-20260901T125849Z-done.ps1` | `0A780A440C5F91C9C110CCD350BC151135FC118E849F3D7EFCBD0835B38C2BF5` | 위 BAT가 호출한 P018-A 전용 얇은 PowerShell entrypoint | common runner 전달 PASS; 재실행 금지 |

공통 `scripts/runners/run_p018_prefix_information.ps1`, 계산 source, frozen contract, result artifact와
primecount evidence는 재현성과 후속 설계 감사에 필요하므로 active 위치에 남겼다.
