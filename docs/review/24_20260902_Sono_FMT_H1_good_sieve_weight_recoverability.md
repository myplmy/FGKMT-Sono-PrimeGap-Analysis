# Sono/FMT H1 good-sieve-weight 복원 가능성·계산 규모 검토

- 작성: 2026-09-02 KST
- 사용자 질문: “어디까지 더 계산해야 특정 (X) 이상에서 부등식이 성립한다고 확인할 수 있는가?”
- H1 판정: `CONSTRUCTIVE_PATH_EXISTS_IN_PRINCIPLE_BUT_QUANTITATIVE_REPROOF_REQUIRED`
- numerical theorem threshold: `X_cert OPEN`
- 실제 전역 최소 threshold: `X_star OPEN`
- machine-readable source trace:
  [`../method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`](../method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json)

> **2026-09-04 H1a 갱신:** 아래 source-tracing에서 제안한 H1a를 수행해 `SIV-06`을
> 모든 정수 (r\ge36)에서 project theorem으로 닫았다. 이 문서의 당시 미완료 서술은 연구
> 이력으로 보존하며, 현재 판정은 10절과
> [`13_Sono_FMT_H1a_finite_r_integral_lemma.md`](../method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md)를 따른다.

## 1. 먼저 답부터

### 지금 조사하는 것이 “부등식이 성립하기 시작하는 하한 (X)”인가?

**대체로 맞지만, 정확히는 두 종류의 (X)를 구분해야 한다.**

이 프로젝트가 현재 이론축에서 먼저 찾으려는 것은 다음을 증명해 주는 계산 가능한 숫자다.

\[
X\ge X_{\mathrm{cert}}
\quad\Longrightarrow\quad
G_1(X)\ge 2\times10^{-17}
\frac{\log X\,\log_2X\,\log_4X}{\log_3X}.
\]

이 (X_{\mathrm{cert}})는 **Sono/FMT 증명을 숫자로 풀어 썼을 때 안전하게 보증되는 시작점**이다.
실제로 부등식이 처음부터 영원히 참이 되는 가장 작은 수 (X_\star)와는 다를 수 있다. 증명은 대개
매우 보수적이므로 보증 시작점이 실제 시작점보다 훨씬 클 수 있다.

사용자가 “FGKMT 부등식”이라고 부른 대상은 scale 관점에서는 맞다. 다만 정확한 계수
(2\times10^{-17})가 붙은 정리는 FGKMT 원 논문의 숨은 상수를 직접 계산한 것이 아니라,
[FMT의 chain large-gap 정리](https://arxiv.org/abs/1511.04468)를 Sono가 explicit하게 만든
부등식이다. 따라서 이 문서에서는 **FGKMT/FMT scale에 대한 Sono explicit inequality**라고 부른다.

### 현재 (10^{20})보다 정확히 몇 자리 더 계산해야 하는가?

현재는 **알 수 없다.** 한 자리, 백 자리, 또는 훨씬 더 큰 범위라는 어떤 숫자도 원문에서 아직
도출되지 않았다. 이유는 최종 계수의 곱셈은 끝났지만, 다음과 같은 중간 조건의 숫자가 비어 있기
때문이다.

- (r_0)이 “충분히 크다”에서 실제 얼마인지
- 여러 (O), (\ll), (o(1)) 안의 상수
- 각 오차가 주항보다 작아지는 최초 (x)
- 여러 실패확률의 합이 1보다 작아지는 최초 (x)
- proof parameter (x)를 모든 실제 (X)에 빈틈없이 옮기는 수치 규칙

즉, 현재 상태는 “목표 높이는 알지만 출발점에서 정상까지 이어지는 계단 몇 개의 높이가 아직
숫자로 적혀 있지 않은 상태”다. 이 숫자들을 복원하기 전에는 (10^{20})에서 몇 배 또는 몇 제곱 더
가야 하는지를 정직하게 계산할 수 없다.

## 2. 세 가지 threshold를 쉬운 말로 구분

| 이름 | 쉬운 뜻 | 현재 상태 |
|---|---|---|
| (X_{\mathrm{emp}}(10^{20})) | 가진 record 자료 범위 안에서 관측상 계속 참인 첫 지점 | `3,814,280`, finite exact |
| (X_{\mathrm{cert}}) | Sono/FMT 증명이 모든 더 큰 (X)에 대해 안전하다고 보증하는 수치 시작점 | `OPEN` |
| (X_\star) | 실제 세계에서 부등식이 그 뒤로 영원히 참이 되는 가장 작은 지점 | `OPEN` |

현재 데이터는

\[
3{,}814{,}280\le X\le10^{20}
\]

의 scale-positive 정수 범위에서 부등식을 exact하게 만족한다. 그러나 이것만으로
(X>10^{20})에서도 계속 참이라고 증명할 수는 없다.

원하는 완전한 결론은 다음 두 조각을 이으면 얻는다.

1. **유한 다리:** (3,814,280)부터 (X_{\mathrm{cert}}) 직전까지 실제 maximal gap을 exhaustive하게
   확인한다.
2. **무한 꼬리:** 수치화된 Sono/FMT 정리로 모든 (X\ge X_{\mathrm{cert}})를 한 번에 덮는다.

(X_{\mathrm{cert}}\le10^{20})가 나오는 행운이 있다면 기존 exhaustive record 자료가 유한 다리의
핵심을 이미 덮는다. (X_{\mathrm{cert}}>10^{20})이면 그 지점까지 새로운 exhaustive coverage가
필요하다. 현재는 (X_{\mathrm{cert}}) 자체가 없으므로 필요한 추가 범위도 없다.

## 3. “연산으로 끝까지 확인”할 때의 예상시간

### 3.1 기존 (10^{20}) 분석이 빨랐던 이유

P003 runner는 7.654초였지만, PC가 (10^{20})까지의 모든 소수를 그 시간에 만든 것이 아니다.
Prime Gap List Project가 이미 exhaustive하게 검증한 maximal-gap record를 읽어 64개 end-bounded
interval을 복원하고 (F,H)를 계산했다. 이미 검증된 record 표가 새 상한까지 제공된다면 같은
정규화 계산은 다시 매우 싸다.

### 3.2 같은 Python prime-stream을 단순 확대하는 설명용 외삽

실제 P013-B에서 관측한 값은 다음과 같다.

| 항목 | 관측값 |
|---|---:|
| 범위 | `10^11 <= gap start < 10^12` |
| 처리 gap start | `33,489,857,205` |
| 1회 analysis | `40,073.308`초, 약 11시간 8분 |
| full recomputation 포함 전체 | 약 23시간 2분 |
| 관측 처리율 | 약 `835,715 gap starts/초` |

소수정리의 로그적분으로 (10^{20}\le p<10^{21})의 gap start 수를 근사하면

\[
\operatorname{li}(10^{21})-\operatorname{li}(10^{20})
\approx1.890644988\times10^{19}
\]

이다. P013-B 처리율이 선형으로 유지된다는 매우 단순한 가정 아래:

| 계산 | 설명용 예상시간 |
|---|---:|
| 한 번 전수 streaming | 약 `716,882년` |
| 같은 범위 full recomputation까지 두 번 | 약 `1,433,765년` |
| P017에서 한 범위에 관측된 `4.3956배`가 그대로 유지된다고 가정한 한 번 계산 | 약 `163,091년` |

이는 **현재 Python recurrence pipeline을 그대로 늘렸을 때의 위험성 설명**일 뿐이다.

- specialized prime-gap search, 분산 서버, 새로운 수학적 skipping을 평가한 수치가 아니다.
- 실제 연산시간의 하한 또는 상한이 아니다.
- P017의 4.3956배가 다른 크기에서도 유지된다는 보장이 없다.
- exhaustive record 발견과 exhaustive coverage 인증의 비용도 서로 다르다.

따라서 “우선 (10^{21})까지 계산해 보자”도 현재 PC에서는 현실적인 다음 단계가 아니다. 더구나
수치 정리 threshold가 (10^{21})보다 작다는 근거도 없다.

### 3.3 proof 상수가 모두 나왔을 때 마지막 계산

반대로 모든 hidden constant와 유효범위를 먼저 수학적으로 복원하면 마지막 산술은 비교적 싸다.

| 마지막 단계 | 예상 계산량 |
|---|---|
| 계수·slack directed interval 검산 | 수초–수분 |
| 후보 proof parameter를 증가시키며 모든 finite inequality 확인 | 수분–수시간 가능 |
| 찾아낸 (X_{\mathrm{cert}})까지 exhaustive finite bridge | (X_{\mathrm{cert}}) 크기와 dataset/search 방법에 따라 미정 |

즉 지금의 병목은 큰 정수를 계산하는 CPU가 아니라, **증명에 생략된 상수들을 엄밀하게 복원하는
수학 작업**이다.

## 4. 누락 상수 하나가 threshold를 얼마나 키울 수 있는가

Sono는 proof parameter를

\[
r=\left\lfloor(\log x)^{1/5}\right\rfloor
\]

로 선택한다. finite proof가 어떤 (r_0)을 요구한다면 (r\ge r_0)을 보장하는 간단한 충분조건은

\[
x\ge\exp((r_0+1)^5)
\]

이다. 이후 construction의 대략적 변환 (X\approx\exp(240x))이 한 번 더 붙는다.

가령 **실제 값이라는 뜻이 전혀 없는 민감도 예시**로 (r_0=2)만 가정해도, 이 거친 조합에서
(X)는 약 (10^{107.55})개의 10진 자릿수를 갖는 규모가 된다. (r_0=2)는 “충분히 큰” 값이라고
주장할 근거가 없고, 이 계산은 (X_{\mathrm{cert}})의 하한·상한·추정값 어느 것도 아니다.
누락된 작은 정수 하나가 중첩 지수 때문에 최종 숫자를 얼마나 폭발시킬 수 있는지만 보여 준다.

이 때문에 현재 (10^{20})와 비교해 “몇 배 더”라고 말하는 방식 자체가 적절하지 않을 가능성이
크다. 먼저 proof의 실제 (r_0)과 각 error threshold를 구해야 한다.

## 5. H1 source tracing: 원문 연결관계

이번 H1은 다음 4개 1차 원문을 대조했다.

1. [Sono 2025](https://doi.org/10.4418/2025.80.2.2), pp. 541–542
2. [Ford–Maynard–Tao, *Chains of Large Gaps Between Primes*](https://arxiv.org/abs/1511.04468),
   Theorem 6, pp. 10–15
3. [Ford–Green–Konyagin–Maynard–Tao, *Long Gaps Between Primes*](https://arxiv.org/abs/1412.5029),
   Theorems 5–6 and Lemma 7.2, pp. 25–38
4. [Maynard, *Dense Clusters of Primes in Subsets*](https://arxiv.org/abs/1405.2593),
   Proposition 6.1, (8.25)–(8.27), Sections 8–9

proof chain은 다음과 같다.

```text
Sono의 explicit coefficient
  -> FMT Theorem 6 good weight
       -> “FGKMT Theorem 5를 보라”
            -> FGKMT Theorem 6 (Maynard Proposition 6.1의 변형)
                 -> Maynard finite-r integrals와 weight moments
                 -> FGKMT Lemma 7.2의 Hypothesis 1
                      -> effective character bound + Bombieri-Vinogradov deduction
```

FMT Theorem 6은 (r_0)을 sufficiently large, (c_0)을 sufficiently small이라고 쓴다. Sono는
FGKMT/Maynard 논증을 따라 (c_0=1/5)을 선택한다고 명시하지만, finite (r_0)과 모든 조건이 동시에
성립하는 공통 시작 (x)는 주지 않는다.

Maynard는 Theorem 3.1의 implied constants가 Hypothesis 1 상수가 effective이면 effectively
computable하다고 명시한다. 이는 중요한 긍정적 증거다. 그러나 “effective”는 “논문에 바로 넣을
숫자가 인쇄돼 있다”는 뜻이 아니다. 실제 proof에는 sufficiently large/small, implied constant,
negligible error absorption이 여러 겹 남아 있다.

## 6. H1 node별 판정

| T1 node | 확인된 것 | 빠진 것 | H1 판정 |
|---|---|---|---|
| `SIV-01` (r_0,c_0) | Sono가 (c_0=1/5)을 인쇄 | finite (r_0), 모든 조건의 공통 시작점 | `DEPENDENCY_BLOCKED` |
| `SIV-02` weight 존재 | weight가 finite sum의 제곱으로 구성돼 symbolic constructive | 모든 근사·uniformity의 수치 bound | `QUANTITATIVE_REPROOF_REQUIRED` |
| `SIV-05` (u\asymp\log r) | leading scale와 (1/4) 계수 구조 | 양방향 finite 상수 | `CONSTRUCTIVE_PATH_IDENTIFIED` |
| `SIV-06` (J_r/I_r) | Maynard (8.27)의 (1+O(1/\log r))와 전 단계 적분식 | (O)-상수, smoothing/tail bound, 최초 (r) | `CONSTRUCTIVE_PATH_IDENTIFIED` |
| `SIV-07` Proposition 6.1 | Hypothesis 1 상수에 대한 effectivity 선언 | Sections 8–9의 모든 implied constant | `QUANTITATIVE_REPROOF_REQUIRED` |
| `SIV-08` Hypothesis 1 | uniform absolute constants·effective character bound의 존재 | Landau–Page/BV/(\psi\to\pi)의 실제 상수·범위 | `QUANTITATIVE_REPROOF_REQUIRED` |
| `SIV-09` moment formulas | 주항과 일부 (\log x)^{-1/10} rate 모양 | rate 앞의 상수와 공통 유효범위 | `QUANTITATIVE_REPROOF_REQUIRED` |
| `SIV-10` secondary absorption | 개별 error 모양 다수 | 전체 slack·failure probability 합성 | `QUANTITATIVE_REPROOF_REQUIRED` |
| `SIV-11` numerical package | symbolic/effective-in-principle chain | 위 모든 numeric input | `DEPENDENCY_BLOCKED` |

### H1의 최종 판정

\[
\boxed{
\text{constructive path는 원칙상 보이지만, 출판본의 단순 대입만으로는 수치화할 수 없다.}
}
\]

- **긍정:** 본질적으로 non-effective한 obstruction은 이번 chain에서 발견되지 않았다.
- **긍정:** `SIV-06` finite-r integral은 독립적인 작은 정량 lemma로 잘라낼 수 있다.
- **부정:** ready-made numerical (r_0), Proposition 6.1 constant, Hypothesis 1 package는 찾지 못했다.
- **부정:** 따라서 지금 threshold calculator나 장시간 CPU runner를 만드는 것은 시기상조다.
- **주의:** 이번 표적 1차 문헌 검색에서 ready-made package를 찾지 못했다는 뜻이지, 전 세계 문헌에
  절대로 없다는 novelty 주장은 아니다.

## 7. 다음 proof 연구 순서와 예상시간

### 1순위 — H1a finite-r integral lemma

- 내용: Maynard (8.25)–(8.27)의 smoothing·tail 적분을 명시 부등식으로 다시 쓰고, 선택한 (r)에
  대해 (J_r/I_r)의 rigorous lower bound를 만든다.
- 이유: H1 중 가장 작게 분리 가능하고, (c_{I,J}=1/4)의 finite 사용 가능성을 직접 판정한다.
- 예상 연구시간: source·수식 추적 1–5일; lemma가 완성된 뒤 interval 계산 수분–수시간.
- 사용자 수행절차: 현재 별도 명령 없음.

### 2순위 — H1b Maynard Proposition 6.1 constant ledger

- 내용: Sections 8–9의 각 lemma에서 상수 의존성과 finite cutoff를 행 단위로 등록한다.
- 이유: `SIV-06` 하나가 성공해도 moment formula가 수치화되지 않으면 good weight는 닫히지 않는다.
- 예상 연구시간: 1차 ledger 2–7일; 완전 정량 재증명은 수주 이상일 수 있다.
- 사용자 수행절차: 현재 별도 명령 없음.

### 3순위 — H1c Hypothesis 1/PAP 공동 추적

- 내용: FGKMT Lemma 7.2가 호출하는 effective Landau–Page, zero-free, Bombieri–Vinogradov,
  (\psi\to\pi) 상수를 실제 함수로 복원한다.
- 이유: Maynard가 effectivity를 이 입력에 조건부로 두므로 독립 root blocker다.
- 예상 연구시간: 수일–수주 이상; 전문 분석수론 검토가 필요할 가능성이 높다.
- 사용자 수행절차: 현재 별도 명령 없음.

### 그 뒤 — T2 slack budget과 threshold calculator

- 선결조건: H1뿐 아니라 PAP·UB·hypergraph·arbitrary-X node도 numeric explicit.
- 예상 연구시간: slack ledger 1–3일, 계산기 구현 1–3일, 첫 계산 수분–수시간.
- 주의: 이 시간이 짧아도 그 전에 필요한 정량 증명 연구는 짧지 않다.

## 8. 사용자에게 지금 요청할 사항

현재 사용자 PC에서 실행할 명령은 없다. 새 prime sweep, WSL, PARI/GP 또는 장시간 runner도
필요하지 않다. 다음 Codex 단계에서 H1a finite-r integral lemma 정식화에 착수할지 승인만 결정하면
된다.

권장 회신:

```text
Sono/FMT H1a finite-r integral lemma 정식화 착수 승인.
```

## 9. 재현에 사용한 수치 근거

- P003: [`../../test_result/202608230503_P003_full_analysis.md`](../../test_result/202608230503_P003_full_analysis.md)
- P013-B: [`../../test_result/202608291712_P013B_result_analysis.md`](../../test_result/202608291712_P013B_result_analysis.md)
- P017: [`../../test_result/202608300229_P017_parallel_calibration_result_analysis.md`](../../test_result/202608300229_P017_parallel_calibration_result_analysis.md)
- T1 원장: [`../method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md`](../method/theory/12_Sono_FMT_T1_proof_obligation_ledger.md)
- H1 machine trace:
  [`../method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json`](../method/theory/data/Sono_FMT_H1_good_sieve_weight_trace_v1.json)

runtime 외삽은 고정 FGKMT Python과 80-dps `mpmath.li`를 사용했다. 새로운 소수 또는 maximal-gap
dataset을 생성하지 않았다.

## 10. 2026-09-04 H1a 실행 결과

H1a는 Maynard (8.27)의 unrestricted product 함수 (F_1)를 Sono가 요구하는 simplex-supported
함수 (F)와 곧바로 동일시하지 않았다. exact one-dimensional envelope와 Cantelli concentration을
사용해 그 사이의 이동을 유한 부등식으로 채웠다.

결과는 다음과 같다.

- 모든 정수 (r\ge36)에서 어떤 허용 함수 (F)에 대해
  (J_r(F)/I_r(F)>\log r/(4r))임을 project theorem으로 증명했다.
- (36\le r\le8103)의 8,068개 정수는 60-dps directed interval로 전수 검사했고 failure는 0이다.
- 정수 (r\ge8104)는 (\log r\ge9)의 단조 해석적 꼬리로 덮었다.
- (r=35)의 실패는 이 보수적 certificate의 실패일 뿐, 다른 함수까지 포함한 불가능성 증명이 아니다.
- 따라서 T1 `SIV-06`은 `EXPLICIT`으로 바뀌지만 H1 전체 판정과 (X_{\mathrm{cert}})는 그대로
  `OPEN`이다.

Sono의 (r=\lfloor(\log x)^{1/5}\rfloor)을 이 한 조건에만 대입하면
(x\ge\exp(36^5)=\exp(60{,}466{,}176))이면 H1a gate를 통과한다. 이 수는 약 26,260,127자리지만,
다른 proof node와 (x\to X) 변환을 포함하지 않으므로 Sono/FMT 정리의 threshold가 아니다.

다음 gate는 H1b Maynard Proposition 6.1 상수 원장이다. H1a 정본과 기계 판독 contract는 각각
[`13_Sono_FMT_H1a_finite_r_integral_lemma.md`](../method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md),
[`Sono_FMT_H1a_finite_r_integral_contract_v1.json`](../method/theory/data/Sono_FMT_H1a_finite_r_integral_contract_v1.json)이다.
