# H1b-1b-2d.1a Maynard 905행 H remainder 작업원장

- 시작: 2026-09-08 10:15 KST
- 현재 상태: COMPLETE
- 사용자 승인: H1b-1b-2d.1a부터 권장 순서대로 문헌 조사·수학 정식화·보조 코드와
  toy/회귀검증·정본·핸드오프 갱신
- 허용: 로컬/웹 원문 취득·감사, 선행 lemma 적용성 검토, 필요한 최소 직접증명,
  고정 FGKMT Python의 데이터 비의존 검증
- 금지·보류: 실제 prime/maximal-gap sweep, P018-B, theorem threshold 계산,
  열린 상수 임의 대입, 새 패키지·Lean 설치, commit/push/PR
- 착수 상태: 기존 H1b-1b-2d 변경은 아직 미커밋 상태이며 최신 완료 원장과
  `handoff/202609080908_HANDOFF.md`를 읽고 그 위에 후속 변경만 추가한다.

## 목적과 완료조건

목적은 Maynard source 905행에서 Lemma 8.4에 입력되는
\(H=F+O(\eta F_2)\)의 remainder를 함수 수준으로 복원해, 수치 \(C^1\) envelope를
증명할 수 있는지 판정하는 것이다.

완료조건:

1. \(H\)가 생성되는 모든 앞 단계와 사용되는 뒤 단계를 source locator로 고정한다.
2. 동형의 명시적 remainder lemma를 선행연구에서 먼저 찾고, 가정·norm·부호·range를
   실제 호출과 대조한다.
3. 선행결과가 직접 적용되지 않으면 가장 작은 연결부만 직접 증명하거나 정확한
   blocker를 남긴다.
4. “값의 \(O(F_2)\) 상계”와 “도함수까지 포함한 \(C^1\) 상계”를 구분한다.
5. 하위 진전만으로 `H1B-L84`, `SIV-07`, \(X_{\rm cert}\)를 잘못 승격하지 않는다.
6. 기계 계약·시험·상위 원장·METHODS/AGENTS·핸드오프를 같은 상태로 동기화한다.

## 영향도 분석

| 축 | 영향 | 통제 |
|---|---|---|
| 수학 정의 | HIGH | opaque \(O\)-항을 숫자 1로 놓지 않고 함수·도함수·지지구간을 각각 추적한다. |
| 실제 데이터 | NONE | `datas/`와 `test_result/`의 actual artifact를 읽거나 생성하지 않는다. |
| source provenance | HIGH | Maynard 출판본·TeX·필요한 선행자료의 위치와 hash를 기록한다. |
| 수치 정밀도 | MEDIUM | 해석적 부등식과 exact/rational 검사를 우선하고 floating grid는 회귀검사로만 쓴다. |
| 승인 경계 | HIGH | 이론·toy 검증까지만 수행하며 장시간 계산과 threshold runner는 만들지 않는다. |
| 상위 proof DAG | HIGH | 하위 \(H\) envelope가 닫혀도 sharp \(\xi\), Lemmas 8.5--8.6, PAP가 남는다. |
| 재현성 | HIGH | source locator, 수식, 기계 계약, 실패 조건과 전체 회귀시험을 남긴다. |

## 접근 후보와 선택 기준

1. **원래 partial-summation error kernel을 함수로 보존해 재구성**
   - 가장 정확하지만 원 proof가 pointwise remainder를 버렸다면 대규모 재증명이 필요하다.
2. **비음수 \(F_2\) majorant와 미분 majorant를 직접 귀납**
   - 필요한 상계만 얻는 최소 경로다. 실제 error operator가 남은 변수의 미분과 교환되는지
     반드시 증명해야 한다.
3. **905행 합 전체를 Lemma 8.4 없이 처음부터 다시 상계**
   - 우회는 가능할 수 있으나 다른 Euler factor·support 누락 위험과 비용이 가장 크다.

우선 1을 source-trace하고, 완전한 함수 복원이 없으면 2의 충분조건을 검토한다.
2가 성립하지 않으면 3으로 성급히 확장하지 않고 blocker와 필요한 새 proof obligation을
먼저 확정한다.

## 단계 현황

1. **COMPLETED — 승인·영향·정본 상태 고정**
2. **COMPLETED — Maynard H 생성 경로와 actual 905행 사용 역추적**
3. **COMPLETED — 선행 explicit functional remainder lemma 조사**
4. **COMPLETED — 최소 project lemma/정확한 blocker와 기계 계약 구현**
5. **COMPLETED — 상위 정본 동기화·검증·새 handoff·완료 처리**

## 단계별 기록

### 2026-09-08 10:15 KST — 착수

- 최신 handoff와 기존 H1b-1b-2d 정본을 확인했다.
- memory의 과거 inventory는 11 analytic subapplication과 fail-closed 경계를 재확인하는
  보조자료로만 사용하며, 최신 정본의 smooth 7/9 진전으로 현재 상태를 다시 검증한다.
- 다음 재개점: Maynard source에서 905행의 \(H\)가 정의되는 800--850행과 그보다 앞선
  \(y_{\mathbf r}^{(m)}\) 변환을 식 단위로 추적한다.

### 2026-09-08 — source 생성·사용 경로와 문헌 우선 조사 완료

- 원문 411--426행에서 \(F,N,W,F_2\), 488--514행에서 `YDifference`,
  838--846행에서 `YmExpression`, 939--1038행에서 실제 \(H\) 생성 proof,
  903--916행에서 905행 Lemma 8.4 사용을 고정했다.
- \(H\)는 원문에서 하나의 전역 smooth remainder 함수로 구성되지 않는다. 외부 격자점마다
  얻은 적분값의 scalar `O`-오차를 \(H\) 표기로 압축했으므로, 그 표기만으로는 남은 변수의
  \(C^1\) norm을 추론할 수 없다.
- 원문 Lemma 9.3·1026행은 \((\log\log R)^2\)인데 915행만 한 제곱을 잃는다. 안전한
  numerical 재구성은 제곱을 보존해야 한다. 또한 986행의 \(\Delta\) 곱은 \(i=m\) 항을
  포함하면 0이 되므로 실제 \(t_j\) 범위와 같이 \(i\ne m\)인 determinant 곱으로 읽어야
  한다. 둘 다 표적 검색에서 정식 erratum을 확인했다는 주장은 하지 않는다.
- Maynard 출판본·arXiv/TeX 외에 Axiom `PrimeGapsLib`의 iterated partial summation을
  구조 교차검사했다. 그러나 다른 sieve datum과 존재형 cutoff를 사용하므로 이번 actual
  numerical input으로 채택하지 않았다. 표적 검색에서는 동일한 905행 remainder를 수치
  함수형으로 닫아 주는 peer-reviewed lemma를 찾지 못했으며, 전 세계 문헌 신규성 주장은
  하지 않는다.
- 최소 안전 경로를 확정했다. \(A=\int Fdt_m\), \(B=\int F_2dt_m\)이고 격자점에서
  \(|Z-A|\le\varepsilon B\)만 수치화하면
  \(|Z^2-A^2|\le2\varepsilon AB+\varepsilon^2B^2\)이다. \(A^2,AB,B^2\)는
  `N2`, `NW`, `W2`의 유한 비음수 smooth tensor 합으로 정확히 전개된다. 이 경로는
  존재가 불명확한 \(H\)의 도함수를 전혀 요구하지 않는다.
- 단, 원문의 986--999행에는 s-Euler product, t-divisor sum과 prefactor의 숨은 `<<`
  상수가 남는다. 이를 숫자 1로 놓지 않는다. 이번 단계는 functional/C1 blocker를
  scalar pointwise multiplier 의무로 축소하고, 그 multiplier가 열려 있음을 기계 계약에
  fail-closed로 남긴다.
- 다음 재개점: tensor 전개·support 순서·symbolic scalar remainder 계약을 코드와 JSON으로
  구현하고, 원래 opaque 분류를 `C1 bypassed / scalar multiplier open`으로 세분화한다.

### 2026-09-08 — square-sum project lemma·기계 계약 구현

- 신규 theory 25와 review 31에
  \(|Z^2-A^2|\le2\varepsilon AB+\varepsilon^2B^2\)를 증명하고,
  \(A^2,AB,B^2\)의 일곱 symmetry class, multiplicity와 wide-first support 순서를
  고정했다.
- `source/h1b1b2d1a_h_remainder_bypass.py`는 exact rational pointwise
  certificate, tensor inventory, support-scaled kappa family와 conditional evaluator를
  구현한다. supplied epsilon은 항상 assumption이고 source-certified로 승격할 API가 없다.
- 신규 JSON은 원문 844/1026행 대 915행의 log-log 제곱 불일치, 986행 determinant의
  \(i=m\) zero-factor, 998--999행 normalization 불명확성을 source caution으로 기록했다.
- source 986--999행의 s-Euler product, t-divisor sum, prefactor와 공통 \(C_Y\)는
  숫자 1로 두지 않고 OPEN으로 남겼다.
- py_compile와 신규 7개 시험 PASS. 상위 원장·분류를 동기화한 뒤 관련 45개
  회귀시험도 `Ran 45 tests`, `OK`였다.
- 오류 원장 E024/E027에 wrapper/context 거부, 잘못 추정한 파일명·Windows wildcard,
  malformed regex와 PDF extractor 권한 오류의 재발을 추가했다. 실패 출력은 수학 증거로
  쓰지 않았다.
- 다음 재개점: 정본 참조·JSON UTF-8·source hash·git diff를 감사하고 전체 unittest를
  실행한 뒤 새 handoff와 완료 원장을 만든다.

### 2026-09-08 11:24 KST — 최종 검증·정본 감사 완료

- 고정 FGKMT Python으로 신규 7개 시험과 관련 회귀 38개가 다시 PASS했다.
- 전체 suite 첫 샌드박스 실행은 임시 디렉터리 권한 때문에 82 errors가 발생했고, 동시에
  앞선 suite가 바꾼 `mp.mp.dps`에 의존한 신규 완전일치 시험 1건의 거짓 실패를 발견했다.
  제품 코드나 수학 정리 실패는 아니었다.
- 수치 비교를 `mp.almosteq`로 교정하고 exact algebra는 `Fraction` 시험에 그대로 보존했다.
  허가된 정상 로컬 권한에서 전체 suite를 재실행해 `Ran 293 tests in 41.392s`, `OK`를
  확인했다. 이 사건은 오류 원장 E030에 기록했다.
- theory JSON 15개 엄격 파싱, 신규 source hash, 내부 참조 6개, UTF-8 replacement character,
  절 번호 순서와 parent non-promotion을 검사했다. 모두 PASS했다.
- `git diff --check`는 exit 0이며 저장소 CRLF 변환 예고 외 whitespace error는 0이다.
- actual prime/maximal-gap 계산, P018-B, threshold 계산, 패키지 설치, commit/push/PR은
  수행하지 않았다.
- 새 핸드오프 `handoff/202609081124_HANDOFF.md`를 작성한 뒤 이 원장을 `-done`으로
  이름 변경한다.

## 완료 전 점검

- [x] 원문 생성·사용 경로 전수 고정
- [x] 선행연구 우선 조사와 실제 적용성 판정
- [x] 값/미분/지지/support order를 분리한 proof
- [x] 열린 상수·범위와 닫힌 하위식 분리
- [x] 실제 실험·threshold 미실행 경계 유지
- [x] 코드·JSON·정본·상위 DAG 동기화
- [x] 고정 FGKMT Python 표적·전체 검증
- [x] 오류·실패를 원장에 기록
- [x] 새 timestamp handoff
- [x] `git diff --check`·UTF-8·참조 경로 검사
- [x] 파일명을 `-done.md`로 변경
