# Sono/FMT H1b-DEP: 실제 호출 의존지도와 유한 적용성

- 작성: 2026-09-09 KST
- 상태: ACTUAL_DEPENDENCY_AUDIT_COMPLETE; root X_cert OPEN
- 증거 수준: SOURCE_AUDIT + PROJECT_FINITE_INTERFACE_PROOF
- 계약: [JSON](data/Sono_FMT_H1bDEP_actual_dependency_v1.json)
- 쉬운 진행현황: [review 54](../../review/54_20260909_H1bDEP_Xcert_진행현황_의존성감사.md)
- 선행: [theory 47](47_Sono_FMT_H1bNORM_common_weight_probability_normalization.md)

## 1. Context·목적·비목표

일반 Maynard Proposition 6.1 전체를 수치화하는 일과, FGKMT/FMT가 실제 사용하는 부분을
수치화하는 일은 다르다. H1b-DEP는 직접 인용뿐 아니라 필요한 보조증명의 의존관계를
추적하여 불필요한 증명을 임계 경로에서 제외한다. 이는 일반 정리 자체의 증명이 아니다.

현재 완료된 것은 W-filtered construction의 고정 sieve-scale X 입력이다. 이하 X는
theory 47의 보조 sieve scale이며, 마지막 maximal-gap 함수에 넣는 변수를 Z로 구별한다.
목표는 어떤 수치 X_cert를 정해 모든 Z>=X_cert에서 end-bounded 부등식을 보이는 것이다.
현재 child 조건 X>=2 exp(10^1000)을 그 X_cert로 이름만 바꾸면 안 된다.

비목표: 새 prime sweep, actual dataset 분석, 최적 threshold, calculator, 일반 P6.1/P95
완전 재증명, only-k u 선언, literal unfiltered weight 동일성, 독립 심사·Lean 인증.

## 2. 원문·버전과 PDF 판독

| 원천 | 채택한 위치 | 읽기·대조 |
|---|---|---|
| FGKMT, DOI [10.1090/jams/876](https://doi.org/10.1090/jams/876), [arXiv:1412.5029](https://arxiv.org/abs/1412.5029) | 출판 pp.78--82, 91--94, 97--102; 특히 p.99 Theorem 6 proof | native text 우선; p.99 원본 화면 대조 |
| FMT, [arXiv:1511.04468](https://arxiv.org/abs/1511.04468) | pp.9--16, Theorems 4--6, Lemmas 6.1--6.4 | native text 우선; p.13 원본 화면 대조 |
| Maynard, DOI [10.1112/S0010437X16007296](https://doi.org/10.1112/S0010437X16007296), [arXiv:1405.2593](https://arxiv.org/abs/1405.2593) | 출판 pp.1523--24, §§8--9, P9.1--9.5와 Lemma 9.3 | 출판 PDF 우선; 이전 Subsets.tex는 참조 탐색 보조 |
| Rosser--Schoenfeld, DOI [10.1215/ijm/1255631807](https://doi.org/10.1215/ijm/1255631807) | p.69, (3.13), n>=6 | 전면 scan+숨은 텍스트층; 원문 식 대조 |
| Sono, DOI [10.4418/2025.80.2.2](https://doi.org/10.4418/2025.80.2.2) | p.542, u와 C 정의 | native text; 기존 source tracing과 대조 |

선택 페이지의 text/font/image/rendering-mode 증거를 JSON에 보존했다. 이는 모든 페이지의
분류가 아니다. 새로운 OCR을 수행하지 않았다. Maynard arXiv v2는 2014 개정본이므로
2016 출판본과 자동 동일시하지 않는다. 원본 hash와 theory 43--47 hash는 불변이다.

## 3. 직접 호출과 P95의 실제 필요성

FGKMT 출판 p.99 Theorem 6 proof의 호출은 다음과 같다.

| 필요한 출력 | 실제 입력 | P95 필요 여부 |
|---|---|---|
| (7.6) weight 총질량 | Maynard P9.1 | 없음 |
| (7.7) 지정 소수 위치 moment | P9.2, gcd(a_L,B)=1 | 없음 |
| (7.8) off-tuple roughness moment | P9.4, xi=theta/10, D=1 | 없음; 이 출력은 FMT sequel에 필요 |
| (7.9) pointwise weight bound | Lemma 8.5(iii) | 없음 |
| profile I,J 상·하계 | Lemma 8.6, finite-r H1a | 없음 |

P9.1--9.4의 실제 증명, P9.2가 사용하는 Lemma 9.3, Section 8의 필요한 보조정리까지
대조했다. 이 closure는 P9.5를 호출하지 않는다. 다음 두 가지를 거짓 의존선으로 넣지 않는다.

1. P9.2 proof의 Proposition 6.1 언급은 E_q^(2)의 **분포 가정**을 사용한 것이다.
   P9.2 자체의 명시된 가정과 H1c의 actual identity input으로 공급한다. 전체 P6.1의
   결론을 다시 요구하여 P9.2→P6.1→P9.2 순환을 만들지 않는다.
2. TeX의 eq:S4Bound2는 P9.4 증명 중 식 label이다. Proposition S4=P9.5 호출이 아니다.
   문자열의 S4만 검색하여 의존선을 만들지 않는다.

P6.1의 네 번째 출력/P9.5는 tuple **안의** L(n)이 작은 소인수를 가지는 경우의 penalty다.
P9.4는 tuple **밖의** L(n)이 작은 소인수를 피하는 경우의 상계다. 다른 명제다.

**판정: P95는 선택한 actual filtered fixed-X 경로의 직접·간접 필수 입력이 아니다.**
따라서 현재 X_cert 목표의 선행조건에서 제외한다. 다만 일반 P6.1 전체를 인증했다고
주장하려면 P95를 포함해야 한다. 일반 원장 17행의 P95와 broad SIV-07 상태는 그대로 둔다.
이 판정은 향후 다른 construction/출력을 택하면 재감사해야 한다.

## 4. source 번호 변경과 가정 차이

| FMT가 인용한 구 FGKMT 번호 | 현재 FGKMT 출판본 | 필요한 점검 |
|---|---|---|
| Lemma 5.1 (FMT Lemma 6.1) | Lemma 6.1, p.91 | 현재는 distinct n_i, t<=log X, abs(n_i)<=X^2 |
| Corollary 4 (FMT local count Corollary 2) | Corollary 5, pp.91--92 | 전체 Q에서 부분구간 Q로의 prime-count/오차 균일성 추가 |
| Lemma 5.3 (FMT Lemma 6.2) | Lemma 6.3, pp.93--94 | good P(a)의 수치 실패확률 |
| Corollary 3 (FMT hypergraph Theorem 4) | 기능상 Corollary 4, pp.78--81 | 완전 동일 정리 아님; 현재판 small codegree 조건 추가 확인 |

FMT의 O(X^O(1)) 범위가 현재 출판 Lemma의 X^2 범위보다 넓다.
아래 §5의 actual support 확인으로 현재 입력은 X^2 안에 들어간다.
일반 polynomial 크기 전체를 이 문서에서 재증명하지 않는다.

현재 hypergraph 판본의 추가 조건은 §5.4처럼 actual geometry에서 조건부로 전달된다.
하지만 FMT Theorem 4의 더 강한 부분집합/고확률 결론까지 같은 번호로 갈음할 수 없다.
그 결론과 finite rate는 DEP-R07에 남긴다. 인용 번호 수정이 전체 확률정리 증명은 아니다.

## 5. 유한 actual-interface 보완

이 절은 theory 47의 모든 전제를 유지한다. a=log X, L=log(X/2),
k=floor(L^(1/5))>=10^200, Y는 (47.1), 1<=h_i<=2k^2,
P subset (X/2,X], Q subset (X,Y]이며 동일 source B와 별도 B0를 유지한다.

### 5.1 admissible tuple의 유한 존재

FMT p.11 자체가 첫 k개의 k보다 큰 소수를 예로 든다. 이를 finite bound로 보완한다.
h_i=p_(pi(k)+i)로 두면 서로 다른 소수이며 pi(k)+i<=2k.
RS1962 (3.13)은 n>=6에서 p_n<n(log n+log log n)을 준다.

k>=36에서 log(2k)<k/4다. 시작점은 log72<5<9이고, 차이의 도함수는
1/4-1/k>0이다. e^5>72는 지수급수의 처음 여섯 양의 항만으로도 확인된다.
log log(2k)<log(2k)이므로 h_i<=p_(2k)<k^2<2k^2.

소수 s<=k에 대해서 n=0이 모든 -h_i 잔여를 피한다. s>k에 대해서는
k개 이하의 금지 잔여가 s개 전체를 덮지 못한다. 따라서 이 tuple은 admissible이다.
실제 k개 소수를 생성한 것이 아니라 모든 k>=36에서의 존재/크기 증명이다.

### 5.2 off-tuple h 범위

w(p,n)>0이면 abs(n)<=Y. q=n+hp in Q이면 abs(h)p=abs(q-n)<=2Y,
p>X/2이므로 abs(h)<4Y/X. 따라서 actual 호출은 C_h=4로 충분하다.
log C_h<=L/4는 기존 L>=10^1000에서 만족한다.
이 연결 때문에 NORM의 max(10^1000,4 log C_h) child cutoff가 더 커지지 않는다.
zero-weight 항에 이 h support를 요구하거나 임의 h로 확장하지 않는다.

### 5.3 correlation lemma의 크기·차원 조건

theory 47 (47.6)의 Y>=2k^2 X를 재사용한다. 정의에서 Y<Xa이고 a>=10.
e^a>a^3/6>6a이므로 6Y<6Xa<X^2.

- abs(n+h_i p)<=Y+2k^2X<=2Y.
- off-tuple의 q+(h_i-h)p는 절댓값이 Y+2k^2X+4Y<=6Y<X^2.
- first/second moment의 point 집합은 많아야 2k개다.
  k>=2에서 2k<=k^5<=L<a=log X.

따라서 실제 등장하는 **서로 다른** point 집합에는 출판 FGKMT Lemma 6.1의
크기·차원 조건이 성립한다. 중복 point/collision 경우는 따로 세어야 한다.
위 연결이 그 lemma의 O(log^-16 X) 상수나 collision 비용까지 닫는 것은 아니다.

### 5.4 hypergraph small codegree: 선행증명의 조건부 명시화

FGKMT 출판 p.82에 이미 같은 divisibility 증명이 있다. 새 이론의 발견이 아니다.
각 e_p가 Q 중 한 residue class mod p의 부분집합이라고 하자.
q_1!=q_2가 동시에 e_p에 속하면 p divides (q_1-q_2).
§5.3에서 Y<X^2/4이다. 서로 다른 두 p>X/2의 곱은 X^2/4보다 크므로
0<abs(q_1-q_2)<Y를 동시에 나눌 수 없다.

따라서 각 고정 residue 선택 a에서
\[
 \sum_{p\in P}\Pr(q_1,q_2\in e_p\mid a)
 \le \max_{p,q}\Pr(q\in e_p\mid a).
 \tag{48.1}
\]
나중에 post-conditioning sparsity X^(-3/5)를 증명하면 RHS<=X^(-1/20)이 되어
출판 Corollary 4의 small codegree 조건이 충족된다.
이는 **CONDITIONAL_INTERFACE_PROVED**다. NORM의 unconditioned point probability
X^(-3/4)를 곧바로 RHS에 넣지 않는다. conditioning denominator X_p(a),
sigma^(-k), 가능한 h의 개수를 먼저 상계해야 한다(DEP-R02).
임의의 무관한 hypergraph나 넓은 Y에서는 이 결론이 자동 성립하지 않는다.

## 6. actual DAG와 아직 남은 12개 작업단위

방향은 입력→출력이다. 닫힌 parent는 과거 project proof에 대한 의존이며 독립 인증이 아니다.
JSON은 각 node의 범위, 원문, 입력, 상태를 보존한다.

~~~text
profile / actual identity Hypothesis
              → P91 · P92 · P94 · pointwise
              → 공통 filtered NORM + §5 actual interfaces
              → FMT correlation / conditioning / first-second moments
              → hypergraph / cover
PAP + UB      → 마지막 확률·계수 여유
              → 보조 X에서 최종 Z의 모든 큰 값으로 전달 → X_cert

일반 P95 → 일반 P6.1 전체 (별도 OPEN 경로; 위 actual 입력 경로에는 없음)
~~~

| ID | 현재 열린 작업 | 반드시 얻어야 하는 것 | 관련 원장 |
|---|---|---|---|
| DEP-R01 | FMT L6.1 / FGKMT L6.1 finite correlation | distinct-point Euler probability 상대오차 상수, 유효범위 | SIV-09 |
| DEP-R02 | sigma^(-k)와 conditioned sparsity | X_p(a) 하한을 유지한 point→residue 비용, §5.4 입력 | SIV-09, COV-07 |
| DEP-R03 | FMT Corollary 2의 local counts | 구간별 prime count, first/second moment, finite partition 동시 실패상계 | COV-01/02 |
| DEP-R04 | FMT Lemma 6.2의 good P(a) | collision 포함 second moment와 bad-prime count 실패율 | SIV-09 |
| DEP-R05 | FMT Lemma 6.3의 off-tuple 제거 | 수치 Markov/union budget, 정확한 h 개수 | SIV-09, COV-08 |
| DEP-R06 | FMT Lemma 6.4의 covering degree | main first/second moment, 대각선·중복점·bad P 제거 비용 | SIV-09, COV-08 |
| DEP-R07 | hypergraph/FMT Theorem 4 | small codegree뿐 아니라 모든 가정·부분집합 결론·finite failure rate | COV-06--10 |
| DEP-R08 | Sono sift/cover 합성 | smooth remainder, 분할·rounding, 동시 good event | COV-01--12 |
| DEP-R09 | numerical PAP | exceptional modulus/B0, uniform AP prime count의 수치 cutoff | PAP-01--11 |
| DEP-R10 | numerical UB | 두 소수 상계 sieve 상수, determinant·singular factor·B0 균일성 | UB-01--09 |
| DEP-R11 | 최종 확률·계수 budget | 모든 오류 합, positive probability와 Sono 2e-17 보존 | AN-01--12, FIN |
| DEP-R12 | auxiliary X→arbitrary final Z | primorial·지수·반복로그·끝점·모든 큰 Z coverage | TRN-01--06 |

12는 이번에 나눈 **작업단위 수**이지 앞으로 증명할 독립 정리의 확정 개수가 아니다.
발견되는 하위 lemma에 따라 바뀐다. DEP-R09/PAP와 actual identity Hypothesis는
동일한 명제가 아니며, DEP-R10/UB와 P94도 동일한 명제가 아니다.

T1의 역사적 66행은 7 EXPLICIT, 9 PARTIAL, 30 RATE_MISSING, 4 SOURCE_REVIEW_REQUIRED,
16 HARD_BLOCKER다. broad/general/복합 row가 섞이므로 7/66을 연구 완료율로 쓰지 않는다.
SIV-07/08/09의 broad 판정을 유지하면서 닫힌 actual branch를 successor DAG로 구분한다.

## 7. 구현·검증·위험

source/h1bdep_actual_dependency.py는 다음만 검사한다.

- 필수 node·edge, cycle, 범위, root OPEN; P95가 actual 입력의 ancestor가 아님.
- source와 선행 proof hash 및 원문 위치 기록.
- bounded toy의 admissible tuple와 residue geometry. 큰 k의 tuple 생성 금지.
- 잘못된 ancestor/root promotion, 가정 없는 codegree 전달, 위조 source hash의 거부.

이는 문서로 증명한 전 범위 명제를 자동 증명하거나 PDF 내용을 기계적으로 이해하는 도구가
아니다. source 감사·해석적 증명·toy unit PASS·외부 독립 검증을 구분한다.
검증 숫자와 명령은 review 54 및 이번 handoff에 기록한다.

## 8. Follow-up·승인 경계

다음 H1b-COR1은 DEP-R01을 우선한다. FGKMT L6.1 proof와 기존 explicit prime-sum
도구를 먼저 대조한 뒤 누락된 multiplier만 증명한다. sigma/post-conditioning은 DEP-R02로
분리해 입력 부채를 숨기지 않는다.

현재 승인 범위는 문헌·수학·짧은 toy/회귀·로컬 commit이다. 실제 dataset 분석,
threshold calculator, 새 설치 또는 장시간 CPU를 시작하지 않는다.
추가 필수 source/패키지가 생기면 사용자에게 요청한다. 현재 별도 수행절차 필요없음.
