# P014-R2 실패 교정·P018 prefix 정보율 준비 작업로그

- 시작: 2026-09-01 00:13 KST
- 사용자 결정: P018 full-range 균형형 B 승인, 탐색형 A는 prefix-only 보조 gate 승인
- 사용자 승인: P014-R2 실패 원인분석·수정, P018 prefix runner 설계
- 금지: Codex가 P014-R3 actual 또는 P018 prefix actual을 직접 실행하지 않음

## 단계 현황

1. **완료 — 최신 handoff·Git 상태·P014-R2 원본 실패 로그 감사**
   - 시작 worktree clean 확인
   - 실패 log SHA-256:
     `beb57218a5d8403686c31f925d809b2bc37a5a20daf052486b659acc3eb77f3b`
   - 첫 resource preflight 전에 종료, result directory·progress JSONL 생성 0
2. **완료 — 실패 원인 재현·영향 범위 확정**
   - Windows PowerShell 5.1 native argument binder가 raw JSON argv의 큰따옴표를 제거
   - Python broker가 `[-B,-m,...]`를 받아 `JSONDecodeError` line 1 column 2
   - 과학 계산·certificate·saved verification은 시작되지 않음
3. **완료 — P014-R3 live broker 인자 전달·오류 로깅 교정**
   - Base64 UTF-8 JSON transport와 broker 자체 오류의 main-log 즉시 append 구현
   - 실제 Windows PowerShell 5.1 quote-sensitive argv 회귀시험 포함 6/6 PASS
   - 실행된 R2 BAT/PS1은 SHA-256 보존 후 `test_done` 이관
   - R3와 R2의 과학 인수는 동일하고 revision·transport·회귀시험만 변경됨을 diff로 확인
   - R3/P018 BAT 승인 플래그 누락 시 exit 1·신규 log 0건 확인
4. **완료 — P018 A-prefix/B-full frozen decision contract·영향도 문서**
   - B는 full-range 정식 gate, A는 prefix-only 보조 gate로 역할 분리
   - P0 calibration, A frozen prefix, B reference-only endpoint와 해석 한계 고정
5. **완료 — P018 prefix 구현·toy·runner·approval denial 검증**
   - blinded margin-only gate, WSL exact primecount handoff, 서로소 dual partition 구현
   - 12시간 deadline에서 대기 segment 취소·실행 중 segment 안전 회수 규칙 추가
   - P014/P018 targeted 최종 25 tests는 샌드박스 외부에서 PASS
   - PowerShell parser·Python compile·WSL `bash -n` PASS
6. **완료 — 계획·결과 색인·AGENTS·실패 분석보고서 갱신**
   - P014-R2 실패 provenance, R3 불변 계약, P018 B-full/A-prefix 결정과 사용자 절차 반영
   - `test_result/00_실험결과_분석보고서_색인.md`에 최신 실패·로컬검증 문서 연결
7. **완료 — 전체 검증·신규 timestamp handoff·최종 보고 준비**
   - 전체 unittest 최종 197/197 PASS, 28.263초
   - active 변경 PowerShell parser 5/5, changed Python `py_compile`, `git diff --check` PASS
   - sandbox WSL service `E_ACCESSDENIED` 뒤 동일 `bash -n` 외부 재실행 exit 0 PASS
   - 신규 handoff: `handoff/202609010135_HANDOFF.md`

## 재개 규칙

- 첫 미완료 단계부터 계속한다.
- R2 실패를 P014 수학 알고리즘 실패로 표현하지 않는다.
- P018 prefix는 정보율 probe이며 enrichment 검정이나 full B gate PASS로 표현하지 않는다.
- actual 실행은 사용자 명령으로만 수행한다.
