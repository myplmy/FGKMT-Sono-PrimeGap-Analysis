# P005 WSL bounded calibration 실행 분석 — 실패

## 한눈에 보는 결과

이번 실행은 `prime-gap` 소스 다운로드와 CPU-only 빌드까지 성공했지만, 첫 공식 Method1 calibration에서 필요한 SQLite 데이터베이스가 없어 종료됐다. 따라서 **P005 calibration 성공이 아니며**, 처리속도·thread scaling·Rank 85 이후 탐색시간을 판단할 수 없다.

```text
run id: 20260823T162845Z_p005_prime_gap_cpu_calibration
overall verdict: FAIL / INCOMPLETE
G1 dependency check: PASS
G2 build: PASS
G2 official Method1: FAIL (exit 1)
G2 Method2 and hashes: NOT RUN
G3 scaling/additional minc: NOT RUN
GPU: not used
target exhaustive search: not run
```

## 사용자가 가리킨 파일은 로그가 아님

사용자가 알려준

```text
tmp/prime-gap-p005/20260823T162845Z_p005_prime_gap_cpu_calibration/
source/unknowns/907_2190_1_200_s11000_l100M.m1.txt
```

는 실행 로그가 아니라 Method1이 만들다 중단된 **후보 unknown 중간파일**이다. 실제 stdout/stderr 로그는 다음이다.

```text
test_result/logs/run_20260823T162845Z_p005_prime_gap_cpu_calibration.log
```

## 실제로 성공한 부분

- WSL이 16 logical CPUs를 인식했다.
- upstream commit `8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d`를 checkout했다.
- `combined_sieve`, `gap_stats`, `gap_test_simple` CPU targets를 정상 빌드했다.
- 빌드 exit code는 0, wall time은 3.28초, peak RSS는 210,264 KiB였다.
- 로그상 GPU target은 빌드·실행하지 않았다.
- 30 GiB virtual-memory hard limit와 upstream `--max-mem 28` 설정이 기록됐다.

## 실패 원인

로그의 마지막 핵심 문장은 다음이다.

```text
'prime-gap-search.db' doesn't exist
```

upstream README는 실행 전 다음 초기화를 요구한다.

```bash
sqlite3 prime-gap-search.db < schema.sql
```

현재 `scripts/run_prime_gap_cpu_calibration.sh`는 clone/build 후 `unknowns` 폴더만 만들고 이 DB 초기화를 하지 않는다. `combined_sieve`가 unknown 파일을 쓰기 시작한 뒤 DB에 range 정보를 기록하려다 exit 1로 끝났다. shell의 `set -Eeuo pipefail` 때문에 그 자리에서 전체 실행도 중단됐다.

## 부분 unknown 파일은 사용 금지

중단된 파일의 실제 hash:

```text
MD5    7daa0dc3c3b908e3ca23d83ade76214c
SHA256 3682939487b616237c7ffa5110a191351e9551cd9d0f2ad301e866edeb134b63
```

공식 기대 MD5는 다음이다.

```text
15a5cbff7301262caf047028c05f0525
```

일치하지 않으므로 이 파일로 `gap_stats`, PRP test, 성능평가를 하면 안 된다. 기존 실패 run은 provenance 증거로 그대로 두고, 수정 후에는 새 run ID를 사용해야 한다.

## `tmp` 저장 위치 판정

저장 위치는 의도된 설계와 일치한다.

- `test_result/logs/`: 사람이 읽는 전체 실행 로그
- `tmp/prime-gap-p005/<run-id>/`: clone/build tree, unknown 후보, metrics처럼 크고 재생성 가능한 작업 산출물

따라서 unknown 파일이 `tmp`에 있는 것은 오류가 아니다. 이 대형 파일들을 Git 관리 결과 폴더로 옮길 필요도 없다. 다만 실패 시에도 `FAILED` manifest를 남기는 trap을 후속 runner 개선으로 추가하면 상태 확인이 더 쉬워진다.

## 수정 가능성

수정은 작고 명확하다. 새 run의 pinned source directory에서 build 다음, Method1 전에 다음을 수행하고 DB schema/table 존재를 확인하면 된다.

```bash
sqlite3 prime-gap-search.db < schema.sql
sqlite3 prime-gap-search.db '.tables'
```

그 후 official Method1/Method2 MD5가 모두 기대값과 일치해야 다음 단계로 진행한다. 이번 요청에서는 원인만 확정했으며 P005 runner를 수정하거나 재실행하지 않았다. 수정·재실행에는 새 사용자 승인이 필요하다.

## 쉬운 설명

프로그램 본체는 잘 만들어졌지만, 작업 기록을 적어 둘 빈 장부(DB)를 먼저 만들지 않았다. 프로그램은 계산 결과 파일을 쓰기 시작한 뒤 장부를 찾지 못해 멈췄다. 그래서 지금 생긴 결과 파일은 완성품이 아니고, 속도 측정에도 쓸 수 없다.

