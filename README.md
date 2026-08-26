# FGKMT-Sono maximal prime-gap empirical analysis

검증된 maximal prime-gap records로 end-bounded maximal gap을 복원하고, Ford–Green–Konyagin–Maynard–Tao(FGKMT)의 large-gap scale에 대한 정규화값과 empirical lower envelope를 분석하는 재현 가능한 계산 연구 프로젝트다.

## 현재 상태

P002–P008 COMPLETED / P009 PARI ADAPTER PASS / P010A·P010B RUNNER READY / P011 PILOT READY

P003 `10^20` end-bounded 분석과 P004 경계·local-envelope 민감도 분석이 완료됐다.
P005 CPU calibration, P006 `[2,10^9]`, P007 modulus 30/210/2310 certificate,
P008 exact prime-count·local phase-A도 PASS했다. P006 figure 3개는 사용자 시각 QA까지
끝났다. P008 actual block certified zero는 0개여서 supplied modulus-2310 direct tiling은
음성 판정이다.

P009 boundary-witness toy, PARI/GP 2.15.4 certificate adapter와 P010 memory-safe
separation oracle toy는 구현·검증됐다. P010은 count upper-bound(P010A)와 실제 search
acceleration(P010B)으로 분리했고, P006 recurrence null-model은 P011 사용자 pilot으로
준비했다. P009 actual `10^20`, P010A replay, modulus-30030 scan/LP solve, P011 pilot은
아직 실행하지 않았다.

## 수학 정의

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n),
\qquad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},
\qquad
H(x)=\frac{G(x)}{F(x)}.
\]

여기서 log_k(x)는 자연로그를 k회 반복한 값이다. 아래 첨자는 로그의 밑이 아니다.

\[
\log_2x=\ln(\ln x),\quad
\log_3x=\ln(\ln(\ln x)),\quad
\log_4x=\ln(\ln(\ln(\ln x))).
\]

canonical 경계는 gap의 끝 소수 p_(n+1)가 x 이하인 경우다. 분석은 F(x)>0인 최소 정수 x=3,814,280부터 시작한다.

## 데이터

- canonical repository: https://github.com/primegap-list-project/prime-gap-list
- commit-pinned inputs: allgaps.sql, schema.sql
- 참고용 high-watermark page: https://primegap-list-project.github.io/lists/prime-gaps-high-watermarks/
- exhaustive coverage 참고: https://primegap-list-project.github.io/fully-analyzed/

canonical 입력은 commit `1a112a1387052d9ad360686313f501c01fe46b68`로 고정돼 있다. 웹페이지는 coverage 참고용이며, 독립 대조에는 OEIS b-files와 Oliveira e Silva 공식 `t0.txt.gz`를 immutable 원본과 SHA-256으로 보존한다.

## 환경

연구 코드와 테스트는 다음 Python을 사용한다.

    W:\miniforge3\envs\FGKMT\python.exe

재현·사전검증 명령:

    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli preflight
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli status
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli fetch --dry-run

실제 재실행은 목적·정의·데이터 범위·수행방법에 대한 사용자 승인 후 새 run ID로만 수행한다.

    .\scripts\runners\run_fgkmt_pipeline.ps1 -Approved

## 문서

- test_result/202608231652_P004_sensitivity_analysis.md: P004 일상용어 결과와 엄밀 보정 판정
- docs/review/12_P005_prime-gap_CPU_exhaustive_타당성검토.md: Rank 85 이후 CPU 탐색 타당성
- test_plan/P005_prime-gap_cpu_exhaustive-extension-feasibility.md: CPU-only calibration과 exhaustive coverage gate
- docs/review/14_P005b_exhaustive-extension-calibration_타당성검토.md: arbitrary x-range calibration 제안 비판 검토
- docs/review/13_P006_plateau_recurrence_타당성검토.md: recurrence 정의·데이터 한계 검토
- test_plan/P006_maximal-gap-plateau-recurrence.md: Windows exact consecutive-gap pilot 실행 계획
- docs/review/15_P007_finite-range-residue-certificate_타당성검토.md: count upper bound와 직접 탐색 가속의 구분
- test_plan/P007_finite-range-residue-state-certificate.md: exact certificate pilot과 작은 modulus 비교 계획
- docs/review/17_20260826_prime-gap_통합이론_비판적_타당성검토.md: 신규 네 이론 초안 통합 비판검토
- docs/method/theory/00_이론_가설_방법론_색인.md: 검증수준별 이론·가설·방법론 지도
- test_plan/P009_P008_boundary-witness_break-even-gate.md: P009 boundary witness와 자원 gate
- test_plan/P010_P007_mod30030_memory-safe_separation.md: modulus-30030 memory-safe 설계
- test_plan/P010A_P007_count-upper-bound.md: count upper-bound certificate 연구
- test_plan/P010B_search-acceleration.md: coverage와 실제 탐색 가속 연구
- test_plan/P011_P006_recurrence-null-model.md: P006 recurrence null-model 파일럿

- AGENTS.md: Codex 작업·수학·데이터·승인 규약
- 연구 작업지시서: 연구 목적과 전체 분석 요구
- docs/METHODS.md: 계산·검증 방법론 정본
- docs/review/: 문헌별·종합 분석
- test_plan/: 실행 전 고정 계획
- test_result/202608230503_P003_full_analysis.md: 일상용어 전체 결과 분석
- docs/review/10_P003_문헌비교와_후속가설.md: 문헌 비교와 반증 가능한 후속 가설
- handoff/: 세션마다 새로 만드는 `YYYYMMDDHHmm_HANDOFF.md`; 최신 파일에 현재 상태와 다음 작업 기록
- scripts/common/: 재사용 공통 로깅
- scripts/runners/: 특정 완료 실험과 분리된 공통 runner
- scripts/experiments/: 신규 실험별 toy·준비 진입점
- scripts/setup/: 사용자가 명시적으로 실행하는 설치 helper
- test_done/: 완료 BAT/PS1/SH와 실험 전용 보조파일의 `-done` 보존 위치; 재실행 금지

유한 계산 결과는 FGKMT 또는 Sono의 무한 범위 정리를 증명·반증·검증하는 근거로 사용하지 않는다.
