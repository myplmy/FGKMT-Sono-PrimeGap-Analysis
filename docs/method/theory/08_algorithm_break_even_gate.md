# 알고리즘 승격을 위한 break-even·자원 gate

## 지위

`DEFINITION + EXACT_ARITHMETIC GATE`

## 사용자 자원 제한

- CPU-only
- 한 run RAM 32 GB 미만, 구현 hard cap은 가능하면 28–30 GiB
- disk 100 GB 미만
- 연속 runtime 168시간 미만

P010A/P010B 조건부 연구는 사용자의 더 엄격한 별도 지시에 따라 disk를 십진 50 GB,
즉 `50,000,000,000` bytes 이하로 제한한다. 50 GiB로 완화하지 않는다.

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

## P010B machine-checkable gate

`source/candidate_cover.py`는 작은 direct universe에서 math·finite-verifier gate를 구현한다.
누락 없는 candidate/rejection partition, exact factor, strict window-prime, equality threshold를
검사한다. break-even은 같은 CPU·범위·threshold·code hash, 최소 5회 median, false negative 0,
50 GB 이하, 생성+검증+survivor 총시간의 최소 5% 개선을 요구한다.

조건을 만족해도 `ACCELERATION_CANDIDATE`일 뿐 독립 반복 전에는 proof로 표시하지 않는다.
현재 toy는 exhaustive oracle을 사용하고 speedup도 1 미만이어서 BLOCKED다. large-range
compressed coverage와 PARI witness가 생기기 전에는 actual gate를 열지 않는다.
