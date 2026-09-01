# P018 prefix 정보율 probe 영향도 분석

최종 갱신: 2026-09-01 KST

## 결론

권장안은 고정 contiguous prefix를 P019 dual-partition으로 두 번 전수 계산하고, 관측 recurrence를
읽지 않는 margin-only 정보량 gate를 별도로 적용하는 것이다. P0는 성능 진단, A만 탐색형 prefix
gate다. P0/A 모두 hypothesis test가 아니다.

## 변경 영향

| 축 | 판정 | 근거 |
|---|---|---|
| iterated log·end-bounded G/H | 영향 없음 | recurrence 보조 연구이며 `source/definitions.py` 미변경 |
| dataset provenance | 영향 있음 | 기존 pinned records만 사용, 새 prime list 저장 금지 |
| 완전성 | 영향 있음 | `pi(U-1)-pi(L-1)` dual-primecount와 두 병렬 pass 필요 |
| 큰 정수·정밀도 | 영향 있음 | endpoint와 count는 Python int/10진 문자열, float는 planning 기대·분산만 |
| 통계 | 영향 있음 | A/B gate 사전동결, 관측 C·p/q/z 접근 금지 |
| 승인 | 영향 있음 | 구현·toy와 actual 사용자 실행을 분리 |
| 재현성 | 영향 있음 | contract/input/code/artifact SHA-256, saved margin 재계산 |
| 정리 주장 | 영향 없음 | 정보량 측정이며 theorem/enrichment claim 금지 |

## 대안 비교

| 접근 | 정확성 | 비용 | 위험 | 판정 |
|---|---|---:|---|---|
| serial+parallel full prefix | 독립 execution shape가 가장 강함 | A가 대략 20시간 이상 가능 | serial 저활용·wall time 과다 | calibration용 외에는 비권장 |
| 서로소 dual-parallel contiguous prefix | exact count·경계·두 분할 검증 | P0 30–60분, A 7–10시간 | shared kernel common-mode | **권장** |
| record 주변 짧은 창만 표본추출 | 빠름 | 수분 | population/plateau 선택편향, 기존 gate와 비동등 | 기각 |

## endpoint 선택의 영향

A gate는 양의 분산 row 최소 2개를 요구한다. `[10^12,1.5e12)` 같은 1시간 안팎 prefix에는
완결 plateau가 record 51 하나뿐이므로 구조적으로 A를 통과할 수 없다. record 52까지 완결하려면
동결된 strict selection rule `next_start<U`에서 record 53 start를 포함해 upper exclusive를
`1,968,188,556,462`로 둔다. 이 선택은 마지막 next-record gap-start 한 개를 population/control에
포함하지만 선택 plateau exposure와 conditioned gap count에는 포함하지 않는다. 이에 따라
기존 10–60분 추정은 P0 전용으로 교정하고 A는 7–10시간으로 계획한다.

## blinding과 결과 사용

gate는 population, conditioned gap count, exposure만 읽는다. `exposure_equal_counts`를 바꾸어도
blinded component와 gate report가 byte-equivalent해야 한다. A PASS도 full 실행 지시가 아니라
`REVIEW_BALANCED_B_DESIGN`만 반환한다. 사용자의 별도 승인 없이는 B reference나 P013-C를 실행하지
않는다.

저장 산출물은 관측 recurrence에 의존하는 full-statistics digest도 제외한다. 대신 raw blinded
margin을 저장하고 saved verifier가 margin→components→gate를 다시 생성한다. primecount 두
알고리즘의 원시 출력과 hash도 최종 run에 복사한다.

운영 안전장치는 Windows process tree 31.5 GB Job Object ceiling, 시작 시 5 GB free-disk gate,
P0/A named mutex, WSL 30,000,000 KiB virtual-memory ceiling과 topology-aware 4 physical/8 logical
CPU affinity다. deadline 도달 시 queued segment를 취소하고 실행 중 segment를 안전하게 회수하므로
프로세스 종료가 최대 한 segment만큼 늦어질 수 있으며 partial은 PASS가 아니다.
