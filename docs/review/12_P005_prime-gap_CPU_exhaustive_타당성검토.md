# P005 — Rank 85 이후 exhaustive 확장과 `prime-gap` CPU 활용 타당성 검토

## 결론

검토용 문서의 문제 제기, 즉 gap 1854 이후 다음 더 큰 gap의 **최초 시작점**을 확정하려면 중간 범위를 누락 없이 검사해야 한다는 원칙은 타당하다. 그러나 `sethtroisi/prime-gap`을 그대로 사용하여

```text
[101412319996363309069, 39422251630462640179641871)
```

를 개인용 CPU 한 대에서 exhaustive하게 인증할 수 있다는 전제는 타당하지 않다.

`prime-gap`은 임의의 연속 정수 범위를 분할하여 모두 검사하는 segmented-sieve 프로그램이 아니다. 원 저장소가 설명하는 대상은 `m * P#/d` 주변의 많은 후보 구간이며, `gap_stats`는 그 후보의 검사 우선순위를 휴리스틱하게 정한다. 따라서 이 도구는 대형 gap **탐색**에는 유용하지만, 위의 일반 구간 전체를 덮었다는 증명은 별도의 coverage map과 누락 불가능성 증명이 없으면 제공하지 못한다.

## 확인된 원천 상태

- `prime-gap-list` pin: `1a112a1387052d9ad360686313f501c01fe46b68`
- `allgaps.sql` SHA-256: `988c3278d95a16460a9897e09829fb061ee854e55efa6c4fcec3b9779930894f`
- gap 1854 row: `ismax=1`, `primecat=C`, `isfirst=F`, `gapcert=C`, start `101412319996363309069`
- gap 1858 row: `ismax=0`, `primecat=C`, `isfirst=?`, `gapcert=C`, start `39422251630462640179641871`

따라서 1858의 양 끝 소수와 내부 합성수열은 인증되었지만, 이 위치가 gap 1858의 진짜 첫 발생인지와 그 전에 1854보다 큰 gap이 없는지는 현재 row만으로 확정되지 않는다.

또한 Rank 85의 start prime은 `10^20`보다 크다. P003의 검증된 `[3814280,10^20]` 분석에는 Rank 84(gap 1724)까지만 들어간다. Rank 85에서 `F`와 pointwise `H`를 계산하는 것은 가능하지만, 이를 P003의 exhaustive 범위 안에서 계산했다고 표현하면 안 된다.

## 범위 규모와 시간 하한

목표 범위의 정수 길이는

```text
39,422,150,218,142,643,816,332,802
```

이고 양 끝 크기의 비는 약 `388,732.37`이다.

실제 알고리즘 처리량과 무관한 극단적으로 낙관적인 하한도 다음과 같다.

| 가정 | 단순 선형 하한 |
|---|---:|
| 초당 `10^12`개 정수 처리 | 약 1,249,213년 |
| 초당 `10^9`개 정수 처리 | 약 1,249,212,558년 |
| 폭 1854마다 최소 한 coverage window, 초당 `10^9` window | 약 673,793년 |

마지막 행도 실제 인증 비용보다 훨씬 낙관적이다. 각 window에서 양 끝 소수와 내부 합성수를 인증하고 경계가 겹치지 않게 관리해야 하기 때문이다. Ryzen 7 9700X 한 대의 실제 완료시간을 시간·일·개월 단위로 제시하는 것은 정직하지 않으며, 현실적인 판정은 **단일 워크스테이션으로 완료 불가능**이다.

## 검토용 문서의 항목별 판정

### 수용

- `gap > 1854`인 모든 실제 gap이 후보 집합에 남아야 한다는 false-negative 금지 invariant
- 1858만 찾는 것으로 exhaustive proof를 대체하지 않는 원칙
- 휴리스틱은 우선순위에만 사용하고 coverage 생략에 사용하지 않는 원칙
- 작은 reference 범위에서 독립 segmented sieve와 일치시킨 뒤 확장하는 단계
- 블록별 provenance, checkpoint, 재시작, 중복·누락 검사
- GPU 경로를 사용하지 않고 CPU 결과를 별도로 검증하는 설계

### 수정

- 문서의 `G(x)=max_{p_n<=x}g_n`는 start-bounded 함수이다. Sono-compatible 본 분석의 canonical 함수는 `max_{p_(n+1)<=x}g_n`이므로 두 정의를 별도 표기해야 한다.
- gap 1858은 “gap 자체가 미확인”이 아니라 `C?C`: gap은 인증됐지만 first occurrence가 미확인이다.
- Rank 85를 “현재 P003가 계산한 H 범위”라고 부르면 안 된다. P003 상한은 `10^20`, Rank 85 start는 그보다 크다.
- `gap_stats`의 probability ranking이나 상위 일부 PRP 검사는 exhaustive 단계가 아니다.
- `prime-gap`의 `m * P#/d` 후보 공간을 임의 x-구간 coverage로 바꾸려면 각 실제 gap이 적어도 하나의 검사 interval에 들어간다는 별도 정리와 기계검증 가능한 coverage ledger가 필요하다.

### 기각 또는 보류

- Rank 85→86 전체를 현재 `prime-gap` 명령 하나로 exhaustive하게 실행
- GPU 가속 또는 GPU 결과 의존
- benchmark 몇 점을 전체 범위에 단순 외삽하여 현실적인 완료시간으로 제시
- 휴리스틱 확률이 낮은 블록을 생략
- 32GB RAM 상한 안에서 끝난다는 이유만으로 계산 가능하다고 판정

## `prime-gap`에서 이미 구현된 최적화와 새 구현 필요성

원 도구에는 combined sieve Method2, OpenMP 1–16 threads, primorial/D 구성, one-side skip, probability ranking, RLE/bit compression, Method1/Method2 교차검증, `--max-mem` OOM 방지 검사가 이미 있다. 이를 다시 Python으로 구현하는 것은 성능과 검증 모두에 불리하다.

따라서 현 단계에서 별도 residue-mask/GPU/새 sieve를 작성하지 않는다. 먼저 고정 commit의 공식 quick test, 1/2/4/8-thread hash 일치, 작은 CPU calibration으로 원 도구가 이 PC에서 정확히 빌드되고 재현되는지 측정한다. 이후에도 다음 둘은 분리한다.

1. `prime-gap`을 이용한 primorial-centered **탐색**
2. 일반 x-범위의 누락 없는 **exhaustive 인증**

두 번째 목적에는 분산 segmented sieve, coverage certificate, 독립 재검산 체계가 별도로 필요하다.

## 권장 환경

Windows native 빌드는 현재 GMP/SQLite/primesieve/OpenMP 도구체인이 갖춰져 있지 않다. WSL2 Ubuntu 24.04에는 `git`, `g++`, `make`가 있고 30 GiB RAM만 노출되어 있으므로 WSL이 더 단순하고 사용자 RAM 제한에도 맞는다.

필요한 설치 명령은 다음과 같으며 사용자는 설치 완료를 보고했다. 실제 설치 상태는 실행기 G1이 다시 확인하고 누락 시 설치하지 않은 채 중단한다.

```bash
sudo apt update
sudo apt install -y build-essential git make sqlite3 libgmp-dev libsqlite3-dev libprimesieve-dev time
```

준비한 WSL-native shell 실행기는 GPU target을 빌드하지 않고 최대 8 threads, upstream `--max-mem 28`, OS-level virtual-memory limit 30 GiB를 함께 적용한다. 의존성이 없으면 설치하지 않고 즉시 중단하여 위 명령을 출력한다. 실행은 WSL에서 다음과 같이 한다.

```bash
cd /mnt/z/FGKMT-Sono-PrimeGap-Analysis
bash ./run_P005_prime_gap_cpu_calibration.sh --confirm-cpu
```

P005b의 arbitrary x-range calibration 제안은 `docs/review/14_P005b_exhaustive-extension-calibration_타당성검토.md`에서 별도로 검토했다. 좌표계 불일치 때문에 독립 실험으로 만들지 않았고 유효한 측정 항목만 P005에 흡수했다.

## 참고 원천

- Seth Troisi, `prime-gap`: https://github.com/sethtroisi/prime-gap
- Prime Gap List Project, high-watermarks: https://primegap-list-project.github.io/lists/prime-gaps-high-watermarks/
- Prime Gap List Project, fully analyzed coverage: https://primegap-list-project.github.io/fully-analyzed/

