# P003 - FGKMT/Sono end-bounded maximal-gap 전체 `10^20` 분석

> 상태: **COMPLETED / AUTOMATED PASS / USER VISUAL QA COMPLETED**
> 승인 근거: 2026-08-23 사용자가 전체 `10^20` 분석, 모든 `F/H` 계산 검증, 독립 source 교차검증, log-bin 및 rolling local envelope, 문헌 비교와 후속 가설 보고를 명시적으로 요청했다.  
> authoritative run: `20260822T195906Z_full1e20`, exit 0, elapsed 7.654초  
> 이 문서는 본 계산 전에 고정한 계획이다. 결과를 본 뒤 계산 정의나 판정 기준을 소급 변경하지 않는다.

## 1. 연구 질문과 비목적

검증된 maximal prime-gap record로 end-bounded 계단함수

\[
G_{\mathrm{end}}(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

를 `x=3,814,280`부터 검증된 exhaustive limit `10^20`까지 복원한다. FGKMT/FMT large-gap scale

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},\qquad
H(x)=\frac{G_{\mathrm{end}}(x)}{F(x)}
\]

에 대한 interval minimum, global running minimum, record-jump recovery, log-bin minimum과 고정 record-window rolling minimum을 계산한다. Sono의 explicit constant `2.0e-17`, Wolf 계열의 경험적 `H=1` 참고선, Cramer형 보조 정규화와 비교한다.

비목적은 다음과 같다.

- 유한 계산으로 FGKMT/FMT 또는 Sono의 무한 범위 정리를 증명·검증·반증하지 않는다.
- Sono 상수를 관측 `H`의 예상 극한으로 취급하지 않는다.
- 기술적 추세선이나 local envelope를 독립 표본의 통계적 추론으로 취급하지 않는다.
- 전체 소수를 `10^20`까지 생성하지 않는다.
- 새 패턴을 검증 없이 정리나 확정된 수론적 추측으로 발표하지 않는다.

## 2. 수학 정의와 경계

모든 로그는 자연로그이며 아래 첨자는 반복 횟수다.

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 적용}}
\]

특히 `log_2`, `log_3`, `log_4`는 base-2, base-3, base-4 로그가 아니다.

record `i`의 시작 소수, gap, 끝 소수를 각각 `s_i`, `g_i`, `e_i=s_i+g_i`라 하면 canonical analysis interval은

\[
[e_i,e_{i+1}-1]
\]

이다. 양의 scale 시작점과 분석 상한으로 clip하며, `F`가 증가하는 이 구간의 정확한 minimum은

\[
H_{i,\min}=\frac{g_i}{F(e_{i+1}-1)}
\]

이 exact minimum은 사전에 고정한 정수 `x` domain에 대한 값이다. 실수 `X`를 쓰면 plateau는 `[e_i,e_(i+1))`이고 해당 값은 `X -> e_(i+1)-`에서의 infimum `g_i/F(e_(i+1))`으로 구분한다.

마지막 record interval은 `10^20`에서 닫는다. 결과 표와 분석 보고서에는 canonical `[interval_start, interval_end]`뿐 아니라 해당 gap의 `start_prime=s_i`와 `end_prime=e_i`를 함께 표시한다.

문헌 경계는 다음처럼 구분한다.

- Sono `G_1(X)`: `p_(n+1) <= X`, 현재 end-bounded 함수와 정확히 일치
- FGKMT 2018 `G(X)`: `p_n <= X`, 유한 함수는 start-bounded
- 본 분석은 Sono 직접 비교를 위해 end-bounded를 정본으로 유지하고 FGKMT에 대해서는 large-gap scale의 출처로 비교한다.

## 3. 입력과 provenance

### 3.1 canonical source

- repository: `https://github.com/primegap-list-project/prime-gap-list`
- 정본 파일: 동일한 40자리 commit으로 고정한 `allgaps.sql`, `schema.sql`
- pilot에서 확인한 commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- pilot raw SHA-256: `988c3278d95a16460a9897e09829fb061ee854e55efa6c4fcec3b9779930894f`
- pilot schema SHA-256: `86ba1748af4d8f95c465812c9103c75e61aa6470751a3fc92c1f957dba00b0ed`
- pilot normalized SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- documented exhaustive limit: `10^20` as of 2026-05-08

실행 직전에 remote `master`를 다시 resolve한다. commit이 pilot과 같으면 기존 immutable raw 및 validated CSV를 hash 대조 후 재사용한다. 달라졌으면 새 commit 디렉터리에 취득·검증하고 기존 파일을 덮어쓰지 않는다.

### 3.2 독립 교차검증 source

1. OEIS A002386 b-file: record gap의 lower/start prime sequence
2. OEIS A005250 b-file: maximal prime-gap size sequence
3. 가능하면 Oliveira e Silva 공식 `t0.txt.gz`: 별도 계산으로 얻은 중첩 record 자료

각 원본은 URL, 취득 UTC, byte 수, SHA-256, 항 수, 경계 의미를 metadata에 남기고 immutable run/source 디렉터리에 저장한다. OEIS는 독립적인 데이터 표현이지만 계산 자체의 완전한 독립성을 보장하지 않는다는 한계를 명시한다. Oliveira e Silva 자료는 중첩 범위의 별도 계산 근거로 분리한다.

## 4. 입력 필터와 record 복원

- SQL을 실행하지 않고 허용된 `INSERT INTO gaps VALUES (...)` 문법만 제한 파싱한다.
- `primecat=C`, `isfirst=F`, exhaustive limit 안의 행만 candidate로 삼는다.
- candidate를 start prime 순으로 정렬해 high watermark를 독립 재도출한다.
- upstream `ismax=1`과 완전히 일치해야 한다.
- 각 record에서 `start+gap=end`, start/end/gap 엄격 증가, `gmpy2.next_prime(start)==end`를 검사한다.
- 큰 정수는 Python `int`와 CSV 10진 문자열로 보존한다.

## 5. local envelope 정의

### 5.1 log-bin minimum

정수 decade bin을

\[
(10^k,10^{k+1}]\cap[3{,}814{,}280,10^{20}]
\]

로 고정한다. 즉 실제 정수 범위는 `[10^k+1, 10^(k+1)]`이고 첫·마지막 bin은 분석 범위로 clip한다. 각 bin과 겹치는 모든 end-bounded record interval에서 겹침의 오른쪽 끝을 평가하고 그중 가장 작은 `H`를 정확한 bin minimum으로 선택한다.

### 5.2 rolling local envelope

interval-minimum sequence에 대해 직전 `w`개 record interval의 최소를 계산한다. 주 window는 `w in {5,10,20}`으로 고정한다. window가 완전히 찬 지점부터만 산출하며, global running minimum과 별개이므로 이전의 낮은 값이 window 밖으로 빠지면 상승할 수 있다.

## 6. 전수 수치검증

정본 계산은 `mpmath` 50 decimal digits로 저장한다. 별도 검증기는 `mpmath` 100 decimal digits에서 `source.definitions.F/H`를 호출하지 않고 직접 중첩한 `mp.log` 식을 사용한다.

모든 interval에 대해 다음을 검사한다.

- record의 `start_prime`, `gap`, `end_prime`
- `[end_i,end_(i+1)-1]` 경계와 마지막 `10^20` clip
- `F(interval_start)`, `F(interval_end)`
- `H(interval_start)=gap/F(interval_start)`
- `H_interval_min=gap/F(interval_end)`
- Sono ratio, Cramer 보조 ratio, running minimum
- 모든 jump의 직전/직후 H와 recovery factor
- 모든 log-bin minimum 및 `w=5,10,20` rolling minimum
- 저장된 40자리 문자열과 독립 100자리 계산의 상대오차 `<=1e-38`

경계 regression으로 실제 `gap=154`, `start=4,652,353`, `end=4,652,507`, 다음 end `17,051,887`을 사용해 interval이 정확히 `[4,652,507,17,051,886]`이고 minimum이 `154/F(17,051,886)`인지 시험한다.

## 7. 사전검증과 중단 조건

다음 중 하나라도 실패하면 실제 전체 분석 또는 해석을 중단한다.

- 지정 Python 불일치 또는 단위시험 실패
- base-k 로그 호출 발견
- remote commit·raw/schema/validated hash 불일치
- validation issue, rejected maximal record 또는 `ismax` 불일치
- exhaustive limit가 `10^20`보다 작음
- end-bounded interval 공백·중복·잘못된 오른쪽 경계
- `F` 비양수 또는 비증가 구간 진입
- 100-dps 전수검증 허용오차 초과
- 독립 source의 공통 범위 record mismatch
- 기존 run/source 경로와 충돌

독립 source mismatch는 canonical 분석값을 자동으로 바꾸지 않고 원인·경계·source version을 조사한 뒤 `FAIL` 또는 설명 가능한 coverage 차이로 기록한다.

## 8. 승인된 실행 명령

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli preflight
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m source.cli analyze `
  --approved-by-user `
  --records-path '<validated maximal_gap_records.csv>' `
  --analysis-limit 100000000000000000000 `
  --run-id '<UTC run id>'
```

독립 source 취득·교차검증과 결과 전수검증은 구현된 CLI의 승인 flag와 동일 run id를 사용한다. 표준 PowerShell 실행기는 stdout/stderr, 시작·종료 UTC, 경과시간, 종료코드를 전용 로그에 보존한다.

## 9. 예상 산출물

```text
test_result/run_<run-id>/summary.json
test_result/run_<run-id>/verification_report.json
test_result/run_<run-id>/cross_validation/*.json
test_result/run_<run-id>/tables/end_bounded_intervals.csv
test_result/run_<run-id>/tables/end_bounded_jumps.csv
test_result/run_<run-id>/tables/log10_bin_minima.csv
test_result/run_<run-id>/tables/rolling_local_envelope_w5.csv
test_result/run_<run-id>/tables/rolling_local_envelope_w10.csv
test_result/run_<run-id>/tables/rolling_local_envelope_w20.csv
test_result/run_<run-id>/figures/*.png
test_result/run_<run-id>/figures/*.pdf
test_result/logs/run_<run-id>.log
test_result/<timestamp>_P003_full_analysis.md
docs/review/10_P003_문헌비교와_후속가설.md
handoff/<YYYYMMDDHHmm>_HANDOFF.md
```

## 10. 판정 기준과 해석 제한

- `PASS`: 모든 canonical interval과 저장된 수치가 독립 100-dps 계산에 일치하고, source validation 및 공통범위 교차검증 mismatch가 0이다.
- `WARNING`: 독립 source가 최신 범위 전체를 제공하지 않거나 계산 독립성이 불명확하지만 중첩 record는 모두 일치한다.
- `FAIL`: canonical record, 경계 또는 수치 mismatch가 설명되지 않는다.

log-log slope와 correlation은 기술통계로만 보고한다. log-bin/rolling 변화는 후속 가설 후보를 찾는 도구이지 점근 법칙의 증거가 아니다. 새 가설은 관측 범위, 반례 탐색 방법, 다음 검증범위를 함께 명시한다.

## 11. 변경 영향 분석

| 축 | 판정 | 근거와 대응 |
|---|---|---|
| 수학 정의·iterated log | 영향 있음 | F/H 값을 양끝 모두 저장하고 100-dps 직접식으로 전수 대조; 정의 자체는 변경 없음 |
| end-bounded 의미론 | 영향 있음 | 표·보고서에 gap start를 추가하되 interval 경계는 오직 end prime; regression test 추가 |
| dataset provenance | 영향 있음 | canonical commit 재확인과 독립 source metadata/hash 추가 |
| 큰 정수·고정밀도 | 영향 있음 | 정수는 문자열/int, 계산은 50 dps, 독립 검증은 100 dps |
| 승인 경계 | 영향 있음 | 이번 사용자 지시로 P003 범위 승인; 그 밖의 start-bounded 본 분석·외부 게시 미승인 |
| 통계·그래프 재현성 | 영향 있음 | log-bin·rolling 정의와 window를 실행 전에 고정; 새 run id로 비덮어쓰기 |
| 정리·경험 관찰 구분 | 영향 있음 | Sono exact boundary, FGKMT start-boundary 차이와 유한 관측 한계를 보고 |
| 문서·테스트·handoff | 영향 있음 | METHODS, 결과보고서, 문헌 비교, 회귀시험, 새 timestamp handoff 갱신 |

## 12. 후속 작업

1. 새 전체 그래프의 사용자 시각 QA는 완료됐다.
2. local-envelope 민감도와 start/end paired 분석은 P004에서 완료됐다.
3. 더 넓은 exhaustive 탐색 가능성은 P005에서 calibration gate로 분리했다.
4. plateau recurrence는 P006에서 별도 pilot으로 준비했다.

## 13. 실행 결과와 판정

최종 판정: **PASS**. 그래프의 표현 품질도 사용자가 큰 문제없다고 확인했다.

### 자동검증

- exact Python: `W:\miniforge3\envs\FGKMT\python.exe` 3.11.16
- tests: 43 PASS
- canonical commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated CSV SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- analyzed intervals/jumps: 64/63
- log bins: 14
- rolling rows `w=5/10/20`: 60/55/45
- 100-dps independent numeric values: 1,160 PASS, issue 0
- maximum stored relative error: 약 `7.64e-41`, criterion `1e-38`
- boundary regression gap 154: `[4,652,507,17,051,886]` PASS
- OEIS overlap: 84 match, mismatch 0
- Oliveira separate-computation overlap: 75 match, mismatch 0
- figure files: 16, missing 0

### 핵심 결과

- global minimum (H=37.81686039672168054712906420750827080243)
- minimum x `1,346,294,311,330`, gap start/end/gap `738,832,927,927 / 738,832,928,467 / 540`
- final (H(10^{20})=44.53116946232701044223115453741495101863)
- minimum Sono ratio 약 `1.890843019836084027e18`
- `H<1` 및 `H<2e-17`: 없음

### 보존된 비정본 실행

- `20260822T194942Z_full1e20`: Oliveira 단계를 추가하기 전 예비 성공 run
- `20260822T195758Z_full1e20`: Oliveira 대조 PASS 후 CP949 console 출력 오류로 exit 1; final verifier 미실행
- 정의·입력·판정기준은 바꾸지 않고 console label만 ASCII-safe하게 수정한 뒤 authoritative run을 새 ID로 재실행

상세 해석은 `test_result/202608230503_P003_full_analysis.md`, 문헌 비교와 후속 가설은 `docs/review/10_P003_문헌비교와_후속가설.md`, 다음 작업은 `handoff/202608230503_HANDOFF.md`에 기록했다.
