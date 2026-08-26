# P010Q — P009/P010 CPU-only 16시간·50 GB bounded queue

## 1. 상태

`COMPLETED / EXPERIMENT_PASS / THREE_CHILDREN_PASS`

이 문서는 새 수학 실험이 아니라 이미 분리된 세 실행을 안전하게 이어 주는 실행계획이다.
각 실험은 자기 PowerShell runner와 결과 폴더를 유지하고, queue는 순서·의존성·시간·disk
한도만 관리한다.

## 2. 고정 자원 한도

- CPU only, GPU 사용 금지
- 총 wall budget: 55,800초(15시간 30분); 사용자 16시간 창에 30분 여유
- `test_result/`와 `tmp/`의 queue 시작 이후 합산 증가량: 50 GB(50,000,000,000 bytes) 이하
- RAM: 각 child의 기존 4 GiB 중단 기준, 프로젝트 상한 32 GB
- full constraint matrix 저장 금지

queue는 child 실행 중 5초마다 `test_result/`+`tmp/` 증가량을 다시 합산하고, 측정 권한
오류도 fail-closed로 처리한다. 세 child 코드 자체도 transition matrix나 대규모 candidate
ledger를 쓰지 않고 작은 JSON/certificate만 저장하도록 구성했다.

## 3. 실행 순서와 조건

| 순서 | child 실험 | hard timeout | 조건 | 예상시간 |
|---:|---|---:|---|---:|
| 1 | P010B modulus-30030 one-candidate scan | 1시간 | P010A replay exact PASS | 1–15분 |
| 2 | P010A modulus-30030 exact lift | 4시간 | P010B floating violation 0 | 2–30분 |
| 3 | P009 single-block boundary actual | 1시간 | P010A replay·PARI adapter PASS | 2–20분 |

P010B가 실행 실패하면 P010A exact lift는 dependency-blocked지만 P009는 계속한다.
P010B가 정상 완료했으나 violation이 0보다 크면 exact lift는 과학적으로
`NOT_APPLICABLE`이며 queue 실패로 세지 않는다. 독립 child 실패가 있어도 다음 독립
child는 계속하고 마지막에 aggregate nonzero를 반환한다.

G4 cutting-plane은 넣지 않는다. G3 실측 없이 iteration 수·solver memory를 정하는 것은
16시간을 유익하게 쓴다는 근거가 부족하기 때문이다.

## 4. 성공·중단 기준

성공:

- 각 실행이 자기 terminal/saved verification 기준을 만족
- queue summary와 event JSONL hash 저장
- wall·disk cap 미초과
- 실행된 child 모두 PASS; 과학적 조건 불충족에 따른 `NOT_APPLICABLE`은 허용

중단:

- 15시간 30분 도달
- artifact 증가량 50 GB 초과
- P010A replay prerequisite hash/binding 불일치
- child timeout; 해당 process tree 종료 후 독립 child는 계속

## 5. 당시 사용자 실행 절차와 현재 재실행 금지

환경: **Windows FGKMT Conda Prompt 또는 Windows PowerShell**. WSL shell에서 실행하지
않는다. PARI/GP는 P009 child가 필요할 때 Windows에서 `wsl.exe`로 설치된 Ubuntu GP를
호출한다.

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\runners\run_p009_p010_bounded_queue.ps1 -ConfirmBoundedQueue
```

위 명령은 실행 당시 provenance다. 완료 runner는
`test_done/run_p009_p010_bounded_queue-20260826T144439Z-done.ps1`로 이관했고 다시 실행하지
않는다. 현재 사용자 수행절차는 별도 수행절차 필요없음이다.

예상 총시간은 보통 10분–1시간, 보수적 단계 timeout 합계는 6시간이다. queue hard cap은
15시간 30분이다. 완료 후 다음을 회신한다.

- 마지막 `[PASS]` 또는 첫 `[FAIL]`
- `test_result/logs/run_<UTC>_p009_p010_bounded_queue.log`
- queue result directory
- 생성된 각 child result directory

## 6. 실제 결과

- queue run: `test_result/run_20260826T144439Z_p009_p010_bounded_queue`
- queue log: `test_result/logs/run_20260826T144439Z_p009_p010_bounded_queue.log`
- elapsed: 25.906초
- artifact delta: 147,867 bytes
- P010B scan, P010A exact lift, P009 single-block actual: 모두 terminal PASS
- Codex 사후 독립 재검증: issue 0
- 해석: `test_result/202608270005_P009_P010_bounded_queue_result_analysis.md`

15시간 30분은 hard safety cap이었고 실제 예상 계산량을 의미하지 않았다. 세 child는
feasibility·certificate 단위였으므로 수십 초에 끝났다. 전체 prime search나 strict bound
improvement는 수행되지 않았다.
