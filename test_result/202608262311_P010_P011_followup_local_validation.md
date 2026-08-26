# P010/P011 후속 구현 로컬검증

## 판정

`LOCALLY_VERIFIED / FULL_UNITTEST_PASS / ACTUAL_P009_P010_NOT_RUN`

검증 기준 commit은 `926887466816794e35259679ef8f692522397f81`이며, 아래 검증은 이번
작업의 미커밋 변경을 포함한다. 연구 계산 Python은
`W:\miniforge3\envs\FGKMT\python.exe` 3.11.16만 사용했다.

## 구현 범위

- modulus 배수 exact-lift 정수 potential mapping
- modulus-30030 5,760 states·35,224,647 constraints memory-safe exact scanner
- signed-int64 overflow 사전 guard와 full-matrix 비생성 계약
- P010B saved verification의 manifest hash binding
- 조건부 P010A exact-lift PowerShell runner
- P010B→조건부 exact lift→독립 P009 순서의 orchestration-only queue
- 총 wall 15시간 30분, decimal 50 GB(50,000,000,000 bytes) 증가량 cap
- child 실패 뒤 독립 child 계속, 마지막 aggregate nonzero
- disk accounting 권한 오류 fail-closed

## 검증 결과

| 검증 | 결과 |
|---|---|
| `py_compile` 7개 변경 Python 파일 | PASS |
| 활성 PowerShell 9개 parser | 9/9 PASS |
| 전체 unittest | 106/106 PASS, 5.372초 |
| queue/정수 lift targeted tests | PASS |
| queue 승인 flag 없음 | exit 1, output directory 미생성 |
| exact-lift 승인 flag 없음 | exit 1, output directory 미생성 |
| queue PowerShell confirmation 없음 | exit 1 |
| P010A saved exact 재검증 | PASS, issue 0, `exact_recomputed=true` |
| P011 saved deterministic 재검증 | PASS, issue 0 |
| `git diff --check` | PASS; line-ending warning만 존재 |

처음 sandbox 내부 TEMP에서 unittest를 실행했을 때 Windows ACL 때문에 네 임시 폴더의
쓰기/삭제가 거부됐다. 같은 fixed Python 테스트를 사용자가 허가한 정상 Windows 권한
경로에서 다시 실행해 106개 전부 PASS했고, 문제의 임시 폴더는 검증된 프로젝트 `tmp/`
경로 안에서만 제거했다. 따라서 해당 오류는 코드 회귀가 아니라 sandbox TEMP 권한
문제다.

검증 시점 기존 `test_result/` 약 0.006 GB, `tmp/` 약 0.054 GB였고 Z: free space는
약 277.449 GB였다. 이는 향후 50 GB 사용 허가가 아니라 queue 시작 전 환경 참고값이다.

## 실행하지 않은 것

- P010B modulus-30030 full floating scan
- P010A modulus-30030 exact lift actual
- P009 `10^20` single-block actual
- modulus-30030 cutting-plane LP
- P012 local/nonstationary null

위 항목 중 앞의 세 개만 사용자 실행 queue에 들어 있다. cutting-plane은 G3 실측 전에는
타당한 iteration/time bound가 없어 제외했고, P012는 null 설계를 사전 고정하지 않아
제외했다.
