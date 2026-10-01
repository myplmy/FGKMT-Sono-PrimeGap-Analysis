# DEP-R09 Liu--Wang first-window 독립 audit 작업원장

- 시작: 2026-10-01 18:26 KST
- 상태: LOCALLY_VERIFIED_COMPLETE
- 기준 HEAD: 6be5f19b7f0f1dd318c16191ff15df9af98ebdbb, clean main
- 선행 정본: Theory 103--104, review 113, handoff 202610011755
- 목표: full fixed-modulus first zero-window의 conservative count를 source와 독립 scalar proof로
  검증하고, original D=160 height-weighted density transfer의 가능성을 판정한다.
- 승인: source-first 원문·학술자료 취득·문서·finite fixtures·Lean·local commit.
- 금지: actual prime/zero/dataset 계산, 설치, threshold/range calculator, 장시간 계산,
  construction law 변경, push/PR.

## 영향도

| 축 | 영향 | 통제 |
|---|---|---|
| 반복로그·end-bounded | 없음 | 정의/data/actual 실행 코드 변경 없음 |
| analytic source | 있음 | LW3.1·3.18·3.22, fixed all-character count·multiplicity 개별 확인 |
| numerical constant | 있음 | printed182/364 미전사; rational safe envelope 독립 proof |
| probability/law | 없음 | D=160·actual sieve/HG law 보존 |
| source provenance | 있음 | official PDF SHA·native text·rendered pages·correction search |
| proof evidence | 있음 | source premise와 kernel/conditional/partial tiers 구분 |
| root goal | 진행 | numerical EF/global composition 전 X_cert/calculator OPEN |

## 접근 비교

| 접근 | 정확성·재현성 | 위험·비용 | 선택 |
|---|---|---|---|
| printed table182를 그대로 채택 | primary statement지만 prose364와 불일치 | 검산·범위 누락 위험 | 채택하지 않음 |
| Eq3.22에서 actual large-log safe bound | source derivation·denominator 독립 검증 가능 | sqrt/floor/spacing source 확인 | 우선 |
| 기존 C_J만 첫 window에 사용 | 전제는 기존에 고정 | full-q coefficient가 커짐 | tail에서만 비교 |
| new numerical EF까지 즉시 주장 | 아직 scope 불일치 | unprinted multiplier 전사 위험 | 별도 source work 유지 |

## 단계

1. DONE — Git·handoff·memory·스킬·PDF SHA 확인
2. DONE — LW3.1·3.18·3.22·Lemma3.1 조건·floor·multiplicity 대조
3. DONE — conservative first-window scalar count144·Lean proof
4. DONE — cumulative count split·height-weighted full-q nonprincipal transfer
5. DONE — docs/tests/Lean/build/ledger·canonical 동기화
6. DONE — next source order·새 handoff·한국어 local commit 메시지 준비

## 완료 증거

- 새 정본: Theory105·review114·Sono_FMT_DEPR09_LW_first_window_v1.json,
  source/dep_r09_lw_first_window.py·tests/test_dep_r09_lw_first_window.py.
- Source (3.22) denominator 두 조건·actual sqrt5·safe count144를 독립 scalar proof로 검증.
- Local (3.6) floor<=2를 먼저 확인했다. Source complex identities·zero spacing·alternating
  selection·counting integrals는 partial/source/unformalized이며 local axiom을 쓰지 않았다.
- Count integral 내부 split을 사용하고 height-dependent fixed zero classes는 채택하지 않았다.
- Source LW count는 all-character, final Jutila target은 nonprincipal이라는 범위를 명시했다.
- Full-q D160의 near nonvanishing kernel<3/1000는 displayed scalar Lean PASS다.
  Principal·far·numeric EF·PAP·root X_cert는 OPEN이다.
- Canonical 문서·status notes·generated formula inventory를 동기화했다.

### 관측 명령·종료코드

~~~bash
/mnt/w/miniforge3/envs/FGKMT/python.exe -m unittest tests.test_dep_r09_lw_first_window -q
# 10 tests,0.035s,exit0
/mnt/w/miniforge3/envs/FGKMT/python.exe -m unittest discover -s tests -p 'test_dep_r09_*.py' -q
# 472 tests,5.671s,exit0
/mnt/w/miniforge3/envs/FGKMT/python.exe -m source.dep_r09_lw_first_window
# 3 pins·exact terminals·false root gates PASS,exit0
/mnt/w/miniforge3/envs/FGKMT/python.exe lean/tools/refresh_and_validate_verification_ledger.py
# final canonical edits 후 generate→validate PASS,exit0
cd /mnt/z/fgkmt-sono-primegap-analysis/lean
/mnt/c/Users/Uranus/.elan/bin/lake.exe env lean FGKMTSono/TheoryVerification.lean
# exit0
/mnt/c/Users/Uranus/.elan/bin/lake.exe build
# 8765 jobs,PASS,exit0
~~~

Inventory106 theory documents·2085 display formulas·443 declarations:
KERNEL126·CONDITIONAL142·DEFINITION231·PARTIAL196·SOURCE210·NOT_YET1175·PARSE5,
proof escape0. Whole unittest NOT RUN; historical PS5.1 failure 재판정 없음.

### 교정·도구 문제

- Status JSON insertion 초안의 중복 object와 literal '+'를 즉시 교정했다.
  json.tool 및 최종 generator→validator는 exit0. Source theorem을 약화하지 않았다.
- Canonical 다중 patch의 색인 anchor가 없어 atomic 적용이 거부됐다. 실제 latest tail과
  179번 기존 항목을 확인하고180/181로 다시 적용했다.
- WSL pdftotext·canonical fitz 없음. 기존 /usr/bin/mutool 경로를 확인했으며 설치하지 않았다.
  이는 PDF source 실패/학술 결과 실패가 아니다.
- Source family 확인에서 A/S를 nonprincipal로 명시했다. Principal은 Jutila tail에 넣지 않았다.

## 핸드오프·커밋 경계

- 실제19:55 KST의 새 handoff: handoff/202610011955_HANDOFF.md.
- 제목: DEP-R09 첫 영점 구간을 감사하고 전체 모듈러스 hybrid 상계를 검증
- 본문: LW 개별 source 조건·count144·D160 kernel·Lean tiers·정본 원장 검증을 기록하고
  numerical EF/PAP/X_cert OPEN, actual/calculator/설치/장시간/push/PR 미실행을 명시한다.
- 시작 clean main이므로 다른 선행/비소유 변경 없음. 이번 관련 변경은 모두 검토·포함한다.
- 실제 commit hash·post-commit clean 여부는 Git에서 확인한다. Raw PDF·.lake는 stage하지 않는다.
- Root 연구는 미완료이며 다음 numerical EF source audit을 계속한다.

## 현재 재개점

이번 batch는 완료했다. 새 EF 원장을 작성하고 LW pp.288--292의 actual q,T,U 조건,
primitive/imprimitive·principal·양측 good heights와 CW2 dependency부터 감사한다.
