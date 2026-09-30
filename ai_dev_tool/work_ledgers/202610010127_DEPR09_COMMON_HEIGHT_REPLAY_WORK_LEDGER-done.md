# DEP-R09 공통 높이 explicit-formula replay 작업원장

- 시작 상태 확인: 2026-10-01 01:27 KST
- 기준 HEAD: <code>3a78356</code>, clean main
- 현재 상태: PROOF_BATCH_COMPLETE_LOCAL_COMMIT_READY
- 선행 정본: Theory 71, 94--96, 101, review 110, handoff 202609291722
- 목표: \((X,U]\)의 두 끝점에 같은 \(T\)를 사용해 low-zero 정규화 항과 principal channel을 정확히 소거하고, signed zero sum과 remainder의 실제 budget을 분리한다.
- 승인: 원문 감사·학술자료 다운로드·문서·유한 fixture·Lean 검증·로컬 커밋.
- 유지 경계: actual prime/zero 계산·threshold calculator·설치·장시간 계산·push/PR 없음.

## 영향도

| 축 | 영향 | 근거·통제 |
|---|---|---|
| 수학·반복로그 | 있음 | Theory 101의 correction을 같은 \(T\), 같은 character convention에서 전개 |
| end-bounded·dataset provenance | 없음 | 데이터 코드·산출물에 접근하지 않음 |
| source provenance | 있음 | TZ official v2 TeX/PDF의 식 (4.2) 직전 식 대조 |
| 큰 정수·수치 | 제한적 | 실제 \(X,f,U\)는 만들지 않고 exponent·유리 대수만 검사 |
| 승인 | 기존 범위 | construction law는 바꾸지 않음 |
| 검증·문서 | 있음 | 유한 centered mask, complex character orientation, source/premise 상태 분리 |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 선택 |
|---|---|---|---|
| endpoint마다 다른 높이 | 잔여 zero shell이 새로 생김 | normalization constant도 다를 수 있음 | 비교 경계 |
| character별 absolute upper를 먼저 합성 | source와 쉽게 연결 | Theory 101 phase 정보 소실 | 재사용하지 않음 |
| 공통 \(T\)에서 centered residue projection | low constant와 principal이 exact cancellation | analytic EF constant는 계속 source 의무 | 채택 |

## 단계

1. DONE — 현재 Git·handoff·스킬 및 primary source locator 확인
2. DONE — primary bracket·canonical prime-power congruence·regularizer 대조
3. DONE — centered exact L1·complex interval bound·T=f^(3/2) correction
4. DONE — Theory 102·review 111·source pins·finite tests·Lean·전수 원장
5. DONE — 202610010221 handoff·정본 동기화·한국어 commit 메시지 준비

## 2026-10-01 02:21 KST 완료 증거

- 정본: Theory 102·review 111·machine ledger, finite helper/tests.
- Source: TZ printed p.9 rendered image와 official native TeX 대조; PDF·TeX hash 일치.
- Convention: p^k congruence, common characterwise regularizer, possible real zero 보존.
- Mathematical result: exact mask L1·principal annihilation·common-height replay,
  \(T=f^{3/2}\) parameterized correction. Numerical K_EF·signed gate·X_cert는 OPEN.
- Correction: Theory 100 floor는 T=f^5 한정; Theory 101 angle은 sufficient certificate.
- Canonical synchronization: AGENTS, METHODS, theory/review indexes, T1, Lean README,
  status·inventory·generated verification ledger.

| 검증 명령/대상 | 실제 결과 |
|---|---|
| canonical Python: tests.test_dep_r09_common_height_replay | 9건·0.020s·exit 0 |
| canonical Python: discover test_dep_r09_*.py | 신규 포함 440건·9.934s·exit 0 |
| Theory 100·101 historical tests | clarification 뒤 17건·exit 0 |
| tests.test_lean_formula_inventory_order | 2건·exit 0 |
| python -m source.dep_r09_common_height_replay | source pins 4건·rational terminals PASS |
| lake env lean FGKMTSono/TheoryVerification.lean | 강화된 finite complex theorem·exit 0 |
| lake build | 8765 jobs PASS·exit 0 |
| refresh_and_validate_verification_ledger.py --repo-root . | generate then validate PASS·exit 0 |
| git diff --check | exit 0 |

Python은 /mnt/w/miniforge3/envs/FGKMT/python.exe,
Lean은 lean/ cwd의 /mnt/c/Users/Uranus/.elan/bin/lake.exe를 사용했다.
Live Lean 4.34.0-rc2·kernel 6a10ac8c22beadecabdbb0919c2b50214762f91d를 관측했다.
설치·업그레이드 없음.

Inventory: theory 103개·display 2018식·declaration 396개.
KERNEL_PASS 108·CONDITIONAL 134·DEFINITION 223·PARTIAL 181·SOURCE 203·
NOT_YET 1164·PARSE_REVIEW 5·proof escape 0.
식 102.7은 generic finite replay만 증명했으므로 PARTIAL_FORMALIZATION이다.

실패·복구:

- 최초 Lean compile은 indicator distributivity·expanded sum syntax에서 FAIL했다.
  정리 statement를 유지하고 ring/finite-sum calc로 수정한 뒤 direct compile과 build PASS.
- 일부 multi-file patch는 context 불일치로 적용 전에 거부됐다. 파일별 context를 확인해
  다시 적용했으며 partial edit 또는 source 결과 유실은 없다.
- Whole-project suite는 이번에 NOT RUN. 이전 PowerShell 5.1 LASTEXITCODE failure를
  재현·수정하거나 whole-project PASS로 바꾸지 않았다.

## 현재 재개점

이번 batch의 증명·검증·정본·handoff는 완료했고 정확한 완료 원장 경로로 이름을 바꿨다.
마감 링크·whitespace를 재검증한 뒤 이번 관련 파일만 local staging·한국어 commit한다.
다음 proof batch는 새 원장과 함께 \(Q=f,T=f^{3/2}\)의 finite density prerequisites부터 시작한다.

## 완료 전 점검

- [x] 요청된 pre-absolute replay·correction 정규화 완료
- [x] source/finite/kernel 증거 수준 구분
- [x] actual 실험·calculator·설치·장시간 계산·push/PR 비실행
- [x] canonical 문서·전수 원장 동기화
- [x] handoff/202610010221_HANDOFF.md 작성
- [x] 선행 다른 변경 없음·이번 관련 파일만 검토
- [x] git diff --check·source pins·local references 검사
- [x] 정확한 원장 경로의 완료 이름 변경

Git 확정 hash와 최종 clean 상태는 같은 변경을 commit한 뒤 git log/status로 확인한다.
이 완료 표시는 Git commit 또는 전체 DEP-R09 성공 판정을 대신하지 않는다.

## 환경 사건

기본 sandbox exec는 shell process 생성 전에 ENOENT로 실패했다. 같은 읽기 전용
명령을 승인된 실행 경로에서 호출해 repository 접근을 확인했다. Toolchain 설치·변경은 없다.
