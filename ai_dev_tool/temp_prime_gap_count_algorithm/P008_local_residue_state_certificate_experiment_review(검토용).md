# P008 — Local Residue-State Certificate를 이용한 Prime-Gap 탐색 가속 실험 제안서 및 검토요청서

## 0. 문서 목적

본 문서는 로컬 ChatGPT/Codex에 다음 연구를 제안하고, **수학적 타당성·논리적 완전성·계산 효율성·실제 prime-gap exhaustive search 가속 가능성**을 검토 요청하기 위한 것이다.

핵심 질문은 다음과 같다.

> 현재 확보한 **global finite-range residue-state dual certificate**를 각 유한 block에 적용하는 **local certificate**로 전환했을 때, `U_local < 1`인 block을 실제로 생성하여 CPU exhaustive prime-gap search를 건너뛸 수 있는가?

최종 목적은 Ryzen 7 9700X 1대에서 다음 범위의 maximal prime-gap 검증을 가능한 한 빠르게 수행하는 것이다.

- 1차 실험 범위: \([10^{20},10^{21})\)
- 장기 범위: \([10^{20},10^{26})\)
- 기본 threshold: \(H=1856\)
- 별도 분석 threshold: \(H=1858\) — 현재 확인되지 않은 후보 기록과 관련하여 parameterized하게 처리

이 문서는 **1856 이상 gap이 없음을 이미 증명했다고 주장하지 않는다.** 현재 확보된 것은 large-gap count의 global upper bound이며, 본 실험의 목적은 이를 실제 계산 skip으로 연결할 수 있는지 확인하는 것이다.

---

# 1. 현재까지 확보된 수학적 상태

## 1.1 기본 함수 정의

다음을 정의한다.

\[
N_{\ge H}(A,B)
:=
\#\left\{
 p:\ A\le p<B,\ p^+=\operatorname{nextprime}(p),\ p^+-p\ge H
\right\}.
\]

여기서:

- \(H\): gap threshold
- \(A\): lower bound
- \(B\): upper bound
- \(p^+\): 다음 consecutive prime

현재 관심사는

\[
N_{\ge1856}(10^{20},10^{21}).
\]

\(N_{\ge H}(A,B)=0\)이면 해당 start-bounded 범위에서 \(H\) 이상의 consecutive-prime gap이 없다.

---

## 1.2 현재 확인된 global certificate

현재 modulus

\[
M=2310=2\cdot3\cdot5\cdot7\cdot11
\]

를 이용하여 residue-state finite-state model을 만들었다.

\[
\varphi(2310)=480
\]

개의 unit residue state를 사용하고, 허용 residue transition마다 small/large representative gap을 구성한다.

dual certificate는 모든 transition에 대해

\[
w(d)D
\le
\lambda_{num}d
+
\mu_{num}
+
\phi_{num}(r)-\phi_{num}(s)
\]

를 정수 산술로 검증한다.

현재 exact verifier에서 다음이 확인되었다.

- states: `480`
- transition constraints: `415223`
- minimum integer slack: `0`
- internal large-gap upper bound:

\[
439161464927854178
\]

- right-boundary correction: 최대 1
- 최종 global bound:

\[
\boxed{
N_{\ge1856}(10^{20},10^{21})
\le
439161464927854179
}
\]

이 결과는 실제 large gap이 그만큼 존재한다는 의미가 아니라 **그 수를 넘을 수 없다는 unconditional upper bound**이다.

---

## 1.3 C-normalized 표현

비교용으로

\[
\mathcal T(H;A,B)
=
\frac{B-A}{\log B}
\exp\left(-\frac{H}{\log B}\right)
\]

를 정의한다.

그리고

\[
C_{\max}
=
\frac{U}{\mathcal T(H;A,B)}
\]

를 normalized upper-bound constant로 사용한다.

현재 global certificate에 대해

\[
\boxed{
C_{\max}
\approx
1.102803437542279\times10^{15}
}
\]

이다.

중요: 이 \(C\)는 표준 문헌의 Cramér 상수나 정리의 고유 상수가 아니며, **현재 연구에서 서로 다른 upper bound의 강도를 비교하기 위한 보조 normalization**이다. 엄밀한 핵심 결과는 정수 upper bound \(U\)이다.

---

# 2. 현재 global certificate의 한계

현재 결과는

\[
N_{\ge1856}(10^{20},10^{21})\le U
\]

라는 **전역 개수 상계**이다.

그러나 이것만으로 실제 탐색 위치를 알 수 없다.

극단적으로 \(U=1\)이라고 해도 그 한 개가 어디 있는지 모르면, 최악의 경우 전체 범위를 확인해야 한다.

따라서

\[
\boxed{
\text{global }U\text{ 자체는 search-space localization을 제공하지 않는다.}
}
\]

이것이 본 실험의 출발점이다.

---

# 3. 본 실험의 핵심 가설

Global certificate와 동일한 residue-state dual mechanism을 **local block**에 적용할 수 있다고 가정하고 검토한다.

임의의 block

\[
I=[x,x+L)
\]

에 대해

\[
U_M(x,L)
\]

이라는 residue-state dual certificate upper bound를 계산한다고 하자.

목표는

\[
\boxed{
U_M(x,L)<1
}
\]

이다.

왜냐하면 \(U_M(x,L)\)가 정수 count의 rigorous upper bound라면

\[
0\le N_{\ge H}(x,x+L)<1
\]

이므로

\[
\boxed{
N_{\ge H}(x,x+L)=0
}
\]

가 즉시 따른다.

따라서 이 block 전체는 **prime-gap exact search 없이 skip 가능**하다.

---

# 4. 연구 목표

## 목표 A — local certificate가 실제로 존재하는지 확인

2310 residue-state formulation을 block-local 형태로 변경하여 다음을 계산한다.

\[
U_{2310}(x,L)
\]

for representative \(x\) and a wide range of \(L\).

특히:

\[
x\in
\{10^{20},
2\times10^{20},
5\times10^{20},
10^{21}-\Delta\}
\]

등의 위치에서 조사한다.

---

## 목표 B — 최대 skip block 크기 측정

다음을 정의한다.

\[
L_{skip}(M,x)
:=-
\max\left\{
L:\ U_M(x,L)<1
\right\}.
\]

정확한 표기:

\[
\boxed{
L_{skip}(M,x)
=
\sup\{L>0:U_M(x,L)<1\}
}
\]

으로 사용한다.

실제로는 integer/range constraints에 맞춰 최대 실현 가능한 block 길이를 구한다.

---

# 5. 왜 이 실험이 중요한가

현재 global certificate는 위치를 주지 않는다.

하지만 local certificate가 다음을 달성하면:

\[
U_M(x_j,L_j)<1
\]

각 block

\[
I_j=[x_j,x_j+L_j)
\]

에 대해

\[
N_{\ge H}(I_j)=0
\]

를 인증할 수 있다.

그러면

\[
I_j
\]

전체를 CPU 계산 없이 skip할 수 있다.

따라서 실제 알고리즘 흐름은

```text
전체 범위
    ↓
local residue-state certificate
    ↓
U_local < 1 ?
 ┌──────────┴──────────┐
 │                     │
YES                    NO
 │                     │
SKIP block             exact candidate search
```

가 된다.

이것이 global C-bound를 실제 CPU 계산 가속으로 연결하는 핵심 메커니즘이다.

---

# 6. 중요한 비교: global U vs local U

## Global upper bound

\[
N_{\ge H}(A,B)\le U_{global}.
\]

이는 전체 count에 대한 정보만 준다.

## Local upper bound

\[
N_{\ge H}(x,x+L)\le U_{local}(x,L).
\]

특히

\[
U_{local}<1
\]

이면 실제 skip이 가능하다.

따라서 본 실험은 단순히 `C_max`를 더 낮추는 실험이 아니라

\[
\boxed{
\text{global certificate}\rightarrow\text{local zero certificate}
}
\]

로 변환하는 실험이다.

---

# 7. 실험 1 — 2310 local certificate sweep

## 입력

\[
M=2310,
\quad H=1856.
\]

Representative \(x\):

\[
10^{20},
1.1\times10^{20},
1.5\times10^{20},
2\times10^{20},
5\times10^{20},
8\times10^{20},
9\times10^{20},
9.9\times10^{20}.
\]

Block length \(L\): logarithmic sweep

\[
10^3,10^4,10^5,\ldots,10^{16}
\]

및 경계 주변에서 adaptive refinement를 수행한다.

## 출력

각 \((x,L)\)에 대해:

- `U_local`
- corresponding normalized `C_local`
- LP solve time
- exact rationalization time
- exact verification time
- `U_local < 1` 여부

를 기록한다.

---

# 8. 실험 2 — local certificate의 scale law 확인

다음 질문을 조사한다.

\[
U_M(x,L)
\]

이 \(L\)에 대해 선형적으로 증가하는가?

아니면 residue-state 구조 때문에 특정 scale에서 비선형적인 개선이 발생하는가?

특히 실험적으로

\[
U_M(x,L)/L
\]

과

\[
U_M(x,L)/\mathcal T(H;x,x+L)
\]

를 비교한다.

만약

\[
U_M(x,L)<1
\]

까지 내려가는 실용적인 \(L\)이 존재한다면, 그것이 바로 실제 skip block size다.

---

# 9. 실험 3 — modulus별 local certificate 비교

다음 순서로 비교한다.

\[
30
\rightarrow
210
\rightarrow
2310
\rightarrow
30030
\rightarrow
510510
\]

각 modulus에 대해

\[
L_{skip}(M,x)
\]

을 비교한다.

목표 표:

| modulus | states | transition representation | max local skip length | solve time | exact verify time |
|---:|---:|---|---:|---:|---:|
| 30 | 8 | dense/small | ? | ? | ? |
| 210 | 48 | dense/small | ? | ? | ? |
| 2310 | 480 | current | ? | ? | ? |
| 30030 | 5760 | sparse/cutting-plane candidate | ? | ? | ? |
| 510510 | 92160 | structured/implicit | ? | ? | ? |

---

# 10. 실험 4 — Candidate Cover 탐색

local certificate가 `U_local < 1`에 이르지 못하는 block에 대해서는 residue-state information을 이용하여 large-gap candidate superset을 생성할 수 있는지 검토한다.

candidate set

\[
S_I
\subset I
\]

에 대해 반드시

\[
\boxed{
\forall p\in I,
\text{ gap}(p)\ge H
\Rightarrow p\in S_I
}
\]

를 증명해야 한다.

false positive는 허용한다.

즉:

\[
\text{actual large-gap starts}
\subseteq S_I
\]

이면 충분하다.

반대로 실제 large-gap start가 하나라도 \(S_I\) 밖에 있을 수 있다면 해당 candidate cover는 사용할 수 없다.

---

# 11. Candidate Cover의 독립 검증

candidate generator와 verifier를 분리한다.

### Generator

residue-state / modular constraints를 이용하여 `S_I`를 만든다.

### Verifier

별도의 구현으로 다음을 검증한다.

\[
S_I
\text{가 모든 necessary residue transition을 포함하는가?}
\]

그리고 toy modulus:

\[
30,210,2310
\]

에서는 brute-force modular enumeration과 candidate generator를 교차비교한다.

---

# 12. 실험 5 — Coverage Ledger

전체 범위를 blocks

\[
I_0,I_1,\\ldots,I_m
\]

로 분해한다.

각 block은 다음 상태 중 정확히 하나를 갖는다.

- `CERTIFIED_ZERO`
- `CANDIDATE_COVER`
- `EXACT_SEARCHED`
- `COUNTEREXAMPLE_FOUND`

coverage invariant:

\[
\bigcup_{j=0}^{m}I_j=[A,B)
\]

및

\[
I_i\cap I_j=\varnothing,
\quad i\ne j.
\]

연속성:

\[
x_0=A,
\qquad
x_{j+1}=b_j,
\qquad
b_m=B.
\]

모든 block 경계를 exact integer/rational arithmetic으로 기록한다.

---

# 13. Coverage Ledger의 역할

coverage ledger는 단순 로그가 아니라 **exhaustiveness proof의 구성요소**다.

다음 질문에 자동으로 답해야 한다.

1. 어떤 구간이 skip되었는가?
2. skip의 수학적 근거는 무엇인가?
3. 어떤 구간이 exact search되었는가?
4. 모든 경계가 연결되어 있는가?
5. overlap 또는 gap(hole)이 없는가?
6. counterexample이 발견되었는가?

이를 통해

\[
\boxed{
\text{complete coverage + no-gap certificates + exact survivors}
}
\]

라는 최종 verification artifact를 만든다.

---

# 14. 실험 6 — Runtime 비교

baseline을 반드시 별도로 benchmark한다.

\[
T_{baseline}

ot=
\text{theoretical estimate only}
\]

실제 Ryzen 7 9700X 1대에서 동일 범위/동일 정확성 조건으로 측정한다.

새 pipeline:

\[
T_{new}
=
T_{certificate}
+T_{ledger}
+T_{candidate}
+T_{exact}.
\]

특히 candidate count를

\[
K=|S|
\]

로 정의한다.

따라서

\[
T_{exact}
\approx
K\,T_{candidate\_unit}
\]

로 모델링하되 실제 benchmark로 보정한다.

성공 조건은

\[
\boxed{
T_{new}<T_{baseline}
}
\]

이다.

실질적 의미가 있는 개선은 단순 몇 %가 아니라 다음 단계별로 기록한다.

- `>1.1x`: 약한 개선
- `>2x`: 유의미한 개선
- `>10x`: 알고리즘적 개선
- `>100x`: 구조적 breakthrough 후보

위 threshold는 연구 기록용 heuristic이며 수학적 기준이 아니다.

---

# 15. 9700X 단일 CPU 제약

모든 검증은 다음을 기준으로 한다.

- CPU: Ryzen 7 9700X 1대
- physical cores: 8
- GPU: 사용하지 않음
- distributed computing: 사용하지 않음
- 최종 exact verification: deterministic

certificate discovery 단계에서 multi-threading을 사용한다면 실제 CPU 시간을 반드시 기록한다.

최종 proof checker는 가능하면 single-thread deterministic integer verifier로도 동작하도록 만든다.

---

# 16. 30030-state를 바로 대규모 LP로 풀지 말아야 하는 이유

\[
\varphi(30030)=5760
\]

이고 ordered pairs만 해도

\[
5760^2=33,177,600
\]

이다.

small transition까지 포함하면 constraint 수는 더 커진다.

따라서 먼저 다음 대안을 비교한다.

1. sparse constraint generation
2. cutting-plane
3. active-set dual search
4. implicit transition oracle
5. dynamic programming / shortest-path relaxation
6. compiled streaming LP/oracle
7. certificate discovery와 certificate verification의 분리

단순 Python dense matrix 생성은 사용하지 않는다.

---

# 17. 2310 local certificate가 유용하지 않을 경우의 판정 기준

만약 전체 실험에서

\[
L_{skip}(2310,x)
\approx O(10^3)
\]

등으로 매우 작게 나오면, 2310 local certificate만으로는 실제 CPU search acceleration이 어렵다고 판정한다.

이 경우에는 즉시:

\[
2310\rightarrow30030
\]

또는 candidate-cover 단계로 이동한다.

반대로

\[
L_{skip}
\gg10^8
\]

등이 나오면 실제 block skipping의 가능성이 있으므로 coverage ledger와 runtime benchmark를 우선 진행한다.

이 threshold는 연구용 우선순위 기준이며 수학적 theorem이 아니다.

---

# 18. 중요한 논리적 구분

## Global count certificate

\[
N_{\ge H}(A,B)\le U
\]

### 제공하는 정보

전체 large-gap 개수의 상한.

### 제공하지 않는 정보

각 gap이 어느 위치에 있는지.

---

## Local zero certificate

\[
N_{\ge H}(x,x+L)=0.
\]

### 제공하는 정보

해당 block 전체를 exact prime-gap search에서 제외할 수 있다.

---

## Candidate cover

\[
\{
\text{actual large-gap starts}
\}
\subseteq S.
\]

### 제공하는 정보

`S` 밖을 탐색하지 않아도 된다는 논리적 근거.

---

# 19. 예상되는 연구 결과의 세 단계

## 결과 A — 실패하지만 유용한 결과

2310 local certificate가 너무 약하여

\[
U_{local}<1
\]

인 practical block이 존재하지 않음.

그러면 결론은:

> global residue-state certificate는 count bound 개선에는 유효하지만 direct search skipping에는 부적합하다.

이것도 유효한 negative result다.

---

## 결과 B — local skip 가능

충분한 수의 block에 대해

\[
U_{local}<1
\]

을 얻는다.

그러면 coverage ledger를 결합하여 실제 CPU skip이 가능하다.

---

## 결과 C — candidate cover 가능

local zero certificate는 약하지만

\[
\text{large-gap starts}\subseteq S
\]

를 증명하고

\[
|S|\ll B-A
\]

를 달성한다.

이 경우 exact prime-gap test는 `S`에 대해서만 실행한다.

---

# 20. 반드시 조사해야 할 수학적 문제

다음을 명시적으로 검토한다.

### Q1
현재 dual certificate를 block-local form으로 바꾸었을 때, 경계 potential term이 실제로 정확히 어떻게 바뀌는가?

### Q2
`M=2310`에서 block 시작 residue를 고정하거나 block 길이를 제한하면 stronger certificate가 가능한가?

### Q3
block의 시작/끝 residue를 알고 있을 때 global `2t` boundary penalty를 더 작게 만들 수 있는가?

### Q4
`U_local < 1`을 위해 최적 block partition을 analytic하게 계산할 수 있는가?

### Q5
candidate residue states만 생성하여 exact prime-gap search로 넘기는 sound superset을 만들 수 있는가?

### Q6
coverage ledger를 자동 생성하면서 모든 skipped block에 machine-checkable certificate를 첨부할 수 있는가?

### Q7
30030 이상의 modulus가 local certificate에서는 global certificate보다 훨씬 강해지는가?

### Q8
Buchstab / Type-I / Type-II factorization이 local certificate의 `U_local`을 실질적으로 낮추는가?

---

# 21. 선행연구 추가 조사 요청

다음 분야에서 본 구조와 직접적으로 연결되는 기존 결과를 조사한다.

- Selberg upper-bound sieve
- Brun sieve
- Buchstab identity
- Type-I / Type-II sums
- large sieve
- Jacobsthal function
- prime-free intervals
- admissible residue patterns
- finite-state modular covering
- large prime gaps
- computational exhaustive prime-gap verification
- Oliveira e Silva–Herzog–Pardi
- Banks–Ford–Tao
- Ford–Green–Konyagin–Maynard–Tao
- `primesieve`
- `primecount`
- existing prime-gap search implementations

특히 다음 질문을 선행연구에서 확인한다.

> 이미 `local prime-gap count upper bound < 1`을 이용해 finite blocks를 인증하는 방법이 존재하는가?

> residue-state / automaton / covering congruence를 이용한 prime-free interval certificate와 본 방법의 관계는 무엇인가?

> P007의 2310 certificate가 기존 연구의 직접적인 재발견인지, 조합/응용의 새로운 formulation인지?

새로운 방법이라고 주장하기 전에 반드시 확인한다.

---

# 22. 성공 판정 기준

이번 연구는 다음 순서로 판정한다.

### Stage 1
2310 local certificate가 수학적으로 정확한지 exact verifier로 확인.

### Stage 2
`U_local < 1` block이 존재하는지 탐색.

### Stage 3
그 block들을 모두 포함하는 coverage ledger 생성.

### Stage 4
남는 block의 candidate cover 생성.

### Stage 5
candidate-only exact prime-gap search를 구현.

### Stage 6
Ryzen 7 9700X에서 baseline과 실제 runtime 비교.

### Stage 7
효과가 있으면 30030으로 확대.

---

# 23. 최종 연구 목적

본 실험의 최종 목적은 단순히 `C_max`라는 숫자를 줄이는 것이 아니다.

목표는 다음 implication을 실제 machine-checked pipeline으로 만드는 것이다.

\[
\boxed{
\text{stronger finite-range certificate}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{local zero certificates or complete candidate cover}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{fewer exact prime-gap tests}
}
\]

\[
\Downarrow
\]

\[
\boxed{
\text{lower Ryzen 7 9700X runtime}
}
\]

궁극적인 대상은

\[
10^{20}\le p<10^{26}
\]

범위에서

\[
G\le1854
\]

또는 검증된 threshold 설정에 따라

\[
G<1858
\]

를 exhaustive/deterministic하게 검증할 수 있는 CPU-only 알고리즘을 만드는 것이다.

---

# 24. Codex에게 요구하는 최종 deliverables

- [ ] 2310 local certificate의 수학적 유도 검토
- [ ] independent local verifier 작성
- [ ] `U_local(x,L)` sweep 코드 작성
- [ ] 최대 skip block `L_skip(M,x)` 계산
- [ ] modulus 30/210/2310 비교
- [ ] 30030에 대한 resource estimate
- [ ] candidate-cover 가능성 분석
- [ ] coverage ledger 구현
- [ ] baseline vs hybrid runtime benchmark 설계
- [ ] 기존 prime-gap exhaustive code와 연결 가능성 검토
- [ ] Buchstab/Type-I/II 적용 가능성 조사
- [ ] 선행연구 조사 및 novelty 판정
- [ ] 결과가 negative라도 명확한 실패 조건과 다음 연구 방향 제시

---

# 25. 핵심 검토 요청

다음 질문에 대해 **증명 가능한 것 / 계산으로 검증 가능한 것 / heuristic인 것 / 현재 불가능한 것**을 각각 구분하여 판정한다.

1. `U_global`을 `U_local(x,L)`로 엄밀히 변환할 수 있는가?
2. `U_local < 1`인 block을 실제로 얻을 수 있는가?
3. 그런 block들의 전체 coverage를 빠짐없이 구성할 수 있는가?
4. local certificate가 없는 block에 대해 완전한 candidate cover를 만들 수 있는가?
5. candidate count가 baseline보다 충분히 작은가?
6. Ryzen 7 9700X 1대에서 실제로 총 runtime이 감소하는가?
7. 이 구조가 `10^20~10^26`으로 확장 가능한가?
8. 기존 문헌에 동일/유사한 방법이 이미 있는가?

최종적으로 다음 명제를 검토한다.

\[
\boxed{
\text{global residue-state upper bound}
\quad\not\Rightarrow\quad
\text{runtime improvement}
}
\]

하지만

\[
\boxed{
\text{global certificate}
\rightarrow
\text{local zero certificate / candidate cover}
\rightarrow
\text{coverage proof}
\rightarrow
\text{exact survivor verification}
}
\]

가 성립한다면 실제 알고리즘 개선으로 연결될 수 있다.

따라서 이번 P008의 1차 목표는 `C_max`의 추가 감소가 아니라, **현재 검증된 residue-state dual certificate를 실제 skip/candidate-localization mechanism으로 전환할 수 있는지 실험적으로·수론적으로 판정하는 것**이다.
