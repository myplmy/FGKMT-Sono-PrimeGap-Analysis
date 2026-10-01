# DEP-R09 actual native primorial·D=160 budget 작업원장

- 시작: 2026-10-01 15:10 KST
- 현재 상태: PROOF_BATCH_COMPLETE_LOCAL_COMMIT_READY
- 기준 HEAD: a33c8f210c1d92b1dada986253422dc5e4b3cb7d, clean main
- 선행 정본: Theory 49·88--90·103, review 112, handoff 202610011445
- 사용자 목표: numerical X_cert 전의 필요한 정규화·source-first 증명 진전
- 승인: source audit·학술자료 다운로드·문서·finite fixture·Lean·local commit
- 금지: actual prime/zero/dataset 실험, 설치, calculator/range search, 장시간 계산,
  construction law 변경, push/PR

## 목적과 완료조건

Fixed raw Pprime과 S에서 B0를 제외한 actual CRT support를 원문 대조하고
f의 primorial split 및 native exponent 범위를 증명한다.
원래 outer D=160을 보존한 actual regime에 Theory 103의 kernel budget을 연결한다.
d_f>=333을 필요조건으로 강제하거나 numerical EF constant를 임의 지정하지 않는다.

## 영향도

| 축 | 영향 | 통제 |
|---|---|---|
| 반복로그·end-bounded | 없음 | 정의·dataset·실험코드 변경 없음 |
| actual law·native modulus | 있음 | raw Pprime versus P(A), S/B0/CRT 원문 확인 |
| source provenance | 있음 | exact registry locator·hash·printed page 대조 |
| 수치 | 제한적 | product partition·supplied finite sets·rational/exp proof; actual X 미생성 |
| 승인 | 기존 범위 | D=160·law 보존, actual/설치/remote 없음 |
| proof·정본 | 있음 | analytic source와 finite kernel/conditional/partial 구분 |
| goal | 진행 | calculator·X_cert는 모든 critical leaf가 닫히기 전 OPEN |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 선택 |
|---|---|---|---|
| actual primorial split + D=160 budget | actual definitions를 직접 보존 | B0 위치·endpoint를 빠뜨리지 않아야 함 | 우선 |
| outer D 변경으로 d333에 맞춤 | parameter capacity 재증명 필요 | 현재 law/계수 변경 및 충분조건 강제 위험 | 이번에는 채택 안 함 |
| 새 joint-angle source | direct phase theorem 가능 | 큰 analytic proof 필요 | 실제 baseline budget 판정 뒤 |

## 단계

1. DONE — 최신 Git·handoff·memory·스킬 확인
2. DONE — FMT raw S/P/B0와 actual potential coordinates 원문 대조
3. DONE — exact prime-product·power cutoff·314<d_f<323 native regime 증명
4. DONE — actual real-zero gap·nonvanishing<1/36·parameterized total 3% budget
5. DONE — Theory 104·review 113·finite tests·Lean·전수 원장·정본 동기화
6. DONE — next source scope·timestamp handoff·한국어 commit 메시지 준비

## 현재 재개점

Proof·검증·정본·새 handoff가 완료됐다. 정확한 done 경로로 이동하고 최종 링크/whitespace를
검사한 뒤 이번 관련 파일만 local staging·한국어 commit한다.

## 2026-10-01 17:47 KST 검증과 진전

- Actual fixed raw Pprime을 good subset P(A)로 바꾸지 않았다.
- f divides P(X/2), B0 lower/inner/no-exception cases·closed X/2 endpoint를 증명했다.
- Original D=160의 314<d_f<323으로 d333 conditional branch의 baseline 적용을 배제했다.
- Actual full-primorial real gap을 보존해 real exponential budget<1/36을 증명했다.
- Numerical K_EF는 null로 보존했다. Symbolic vanishing gate에서 total CF<3/100이다.
- Density common log cutoff<30000은 source components로 확인했다; entire source theorem의
  Lean formalization으로 승격하지 않는다.

| 명령/대상 | 실제 결과 |
|---|---|
| native+adjacent finite tests | 22건·0.015s·exit 0 |
| discover test_dep_r09_*.py | 462건·6.335s·exit 0 |
| source.dep_r09_native_primorial_baseline | 6 source pins·rational terminals PASS |
| lake env lean TheoryVerification.lean | strengthened proof exit 0 |
| lake build | 8765 jobs·exit 0 |
| refresh_and_validate_verification_ledger.py | generate then validate PASS·exit 0 |

Inventory: 105 documents·2066 display식·432 declarations,
KERNEL121·CONDITIONAL141·DEFINITION227·PARTIAL192·SOURCE209·NOT_YET1171·PARSE5,
proof escape0. Global correlation·PAP·X_cert는 OPEN이다.

## Source 취득·미채택

Official Liu--Wang 2002 PDF 33쪽을 primary endpoint에서 직접 다운로드했다.
Path: tmp/pdfs/depr09_ef_lw_20261001/Liu_Wang_2002_explicit_psi.pdf
SHA: 50c6b5d628a07cfb216078571a846ef658aa7db29515d21bb8dbb4f20dc5055d
Theorem8 q<=log(N)^6,T=log(N)^15는 current regime에 그대로 못 쓴다.
Theorem4 source table는 후보이나 p278 prose 364와 p279 Table5 182가 다르므로 미채택.
Eq.(3.22)를 conservative bound로 독립 감사해야 한다.
Downloaded PDF는 ignored source cache에 보존하며 Git에 raw PDF를 stage하지 않는다.

## 실패·복구·비실행

- 초기 Lean compile: unknown Finset erase lemma, explicit x API argument 누락.
  같은 statement를 유지하고 simp/정확한 named argument로 교정; 이후 exit 0.
- 일부 path lookup/regex 실패는 canonical file list/fixed-string으로 복구했다.
- Full unittest suite는 미재실행; historical PowerShell5.1 failure는 수정/재판정하지 않았다.
- Actual prime/zero/dataset·calculator·install·long computation·push/PR은 NOT RUN.
- No academic novelty or bounded X_cert range is claimed.

## 마감 체크

- [x] Actual raw-coordinate source·B0/endpoint·power geometry 대조
- [x] Native 314<d_f<323·real exponential/vanishing budgets 검증
- [x] Source/kernel/conditional/partial boundaries와 unknown K_EF 보존
- [x] Canonical docs·inventory·verification ledger 동기화
- [x] handoff/202610011755_HANDOFF.md 작성, 2026-10-01 17:55 KST actual time 사용
- [x] Related tracked/untracked files 확인, pre-existing other changes 없음
- [x] Raw/ignore-cr-at-eol numstat 일치, EOL-only normalization 없음
- [x] Actual 실험·calculator·install·long compute·remote mutations 미실행

Completion marker는 이 proof batch만 뜻하며 전체 X_cert goal 완료가 아니다.
Local commit hash와 clean 여부는 commit 뒤 git log/status로 확인한다.
