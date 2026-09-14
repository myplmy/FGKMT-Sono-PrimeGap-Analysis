# DEP-R09 사전 절댓값 moment·pointwise PNT source 타당성검토

- 작성일: 2026-09-14 KST
- 기술 정본: [Theory 76](../method/theory/76_Sono_FMT_DEPR09_preabsolute_moment_pointwise_PNT_source_audit.md)
- 기계 원장: [pre-absolute moment source screen v1](../method/theory/data/Sono_FMT_DEPR09_preabsolute_moment_source_screen_v1.json)
- 최종 판정: **기존 공개 명시적 후보를 그대로 넣어서는 R09가 닫히지 않지만,
  Maier가 실제로 필요로 하는 합계만 제어하는 second-moment 경로는 연구할 가치가 있다.**

## 1. 무엇을 알아보았나

직전 연구에서 현재 Gallagher--Jutila 방식은 모든 오차를 절댓값으로 바꾼 뒤 더하기 때문에
허용 예산보다 너무 큰 상계가 남는다는 것을 확인했다. 이번에는 다음 질문을 조사했다.

> 오차의 부호가 사라지기 전에 서로 상쇄시키거나, 각 산술진행을 모두 따로 정확하게
> 맞추지 않고 Maier가 마지막에 사용하는 전체 소수 개수만 정확하게 맞추면 되는가?

결론은 “수학적으로 가능한 정확한 충분조건은 찾았지만, 그 조건을 실제로 보장하는 완전 수치
정리는 아직 찾지 못했다”이다.

## 2. Maier 증명을 다시 읽어 발견한 중요한 여지

Maier의 원래 증명은 여러 세로 열로 된 표를 만든다. 각 열은 같은 나머지값을 갖는
산술진행이다. 인쇄된 증명은 허용되는 모든 열마다 소수 개수가 예상과 비슷하다고 보장한다.

하지만 다음 단계가 실제로 쓰는 것은 각 열의 개별 성적표가 아니라 **모든 허용 열을 합친
총 소수 개수**다.

쉽게 비유하면 다음과 같다.

- 기존 방식: 반 학생 30명 모두가 목표 점수와 1점 이내인지 확인한다.
- 새 가능성: 이후 계산에 반 전체 평균만 필요하다면, 개인 점수 대신 총점 오차만 확인한다.

개별 오차가 서로 일부 상쇄된다면 총점 조건이 더 약할 수 있다. 실제 대수 계산에서는 허용
residue가 $M$개일 때 second-moment 허용 예산이 기존 pointwise 예산보다 정확히 $M$배 커진다.
이 implication은 Lean으로 검증할 대상이다.

다만 아무 평균정리나 사용할 수는 없다. 평균에서 “좋은 modulus 하나”가 있다는 것과 Maier가
필요로 하는 **특정 good primorial**이 좋다는 것은 다른 주장이다. 이 quantifier 차이를 해결하는
정리가 필요하다.

## 3. 조사한 명시적 정리들이 통과하지 못한 이유

### Akbary--Hambrook과 Sedunova

두 논문은 상수가 실제 숫자로 적힌 Bombieri--Vinogradov형 평균정리를 제공한다. 이것은 매우
유용한 결과이지만 현재 예산에 그대로 대입하면 상계식의 가장 작은 기본항부터 너무 크다.

| source | direct certificate의 최소 진단 | 허용 예산과의 비 |
|---|---:|---:|
| Akbary--Hambrook | 612.7196 이상 | $e^{-2}$의 4,527배 초과 |
| Sedunova | 1,853.2524 이상 | $e^{-2}$의 13,693배 초과 |

이 숫자는 실제 소수분포 오차가 그렇게 크다는 뜻이 아니다. 논문이 제공하는 안전한 최악의
상계만으로는 우리 합격 기준을 증명할 수 없다는 뜻이다.

### Bennett et al.

이 논문은 각 산술진행을 직접 제어하므로 구조상 가장 가까운 후보였다. 그러나 큰 modulus에서
정리를 쓰려면

\[
 d\ge0.03\sqrt q(\log q)^2
\]

가 필요하다. $q>10^5$가 시작되는 바로 그 경계에서도 필요한 $d$는 약 1,257이고, 현재 Sono
계수를 유지할 수 있는 최대 capacity는 186이다. 첫 primorial $510510$에서는 필요한 $d$가
약 3,703이다. 즉 큰 수를 더 넣으면 해결되는 것이 아니라 **정리의 적용 조건과 현재 증명
설계가 처음부터 겹치지 않는다.**

그 cutoff를 잠시 무시해도 $q=510510,d=186$의 published uniform error certificate는
0.2356으로, 현재 near budget 0.1353보다 약 1.741배 크다.

## 4. 이번 결과가 증명한 것과 증명하지 않은 것

증명·검증한 것:

- Maier의 최종 prime-mass 단계에는 aggregate residue error 조건이 충분하다.
- 그 aggregate 조건은 특정 character second moment 상계로부터 정확히 따라온다.
- Akbary--Hambrook과 Sedunova의 명시적 L1 RHS를 그대로 쓰는 certificate는 현재 예산을
  통과하지 못한다.
- Bennett large-$q$ branch는 $d\le186$과 유한 범위 자체가 겹치지 않는다.

증명하지 않은 것:

- 실제 소수분포 오차가 위 상계 숫자보다 크다는 주장
- 모든 second-moment·cancellation 방법이 실패한다는 주장
- 기존 문헌 어디에도 필요한 정리가 없다는 전 세계적 부재 증명
- Sono의 fixed coefficient가 틀렸다는 주장
- numerical $X_{\rm cert}$의 값 또는 상한

## 5. 다른 variance 문헌은 왜 바로 쓸 수 없나

Friedlander--Goldston은 정확히 residue-class variance를 연구한다. 하지만 이번에 확인한 범위에서는
Maier의 무한 primorial sequence, $Y=q^d$의 $d\le186$, numerical multiplier와 공통 cutoff를
동시에 만족하는 unconditional 정리를 복원하지 못했다.

Baker의 few-exception theorem은 좋은 modulus를 선택하는 아이디어와 가깝다. 그러나 modulus들이
pairwise coprime이어야 하고 상수도 numerical package가 아니다. Maier primorial들은 앞의
primorial이 뒤의 primorial을 나누므로 이 조건에 맞지 않는다.

고전 Barban--Davenport--Halberstam 평균도 평균적으로 좋은 분포를 말하지만, 평균에서 좋은
modulus와 Maier Lemma 1의 good primorial이 동일하다는 추가 증명이 없다.

## 6. $X_{\rm cert}$에 미치는 실제 영향

이번 단계에서 $X_{\rm cert}$의 수치 범위를 새로 얻지는 못했다. 따라서 사용자 CPU로 장시간
소수를 계산하거나 threshold calculator를 만드는 단계가 아니다.

대신 병목을 더 정확히 좁혔다. 다음에 필요한 정리는 대략 다음 문장이다.

> Maier가 선택하는 good primorial $q$와 그 admissible residue 집합 $\mathcal A$에 대해,
> character explicit-formula contributions의 second moment가
> $\varepsilon^2M Y^2/\varphi(q)$ 이하임을 numerical 상수와 finite cutoff까지 보장한다.

이 정리를 기존 문헌에서 찾거나 새로 증명할 수 있다면 R09의 구조적 돌파구가 된다. 그때
principal/exceptional character, prime powers, endpoint, $\psi\to\pi$를 합쳐 처음으로
$X_{\rm cert}$ 후보 cutoff를 계산할 수 있다.

## 7. 권장 다음 연구 순서

1. **restricted-residue / individual-primorial variance source audit**
   - 목적: 위 missing theorem과 가장 가까운 선행 정리를 찾는다.
   - 예상: 문헌 선별 1--3주.
2. **Maier admissible set의 character energy 계산**
   - 목적: 일반적인 $M$배 이득보다 더 강한 구조적 이득이 있는지 증명한다.
   - 예상: 대수·조합 분석 2--6주; 작은 exact toy는 수분--수시간.
3. **새 theorem target 정식화 및 proof decomposition**
   - 기존 drop-in이 없을 때만 수행한다.
   - 예상: 1--3개월 설계, 실제 analytic proof는 6--24개월 이상 가능.
4. **R09 종단 수치 합성**
   - 위 gate 통과 후 principal/exceptional·endpoint·prime-power·$\psi\to\pi$를 결합한다.
   - 예상: 1--3개월.

현재 사용자 수행절차는 없다. 별도 설치나 장시간 연산은 필요하지 않다.

## 8. 최종 판정

이번 연구는 $X_{\rm cert}$ 숫자를 얻은 성공은 아니다. 대신 다음 두 가지를 명확히 했다.

1. Bennett pointwise 정리처럼 겉으로 가장 가까운 기존 명시적 결과도 현재 capacity와 범위가
   겹치지 않는다.
2. 기존 pointwise 조건보다 약한 aggregate second-moment 조건이 Maier의 실제 downstream에는
   충분하며, 이것이 다음에 집중해야 할 정확한 연구 목표다.

따라서 상태는 다음과 같다.

- `PAP-11`: `OPEN`
- `DEP-R09`: `OPEN`
- fixed $2\times10^{-17}$: 프로젝트 독립 인증 전
- numerical $X_{\rm cert}$: `OPEN`
- 다음 유망 경로: `RESTRICTED-RESIDUE / INDIVIDUAL-PRIMORIAL MOMENT SOURCE OR NEW THEOREM`

## 9. 참고문헌

정확한 source statement, printed page, DOI·arXiv, local hash는 Theory 76 §13과 machine
ledger에 기록했다. 핵심 공개 원문은 Akbary--Hambrook
[arXiv:1309.2730](https://arxiv.org/abs/1309.2730), Bennett et al.
[arXiv:1802.00085](https://arxiv.org/abs/1802.00085), Baker
[arXiv:1905.12488](https://arxiv.org/abs/1905.12488), Sedunova
[DOI 10.5802/pmb.24](https://doi.org/10.5802/pmb.24), Friedlander--Goldston
[DOI 10.1093/qmath/47.3.313](https://doi.org/10.1093/qmath/47.3.313)이다.
