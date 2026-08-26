# P010A — residue-state count upper-bound 연구

## 1. 상태

`PLAN_FROZEN / LOCAL_TEST_PASS / MOD2310_REPLAY_RUNNER_READY / USER_RUN_PENDING / MOD30030_SOLVE_NOT_AUTHORIZED`

P010A는 `gap >= 1856`인 consecutive-prime gap의 **개수 상한**을 더 낮추는 축이다.
P007의 modulus-2310 exact certificate를 memory-safe oracle로 먼저 완전 replay한 뒤,
modulus 30030 cutting-plane이 실제로 필요하고 안전한지 판단한다.

더 낮은 count upper bound는 위치 목록이나 prime search 가속을 자동으로 주지 않는다.
그 연결은 P010B의 별도 책임이다.

## 2. 입력·provenance

- certificate: `test_result/run_20260824T090010Z_p007_full/certificate_mod2310.txt`
- SHA-256: `725a2dcd4fd04b870a7f42edb85e6d9c029290fba861c592348a54d370c88ae5`
- modulus: 2310
- threshold: 1856 (`>=1856`을 위험 gap으로 포함)
- states: 480
- expected transition constraints: 415,223
- P007 exact total upper bound: `439,161,464,927,854,179`
- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- CPU only, RAM 32 GB 미만, disk 100 GB 미만

## 3. G2 modulus-2310 replay

한 실행에서 다음 독립 경로를 대조한다.

1. pairwise exact edge builder
2. offset exact edge builder
3. floating chunk separation oracle의 전 제약 scan
4. 저장 후 exact 재계산과 hash 검증

floating scan은 위반 발견용일 뿐 exact certificate 판정은 두 integer verifier가 한다.

### 성공 기준

- pinned certificate hash 일치
- 두 exact builder의 constraint count·minimum integer slack·상한 일치
- exact constraint count 415,223
- minimum integer slack 0 이상
- chunk scan count 415,223, violation count 0
- saved-artifact verification issue 0, `exact_recomputed=true`
- `saved_verification_report.json`의 manifest SHA-256 binding 일치
- terminal `[PASS] P010A modulus-2310 replay completed.`

### 중단 기준

- hash 또는 modulus 불일치
- exact builder 불일치
- floating violation 1개 이상
- 결과 폴더 덮어쓰기 시도
- RAM 4 GB 또는 30분 초과

## 4. 실행 절차

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p010a\run_p010a_mod2310_replay.ps1 -ConfirmP010A
```

예상시간: 1–5분. 예상 RAM: 1 GB 미만. 예상 disk: 100 MB 미만.

사용자 회신:

- 마지막 `[PASS]` 또는 첫 `[FAIL]` 줄
- `test_result/logs/run_<UTC>_p010a_mod2310_replay.log`
- `test_result/run_<UTC>_p010a_mod2310_replay/manifest.json`

## 5. G3 이후 조건부 연구

replay PASS 뒤에도 곧바로 modulus-30030 LP를 풀지 않는다. 먼저 P010B one-candidate
scan으로 35,224,647개 transition의 실제 시간·메모리를 측정한다. 그 뒤에만 다음을
검토한다.

1. 위반 제약만 추가하는 cutting-plane prototype
2. 종료 candidate의 모든 transition exact integer streaming verification
3. 새 upper bound가 P007보다 strict하게 작은지 비교
4. 168시간·32 GB 중단조건

modulus가 커졌다는 사실만으로 상한 개선을 보장하지 않는다.
