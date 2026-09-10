# FGKMT/Sono 정규화와 maximal-gap 경계

## 지위

`DEFINITION + THEOREM + EXACT_FINITE`

## 반복로그와 scale

모든 로그는 자연로그이며 아래 첨자는 반복 횟수다.

\[
\log_kx=\underbrace{\ln(\ln(\cdots\ln x))}_{k\text{회}},\qquad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}.
\]

base-2/3/4 로그는 금지한다. `F(x)>0`인 프로젝트의 최소 정수 시작점은
`3,814,280`이다.

Lean 커널 검증에서는 소수 근사값을 가정하지 않고 연속 경계
`scaleThreshold = exp(exp(exp(1)))`를 사용한다. `x > scaleThreshold`이면 의도한
양의 반복로그 branch에서 `F(x)>0`이고 `F`가 엄격히 증가함을, 외부 가정과
proof escape 없이 형식화했다. 100-dps Python 대조에서 이 실수 경계는
`3814279.104760220592209...`이므로 첫 정수가 `3,814,280`이다. 단, 이 소수점
경계대조 자체는 현재 Lean 커널 증명이 아니라 독립 수치 검사다.

## 두 maximal-gap finite 함수

Sono와 프로젝트 canonical 함수는

\[
G_{end}(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

이다. FGKMT 원문의 finite 표기와 대조할 보조 함수는

\[
G_{start}(x)=\max_{p_n\le x}(p_{n+1}-p_n)
\]

이다. scale을 비교할 수는 있지만 둘을 같은 함수라고 쓰지 않는다.

## integer interval minimum 정리

record `i`의 start, end, gap을 `s_i,e_i,g_i`라 하면 canonical 정수 plateau는

\[
e_i\le x\le e_{i+1}-1,\qquad G_{end}(x)=g_i.
\]

양의 scale 구간에서 `F`가 증가하므로

\[
\boxed{H_{i,min}=\frac{g_i}{F(e_{i+1}-1)}}
\]

이다. 실수 domain에서는 `[e_i,e_{i+1})`이므로 minimum이 아니라
`x -> e_(i+1)-`에서의 infimum이다. 마지막 record는 verified exhaustive limit까지만
닫는다.

`lean/FGKMTSono/TheoryVerification.lean`의 `intervalMinimum_is_minimum`은 정수 plateau의
임의의 `x`에서 오른쪽 끝점 표현이 더 크지 않음을 Lean 커널로 검증한다.
이 명제는 end-bounded 정수 경계와 scale 단조성을 결합한 것이며, 실수
half-open plateau의 infimum 주장이나 maximal-gap record 데이터의 완전성을 증명하는
명제는 아니다.

## 검증 상태

- P003: 64 end-bounded intervals, 모든 `F/H`와 envelope 100-dps 재계산 PASS
- P004: 64 start/end paired intervals, 차이가 생기는 50,016 integer windows 확인
- global minimum record와 주요 local-envelope 판정은 경계 선택으로 바뀌지 않음

이 명제들은 `10^20`까지의 고정 자료에 관한 finite 결과다. FGKMT/Sono 무한범위
정리의 재증명 또는 수치 threshold 검증이 아니다.

## 의존 문서

- `docs/METHODS.md`
- `test_result/202608230503_P003_full_analysis.md`
- `test_result/202608231652_P004_sensitivity_analysis.md`
