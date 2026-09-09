# H1c-1b.3r1 FGKMT 실제 끝점 교정 타당성 검토

- 작성: 2026-09-09 KST
- 판정: `CORRECTION REQUIRED AND COMPLETED AT THE UNWEIGHTED INPUT LAYER`
- 영향: 기존 H1c-1b.3의 실제 적용 설명은 틀렸지만, 사용한 endpoint upper의 크기는 안전했고
  상위 정리는 아직 OPEN이었으므로 잘못된 theorem threshold나 실험 결과는 생성되지 않았다.

## 1. 무엇이 틀렸는가

기존 검토는 Maynard 2016 Definition (2.1)의 \([T,2T)\)를 확인한 뒤 FGKMT의 실제 호출도
같은 구간이라고 판단했다. 이 판단은 FGKMT 원문 printed p.95의 재정의를 놓쳤다. FGKMT는

\[
\mathcal A(x)=\{n:x\le n\le2x\}
\]

를 사용하며, Theorem 6을 Maynard Proposition 6.1의 “slightly modified form”이라고
명시한다. 따라서 인용된 원정리만 보는 것으로 충분하지 않고, 인용하는 논문이 정의를
변경했는지도 실제 호출점까지 확인해야 했다.

## 2. 수학적 영향

잘못된 과거 변환은

\[
(T,2T]\longrightarrow[T,2T)
\]

이라서 (T)를 더하고 (2T)를 뺐다. 실제 필요한 변환은

\[
(T,2T]\longrightarrow[T,2T]
\]

이라서 (T)만 더한다. 둘 다 한 modulus당 centered correction 절댓값이 1 이하라서
전체 상계 (M_B(T))는 같다. 따라서 H1c-1b.4c의 13개 non-(C_A) component와 H1c-1b.4d의
source-constant 판정은 수치상 무효화되지 않는다.

다만 다음 두 주장을 구분해야 한다.

- **닫힘:** Bordignon/Abel의 ((T,2T]\) unweighted count를 FGKMT Hypothesis 1의
  closed \([T,2T]\) count로 옮기는 일.
- **열림:** Theorem 6의 closed weighted sum에서 FGKMT Section 8 외부 소수집합
  ((T,2T]\)로 돌아갈 때 lower endpoint weight를 제거하고 전체 오차에 흡수하는 일.

후자는 (1/\varphi(q)) 크기의 단순 count atom이 아니라 sieve weight (w(T))를 포함하므로
이번 endpoint-count lemma만으로 해결되지 않는다.

## 3. 검산의 독립성

toy 시험은 정수와 반정수 (T), 여러 (q,a)에서 네 count를 직접 열거한다. source와 closed
target의 centered discrepancy 차이가 정확히 lower-endpoint correction인지 확인하고,
과거 half-open envelope와 새 closed envelope의 **수치값은 같지만 field와 의미가 다름**을
검사한다. 또한 source PDF 두 편의 SHA-256을 고정한다.

이는 원 논문을 재증명하는 계산이 아니라 endpoint 전사 오류를 막는 회귀시험이다.

## 4. 과승격 방지 판정

| 질문 | 답 |
|---|---|
| 기존 실제 target 표기는 맞았는가 | 아니오 |
| endpoint 오차 크기 (M_B(T))는 안전했는가 | 예 |
| density (>T/(2\log T))는 유지되는가 | 예, closed 구간에서는 더 직접적 |
| H1(2) 전체가 이번 교정만으로 닫히는가 | 아니오, 4e 합성이 남음 |
| FGKMT (6.5)의 weighted endpoint가 닫혔는가 | 아니오 |
| `SIV-08`, (X_{\rm cert})가 닫혔는가 | 아니오 |

따라서 올바른 판정은

```text
unweighted FGKMT endpoint semantics = CORRECTED AND CLOSED
numeric endpoint envelope           = PRESERVED
downstream weighted endpoint        = OPEN
SIV-08                              = HARD_BLOCKER
X_cert                              = OPEN
```

이다.
