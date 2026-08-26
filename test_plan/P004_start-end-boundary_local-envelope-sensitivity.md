# P004 — Start/End 경계 및 Local Envelope 민감도 분석

## 1. 상태

`COMPLETED` — authoritative run `20260823T075238Z_p004_sensitivity`가 전체 47 tests와 100-dps 독립 검증 3,747개(issue 0)를 PASS했고, 사용자가 새 제한축 그래프도 큰 문제없다고 확인했다.

## 2. 연구 질문과 비목적

연구 질문은 다음과 같다.

1. P003의 Sono-compatible end-bounded 정수 함수와 FGKMT 원문의 start-bounded 정수 함수가 유한 범위에서 얼마나 다르게 보이는가?
2. P003의 global minimum과 local-envelope 관찰이 log-bin 원점이나 record-count window 선택에 민감한가?
3. record 개수가 아닌 고정된 log10(x) 폭으로 정의한 trailing local envelope에서도 최근 하한 회복이 나타나는가?
4. 첫 interval의 큰 값 때문에 가려진 후반부 궤적을 제한축 그래프로 더 잘 판독할 수 있는가?

비목적:

- end-bounded 함수를 start-bounded 함수로 교체하지 않는다.
- Sono 정리의 finite threshold나 무한 범위 명제를 검증하지 않는다.
- start-bounded H를 Sono의 G_1과 동일한 함수라고 부르지 않는다.
- bin/window 선택을 사후적으로 유리한 결론에 맞추지 않는다.

## 3. 수학 정의

반복로그는 항상 자연로그를 반복한다.

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)))}_{k\text{회}},\qquad
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}.
\]

record i를 `(s_i,g_i,e_i=s_i+g_i)`라 한다.

### 3.1 Sono-compatible end-bounded 함수

\[
G_{\mathrm{end}}(x)=\max_{e_i\le x}g_i,qquad
e_i\le x\le e_{i+1}-1.
\]

정수 interval minimum은 `g_i/F(e_(i+1)-1)`이다.

### 3.2 FGKMT finite start-bounded 함수

\[
G_{\mathrm{start}}(x)=\max_{s_i\le x}g_i,qquad
s_i\le x\le s_{i+1}-1.
\]

정수 interval minimum은 `g_i/F(s_(i+1)-1)`이다. 두 함수는 새 record i마다 `[s_i,e_i-1]`에서만 다르고 그 구간에서는 같은 x에서의 H 비가 정확히 `g_i/g_(i-1)`이다.

논문 변수를 실수 X로 연장할 때는 각 half-open interval의 minimum이 아니라 다음 jump에서의 좌극한 infimum을 사용해야 한다. 본 계산은 P003과 같이 정수 x만 사용한다.

### 3.3 Shifted log-bin

shift `a in {0.25,0.50,0.75}`에 대해

\[
(10^{k+a},10^{k+1+a}]
\]

의 정수점을 사용한다. 각 bin은 분석 범위에 clip하고, 모든 end-bounded plateau와의 교집합 오른쪽 끝을 후보로 하여 정확한 최솟값을 고른다.

### 3.4 추가 record-count rolling envelope

P003의 `w={5,10,20}`은 보존하고 `w={3,8,15,30}`을 추가한다. 완전한 trailing record window만 출력한다.

### 3.5 x-width trailing envelope

`d in {0.5,1,2}` decades에 대해 각 end-bounded interval 오른쪽 끝 x에서

\[
E_d(x)=\min_{\lceil x/10^d\rceil\le t\le x}H_{\mathrm{end}}(t)
\]

를 계산한다. 분석 시작점보다 왼쪽으로 나가는 초기 window는 clip 여부를 별도 필드로 저장한다.

## 4. Dataset와 provenance

- canonical records: `datas/validated/prime-gap-list-project/1a112a1387052d9ad360686313f501c01fe46b68/maximal_gap_records.csv`
- source commit: `1a112a1387052d9ad360686313f501c01fe46b68`
- records SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- verified exhaustive limit: `100000000000000000000`
- 분석 범위: `[3814280, 10^20]`
- 새 외부 dataset 취득 없음

## 5. 입력 필터와 record 복원 규칙

- P003에서 검증 완료한 84개 record CSV를 그대로 읽는다.
- record gap, start prime, end prime은 엄격히 증가해야 한다.
- 분석 상한을 넘는 record를 사용하지 않는다.
- start/end 경계마다 별도 interval을 만들고 동일 record_index로 pair한다.
- gap start와 gap end를 모든 결과 표에 병기한다.

## 6. 영향 분석 및 사전검증·중단 조건

상세 영향 분석은 `docs/review/11_P004_엄밀한_경계_보정_영향분석.md`를 따른다.

실행 전 자동 게이트:

1. Python executable이 `W:\miniforge3\envs\FGKMT\python.exe`와 정확히 일치해야 한다.
2. 기존 `source.cli preflight`와 전체 단위시험이 PASS해야 한다.
3. records SHA-256과 source commit, exhaustive limit가 위 값과 일치해야 한다.
4. log_k base-log 금지 시험과 gap 154 end-boundary 회귀시험이 PASS해야 한다.
5. start-boundary toy 회귀시험과 shifted/x-width brute-force toy 비교가 PASS해야 한다.
6. 출력 run directory와 log가 이미 존재하면 중단한다.
7. end/start interval이 분석 범위를 각각 빈틈 없이 덮지 못하거나 F가 증가하지 않으면 중단한다.
8. 100-dps 독립 직접식 검산에서 하나라도 불일치하면 결과를 PASS로 해석하지 않는다.

## 7. 실행 당시 명령 provenance — 재실행 금지

```powershell
.\test_done\run_sensitivity_analysis-20260823T075238Z-done.ps1 -Approved
```

위 명령은 실행 당시 provenance를 설명하기 위한 기록이다. `test_done` 파일은 다시
실행하지 않는다. 재실험이 필요하면 `scripts/experiments/` 아래에 새 revision runner를
만들고 새 run id와 별도 사용자 승인을 사용한다.

실행기는 `source.cli preflight` → P004 단위시험 → 분석 → 100-dps 검산 순서로 진행하며 첫 실패에서 중단한다.

## 8. 산출물

- `test_result/run_<run-id>/summary.json`
- `test_result/run_<run-id>/verification_report.json`
- start/end interval 및 paired CSV
- start/end가 다른 짧은 boundary-window CSV
- shift별 log-bin CSV
- w=3,8,15,30 rolling CSV
- d=0.5,1,2 x-width envelope CSV
- y 최대 10^4 trajectory, 첫 interval 생략+y 최대 10^3 trajectory
- paired boundary, shifted bin, rolling, x-width 그래프 PNG/PDF
- `test_result/logs/run_<run-id>.log`

## 9. 판정 기준과 해석 제한

- 모든 저장 수치와 경계의 100-dps 재계산 일치가 PASS 조건이다.
- start/end 차이는 finite boundary convention의 효과이며 어느 한쪽의 오류를 뜻하지 않는다.
- shifted/bin/window 결과가 비슷해도 점근적 안정성을 증명하지 않는다.
- 서로 겹치는 rolling·x-width window는 독립 표본이 아니므로 p-value를 산출하지 않는다.
- 그래프 시각 QA는 사용자의 직접 확인을 받아 완료로 표시한다.

## 10. 후속 작업

- 그래프 사용자 시각 QA — 완료
- 필요 시 real-X infimum 표를 별도 이론 부록으로 추가
- P005 exhaustive-range 확장 타당성 calibration과 P006 plateau recurrence pilot은 별도 승인·계획으로 유지

## 11. 완료 결과

- authoritative run: `20260823T075238Z_p004_sensitivity`
- runner elapsed / exit: `9.466초 / 0`
- end/start/paired intervals: `64 / 64 / 64`
- end global minimum: `37.81686039672168054712906420750827080243`
- start global minimum: `37.81686039812796235781969318162473189002`
- 두 minimum의 record/gap: record 50, gap 540
- start/end difference windows: 63개, 총 정수 폭 50,016
- largest paired interval-minimum relative effect: 약 `0.0167%`
- shifted bin 3종의 global minimum record: 모두 record 50로 동일
- additional rolling final H: w3 `43.1355`, w8 `41.9065`, w15 `41.4586`, w30 `38.8990`
- x-width final H: 0.5 decade `43.9239`, 1/2 decades `41.9065`
- verification: 100 dps, 3,747개, issue 0, 최대 상대오차 약 `4.79e-40`
- graph files: 12개 존재·hash 검증 PASS; 사용자 visual QA 완료

첫 실행은 승인 token 불일치로 분석 전 중단했고, 두 번째 실행은 극소 paired delta의 cancellation을 독립 검증이 검출해 FAIL했다. guard precision과 안정적인 상대차 수식으로 수정한 세 번째 실행만 authoritative로 사용한다. 실패 산출물은 감사 추적용으로 보존한다.

일상용어 상세 결과는 `test_result/202608231652_P004_sensitivity_analysis.md`, 수학적 영향 분석은 `docs/review/11_P004_엄밀한_경계_보정_영향분석.md`를 따른다.
