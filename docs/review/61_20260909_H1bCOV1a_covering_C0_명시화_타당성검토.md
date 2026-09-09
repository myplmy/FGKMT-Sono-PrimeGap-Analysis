# H1b-COV1a 검토: covering 정리의 숨은 상수 C0 명시화

- 작성·최종 갱신: 2026-09-09 KST.
- 현재 방향: 같은 Sono 계수의 X_cert proof 사슬. 다른 방향은
  [review57의 사용자 결정](57_20260909_연구방향_세가지제안_비교검토.md)에 따라 후속 별도 연구.
- 결론: **C0=100이면 FGKMT Theorem3의 결론이 성립함을 project analytic proof로 얻었다.**
  기존 actual 입력의 smallness gate도 닫혔다. X_cert·독립 형식검증·최적성은 미주장.
- 증명 정본: [theory54](../method/theory/54_Sono_FMT_H1bCOV1a_explicit_covering_constant.md).
- machine-readable 정본:
  [COV1a contract](../method/theory/data/Sono_FMT_H1bCOV1a_covering_constant_v1.json).

## 1. 무엇을 해결했는가 — 쉬운 설명

우리는 소수가 될 수 있는 후보들을 여러 묶음으로 덮어 지우는 정리를 사용한다.
이때 앞에서 지운 후보를 피하려고 다음 묶음을 선택하면,
**큰 묶음일수록 불리해지는 선택 편향**이 생긴다.
FGKMT의 covering proof는 묶음을 뽑는 확률을 다시 조정하여 그 편향을 보정한다.

원문은 “충분히 큰 상수 C0를 쓰면 이 보정이 안전하다”는 것까지 증명했다.
하지만 C0가 얼마인지 숫자로 쓰지 않았으므로, 우리에게 필요한
“이 조건은 어느 크기부터 성립한다”는 수치 점검을 그대로 할 수는 없었다.

이번에는 보정에 필요한 나눗셈, 중복, 작은 실패확률을 하나씩 계산했다.
그 결과 **100이라는 상수 하나로 이 정리 내부의 오차를 모두 감당할 수 있음**을 얻었다.
이 100은 Sono의 계수 2×10^-17을 바꾼 숫자가 아니다.
서로 다른 역할의 상수이며 Sono 계수는 그대로다.

비유하면, 여러 안전검사 가운데 한 검사가 요구하던 “충분한 여유”를
구체적인 숫자로 바꾼 것이다. 다른 안전검사와 최종 합격조건까지 끝났다는 뜻은 아니다.

## 2. 원문을 먼저 검토했는가

그렇다. [FGKMT, DOI 10.1090/jams/876](https://doi.org/10.1090/jams/876),
[arXiv:1412.5029](https://arxiv.org/abs/1412.5029)의 출판본을 사용했다.

| 읽을 곳 | 확인한 사항 |
|---|---|
| PDF12–13 / 출판76–77, Theorem3 (4.1)–(4.11) | parameter 범위, smallness 지수, support, 모든 J와 E의 결론 |
| PDF19–21 / 출판83–85, Lemma5.1 | 정규화 Xi, 작은 분모와 정규화 1·2차 moment |
| PDF23–25 / 출판87–89 | 조건부 degree moment, 동일 index·중복 edge, codegree 비용 |
| PDF21–23 / 출판85–87 | 조건부 독립 곱, Taylor, 실패사건과 분모 전달 |
| theory54 §§2–7 | 위 정리의 모든 parameter에 대한 수치 재증명 |
| theory54 §8 및 theory53 §5 | 우리 연구의 실제 parameter를 대입하는 연결 |

이 PDF는 native text여서 먼저 문자로 읽었다. 핵심 9개 page를 원본 전체 page와
대조해 지수·분모·합 위치를 확인했다. OCR이나 새 PDF 다운로드는 없었다.
저자 primary source·arXiv를 표적 확인했지만 바로 재사용할 수치 C0를 찾지는 못했다.
따라서 기존 증명 구조를 쓰고 빠진 수치 부분을 직접 증명했다.
다른 문헌에 절대로 같은 결과가 없다는 주장이나 학술적 새로움의 확정은 아니다.

## 3. 비판적으로 확인한 핵심 위험

### 3.1 분모가 0이면 나누면 안 된다

묶음 선택의 정규화 Xi가 0 또는 너무 작으면 보정식이 불안정하다.
이번 구성은 |Xi−1|≤t^30인 사건에서만 Xi로 나누고,
그 밖에서는 그 묶음을 사용하지 않는 ∅로 보낸다.
사용하지 않은 비용도 실패율에 포함한다.
“거의 항상 괜찮다”는 말로 이 경우를 생략하지 않았다.

### 3.2 같은 index의 두 항도 독립 복사본으로 전개해야 한다

가중합 H를 제곱한 H²는 원래 같은 random edge 하나를 뽑아 제곱하는 것과 다르다.
검사에 넣은 작은 예에서는 올바른 제곱 전개 값이 **5**,
같은 draw로 잘못 합치면 **6**이 된다.
이는 실제 소수 실험값이 아니라 계산식의 구별을 확인하는 exact toy다.

### 3.3 세 집합이 겹치면 제곱 인자가 나온다

특별히 고정한 점 v 이외에 같은 점이 세 집합에 들어 있으면
해당 생존확률의 역수를 두 번 곱해야 한다.
검사 예에서는 9/4가 맞고 3/2로 계산하면 안 된다.
증명과 toy 모두 이 삼중 중복을 보존한다.

### 3.4 조건부 사건은 드물 수 있다

“E가 이전 단계에서 모두 살아남았을 때”라는 조건을 걸면,
그 사건 확률만큼 나누는 비용이 생긴다.
이 비용과 나쁜 정규화 사건의 비용을 오차 예산에 모두 포함했다.
원래 edge들 사이의 독립성을 추가로 가정하지 않았다.
새롭게 구성하는 마지막 round의 edge들만 W 조건부로 독립이다.

### 3.5 수치검사가 증명 전체를 대신하지 않는다

모든 m·D·r·A·κ·δ를 컴퓨터로 나열한 것은 아니다.
theory54에서 해석적으로 모든 범위를 증명한 다음,
남은 양의 단항식 부등식을 t=1/100의 exact rational 계산으로 확인한다.
그 환원에는 각 부등식의 단조성을 사용한다.
toy는 전개·경계·source pin 오류를 잡는 검사이며 독립 수학 심사나 Lean proof가 아니다.

## 4. 얻은 수치와 의미

증명에서 t=δ^(1/10^(m+2)), 0<t≤1/100이다.

| 항목 | 상계 | 의미 |
|---|---|---|
| 이전 단계 상대오차 | t^100 | 귀납으로 받아오는 입력 |
| 정규화 centered square | 4t^100 | Xi가 1에서 벗어나는 양 |
| 정규화 실패확률 | 4t^40 | Xi로 나누지 않고 ∅로 보낼 가능성 |
| 조건부 degree centered square | 12t^98 | 평균 degree 주변의 흔들림 |
| 고정 E의 동시 degree 실패율 | 7t^14 | E 안의 모든 점을 합친 비용 |
| 최종 상대오차 | 8t^11≤t^10 | source Theorem3가 요구한 오차 이내 |

원문 정규화 허용오차 t^(100/3)을 t^30으로 바꾸었다.
가정과 최종 결론은 같지만 인쇄된 계산을 숫자만 바꿔 복사한 것은 아니다.
**C0=100은 충분한 값일 뿐 최소값이라는 뜻은 아니다.**
C0가 커질수록 smallness 조건은 더 엄격해진다. 이번 단계에서 C0의 최적화는 하지 않는다.

실제 입력의 log gate는

\[
 \frac{a}{20\,10^{m+2}}\ge\ln100+A_{\rm hg}\{2+\ln(1/\kappa)\}.
\]

theory53의 상계와 ln100<5를 합치면 기존 보조 child
X≥2exp(10^1000)에서 성립한다. 이 지점까지 새 소수를 계산했다는 뜻이 아니며
해석적 부등식으로 확인했다. **이 X는 아직 최종 X_cert가 아니다.**

## 5. 남아 있는 일과 연구 방향

| 작업 | 남은 질문 | 이번 단계와의 차이 |
|---|---|---|
| R08 / 다음 COV2 | 필요한 구간들을 동시에 보장하는가? 예외복원·smooth remainder를 합쳐도 오차가 작은가? | 개별 moment를 최종 구간 family에 맞추는 단계 |
| R09 / PAP | 필요한 산술진행 소수 하계를 숫자와 유효범위로 쓸 수 있는가? | actual identity Hypothesis 입력과 별개 |
| R10 / UB | 두 소수가 함께 나오는 수의 상계가 필요한 모든 parameter에 균일한가? | P94와 동일 정리가 아님 |
| R11 / 계수 | 모든 실패확률·오차를 합쳐도 같은 2×10^-17을 지키는가? | 개별 child PASS만으로 대체 불가 |
| R12 / 최종변수 | 보조변수를 임의의 모든 큰 최종 X로 전달할 수 있는가? | 표본·특정 부분수열만 보장하면 불충분 |

현재 R01–R07 actual child는 project explicit이다. 남은 5개 묶음은
난이도가 서로 다르므로 “7/12 완료율”로 해석하지 않는다.
T1의 66행 중 COV-06 한 행을 EXPLICIT으로 바꾸었고,
집계는 EXPLICIT8/PARTIAL9/RATE_MISSING30/SOURCE_REVIEW_REQUIRED4/HARD_BLOCKER15다.
COV-07의 일반 wrapper는 PARTIAL, COV-08과 broad SIV-07/08/09는 HARD_BLOCKER다.

특히 예외점의 복원비 상계 8000/√b는 현재 child의 b≈2302에서 작지 않다.
따라서 “C0가 닫혔으니 모든 오차도 작다”고 결론 내리면 안 된다.
다음 R08에서 필요한 구간폭·개수·오차를 맞춘 뒤 공통 cutoff를 판단해야 한다.
지금은 이론의 연결을 채우는 것이 우선이며, 긴 prime sweep을 돌릴 이유는 없다.

## 6. 구현·검증·승인 경계

- [helper](../../source/h1bcov1a_covering_constant.py):
  최대 5개 vertex·4개 law의 exact rational 계산, product/oracle 비교,
  scalar budget·source hash·scope guard. threshold calculator나 actual runner가 아니다.
- [전용 tests](../../tests/test_h1bcov1a_covering_constant.py):
  32개 검사. 같은 index, 삼중 중복, 0분모, equality 경계, float 거부,
  support 보존과 root 오승격 방지를 포함한다.
- 전용 및 기존 관련 모듈 **146 tests PASS, 0.332초**.
- 전체 **645 tests PASS, 63.405초**, exit0. 관련 보충 59 tests PASS, 0.348초.
- Python10파일 py_compile, 본체21파일 UTF-8/AST·JSON4개·local link72개,
  source/proof pin4개 검사가 issue0으로 통과했다.
- 첫 전체 회귀에서는 과거 T1 count7/16을 현재8/15와 같다고 가정한 테스트1개가
  실패했다. 과거 계약은 보존하고 COV-06의 한 행 승격만 delta로 확인하도록
  검사를 교정한 뒤 위 전체 회귀를 다시 통과했다.
- 기존 source-pinned theory49–53·contract·actual 결과는 소급 수정하지 않았다.
- AGENTS/METHODS·T1/H1b/H1c parent overlay와 현재 상태 tests를 동기화했다.
- 새 dataset, actual prime 실험, threshold calculator, 연구 figure, GPU,
  Lean/패키지 설치, 외부 게시를 수행하지 않았다.

자동검사 PASS와 수학적 외부 인증을 구분한다.

## 7. 다음 권장 순서·예상시간·사용자 절차

| 우선 | 작업 | 이유 | 예상시간 | 사용자 수행 |
|---|---|---|---|---|
| 1 | COV2a: 실제 Sono/FMT 구간 family·폭·rounding source 대조 | 최종 목적에 필요한 양화를 먼저 고정 | 문헌·증명 검토 30–90분 예상 | 별도 수행절차 필요없음 |
| 2 | COV2b: post-covering·예외복원·smooth remainder 총 예산 | 상수는 알아도 총 오차가 작아야 함 | 1–3시간 예상; 중간 lemma에 따라 재산정 | 별도 수행절차 필요없음 |
| 3 | PAP → UB → 계수 → 최종변수 | root 의존 순서 | 앞 단계 완료 후 산정 | 별도 수행절차 필요없음 |

위 시간은 ChatGPT의 문헌·증명 작업 예상이며 PC 연산시간 또는 완료 보장이 아니다.
환경은 Windows 프로젝트 루트와 기존 PDF·FGKMT Python이다.
산출물은 새 이론문서·검사·원장·handoff이며 지금 사용자에게 실행받을 명령이나 로그는 없다.
새 자료 취득·설치·장시간 연산이 필요해지면 이유와 복사 가능한 절차를 안내하고 멈춘다.

사용자가 원한다면 이미 끝난 검사를 아래 명령으로 다시 확인할 수 있으나, 재실행은 필요 없다.

~~~powershell
Set-Location -LiteralPath 'Z:\FGKMT-Sono-PrimeGap-Analysis'
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_h1bcov1a_covering_constant -q
~~~

예상 수초, 출력은 terminal, actual 결과 폴더를 만들지 않는다.
문제가 있을 때만 전체 오류 출력을 보내면 된다.
