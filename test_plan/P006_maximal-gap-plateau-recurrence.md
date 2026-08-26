# P006 — Maximal-gap Plateau·Recurrence 통계 실험

## 1. 상태

`FULL_1E9_EXPERIMENT_PASS / NUMERIC_QA_PASS / USER_VISUAL_QA_PASS` — 사용자 실행 `20260824T065339Z_p006_full_1000000000`은 `[2,10^9]` 모든 consecutive gap을 처리하고 exact `pi(10^9)`, 30 reference records, 12 saved artifacts를 issue 0으로 검증했다. complete/right-censored plateau는 29/1이다. 새 figure 3개는 자동검사와 2026-08-26 사용자 시각검사를 모두 PASS했다.

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

## 7. 완료 실행 명령 provenance — 재실행 금지

주 실행환경은 Windows의 고정 Python `W:\miniforge3\envs\FGKMT\python.exe`다. NumPy odd-only segmented sieve가 prime chunk 사이의 마지막 소수를 이어 붙여 경계 gap을 보존한다. WSL을 호출하지 않으며 새 Python 패키지를 설치하지 않는다.

`[2,10^8]` pilot:

```bat
test_done\run_P006_plateau_recurrence_pilot-20260823T190035Z-done.bat --confirm-p006
```

기본 `[2,10^9]` complete configured expansion:

```bat
test_done\run_P006_plateau_recurrence_full-20260824T065339Z-done.bat --confirm-p006
```

선택적 `[2,10^10]`:

```bat
새 P006 revision runner가 필요함; 완료 `test_done` BAT는 사용하지 않음
```

위 BAT 표기는 완료 실행 provenance다. 모두 재실행 금지이며, 선택적 `10^10` 확대를
다시 결정하면 `scripts/experiments/p006/`에 새 runner와 계획 revision을 만든다.

여기서 `full`은 선택한 유한 범위를 모든 consecutive gap으로 완전히 처리한다는 뜻이며 `10^20` 전체를 뜻하지 않는다. 설치된 WSL `primesieve-bin`·`primecount`는 `2^64` 이하의 선택적 독립 교차검산에만 사용할 수 있다.

구현 파일은 `source/plateau_recurrence.py`, `source/plateau_recurrence_cli.py`, `tests/test_plateau_recurrence.py`다. 완료된 공통 runner와 BAT 진입점은 `test_done/`에 hash와 함께 보존하며 재실행하지 않는다.

교정판은 `Start-Process` stdout/stderr 분리 수집, blank-line 보존, nonzero exit와 전체 PowerShell ErrorRecord 로깅을 사용한다. parser, synthetic stdout/stderr·exit-7 toy self-test, approval-denial, 전체 61 tests를 통과했고 실제 pilot도 PASS했다. 로컬 교정 증거는 `test_result/202608240329_P005_P006_P007_runner_fix_local_validation.md`, 실제 결과는 `test_result/202608240433_P006_pilot1e8_result_analysis.md`다.

실측 actual analysis는 `[2,10^8]`에서 1.151초였고 전체 runner는 tests 포함 약 11초였다. 단순 선형 외삽은 sieve/cache 효과 때문에 확정값이 아니므로 `[2,10^9]`은 약 1–5분, 선택적 `[2,10^10]`은 약 10–60분의 새 보수적 범위로 먼저 잡고 실제 로그로 교체한다. segment working set은 2 GiB보다 훨씬 작게 설계했다.

## 8. 실행 감사

- first log: `test_result/logs/run_20260823T161227Z_p006_pilot1e8.log`
- second log: `test_result/logs/run_20260823T173021Z_p006_pilot1e8.log`
- analyses: `test_result/202608240158_P006_pilot_failure_analysis.md`, `test_result/202608240315_P006_second_pilot_failure_analysis.md`
- 두 실행 모두 preflight: PASS
- 두 실행 모두 unit-test stage: 같은 정상 stderr 오판으로 중단
- approved analysis: NOT RUN
- saved-artifact verification: NOT RUN
- P006 result directory: 생성되지 않음
- 실행 당시 BAT: `test_done/run_P006_plateau_recurrence_pilot-done.bat`에 hash 보존
- 당시 실패 BAT: `test_done/run_P006_plateau_recurrence_pilot-done.bat`에 hash 보존

두 실패는 P006 수학 코드 또는 segmented sieve 실패의 증거가 아니다. 실제 데이터 단계에 들어가지 않았으므로 pilot 결과값·처리시간·그래프는 없다.

교정판 성공 실행:

- log: `test_result/logs/run_20260823T190035Z_p006_pilot1e8.log`
- result: `test_result/run_20260823T190035Z_p006_pilot1e8`
- prime count 5,761,455, gap count 5,761,454
- complete/censored plateaus 24/1
- saved verification issue 0, user visual QA 큰 문제 없음
- 상세: `test_result/202608240433_P006_pilot1e8_result_analysis.md`
- 실행 BAT 보존: `test_done/run_P006_plateau_recurrence_pilot-20260823T190035Z-done.bat`, SHA-256 `6527806481AAB168D1143EA37FAF59815D19BECD07CB04BDD365FA3CAF0F5FDE`

`[2,10^9]` 확대 성공 실행:

- log: `test_result/logs/run_20260824T065339Z_p006_full_1000000000.log`
- log SHA-256: `BDAACBEA9CEA0DF331300C52EA4CC8DED5F336F312A923979F1F7D13E2350206`
- result: `test_result/run_20260824T065339Z_p006_full_1000000000`
- prime/gap count: 50,847,534 / 50,847,533
- complete/censored plateaus: 29/1
- saved verification issue 0
- numeric QA PASS, 새 figure 3개 user visual QA PASS (2026-08-26)
- 상세: `test_result/202608241831_P006_full1e9_result_analysis.md`
- 실행 BAT 보존: `test_done/run_P006_plateau_recurrence_full-20260824T065339Z-done.bat`

## 9. 예정 산출물

- complete plateau table: `k,G_k,s_k,e_k,s_next,e_next,L_end,D_end,L_start,N,M,C,Q,R`
- right-censored plateau table
- 전체 gap histogram과 record transition table
- validated maximal-record triplet과 exact `pi(10^n)` 교차검증 report
- complete plateau의 `M/C`, `Q/R`, end/start lifetime PNG·PDF 6개
- saved-artifact SHA-256 manifest와 독립 재해시 report
- 실행 로그와 환경·입력 provenance
- 기존 산출물을 덮어쓰지 않는 독립 run directory

## 10. 판정 기준과 해석 제한

- 모든 consecutive gap이 coverage된 pilot만 `EXACT_PILOT`로 부른다.
- record 목록에서 추정한 count는 exact 결과로 채택하지 않는다.
- complete plateau만 상관·회귀 입력에 사용하고 censored 행은 별도 기술한다.
- overlapping/selected record sample에 독립·동일분포를 가정하지 않는다.
- Poisson/negative-binomial은 descriptive sensitivity model이며 증명이 아니다.
- Hardy–Littlewood, Gallagher, Goldston–Ledoan, Wolf 기준은 조건부 또는 heuristic임을 표기한다.
- 작은 pilot에서 패턴이 보여도 `10^20` 또는 점근 범위로 외삽하지 않는다.

## 11. 선행연구와 후속 작업

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
3. PowerShell 전체 stderr·오류 수집 교정과 로컬 parser/toy/approval-denial 검증 완료
4. `[2,10^8]` pilot 및 수치·manifest·사용자 시각검사 완료
5. `[2,10^9]` 확대 및 수치·manifest·사용자 시각검사 완료
6. 선택적 `[2,10^10]` 확대는 현재 승인되지 않았으며, 필요성이 생기면 새 계획 revision과 새 runner부터 작성
