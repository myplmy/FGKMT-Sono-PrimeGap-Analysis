# P017 P013 병렬 actual-calibration 구현·로컬검증 보고서

검증 시각: 2026-08-29 14:53 KST

## 판정

`APPROVED / IMPLEMENTED / LOCALLY_VERIFIED / USER_RUN_NOT_STARTED`

P013-A 전체범위와 P013-B 중간범위에 대해 8-process 병렬 결과가 serial 정본과 exact하게 같은지
검증할 runner를 구현했다. actual prime range는 실행하지 않았고 현재 진행 중인 P013-B process,
checkpoint, result directory를 읽거나 변경하지 않았다.

## 사용자 승인 해석

- P013-A 완료 결과와 동일성 확인은 전체 `[10^10,10^11)`에서 허용
- P013-B full 중복은 20시간 이상이므로 금지
- P013-B는 첫 primary half-decade `[10^11,316227766017)`만 허용
- 한 번의 combined queue는 16시간 이하
- 새로운 방식이 prime/gap·통계량·100,000회 inference를 생략하거나 근사하면 안 됨

이 조건을 그대로 구현했다. 별도 P013-C scientific experiment는 현재 LOW_INFORMATION과 P013-B
미완료 때문에 만들지 않았다.

## 구현한 검증

### P017-A

1. 8 worker·32 segment로 P013-A 전체범위 sufficient statistics 계산
2. 각 segment 오른쪽 crossing gap을 boundary prime으로 닫음
3. 인접 boundary prime과 worker 8개 실제 참여 확인
4. 완료된 serial checkpoint SHA-256
   `cd6a85ef2cb766bc04a9ddc3bf98a2fc8f12c5f19efbcaaa740318622edf4502`와 payload exact 비교
5. parallel checkpoint로 seed `20260828`, 100,000회 analysis를 재계산하고 완료 serial
   `analysis.json`과 exact 비교

즉 serial 전체 sieve를 다시 반복하지 않지만, 기존 serial full-range oracle 전체를 비교 기준으로
사용한다. prime/gap·plateau·component·inference 어느 단계도 생략하지 않는다.

### P017-B

1. 범위 `[100000000000,316227766017)`를 새 serial oracle로 계산
2. 같은 범위를 8 worker·64 segment로 계산
3. populations·gap counts·exposure·equal exposure 전체 exact 비교
4. complete record indices `41–45` 고정
5. plateau·component와 seed `20260829`, 100,000회 fixed-seed inference를 양쪽에서 계산해 exact 비교

이 중간범위는 engineering calibration이며 P013-B full scientific 결과로 사용하지 않는다.

## 자원·시간 gate

| 항목 | 설정 |
|---|---:|
| CPU | 물리 4코어·논리 8프로세스, affinity `0xff` |
| worker | 8 process |
| native thread | worker당 1 |
| P017-A timeout | 4시간 |
| P017-B timeout | 11시간 |
| child timeout 합 | 15시간 |
| queue global hard wall | 16시간 |
| 신규 artifact cap | decimal 5 GB |
| GPU | 사용 안 함 |

실제 예상은 A 약 0.5–1.5시간, B-mid 약 3–6시간, 합계 약 3.5–7.5시간이다. 이는 기존 serial
실측의 범위 크기 비례 외삽이므로 보장값이 아니며 queue hard wall이 최종 안전장치다.

## 진행상황 출력

Python이 각 완료 segment를 즉시 `progress.jsonl`에 append·flush한다. 표준 runner log는 기존
PowerShell capture 정책상 long stage가 끝난 뒤 병합되므로, 실행 중에는 runner가 시작 때 알려주는
별도 명령 `Get-Content <progress.jsonl> -Wait`로 실시간 상태를 볼 수 있다.

## 자동검증 증거

- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- `py_compile`: 새 source/test 8개 PASS
- P017/P016 targeted: 16/16 PASS, 10.166초
- 전체 unittest: 170/170 PASS, 26.900초
- A/B preflight: PASS; actual range read=false, P013-B artifact read=false
- PowerShell parser: 4/4 PASS
- BAT 승인 flag 없는 실행: 3/3 exit 1·usage 출력
- `git diff --check`: PASS

초기 runner 정적 감사에서 PowerShell의 `-Arguments @(…) + $CommonArguments`가 문법상 통과하지만
실제로 뒤쪽 공통 인수를 전달하지 않는 문제를 발견했다. actual 실행 전에 명명된
`$PreflightArguments`·`$RunArguments` 배열로 교정하고 전용 회귀시험을 추가했다. 교정 뒤 위의
16/16·170/170 최종 시험을 다시 통과했다.

combined queue에서도 진행상황을 즉시 볼 수 있도록 queue run directory의 고정
`live_console.log`에 Python이 child 출력을 append·flush한다. runner는 파일이 생길 때까지 기다린
뒤 `Get-Content -Wait`하는 복사 가능한 명령을 actual 시작 전에 출력한다.

sandbox 내부 첫 multiprocessing 시험은 Windows Pipe와 임시폴더 권한에서 `WinError 5`로
차단됐다. 같은 명령을 허가된 sandbox 외부 FGKMT 환경에서 재실행해 모두 PASS했으므로 구현
오류로 판정하지 않는다.

## 아직 하지 않은 일

- P017-A/B actual range 실행
- 실제 wall time·peak RAM 측정
- P013-B original 결과 감사
- existing serial P013 runner를 병렬 runner로 교체
- 더 큰 P013-C range 또는 새 scientific 가설검정
- figure 생성; 따라서 이번 로컬검증에는 사용자 시각 QA가 필요하지 않음

## 결론

구현은 실제 실행 준비가 됐지만, 원래 P013-B가 끝나기 전에는 실행하면 안 된다. actual PASS 후에도
속도·RAM·exact saved verification을 감사하고 사용자에게 다시 확인받기 전에는 serial 정본을
교체하지 않는다.
