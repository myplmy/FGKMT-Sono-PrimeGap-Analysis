# FGKMT-Sono maximal prime-gap empirical analysis

검증된 maximal prime-gap records로 end-bounded maximal gap을 복원하고, Ford–Green–Konyagin–Maynard–Tao(FGKMT)의 large-gap scale에 대한 정규화값과 empirical lower envelope를 분석하는 재현 가능한 계산 연구 프로젝트다.

## 현재 상태

P003 COMPLETED / AUTOMATED VERIFICATION PASS / FULL GRAPH USER QA PENDING

authoritative run `20260822T195906Z_full1e20`에서 \(10^{20}\)까지 64개 end-bounded interval을 분석했다. 100-dps 수치 1,160개, OEIS 84개 record, Oliveira e Silva 별도 계산자료 75개가 모두 일치했다. PNG 8종은 사용자 시각 QA 대기다.

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

    .\run_full_analysis.ps1 -Approved

## 문서

- AGENTS.md: Codex 작업·수학·데이터·승인 규약
- 연구 작업지시서: 연구 목적과 전체 분석 요구
- docs/METHODS.md: 계산·검증 방법론 정본
- docs/review/: 문헌별·종합 분석
- test_plan/: 실행 전 고정 계획
- test_result/202608230503_P003_full_analysis.md: 일상용어 전체 결과 분석
- docs/review/10_P003_문헌비교와_후속가설.md: 문헌 비교와 반증 가능한 후속 가설
- handoff/: 세션마다 새로 만드는 `YYYYMMDDHHmm_HANDOFF.md`; 최신 파일에 현재 상태와 다음 작업 기록

유한 계산 결과는 FGKMT 또는 Sono의 무한 범위 정리를 증명·반증·검증하는 근거로 사용하지 않는다.
