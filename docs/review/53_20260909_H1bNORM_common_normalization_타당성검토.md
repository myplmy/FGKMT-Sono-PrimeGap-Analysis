# H1b-NORM 공통 정규화: 무엇을 연결했고 무엇이 남았는가

- 작성·최종 갱신: 2026-09-09 KST
- 판정: PROJECT FINITE PROOF; 전체 X_cert OPEN
- 정본: [theory 47](../method/theory/47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md)

## 1. 쉬운 설명

서로 다른 저울 세 개로 잰 값을 비교하려면 눈금이 같은지 먼저 확인해야 한다.
이번의 세 “저울”은 모든 정수의 점수 합(P91), 원하는 소수 위치의 점수 합(P92),
다른 위치의 점수 합 상계(P94)다. 앞 단계는 각 저울의 오차를 분석했고,
이번 단계는 같은 눈금으로 옮긴 뒤 확률로 나누어도 오차가 통제됨을 증명했다.

예를 들어 점수 계산 전의 coefficient가 1.01배 달라지면 점수는 제곱이므로 1.0201배
달라진다. 이를 1.01배로만 옮기면 틀린다. 실제 연결에서는 소수 p마다 보정비가
달라지므로 상수 하나인 것처럼 합 밖으로 꺼내지도 않았다.

## 2. 구체적으로 닫은 연결

| 대상 | 이번 명시 결과 | 의미 |
|---|---|---|
| singular series | alpha=(p-1)/(p-k), beta=(q-1)/(q-k), 제외 B일 때 1 | 대략 같다는 주장 대신 exact factor |
| 가중치 | alpha/beta의 제곱 | 부호 취소를 훼손하지 않는 동일 scalar 변환 |
| dyadic 소수 개수 | 상대오차 3/log X 이하 | 새 소수 계산 없이 선행 explicit theorem 적용 |
| P91 공통 합 | 상대오차 4/k 이하 | 확률의 분모가 양수임도 확보 |
| P92 공통 합 | 상대오차 2/sqrt(k) 이하 | B0 한 소수 삭제 비용 포함 |
| 지정 위치 확률 | 상대오차 3/sqrt(k) 이하 | FMT의 (log_2 X)^(-10)보다 작음 |
| 단일 정수 확률 | X^(-3/4) 이하 | 특정 정수 한 곳에 점수가 과도하게 몰리지 않음 |
| tau/u_X | tau>=2, log(k)/160<u_X<log(k) | tau 양수와 u_X의 로그 크기를 확보 |

조건은 매우 강한 k>=10^200 및 같은 Maynard W-filter·profile·source B다.
X>=2 exp(10^1000)는 이 child 합성의 충분조건이지 Sono 정리 전체의 임계값이 아니다.
이를 그 크기까지 소수를 실제 계산했다는 뜻으로 읽으면 안 된다.
더 작은 시작점을 얻을 수 없다는 뜻도 아니다.

## 3. 중요한 양화·정의 주의

원문 선언에는 u가 차원만의 함수라고 적혀 있지만, 실제 표시된 u 정의에는 현재 X와
예외 parameter B가 들어 있다. 이번에는 이를 숨기지 않고 u_X로 쓴다.

한 번의 증명에서 X를 고정하면 u_X는 p,q,i나 무작위 추출 결과에 따라 바뀌지 않는다.
이번 확률식은 이 조건만으로 직접 유도했다. 서로 다른 X에서도 u가 같다는 더 강한
명제는 인증하지 않았다. FMT 뒤쪽의 first/second moment에서 쓰는 것은 고정-X
scalar이지만, 그 뒤 확률 실패율과 전체 정리 연결까지 끝났다는 뜻은 아니다.

또 B와 B0는 별개다. B는 sieve construction의 예외 소수이고,
B0는 FMT에서 소수 집합에서 최대 한 개를 빼는 별도 parameter다.
“한 개쯤 빼도 괜찮다”는 원문 각주를 실제 가중치 비용으로 계산했다.
literal unfiltered weight와 Maynard W-filtered weight도 동일시하지 않았다.

## 4. 선행연구 적용성

theory 47 §1에 DOI/arXiv와 정확한 페이지·식 번호를 모았다.
FGKMT §8은 공통 정규화 구조를 제공하나 O(k/X)의 숫자 multiplier를 모두 주지는 않는다.
FMT p.12 각주 2는 B0 삭제를 설명하나 finite 비용은 별도 필요하다.
Rosser--Schoenfeld p.69 Theorem 1은 필요한 양측식과 범위가 explicit해서 직접 채택했다.
Sono p.542는 phi(B)/B in [1/2,1]을 유지하므로 이를 1로 대체하지 않았다.

텍스트 우선으로 읽고 핵심 수식·각주만 이미지로 확인했다.
RS 추출문에서 부호·분수 배치가 흐트러진 실제 사례가 있어 원문을 우선했다.
표적 검색에서 적합한 완성 package를 찾지 못한 것은 세계적 부재나 novelty의 증거가 아니다.
이 결과는 프로젝트 analytic proof이며 peer review·독립 전문가 검증·Lean proof가 아니다.

## 5. 검증과 한계

FGKMT Python의 전용 17/17 (0.098초), 표적 93/93 (0.292초),
전체 483/483 (59.932초, exit 0) 시험을 통과했다.
첫 표적 회귀에서는 parent schema 기대값 1.14.0이 남아 1건 실패했고,
실제 schema 1.15.0을 반영한 뒤 다시 통과했다. 수학 gate를 완화하지 않았다.
helper·전용/parent 시험 5개 py_compile 및 원문/선행 proof·code 10개 hash도 일치한다.
독립 bounded fixture는 작은 residue 전수검사, source coefficient 직접 합,
prime-slice 제곱비, B0 삭제, 확률 분모 오차와 exact dimension bin을 확인한다.
전체 k의 증명은 theory 47의 단조식과 다항식 부등식에 있으며 scalar 표본으로 대신하지 않는다.

새 actual dataset, 실험 결과, 그래프, threshold calculator는 생성하지 않았다.
필수 설치나 장시간 실행 요청도 현재 없다. 별도 수행절차 필요없음.

## 6. 다음 권장 순서

환경은 Codex의 문헌·증명 작업과 FGKMT Python, 시작 경로는 프로젝트 루트다.
시간은 조사 계획치이며 CPU 연속 사용시간 약속이 아니다.

| 순서 | 작업·이유 | 계획 시간 | 사용자 절차 |
|---|---|---:|---|
| 1 | H1b-DEP actual dependency: 필요 없는 일반 P95 재증명을 피하고 root와 child 범위 구분 | 1--2시간 | 별도 수행절차 필요없음 |
| 2 | FMT Lemma 6.1--6.4 finite correlation·failure rate: 확률 입력 다음의 실제 빈 연결 | 2--6시간, source 감사 뒤 조정 | 현재 별도 수행절차 필요없음 |
| 3 | PAP/UB·hypergraph·arbitrary-X 남은 rate 재분류 | 1--3시간 inventory; 증명은 재산정 | 자료/설치/장시간 계산 필요시 정확한 절차로 요청 후 중단 |

이번에 정규화가 닫혔다고 threshold calculator를 만들지 않는다.
최종 root 의무가 모두 닫혔다는 별도 requirement-by-requirement 감사가 먼저다.
