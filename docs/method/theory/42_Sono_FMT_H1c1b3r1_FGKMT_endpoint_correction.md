# Sono/FMT H1c-1b.3r1 FGKMT 실제 끝점 규약 교정

- 작성: 2026-09-09 KST
- 증거 수준: `PRIMARY-SOURCE CORRECTION / EXACT FINITE BRIDGE`
- 판정:
  `FGKMT_CLOSED_INTERVAL_ENDPOINT_SEMANTICS_CORRECTED / NUMERIC ENVELOPE PRESERVED`
- 기계 판독 정본:
  [`data/Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction_v1.json`](data/Sono_FMT_H1c1b3r1_FGKMT_endpoint_correction_v1.json)
- 검산 구현:
  [`source/h1c1b3r1_fgkmt_endpoint_correction.py`](../../../source/h1c1b3r1_fgkmt_endpoint_correction.py)
- 비판적 검토:
  [`docs/review/48_20260909_H1c1b3r1_FGKMT_endpoint_교정_타당성검토.md`](../../review/48_20260909_H1c1b3r1_FGKMT_endpoint_교정_타당성검토.md)

## 1. 교정 결론

직전 H1c-1b.3은 Maynard 원논문 Definition (2.1)의

\[
\mathcal A(T)=\{n\in\mathcal A:T\le n<2T\}
\]

를 실제 FGKMT 적용구간이라고 기록했다. 그러나 FGKMT는 원문을 그대로 인용하면서도
Definition 2 직전에 별도 정의를 두어

\[
\boxed{\mathcal A(T)=\{n\in\mathcal A:T\le n\le2T\}}
\tag{42.1}
\]

로 바꿨다. FGKMT가 이것을 “slightly modified form”이라고 부르는 Theorem 6과 Section 8의
실제 적용은 이 수정 정의를 따른다. 따라서 actual Hypothesis 1(2)의 identity-form 목표는

\[
P_T^{\rm cl}(q,a)=\#\{p:T\le p\le2T,\ p\equiv a\pmod q\}
\]

와 정확한 전체수 (P_T^{\rm cl})로 중심화한 discrepancy다.

H1c-1b.2와 Abel 변환이 직접 주는 구간은 ((T,2T]\)이다. 실제 FGKMT closed target으로
가는 정확한 식은

\[
\boxed{P_T^{\rm cl}=P_T^{(T,2T]}+1_{\mathbb P}(T)}
\tag{42.2}
\]

이고, 각 나머지류에도 같은 식이 성립한다. 즉 **아래 끝 (T)만 더하며 (2T)는 빼지
않는다.** H1c-1b.3의 half-open 식은 일반 Maynard 문장에는 정확하지만 actual FGKMT 문장에는
적용하지 않는다.

## 2. 왜 수치 오차예산은 살아남는가

(T)가 소수이면 한 modulus (q)와 reduced residue class (a)에서 centered correction은

\[
1_{T\equiv a\pmod q}-\frac1{\varphi(q)}.
\tag{42.3}
\]

(T)가 소수가 아니면 0이다. 어느 경우든 절댓값은 1 이하다. 따라서 modulus family의
크기를 (M_B(T))라 하면 전체 끝점 비용은 여전히

\[
\boxed{M_B(T)\le T^{1/3}}
\tag{42.4}
\]

이다. 과거 half-open 변환도 우연히 같은 크기 (M_B(T))를 사용했다. 그러므로 H1c-1b.4c의
정규화된 끝점 항

\[
2(\log T)^{100r^2+1}T^{-2/3}
\]

은 **의미를 lower-endpoint addition으로 고치면 그대로 안전하다.** 식의 크기가 맞았다는
사실이 과거 target 설명까지 맞았다는 뜻은 아니다.

또 Rosser--Schoenfeld가 세는 ((T,2T]\) 소수는 closed target의 부분집합이므로

\[
P_T^{\rm cl}\ge\pi(2T)-\pi(T)>\frac{3T}{5\log T}
>\frac{T}{2\log T}
\]

이다. H1c-1b.4b의 더 약한 density 하한도 유지된다. 실제 closed target에는 과거처럼 한
소수를 먼저 뺄 필요가 없다.

## 3. 세 구간을 분리해야 하는 이유

| 역할 | 구간 | 현재 처리 |
|---|---:|---|
| Bordignon cumulative difference와 Abel source | ((T,2T]\) | exact |
| FGKMT 수정 Hypothesis 1 / Theorem 6 입력 | \([T,2T]\) | 아래 끝 한 atom을 더해 exact |
| FGKMT Section 8의 외부 소수 (p\) 범위 | ((T,2T]\) | source와 같은 구간 |
| Maynard 원논문의 일반 Definition (2.1) | \([T,2T)\) | 역사적 H1c-1b.3에만 해당 |

FGKMT printed p.101은 외부 (p\in(T,2T]\) 합을 closed (mathcal A(T))의 weight 합으로
옮긴다. (T) 자체가 소수이면 closed 합에는 한 가중항이 더 생긴다. asymptotic 문맥에서는
한 점이라 무시할 수 있지만 numerical threshold 증명에서는 그 가중치까지 명시적으로
상계하고 흡수해야 한다. 이 **downstream weighted endpoint**는 (42.3)의 unweighted
discrepancy와 다른 의무이므로 이번 단계에서 닫았다고 하지 않는다.

## 4. 정확한 상태

| 항목 | 상태 |
|---|---|
| Maynard 원문 \([T,2T)\) bridge | `HISTORICALLY EXACT, NOT ACTUAL FGKMT TARGET` |
| FGKMT 수정 \([T,2T]\) unweighted endpoint bridge | `EXACT FINITE BRIDGE CLOSED` |
| H1c-1b.4c 수치 endpoint envelope | `PRESERVED WITH CORRECTED SEMANTICS` |
| closed target density (>T/(2\log T)) | `PRESERVED` |
| Section 8 외부합으로 돌아가는 weighted endpoint | `OPEN` |
| Hypothesis 1(2) full absorption / `SIV-08` | `OPEN / HARD_BLOCKER` |
| (X_{\rm cert}) | `OPEN` |

이번 교정은 actual prime 계산을 하지 않았고 새 Python package나 Lean이 필요하지 않았다.
사용자 수행절차는 **별도 수행절차 필요없음**이다.

## 5. 다음 gate

H1c-1b.4e에서 다음을 분리해 합성한다.

1. 수정된 closed target에 H1c-1b.4a--4d의 density·source constant·흡수식을 적용한다.
2. Hypothesis 1의 쉬운 조건 (1),(3), 공통 (B), coefficient와 scale 조건을 같은 cutoff에서
   확인한다.
3. actual identity-form Hypothesis 1 입력이 닫혀도, Section 8 외부합의 가중 lower-endpoint와
   Theorem 6 나머지 상수는 별도 의무로 남긴다.
4. 이 구분 뒤에만 `SIV-08`의 상태를 재판정한다.
