# P006 — Maximal-gap Plateau·Recurrence 통계 pilot

## 1. 상태

`WAITING_FOR_USER_APPROVAL` — 정의·코드·자동검증·Windows 실행기를 준비했고 전체 53 tests와 P006 preflight를 PASS했다. 실제 `[2,10^8]` consecutive-prime 생성과 통계 실행은 아직 수행하지 않았으며 사용자의 별도 실험 승인 후에만 시작한다.

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
2. validated record CSV의 pinned SHA-256과 source commit 확인
3. 손계산 gap fixture에서 record transition, `M,C,N,Q,R`, censoring 100% 일치
4. 여러 chunk로 나눈 stream과 단일 chunk stream의 gap·record 결과 일치
5. prime count가 알려진 exact `pi(10^n)` 상수와 일치
6. reconstructed record triplet `(start,gap,end)`가 validated reference와 전부 일치
7. histogram 총합=`prime_count-1`, gap 1은 1회, 그 밖의 gap은 짝수인지 확인
8. 누락·중복 prime, boundary gap, `C=M-1`, `Q`, `R` 불일치 시 즉시 중단

### Codex 수동 2차 게이트

- 데이터 license/provenance와 exhaustive 의미
- end/start 표본공간 라벨의 정합성
- complete/censored 분리
- expected model이 정리인지 heuristic인지 문헌별 라벨
- 작은 record 표본에 대한 통계 해석의 과장 여부

## 7. 승인 후 실행 명령

주 실행환경은 Windows의 고정 Python `W:\miniforge3\envs\FGKMT\python.exe`다. NumPy odd-only segmented sieve가 prime chunk 사이의 마지막 소수를 이어 붙여 경계 gap을 보존한다. WSL을 호출하지 않으며 새 Python 패키지를 설치하지 않는다.

`[2,10^8]` pilot:

```bat
run_P006_plateau_recurrence_pilot.bat --confirm-p006
```

기본 `[2,10^9]` complete configured expansion:

```bat
run_P006_plateau_recurrence_full.bat --confirm-p006
```

선택적 `[2,10^10]`:

```bat
run_P006_plateau_recurrence_full.bat --confirm-p006 10000000000
```

여기서 `full`은 선택한 유한 범위를 모든 consecutive gap으로 완전히 처리한다는 뜻이며 `10^20` 전체를 뜻하지 않는다. 설치된 WSL `primesieve-bin`·`primecount`는 `2^64` 이하의 선택적 독립 교차검산에만 사용할 수 있다.

구현 파일은 `source/plateau_recurrence.py`, `source/plateau_recurrence_cli.py`, `tests/test_plateau_recurrence.py`, 공통 `run_plateau_recurrence.ps1`, 두 BAT 진입점이다.

사전 추정은 `[2,10^8]` 약 1–5분, `[2,10^9]` 약 10–60분, `[2,10^10]` 약 2–12시간이다. 아직 이 PC의 실제 P006 처리량을 측정하지 않은 넓은 계획값이며 pilot 로그로 교체한다. segment working set은 2 GiB보다 훨씬 작게 설계했다.

## 8. 산출물

- complete plateau table: `k,G_k,s_k,e_k,s_next,e_next,L_end,D_end,L_start,N,M,C,Q,R`
- right-censored plateau table
- 전체 gap histogram과 record transition table
- validated maximal-record triplet과 exact `pi(10^n)` 교차검증 report
- complete plateau의 `M/C`, `Q/R`, end/start lifetime PNG·PDF 6개
- saved-artifact SHA-256 manifest와 독립 재해시 report
- 실행 로그와 환경·입력 provenance
- 기존 산출물을 덮어쓰지 않는 독립 run directory

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

1. corrected rate와 end/start 표본공간 합의 완료
2. Windows pilot 구현·toy 자동검증 완료
3. 사용자에게 `[2,10^8]` 실제 pilot 실행 승인 요청
4. 승인 시 사용자가 BAT 실행 후 로그·run 경로 제공
5. Codex 검토와 사용자 그래프 시각검사 PASS 후에만 `[2,10^9]` 결정
6. `10^9` 자원 결과를 본 뒤에만 선택적 `10^10` 확대 여부 결정
