# H1b-P91a unweighted moment·W-filter 적용성 검토

- 검토일: 2026-09-09 KST
- 정본 증명: [theory 45](../method/theory/45_Sono_FMT_H1bP91a_unweighted_moment_W_filter.md)
- 기계 계약: [P91a contract](../method/theory/data/Sono_FMT_H1bP91a_unweighted_moment_v1.json)
- 판정: 명시적 Maynard W-filter를 쓰는 actual child의 finite proof 완료; 전체 정리 미완료
- 핵심 정정: 과거 P92a의 적용 범위를 filtered weight로 명시; unfiltered transfer는 인증하지 않음

## 1. 쉽게 설명하는 이번 목적

각 정수에 “좋은 소수 후보일수록 높은 점수”를 붙였다고 생각하면 된다.

- P92는 **소수에 붙은 점수만** 더하는 문제였다.
- P91은 **모든 정수에 붙은 점수**를 더하는 문제다.
- 나중에 소수를 뽑을 확률을 만들려면, 분자뿐 아니라 전체 점수인 분모도 정확히 알아야 한다.

이번에는 전체 점수의 예측식, 오차 한계, 구간 이동, 끝 정수 개수의 차이를 한꺼번에 정리했다.
단순히 소수를 더 많이 계산한 것이 아니라 증명에 남은 모호한 상수를 수치식으로 바꾼 작업이다.

## 2. 실제로 얻은 결과

원문의 긴 구간을 \([-Y,Y]\)라고 할 때, 정수만 포함하면
\(-\lfloor Y\rfloor,\ldots,\lfloor Y\rfloor\)가 들어간다.
이를 양의 구간으로 옮기면 \([2\lfloor Y\rfloor,4\lfloor Y\rfloor]\)가 되고,
정수는 정확히 \(2\lfloor Y\rfloor+1\)개다.

예를 들어 \(Y=10.7\)이면 정수는 -10부터 10까지 **21개**다.
길이 \(2Y=21.4\)와 개수가 같지는 않지만 차이는 1 이하이다.
큰 수에서 작아 보이는 차이도 finite proof에서는 빼먹으면 안 된다.

이번 증명은
\[
 k=\lfloor(\log(X/2))^{1/5}\rfloor\ge10^{200}
\]
에서 전체 점수의 relative error를
\[
 \eta_k=10^{134}(\log k)^4/k^2
\]
이하로, 구간 길이 \(2Y\)에 맞춘 값의 error를 \(2\eta_k\) 이하로 묶는다.
둘 다 원문의 허용 오차보다 작다. 실제 충분조건은 \(X\ge2\exp(10^{1000})\)다.

**이 값은 이 하위 증명의 보수적 충분조건일 뿐이다.**

- 그 수까지 실제 소수를 검사하지 않았다.
- Sono 부등식이 시작하는 최소 수를 찾은 것이 아니다.
- 전체 정리의 \(X_{\rm cert}\)를 얻은 것도 아니다.
- 이 cutoff를 작게 최적화한 것도 아니다.

## 3. 새로 발견한 원문 차이와 과거 설명 교정

Maynard 출판 p.1530 (7.5)는 “작은 소수에 이미 걸린 정수의 점수는 0”이라는 필터를
명시한다. FGKMT p.98 (7.4) 표시식에는 이 필터가 보이지 않는다.
그런데 FGKMT가 인용하는 Maynard P91/P92 증명은 필터를 사용한다.

이를 단순히 같다고 넘길 수 없다. toy에서 점수가 원래 전부 9이고,
30으로 나눈 나머지 중 허용되는 3개만 남긴다면 총점은 270과 27로 달라진다.
“큰 divisor에만 coefficient가 있다”는 다른 조건이 이 작은 소수 필터를 대신해 주지 않는다.

이번 조치:

1. 사용할 weight를 Maynard와 같은 명시적 filtered weight로 정의했다.
2. 정수 구간 이동은 필터까지 정확히 보존함을 증명했다.
3. P92에서 두 소수 p,q를 교체하는 변환도 둘 다 W와 서로소이면 필터를 보존함을 증명했다.
4. 기존 P92a의 수치 증명은 이 filtered weight에 대한 결과로 명시했다.
5. unfiltered 정의로 certificate를 요청하면 코드가 거부한다.

직전 P92a에서 이 적용 범위를 충분히 명시하지 않은 것은 프로젝트 감사의 누락이었다.
[오류 원장](../../ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md)에 공개했다.
원문 PDF, 과거 핸드오프, 실제 empirical 결과는 고치지 않았다.

이 발견을 “Sono의 정리가 틀렸다”거나 “정식 erratum이 확인됐다”라고 해석하면 안 된다.
현재 확인한 것은 표시식과 인용 proof 사이의 정의 차이이며,
명시적 filtered construction으로 보완할 수 있는 경로를 제공한 것이다.
전체 FMT/Sono 증명에 충분한지는 남은 공통 합성으로 확인해야 한다.

## 4. 선행연구 재사용과 자체 증명 범위

| 자료·위치 | 채택/미채택 이유 |
|---|---|
| [Maynard 2016](https://doi.org/10.1112/S0010437X16007296), arXiv:1405.2593, (7.5), (9.1)--(9.15) | 정확한 weight·CRT·대각/비대각 구조는 그대로 재사용 |
| [FGKMT 2018](https://doi.org/10.1090/jams/876), arXiv:1412.5029, pp.95,97--101 | closed interval, actual shift, R, empty selected subset 확인 |
| [저자 호스팅 FGKMT 원고](https://ford126.web.illinois.edu/wwwpapers/primegaps2.pdf), (7.4) | 같은 filter 미표시를 보조 대조; 공식 교정본으로 주장하지 않음 |
| [PrimeGapsLib S1_aggregate](https://github.com/AxiomMath/PrimeGapsLib/blob/main/PrimeGapsTheory/Sieve/S1/ApplyPartialSum.lean) | fixed-k 존재형 C,N0·다른 W/profile 정규화라 즉시 쓸 numerical theorem은 아님 |
| theory 23·24·28·44 | 교정된 summation, finite smooth composition, coefficient lower/upper, uniform integral 비교 재사용 |

새로 채운 부분은 실제 T' 조건, 정확한 정수 discrepancy, 상수 1,384,128의 재배치 오차,
W-factor cancellation, 끝점 및 필터 호환성이다.
적합한 drop-in 증명을 표적 검색에서 못 찾았다는 사실을 세계적 novelty로 바꾸지 않는다.
Lean repository의 전체 axiom/build를 감사하지 않았고 새 Lean 설치도 하지 않았다.

## 5. 검증 증거

환경: Windows PowerShell / 프로젝트 루트 /
W:\miniforge3\envs\FGKMT\python.exe.

~~~powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_h1bp91a_unweighted_moment tests.test_h1bp92a_identity_prime_moment tests.test_h1b_maynard_constant_ledger -v
~~~

- 새 P91 시험 15개 + P92 16개 + H1b 원장 7개: **38/38 PASS, 0.109초**.
- py_compile: 변경 helper 2개·새 test 1개 PASS.
- source/proof dependency 10개 SHA-256 대조 PASS.
- exact dimension bin 바로 아래·위, float/bool/NaN, unfiltered 정의의 잘못된 입력 거부.
- toy는 원문 식을 그대로 복사한 검사뿐 아니라 divisor membership에서 local matrix를 다시 계산한다.

최소 k에서 scalar 진단 29개 PASS:
\( \eta_k\approx4.49762\cdot10^{-256}\),
\(2\eta_k\approx8.99524\cdot10^{-256}\),
허용 오차의 보수적 하한 \(\approx9.33033\cdot10^{-101}\).
1062 dps에서 계산하되 X,Y,T',W나 k개 원소 배열을 만들지 않았다.
이 수치 점검은 모든 k에 대한 문서 증명의 보조 검사이며 독립 수학 심사의 대체가 아니다.

상위 H1c/T1까지 동기화한 표적 검사는 59/59 PASS(0.132초), 그 통과를 확인한 뒤 실행한
전체 회귀는 449/449 PASS(59.546초)였다. 실제 데이터 실험이 아니라 toy/unit 회귀다.
문서 참조·staged scope 검사는 마감 원장과 핸드오프에 별도 기록한다.

## 6. 다음 권장 순서

아래는 문헌·증명 작업 시간의 계획 추정이다. 장시간 CPU 실행 예상이 아니다.

| 순서 | 작업 | 이유 | 예상시간 | 사용자 절차 |
|---|---|---|---:|---|
| 1 | H1b-P94g growing-k 호환성·filtered weight | 아직 필수인 다른 moment에 같은 차원 경로를 적용 | 1--3시간; 검산 수초--수분 | 별도 수행절차 필요없음 |
| 2 | H1b-NORM singular-series/λ/weight/τ/u 합성 | 개별 점수식을 하나의 확률식으로 연결 | 2--6시간 | 별도 수행절차 필요없음 |
| 3 | actual dependency 가지치기·PAP/UB·hypergraph rate | 전체 numerical threshold의 나머지 관문 식별·복원 | source 감사 뒤 재산정 | 현재 별도 수행절차 필요없음 |

현재 사용자 PC에서 돌릴 actual runner, 새 설치, 새 figure QA 요청은 없다.
필수 원문이나 장시간 계산이 실제로 필요해지면 환경·명령·시간·회신 항목을 별도 안내한다.
