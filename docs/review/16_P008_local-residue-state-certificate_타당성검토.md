# P008 local residue-state certificate 제안 비판적 타당성 검토

## 판정

검토용 문서의 가장 중요한 방향은 맞다.

> 전역 개수 상한을 낮추는 것만으로 탐색 위치가 줄지는 않으며, 실제 가속에는 block별 0개 인증 또는 누락 없는 candidate cover, 전체 coverage 증명, survivor의 exact 검사가 필요하다.

다만 제안서의 `U_local < 1이면 block을 skip한다`는 문장은 **오른쪽 경계 gap을 해결한다는 조건이 빠져 있어 그대로 구현하면 안전하지 않다.** 현재 P007의 start-bounded 정의에서는 block 안의 마지막 소수에서 다음 소수로 넘어가는 gap이 최대 1개 남는다. 이 gap을 `+1`로 처리하는 한, 소수가 하나 이상 있는 block의 전체 상한은 최소 1이다. 따라서 P008은 다음처럼 제한해 채택한다.

- 채택: P007 인증서의 block-local exact 적용, `floor` 정수 상한, 경계 상태 분리, toy 독립검증, exact prime-count 입력 비용 측정
- 조건부 채택: 경계 gap이 작다는 exact 증거가 붙은 block만 `CERTIFIED_ZERO`
- 보류: 30030 이상 local LP, candidate cover 생성, `prime-gap` 탐색과의 결합
- 기각: 겹치는 대표 block sweep을 coverage ledger로 부르는 것, unresolved boundary가 있는 block을 skip하는 것, residue state만으로 candidate 위치가 자동 생성된다는 주장

따라서 P008은 **직접 가속기 구현**이 아니라, 그 가속기가 성립할 수 있는지 먼저 판정하는 P008-A feasibility experiment로는 타당하다.

## 검토 대상

- `ai_dev_tool/temp_prime_gap_count_algorithm/P008_local_residue_state_certificate_experiment_review(검토용).md`
- P007 인증서 `ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt`
- P007 정본 구현 `source/finite_gap_certificate.py`
- P007 계획 및 검토 `test_plan/P007_finite-range-residue-state-certificate.md`, `docs/review/15_P007_finite-range-residue-certificate_타당성검토.md`

## 제안서가 올바르게 포함한 연결 증명

다음 항목은 실제 알고리즘 개선에 필요한 핵심을 잘 짚었다.

1. 전역 `N≤U`는 사건의 위치를 알려주지 않는다는 구분
2. block별 `N=0` 또는 모든 실제 start를 포함하는 candidate superset이 필요하다는 조건
3. false positive는 허용하지만 false negative는 한 건도 허용하지 않는 candidate-cover 계약
4. generator와 verifier의 분리 및 toy brute-force 교차검증
5. block의 hole·overlap·상태·증거 hash를 기록하는 coverage ledger
6. certificate 생성비, ledger 비용, survivor 검사비를 모두 포함한 실제 runtime 비교
7. 30030/510510 dense LP의 상태·제약 폭발을 인정하고 cutting plane 또는 separation oracle을 먼저 요구한 점
8. negative result도 유효한 연구결과로 미리 정의한 점

이 구성은 P007 상한을 실제 탐색 감소로 연결하기 위한 큰 뼈대로 충분하다.

## 반드시 보정해야 하는 수학 사항

### 1. 오른쪽 경계 `+1`은 local zero를 막는다

정확한 대상은

\[
N_{\ge H}(A,B)
=\#\{p:\ A\le p<B,\ p^+-p\ge H\}
\]

이다. `[A,B)` 안의 마지막 소수 `p_last`가 있으면 그 다음 소수는 `B` 이상일 수 있다. 내부 endpoint가 모두 block 안에 있는 gap의 상한을 `U_internal`이라 할 때, 경계를 모르면 안전한 전체 상한은

\[
U_{total}\le U_{internal}+1
\]

이다. 따라서 nonempty block에 generic `+1`을 둔 상태로는 `U_total<1`이 될 수 없다.

`CERTIFIED_ZERO`를 허용하려면 다음 중 하나가 필요하다.

1. 마지막 start prime과 그 다음 consecutive prime을 exact하게 찾아 crossing gap `<H`를 인증
2. block 경계를 prime endpoint에 맞춘 뒤 어느 이웃 block이 경계 gap을 담당하는지 증명
3. endpoint state와 crossing을 함께 포함하는 더 강한 local certificate

구현에서는 `right_boundary_status=UNRESOLVED`인 nonempty block을 절대로 0개 인증하지 않도록 했다.

### 2. 임의 block에서는 `pi(B)-pi(A)-1`을 그대로 쓰면 안 된다

P007의 `A=10^20`, `B=10^21`은 둘 다 합성수라서 기존 식이 맞았다. 임의의 local endpoint가 소수일 수도 있으므로 `[A,B)` 안의 start-prime 수는 항상

\[
K=\pi(B-1)-\pi(A-1)
\]

로 계산해야 한다. 내부 gap 수는 `max(K-1,0)`이고 crossing gap은 최대 1개다. 이 보정 없이 endpoint가 소수인 block을 처리하면 한 gap을 누락할 수 있다.

### 3. 정수 개수 상한은 `ceil`보다 `floor`가 맞다

dual 합산으로 정수 `N`에 대해 `N≤q`라는 유리수 상한을 얻으면

\[
N\le\lfloor q\rfloor
\]

가 따른다. P007은 안전하지만 한 단위 약한 `ceil(q)`를 저장했다. 실제 P007 유리수 내부 상한은

\[
q=439161464927854177.594632421806887
\]

이므로 인증서가 직접 주는 더 날카로운 값은

\[
N_{internal}\le439161464927854177,
\qquad
N_{total}\le439161464927854178
\]

이다. 기존 실행이 보고한 `439161464927854179`도 여전히 참인 상한이므로 결과가 무효가 되는 것은 아니다. P008 구현은 `floor`와 기존 보수적 `ceil`을 둘 다 기록한다.

### 4. block 정수 경계의 residue는 prime-path endpoint state가 아니다

potential telescope의 끝 상태는 `A mod M`, `B mod M`가 아니라 block 안의 **첫 소수와 마지막 소수의 residue**다. 이 소수들을 모르면 `phi(first)-phi(last)`를 쓸 수 없고 안전한 worst case `2t`를 써야 한다. 따라서 제안서의 “block 시작 residue 고정”은 정수 `x mod M`만 고정해서는 충분하지 않다.

### 5. `L_skip`의 단조성을 가정할 수 없다

현재 인증서는 `mu<0`이고 local prime count는 endpoint에서 계단식으로 변한다. endpoint state까지 쓰면 potential도 바뀐다. 따라서 `U_M(x,L)`이 모든 `L`에서 단조 증가한다는 증명 없이 binary search로 “최대 skip 길이”를 찾으면 안 된다. 실제로 검사한 discrete set과 각 bound를 저장하고, 단조성이 증명된 경우에만 `sup` 또는 adaptive binary search를 사용해야 한다. 원문의 `:=-`는 단순 오타다.

### 6. 대표 block sweep은 coverage ledger가 아니다

서로 겹치는 `(x,L)` 표본은 강도 민감도 자료일 뿐 `[10^20,10^21)`의 분할이 아니다. coverage를 주장하려면 half-open block들이 정확히 연결되고 모든 block에 zero/candidate/exact evidence hash가 있어야 한다.

## 계산·알고리즘 타당성

### exact prime count 비용이 certificate보다 더 클 수 있다

local bound에는 정확한 `K`가 필요하다. 설치된 WSL `primecount 7.10`은 `--double-check` 옵션이 없으므로 Gourdon과 Deleglise–Rivat 두 알고리즘을 따로 실행해 정수 결과 일치를 요구하도록 준비했다.

공식 최신 benchmark에서 `pi(10^20)`은 32-core Zen 5에서 Gourdon 약 15.74초, Deleglise–Rivat 약 78.64초이고 `pi(10^21)`은 각각 약 62.69초와 352.86초다. Ryzen 7 9700X 8-core와 배포판 7.10에서는 더 오래 걸릴 수 있다. 수백 endpoint를 처음부터 계산하면 local certificate가 절약할 시간보다 입력 생성비가 더 커질 가능성이 높다. [primecount 공식 README](https://github.com/kimwalisch/primecount#benchmarks)

그래서 P008-A full은 `x=10^20`에서 `L=10^3,10^6,10^9,10^12` 네 block, 총 다섯 unique endpoint만 먼저 계산한다. 이 단계가 약하면 112-block sweep은 실행하지 않는다.

### candidate cover는 아직 도출되지 않았다

P007 state는 소수가 modulus 2310의 unit residue라는 필요조건을 압축한다. 이 정보만으로 actual large-gap start의 작은 위치 목록이 생기지는 않는다. candidate cover를 채택하려면 다음 명제를 별도로 증명해야 한다.

\[
\forall p\in[A,B),\quad p^+-p\ge H\Rightarrow p\in S.
\]

그리고 `S`의 각 원소가 `prime-gap`의 `m·P#/d` 작업단위에 어떻게 대응하는지, 그 표현 밖의 실제 start가 없다는 mapping theorem이 필요하다. Seth Troisi의 도구는 임의 연속 `x` block scanner가 아니라 `m·P#/d` 주변을 sieve·통계·PRP 검사하는 pipeline이다. [prime-gap 공식 README](https://github.com/sethtroisi/prime-gap)

### final gap 인증은 primality와 interior compositeness를 요구한다

어떤 survivor가 실제 consecutive-prime gap임을 말하려면 양 endpoint의 소수성과 그 사이 모든 정수의 합성수를 확인해야 한다. probable-prime 판정이나 residue 조건만으로는 충분하지 않다. 대규모 계산에서 interval별 prime count를 독립 확인하고 이상 구간 전체를 재계산한 Oliveira e Silva–Herzog–Pardi의 절차가 coverage와 교차검증의 적절한 선례다. [Math. Comp. 논문, DOI 10.1090/S0025-5718-2013-02787-1](https://doi.org/10.1090/S0025-5718-2013-02787-1)

## Jacobsthal·sieve 문헌과의 관계

Jacobsthal 함수 계산은 선택한 작은 소수들의 residue class가 연속 정수열을 완전히 덮는 문제와 직접 연결된다. Ziller–Morack은 residue cover, exhaustive enumeration, pruning, 서로 다른 알고리즘의 결과 대조를 제시한다. 이는 future candidate/composite-cover verifier의 참고가 되지만 “실제 prime이 없다”는 결론은 사용한 작은 소수들이 모든 interior integer를 실제로 나눈다는 certificate가 있을 때만 성립한다. [arXiv:1611.03310](https://arxiv.org/abs/1611.03310)

Buchstab identity, Type-I/II sums, Selberg/large sieve는 count bound를 개선할 수 있는 이론 후보지만, 그 자체로 특정 finite block의 exact zero 또는 후보 위치 파일을 주지는 않는다. P008의 machine-checkable finite implication으로 바꾸는 추가 정리와 verifier가 나오기 전에는 탐색 가속 단계에 넣지 않는다.

## 구현에 반영한 안전 계약

- `[A,B)` prime 수는 `pi(B-1)-pi(A-1)`로 계산
- 내부 exact rational bound와 `floor`, historic conservative `ceil`을 함께 저장
- endpoint prime state가 없으면 `2t`; 정수 block residue를 대신 사용하지 않음
- crossing 미해결 nonempty block은 total upper bound에 1을 유지
- `CERTIFIED_ZERO`는 empty block 또는 crossing `<H` exact 증거가 있을 때만 허용
- 대표 sweep에는 `representative_blocks_are_not_a_coverage_ledger=true`
- candidate cover와 direct speedup은 항상 false로 시작
- saved CSV를 별도 direct `Fraction` 구현으로 재계산하고 artifact hash를 확인
- future ledger verifier는 연속 경계와 상태별 evidence hash를 요구

## 실행 후 보완 판정 — 2026-08-24

P008-A의 toy pilot, exact prime-count 입력, `x=10^20`의 네 representative block full이 모두 PASS했다. 그러나 실제 full에서는 다음 결과가 나왔다.

| block length L | internal rational bound q | internal floor | crossing 포함 total | certified zero |
|---:|---:|---:|---:|---:|
| `10^3` | 0.499300014467527 | 0 | 1 | 0 |
| `10^6` | 486.369964055189447 | 486 | 487 | 0 |
| `10^9` | 486,149.337346680925757 | 486,149 | 486,150 | 0 |
| `10^12` | 486,138,172.074728280481962 | 486,138,172 | 486,138,173 | 0 |

따라서 구현은 타당하게 작동했지만 supplied modulus-2310 certificate를 그대로 local tiling에 쓰는 방법은 직접 가속 후보가 되지 못했다. 대표 block 네 개는 coverage ledger가 아니며, `certified zero=0`이므로 건너뛸 수 있다고 증명된 실제 block도 0개다.

### 경계 gap을 해결하는 데 필요한 최소 정리

block 안의 마지막 소수를 `p<B`라 하자. `B` 이상에서 어떤 **증명된 소수** `q`를 찾아

\[
q-p<1856
\]

을 확인하면 crossing consecutive gap은 1856 미만이다. 이유는 `p` 다음의 실제 consecutive prime을 `p^+`라 할 때 `p^+≤q`이므로

\[
p^+-p\le q-p<1856
\]

이기 때문이다. 따라서 `p`와 `q` 사이에 다른 소수가 없는 것까지 증명할 필요는 없다. 다만 `p`가 block 안의 마지막 소수라는 사실과 `p,q`의 소수성은 exact하게 인증해야 한다.

PARI/GP의 `isprime`은 fully proven primality test를 제공하므로 작은 boundary witness verifier 후보가 될 수 있다. 함수 의미는 [PARI/GP 공식 문서](https://pari.math.u-bordeaux.fr/doc.html)를 정본으로 삼는다. 현재 WSL에는 `gp`가 설치되어 있지 않으므로 설치와 actual 실행은 별도 사용자 승인·행동이 필요하다.

## 수행 주체와 자원 한계 분류

아래 분류는 “이론상 언젠가 가능”이 아니라 현재 프로젝트의 168시간·32 GB RAM·100 GB disk 제한에서 실제로 맡을 수 있는 작업을 기준으로 한다.

### A. ChatGPT가 로컬에서 수행할 수 있는 일

| 작업 | 가능한 산출물 | 제한 |
|---|---|---|
| 경계 정리와 반올림·coverage 논리 증명 감사 | 정리, exact verifier 계약, 반례 toy fixture | 새로운 난해한 수론 정리를 반드시 발견한다고 약속할 수 없음 |
| 선행연구·공식 도구 조사 | DOI/arXiv/공식 문서가 붙은 검토보고서 | 문헌의 명제를 프로젝트 finite certificate로 바꾸는 추가 증명은 별개 |
| candidate-cover/mapping theorem 명세 | false-negative 0 계약, coverage ledger schema | 명세만으로 theorem이 증명되는 것은 아님 |
| memory-safe separation-oracle 설계·toy 구현 | 작은 modulus에서 dense LP와 동등성 시험 | 실제 30030 성능은 사용자 PC 실측 전 미확정 |
| break-even·민감도 계산 | 시간·RAM·disk 상한표, 중단 게이트 | 입력 성능모델이 실제와 다르면 재보정 필요 |
| 독립 exact 검증기·runner 작성 | hash, non-overwrite, PASS/FAIL 로그 | heavy actual 실행은 사용자가 수행 |

ChatGPT가 수행할 수 있는 “수학적 증명”은 기존 정의에서 따라오는 유한 정리, 반올림·경계·cover soundness 같은 명제를 엄밀히 전개하고 machine-checkable verifier로 바꾸는 범위다. candidate set을 획기적으로 희소화하는 새로운 정리를 정해진 시간 안에 반드시 만들어 낸다는 보장은 할 수 없다.

### B. 사용자 PC의 도움을 받아 수행할 수 있는 일

| 우선순위 | 사용자 실행 후보 | 예상 자원 | 진행 조건 |
|---:|---|---|---|
| 1 | 선택한 1–10개 block의 exact boundary witness pilot | 대략 수분–수십 분, RAM 1 GB 미만 예상, disk 1 GB 미만 | ChatGPT가 verifier/runner를 먼저 구현하고 PARI/GP 설치 승인 필요 |
| 2 | 30030 separation-oracle/cutting-plane bounded pilot | 설계 후 약 1–6시간의 초기 상한, RAM hard cap 28–30 GiB, disk 수 GB 이하 | 작은 modulus 동등성·메모리 guard PASS 후에만 |
| 3 | 추가 10–20개 exact prime-count endpoint 민감도 | 현재 실측 기준 약 2–4시간, RAM 0.3 GB 미만, disk 1 GB 미만 | P008 direct-tiling 음성결과 때문에 낮은 우선순위 |
| 4 | candidate-cover가 나온 뒤 survivor baseline 비교 | 후보 수에 따라 수분–168시간 | coverage theorem과 total-cost 모델이 먼저 PASS해야 함 |

1번은 crossing 증명을 실제로 만들 수 있는지 확인하는 과학적 pilot이다. 하지만 길이 1,000 block 하나를 zero로 만들더라도 전체 `9×10^20` 범위에 9×10^17개 block이 필요하므로 알고리즘 개선으로 바로 승격하지 않는다.

### C. 현재 제한에서 불가능하거나 실행하면 안 되는 일

| 작업 | 불가능 판정 근거 |
|---|---|
| 길이 1,000 block으로 `[10^20,10^21)` 전체 tiling | 9×10^17 blocks; 1 microsecond/block여도 약 28,500년, 1 byte/block도 약 0.9 EB |
| block마다 두 primecount 알고리즘을 새로 실행 | endpoint 5개만 약 58분; 전체 tiling은 시간 제한을 압도 |
| dense modulus 510510 LP | 추정 constraints 약 85.2억, COO lower bound 약 825.7 GiB로 RAM 32 GB 초과 |
| 검증 없이 dense modulus 30030 full LP | 보수 추정 20.47 GiB가 32 GB 아래여도 solver 복사·Python 객체 peak 보장이 없어 OOM 위험 |
| 새로운 candidate-cover theorem의 발견을 168시간 내 보장 | 열린 형태의 수론 연구이며 유한 연산처럼 종료시간을 보장할 수 없음 |
| 100 GB 초과 ledger 또는 168시간 초과 queue | 사용자 지정 hard stop 위반 |

“불가능”은 수학적으로 영원히 불가능하다는 뜻이 아니라, 현재의 알고리즘·증명·PC 제한으로 승인 가능한 실험이 아니라는 뜻이다.

## 알고리즘 개선 후보가 되기 위한 정량 문턱

전체 폭 `W=9×10^20`, block 길이 `L`, block당 실제 총비용 `t(L)`, 저장 bytes `b(L)`라 하면 최소 조건은

\[
\frac{W}{L}t(L)\le604800\ \text{seconds},
\qquad
\frac{W}{L}b(L)\le10^{11}\ \text{bytes}
\]

이다. 여기에 각 block이 zero이거나 모든 실제 start를 포함하는 candidate set을 내놓아야 한다.

- 비현실적인 `t=1 microsecond`에서도 `L≥1.488×10^9`가 필요하다. 현재 관측 `q/L≈4.86138×10^-4`이면 이 길이의 q는 약 723,000이므로 70만 배 이상 낮춰야 `q<1` 근처가 된다.
- `b=1 byte/block`에서도 `L≥9×10^9`가 필요하고 현재 q는 약 4.38 million이다.
- 현실적인 `b=100 bytes/block`이면 `L≥9×10^11`, 현재 q는 약 437.5 million이므로 4억 배 이상의 bound 개선이 필요하다.
- 어느 경우에도 unresolved crossing을 별도로 0으로 인증해야 한다.

따라서 단순 floating precision 증가나 `ceil→floor` 1단위 보정은 성능 문턱에 거의 영향을 주지 않는다. 필요한 것은 다음 둘 중 하나다.

1. 큰 L에서도 bound를 수십만–수억 배 낮추고 boundary까지 해결하는 훨씬 강한 certificate
2. zero bound를 만들지 않고도 실제 large-gap start를 모두 포함하며 survivor가 극히 적은 candidate-cover theorem

이 정량 판정을 사전 게이트로 고정한 후, P009에서는 boundary witness가 **수학적으로 가능하고 싸게 검증되는지**만 먼저 확인한다. 이 게이트를 통과해도 전체 알고리즘 후보 판정은 별개다.

## 최종 결론

P008 검토용 문서는 필요한 큰 연결고리를 대부분 포함했지만, 가장 중요한 right-boundary gap과 임의 endpoint의 `pi(B-1)-pi(A-1)` 규칙, `floor` 반올림, endpoint prime state의 의미, exact prime-count 비용을 보완해야 한다. 이 보정 뒤의 P008-A는 타당하다.

좋은 결과가 나온다는 뜻은 단순히 `C_local`이 작아지는 것이 아니다. 먼저 내부 bound가 0까지 내려가고, 이어서 crossing gap까지 싸게 해결되며, 이 비용이 baseline exact search보다 작아야 한다. 그 세 조건을 모두 통과했을 때만 실제 알고리즘 개선 후보가 된다.

실제 phase-A 결과에서는 첫 조건이 L=1,000 한 곳에서만 성립했고 두 번째 조건은 성립하지 않았다. 더 큰 L에서는 첫 조건조차 486배–4.86억 배 부족했다. 따라서 현재 P008은 **구현 PASS, supplied certificate direct-tiling 음성 판정**으로 종결하고, 추가 연산은 P009의 작은 boundary witness와 break-even gate로 제한하는 것이 타당하다.
