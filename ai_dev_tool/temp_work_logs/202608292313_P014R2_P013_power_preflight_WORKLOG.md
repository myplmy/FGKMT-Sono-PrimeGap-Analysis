# P014-R2 actual 승격·P013 power preflight 작업로그

- 시작: 2026-08-29 23:13 KST
- 사용자 승인:
  - P014-R2 toy에 문제가 없으면 actual 승격
  - P013 expected-information/power preflight 설계 착수
- 현재 보호 대상: P017 combined queue actual 진행 중
- 금지: P017 process·active 산출물 변경/이동/해시 고정, P014/P013 신규 actual 실행, CPU-heavy 검증

## 단계 현황

1. **완료 — P017 read-only 진행상태·로그 관찰 경로 확인**
   - P017-A child PASS, queue event elapsed `709.687s`.
   - P017-B serial oracle 진행 중; `progress.jsonl` 갱신 확인.
   - 바깥 PowerShell 무출력은 stage capture 구조상 정상이며 Python live log는 정상 동작.
   - P017-B 저 CPU는 `serial_oracle_started` 뒤 단일-stream `_serial_accumulate` 단계라 정상.
     progress가 `1.95e11`, 1,900 chunks까지 단조 증가했으며 serial 완료 뒤 8-worker parallel로 전환 예정.
2. **완료 — P014-R2 toy 증거·현재 actual 구현·승격 영향도 감사**
   - 기존 8-worker modulus-30030 exact equality·무누락 증거가 actual 승격 gate를 충족.
   - analysis 병렬, saved full recomputation serial oracle 분리 방식을 채택.
3. **완료 — P014-R2 actual 계획·코드·runner 구현**
   - 별도 P014-R2 plan/BAT/PS1, parallel backend·manifest revision·parent progress 구현.
   - actual은 P017 종료 뒤 사용자만 실행; 현재 미실행.
4. **완료 — P013 expected-information/power preflight 계획·코드/toy 구현**
   - P018 계획·read-only loader·Poisson screening proxy·toy 4 tests 구현.
   - P013-B 판정 `HOLD_NEXT_RANGE`; formal hypergeometric power는 미인증.
5. **완료 — 비경합 정적검증·문서·색인·AGENTS 갱신**
   - 경량 tests 9 PASS(outside sandbox), progress callback 1-worker toy PASS, py_compile PASS,
     P014-R2 PS1 parser·BAT approval gate PASS.
   - P013-A/B 사용자 figure QA PASS를 결과보고서·계획·색인에 반영.
6. **완료 — 신규 timestamp handoff·최종 감사**
   - `handoff/202608292333_HANDOFF.md` 신규 작성.
   - P017은 active 상태 그대로 유지; P014-R2/P018 actual 미실행.

## 재개 규칙

- P017이 진행 중이면 multiprocessing·full unittest·actual prime/certificate 계산을 실행하지 않는다.
- 첫 `진행 중` 또는 `대기` 단계부터 이어간다.
- P014-R2는 serial exact equality·constraint 무누락·saved verifier 독립성을 보존해야 한다.
- P013 power preflight는 사후 pooling이나 새 과학 결과가 아니라 P013-C 착수 전 계산가치 gate다.
