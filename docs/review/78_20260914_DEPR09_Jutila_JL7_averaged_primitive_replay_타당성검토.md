# DEP-R09 Jutila JL7 averaged primitive replay 타당성검토

- 검토일: 2026-09-14 KST
- 대상: [Theory 71](../method/theory/71_Sono_FMT_DEPR09_Jutila_JL7_averaged_primitive_replay.md)
- 판정: **PASS WITH STRICT SCOPE LIMIT**
- 닫힌 범위: primitive nonprincipal, near-one, variable-modulus averaged branch
- 닫히지 않은 범위: printed all-alpha theorem, pointwise PAP, fixed Sono coefficient,
  numerical \(X_{\rm cert}\)

## 1. 한눈에 보는 판정

이번 재구성의 핵심 결론은 타당하다. Jutila 식 (3.7)의 phase
\(|\eta_j|=q_j/\varphi(q_j)\)는 각 detector의 \(\varphi(q_j)/q_j\)를 정확히 지운다.
primitive character의 product가 principal인 경우는 같은 primitive character일 때뿐이고,
그때 두 residue totient factor가 phase weight의 제곱과 정확히 상쇄된다. 따라서 modulus
개수 \(Q\)를 residue에 다시 곱하지 않아도 된다.

다만 이 판정은 Theory 71에 적힌 실제 좁은 범위에서만 유효하다. 특히

\[
 0<1-\alpha\le\theta\le\frac1{21},\qquad
 D=Q^2T
\]

의 primitive nonprincipal branch다. Jutila의 인쇄된 모든 \(4/5\le\alpha\le1\) 범위나
Gallagher--Maier의 pointwise prime lower bound까지 완성됐다고 읽으면 틀린다.

> **쉬운 설명:** 여러 상자를 한꺼번에 셀 때 상자마다 붙은 할인율이 서로 달랐는데,
> 원 논문의 가중치를 쓰면 그 할인율이 정확히 없어지는 것을 확인했다. 상자 수 자체를
> 한 번 더 곱할 이유도 없었다. 하지만 이 상자 수 계산을 실제 소수 개수 보증으로 바꾸는
> 마지막 배송 과정은 아직 검증하지 않았다.

## 2. 왜 이 결과가 이전보다 진전인가

Theory 70은 한 fixed modulus \(q\)의 selected system만 다뤘다. 이를 \(q\le Q\)에
그대로 합하면 최악에는 modulus마다 한 번씩 합계가 늘어 raw \(Q\) 손실이 생긴다.
Jutila 식 (3.7)은 처음부터 모든 primitive character를 한 generalized Halasz inequality에
넣으므로 그 손실을 피한다.

이번 단계는 다음 세 항목을 동시에 확인했다.

1. detector의 modulus별 totient factor를 phase가 제거한다.
2. principal residue는 같은 character끼리만 남으며 totient factor가 완전히 상쇄된다.
3. 서로 다른 character pair는 product conductor \(\le Q^2\)라 공통 \(D=Q^2T\) contour가
   덮고, phase의 최악 손실 36은 기존 strict absorption의 36과 같은 위치에 들어간다.

따라서 Theory 70의 selected-system coefficient

\[
 C_J(\theta)=\frac{884000}{9(1-\theta)^2\theta^6}
\]

를 바꾸지 않고 averaged near-one branch에 재사용할 수 있다.

## 3. 가장 위험했던 오류와 방지 여부

### 3.1 Theory 64의 \(D=qT\)를 글자만 바꾸는 오류

가변 modulus에서 \(D=Q^2T\)는 각 \(q_jT\)보다 훨씬 클 수 있다. 그러므로 기존
detector cutoff를 아무 증명 없이 재사용하면 안 된다. Theory 71은 Mellin quantity

\[
 A_j=(q_jT)^{1/2}D^{1/2+9\theta}
\]

에 대해 하계와 상계를 따로 증명했다.

- \(A_j\le D^{1+9\theta}\): power condition용
- \(A_j\ge D^{1/2+9\theta}\): 음의 거듭제곱 오차 decay용

Python 시험은 averaged decay exponent가 fixed-modulus exponent보다 작다는 사실까지
검사한다. 이는 작은 \(q_j\)에서 더 강한 fixed-modulus decay를 잘못 가져오는 오류를
막는다.

판정: **교정됨.**

### 3.2 `principal pair`를 \(j=k\)라고 오해하는 오류

같은 character에 서로 다른 높이의 선택 영점이 여러 개 있을 수 있다. 따라서
principal pair는 \(\chi_j=\chi_k\)이지 반드시 index \(j=k\)는 아니다. Theory 71은
Theory 69의 same-character height-row sum을 그대로 보존했다.

판정: **교정됨.**

### 3.3 raw \(Q\) factor를 추가하는 오류

primitive character equality가 conductor equality를 강제하고 residue가 character별
대각화되므로, 각 row는 한 번만 계산된다. phase·residue·pseudocharacter factors의
exact product는 1이다. 별도 \(Q\) 또는 \(Q^2\) multiplier는 없다.

판정: **추가 factor 없음이 타당함.**

### 3.4 phase 손실을 residue에서 지우고 off-diagonal에서도 잊는 오류

residue에서는 phase가 정확히 상쇄되지만 off-diagonal에서는 상쇄되지 않는다. 각
\(q_j/\varphi(q_j)\le6L\)를 써서 pair마다 \(36L^2\)를 지불한다. 이 \(L^2\)는
detector normalization으로 나눈 뒤 36만 남는다.

판정: **누락 없이 계상됨.**

## 4. 두 번째 Jutila 논문의 역할을 과장하지 않았는가

Jutila의 *Zero-density estimates for L-functions*는 primitive conductor \(\le Q\)인
variable-character Dirichlet polynomial을 별도 case로 다루고, Lemma 3(ii)에
\(N+(RT)^{1/2}Q\) 형태의 구조를 준다. 이는 가변 conductor를 한꺼번에 다루는 방법이
표준적인 구조라는 좋은 교차검증이다.

이 PDF는 native text가 사실상 없는 5개 landscape scan이므로 OCR은 위치 찾기에만
사용했다. 각 PDF page에 함께 수록된 printed pp.55--62의 모든 인쇄면을 렌더 원문으로
대조했으며, 핵심 수식 판독을 OCR 문자열만으로 확정하지 않았다.

그러나 해당 논문은 \(\ll_{\varepsilon,k}\), \((QT)^\varepsilon\), mean fourth-power
입력에 수치 multiplier를 남긴다. 또한 Jutila 식 (3.7)의 modulus-dependent
pseudocharacter kernel을 같은 상수로 직접 처리한다고 쓰지 않는다. 따라서 이를
“식 (3.7)의 수치 증명”으로 인용하지 않고 구조 교차검증으로만 사용한 판단이 타당하다.

## 5. Lean과 Python이 실제로 보증하는 범위

Python은 다음을 보증한다.

- source PDF hash와 판독 방식 고정
- exact phase·residue cancellation
- off-diagonal phase factor 36의 fail-closed 검사
- common detector cutoff와 세 \(\theta\) 진단점
- root 상태가 계속 false임

Lean은 다음 유한 대수만 kernel에서 검사한다.

- \((q/\varphi)(\varphi/q)=1\)
- \((q/\varphi)^2(\varphi/q)^2=1\)
- 두 \(6L\) 상계에서 36이 나오는 방향
- Mellin scale의 상·하 envelope와 exponent 방향
- averaged terminal이 Theory 70과 같은 \(A,B,E\)식으로 환원되는 계수 대수

generalized Halasz inequality, primitive conductor uniqueness, complex contour 이동과
source analytic bounds 전체는 Lean에서 새 axiom으로 선언하지 않는다. 그러므로 Lean
PASS는 외부 해석적 정리의 독립 형식증명이 아니다.

## 6. \(X_{\rm cert}\) 연구에 미치는 실제 영향

이번 결과로 “여러 modulus를 평균낼 때 fixed-modulus 상수에 raw \(Q\) 손실이 생기는가”라는
의문은 actual near-one branch에서 해소됐다. 이는 `JL7-AVERAGED`를 좁은 범위에서
계산 가능한 입력으로 바꾼 실질적 진전이다.

하지만 \(X_{\rm cert}\) 계산기는 아직 만들 수 없다. 이유는 다음과 같다.

1. averaged zero count는 각 residue class의 prime count lower bound와 같은 명제가 아니다.
2. Gallagher--Maier proof에서 이 near-one family가 정확히 어떤 kernel과 exceptional
   character 조건으로 들어가는지 아직 수치 재생하지 않았다.
3. principal term, exceptional zero, prime powers, \(\psi\to\pi\), endpoint와 모든
   cutoff의 maximum이 남아 있다.
4. 최종 PAP coefficient가 필요한 최소값 약 0.863831...을 넘는지도 아직 계산할 수 없다.

따라서 이번 진전은 **최종 문을 열 열쇠의 한 부품을 완성한 것**이지, 문이 열린 것은 아니다.

## 7. 남은 리스크

| 리스크 | 현재 통제 | 후속 필요 |
|---|---|---|
| 식 (3.7) complex inequality 전체의 형식증명 부재 | peer-reviewed 원문 식을 source premise로 고정 | PAP 합성 전에 필요한 exact specialization만 재대조 |
| primitive equality와 conductor uniqueness의 Lean 미형식화 | 표준 source 사실로 분리하고 local axiom 금지 | 필요할 때 Mathlib character API 가능성 검토 |
| printed all-alpha theorem 미완 | near-one 결과로 명확히 제한 | PAP가 away-from-one을 실제 요구하는지 먼저 확인 |
| decimal cutoff의 directed rounding 부재 | symbolic max 식이 엄밀 판정 | 최종 calculator 직전에 interval arithmetic 또는 rational fallback |
| common \(\mathcal B_q\) envelope가 매우 거침 | cutoff 지배항으로 투명하게 기록 | PAP 전체가 닫힌 뒤에만 최적화 가치 평가 |

## 8. 권장 다음 순서

1. **Gallagher--Maier source call map — 6--14시간**
   - zero family, height integral, exceptional character와 modulus exclusion을 페이지·식 단위로
     고정한다.
   - near-one Theory 71만으로 충분한지 먼저 판단해 불필요한 all-alpha 재증명을 피한다.
2. **averaged density-to-prime-sum finite transfer — 12--30시간**
   - 각 zero contribution의 multiplier와 decay를 한쪽 prime-count error budget으로 합친다.
3. **principal·prime-power·endpoint package — 8--20시간**
   - 비주영점 오차와 섞지 말고 별도 예산으로 닫는다.
4. **PAP coefficient capacity 재평가 — 4--10시간**
   - 실제 \(C_{\rm PAP}\), 공통 cutoff가 생긴 뒤에만 fixed \(2\times10^{-17}\) 유지 여부를
     계산한다.
5. **threshold calculator — 모든 root가 닫힌 뒤**
   - 그 전 장시간 prime sweep은 증명 공백을 메우지 못하므로 수행하지 않는다.

현재 단계에는 추가 Python package, Lean 설치 변경 또는 사용자 장시간 CPU 계산이 필요 없다.

## 9. 참고문헌

- M. Jutila, *On Linnik's constant*, Math. Scand. 41 (1977), 45--62,
  DOI [10.7146/math.scand.a-11701](https://doi.org/10.7146/math.scand.a-11701).
- M. Jutila, *Zero-density estimates for L-functions*, Acta Arith. 32 (1977),
  55--62, DOI
  [10.4064/aa-32-1-55-62](https://doi.org/10.4064/aa-32-1-55-62).
