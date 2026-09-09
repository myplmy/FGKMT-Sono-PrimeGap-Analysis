# H1b-COR3: 구간별 후보 수·주된 덮기 기여의 finite 증명 검토

- 작성: 2026-09-09 KST
- 사용자 결정: review 57에 기록한 **기존 고정 Sono 계수의 X_cert 방향 우선**을 유지
- 이번 판정: DEP-R03·R06 actual child PROJECT_EXPLICIT
- 전체 판정: R07–R12 OPEN, SIV-07/08/09 HARD_BLOCKER, X_cert OPEN
- 새 소수 실험·다운로드·설치·figure: 없음
- 증거 수준: 출판 정리의 실제 적용 + 프로젝트 해석적 증명 + bounded exact toy
  (독립 동료심사나 Lean 형식 인증은 아님)

## 1. 쉬운 설명: 이번에는 무엇을 했는가

현재 proof는 여러 단계로 후보 소수들을 걸러 낸 뒤, 남은 후보들을 잘 덮을 수 있는
구조를 만드는 방식이다. 여기서 “덮는다”는 후보를 어떤 residue class에 배정한다는
수학적 뜻이며, 실제 컴퓨터에서 소수 목록을 새로 지우는 작업이 아니다.

이번에 다룬 두 질문은 다음과 같다.

| 질문 | 쉬운 예 | 이번 결과 |
|---|---|---|
| R03: 각 구간에 후보가 얼마나 남는가? | 운동장을 미리 여러 칸으로 나눴을 때 각 칸에 남는 사람 수가 예상과 크게 다른가? | 칸의 최소 폭·칸 수·전체 실패확률을 명시 |
| R06: 특정 후보에 배정되는 덮기 기여가 너무 치우치지 않는가? | 몇 사람에게만 배정이 몰리는 대신, 대부분에게 예상한 정도의 배정이 가는가? | 평균·흔들림·중복·제외 비용을 모두 포함한 오차식 확보 |

예시는 개념 설명이다. 실제 후보들은 서로 독립인 동전 던지기가 아니며,
이번 proof도 그런 독립성을 가정하지 않는다.

지금 한 일은 X_cert 후보 숫자까지 소수를 세어 본 것이 아니다.
기존 증명 속 “오차가 작다”에 실제 사용할 수 있는 숫자식을 붙인 것이다.

## 2. 기존 문헌을 먼저 확인한 결과

| 자료 | 확인 위치 | 사용할 수 있는 부분 | 그대로 쓸 수 없는 부분 |
|---|---|---|---|
| [FMT, arXiv:1511.04468](https://arxiv.org/abs/1511.04468) | p.10 (5.7)–(5.8), p.13 Corollary 2, pp.14–16 Lemma 6.4 | local count와 main-degree의 moment 증명 구조 | 숨은 O/o 상수와 finite family의 수치 예산 |
| [FGKMT, DOI 10.1090/jams/876](https://doi.org/10.1090/jams/876) | 출판 pp.91–92, Corollary 5·Lemma 6.2 | 같은 count·second-moment 구조 | FMT 구판 인용번호를 출판본 번호로 그대로 읽는 것 |
| [Rosser–Schoenfeld 1962](https://doi.org/10.1215/ijm/1255631807) | 인쇄 p.69 Theorem 1, p.70 Theorem 7 | 명시적 prime count와 Mertens 곱 양측 경계 | 적용 범위와 곱 끝점/B0 삭제를 생략하는 것 |

이 구조를 새로 발명할 필요는 없었다. 다만 현재의 W-filtered law와 매우 큰
growing dimension을 넣었을 때 필요한 상수·폭·동시성 연결은 직접 보완해야 했다.
이는 표적 문헌 검토이며 전 세계에 동일한 결과가 없다는 novelty 판정이 아니다.

PDF는 모두 이미지로만 읽지 않았다. FMT/FGKMT는 native text를 먼저 읽고 채택 수식의
원문 페이지를 대조했다. RS는 scan-with-text-layer이므로 부등호·분수·유효범위를
원문 이미지와 대조했다. 새 OCR은 하지 않았다.

## 3. 얻은 식과 적용 조건

모든 로그는 자연로그다. 이 절의 X는 보조 sieve 변수이며,
a=ln X, b=ln a, k=floor((ln(X/2))^(1/5)),
c_aux=1/(153600 ln5)이다. c_aux를 최종 Sono 계수 2e-17과 혼동하지 않는다.
기존 child sufficient cutoff X>=2exp(10^1000)를 유지한다.

### 3.1 R03: 미리 정한 유한 구간

residue 선택 전에 정한 J개 구간 각각의 상대 폭 delta가 a^(-1/4) 이상이면

- 생존 후보 수의 기준값 80 c_aux delta Xb/a에 대한 상대오차는 1/(100b²) 이하.
- 그 중 어느 구간이라도 정해진 편차 조건을 벗어날 확률은 3Jb^6/a^17 이하
  (항상 1과의 최솟값으로 해석).
- 같은 폭의 서로소 cell들로 전체를 나누면 prime endpoint를 두 번 세거나 빠뜨리지 않는다.

상세 명제·증명은 [theory 51 §§3–6](../method/theory/51_Sono_FMT_H1bCOR3_finite_local_count_partition.md)다.
예를 들어 10칸을 사전 고정하면 한 칸 실패 상계의 10배로 전체를 상계한다.
칸들이 독립이어야 하는 계산은 아니다.
아주 작은 구간을 무제한으로 골라도 같은 보증을 준다는 뜻은 아니다.

### 3.2 R06: 같은 후보의 주된 덮기 기여

같은 p를 두 번 쓰는 모든 항을 남기고, 좋지 않은 p의 질량과 조건부 분모를
별도로 처리했다. COR2의 off-tuple 결과와 합하면 살아남은 q 중
floor(X/(ab))개를 제외하고

\[
\left|\sum_{p\in P'}\Pr(q\equiv n_p\pmod p\mid\mathbf A)-C\right|\le b^{-2}
\]

가 성립하는 실패확률은

\[
\min\left(1,\frac{1600c_{\rm aux}}{b^5}
+\frac{800c_{\rm aux}}{b^{10}}+\frac{112kb^4}{a^{11}}\right)
\]

이하다. C>(5/4)ln5와 C<400을 유지한다.
상세 명제·증명은 [theory 52 §§2–6](../method/theory/52_Sono_FMT_H1bCOR3_main_degree_finite_moments.md)다.
이것은 FMT (5.8)의 실제 입력에 대한 finite replacement이며,
보수적인 하위 조건을 최적화한 결과는 아니다.

## 4. 비판적 검토에서 보존한 안전장치

1. **q가 살아남는다는 조건:** 이를 빼면 sigma 인수가 사라져 다른 계산이 된다.
2. **cross-p는 2k점이 아니라 2k-1점:** 두 tuple의 공통 q를 한 번만 세었다.
3. **same-p는 별도 diagonal:** 서로 다른 index라도 p가 같으면 모두 포함했다.
4. **bad-P 개수와 질량은 다르다:** 적은 수의 p에 큰 가중치가 몰릴 수 있어,
   개수만으로 결론내지 않고 E[(U_p-1)²]를 써서 제거 질량을 상계했다.
5. **조건부 분모 비용:** 살아남은 조건을 건 뒤의 확률을 원래 확률과 동일시하지 않았다.
6. **finite family와 arbitrary interval:** 사전 고정 cell 사건에서 결정론적으로
   보간하되, covering 이후까지 이 보증을 옮기지는 않았다.
7. **더 강한 source rate를 주장하지 않음:** sigma에 필요한 O(b^-2)를 얻었으며,
   인쇄된 O(b^-10)를 복원했다고 쓰지 않았다.

특히 T1의 COV-01/02는 covering **이후** 단계까지 포함한다.
이번 R03은 covering **전** count이므로 T1의 해당 broad row는 RATE_MISSING을 유지한다.
이 구분 없이 둘을 함께 닫는 것은 과장이다.

## 5. 로컬 검증과 발견·보완 사항

- 전용 exact/toy와 scope 검사: 37/37 PASS, 0.085초.
- parent 포함 6 module 표적 검사: 99/99 PASS, 0.288초
  (이후 bad-P fixture를 강화해 전용 37개를 다시 통과).
- helper와 관련 시험 6파일 py_compile PASS.
- 원문·선행/신규 proof 11개 SHA-256 pin 일치.
- 전체 회귀검사 첫 시도: sandbox의 temporary directory 접근 WinError 5,
  581개/82 errors, 35.882초. 수학 오류로 분류하거나 PASS로 숨기지 않는다.
- 전체 회귀검사 정상 로컬 권한 재실행 결과는 아래 최종 검증 기록에 남긴다.

처음 bad-P fixture는 eta=1/2에서 실제 제거질량이 0이었다.
부등식은 통과하지만 제거 단계 검산이 약하므로 eta=1/10로 강화하고
양의 제거질량과 bad-P 발생을 반드시 요구했다. 이는 증명 조건 완화가 아니다.
parent MD 12/14/16의 최신 머리가 COR1 상태에 머물러 있는 점도 교정하고
상태 머리의 정합성 시험을 추가했다.

이번 검산은 실제 거대 소수를 전수생성하거나 analytic proof를 Lean으로 인증한 것이 아니다.
전체 회귀검사에는 기존 작은 fixture의 임시 그림 생성도 포함되지만 신규 연구 figure는 없다.

## 6. 지금도 남은 일

| 다음 의무 | 아직 필요한 이유 |
|---|---|
| R07 full hypergraph | 크기·parameter 범위·subset 보존과 수치 실패율 전체를 연결해야 함 |
| R08 simultaneous covering | covering 후 partition·smooth remainder·rounding을 다시 합쳐야 함 |
| R09 numerical PAP | 현재 닫힌 identity Hypothesis와 동일한 정리가 아님 |
| R10 numerical two-prime UB | determinant·예외 prime까지 uniform한 finite bound 필요 |
| R11 전체 예산 | 각 단계 오차를 같은 Sono 계수 2e-17에 맞춰 한 번에 합쳐야 함 |
| R12 최종변수 전달 | 보조 X에서 모든 큰 최종변수로 넘어가는 선택 규칙 필요 |

R01–R06을 닫았다는 것은 50% 완료라는 의미가 아니다. 여섯 남은 작업의 난도가
동일하지 않고, 하위 lemma가 더 필요할 수 있다. 특히 R07은 이번 C나 main-degree
한 식만 만족한다고 자동으로 통과하는 문이 아니다.

## 7. 권장 순서·시간·사용자에게 필요한 일

| 우선순위 | 작업 | 권장 근거 | 예상 시간 |
|---|---|---|---|
| 1 | H1b-COV1: R07 원문·실제 parameter/subset/failure inventory | 이제 필요한 확률 입력이 모였으므로 다음 연결부를 정확히 분해 | ChatGPT 문헌·수학 감사 1–3시간의 작업 예상, 완료 보장 아님 |
| 2 | R07 finite proof의 명시적 child를 순차 정식화 | 인쇄된 sufficiently large와 uniform o(1)을 숫자로 바꾸는 핵심 | source inventory 후 재산정; 지금 총시간 약속 불가 |
| 3 | R08→R09→R10→R11→R12 | 기존 root 순서 유지; 최종 모든 양화·계수 확인 | 각 선결 의무가 닫힌 뒤 산정 |
| 보조 | 새 child의 exact toy·회귀검사 | 수식 연결·상태 과장·구현 실수 방지 | 전용 수초 이내, 현재 전체 약 1분 예상 |

사용자: **별도 수행절차 필요없음**. 현재 새 자료, 설치, Lean, 추가 Python library,
장시간 CPU 실행을 요청하지 않는다. 다음 단계에서 정말 필요해지면 필요한 이유·환경·
정확한 명령·시간·회신 내용을 안내하고 해당 지점에서 멈춘다.
소수 범위를 늘리거나 coefficient 연구로 전환하는 일은 별도 후속 연구로 유지한다.

## 8. 재현성·작업 방법

적용한 스킬은 [impact-analysis](../../.agents/skills/impact-analysis/SKILL.md),
[plan-doc](../../.agents/skills/plan-doc/SKILL.md),
[session-handoff](../../.agents/skills/session-handoff/SKILL.md),
[pr-workflow](../../.agents/skills/pr-workflow/SKILL.md)와 PDF 판독 스킬이다.
이에 따라 actual 승인 범위를 넓히지 않고, PDF를 유형별로 대조하고,
과거 hash-pinned proof는 보존하면서 successor와 현재 상태를 연결했다.
작업원장: ai_dev_tool/work_ledgers/202609092205_H1BCOR3_WORK_LEDGER-done.md.

### 최종 검증 기록

- 정상 로컬 권한 재실행: **581/581 PASS**, 68.569초, exit 0.
  기존 sandbox의 82 errors와 분리해 기록한다.
- dedicated 37/37 PASS, 0.085초; 기존 COR1/COR2 contract/source pin도 유지됐다.
- 이번 본체 18파일 UTF-8·4 JSON·78개 local link 검사 issue 0,
  연구 helper/관련 시험 6파일 py_compile PASS.
- 현재 수학적 결론은 프로젝트 해석적 증명이며, 전체 회귀 PASS를 독립 심사나
  최종 X_cert의 인증으로 승격하지 않는다.
