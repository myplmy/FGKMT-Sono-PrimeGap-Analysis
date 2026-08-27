# P010A — residue-state count upper-bound 연구

## 1. 상태

`MOD2310_REPLAY_PASS / MOD30030_EXACT_LIFT_PASS / G4_STRICT_BOUND_IMPROVEMENT_PASS / SEARCH_ACCELERATION_NOT_PROVED`

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
- CPU only, RAM 32 GB 미만
- P010A/P010B 연속 실행 전체 disk 증가량 50 GB(50,000,000,000 bytes) 이하

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

## 5. G2 실제 결과 (`EXPERIMENT_PASS`)

- run: `test_result/run_20260826T100715Z_p010a_mod2310_replay`
- log: `test_result/logs/run_20260826T100715Z_p010a_mod2310_replay.log`
- pairwise/offset exact constraints: 각각 415,223
- minimum integer slack: 0
- floating minimum slack: `-2.220446049250313e-16`; tolerance 내 반올림 오차이며 exact 위반 0
- total upper bound: `439,161,464,927,854,179`로 P007과 동일
- saved exact recomputation: issue 0

이 결과는 verifier와 memory-safe oracle의 동등성을 확인했다. 상한을 낮춘 결과나
search acceleration 결과는 아니다.

## 6. G3 이후 조건부 연구

replay PASS 뒤에도 곧바로 modulus-30030 LP를 풀지 않는다. 먼저 P010B one-candidate
scan으로 35,224,647개 transition의 실제 시간·메모리를 측정한다.

scan 위반이 0이면 modulus-2310 certificate를 residue reduction으로 exact lift하고,
35,224,647개 제약을 정수 streaming으로 두 번 검사한다. 이 lift는 **같은 상한을
modulus 30030에서도 재현하는 feasibility baseline**이며 strict improvement가 아니다.

그 뒤에만 다음을 검토한다.

1. 위반 제약만 추가하는 cutting-plane prototype
2. 종료 candidate의 모든 transition exact integer streaming verification
3. 새 upper bound가 P007보다 strict하게 작은지 비교
4. 16시간·32 GB RAM·50 GB disk 중단조건

modulus가 커졌다는 사실만으로 상한 개선을 보장하지 않는다.

### exact-lift 단독 실행 절차

P010B PASS 결과의 manifest를 `<P010B_MANIFEST>`에 넣는다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p010a\run_p010a_mod30030_exact_lift.ps1 -ConfirmP010AExactLift -P010AReplayManifest '.\test_result\run_20260826T100715Z_p010a_mod2310_replay\manifest.json' -P010BScanManifest '<P010B_MANIFEST>'
```

예상시간 2–30분, RAM 1 GiB 미만, disk 1 GiB 미만이다. P010B의 floating violation이
0이 아니면 이 단계는 실행하지 않는다.

### G3 실제 결과

- P010B scan: `test_result/run_20260826T144440Z_p010b_mod30030_candidate_scan`
- exact lift: `test_result/run_20260826T144450Z_p010a_mod30030_exact_lift`
- 35,224,647 constraints floating/exact scan 모두 위반 0
- exact minimum integer slack 0
- total upper bound `439161464927854179`, strict improvement false
- 핵심 exact scan elapsed 0.7684초

완료 runner는 `test_done/`으로 이관했으므로 위 단독 실행 절차는 provenance로만 남기고
재실행하지 않는다. 다음 실제 질문은 working-set cutting-plane이 strict improvement를
만드는지 여부다.

G4의 11시간 자원·정확성·실행 절차 정본은
`test_plan/P010A_G4_mod30030_cutting_plane_11h.md`다.

## 7. G4 actual 결과

사용자 실행 `20260826T155918Z`은 4회 working-set LP와 전체 streaming scan 뒤
`FULL_FLOATING_CONVERGENCE`로 종료했다. exact integer verifier는 35,224,647 constraints,
minimum slack 0, violation 0을 재확인했다.

\[
N_{\ge1856}(10^{20},10^{21})
\le436001550591586306.
\]

기존 상한보다 `3159914336267873`, 약 0.7195336% 낮다. 이는 P010A count 연구의 성공이지만
절대 후보 위치와 P005/P010B search acceleration은 제공하지 않는다. 같은 modulus-30030
floating LP는 full scan 위반 0으로 수렴했으므로 장시간 반복하지 않는다.
