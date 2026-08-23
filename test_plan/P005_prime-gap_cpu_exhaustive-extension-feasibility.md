# P005 — `prime-gap` CPU 탐색과 exhaustive 범위 확장 타당성

## 1. 상태

`PREPARATION_ONLY` — CPU-only calibration 실행기는 준비하지만, Rank 85→86 전체 exhaustive 실행은 coverage 방법과 계산 가능성이 성립하지 않아 승인 가능한 실행 단계가 아니다. BAT 실행 자체도 사용자가 `--confirm-cpu`를 명시해야 한다.

## 2. 연구 질문과 비목적

연구 질문:

1. 고정한 `sethtroisi/prime-gap`이 Ryzen 7 9700X/WSL2에서 CPU-only로 재현 가능하게 빌드·검증되는가?
2. 공식 Method1/Method2 출력이 일치하고 작은 primorial-centered 탐색이 정상 작동하는가?
3. 이 도구가 gap 1854 이후 일반 x-범위의 exhaustive coverage에 직접 사용될 수 있는가?
4. 사용할 수 없다면 어떤 추가 coverage 알고리즘과 인증 산출물이 필요한가?

비목적:

- GPU를 빌드·실행·비교하지 않는다.
- `gap_stats` 상위 후보만 검사한 결과를 exhaustive라고 부르지 않는다.
- calibration 처리량을 Rank 85→86 전체 완료시간으로 단순 외삽하지 않는다.
- P003의 검증 상한이 Rank 85까지 포함한다고 주장하지 않는다.
- 사용자 승인 없이 패키지를 설치하거나 장시간 탐색을 시작하지 않는다.

## 3. 수학 정의와 coverage 계약

본 프로젝트의 canonical 함수는

\[
G_{\mathrm{end}}(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

이다. gap의 first occurrence를 찾는 계산에서는 gap start `p_n`을 검색 key로 쓰지만, 발견한 record를 `G_end`에 반영하는 jump는 end prime `p_(n+1)`이다.

Rank 85 이후 first-occurrence 확장을 위해 필요한 명제는 다음과 같다.

\[
\forall p\in[X_0,X_1)\cap\mathbb P,
\quad p_{next}-p>1854
\Rightarrow p\text{가 검사 후보에 포함된다.}
\]

여기서

```text
X0 = 101412319996363309069
X1 = 39422251630462640179641871
```

이다. false positive는 후속 소수성·합성수 인증으로 제거할 수 있지만 false negative는 허용하지 않는다.

## 4. Dataset와 provenance

### Prime-gap record 원천

- repository: https://github.com/primegap-list-project/prime-gap-list
- pinned commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- `allgaps.sql` SHA-256: `988c3278d95a16460a9897e09829fb061ee854e55efa6c4fcec3b9779930894f`
- exhaustive coverage registry limit: `10^20`
- Rank 85, gap 1854: `ismax=1`, `isfirst=F`, `gapcert=C`
- Rank 86 candidate row, gap 1858: `ismax=0`, `isfirst=?`, `gapcert=C`

Rank 86 row는 gap 1858 자체가 인증됐음을 뜻하지만 first occurrence/maximal 여부는 확정하지 않는다.

### Search code 원천

- repository: https://github.com/sethtroisi/prime-gap
- pinned commit: `8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d`
- suite role: `m * P#/d` 주변 후보 탐색
- non-role: 임의의 `[X0,X1)` 전 구간 segmented-sieve 인증

## 5. 환경과 고정 자원

- host CPU: AMD Ryzen 7 9700X, 8 cores/16 logical processors
- runtime: WSL2 Ubuntu 24.04
- threads: 8
- upstream memory flag: `--max-mem 28` GiB
- shell hard limit: `ulimit -v 31457280` KiB = 30 GiB
- GPU: 금지; `gap_test_gpu`/CUDA/CGBN target을 빌드하지 않음
- output: `tmp/prime-gap-p005/<run-id>/`와 `test_result/logs/`의 새 run-id 경로

필수 WSL 패키지:

```bash
sudo apt update
sudo apt install -y build-essential git make sqlite3 libgmp-dev libsqlite3-dev libprimesieve-dev time
```

실행기는 의존성을 자동 설치하지 않는다.

## 6. 단계별 사전검증 및 중단 조건

### G0 — 정적 타당성 (`PASS`)

- upstream HEAD와 빌드 의존성 확인
- `combined_sieve`의 대상이 primorial-centered interval임을 확인
- 1–16 OpenMP threads와 `--max-mem` GiB 단위를 원 코드에서 확인
- Rank 85/86 classification과 P003 상한을 원천 row에서 확인
- 전체 범위 규모의 낙관적 시간 하한 계산

### G1 — 의존성 검사 (`WAITING_FOR_USER`)

- WSL distribution이 Ubuntu인지 확인
- `git`, `g++`, `make`, `sqlite3`, `md5sum`, `/usr/bin/time` 확인
- `libgmp-dev`, `libsqlite3-dev`, `libprimesieve-dev` 확인
- 하나라도 없으면 설치하지 않고 중단

### G2 — 공식 correctness calibration (`WAITING_FOR_USER`)

- exact upstream commit을 새 디렉터리에 clone/checkout
- `combined_sieve`, `gap_stats`, `gap_test_simple`만 CPU로 빌드
- upstream 공식 `P=907,D=2190,minc=200` quick test 실행
- Method1/Method2 unknown file MD5가 각각 upstream 기대값 `15a5cbff7301262caf047028c05f0525`와 일치해야 함
- stats와 simple gap test가 성공해야 함

### G3 — 소규모 CPU 탐색 calibration (`WAITING_FOR_USER`)

- 같은 파라미터에서 `minc=2000`, `10000`을 Method2로 실행
- 각 규모에 대해 wall time, maximum resident set, exit code, output hash 저장
- 메모리 제한 초과, output 충돌, hash/check 실패 시 즉시 중단

### G4 — 일반 x-range coverage 설계 (`BLOCKED_BY_FEASIBILITY`)

다음이 모두 제시되기 전에는 target exhaustive 실행기를 만들지 않는다.

1. `[X0,X1)`의 every-prime-start coverage를 보장하는 분할 규칙
2. block별 누락·중복을 기계 검증할 coverage ledger
3. 경계 prime pair를 잃지 않는 overlap 규칙
4. 각 survivor의 endpoint primality와 interior compositeness certificate
5. 독립 구현으로 일부 block을 재검산하는 계획
6. benchmark로 산출한 현실적 총 CPU core-year와 저장공간

## 7. 승인 후 실행 명령

의존성 설치 후 저장소 루트의 Windows 터미널에서:

```bat
run_P005_prime_gap_cpu_calibration.bat --confirm-cpu
```

이 명령은 작은 탐색/calibration만 수행한다. Rank 85→86 전체 exhaustive 실행 명령이 아니다.

## 8. 산출물

- `test_result/logs/run_<UTC>_p005_prime_gap_cpu_calibration.log`
- `tmp/prime-gap-p005/<UTC>/source/` pinned source/build
- `tmp/prime-gap-p005/<UTC>/metrics.txt`
- Method1/Method2 및 추가 minc별 unknown files
- 각 minc의 `gap_stats`와 `gap_test_simple` 출력
- source commit, CPU/thread/memory limit, command가 적힌 manifest

`tmp/` 결과는 대형·재생성 가능 산출물이므로 git에 커밋하지 않는다. 실행 로그도 기존 정책대로 ignore한다.

## 9. 판정 기준과 해석 제한

- G2 hash 일치와 모든 exit code 0이어야 `CALIBRATION_PASS`이다.
- G3 성공은 이 PC에서 도구가 작동한다는 뜻이지 목표 범위 exhaustive 가능성을 뜻하지 않는다.
- `gap_stats` probability는 작업 순서 휴리스틱이며 coverage certificate가 아니다.
- 범위 길이는 `39,422,150,218,142,643,816,332,802`; 초당 `10^12` 정수라는 비현실적 가정에서도 약 125만 년이다.
- 따라서 현재 단일 CPU full exhaustive 예상시간은 “완료 불가능”으로 판정하며 시간·일 단위 ETA를 제공하지 않는다.

## 10. 후속 작업

1. 사용자 의존성 설치 및 G2/G3 BAT 실행
2. calibration 로그의 실제 처리량·메모리 분석
3. 탐색 목적이면 primorial-centered 후보 탐색 계획을 별도 수립
4. exhaustive 목적이면 분산 segmented-sieve와 coverage certificate를 별도 프로젝트로 설계
5. Rank 85 pointwise `F,H` 계산은 exhaustive 확장과 분리하여 필요 시 별도 승인 실행

