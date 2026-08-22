# 연구 작업지시서: FGKMT-Sono 대형 소수간격 하한과 실제 maximal prime gap의 경험적 비교 분석

## 1. 연구 목적

검증된 maximal prime-gap records를 이용하여 실제 maximal gap \(G(x)\)를 복원하고, Ford–Green–Konyagin–Maynard–Tao(FGKMT)의 large-gap asymptotic scale에 대한 정규화값 \(H(x)\)를 계산한다.

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n),
\]

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},
\]

\[
H(x)=\frac{G(x)}{F(x)}
\]

를 정의하고 실제 \(H(x)\)의 변화와 lower envelope를 분석한다. 본 연구에서 \(G(x)\)의 record jump 위치는 gap의 끝 소수 \(p_{n+1}\)이며, 이후 모든 표·그래프·통계에서 이 end-bounded 정의를 정본으로 사용한다.

특히 다음을 조사한다.

- \(H(x)\)가 \(x\)의 증가에 따라 어떤 장기적 추세를 보이는지
- maximal-gap record 사이에서 \(H(x)\)가 어떻게 감소하고 새로운 record 발생 시 어떻게 회복되는지
- \(H(x)\)의 running minimum 또는 empirical lower envelope가 \(x\)의 증가에 따라 어떻게 변화하는지
- Wolf 계열의 경험적 관찰과 실제 데이터가 어느 정도 일치하는지
- Sono가 explicit하게 제시한 \(c_{\mathrm{LG}}\ge2\times10^{-17}\) 및 이에 대응하는 \(G(x)\ge2\times10^{-17}F(x)\)와 실제 maximal gap 사이에 어느 정도의 격차가 존재하는지
- 이 격차가 \(x\)의 증가에 따라 줄어드는지, 증가하는지, 특정 패턴을 보이는지 또는 상당히 느리게 변화하는지
- 계산 범위 내에서 이론적 lower bound가 실제 데이터와 어떤 관계를 가지며, 그 관계에 특이한 구조나 새로운 패턴이 존재하는지

본 연구의 목적은 유한한 계산 결과를 이용해 FGKMT 또는 Sono의 무한 범위 정리를 재증명하거나 검증하는 것이 아니다. 또한 계산 범위에서 부등식이 성립한다는 사실만으로 그 부등식이 모든 더 큰 \(x\)에서도 성립한다고 주장하지 않는다.

대신 실제 maximal prime-gap 데이터와 이론적 large-gap scale 사이의 관계를 정량적으로 분석하고, 그 결과에서 나타나는 empirical behavior 및 lower-envelope의 구조를 확인한다. 관찰된 패턴이 기존 이론과 어떤 관계가 있는지 검토하고, 필요하다면 이를 새로운 수론적 추측, 명시적 임계값 연구 또는 후속 이론적 연구로 발전시킬 가능성도 탐색한다.

### 1.1 실행 승인 경계

P002 제한 pilot은 계산·자동검증까지 완료됐고 사용자 그래프 시각 QA를 기다린다. 사용자가 허가한 범위는 `x=16`, `x=3,814,280` 및 그 지점부터 연속 5개 end-bounded record interval이었다. 전체 `10^20` 분석은 별도 허가 전까지 수행하지 않는다.

사용자 허가 전에는 다음을 수행하지 않는다.

- allgaps.sql과 schema.sql 다운로드
- raw 또는 validated 실제 dataset 생성
- 실제 maximal-gap record 계산
- test_result의 표·그래프·통계·결과 보고서 생성

Codex는 먼저 연구 목적, end-bounded \(G(x)\), iterated-log \(F(x)\), 데이터 원천과 exhaustive 범위, 계산·검증·해석 방법을 사용자에게 설명한다. 사용자가 같은 목적과 방법으로 인식하는지 확인하고 실제 실행을 명시적으로 허가한 뒤에만 데이터 취득 단계로 이동한다.

### 1.2 중요 수정 — \(\log_k\)는 base-\(k\) 로그가 아니다

이 문서와 FGKMT/Sono 문맥의 아래 첨자 \(k\)는 로그의 밑이 아니라 자연로그의 반복 횟수다.

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 반복}}.
\]

정확히는

\[
\log_1(x)=\ln(x),
\]

\[
\log_2(x)=\ln(\ln(x)),
\]

\[
\log_3(x)=\ln(\ln(\ln(x))),
\]

\[
\log_4(x)=\ln(\ln(\ln(\ln(x)))).
\]

따라서 연구의 정본 scale은

\[
F(x)=
\frac{\ln(x)\,\ln(\ln(x))\,\ln(\ln(\ln(\ln(x))))}
{\ln(\ln(\ln(x)))}
\]

이다. `math.log(x, 2)`, `math.log(x, 3)`, `math.log(x, 4)` 또는 `numpy.log2(x)`를 연구 계산에 사용하는 것은 금지한다. 이들은 각각 base-\(k\) 로그이며 iterated natural logarithm이 아니다.

정본 구현은 다음 형태를 따른다.

```python
import mpmath as mp

mp.mp.dps = 50

def iter_log(x, n):
    x = mp.mpf(x)
    for _ in range(n):
        x = mp.log(x)
    return x

def F(x):
    x = mp.mpf(x)
    log1 = iter_log(x, 1)
    log2 = iter_log(x, 2)
    log3 = iter_log(x, 3)
    log4 = iter_log(x, 4)
    return log1 * log2 * log4 / log3
```

코드 실행 전에 `log_2`, `log_3`, `log_4`를 직접 중첩한 `mp.log` 값과 대조하고, base-2/3/4 로그와는 서로 다름을 negative-control 단위시험으로 확인한다.

기존 연구 코드에 base-\(k\) 오구현이 발견되면 해당 실행에서 생성한 다음 산출물은 모두 무효로 처리하고 교정된 코드로 재생성한다.

- \(F(x)\)
- \(H(x)=G(x)/F(x)\)
- Sono bound와의 ratio
- interval-wise minimum
- running minimum
- 모든 그래프
- 모든 통계 요약

최종 결과 보고서에도 \(\log_k(x)\)가 \(k\)회 반복한 자연로그라는 정의를 명시한다.

global running minimum은 정의상 단조 비증가하므로, 국소적인 증가·회복·요동은 interval minima와 record-jump recovery 또는 별도의 local envelope에서 분석한다.

---

## 2. 선행연구 및 연구의 위치

### 2.1 FGKMT large-gap result

FGKMT(Ford, Green, Konyagin, Maynard, Tao)는 maximal prime gap에 대해 다음 형태의 점근적 하한을 증명하였다.

\[
G(x)\gg
\frac{\log x\,\log_2x\,\log_4x}{\log_3x}.
\]

본 연구에서는 이 정리의 증명 자체를 재구현하지 않는다.

### 2.2 Wolf 계열의 empirical maximal-gap 연구

Marek Wolf 및 Kourbatov–Wolf 계열 연구에서는 실제 maximal prime gaps를 계산하고, 경험적 maximal-gap growth와 관련 heuristic을 조사하였다.

특히 다음 형태의 함수를 기준으로 실제 데이터를 비교하는 연구가 존재한다.

\[
F(x)=
\frac{\log x\,\log_2x\,\log_4x}{\log_3x}.
\]

Wolf 계열의 경험적 관찰에서는 사실상 \(G(x)\)가 \(F(x)\)보다 큰지 여부와 maximal-gap growth를 조사한다.

### 2.3 Sono의 explicit constant와 계보

Sono는 Ford–Maynard–Tao의 *Chains of large gaps between primes* 정리를 explicit화하여, 고정된 \(k\)와 충분히 큰 \(X\)에 대해

\[
c_{\mathrm{LG}}\ge2.0\times10^{-17}
\]

이라는 값을 제시하였다. \(k=1\)에서는 FGKMT와 동일한 함수형 scale \(F(x)\)에 대응하므로 본 연구의 explicit 비교선으로 사용한다. 다만 이를 “FGKMT 5인 논문에 숨은 상수를 그대로 계산한 값”이라고 서술하지 않는다.

따라서 본 연구에서는 다음의 구체적인 함수

\[
L_{\mathrm{Sono}}(x)
=
2.0\times10^{-17}
\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

를 사용한다.

### 2.4 본 연구의 차별점

기존 연구와 중복되지 않도록 다음을 핵심 차별점으로 한다.

- 실제 maximal prime-gap 데이터 사용
- FGKMT/Sono의 explicit lower-bound scale을 직접 사용
- 정규화된 함수의 전체 궤적 분석
- maximal-gap record 사이 interval 전체를 고려
- 단순한 특정 \(x\)에서의 비교가 아니라 empirical lower envelope 분석
- Wolf의 경험적 \(c\approx1\) 영역과 Sono의 \(2\times10^{-17}\) 보장 사이의 격차를 정량적으로 측정
- \(x\) 증가에 따른 ratio/envelope의 장기 거동 분석

---

## 3. 핵심 수학적 정의

### 3.1 개별 prime gap

소수를

\[
p_1=2,\ p_2=3,\ p_3=5,\ldots
\]

라고 할 때

\[
g_n=p_{n+1}-p_n
\]

이다.

### 3.2 maximal prime gap — end-bounded 정본

다음 함수로 정의한다.

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

로 고정한다. 원 데이터 표가 start prime을 기준으로 high watermark를 제공하더라도 정규화 후 record jump 위치는 반드시 \(e_i=p_i+g_i\), 즉 end prime으로 변환한다. start-bounded 함수를 같은 이름의 \(G(x)\)로 혼용하지 않는다.

### 3.3 FGKMT scale

\[
F(x)=
\frac{\log x\,\log_2x\,\log_4x}{\log_3x}.
\]

### 3.4 정규화된 empirical coefficient

본 연구의 핵심 변수:

\[
\boxed{
H(x)=\frac{G(x)}{F(x)}
}
\]

이다.

그러면 FGKMT/Sono 형태의 lower bound

\[
G(x)\ge cF(x)
\]

는

\[
H(x)\ge c
\]

로 표현된다.

### 3.5 Sono 기준선

\[
c_{\mathrm{Sono}}
=
2.0\times10^{-17}.
\]

따라서

\[
H(x)\ge2.0\times10^{-17}
\]

가 Sono의 explicit lower-bound 기준이다.

### 3.6 Wolf 경험적 기준선

선행연구에서 보고된 Wolf 계열의 경험적 관찰과 비교하기 위해

\[
H(x)=1
\]

을 별도의 reference line으로 표시한다.

주의: \(1\)은 Sono와 같은 의미의 "증명된 constant"가 아니라 **empirical/heuristic reference**임을 명확히 표시한다.

---

## 4. 가장 중요한 분석 대상: interval-wise lower envelope

Maximal gap 데이터는 record가 발생할 때만 \(G(x)\)가 증가하는 계단함수이다.

maximal-gap record를 시작 소수 \(s_i\), gap \(g_i\), 끝 소수 \(e_i=s_i+g_i\)의 삼중항

\[
(s_i,g_i,e_i)
\]

라 하고 다음 record를

\[
(s_{i+1},g_{i+1},e_{i+1})
\]

라 하자.

그러면

\[
e_i\le x<e_{i+1}
\]

에서

\[
G(x)=g_i
\]

이다.

\(F(x)\)는 충분히 큰 영역에서 증가하므로 같은 interval에서

\[
H(x)=\frac{g_i}{F(x)}
\]

는 감소한다.

따라서 각 maximal-gap interval에서 가장 작은 \(H(x)\)를 계산하면 해당 interval 전체를 검사할 수 있다.

정확한 정수 \(x\)를 사용할 경우 다음을 사용한다.

\[
H_i^{\min}
=
\frac{g_i}{F(e_{i+1}-1)}.
\]

이 값이 각 maximal-gap record interval의 worst-case normalized value이다.

이 값을 이용하면 전체 정수 \(x\)를 하나씩 계산하지 않고도 모든 maximal-gap interval을 정확하게 비교할 수 있다.

---

## 5. 핵심 분석량

### 5.1 실제 normalized coefficient

\[
H_i^{\mathrm{jump}}=
\frac{g_i}{F(e_i)}
\]

### 5.2 interval minimum

\[
H_i^{\min}
=
\frac{g_i}{F(e_{i+1}-1)}
\]

### 5.3 running minimum

\[
M(X)=\min_{X_{\mathrm{scale+}}\le x\le X}H(x),
\qquad X_{\mathrm{scale+}}=3{,}814{,}280
\]

이 함수가 본 연구의 핵심 empirical lower envelope이다.

### 5.4 Sono 대비 배수

\[
Q(x)
=
\frac{H(x)}
{2.0\times10^{-17}}
\]

따라서

\[
Q(x)=1
\]

은 Sono 기준선을 의미한다.

### 5.5 Wolf 기준 대비 배수

\[
W(x)=H(x)
\]

이며

\[
W(x)=1
\]

을 Wolf empirical reference로 사용한다.

---

## 6. 연구에서 확인해야 할 패턴

단순히 "부등식이 참인가?"만 확인하지 않는다.

다음 현상을 모두 조사한다.

### A. 반복로그 domain 진단 영역

\[
16\le x<3{,}814{,}280
\]

에서는 반복로그의 정의 가능 여부와 \(F(x)\)의 부호만 진단한다.

\(F(x)\)의 수학적 정의 가능 최소 정수는

\[
x=16
\]

이다.

이 구간에서는 \(F(x)\le0\)인 값이 존재하므로 theorem-scale \(H\), Sono ratio, running minimum에 포함하지 않는다.

### B. Wolf 영역

\[
H(x)\approx1
\]

과 어떤 관계를 보이는지 확인한다.

### C. 장기 추세

\[
H(x)
\]

가 증가하는지, 감소하는지, 요동하는지 확인한다.

### D. lower envelope

\[
M(X)=\min_{X_{\mathrm{scale+}}\le x\le X}H(x)
\]

는 정의상 단조 비증가하므로 새 최저치와 plateau를 확인한다. 증가·회복·요동 및 느린 국소 변화는 interval minima, record-jump recovery, log-bin/rolling local envelope를 별도로 산출하여 확인한다.

### E. Sono bound

\[
M(X)<2\times10^{-17}
\]

인 사례가 있는지 검색한다.

발견될 경우 정의·입력·정밀도를 재검증하고 theorem applicability와 비교한다. Sono 정리의 수치 임계값이 알려지지 않았으므로 유한 \(x\)의 하회만으로 정리 반례라고 판정하지 않는다.

### F. Cramér/heuristic scaling

실제 \(H(x)\)의 거동을 Cramér형 maximal-gap scaling과도 비교한다.

다만 본 연구의 주된 기준선은 Cramér가 아니라 FGKMT/Sono임을 명확히 한다.

---

## 7. 데이터 수집 전략

### 7.1 1차 데이터와 정본 출처

1차 데이터는 Prime Gap List Project의 GitHub 저장소를 사용한다.

- 저장소: `https://github.com/primegap-list-project/prime-gap-list`
- 정본 파일: commit으로 고정한 `allgaps.sql`
- 참고 웹 표: `https://primegap-list-project.github.io/lists/prime-gaps-high-watermarks/`
- exhaustive 범위 참고: `https://primegap-list-project.github.io/fully-analyzed/`

웹 표는 참고·대조용이며 파이프라인 입력으로 사용하지 않는다. 실행 시 `master`를 40자 commit으로 resolve하고 raw URL, 취득 UTC, SHA-256을 보존한다.

필요한 최소 열:

```text
start_prime
gap
next_prime
```

여기서

```text
next_prime = start_prime + gap
```

으로 확인한다.

### 7.2 데이터 우선순위

1. Prime Gap List Project의 최신 maximal-gap records
2. exhaustive verification 범위가 명시된 데이터
3. Oliveira e Silva–Herzog–Pardi 계열의 검증 데이터
4. Wolf/Cohen 등의 표와 교차검증

### 7.3 전체 prime list는 원칙적으로 필요하지 않다

\(G(x)\)를 복원하는 목적이라면 maximal-gap record만으로 충분하다.

단, 데이터 완전성 검증을 위해 exhaustive range를 별도로 기록한다.

---

## 8. 구현 환경

Python 권장.

필수:

```text
Python 3.11+
numpy
pandas
matplotlib
mpmath
scipy
```

선택:

```text
polars
pyarrow
jupyter
```

전체 maximal-gap record는 데이터량이 작기 때문에 pandas로 충분할 가능성이 높다.

거대한 정수 또는 극단적으로 큰 \(x\)를 실험할 경우 `mpmath`를 사용한다.

---

## 9. 소수 데이터를 직접 다시 계산할 필요가 있는가?

1차 연구에서는 하지 않는다.

현재 목표는 **이미 검증된 maximal-gap record를 기반으로 이론식과 실제 데이터를 비교**하는 것이다.

따라서 먼저 공개 데이터로 재현한다.

추후 필요할 경우 다음을 별도 단계로 추가한다.

- 독립적인 prime-gap 재계산
- 공개 dataset과 checksum 비교
- exhaustive verification 범위 내 재검증

---

## 10. 권장 코드 구조

현재 작업 루트와 구현 구조를 정본으로 사용한다.

    Z:\FGKMT-Sono-PrimeGap-Analysis/
    ├─ AGENTS.md
    ├─ handoff/YYYYMMDDHHmm_HANDOFF.md
    ├─ .agents/skills/                 # Codex가 발견하는 프로젝트 스킬
    ├─ .claude/skills/                 # 삭제하지 않는 호환 원본 mirror
    ├─ ai_dev_tool/                    # 계산 함정·착수·핸드오프 규약
    ├─ article/                        # 제공된 원 논문 PDF
    ├─ datas/
    │  ├─ source_registry.json
    │  ├─ raw/prime-gap-list-project/<commit>/
    │  │  ├─ allgaps.sql
    │  │  ├─ schema.sql
    │  │  └─ metadata.json
    │  └─ validated/prime-gap-list-project/<commit>/
    │     ├─ maximal_gap_records.csv
    │     └─ validation_report.json
    ├─ source/                         # definitions, parser, provenance, analysis, plots, CLI
    ├─ tests/                          # 데이터 비의존·합성 fixture 시험
    ├─ test_plan/
    ├─ test_result/
    │  ├─ logs/
    │  └─ run_<run-id>/
    │     ├─ tables/
    │     ├─ figures/
    │     └─ summary.json
    └─ docs/
       ├─ METHODS.md
       └─ review/

Notebook은 정본 계산 경로로 사용하지 않는다. 모든 결과는 source 모듈과 CLI로 재생성 가능해야 한다.

---

## 11. 1차 구현 목표

Codex는 우선 논문 작성이나 해석보다 **재현 가능한 계산 파이프라인 구축**을 목표로 한다.

### Step 1 — 데이터 확보

- Prime Gap List Project GitHub의 동일한 40자리 commit에서 allgaps.sql과 schema.sql을 취득
- 파일별 commit-pinned URL, SHA-256, byte 수, 취득 UTC 기록
- 웹 high-watermark와 fully-analyzed 페이지는 의미와 coverage 확인에만 사용
- exhaustive verification 범위 기록
- 원본은 datas/raw/prime-gap-list-project/<commit>/에 불변 보존

### Step 2 — 데이터 검증

각 row에 대해

\[
next\_prime=start\_prime+gap
\]

확인.

record gap이 이전 record보다 엄격하게 큰지 확인.

start prime이 증가하는지 확인.

published ismax와 eligible first occurrences에서 독립 재구성한 high watermark를 대조.

현재 canonical source 하나만으로 독립 source 교차검증을 했다고 주장하지 않는다.

### Step 3 — 수학 함수 구현

다음 함수를 구현:

```python
F(x)
H(x, gap)
sono_bound(x)
wolf_reference(x)
```

iterated logarithm은 명시적인 함수로 구현.

```python
log1(x)
log2(x)
log3(x)
log4(x)
```

초기 영역에서 domain error 방지.

구현 정본과 사전검증은 각각 `source/definitions.py`, `tests/test_iterated_logs.py`를 사용한다.

### Step 4 — interval analysis

각 maximal-gap record에 대해:

```text
start_x
end_x
gap
H_at_start
H_interval_min
Q_interval_min
```

계산.

### Step 5 — running minimum

\[
M(X)=\min_{x\le X}H(x)
\]

계산.

### Step 6 — 시각화

최소한 다음 그래프를 생성한다.

1. \(H(x)\) vs \(\log_{10}x\)
2. \(\log_{10}H(x)\) vs \(\log_{10}x\)
3. running minimum \(M(X)\)
4. \(Q(x)=H(x)/(2\times10^{-17})\)
5. Cramér normalization과 비교
6. 새 maximal-gap record 직전·직후의 \(H\)와 recovery

모든 그래프에는 사용한 데이터 범위와 데이터 출처를 명시한다.

---

## 12. 매우 중요한 해석상의 주의점

### 12.1 Sono constant는 실제 "예상값"이 아니다

\[
2\times10^{-17}
\]

은 실제 \(H(x)\)가 수렴할 것으로 예상하는 값이 아니다.

이것은 **현재 증명으로 보장되는 explicit lower-bound constant**이다.

따라서 다음과 같은 해석은 금지:

```text
H(x)가 2×10^-17로 수렴하는지 확인한다.
```

대신:

```text
H(x)의 empirical lower envelope가 어떻게 움직이는지 확인하고,
그것을 Sono의 rigorously proved lower-bound constant와 비교한다.
```

라고 해석한다.

### 12.2 Wolf의 1도 엄밀한 bound가 아니다

Wolf의 \(c\approx1\)은 empirical/heuristic reference이다.

### 12.3 계산으로 정리가 증명되는 것은 아니다

아무리 큰 \(X\)까지

\[
H(x)\ge2\times10^{-17}
\]

가 관찰되어도, 그 사실만으로 무한한 \(x\)에 대한 Sono 정리를 증명하지 않는다.

### 12.4 유한 범위의 하회 관측은 threshold 정보로만 해석한다

Sono theorem의 실제 적용 threshold가 \(x_0\)라고 할 때,

\[
H(X)<2\times10^{-17}
\]

인 \(X\)가 verified exhaustive 범위에서 발견되고 Sono와 동일한 함수 정의가 적용된다면

\[
x_0>X
\]

인 형태의 uniform threshold가 존재할 경우 그 threshold는 \(X\)보다 커야 한다고 해석할 수 있다.

이는 asymptotic theorem의 반례가 아니며, 유한 범위의 명시적 threshold 연구 자료다.

---

## 13. 연구의 novelty 검증

코드 작성과 동시에 다음 literature search를 수행한다.

검색 대상:

```text
"maximal prime gaps" "Ford" "Maynard" "Tao"
"maximal prime gaps" "Sono"
"prime gaps" "Sono" "Wolf"
"G(x)" "Ford Green Konyagin Maynard Tao" "Wolf"
"c_LG" prime gaps
"2×10^-17" prime gaps
"large gaps between primes" empirical FGKMT
"maximal prime gaps" "lower envelope"
```

특히 다음을 우선 검토:

- Wolf
- Kourbatov–Wolf
- Feliksiak
- Cohen
- Banks–Ford–Tao
- Sono 이후 2024–2026의 citing papers

단순히 제목/초록만 보지 말고 다음을 확인:

1. \(G(x)\) 실제 계산 여부
2. FGKMT 하한식 사용 여부
3. \(H(x)=G(x)/F(x)\) 또는 동등한 정규화 사용 여부
4. running minimum/lower envelope 사용 여부
5. Sono constant \(2\times10^{-17}\) 사용 여부
6. 실제 데이터 범위
7. 수행한 분석과 본 연구의 중복 여부

동일한 연구가 발견되면 즉시 별도 보고하고 중복 연구를 진행하지 않는다.

---

## 14. 1차 결과에서 기대하는 관찰

결과가 사전에 정해져 있다고 가정하지 않는다.

다음 가능성을 모두 열어둔다.

### Pattern A

\[
H(x)
\]

가 일정한 수준으로 안정.

### Pattern B

\(H(x)\)가 천천히 증가.

### Pattern C

\(H(x)\)가 천천히 감소.

### Pattern D

큰 폭으로 요동.

### Pattern E

running minimum이 특정한 함수에 따라 감소.

### Pattern F

Sono bound와 실제 데이터 사이의 격차가 \(x\) 증가와 함께 계속 커짐.

### Pattern G

예상하지 못한 낮은 \(H(x)\)가 나타남.

결과를 보기 전에 결론을 설정하지 않는다.

---

## 15. 최우선 산출물

Codex의 1차 목표는 논문이 아니라 다음을 자동 생성할 수 있는 **재현 가능한 computational research package**다.

```text
1. validated maximal-gap dataset
2. source metadata
3. F(x), H(x), Sono bound 계산 모듈
4. interval-wise minimum H 계산
5. running minimum M(X)
6. 핵심 통계량 CSV
7. 주요 그래프 PNG/PDF
8. 모든 계산을 재현할 수 있는 script
9. README에 수학적 정의와 데이터 출처 명시
10. literature overlap report
```

최종적으로 결과에 다음 항목을 포함한다.

```text
maximum analyzed x
number of maximal-gap records
verified exhaustive range
minimum observed H(x)
location of minimum
minimum observed H(x) / Sono constant
whether H(x) ever fell below Sono bound
whether H(x) ever fell below Wolf reference c=1
behavior of running minimum
```

---

## 16. 연구의 성공 기준

이 프로젝트의 1차 성공 조건은 "논문이 나오는 것"이 아니다.

다음 중 하나 이상의 의미 있는 결과를 발견하는 것이 목표다.

1. 기존 연구에서 다루지 않은 \(H(x)\) empirical envelope를 확인
2. Sono bound와 실제 maximal-gap 데이터 사이의 정량적 격차를 재현 가능하게 체계화
3. \(H(x)\)의 예상 밖 장기 패턴 발견
4. 기존 empirical model과 FGKMT lower-bound scale 사이의 관계 발견
5. Sono constant를 하회하거나 특이하게 근접하는 유한 범위 구조 발견
6. 향후 explicit-threshold 증명을 위한 유용한 수치적 conjecture 도출

결과가 단순한 기존 연구 재현이라면 그 사실을 명시하고 연구 방향을 수정한다.

---

## 17. 코딩 시 금지사항

- 모든 소수를 무작정 \(10^{20}\)까지 생성하지 말 것
- maximal-gap record로 충분한 문제에 full prime list를 사용하지 말 것
- 계산된 데이터와 exhaustive verified data를 구분하지 않고 혼용하지 말 것
- empirical observation을 theorem처럼 표현하지 말 것
- Wolf의 \(c=1\)과 Sono의 \(2\times10^{-17}\)을 동일한 종류의 상수로 설명하지 말 것
- Sono의 constant를 실제 asymptotic limit이라고 해석하지 말 것
- \(x_0\)가 explicit하게 알려졌다고 가정하지 말 것
- 모든 logarithm의 정의 및 밑을 명시하지 않고 계산하지 말 것
- `math.log(x, 2|3|4)` 또는 동등한 base-\(k\) 로그를 \(\log_2,\log_3,\log_4\)로 사용하지 말 것
- 기존 선행연구와 동일한 결과를 새 결과로 포장하지 말 것

---

## 18. 최종적으로 Codex에게 요구하는 것

먼저 아래 순서대로 작업한다.

1. 최신 공개 maximal prime-gap 데이터의 출처와 범위를 읽기 전용으로 확인한다.
2. 연구 이해를 사용자에게 설명하고 목적·정의·범위·방법의 일치와 실제 실행 허가를 확인한다.
3. 허가 후 원본 데이터와 검증 데이터를 확보한다.
4. \(G(x)\), \(F(x)\), \(H(x)\)를 정확하게 구현한다.
5. 각 maximal-gap interval의 정확한 \(H_{\min}\)을 계산한다.
6. running minimum \(M(X)\)을 계산한다.
7. Wolf 기준 \(H=1\)과 Sono 기준 \(H=2\times10^{-17}\)을 표시한다.
8. verified exhaustive limit 안의 가능한 최대 \(x\)까지 결과를 계산한다.
9. 그래프와 CSV를 생성한다.
10. 기존 Wolf/Kourbatov-Wolf/Feliksiak/Cohen/Banks-Ford-Tao/Sono 및 이후 논문과 결과를 비교한다.
11. 동일 연구 여부를 문헌별로 판정한다.
12. 그 후에야 연구 결과를 해석한다.
13. 새로운 패턴이 발견될 경우 해당 패턴을 독립적인 수학적 가설로 분리한다.

**첫 단계에서는 해석보다 정확한 데이터 재현성과 기존 연구와의 중복 여부 확인을 우선한다.**
