# P002 — FGKMT-Sono 5개 record interval 제한 pilot

> 상태: **COMPLETED (사용자 그래프 시각 QA 완료)**
> 승인 근거: 사용자가 2026-08-23 대화에서 데이터 다운로드와 `x=16`, `x=3,814,280`, 이후 5개 소수 interval에 대한 실제 실행을 명시적으로 요청했다.  
> 범위 고정: 이 승인은 아래 제한 pilot에만 적용되며 P001의 전체 `10^20` 분석 승인이 아니다.

## 1. 연구 질문과 비목적

이 pilot은 실제 Prime Gap List Project 자료를 내려받아 provenance·검증·계산·그래프 파이프라인이 올바르게 작동하는지 작은 분석 범위에서 확인한다.

- `x=16`에서 반복로그가 실수로 정의되지만 `F(x)<0`임을 확인한다.
- `x=3,814,280`에서 `F(x)>0`이며 end-bounded `G(x)`와 `H(x)` 계산을 시작할 수 있음을 확인한다.
- `x=3,814,280`을 포함하는 record plateau를 첫 구간으로 삼아 연속된 end-bounded maximal-gap record interval 5개만 분석한다.
- 각 구간의 감소, 오른쪽 끝 최소, running minimum, 다음 record에서의 회복과 Sono/Wolf 참고선 대비 값을 시험한다.

비목적:

- `10^20`까지의 전체 empirical envelope 분석
- 장기 추세 또는 새로운 수론적 추측 확정
- FGKMT/Sono 무한 범위 정리의 증명·검증·반증
- `x=16`을 theorem-scale `H`, Sono ratio 또는 running minimum에 포함

## 2. 수학 정의

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 반복}}
\]

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\qquad
H(x)=\frac{G(x)}{F(x)}.
\]

`math.log(x, 2|3|4)` 같은 base-`k` 로그는 금지한다. 작업 정밀도는 `mpmath` 50 decimal digits 이상이다.

## 3. 데이터 원천과 provenance

- canonical repository: `https://github.com/primegap-list-project/prime-gap-list`
- 입력: 실행 시점의 `master`를 40자리 commit으로 resolve한 동일 commit의 `allgaps.sql`, `schema.sql`
- 웹 high-watermark 표: 참고만 하며 입력으로 스크레이핑하지 않음
- 문서화된 exhaustive limit: `10^20` (2026-05-08)
- 실제 commit, raw URL, 취득 UTC, byte 수, SHA-256: 취득 직후 이 계획의 실행 이력과 metadata에 기록
- raw 및 validated 경로: commit별 불변 경로, 기존 파일 비덮어쓰기

원자료 전체는 record를 복원·검증하기 위해 읽되, 수학 분석 및 그래프는 고정한 5개 interval까지만 수행한다.

## 4. 입력 필터와 record 복원

1. SQL을 실행하지 않고 허용된 `INSERT INTO gaps VALUES (...)` 문법만 제한 파싱한다.
2. `primecat='C'`, `isfirst='F'`, `end_prime<=10^20`인 row를 대상으로 한다.
3. eligible first occurrences에서 high-watermark를 독립 재도출해 upstream `ismax`와 대조한다.
4. `end_prime=start_prime+gap`, record 순서·gap 증가, `gmpy2.next_prime(start_prime)==end_prime`을 검증한다.
5. source의 start-prime ordering을 `end_prime` jump로 변환한다.
6. `x=3,814,280`에서 활성인 record를 찾고, 그 plateau를 포함해 연속 5개 interval을 선택한다.
7. 다섯째 interval의 오른쪽 끝은 여섯째 plateau가 시작되는 `end_prime-1`로 정한다.

## 5. 사전검증과 중단 조건

실행 전 필수:

- Python executable이 정확히 `W:\miniforge3\envs\FGKMT\python.exe`
- 전체 단위시험 PASS
- CLI preflight PASS
- iterated-log 직접 중첩 대조 및 base-2/3/4 negative control PASS
- source 코드의 금지된 base-`k` 호출 0건
- 원격 commit을 40자리 SHA로 고정
- raw, validated, log, run output 충돌 0건

즉시 중단:

- schema 변경, 미해석 row, `ismax` 불일치, consecutive-prime 실패
- source hash 또는 commit 불일치
- 5개 interval을 정확히 닫을 다음 record 부족
- 분석 interval 수가 5가 아님
- `x=16`의 `F`가 음수가 아니거나 `x=3,814,280`의 `F`가 양수가 아님
- running minimum이 증가함
- 기존 산출물 덮어쓰기 위험

## 6. 승인된 실행 명령

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli preflight
.\run_pilot.ps1 -Approved -IntervalCount 5
```

실행 시 resolve한 commit을 명령에 명시해 재현할 수도 있다.

```powershell
.\run_pilot.ps1 -Approved -IntervalCount 5 -Commit '<40-character-commit>'
```

## 7. 예상 산출물

```text
datas/raw/prime-gap-list-project/<commit>/allgaps.sql
datas/raw/prime-gap-list-project/<commit>/schema.sql
datas/raw/prime-gap-list-project/<commit>/metadata.json
datas/validated/prime-gap-list-project/<commit>/maximal_gap_records.csv
datas/validated/prime-gap-list-project/<commit>/validation_report.json
test_result/logs/run_<run-id>.log
test_result/run_<run-id>/tables/end_bounded_intervals.csv
test_result/run_<run-id>/tables/end_bounded_jumps.csv
test_result/run_<run-id>/figures/*.png
test_result/run_<run-id>/figures/*.pdf
test_result/run_<run-id>/summary.json
test_result/<timestamp>_P002_analysis.md
```

## 8. 성공 기준과 해석 제한

- validation status `PASS`, error issue 0, `ismax` 불일치 0
- 결과 interval 정확히 5개와 내부 jump 4개
- `x=16`은 domain diagnostic으로만 기록되고 주 분석에서 제외
- `x=3,814,280`부터 양의 scale 분석
- interval minimum은 각 구간의 정확한 정수 오른쪽 끝에서 계산
- running minimum 비증가
- 선택 행의 `G`, `F`, `H`, Sono ratio를 별도 계산과 대조
- 로그와 분석 보고서를 서로 다른 파일로 보존

5개 구간은 코드 작동과 정의·경계 검증에는 충분하지만 장기 추세 판단에는 너무 작다. Wolf 또는 Sono와의 비교값은 이 제한 범위의 관측치일 뿐 일반 결론이 아니다.

## 9. 예상 수행시간

- source commit 조회 및 다운로드: 약 1~3분
- 전체 raw validation: 약 1~5분
- 5개 interval 계산·그래프: 약 1분 이내
- 독립 대조·결과 문서화: 약 5~15분

네트워크와 원자료 크기에 따라 달라지며, 완료 뒤 실행 로그의 실제 elapsed time으로 교체한다.

## 10. 실행 이력

- 계획 고정 시점: 2026-08-23 (Asia/Seoul)
- pin commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- raw SHA-256: `988c3278d95a16460a9897e09829fb061ee854e55efa6c4fcec3b9779930894f`
- schema SHA-256: `86ba1748af4d8f95c465812c9103c75e61aa6470751a3fc92c1f957dba00b0ed`
- validated records SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- run id: `20260822T181837Z_pilot5`
- 실제 runner 시간: 4.933초
- validation: PASS, issues 0, selected maximal records 84
- 분석: `x=3,814,280`부터 `x=122,164,968`까지 5 intervals, 4 jumps
- minimum H: `61.490063260711694...` at `x=122,164,968`
- minimum Sono ratio: `3.074503163035584702e18`
- 독립 hash·직접 중첩 자연로그·경계·running minimum 검증: PASS
- 자동 판정: COMPLETED
- 사용자 확인: PNG 6개의 축·범례·provenance·가독성 시각 QA 완료
- 결과 분석: `test_result/202608230323_P002_analysis.md`

