# H1b-P94g growing-k actual upper moment 타당성 검토

- 작성: 2026-09-09 KST
- 정본: [theory 46](../method/theory/46_Sono_FMT_H1bP94g_growing_dimension_rough_moment.md)
- 계약: [P94g JSON](../method/theory/data/Sono_FMT_H1bP94g_growing_dimension_v1.json)
- 판정: actual filtered growing-dimension child 정식화 완료; 전체 X_cert 미완료

## 1. 이번 작업을 쉽게 설명하면

소수 후보마다 점수를 붙이는 방법에서, 우리가 의도한 위치 이외의 소수에 점수가 너무 많이
몰리지 않는지도 확인해야 한다. P94는 그 “다른 위치로 가는 점수의 총량”을 제한하는 도구다.

기존 증명에는 차원 k가 증가할 때 오차를 매우 크게 잡는 2^k 비교가 있었다.
k=10이면 1024이지만, 우리 증명에서 쓰는 k는 그보다 훨씬 크다.
이를 처리하려고 기존 방법은 오차가 2^(-k) 이하가 될 만큼 큰 cutoff를 요구했다.

P92 단계에서 이미 증명한 새 비교는 필요한 큰 차원에서 **최대 2배**면 충분하다고 말한다.
이번에는 그 결과를 P94에 정확하게 연결했다.
계산 항을 생략하거나 낮은 정밀도로 근사한 것이 아니라, 더 적합한 부등식을 사용한 것이다.

## 2. 얻은 결과와 얻지 못한 결과

새 조건
\[
 k=\lfloor(\log(X/2))^{1/5}\rfloor\ge10^{200}
\]
과 명시적 h 범위·W-filter 아래에서 P94 표준 크기에 붙일 multiplier를 1로 둘 수 있다.
마지막 비교는
\[
 8249009/8820900<1
\]
이라는 정수·유리수 계산으로 닫았다. float 소수값만 보고 1보다 작다고 한 것이 아니다.

기존 13 상계를 “틀렸다”고 바꾼 것이 아니다.
기존 것은 별도 parameterized cutoff에서의 보수적 결과이고,
새 1은 **훨씬 강한 growing-k regime**에서의 결과다.
이 둘을 같은 조건에서 13배 성능이 개선된 것처럼 해석하면 안 된다.

아울러 각 p에 대해 원래 tuple 밖의 prime 위치가 받는 점수 총량을
local weight scale의 \(1/(\log_2X)^{10}\) 이하로 제한했다.
공통 singular series·tau·u로 옮기는 일과 p-average는 아직 남는다.

현재 결과는 다음 어느 것도 아니다.

- Sono 부등식의 최소 성립점 또는 전체 X_cert
- 실제 prime-gap 데이터를 더 큰 범위까지 조사한 결과
- 소수 탐색 알고리즘의 속도 개선
- Lean이나 외부 수학자의 독립 증명 심사

고정 h 범위 상수 C_h에 대한 충분조건은
\(X\ge2\exp\{\max(10^{1000},4\log C_h)\}\)다.
엄청나게 큰 수를 하나하나 계산했다는 뜻이 아니며 child cutoff일 뿐이다.

## 3. 원문 대조에서 실제로 보완한 세 가지

### 3.1 외부 크기와 실제 적용 구간은 다르다

P94의 실제 구간 크기는 X가 아니라 \(T_0=\lfloor Y\rfloor-\lfloor X\rfloor\)다.
원래 q가 (X,Y]에 있으면 이동 뒤 정수는 (T0,2T0]에 있다.

예를 들어 X=13, Y=55이면 T0=42이다.
q=14,...,55가 t=43,...,84로 옮겨진다.
42를 포함하는 [42,84]와 정확히 같지는 않다.
상계만 필요하고 점수가 모두 0 이상이므로 42를 추가한 더 큰 합을 사용해도 안전하다.
새 toy는 이 추가 점수 차이를 일부러 검출한다.

기존 theory 31의 R=(x/4)^(1/9)와 x를 그대로 actual shifted interval의 등식으로
읽으면 부족하다. 새 증명은 R를 외부 X에 고정하고,
local T0에 대해 허용 범위가 성립하는지를 따로 확인한다.

### 3.2 원래 점수의 범위 제한은 자동이 아니다

원래 weight는 [-Y,Y] 밖에서 0이다.
h가 크면 q-hp가 그 밖으로 나갈 수 있으므로 이 제한을 제거한 합과 같다고 할 수 없다.
새 proof는 “같다”가 아니라 “범위 제한을 없애면 합이 더 커지거나 같다”로 연결한다.

### 3.3 h의 숨은 상수를 숫자 조건으로 바꿨다

“h=O(Y/X)”의 O에는 범위 상수가 숨어 있다.
C_h>=1을 명시하고 |h|<=C_h Y/X 및 log(C_h)<=log(X/2)/4를 사용한다.
따라서 C_h=1만으로 문제를 축소하지 않으면서도 form 크기·Delta 조건을 확인할 수 있다.
helper는 이 범위를 넘기거나 h=h_i가 되어 Delta=0인 toy 입력을 거부한다.

## 4. 재사용한 선행증명과 문헌 한계

| 자료·정확한 위치 | 채택·확인 내용 |
|---|---|
| [Maynard 2016](https://doi.org/10.1112/S0010437X16007296), arXiv:1405.2593, pp.1547--1550 P9.4 (9.49)--(9.70) | Selberg 제곱, CRT, exact local factors와 마지막 residue normalization |
| [FGKMT 2018](https://arxiv.org/abs/1412.5029), DOI:10.1090/jams/876, p.102 | 실제 shifted interval, extra form, Delta와 off-tuple 합 |
| theories 27/29/30/31 | strict sharp·Euler·정수 distribution·합성식 재사용 |
| theories 44/45 | uniform integral 비교와 W-filter·정수 이동 보존 |
| [Mastrostefano, arXiv:1804.06290](https://arxiv.org/abs/1804.06290) | 관련 weighted m-tuple 연구; 새 finite growing-k proof 입력으로 채택하지 않음 |

마지막 문헌의 제목은 *Weighted Average Number of Prime m-tuples lying on an Admissible
k-tuple of Linear Forms*이다. 이전 theory 31에는 다른 제목이 적혀 있었다.
이는 source metadata 오류로 오류 원장에 기록했다. 그 잘못된 제목을 근거로 새로운 lemma가
검증됐다고 주장하지 않는다. 이번에는 직접 원문과 이미 감사된 finite child만 사용했다.

원문에 인쇄되지 않은 numerical growing-k 대체 정리를 표적 검색에서 찾지 못했다고 해서
전 세계에 그런 연구가 없다고 단정하지 않는다. 새로운 PDF 다운로드·Lean 설치는 필요하지 않았다.

## 5. 자동 검증

환경: Windows PowerShell, 프로젝트 루트, FGKMT Python.

~~~powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest tests.test_h1bp94g_growing_dimension -v
~~~

첫 전용 검사 **17/17 PASS, 0.065초**. helper py_compile PASS.
2개 원문·8개 선행 proof/code SHA-256을 대조했다.
시험은 정확한 endpoint, support 제거 방향, form/Delta/filter, Selberg 제곱,
signed quadratic matrix, Euler factor, 유리수 multiplier와 잘못된 입력 거부를 포함한다.

최소 k에서 1062 dps로 계산한 scalar 35개도 PASS했다.

- smooth delta 약 1.850779e-264
- sharp delta 약 9.696628e-873
- distribution을 실제 tiny exponential 대신 0.01로 과대계수한 total upper 약 0.8310063
- off-tuple 상대계수 상계의 log10 약 -993.5252

이 소수값은 설명용이며 정리는 문서의 전 범위 부등식과 exact 유리수 비교에 근거한다.
k개 배열이나 2^k 정수, X/Y/T0/Delta, 실제 소수 목록은 생성하지 않았다.
parent 동기화 뒤 표적 회귀 **98/98 PASS, 0.477초**, 전체 unittest
**466/466 PASS, 64.444초**를 확인했다. 전체 회귀는 승인된 정상 로컬 권한으로
FGKMT Python을 사용했으며 actual 실험은 실행하지 않았다.
T1의 66행 상태·source hash·DAG와 root 비승격 검사도 통과했다.
git diff --check는 exit 0이었다. Git의 LF/CRLF 안내는 실패가 아니며 내용을 바꾸지 않았다.
문서 첫 검사에서 tau 표기가 잘못된 q 링크로 해석되는 1건을 찾아 수식 표기로 수정했다.
재검사 결과 18개 파일의 strict UTF-8·control character·수식 구분자, JSON 4개,
로컬 링크 132개에서 issue 0이었다. 관련 Python 5개 py_compile도 PASS했다.

## 6. 다음 권장 작업

| 순서 | 내용 | 이유 | 계획용 시간 | 사용자 절차 |
|---|---|---|---:|---|
| 1 | H1b-NORM 공통 singular-series·lambda·weight·tau·u | 세 moment를 같은 점수·확률 기준으로 연결 | 2--6시간; 검산 수초--수분 | 별도 수행절차 필요없음 |
| 2 | actual dependency 가지치기 | P95 등 일반 정리 의무와 실제 필요한 경로를 구분 | 1--2시간 | 별도 수행절차 필요없음 |
| 3 | 남은 PAP/UB·hypergraph probability·arbitrary-X rate | 전체 X_cert의 아직 열린 관문 | source 감사 후 재산정 | 현재 별도 수행절차 필요없음 |

시간은 조사·증명 계획 추정이며 그만큼 CPU를 연속 점유한다는 뜻이 아니다.
현재 새 actual runner, package 설치, figure QA 요청은 없다.
필수 원문이나 장시간 계산이 필요해지면 환경·명령·예상시간·회신 항목을 안내하고 요청한다.
