# Residue-state finite count certificate

## 지위

`THEOREM + EXACT_FINITE + OPEN`

## 무엇을 증명하는가

P007 certificate는 start prime이 `[A,B)`에 있고 gap이 `H` 이상인 사건 수

\[
N_{>=H}(A,B)=\#\{p\in[A,B):p^+-p\ge H\}
\]

의 무조건적 upper bound를 준다. LP는 candidate를 발견할 뿐이며, 최종 판정은
고정 denominator 정수와 `Fraction` arithmetic으로 모든 transition inequality를
검증한다.

## 확인된 결과

`A=10^20`, `B=10^21`, `H=1856`에서:

| modulus | states | constraints | 저장 total upper bound |
|---:|---:|---:|---:|
| 30 | 8 | 128 | 447,557,793,758,307,014 |
| 210 | 48 | 4,608 | 442,672,596,769,194,837 |
| 2310 | 480 | 415,223 | 439,161,464,927,854,179 |

minimum integer slack는 모두 0이다. 기존 저장값은 conservative `ceil+crossing`이며
정수 `floor`를 쓰면 각 total bound를 1 낮출 수 있다. 기존 값도 참인 상한이므로
산출물은 유효하다.

## 무엇을 증명하지 않는가

- 실제 large gap이 어느 위치에 있는지
- Rank 85→86 사이를 exhaustive하게 덮었는지
- `prime-gap` 작업단위와 연속 x-range의 coverage mapping
- upper bound를 낮춘 만큼 실행시간이 줄어드는지

전역 `N<=U`만으로는 위치 목록이 생기지 않는다. 따라서 `C_max` 개선은 algorithm
acceleration의 필요조건 후보일 수 있지만 충분조건이 아니다.

## modulus 30030

states 5,760, transition constraints 35,224,647로 기존 monolithic LP는 위험하다.
P010은 chunked separation oracle을 구현했으며 64-row chunk의 보수적 working estimate는
약 34.24 MiB다. 아직 30030 scan·LP solve·certificate 생성은 하지 않았다.

## 승격 조건

1. memory-safe discovery
2. 모든 transition의 streaming exact verification
3. 더 작은 upper bound
4. local zero 또는 누락 없는 candidate cover로 위치 연결
5. 동일 coverage baseline보다 총비용 감소

1–3만 성공하면 더 좋은 count theorem이지 탐색 가속기는 아니다.
