# P006 — Maximal-gap Plateau·Recurrence 통계 pilot

## 1. 상태

`PREPARATION_ONLY` — 정의와 데이터 게이트를 확정했으며 실제 consecutive-prime 생성·통계 실행은 별도 사용자 승인 전에는 수행하지 않는다.

## 2. 연구 질문과 비목적

연구 질문:

1. 한 maximal-gap record가 유지되는 동안 같은 크기의 gap이 총 몇 번 나타나는가?
2. 최초 발생을 제외한 재출현은 동일한 관측기회로 정규화했을 때 어떻게 달라지는가?
3. canonical end-bounded plateau 수명과 start-prime recurrence exposure 사이에 어떤 경험적 관계가 있는가?
4. raw count 패턴이 gap-specific singular series와 위치 효과를 보정한 뒤에도 남는가?

비목적:

- maximal-gap record 표만으로 exact recurrence를 추정하지 않는다.
- 상관관계로 인과관계나 점근 법칙을 주장하지 않는다.
- right-censored plateau를 complete sample로 취급하지 않는다.
- start-bounded exposure와 end-bounded `G(x)`를 같은 함수라고 부르지 않는다.
- 사용자 승인 없이 `10^20` 재열거 또는 새 패키지 설치를 하지 않는다.

## 3. 수학 정의

연속 소수와 gap:

\[
g_n=p_{n+1}-p_n.
\]

canonical maximal-gap 함수:

\[
G_{\mathrm{end}}(x)=\max_{p_{n+1}\le x}g_n.
\]

record `k`를 `(s_k,G_k,e_k=s_k+G_k)`라 한다. 다음 record는 `(s_(k+1),G_(k+1),e_(k+1))`이다.

### 3.1 End-bounded plateau

정수 또는 실수 x에서 canonical plateau는

\[
e_k\le x<e_{k+1}
\]

이고 수명은

\[
L_k^{end}=\ln(e_{k+1}/e_k),\qquad
D_k^{end}=\log_{10}(e_{k+1}/e_k).
\]

### 3.2 Start-event exposure와 recurrence

gap occurrence를 세는 표본공간은

\[
A_k=\{p_n:s_k\le p_n<s_{k+1}\}
\]

이다.

\[
N_k=|A_k|=\pi(s_{k+1})-\pi(s_k),
\]

\[
M_k=\#\{p_n\in A_k:g_n=G_k\},
\]

\[
C_k=M_k-1.
\]

정합적인 rate는

\[
Q_k=M_k/N_k
\]

와, `N_k>1`일 때

\[
R_k=C_k/(N_k-1)
\]

이다. `C_k/N_k`는 분자·분모 표본공간이 달라 주 지표로 사용하지 않는다.

보조 start 수명:

\[
L_k^{start}=\ln(s_{k+1}/s_k).
\]

### 3.3 FGKMT scale과의 선택적 결합

필요할 때만 다음을 기존 canonical 정의 그대로 붙인다.

\[
\log_j(x)=\underbrace{\ln(\ln(\cdots\ln x))}_{j\text{회}},\quad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\quad
H(x)=G_{\mathrm{end}}(x)/F(x).
\]

P006 recurrence 자체에는 `F,H`가 필수가 아니며 연구 질문을 혼합하지 않는다.

## 4. Dataset 원천과 완전성 한계

- record reference: `prime-gap-list-project/prime-gap-list`, commit `1a112a1387052d9ad360686313f501c01fe46b68`
- `allgaps.sql` SHA-256: `988c3278d95a16460a9897e09829fb061ee854e55efa6c4fcec3b9779930894f`
- current verified exhaustive record coverage: `10^20`
- critical limitation: `allgaps.sql`은 모든 consecutive prime gap stream이 아님

따라서 exact `M,C,N,Q,R` 입력은 pilot에서 직접 생성한 모든 consecutive primes/gaps로 제한한다. 외부 raw stream을 사용할 경우 source commit/hash, coverage interval, boundary overlap, generation algorithm, certificate를 별도 registry에 고정한다.

## 5. 입력 필터와 record 복원 규칙

- pilot 범위 기본값: `[2,10^8]`
- 단계 확장 후보: `[2,10^9]`, `[2,10^10]`
- 인접 block 사이에 마지막 prime/첫 prime을 overlap하여 경계 gap을 보존
- 모든 prime은 엄격 증가하고 모든 gap은 양의 짝수(2→3 예외 gap 1 별도 처리)
- 새 gap이 이전 running maximum보다 클 때만 새 maximal record
- complete plateau는 다음 record가 pilot 상한 안에 존재하는 경우만
- 마지막 open plateau는 `right_censored=true`
- `M_k`는 최초 record occurrence를 포함하고 `C_k=M_k-1`을 자동 검증

## 6. 사전검증 및 중단 조건

### 자동 1차 게이트

1. 고정 실행환경과 입력·출력 non-overwrite 확인
2. 직접 중첩 자연로그/base-log negative control은 `F,H`를 계산할 때만 기존 preflight 재사용
3. 손계산 gap fixture에서 record transition, `M,C,N,Q,R`, censoring 100% 일치
4. 두 block으로 나눈 stream과 단일 block stream의 gap·record hash 일치
5. prime count가 독립 `primecount` 또는 알려진 `pi(10^n)`와 일치
6. histogram에서 각 plateau의 `histogram[G_k]`가 `M_k`와 일치
7. 누락·중복 prime 또는 boundary gap 불일치 시 즉시 중단

### Codex 수동 2차 게이트

- 데이터 license/provenance와 exhaustive 의미
- end/start 표본공간 라벨의 정합성
- complete/censored 분리
- expected model이 정리인지 heuristic인지 문헌별 라벨
- 작은 record 표본에 대한 통계 해석의 과장 여부

## 7. 승인 후 실행 명령

아직 구현·승인되지 않았다. pilot 코드와 독립 reference가 준비된 뒤 사용자에게 예상 CPU/RAM/시간을 먼저 보고하고 별도 승인형 실행기를 제공한다.

권장 외부 도구는 WSL의 `primesieve-bin`과 `primecount`이다. 설치는 사용자 승인 후:

```bash
sudo apt update
sudo apt install -y primesieve-bin primecount
```

현재 `FGKMT` Conda에는 `numpy`, `pandas`, `scipy`, `statsmodels`가 있고 `sympy`, Python `primesieve`는 없다. production generator는 WSL `primesieve`를 권장하며, 작은 독립 Python reference가 필요하면 `sympy` 설치를 별도로 승인받는다.

## 8. 산출물

- complete plateau table: `k,G_k,s_k,e_k,s_next,e_next,L_end,D_end,L_start,N,M,C,Q,R`
- censored plateau table
- 전체 gap histogram과 record transition table
- block coverage ledger와 boundary overlap report
- direct/reference cross-validation report
- raw/normalized recurrence scatter와 confidence-free descriptive summaries
- optional heuristic expected count 및 observed/expected table
- 실행 로그, 환경 manifest, 입력·출력 SHA-256

## 9. 판정 기준과 해석 제한

- 모든 consecutive gap이 coverage된 pilot만 `EXACT_PILOT`로 부른다.
- record 목록에서 추정한 count는 exact 결과로 채택하지 않는다.
- complete plateau만 상관·회귀 입력에 사용하고 censored 행은 별도 기술한다.
- overlapping/selected record sample에 독립·동일분포를 가정하지 않는다.
- Poisson/negative-binomial은 descriptive sensitivity model이며 증명이 아니다.
- Hardy–Littlewood, Gallagher, Goldston–Ledoan, Wolf 기준은 조건부 또는 heuristic임을 표기한다.
- 작은 pilot에서 패턴이 보여도 `10^20` 또는 점근 범위로 외삽하지 않는다.

## 10. 선행연구와 후속 작업

### 참고문헌

1. Hardy–Littlewood (1923), DOI https://doi.org/10.1007/BF02403921
2. Gallagher (1976), DOI https://doi.org/10.1112/S0025579300016442
3. Goldston–Ledoan, arXiv:1111.3380, https://arxiv.org/abs/1111.3380
4. Wolf, arXiv:1102.0481, https://arxiv.org/abs/1102.0481
5. Kourbatov–Wolf, arXiv:1901.03785, https://arxiv.org/abs/1901.03785
6. Lemke Oliver–Soundararajan, DOI https://doi.org/10.1073/pnas.1605366113
7. Prime Gap List Project, https://primegap-list-project.github.io/

### 후속 순서

1. 사용자와 corrected rate `Q=M/N`, `R=C/(N-1)` 정의 합의
2. pilot 구현 계획 승인
3. WSL `primesieve-bin`, `primecount` 설치 승인
4. `[2,10^8]` pilot 및 독립 검증
5. 결과·자원 사용량 검토 후 `10^9`, `10^10` 확대 여부 결정
6. external exhaustive raw stream 확보 가능성 조사
