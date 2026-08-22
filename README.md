# FGKMT-Sono maximal prime-gap empirical analysis

검증된 maximal prime-gap records로 end-bounded maximal gap을 복원하고, Ford–Green–Konyagin–Maynard–Tao(FGKMT)의 large-gap scale에 대한 정규화값과 empirical lower envelope를 분석하는 재현 가능한 계산 연구 프로젝트다.

## 현재 상태

PREPARATION_ONLY / WAITING_FOR_USER_APPROVAL

코드·문서·합성 데이터 시험만 준비했다. 실제 dataset 다운로드, validation, maximal-gap 분석, 결과 표·그래프 생성은 아직 수행하지 않았다.

## 수학 정의

[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n),
qquad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},
qquad
H(x)=\frac{G(x)}{F(x)}.
]

여기서 log_k(x)는 자연로그를 k회 반복한 값이다. 아래 첨자는 로그의 밑이 아니다.

[
\log_2x=\ln(\ln x),\quad
\log_3x=\ln(\ln(\ln x)),\quad
\log_4x=\ln(\ln(\ln(\ln x))).
]

canonical 경계는 gap의 끝 소수 p_(n+1)가 x 이하인 경우다. 분석은 F(x)>0인 최소 정수 x=3,814,280부터 시작한다.

## 데이터

- canonical repository: https://github.com/primegap-list-project/prime-gap-list
- commit-pinned inputs: allgaps.sql, schema.sql
- 참고용 high-watermark page: https://primegap-list-project.github.io/lists/prime-gaps-high-watermarks/
- exhaustive coverage 참고: https://primegap-list-project.github.io/fully-analyzed/

웹페이지를 dataset으로 스크레이핑하지 않는다. 승인 후 실행 시 master를 다시 조회하고 40자리 commit을 고정한 뒤 파일별 URL, 취득 UTC, byte 수, SHA-256을 기록한다.

## 환경

연구 코드와 테스트는 다음 Python을 사용한다.

    W:\miniforge3\envs\FGKMT\python.exe

승인 전에 허용되는 검증:

    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli preflight
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli status
    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli fetch --dry-run

실제 실행은 사용자가 목적·정의·데이터 범위·수행방법을 확인하고 명시적으로 허가한 뒤에만 다음 명령으로 수행한다.

    .\run_experiment.ps1 -Approved

## 문서

- AGENTS.md: Codex 작업·수학·데이터·승인 규약
- 연구 작업지시서: 연구 목적과 전체 분석 요구
- docs/METHODS.md: 계산·검증 방법론 정본
- docs/review/: 문헌별·종합 분석
- test_plan/: 실행 전 고정 계획
- HANDOFF.md: 현재 상태와 다음 작업

유한 계산 결과는 FGKMT 또는 Sono의 무한 범위 정리를 증명·반증·검증하는 근거로 사용하지 않는다.

