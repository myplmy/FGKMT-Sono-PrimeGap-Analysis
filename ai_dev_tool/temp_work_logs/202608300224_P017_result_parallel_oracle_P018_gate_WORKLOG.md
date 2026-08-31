# P017 결과감사·병렬 oracle revision·P018 gate 검토 작업로그

- 시작: 2026-08-30 02:24 KST
- 입력: P017 combined queue terminal PASS 회신
- 사용자 승인:
  - P017 결과 분석
  - PowerShell 실시간 표시 권장안 교정
  - serial 정답표 없는 범위의 병렬 계산 가능성 검토와 타당한 경우 구현·toy
  - P018 gate 후보 3안·문헌 비교
- 실제 heavy/새 actual: 사용자 추가 승인 전 실행하지 않음

## 단계 현황

1. **완료 — P017 queue·A/B child terminal/manifest/saved/exact equality 감사**
   - queue terminal PASS, FAIL 0, traceback 0
   - A/B manifest 전 산출물 SHA-256 독립 재계산 일치, saved report issue 0
   - A: 32 segments/31 boundaries, serial checkpoint·analysis와 exact equality
   - B: 64 segments/63 boundaries, serial/parallel statistics·checkpoint·fixed-seed inference exact equality
   - B 동일 구간 serial 12,598.410초, parallel phase 2,866.160초, 관측 wall-time 비 약 4.396배
2. **완료 — P017 완료 실행기 test_done 이관과 결과보고서·색인 갱신**
   - 결과 정본: `test_result/202608300229_P017_parallel_calibration_result_analysis.md`
   - P017 계획 상태·결과 색인 갱신
   - root BAT 3개와 experiment PS1 3개를 timestamp `-done`으로 이관, 전후 SHA-256 일치
3. **완료 — .NET 없는 동일 PowerShell 실시간 표시 방식 비교·권장 구현**
   - `scripts/common/live_native_tee.py` + `Invoke-LiveLoggedNativeStage` 구현
   - P014-R2의 4개 stage를 live broker로 전환; 수학 계산 인자·backend 불변
   - stdout/stderr/빈 줄/nonzero exit toy 3/3 PASS, PowerShell 직접 통합 self-test PASS
   - 첫 sandbox test는 `%TEMP%` 권한 `PermissionError`였고 허가된 외부 FGKMT 실행 3/3 PASS
4. **완료 — serial 정답표 없는 병렬 계산의 검증 구조 영향도 분석**
   - 한 번 병렬은 기각; 서로소 segment 수의 full parallel dual-pass + independent pi difference 권장
   - P017-B 실측 기반 예상 약 1.59시간, serial+parallel 대비 약 2.70배 단축 후보
   - shared sieve/accumulator common-mode risk를 독립 oracle로 과장하지 않도록 문서화
5. **완료 — 적합한 revision 계획·코드·toy 검증**
   - P019 계획·impact 문서·`parallel_dual_partition.py`·tests 구현
   - `[100,200)` primary 8/verifier 11 segments, worker 4, exact gap count 21
   - exact equality·잘못된 count 거부·partition gate 3/3 PASS (실제 test runtime 3.970초)
   - actual P013 future runner는 P018 HOLD 때문에 만들지 않음
6. **완료 — P018 gate 의미·민감도·선행연구 근거·3후보 작성**
   - 일반 통계 근거(Cohen power, Holm multiple testing, ASA threshold 경고)와 prime-gap 문헌 분리
   - 탐색형 A·균형형 B·확인형 C 수치화; B를 full-range gate 권장, A는 prefix-only 후보
   - P013-B에서 세 후보 모두 HOLD; B power target은 null expectation 약 11.2691·현재의 약 168.7x
   - discrete Poisson power requirement 함수·회귀시험 추가, targeted 5/5 PASS
7. **완료 — AGENTS·계획·색인·신규 handoff·최종 감사**
   - P017 정본 결과·done hash, P014/P018/P019 로컬검증 보고서와 색인 갱신
   - AGENTS·실행로그 규약·방법론 색인·P014/P017/P018 계획 정합화
   - 최종 전체 unittest 184/184 PASS, parser 11/11, approval denial·diff check PASS
   - P017 완료 실행기 6개 활성 경로 부재·`test_done` SHA-256 일치·A/B/queue 산출물 존재 재확인
   - P014-R2·P019 actual 산출물 부재 확인; 과거 핸드오프의 당시 진행 상태는 역사 기록으로 유지
   - 전체 재귀 감사는 기존 접근불가 `tmp/p010b-cover-test-l28v4y4g`에서 중단되어, 해당 경로를
     변경하지 않고 정본·tracked 작업경로만 대상으로 다시 감사해 PASS
   - 신규 handoff: `handoff/202608300254_HANDOFF.md`

## 재개 규칙

- 첫 미완료 단계부터 이어간다.
- P017 PASS는 terminal marker와 두 child exact equality·saved report를 직접 확인한 뒤 확정한다.
- 병렬 계산 자체를 serial 독립 검증으로 오해하지 않는다. serial oracle이 없으면 별도 독립
  verification 구조를 먼저 설계한다.
- Poisson gate는 planning proxy이며 실제 stratified-hypergeometric power라고 쓰지 않는다.
