# P018-A blinded prefix information probe 결과 분석

- 분석 작성: 2026-09-02 10:00 KST
- 실행 ID: `20260901T125849Z_p018a_prefix_information_probe`
- 판정:
  - `EXPERIMENT_PASS`
  - `HOLD_PREFIX_INFORMATION`
  - `LOW_INFORMATION = 100%`
  - `NO_HYPOTHESIS_TEST`
  - `NO_AUTOMATIC_FULL_RANGE_PROMOTION`
- figure: 계획상 생성하지 않음; 시각 QA 대상 없음

## 1. 쉬운 결론

프로그램과 검증 절차는 정상적으로 끝났다. 약 5시간 49분 동안
`[10^12, 1,968,188,556,462)`의 gap-start 34,570,543,382개를 두 개의 서로 다른
segment 분할로 모두 계산했고, 두 결과는 정확히 같았다.

그러나 이 구간은 recurrence 질문에 답할 정보를 만들지 못했다. 조사한 maximal record gap은
582와 588인데, 각각이 해당 primary bin에서 정확히 한 번만 나타났다. 그 한 번은 바로 record
자신이므로 설계대로 강제 record를 제거하면 같은 크기의 비교 대상이 둘 다 0개가 된다.

일상적인 비유로 설명하면, “같은 물건이 다시 나오는 비율”을 재려고 상자를 모두 열어 봤는데
기준 물건 한 개씩만 있고 복제품은 하나도 없었다. 계산기는 정확히 작동했지만, 비교할 표본이
없어서 증가·감소를 판단할 수 없는 상태다.

따라서 A gate의 HOLD는 코드 실패나 recurrence 가설 기각이 아니다. 미리 정한 규칙에 따라
“이 prefix만으로는 B full-range 계산의 정보가치를 지지하지 못한다”고 판정한 것이다.

## 2. 입력과 동결 계약

| 항목 | 값 |
|---|---|
| 모드 | `A_EXPLORATORY_PREFIX_ONLY` |
| gap-start 범위 | `[1,000,000,000,000, 1,968,188,556,462)` |
| 완결 record index | 51, 52 |
| record gap | 582, 588 |
| source commit | `1a112a1387052d9ad360686313f501c01fe46b68` |
| validated records SHA-256 | `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297` |
| frozen contract SHA-256 | `7171efef2659340e240993a384f5dfdfb1b5d60c1b1ab20880aa2129317b0f92` |
| verified exhaustive limit | `10^20` |
| boundary semantics | gap-start half-open range; complete plateau만 사용 |

결과 디렉터리에 복사된 contract hash는 사전계획의 frozen contract와 일치했다. endpoint, gate,
중단조건을 결과를 본 뒤 바꾼 흔적은 없다.

## 3. 실행·무결성 감사

### 3.1 원본 로그

- log:
  `test_result/logs/run_20260901T125849Z_p018a_prefix_information_probe.log`
- byte size: 12,841
- SHA-256:
  `7cd15ad17ca1979c1c62069ddbdcea637ee6814c6b90542c7c518d46fa30418e`
- `[FAIL]`: 0개
- targeted unit tests: 25/25 PASS
- 마지막 계산 stage: `p018-a-saved-blinded-recomputation` PASS
- terminal marker:
  `[PASS] P018-A blinded prefix information probe completed.`
- BAT launcher marker:
  사용자가 `[PASS] P018-A prefix launcher completed.`를 확인해 회신

사후감사에서 같은 25 tests를 sandbox 안에서 다시 실행한 첫 시도는 23개가
`TemporaryDirectory`·Windows multiprocessing pipe `PermissionError`로 끝났다. assertion
failure는 없었다. 동일 명령을 정상 로컬 권한으로 재실행해 25/25 PASS했으므로 코드 회귀와
실행환경 실패를 분리했다.

### 3.2 runtime과 자원

| 구분 | 값 |
|---|---:|
| 사전 예상 full path | 7–10시간 |
| 실제 full dual-pass 계산 | 20,940.094초 = 약 5.8167시간 |
| hard wall | 12시간 |
| 처리한 gap-start | 34,570,543,382 |
| 기술적 처리량 | 약 5.94 billion gap-start/hour |
| CPU 정책 | 물리 4코어·논리 8프로세서, affinity `0xff` |
| worker | 각 pass에서 8개 관측 |
| worker native thread ceiling | 1 |
| GPU | 사용하지 않음 |
| process-tree RAM ceiling | 31.5 GB, Job Object 적용·child 상속 확인 |
| 관측 peak RAM | 측정값 없음 |

이 실행은 gate 조기종료가 아니라 두 full pass와 saved verification을 모두 마친 full path다.
기술적 처리량은 이번 범위의 관측값일 뿐, 다른 범위의 시간을 선형 외삽하는 보장값으로 쓰지 않는다.

### 3.3 artifact와 hash

- result directory:
  `test_result/run_20260901T125849Z_p018a_prefix_information_probe`
- manifest artifact: 21개
- 독립 hash 재대조 issue: 0
- result directory 전체: 23 files, 38,920 bytes
- manifest SHA-256:
  `c0a1309d7bb33ac5de8f4840f3198f4b223f26f30c198c72490c0742c10b75ad`
- progress log: 200 lines, START·5분 heartbeat·END PASS 보존
- progress log SHA-256:
  `2bcbd1b4435be4aa07feba296a3c370c7b9a5222cf9e5942302e49e745669d4e`

현재 source·공통 runner·contract hash는 실행 로그에 기록된 값과 모두 일치했다.

## 4. exact count와 dual-partition 검증

독립 `primecount` 입력은 Gourdon과 Deleglise–Rivat 두 알고리즘이 같은 값을 냈다.

\[
\pi(1{,}968{,}188{,}556{,}461)=72{,}178{,}455{,}400,
\]

\[
\pi(999{,}999{,}999{,}999)=37{,}607{,}912{,}018.
\]

따라서 exact gap-start 수는

\[
72{,}178{,}455{,}400-37{,}607{,}912{,}018
=34{,}570{,}543{,}382
\]

이며 저장 결과와 일치한다.

prime stream 계산은 다음 두 full pass로 수행됐다.

| 검증 | primary | verifier |
|---|---:|---:|
| segment 수 | 64 | 65 |
| 서로소 여부 | 예 | 예 |
| adjacent boundary checks | 63 | 64 |
| 관측 worker | 8 | 8 |

- exact sufficient statistics equality: PASS
- interior boundary overlap: 0
- omitted work item: 없음
- precision reduction: 없음
- observed equal-count 직접 통계 저장: 하지 않음

두 pass는 분할 경계가 다르므로 segment 누락·중복을 강하게 점검한다. 다만 같은 sieve와
accumulator kernel을 공유하므로 완전히 독립적인 수학 oracle은 아니다. 이 공통-mode 위험은
`dual_partition_verification.json`에도 명시돼 있다.

## 5. 정보량 결과

### 5.1 primary 두 행

| record | gap | bin 안의 같은 gap 수 | forced record 제거 후 | expected | variance | 판정 |
|---:|---:|---:|---:|---:|---:|---|
| 51 | 582 | 1 | 0 | 0 | 0 | LOW_INFORMATION |
| 52 | 588 | 1 | 0 | 0 | 0 | LOW_INFORMATION |

두 record가 속한 primary bin의 population은 34,570,543,382다. 강제 record를 하나 제거한
population은 34,570,543,381이지만, conditioned gap count가 0이므로 exposure가 아무리 커도
hypergeometric 기대값과 분산은 정확히 0이다.

사전등록한 두 sensitivity scheme의 추가 5개 행도 모두 conditioned count·expected·variance가
0이고 `LOW_INFORMATION`이었다. 즉 특정 primary bin 경계 하나 때문에 생긴 결과가 아니다.

### 5.2 A gate 네 조건

| 조건 | 사전 기준 | 실제 | 통과 |
|---|---:|---:|---|
| null recurrence가 1회 이상일 proxy 확률 | 0.25 이상 | 0 | 실패 |
| positive-variance primary rows | 2 이상 | 0 | 실패 |
| LOW_INFORMATION 비율 | 0.75 이하 | 1.00 | 실패 |
| 5x Poisson planning power | 0.60 이상 | 0 | 실패 |

5x planning proxy가 60% power에 도달하려면 null expected recurrence가 최소 약 0.6211이어야
하지만 실제 primary total은 0이었다. 이 proxy는 계산가치 선별 지표이며 정식 stratified
hypergeometric power 인증은 아니다.

독립 재계산으로 얻은 `expected=0`, positive-variance row 0, LOW_INFORMATION 100%,
structural gate FAIL, power gate FAIL은 저장 `prefix_gate_report.json`과 정확히 일치했다.

## 6. saved blinded recomputation의 의미

saved verifier는 저장 margin에서 information component와 gate를 다시 계산했고 다음을 확인했다.

- saved blinded margin recomputation: PASS
- issue: 0
- manifest hash: 일치
- hypothesis test: 수행하지 않음
- theorem claim: 없음

saved verifier는 34,570,543,382개 prime range를 세 번째로 다시 sieve하지 않았다. full range는
이미 64/65 dual pass가 계산했다. 따라서 saved verifier의 독립성은 artifact·margin·gate
재구성 범위이며, prime generation kernel까지 독립적인 것은 아니다.

## 7. 과학적으로 말할 수 있는 것

1. frozen A prefix와 사전등록 margin에서 recurrence 분석 정보량은 정확히 0이었다.
2. 582와 588은 해당 분석 bin에서 강제 record 외의 conditioned occurrence가 없었다.
3. 이 때문에 더 정교한 p-value 계산 문제가 아니라, 검정에 넣을 변동 자체가 없는 구조적
   LOW_INFORMATION 문제가 발생했다.
4. A는 사전계획대로 `HOLD_PREFIX_INFORMATION`을 반환했다.
5. A 결과는 B full-range 실행을 자동 승인하지 않으며, 현재 증거는 오히려 B를 바로 실행하지
   말고 설계를 재검토하라는 방향이다.

## 8. 말할 수 없는 것

- recurrence enrichment가 없다고 증명하지 않았다.
- recurrence 가설을 기각하거나 채택하지 않았다.
- 관측 recurrence, p-value, q-value, z-score를 계산·저장하지 않았다.
- B 범위도 반드시 정보량 0이라고 증명하지 않았다. B는 새 record와 범위를 추가하므로 별도다.
- prime-gap theorem, FGKMT/Sono threshold, maximal-gap completeness 또는 search acceleration을
  증명하지 않았다.
- A의 처리속도를 B나 다른 범위에 선형 외삽해 보장할 수 없다.

## 9. 후속 판정

### P018-B

현재는 `HOLD`를 권장한다. A가 B 설계 검토를 요청할 최소 gate조차 통과하지 못했고, 34.57
billion gap-start를 계산해도 모든 pre-registered scheme에서 정보량이 0이었다. B를 즉시
12–16시간 계산하는 것은 비용 대비 근거가 부족하다.

B 자체가 논리적으로 불가능하다는 뜻은 아니다. 다시 검토하려면 다음을 먼저 해야 한다.

1. A와 겹치는 development evidence와 향후 판정 범위를 분리한다.
2. 결과를 본 뒤 유리한 gap·bin만 고르는 것을 막는 새 frozen contract를 만든다.
3. 적어도 positive-variance row가 생길 합리적 사전 근거를 제시한다.
4. 새 설계가 기존 recurrence 질문을 바꾸는지 명시한다.

### recurrence 연구축

현재까지 P011–P013과 P018-A는 일관되게 “코드가 실패했다”가 아니라 “희귀 record gap의
recurrence를 판정하기에 정보가 지나치게 적다”는 결과를 냈다. 따라서 같은 형태의 더 큰
계산을 바로 반복하기보다, 독립 범위·다른 summary statistic·record gap이 아닌 대조 gap군을
사용해도 원래 연구 질문을 보존할 수 있는지 방법론 검토를 먼저 하는 편이 타당하다.

## 10. 권장 다음 순서

1. **P018 recurrence 설계 사후감사 — Codex 2–4시간**
   - 목적: 현재 연구 질문을 유지하면서 positive-variance 정보를 만들 수 있는 독립 설계가
     존재하는지, 아니면 이 연구축을 종료·보류해야 하는지 판정한다.
   - 사용자 수행절차: 별도 수행절차 필요없음.
2. **Sono/FMT explicit-threshold proof-dependency audit — Codex 3–8시간**
   - 목적: “sufficiently large”를 numerical `X_0`로 바꾸는 데 필요한 비명시 상수와 보조정리를
     목록화한다.
   - 사용자 수행절차: 별도 수행절차 필요없음.
3. **P014 bounded-seed LP 이론·toy — Codex 2–6시간**
   - 목적: restricted LP가 bounded가 되는 충분조건과 strict improvement 가능성을 확인한다.
   - 사용자 수행절차: 별도 수행절차 필요없음.
4. **P018-B, P019 actual, P013-C — HOLD**
   - 선결 gate가 없으므로 현재 실행 명령을 제공하지 않는다.

## 11. 최종 판정

\[
\boxed{
\text{P018-A}
=\text{EXPERIMENT PASS}
\land\text{HOLD PREFIX INFORMATION}
\land\text{NO AUTOMATIC PROMOTION}
}
\]

계산과 검증은 성공했다. 과학적 결론은 “A prefix에서 정보를 얻지 못했다”이며, 이는 음성 결과로
보존해야 한다. B를 자동 실행하거나 recurrence 부재·수론 정리로 확대 해석하면 안 된다.
