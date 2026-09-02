# P020 recurrence 정본 artifact 전수 종합 시각화 결과 분석

- 작성: 2026-09-02 11:51 KST
- 정본 실행: `run_20260902T024622Z_p020r2_recurrence_artifact_synthesis`
- 정본 로그: `test_result/logs/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis.log`
- manifest SHA-256: `4fe08a450b01d2d483018c61240c53a8e2b75a4c05864b096775280a9466a101`
- contract SHA-256: `5dc9c131b5f0c5eb4580af6cd0e971a40b8c079f2189846e088ea12313f6eacc`
- 실행 판정: `EXPERIMENT_PASS`
- 과학적 판정: `SYNTHESIS_ONLY`
- 사용자 시각 QA: `PASS` (2026-09-02 사용자 확인)
- 새 prime 계산: **없음**

## 1. 한눈에 보는 결론

P020은 P006·P011·P012-A/B·P013-A/B·P018-P0/A의 정본 결과를 새로 소수를
생성하지 않고 한데 모아, 6개 표와 6개 figure family(PNG·PDF 12파일)를 만들었다. 입력
manifest 8개, 그 manifest에 등록된 모든 artifact hash, 과거 saved verifier의 clean PASS,
새 표·요약의 독립 재계산과 그림 파일의 자동 검사를 모두 통과했다.

그림과 수치가 함께 말하는 핵심은 다음과 같다.

1. 작은 수 범위에서는 같은 record gap이 실제로 다시 나타난다. P006 complete plateau 29개 중
   11개에서 recurrence가 있었고, 첫 발생 뒤 recurrence 합은 20회다.
2. 그러나 모든 위치에서 같은 gap 확률을 쓴 P011 stationary null은 관측 9회에 대해
   109.079회를 기대했다. 위치를 log-x로 층화한 P012-A는 기대값을 8.587회로 낮췄다.
   기대값 감소율은 `92.1274%`다. 즉 초기의 큰 차이는 새로운 수론 현상보다 null 모형의
   위치 비정상성 무시가 만든 과대예측으로 해석하는 편이 타당하다.
3. 독립·전향 범위를 더 크게 계산했지만 primary 기대 recurrence는 P012-B `0.4970`,
   P013-A `0.07783`, P013-B `0.06680`으로 작아졌다. 처리량 증가가 통계 정보량 증가를
   보장하지 않았다.
4. P018-A는 34,570,543,382 gap-start를 처리했지만 gap 582와 588이 각각 forced record 한
   번뿐이었다. 그것을 제거하면 conditioned count·기대값·분산이 모두 0이다. 따라서
   `HOLD_PREFIX_INFORMATION`은 계산 실패가 아니라 “현재 질문으로는 비교 표본이 없다”는
   정확한 정보 판정이다.
5. 이 결과는 recurrence 구조가 없다는 증명이 아니다. 현재의 **exact record-gap 재등장** 질문이
   큰 x에서 너무 희소해졌고, 같은 질문을 더 넓은 decade에 그대로 반복하는 방식의 효율이
   낮다는 증거다.

## 2. 무엇을 종합했는가

P020은 다음 8개 정본 run의 저장 artifact만 읽었다.

| 입력 | 역할 | 원래 범위·성격 |
|---|---|---|
| P006 full | 기술통계 | `[2,10^9]` |
| P011 | stationary-null 진단 | P006 aggregate 재사용 |
| P012-A r2 | stratified development | P006 gap stream 재사용 |
| P012-B | 독립 holdout | `[10^9,10^10)` |
| P013-A r2 | prospective | `[10^10,10^11)` |
| P013-B | prospective | `[10^11,10^12)` |
| P018-P0 | calibration, margin-only | P018-A 내부의 작은 부분범위 |
| P018-A | prefix information, margin-only | `[10^12,1,968,188,556,462)` |

중복을 제거한 **보고 처리량 회계값**은

\[
72{,}178{,}455{,}399
\]

gap-start다. 이 값은 721억 행 raw 자료가 저장됐다는 뜻이 아니다. 각 실험은 prime/gap stream을
순차 처리한 뒤 필요한 plateau·histogram·충분통계만 보존했다.

또한 이 범위를 완전히 이어진 하나의 raw stream이라고 부르지 않는다. `10^9` 경계의

```text
999,999,937 -> 1,000,000,007, gap 70
```

한 건은 P006과 P012-B 어느 쪽의 저장 raw 관측에도 포함되지 않았다. 각 원 실험의 계약과
primary 결과에는 영향이 없지만 “모든 consecutive gap의 빈틈없는 합집합”이라는 표현은 금지한다.

## 3. 정량 결과

### 3.1 P006의 유한 기술통계

| 지표 | 값 |
|---|---:|
| complete plateau | 29 |
| recurrence가 1회 이상인 plateau | 11 |
| 첫 발생을 뺀 recurrence 합 | 20 |
| gap `>=100`인 plateau | 13 |
| gap `>=100`에서 recurrence 합 | 4 |

작은 record gap은 실제 plateau 안에서 반복된다. 다만 이 표는 유한 기술통계이며, 그 반복이
특정 null보다 과도한지 여부는 별도 모형이 필요하다.

### 3.2 stationary null을 층화했을 때의 교정

같은 21개 primary row에서 관측 합은 9다.

| 모형 | 기대 recurrence 합 |
|---|---:|
| P011 전역 stationary null | 109.0790188112 |
| P012-A log-x stratified null | 8.5873760190 |
| 관측 | 9 |

층화 후 기대값은 전역 stationary 값보다 `92.1274%` 작다. 일상적인 비유로는, 초등학교와
대학교의 평균 키를 한 확률로 섞어 비교하던 것을 연령대별로 나눠 비교한 것과 같다. prime-gap
빈도는 위치와 gap 크기에 따라 크게 달라지므로 전역 평균 하나는 후기 record gap을 심하게
과대예측했다.

이 결과가 보여 주는 것은 “층화 null이 참임”이 아니라 다음 두 가지다.

- P011 stationary null은 이 자료의 정본 가설검정 null로 부적절하다.
- P012 층화는 확인된 과대예측을 크게 줄이는 경험적으로 더 나은 기준선이다.

### 3.3 독립·전향 범위

| 단계 | complete primary plateau | 양의 분산 plateau | 관측 | 기대 |
|---|---:|---:|---:|---:|
| P012-B holdout | 4 | 3 | 1 | 0.4970217812 |
| P013-A r2 | 4 | 1 | 0 | 0.0778288135 |
| P013-B | 9 | 1 | 0 | 0.0667971884 |

P012-B의 관측 1은 기대 0.497보다 크지만 기존 정본 family 검정에서 유의하지 않았고, P013-A/B의
0회도 기대 자체가 0에 매우 가까워 구조 부재 증거가 약하다. 세 단계의 모든 primary row가
`LOW_INFORMATION`이었다.

### 3.4 계산량과 정보량의 분리

| 단계 | gap-start 수 | 양의 분산 비율 | LOW_INFORMATION 비율 | primary 기대/10억 gap-start |
|---|---:|---:|---:|---:|
| P012-A r2 | 50,847,533 | 66.7% | 100% | 168.8848 |
| P012-B | 404,204,977 | 75.0% | 100% | 1.2296 |
| P013-A r2 | 3,663,002,302 | 25.0% | 100% | 0.02125 |
| P013-B | 33,489,857,205 | 11.1% | 100% | 0.001995 |
| P018-P0 | 2,232,503,547 | 0% | 100% | 0 |
| P018-A | 34,570,543,382 | 0% | 100% | 0 |

후기 범위는 더 많은 소수를 처리했지만 exact target gap이 희소해져 단위 계산량당 기대 정보가
급락했다. 따라서 현재 병목은 CPU 속도가 아니라 질문이 만들어 내는 비교 표본의 수다.

### 3.5 P018 forced-record funnel

gap 582와 588은 각각 전체 bin에서 한 번 발견됐고, 그 한 번이 해당 record의 강제 첫 발생이다.

```text
target gap count 1
  -> forced record 1개 제거
  -> conditioned count 0
  -> expected 0, variance 0
  -> LOW_INFORMATION
  -> HOLD_PREFIX_INFORMATION
```

P018은 관측 recurrence·residual·p/q/z를 저장하거나 가설검정하지 않았다. 다만 bin 전체 target
count가 forced record 한 번뿐이라는 margin은 추가 recurrence가 0임을 논리적으로 드러낸다.
따라서 이를 강한 outcome-blind가 아니라 `margin-only / allocation-blinded information probe`로
부르는 것이 정확하다.

## 4. 각 figure가 설명하는 것

모든 figure의 PNG와 PDF는
`test_result/run_20260902T024622Z_p020r2_recurrence_artifact_synthesis/figures/`에 있다.

### Figure 1 — `01_recurrence_coverage_map`

각 실험이 어느 log-x 범위를 맡았고 development, holdout, prospective, information-only 중 어떤
역할인지 보여 준다. P011/P012-A가 P006 자료를 재사용하고 P018-P0가 P018-A에 포함되므로 단순
합산하면 중복된다는 점, `10^9` crossing gap 한 건이 seamless raw union에서 빠진다는 점도 표시한다.

### Figure 2 — `02_p006_descriptive_recurrence`

P006의 complete plateau별 gap 크기, 최초 포함 출현 수 `M`, 최초 이후 recurrence `C`를 보여 준다.
초기 작은 gap에서는 recurrence가 보이지만 큰 record gap으로 갈수록 희소해지는 유한 패턴을 읽을
수 있다. 이것만으로 enrichment를 판정하지 않는다.

### Figure 3 — `03_null_model_correction`

같은 21개 row에서 관측값, P011 stationary 기대값, P012 stratified 기대값을 나란히 비교한다.
P011의 큰 기대값이 몇몇 gap에서 발생한 위치효과 무시 때문이며, 층화 후 관측과 기대의 전체 규모가
비슷해졌음을 보여 준다.

### Figure 4 — `04_prospective_stage_summary`

P012-B·P013-A/B의 primary 관측과 기대를 단계별로 표시한다. x 범위가 커지는데도 기대 recurrence가
증가하지 않는다는 점을 보여 준다. 서로 다른 단계의 p-value를 연결하거나 합치지 않는다.

### Figure 5 — `05_information_collapse`

단계별 기대 recurrence, 양의 분산 비율, LOW_INFORMATION 비율을 한눈에 비교한다. 모든 단계가
LOW_INFORMATION 100%이고, P018에서는 양의 분산도 0이라는 사실을 강조한다. “계산 범위가 크다”와
“가설검정 정보가 많다”를 분리해 보여 주는 핵심 figure다.

### Figure 6 — `06_p018_forced_record_funnel`

P018의 target count 1이 forced record 제거 뒤 0이 되고, 그 결과 분산과 검정 가능성이 0으로
닫히는 과정을 단계식으로 보여 준다. 이는 P018-B 자동실행을 막은 gate가 왜 타당했는지 설명한다.

## 5. 검증과 재현성

- 고정 Python: `W:\miniforge3\envs\FGKMT\python.exe`, Python 3.11.16
- `pip check`: broken requirement 0
- iterated-log 회귀시험: 7/7 PASS
- P020 toy: 4/4 PASS
- 전체 unittest: 201/201 PASS, 34.320초
- 입력 manifest: 8/8 SHA-256 일치
- manifest 내부 artifact: 전부 SHA-256 일치
- 원 실행 saved-verifier: 전부 clean PASS 및 manifest 연결 일치
- P020 표·summary saved full recomputation: PASS
- P018 margin-only output contract: PASS
- PNG/PDF 파일 수·decode·크기·hash: PASS
- 정리 주장: `false`
- 새 prime sweep: `false`

R1 `run_20260902T024226Z_p020_recurrence_artifact_synthesis`도 수치 검증은 PASS했다. 그러나 Codex
시각 점검에서 좁은 라벨·주석 겹침, Figure 3의 상자 위치, Figure 5의 상수 열 색 전달을 보완할
필요가 있었다. R1은 변경하지 않고 보존했으며, 수치와 contract가 같은 R2를 새 run으로 만들었다.
따라서 해석 정본은 R2다.

## 6. 사전검증 중 발견한 절차 오류

초기 P020 input verifier가 기존 P012/P013의 `verify_saved_*`를 이름만 보고 저장표 전용 함수로
잘못 판단했다. 실제로는 segmented prime-range 전체 재계산 함수였고, P013 재계산이 시작된 것을
발견한 즉시 그 P020 preflight process만 중단했다.

- 발견 시점: P020 result directory와 figure 생성 전
- P020 과학 산출물: 0
- 다른 사용자 프로세스: 중단하지 않음
- 교정: manifest hash, manifest 안의 모든 artifact hash, 원 실행의 clean saved-verifier 증거만
  확인하는 경량 verifier로 교체
- 회귀 확인: 약 8초 내 8/8 PASS, prime iterator 호출 없음
- 오류 원장: `ai_dev_tool/05_ChatGPT_오류_실수_환각_원장.md`의 E018

이 실수는 최종 R2 결과의 수치에는 영향을 주지 않았지만, “새 prime 계산 없음” 승인 경계를
preflight 구현이 잠시 침범한 절차 오류이므로 숨기지 않고 보존한다.

## 7. 연구적으로 새로 알게 된 것

### 확인된 것

- 초기 record gap recurrence는 유한 범위에서 실제 존재한다.
- 위치를 무시한 stationary null은 recurrence를 크게 과대예측한다.
- log-x 층화는 그 과대예측을 크게 줄인다.
- 큰 범위의 처리량은 exact-record-gap 정보량의 대리변수가 아니다.
- P018-A는 비교 표본이 0이라는 이유로 B 자동승격을 멈춘 올바른 gate였다.

### 아직 열린 것

- recurrence enrichment가 실제로 존재하는가
- singular-series와 record selection을 함께 반영한 더 나은 null은 무엇인가
- exact gap 하나가 아니라 사전 고정한 gap family를 쓰면 정보량을 늘릴 수 있는가
- 그 질문 변경이 원래 recurrence 질문과 어떤 관계를 갖는가

### 현재 버려야 할 해석

- P011 stationary null을 정본 null로 유지하는 것
- decade를 넓히기만 하면 power가 자동 증가한다는 가정
- 관측 0회를 recurrence 구조 부재의 강한 증거로 읽는 것
- P018-A PASS를 P018-B 실행 승인으로 바꾸는 것

## 8. 한계와 다음 결정

P020은 저장 artifact 수준의 전수 종합이다. 721억 raw point를 저장하거나 새 bin으로 다시 세지
않았고, P018에서 금지된 관측 allocation을 복원하지 않았다. 서로 다른 null·cohort의 p-value도
pooling하지 않았다.

현재 권장 결정은 다음과 같다.

1. P018-B와 P013-C brute-force는 계속 `HOLD`한다.
2. recurrence 축은 폐기하지 않고 새 질문·formal power·독립 holdout 설계를 기다린다.
3. 다음 주 연구축은 계산을 더 늘리는 것보다 Sono/FMT numerical-threshold proof dependency를
   감사하는 쪽이 가치가 높다.
4. 사용자는 2026-09-02 R2의 6개 PNG에 문제가 없다고 확인했다. 자동 수치 QA와 사용자
   시각 QA가 모두 PASS다.

## 9. 최종 판정

\[
\boxed{
\begin{aligned}
&\text{실행·saved 검증: PASS}\\
&\text{새 prime 계산: 없음}\\
&\text{recurrence enrichment: OPEN / NOT DETECTED}\\
&\text{P018-B 자동승격: HOLD}\\
&\text{사용자 figure QA: PASS}
\end{aligned}
}
\]

P020의 가장 중요한 성과는 여러 실험을 한 그림에 넣었다는 사실보다, **계산량·재현성·통계
정보량을 서로 다른 축으로 분리했다는 것**이다. 현재 recurrence 연구의 다음 병목은 연산 능력이
아니라 답할 수 있는 표본을 만드는 연구 질문의 재설계다.

## 10. 사용자 시각 QA 사후 기록 — 2026-09-02

사용자가 여섯 figure 모두 문제없다고 회신했다. 이 확인은 배치·가독성 판정이며 저장 수치,
통계 해석, `SYNTHESIS_ONLY` 과학 판정을 바꾸지 않는다. 실제 run의 immutable manifest에 남은
`PENDING_USER`는 소급 수정하지 않고 이 결과보고서와 계획서에서 후속 증거로 닫는다.
