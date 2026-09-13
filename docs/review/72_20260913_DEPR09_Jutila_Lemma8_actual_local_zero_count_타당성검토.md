# DEP-R09 Jutila Lemma 8 actual 국소 영점 개수 타당성검토

- 작성일: 2026-09-13 KST
- 상세 수식 정본: [Theory 65](../method/theory/65_Sono_FMT_DEPR09_Jutila_Lemma8_actual_local_zero_count.md)
- 기계 원장: [JL8 local count v1](../method/theory/data/Sono_FMT_DEPR09_Jutila_Lemma8_local_count_v1.json)
- 판정: **actual near-one 호출은 명시화 / 전체 density·PAP·\(X_{\rm cert}\)는 미완성**

## 1. 무엇을 해결했는가

Jutila의 Lemma 8은 “작은 상자 안에 영점이 너무 많이 몰리지 않는다”는 장치다. 원문은
정확한 상자 모양은 주지만, 상자당 최대 개수 앞의 배수를 `≪`로 숨겼다. 이 숨은 배수는
컴퓨터가 계산할 수 있는 \(X_{\rm cert}\)를 만들 때 그대로 둘 수 없다.

McCurley 1984의 숫자가 적힌 로그미분 공식과 네 lemma를 재조합한 결과, 실제 Jutila
증명에서 사용하는 \(r\le1/21\)의 얇은 상자에는

\[
 N_{\square}<3+r\log(q(1+|t_0|))
\]

개의 영점만 들어간다는 보수적 명시 상계를 얻었다. Jutila의 strip을 짝수·홀수 두 묶음으로
나누는 단계까지 포함하면 전체 nonprincipal 영점 수는

\[
 N_{\rm nonprin}\le2J\{3+r\log(2qT)\}
\]

로 바뀐다. 여기서 \(J\)는 두 well-spaced 묶음 중 큰 쪽의 대표 영점 개수다.

> 쉬운 예: 책장 칸마다 책이 몇 권 들어가는지 원 논문은 “대략 제한된다”고만 했다.
> 이번에는 한 칸에 들어가는 책 수를 `3 + 폭×로그크기`로 적었고, 홀수·짝수 책장을
> 합칠 때 필요한 2배도 빠뜨리지 않았다.

## 2. 왜 이 결론이 타당한가

1. McCurley 식 (5)의 Dirichlet-series coefficient가 모두 양수여서 임의 character의
   로그미분 항을 principal character 항으로 아래에서 제어할 수 있다.
2. McCurley Lemma 3이 그 principal 항을 \(1/r\)보다 작게 제한한다.
3. Lemmas 1--2는 감마항에 exact 상수 `0.3918`을 주고, 식 (13)과 Lemma 4는 각 영점이
   양의 Stechkin kernel을 기여하게 한다.
4. 상자 안 영점 하나의 kernel이 최소 \(3/(8r)\)라는 유리 부등식을 별도로 증명했다.
5. imprimitive character의 추가 Euler-factor 영점은 실수부 0에만 있어 실수부가 거의
   1인 이번 상자에는 들어오지 않는다.

이 중 1--3의 analytic identity는 peer-reviewed McCurley 원문에 있다. 4와 strip 전달의
유한대수는 문서·Python·Lean으로 서로 다른 방식에서 점검했다. 5의 Euler-factor identity와
닫힌 \(\beta=1\) 경계의 비소멸 사실은 문서에서 source analytic 입력으로 보존하며 아직
Lean 독립증명으로 과장하지 않는다. source theorem을 Lean의 local axiom으로 선언하지
않으며 `sorry`, `admit`도 사용하지 않는다.

## 3. 채택하지 않은 지름길

| 후보 | 채택 여부 | 이유 |
|---|---|---|
| Turan의 `a2 about 1/2` | 미채택 | `about`은 exact directed constant가 아님 |
| Gallagher의 disk `≪ r log T` | 구조만 사용 | multiplier·최초 범위가 숨음 |
| Bennett et al. global \(N(T,\chi)\) 차분 | 미채택 | 작은 창 폭 \(r\)에 비례하는 이득을 잃음 |
| Prachar p.331 숫자 추정 | 금지 | 원페이지가 access-restricted이고 snippet에 exact 숫자가 없음 |
| McCurley 공식의 직접 합성 | 채택 | 필요한 숫자와 범위가 인쇄돼 있고 actual square를 직접 덮음 |

따라서 “정확한 옛 숫자를 못 찾았으니 임의로 큰 숫자를 넣었다”가 아니다. 같은 목적을
달성하는 더 상세한 peer-reviewed 명시식에서 새로운 보수적 숫자를 증명했다.

## 4. 아직 해결되지 않은 것

이번 결과는 local box 하나와 strip-to-\(J\) 전달까지만 닫는다. 다음이 남아 있다.

- Jutila Lemma 7의 Halasz 합을 실제 식 (3.6)에 넣었을 때 생기는 multiplier
- Theory 66에서 교정한 식 (3.6)의 theta-dependent Barban--Vehov 계수와 finite
  \(\log\log D/\log D\) 보정의 종단 흡수. Theory 60의 고정 `37.769894`는
  Theorem 1-prime branch에만 해당한다.
- Theory 64의 detector lower bound와 이번 local factor의 공통 cutoff
- Theorem 1-prime density에서 Gallagher/Maier PAP까지의 multiplier·exception 처리
- 최종 fixed \(2\times10^{-17}\) coefficient budget과 numerical \(X_{\rm cert}\)

즉 “상자당 영점 수” 부품은 고쳤지만, 상자들을 모두 합쳐 최종 prime-distribution
부등식으로 만드는 조립은 아직 남았다.

## 5. 현재 상태와 다음 권장 작업

```text
JL5 finite lower bound                 = EXPLICIT SOURCE REPLACEMENT
JL6 actual detector                    = PARAMETERIZED EXPLICIT
JL8 actual near-one local count        = EXPLICIT SOURCE REPLACEMENT
JL8 printed unrestricted statement     = OPEN
Jutila (3.6) terminal density           = OPEN
PAP-11 / DEP-R09                        = OPEN
fixed 2e-17                             = NOT INDEPENDENTLY CERTIFIED
X_cert                                  = OPEN
threshold calculator                    = NOT READY
long CPU computation justified now      = NO
```

Theory 65 반영 뒤 Lean 전수 원장은 66개 theory 문서의 display 1,163식을 모두 등록했다.
declaration 161개, 금지 proof escape 0건이며 새 finite algebra는 커널 검사를 통과했다.

다음에는 Jutila 식 (3.6)의 종단 합성을 수식별로 해체하는 것이 가장 효율적이다. 이미 숫자가
생긴 JL5·JL6·JL8을 다시 조사하는 것보다, 이 숫자들이 최종 density multiplier에 어떻게
들어가는지 확인해야 다음 blocker가 정확히 드러난다. 예상 연구시간은 문헌·대수 작업
4--12시간이며 사용자 PC의 장시간 계산은 아직 필요하지 않다.

## 6. 사용자 수행절차

별도 수행절차 필요 없음. 새 라이브러리 설치, Lean 설정 변경, 소수 탐색 실행도 현재는
필요하지 않다.

## 7. 참고문헌

- M. Jutila, [*On Linnik's constant*](https://doi.org/10.7146/math.scand.a-11701).
- K. S. McCurley,
  [*Explicit Zero-Free Regions for Dirichlet L-functions*](https://doi.org/10.1016/0022-314X(84)90089-1).
- P. X. Gallagher,
  [*A Large Sieve Density Estimate near sigma=1*](https://doi.org/10.1007/BF01403187).
- M. A. Bennett, G. Martin, K. O'Bryant and A. Rechnitzer,
  [*Counting Zeros of Dirichlet L-Functions*](https://doi.org/10.1090/mcom/3599),
  [arXiv:2005.02989](https://arxiv.org/abs/2005.02989).
