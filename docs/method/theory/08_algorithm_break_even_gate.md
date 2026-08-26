# 알고리즘 승격을 위한 break-even·자원 gate

## 지위

`DEFINITION + EXACT_ARITHMETIC GATE`

## 사용자 자원 제한

- CPU-only
- 한 run RAM 32 GB 미만, 구현 hard cap은 가능하면 28–30 GiB
- disk 100 GB 미만
- 연속 runtime 168시간 미만

## 전체 폭 모델

`W=9 x 10^20`, block length `L`, blocks `n=ceil(W/L)`, block당 시간 `t`, bytes `b`이면

\[
nt\le604800\text{ seconds},\qquad nb<10^{11}\text{ bytes}
\]

가 최소 조건이다. 이론층의 비용까지 포함해

\[
T_{hybrid}=T_{base}+T_{extra}-T_{saved}
\]

이고 실제 승격에는 `T_saved>T_extra`가 필요하다.

## P008에서 계산된 문턱

- 비현실적으로 빠른 `1 microsecond/block`이어도 `L>=1.488 x 10^9`
- 현재 local bound 비율을 적용하면 이 길이의 internal `q`가 약 723,420
- 1 byte/block disk gate: `L>=9 x 10^9`, 현재 q 약 4.38 million
- 100 bytes/block disk gate: `L>=9 x 10^11`, 현재 q 약 437.5 million

따라서 소수점 정밀도를 높이는 문제가 아니라 bound 차수를 크게 줄이거나 very sparse
candidate cover를 만들어야 한다.

## 승격 단계

1. **Math gate:** soundness와 100% coverage
2. **Finite verifier gate:** exact arithmetic, issue 0, non-overwrite hash
3. **Resource gate:** peak RAM/disk/runtime hard cap
4. **Benefit gate:** 동일 coverage baseline보다 total CPU work 감소
5. **Reproducibility gate:** 독립 source/implementation 또는 명시된 한계

하나라도 실패하면 “흥미로운 finite result”로는 남길 수 있지만 “탐색 알고리즘
개선”으로 승격하지 않는다.
