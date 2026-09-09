# 2026-09-09 H1b-COR1 타당성 검토·X_cert 진행현황 갱신

## 1. 결론부터

H1b-DEP에서 남긴 12개 작업 중 **R01 correlation, R02 조건부 희소성, R04 good-P 확률**을
이번 project finite proof로 닫았다. 실제 small-codegree 입력도 공급했다.
남은 것은 **9개 작업 묶음**이며, 전체 X_cert는 계속 OPEN이다.
12→9를 연구 완료율이나 남은 시간의 비율로 해석하면 안 된다.

정본 증명은 [theory 49](../method/theory/49_Sono_FMT_H1bCOR1_finite_correlation_conditioning.md),
machine-readable 상태는 [COR1 successor](../method/theory/data/Sono_FMT_H1bCOR1_finite_correlation_v1.json)다.
[theory 48](../method/theory/48_Sono_FMT_H1bDEP_actual_dependency_map.md)와
[직전 진행현황](54_20260909_H1bDEP_Xcert_진행현황_의존성감사.md)은 당시 12개 OPEN의 이력으로 보존했다.

## 2. 무엇을 증명했는가 — 쉬운 설명

소수 후보를 걸러내는 체를 생각하자. 각 작은 소수마다 제거할 나머지 한 가지를 무작위로 고른다.
한 점이 남을 확률을 sigma라 하더라도, 여러 점이 모두 남을 확률이 무조건 sigma의 거듭제곱은 아니다.
서로 같은 나머지를 갖는 점들이 있기 때문이다.

### 2.1 점들이 서로 얽히는 오차 — R01

기존 논문은 이 차이가 매우 작다고 증명하지만, 우리가 필요한 것은 **숫자가 들어간 오차식**이다.
동일한 나머지를 가진 점들의 쌍을 세어, 실제 입력 범위에서
\[
 \left|\Pr(\text{t점 모두 생존})/\sigma^t-1\right|
 \le 2/(\ln X)^{17}\le 1/(\ln X)^{16}
\]
을 얻었다. 출판 논문의 증명 구조를 사용한 수치 명시화이지,
수많은 실제 소수를 새로 세어 관찰한 결과가 아니다.
서로 다른 점에만 적용하며, 같은 점을 두 번 적었다고 독립 사건으로 취급하지 않는다.

### 2.2 살아남았다는 조건을 걸 때 확률이 커지는 문제 — R02

어떤 사건의 확률이 원래 1/4인데, 전체 경우 중 절반만 남기는 조건을 걸면
조건부 확률은 1/2로 커질 수 있다. 따라서 원래의 작은 확률 상계를 그대로 복사하면 안 된다.

Rosser–Schoenfeld의 기존 정리에서 sigma의 하계를 얻어, 생존확률로 나누는 비용을 포함했다.
그 결과 같은 residue로 들어갈 확률은 X^(-3/5) 이하로 제한된다.
이전 DEP에서 조건부로 남겨 둔 “두 점을 같은 묶음에 넣는 확률”도 이 입력으로 닫혔다.
다만 이것 하나로 전체 covering 정리가 완성되는 것은 아니다.

### 2.3 체가 좋지 않게 뽑힐 확률 — R04

무작위 체를 고르면 일부 소수는 예상과 다르게 행동할 수 있다.
그런 bad 소수가 X/(ln X)^4개보다 많아질 확률을
\[
 7/(\ln X)^8
\]
이하로 제한했다. 두 독립 copy에서 점이 겹치는 비용과,
평균이 정확히 1이 아닌 오차를 모두 포함했다.
소수 p들 사이의 독립성을 가정하지 않고 선형기댓값과 Markov 부등식을 사용했다.

이 결과들은 독립 심사·Lean 인증을 받은 새 출판 정리가 아니라,
명시된 선행 입력 아래 작성한 **프로젝트의 해석적 증명**이다.
toy 검산은 식을 잘못 옮기거나 조건을 빠뜨리는 일을 막는 보조 장치다.

## 3. 현재 위치와 남은 증명

목표는 “이 숫자 이상에서는 항상 Sono의 2e-17 부등식이 성립한다”는 충분한 시작점 X_cert다.
실제 가장 작은 전역 시작점과 같다는 보장은 없으며, 유한 관찰 X_emp와도 다르다.

현재 확보한 핵심 입력:

- finite-r 적분비, 교정된 summation 상수·profile와 실제 moment child.
- 실제 identity Hypothesis 1, weighted P92, W-filtered P91, growing-k P94.
- 공통 정규화와 고정-X preliminary probability.
- 이번 finite correlation, 조건부 분모·희소성, good-P failure, actual small-codegree.

남은 작업은 다음과 같다.

| 구분 | 미완료 작업 | 왜 필요한가 |
|---|---|---|
| R03 | local prime count·finite partition | 전체 평균만 아니라 필요한 각 구간의 후보 수를 보장해야 함 |
| R05 | off-tuple Markov·union 예산 | 원치 않는 위치의 영향이 여러 경우를 합쳐도 작아야 함 |
| R06 | main covering degree의 1·2차 moment | 좋은 p가 많다는 사실만으로 각 q가 충분히 덮인다고 결론낼 수 없음 |
| R07 | full hypergraph theorem의 수치 가정·실패율·subset 결론 | small-codegree 한 조건 외의 가정도 필요 |
| R08 | covering의 동시 사건·smooth remainder·반올림 | 따로 성공하는 사건들이 동시에 성공할 양의 확률 필요 |
| R09 | numerical PAP | 실제 identity Hypothesis로 대체되지 않는 별도 소수 분포 의무 |
| R10 | numerical two-prime UB | determinant·exceptional prime까지 균일한 상계 필요 |
| R11 | 전체 오차·같은 2e-17 계수의 공통 예산 | 개별 cutoff·성공확률을 한 곳에 합쳐야 함 |
| R12 | 보조 X→모든 큰 최종 변수 Z | 일부 구성점만 아니라 그 뒤 모든 값에서 성립함을 보여야 함 |

위 번호는 관리용 작업 단위이며 독립 정리가 정확히 9개 남았다는 의미가 아니다.
T1의 66개 general/복합 obligation 상태 수를 완료율로 쓰지 않는다.
broad SIV-07/08/09는 HARD_BLOCKER를 유지했다.

**얼마나 더 큰 수까지 실제 소수를 세어야 하는가?**
현재 막힌 것은 “데이터가 조금 부족하다”가 아니라 “증명 안의 여러 오차를 수치로 연결하지 못했다”는 점이다.
기존 child 조건 X≥2 exp(10^1000)는 유지하지만 이것은 최종 X_cert가 아니다.
이번 계산도 이 숫자까지 소수를 센 것이 아니다.
따라서 현재 결과만으로 더 검사할 소수 범위나 소요 CPU 시간을 정직하게 산출할 수 없다.
그런 이유로 threshold calculator나 긴 prime sweep을 만들지 않았다.

## 4. 선행연구와 PDF 판독 감사

| 원문 | 판독 | 대조한 부분 |
|---|---|---|
| [FGKMT](https://arxiv.org/abs/1412.5029), DOI [10.1090/jams/876](https://doi.org/10.1090/jams/876) | 확인 페이지는 native text, 새 OCR 없음 | 출판 pp.91,93: Lemmas 6.1,6.3, independence·distinct·두 copy 충돌 |
| [FMT](https://arxiv.org/abs/1511.04468) | 확인 페이지는 native text, 새 OCR 없음 | pp.13–14: S의 B0 제외, good P·조건부 분포, 구판 인용 번호 |
| [Rosser–Schoenfeld](https://doi.org/10.1215/ijm/1255631807) | PDF p.7은 scan+숨은 OCR text | 원이미지의 Theorem 7 (3.25)–(3.26): ± 부호·분모 2log²t·t≥285/t>1 |

텍스트가 추출된다는 이유만으로 scan을 native text로 분류하지 않았다.
FGKMT/FMT는 원래의 조판 텍스트를 먼저 사용했고, RS는 기존 image를 대조했다.
이번에 새 OCR·PDF 다운로드·PDF 수정은 없었다. 페이지 유형을 전체 PDF 모든 페이지의 판정으로 확대하지 않는다.
별도 TeX 파일을 이번 proof의 출판 정본 대신 사용하지 않았다.
원천/선행 문서 7개 SHA-256은 successor에 고정했다.

기존 Lemma의 proof가 이미 있으므로 불필요하게 처음부터 새 방법을 찾지 않았다.
다만 그 문헌의 “충분히 큼”이나 O 상수를 숫자 1로 임의 치환하지 않고,
theory 49 §§3–5에서 해당 multiplier와 actual 충분조건을 직접 증명했다.

## 5. 비판적 점검과 남긴 한계

| 위험 | 이번 처리 |
|---|---|
| 같은 점을 distinct correlation에 넣기 | 중복 입력을 거부; second moment collision은 최대 atom으로 따로 계산 |
| sigma 상계만으로 sigma^(-k)를 상계하기 | RS lower numerator / upper denominator로 올바른 하계를 새로 도출 |
| conditioning 분모 생략 | D_p≥sigma^k/2를 명시, 조건부 atom은 원래보다 느슨한 별도 상계 |
| E U=1로 놓고 오차 누락 | E(U−1)²≤3epsilon+collision 비용을 사용 |
| good p들 간 independence 요구 | 필요 없음: 선형기댓값/Markov만 사용 |
| small-codegree→full hypergraph 완료로 확대 | R07 OPEN 유지 |
| previous contract를 소급해 바꾸기 | DEP의 12 OPEN은 이력 보존; 새 successor에 3 closure/9 OPEN 기록 |
| 큰 child cutoff를 최종 threshold로 보고 | X_cert OPEN, 새 실제 계산·calculator 금지 유지 |

구체적 원문/입력에 대한 적용성 감사이지 외부 독립 검증은 아니다.
어느 선행 child에 오류가 발견되면 이 successor도 의존 영향을 다시 평가해야 한다.

## 6. 로컬 검증

- 최초 전용 23/23 PASS (0.059초) 후 parent 연결 시험을 추가했다.
- 최종 전용 exact/negative tests: 24/24 PASS, 0.075초, exit 0.
- 전수 residue 열거와 prime별 곱 공식의 독립 비교, 조건부 확률의 합 1 확인.
- 20점 균등 prior·두 shift의 충돌확률을 56/400으로 exact 계산하고 독립 pair second moment와 대조.
- 같은 작은 toy의 평균은 정확히 1이 아니므로 그 중심 오차를 실제로 보존하는지 검사.
- 실제 차원 diagnostic은 k=10^200,10^200+1,10^210에서 O(1)개 정수·유리수 비교만 수행.
- parent 포함 표적 137/137 PASS, 0.583초; 전체 527/527 PASS, 59.701초, exit 0.
- 전체 suite는 승인된 정상 로컬 권한에서 실행했다. 임시 디렉터리·multiprocessing toy를 포함하지만 actual 실험은 아니다.
- helper·전용/parent tests 5파일 py_compile PASS. 19파일 strict UTF-8, 4 JSON, 157 local links, source/선행 hash 7개 검사 issue 0.
- git diff --check 단독 exit 0. LF/CRLF 안내는 있었으나 whitespace 오류는 없다.
- RAM peak는 not measured. 새 figure가 없으므로 사용자 시각 QA 요청도 없다.
- actual prime/data 실험·통계·그래프, 새 source/설치, calculator, 외부 게시 없음.

## 7. 다음 권장 순서와 사용자에게 필요한 일

| 순서 | 작업·권장 근거 | 예상시간 구분 | 사용자 수행절차 |
|---|---|---|---|
| 1 | H1b-COR2 / R05: 새 R01/02/04를 바로 쓰는 off-tuple 예산 | 첫 감사·증명 초안 1–3시간; toy 수초–분 | 별도 수행절차 필요없음 |
| 2 | R03/R06: local count와 main-degree의 공통 finite moment | 첫 감사 2–6시간, 완결 시간 미정 | 현재 별도 수행절차 필요없음 |
| 3 | R07/R08: hypergraph·동시 covering의 남은 rate | inventory 1–3시간, 증명 난이도 재평가 | 현재 별도 수행절차 필요없음 |
| 4 | R09–R12: PAP/UB 및 최종 공통 cutoff/변수 이동 | source/의무 정리 1–3시간, 전체 해결시간 미정 | 현재 별도 수행절차 필요없음 |

위 시간은 연구 검토의 계획치이며 사용자 PC 장시간 실행 요청이나 완료 보장이 아니다.
지금은 설치·다운로드·사용자 실행이 필요 없다.
active goal의 승인 안에서 다음 순서로 진행할 수 있다.
필수 새 자료·설치·장시간 연산이 필요하면 이유와 정확한 사용자 절차를 보고한 뒤 멈춘다.
