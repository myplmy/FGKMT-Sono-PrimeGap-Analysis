# FGKMT-Sono maximal prime gap 비교 방법론

## 0. 문서 상태와 실행 경계

이 문서는 `Z:\FGKMT-Sono-PrimeGap-Analysis`에서 수행할 대형 소수간격 비교 실험의 방법론 정본이다.

- 현재 단계: P003/P004 본체와 P005–P012-B 단계별 실제 실행·사후 검증 완료; P012-B 사용자 시각 QA 대기
- 완료 승인 범위: P003/P004 분석, P005 calibration, P006–P012-B 실제 실행과 사후 검증
- 현재 비승인·미실행 범위: P010B large-range acceleration, 신규 P013 actual, 외부 게시, commit/push/PR
- 다음 사용자 단계: P012-B PNG 두 장을 시각검사한다. 다음 연구 구현은 P010B compressed absolute coverage와 P013 검정력 설계다.

모든 실패·성공 로그는 독립 run id로 보존하며 기존 산출물을 덮어쓰지 않는다.

## 1. 연구 목적

검증된 maximal prime-gap records를 이용해 end-bounded 실제 maximal gap

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
\]

을 복원하고 FGKMT large-gap asymptotic scale에 대한 \(H(x)=G(x)/F(x)\)의 변화와 lower envelope를 분석한다. record 사이의 감소, 새 record에서의 회복, interval minima, global running minimum과 local empirical envelope, Wolf 계열 경험적 관찰, Sono explicit constant와의 정량적 격차를 조사한다.

유한 계산으로 FGKMT 또는 Sono의 무한 범위 정리를 재증명·검증하지 않으며, 계산 범위의 부등식을 모든 더 큰 \(x\)로 일반화하지 않는다. 관찰 패턴은 empirical statement로 분리하고, 후속 추측·명시적 임계값·이론 연구 후보로만 제안한다.

자연로그와 반복로그를 다음과 같이 정의한다.

\[
\log_1 x=\log x,\quad
\log_2 x=\log\log x,\quad
\log_3 x=\log\log\log x,\quad
\log_4 x=\log\log\log\log x.
\]

여기서 아래 첨자 \(k\)는 로그의 밑이 아니라 자연로그를 적용한 횟수다. 즉,

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 반복}}
\]

이며, 특히

\[
\log_2(x)=\ln(\ln x),\quad
\log_3(x)=\ln(\ln(\ln x)),\quad
\log_4(x)=\ln(\ln(\ln(\ln x))).
\]

FGKMT scale은

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

로 둔다. 주 분석량은

\[
H(x)=\frac{G(x)}{F(x)},\qquad
Q(x)=\frac{H(x)}{c_{\mathrm{Sono}}},\qquad
c_{\mathrm{Sono}}=2.0\times10^{-17}
\]

이다.

### 1.1 반복로그 구현 계약과 사전검증

정본 구현은 `source/definitions.py`의 `iter_log`와 `F`다. 최소 작업 정밀도는 `mpmath` 50 decimal digits로 고정한다.

```python
import mpmath as mp

mp.mp.dps = 50

def iter_log(x, n):
    value = mp.mpf(x)
    for _ in range(n):
        value = mp.log(value)
    return value

def F(x):
    log1 = iter_log(x, 1)
    log2 = iter_log(x, 2)
    log3 = iter_log(x, 3)
    log4 = iter_log(x, 4)
    return log1 * log2 * log4 / log3
```

다음은 base-\(k\) 로그이므로 연구 계산 코드에서 금지한다.

```python
math.log(x, 2)
math.log(x, 3)
math.log(x, 4)
numpy.log2(x)
```

단위시험에서 위 base-\(k\) 값을 negative control로 계산해 iterated natural logarithm과 서로 다름을 검증하는 경우만 예외다. 실제 데이터 단계로 가기 전에 반드시 아래 명령을 통과시킨다.

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest discover -s tests -v
```

필수 preflight 판정은 다음과 같다.

1. `iter_log(x, 2|3|4)`가 직접 중첩한 `mp.log`와 고정밀도로 일치한다.
2. 위 값이 밑이 2, 3, 4인 로그와 각각 다르다.
3. `F(x)`가 풀어 쓴 식과 일치한다.
4. `source/`에서 base-\(k\) 로그 호출이 발견되지 않는다.
5. `x=16`의 음의 \(F\)와 `X_SCALE_POSITIVE_MIN=3_814_280`의 양의 \(F\)를 재확인한다.

정의 오류가 발견된 코드로 계산한 결과는 부분 수정하지 않는다. 해당 실행의 `F`, `H`, Sono ratio \(Q\), interval-wise minimum, running minimum, 그래프와 통계 요약을 모두 무효 처리한 뒤 교정된 코드와 동일 입력으로 전부 재생성한다.

## 2. 정리 계보와 상수의 의미

### 2.1 FGKMT와 FMT를 구분한다

- Ford-Green-Konyagin-Maynard-Tao(2018)는 `LONG GAPS BETWEEN PRIMES`에서 start-bounded \(G(X)\)에 대해 \(G(X)\gg F(X)\)를 증명했다.
- Sono가 수치화한 \(c_{\mathrm{LG}}\)는 Ford-Maynard-Tao의 `Chains of large gaps between primes`에 제시된 \(G_k(X)\) 정리의 explicit constant이다.
- \(k=1\)이면 동일한 함수형 scale을 갖지만, “Sono가 FGKMT 5인 논문의 숨은 상수를 그대로 계산했다”고 쓰지 않는다.

Sono의 2025년 출판본은 [An explicit lower bound for large gaps between some consecutive primes](https://doi.org/10.4418/2025.80.2.2)이며, 현재 `article/`의 6번째 PDF와 `docs/review/06_Sono_2025.md`에서 직접 검토했다.

### 2.2 상수와 threshold

Sono 결과는 고정된 \(k\)와 충분히 큰 \(X\)에 대해

\[
G_k(X)\ge \frac{c_{\mathrm{LG}}}{k^2}F(X),
\qquad c_{\mathrm{LG}}\ge2.0\times10^{-17}
\]

형태이다.

- `2.0e-17`은 경험적 예상값이나 극한값이 아니라 증명에서 확보한 보수적 상수이다.
- 정리의 문구는 “for any sufficiently large X”이며, 출판본에 바로 사용할 수 있는 수치 \(X_0\)가 제시되어 있지 않다.
- 유한 데이터에서 \(H(x)<c_{\mathrm{Sono}}\)가 나와도 정의와 계산이 맞다면 정리 반례가 아니라 그 \(x\)가 보장 구간 밖이라는 정보이다.
- 유한 데이터에서 항상 \(H(x)\ge c_{\mathrm{Sono}}\)여도 정리를 계산으로 입증한 것이 아니다.

### 2.3 Wolf 기준선의 지위

\(H=1\)은 작업지시서에 따른 경험적 참고선으로만 표시한다. Kourbatov-Wolf 2020(p. 2)은 FGKMT 함수형 lower bound가 계산상 \(A=1\)로 성립한다는 2차 진술을 제공하지만 exact \(H\) envelope나 극한을 입증하지 않는다. 따라서 그래프 범례는 `Kourbatov-Wolf 2020 empirical reference H=1 (not a theorem)`처럼 쓰고, “Wolf가 \(c=1\)을 증명했다”거나 “\(H\to1\)을 예측했다”고 단정하지 않는다.

## 3. maximal gap 경계 정의

record gap을 시작 소수 \(s_i\), gap \(g_i\), 끝 소수 \(e_i=s_i+g_i\)로 기록한다.

### 3.1 canonical end-bounded 정의

사용자가 지정한 연구 정본이며 Sono의 \(G_1(X)\), Kourbatov-Wolf 2019의 정의와 맞춘다.

\[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n).
\]

record \(i\)의 점프 위치는 \(e_i\)이다.

### 3.2 source와 분석 경계의 변환

- Prime Gap List Project의 high-watermark 표는 작은 start prime이 있는지로 record를 배열한다.
- 원본의 `startprime`과 `gapsize`로 \(e_i=s_i+g_i\)를 계산한 뒤 분석 jump를 end prime으로 변환한다.
- 모든 표·그래프·요약에 `boundary_mode=end`와 `G definition: end_prime <= x`를 기록한다.
- start-bounded 보조 계열은 P004 전용 파일과 변수명으로 격리하고 canonical end-bounded 계열을 교체하지 않는다.

## 4. 반복로그 도메인과 분석 시작점

\(F(x)\)는 실수식으로는 정수 \(x=16\)부터 계산할 수 있지만, 이때 \(\log_4x<0\)이므로 양의 lower-bound scale 비교에는 부적합하다. \(F(x)>0\)이 되는 조건은

\[
\log_4x>0
\iff x>e^{e^e}=3814279.1047602205\ldots
\]

이다. 따라서

```text
X_SCALE_POSITIVE_MIN = 3_814_280
```

을 theorem-scale 분석의 최소 정수로 고정한다.

- `16 <= x < 3_814_280`은 반복로그 도메인 진단표에만 포함할 수 있다.
- 이 초기 구간을 \(H\), \(Q\), global running minimum에 포함하지 않는다.
- \(\log_4x=0\) 부근의 부호 변화와 작은 분모가 전체 결과를 지배하지 않도록 한다.
- 양의 scale 구간에서 \(F(x)\)의 단조증가를 수식 검토와 수치 단위시험으로 모두 확인한다.

## 5. interval-wise minimum과 envelope

점프 위치 \(e_i\)에 대해

\[
e_i\le x<e_{i+1}\quad\Longrightarrow\quad G(x)=g_i.
\]

정수 구간을 양의 scale 시작점으로 자른다.

\[
\ell_i=\max(e_i, X_{\mathrm{scale+}}),\qquad
r_i=e_{i+1}-1.
\]

\(\ell_i\le r_i\)이고 \(F\)가 증가하는 구간에서 정확한 interval minimum은

\[
H_i^{\min}=\frac{g_i}{F(r_i)}
\]

여기서 “정확한 minimum”은 프로젝트가 고정한 정수 격자 `x in Z`에 대한 말이다. 논문의 변수를 실수 `X` 전체로 연장하면 plateau는 `[e_i,e_(i+1))`이고 오른쪽 끝이 포함되지 않으므로 minimum은 일반적으로 달성되지 않는다. 그 경우 대응하는 양은
`inf H(X) = g_i/F(e_(i+1))`, 즉 `X -> e_(i+1)-`의 극한이다. 현재 코드·CSV·log-bin은 일관되게 정수 domain을 사용한다.

마지막 record는 다음 record가 없으므로 `verified_exhaustive_limit` 또는 사용자가 승인한 분석 상한까지만 닫는다. 검증범위를 넘어 무한히 연장하지 않는다.

running minimum은

\[
M(X)=\min_{X_{\mathrm{scale+}}\le x\le X}H(x)
\]

로 정의한다. 정의상 \(M(X)\)는 단조 비증가한다. 따라서 “증가”나 “상하 요동”은 global running minimum의 가능한 패턴이 아니다. 1차 분석에서는 interval minima 궤적과 ln H 대 ln x의 descriptive slope·correlation을 함께 산출한다.

P003에서는 다음 두 local envelope를 실행 전에 고정한다.

1. 정수 decade log-bin

\[
(10^k,10^{k+1}]\cap[3{,}814{,}280,10^{20}]
\]

즉 정수 범위 `[10^k+1,10^(k+1)]`을 사용하고 첫·마지막 bin은 분석 범위로 clip한다. 각 bin과 겹치는 모든 end-bounded interval에서 겹침의 오른쪽 끝을 평가한 뒤 가장 작은 `H`를 정확한 bin minimum으로 선택한다.

2. 고정 record-window rolling minimum

interval-minimum sequence에서 직전 `w`개 record interval의 최소를 계산하며 `w=5,10,20`을 주 window로 고정한다. window가 완전히 찬 지점부터만 산출한다. 오래된 최저값이 window 밖으로 빠지면 이 local 지표는 상승할 수 있다.

고정 log-width robust quantile은 P003 정본 산출물에 포함하지 않고 후속 민감도 분석 후보로 남긴다. global running minimum에서는 새 최저치와 plateau만 해석한다.

### 5.1 결과 표의 경계 필드

각 interval 행에는 gap의 `start_prime`, `end_prime`, canonical `[x_left,x_right]`, `F(x_left)`, `F(x_right)`, `H(x_left)`, `H_interval_min`을 함께 저장한다. `start_prime`은 provenance와 사람이 읽는 식별자일 뿐 interval 시작점으로 사용하지 않는다.

Sono 원문의 `G_1(X)`는 `end_prime <= X`여서 현재 함수와 정확히 일치한다. FGKMT 2018 원문의 `G(X)`는 `start_prime <= X`이므로 유한 계단함수는 다르다. 현재 연구는 end-bounded `G`와 Sono를 직접 비교하고, FGKMT는 동일한 large-gap scale의 이론적 출처로 구분해 비교한다.

## 6. 데이터 정책

### 6.1 우선순위

1. 정본 입력: [Prime Gap List Project GitHub 저장소](https://github.com/primegap-list-project/prime-gap-list)의 commit-pinned `allgaps.sql`
2. 참고 표: `prime-gaps-high-watermarks` 웹페이지(입력으로 사용하지 않음)
3. exhaustive limit: `fully-analyzed` 페이지와 연결된 원 발표
4. Oliveira e Silva-Herzog-Pardi 자료의 중첩 범위 교차검증

준비 시점(2026-08-22 UTC)에 `master`는 `1a112a1387052d9ad360686313f501c01fe46b68`로 확인했다. 실제 취득 시 다시 resolve하고 그 시점의 40자 commit으로 raw URL을 고정한다. 현재 웹페이지가 명시한 exhaustive upper bound는 2026-05-08의 \(10^{20}\)이다.

전체 소수를 상한까지 다시 생성하지 않는다. 이 연구의 1차 데이터 단위는 record gap이다.

### 6.2 원본 보존

승인 후 사용할 구조는 다음과 같다.

```text
datas/
  raw/prime-gap-list-project/<commit>/
    allgaps.sql     # 다운로드 원본, 수정·덮어쓰기 금지
    schema.sql      # 같은 commit의 upstream schema
    metadata.json   # 두 파일의 commit, URL, 취득 UTC, byte 수, SHA-256
  validated/prime-gap-list-project/<commit>/
    maximal_gap_records.csv
    validation_report.json
```

각 원본에 다음 메타데이터를 남긴다.

```text
source_url
retrieved_at_utc
publisher_or_maintainer
source_version_or_date
sha256
license_or_usage_note
column_semantics
boundary_semantics
record_count
claimed_exhaustive_limit
parser_version
```

원본과 사람이 수정한 CSV를 같은 경로에 두지 않는다.

### 6.3 필수 열

정규화 데이터의 최소 schema:

```text
record_index
start_prime
gap
end_prime
source_id
source_row_id
source_commit
verified_exhaustive_limit
```

큰 정수는 float로 변환하지 않는다. CSV에서는 10진 문자열로 직렬화하고 Python `int`로 복원한다. Parquet을 추가할 경우 `int64`가 \(10^{20}\)을 담지 못하므로 decimal 또는 string schema를 명시하기 전에는 사용하지 않는다.

### 6.4 검증 항목

- `end_prime == start_prime + gap`
- `start_prime` 엄격 증가
- `end_prime` 엄격 증가
- record `gap` 엄격 증가
- published `ismax=1`과 eligible first-occurrence rows에서 독립 재구성한 high watermark의 완전 일치
- `gmpy2.next_prime(start_prime) == end_prime` 보조검사
- 중첩 출처 간 `(start_prime, gap, end_prime)` 일치
- source가 주장한 record 수와 exhaustive limit 일치
- 시작점/끝점 경계 의미를 metadata와 결과에 보존
- 미검증 확장 record와 exhaustive verified 범위를 별도 표시

probable-prime 검사만으로 exhaustive completeness를 주장하지 않는다.

## 7. 계산 정밀도

- 모든 로그의 밑은 \(e\)이다.
- record 소수는 Python `int`로 유지한다.
- 반복로그와 비율은 `mpmath`로 계산하고 작업 정밀도(`mp.dps`)를 결과 metadata에 기록한다.
- 정본 50-dps 계산은 `source.definitions.F/H`를 호출하지 않는 별도 100-dps 직접 중첩식으로 전수 교차검증한다. float64를 사용할 경우 진단값일 뿐 정본으로 삼지 않는다.
- CSV에는 표시용 반올림 값과 재계산 가능한 고정밀 문자열을 구분한다.
- Sono 대비 배수 \(Q\)는 매우 크므로 선형축과 로그축을 혼동하지 않는다.

## 8. 재현 가능한 단계

각 단계는 독립적으로 재실행 가능해야 하며, 이전 단계의 hash를 입력 metadata에 기록한다.

### P0 - 준비(완료)

- 작업지시서 검토
- PDF 9편 분석
- 정의 충돌과 도메인 교정
- Conda 환경 검증
- iterated-log 정본 모듈과 negative-control 단위시험 검증
- 기존 코드와 결과의 base-\(k\) 오염 여부 정적 감사
- GitHub allgaps.sql 제한 parser, schema.sql 검증, immutable acquisition, end-bounded interval/jump 분석 코드 작성
- toy record 기반 parser·high-watermark·interval·승인 gate 단위시험
- P003 실행 승인, 계획 고정과 preflight 완료

### P1 - 데이터 취득(완료)

- `master`를 40자 commit으로 resolve
- commit-pinned raw URL에서 allgaps.sql과 schema.sql 다운로드
- 두 raw source와 같은 commit 디렉터리에 hash/retrieval metadata 기록

### P2 - 데이터 검증(완료)

- schema 열 순서 검증과 row 정규화
- record 및 endpoint 산술 검증
- `ismax`와 독립 high-watermark 재구성 대조
- external exhaustive coverage provenance와 record count 확인
- OEIS 84개 공개표현과 Oliveira 별도 계산자료 75개 중첩 record 교차검증

### P3 - 수학 계산(완료)

- `log1`-`log4`, `F`, end-bounded `G`, `H`, `Q`
- end-prime jump interval minimum과 record recovery factor
- global running minimum, interval-minimum trajectory와 descriptive log-log trend
- `(10^k,10^(k+1)]` exact log-bin minimum
- full trailing record-window `w=5,10,20` rolling local envelope와 100-dps 전수검증

### P4 - 산출물(완료; 사용자 시각 QA 완료)

- 큰 정수를 10진 문자열로 보존한 핵심 통계 CSV
- end-bounded trajectory, interval minimum, running minimum, jump recovery 그래프
- Sono 및 `H=1` 참고선
- Cramér/Wolf 계열 \(\log^2x\) trend와 보조 비교
- 8종 PNG/PDF 16개 생성 및 파일 존재 자동검증; 사용자 시각 판정 완료

### P5 - 해석과 중복성 검토(완료)

- observed, heuristic, conditional, proved를 분리
- 9편 corpus 안의 중복 여부와 추가 문헌검색 결과를 분리
- 새 패턴은 재현 결과와 독립 가설로 구분
- P003 상세 결과와 문헌 비교·후속 가설 보고서 분리 작성

## 9. 예상 산출물 위치

```text
source/                 # 정의, source parser, provenance, validation, analysis, plotting, CLI
tests/                  # 데이터 비의존 및 toy-record preflight 단위시험
test_plan/P003_*.md     # 전체 실행 전 목적, source, gate, 성공/중단 기준
datas/raw/prime-gap-list-project/<commit>/ # 승인 후 immutable raw + schema + metadata
datas/validated/prime-gap-list-project/<commit>/
test_result/run_<run-id>/
  tables/
  figures/
  summary.json
  verification_report.json
  cross_validation/
  tables/log10_bin_minima.csv
  tables/rolling_local_envelope_w5.csv
  tables/rolling_local_envelope_w10.csv
  tables/rolling_local_envelope_w20.csv
docs/review/            # 이번 연구의 문헌 리뷰 정본
docs/method/             # 세부 방법 문서
```

문헌 리뷰는 `docs/review/`에만 작성하며 유사 철자의 별도 경로를 만들지 않는다.

## 10. 필수 단위시험과 불변식

실제 데이터 계산 전에 최소한 다음을 통과해야 한다.

1. `log_2`, `log_3`, `log_4`가 직접 중첩한 자연로그와 일치
2. iterated natural logarithm이 base-\(2\), base-\(3\), base-\(4\) 로그와 다름
3. `source/`의 금지된 base-\(k\) 구현 0건
4. 반복로그 domain 및 `X_SCALE_POSITIVE_MIN == 3_814_280`
5. 양의 분석 구간에서 \(F(x)>0\)
6. 대표 구간에서 \(F(x)\) 단조증가
7. end-prime 점프 위치 toy record 정답
8. interval minimum이 brute-force 정수 열거와 일치하는 소형 사례
9. running minimum 단조 비증가
10. 마지막 record가 verified limit에서 정확히 잘림
11. 임의정밀도와 float64 교차검증 허용오차
12. 정규화 row마다 원본 line 기반 source_row_id가 보존됨
13. 모든 결과 schema와 그래프에 `boundary_mode=end`가 표시됨
14. 승인 marker 없이는 fetch/validate/analyze가 network·파일 write 전에 중단됨
15. 프로젝트 텍스트와 파일명에 잘못된 4글자 약어가 0건임
16. 실제 gap 154가 `[4,652,507,17,051,886]`을 사용하고 minimum이 `154/F(17,051,886)`임
17. 모든 저장 `F/H`와 envelope 값을 별도 100-dps 직접 중첩 자연로그 식으로 상대오차 `1e-38` 이내 대조
18. log-bin이 `(10^k,10^(k+1)]`, rolling이 full-window `w=5,10,20` 계약을 지킴

## 11. 해석 금지사항

- Sono 상수를 실제 극한 또는 예상 계수로 부르지 않는다.
- `H=1`을 증명된 Wolf bound로 부르지 않는다.
- 유한 계산을 무한 범위의 증명으로 표현하지 않는다.
- unknown \(X_0\) 아래 관측을 정리 위반으로 표현하지 않는다.
- source의 start-prime ordering을 canonical end-bounded \(G(x)\)와 혼동하지 않는다.
- `x=16`부터 계산 가능하다는 사실을 양의 lower-bound 비교 가능성과 혼동하지 않는다.
- global running minimum이 증가하거나 상하 요동한다고 해석하지 않는다.
- 최신 record와 exhaustive verified coverage를 같은 뜻으로 쓰지 않는다.
- 9편에서 동일한 검증 pipeline이 없다는 사실을 전 세계 문헌 novelty 확정으로 확대하지 않는다.
- Feliksiak preprint의 fitted \(LB/F\) 비교를 무시하고 “FGKMT scale과 record의 최초 비교”라고 주장하지 않는다.

## 12. 실행 승인 체크포인트

실험 허가 요청 시 사용자는 다음 인식이 일치하는지 확인한다.

1. canonical \(G(x)\)는 사용자가 지정한 `end_prime <= x` 정의 하나다.
2. theorem-scale envelope는 `3_814_280`부터이며, `16`부터의 앞 구간은 domain 진단뿐이다.
3. GitHub `allgaps.sql`을 commit으로 고정하고, 실제 \(G(x)\) 주장은 문서화된 exhaustive limit 안에서만 한다.
4. Sono 비교는 같은 \(F(x)\) scale의 \(k=1\) explicit 기준선이지만, FGKMT 5인 논문의 상수를 그대로 추출한 것으로 표현하지 않는다.
5. 유한 관측은 empirical result이며 asymptotic theorem의 검증이 아니다.

사용자는 2026-08-23에 위 경계와 P003 범위를 승인했다. 실제 실행 직전에는 승인 사실과 별개로 `exp-preflight`의 환경·수학·provenance·비덮어쓰기 gate를 모두 통과해야 한다.

## 13. P003 실제 실행 기록

authoritative run:

```text
run_id = 20260822T195906Z_full1e20
analysis_limit = 100000000000000000000
python = W:\miniforge3\envs\FGKMT\python.exe
working_dps = 50
verification_dps = 100
stored_relative_tolerance = 1e-38
exit_code = 0
elapsed_seconds = 7.654
```

검증 결과:

- canonical pin: `1a112a1387052d9ad360686313f501c01fe46b68`
- validated records SHA-256: `62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297`
- 64 end-bounded intervals, 63 jumps, 14 log bins
- rolling rows `w=5/10/20`: 60/55/45
- 독립 100-dps 수치 필드 1,160개 PASS, issue 0
- gap 154 interval `[4,652,507,17,051,886]` 회귀시험 PASS
- OEIS record 84/84 PASS; 독립 공개 표현으로 분류
- Oliveira e Silva 별도 계산 record 75/75 PASS; source limit `4e18`
- figure 16 files 존재, 누락 0; 사용자 시각 QA 완료

해석 정본은 `test_result/202608230503_P003_full_analysis.md`, 문헌 비교와 가설은 `docs/review/10_P003_문헌비교와_후속가설.md`다. machine summary의 `COMPUTED_NOT_INTERPRETED` 상태는 실행 시점의 사전 분리 원칙을 보존하기 위해 사후 변경하지 않는다.

## 14. P004–P008 실제 실행 기록

P004 authoritative run `20260823T075238Z_p004_sensitivity`는 전체 47 tests와 100-dps 독립 검증 3,747개를 issue 0으로 PASS했다. end/start global minimum은 같은 record 50, gap 540에서 각각 `37.81686039672168...`, `37.81686039812796...`였고 shifted log-bin 3종도 같은 global minimum을 보존했다. 상세 해석은 `test_result/202608231652_P004_sensitivity_analysis.md`다.

P004 실행기는 기존 `source.cli preflight` → 전체 unit tests → 분석 → 독립 verifier를 직렬로 실행하고 첫 실패에서 중단한다. 자동 스크립트가 정의·환경·hash·toy 회귀·수치를 1차로 검증하고, Codex는 source semantics·문헌 적용 범위·해석 라벨·graph visual QA처럼 자동화하기 어려운 부분만 2차 점검한다.

P005에서는 `sethtroisi/prime-gap`이 `m * P#/d` 주변 탐색 도구임을 확인했다. Rank 85→86 일반 x-범위 exhaustive 인증과 동일하지 않으므로 WSL-native CPU-only shell은 official correctness, 1/2/4/8-thread hash 일치와 작은 calibration만 수행했다. `20260824T054203Z` bounded calibration은 PASS했지만 full exhaustive 실행은 coverage certificate와 현실적 계산계획이 생길 때까지 금지한다.

P006에서는 canonical plateau `[e_k,e_(k+1))`와 recurrence exposure `{p_n:s_k<=p_n<s_(k+1)}`를 분리한다. Windows NumPy segmented sieve가 모든 consecutive gap을 직접 생성하고, 최초 발생 포함 rate `M/N`과 최초 이후 rate `C/(N-1)`를 계산한다. `[2,10^8]` pilot과 `[2,10^9]` full은 모두 PASS했고 full의 complete/censored plateau는 29/1이다. figure 3개는 2026-08-26 사용자 시각 QA도 PASS했다.

P007은 start-bounded `gap>=1856` count의 residue-state dual certificate를 floating LP로 발견하고 exact integer/Fraction arithmetic으로 모든 constraint를 재검증한다. modulus 30/210/2310 비교는 PASS했다. modulus-2310 저장 total upper bound는 `439161464927854179`이지만 위치 정보와 exhaustive search acceleration은 증명하지 않는다.

P008은 P007 certificate를 block-local하게 적용하고 exact prime-count 입력을 두 알고리즘으로 교차검증했다. actual four blocks는 saved verification PASS였으나 certified zero 0개다. nonempty block의 right-boundary crossing을 해결하지 않고 zero라고 판정하지 않는다.

## 15. P009/P010/P011 준비와 이론 문서 체계

P009 boundary witness는 `[a,b)`의 마지막 증명 소수 `p`, `p<n<b` 전체 합성수 coverage,
증명 소수 `q>=b`, `q-p<1856`을 검사한다. PARI/GP 2.15.4 설치와 small integer·중간
ECPP adapter의 fresh-process verification은 PASS했다. 실제 `[10^20,10^20+1000)` block은
P008 internal upper bound 0, last prime `10^20+993`, proven right prime `10^20+1071`,
거리 78을 결합해 exact certified zero PASS했다. 이는 한 block의 feasibility이며 전체
범위 가속이 아니다.

P010은 두 연구축으로 분리한다. P010A는 modulus-2310 replay와 modulus-30030
cutting-plane으로 count upper bound를 연구한다. P010B는 누락 없는 absolute candidate
mapping, boundary closure, total-cost break-even으로 실제 search acceleration을 연구한다.
count upper bound만 낮아져서는 P010B 가속이 증명되지 않는다. modulus-2310 replay는 두
exact builder와 chunk oracle, saved recheck가 PASS했지만 상한은
`439161464927854179`로 동일하다. 35,224,647 constraints의 modulus-30030 one-candidate
floating scan과 exact integer lift도 실제 PASS했고 핵심 scan은 각각 약 0.77초였다.
`M|M'`, `lambda>=0`에서 potential을 residue reduction으로 lift하면 기존 certificate가
target modulus에서도 성립한다. exact lift 자체는 같은 상한의 feasibility baseline이다.
P010A G4 actual은 seed 20,000에서 위반 제약 123개를 추가하고 4회 solve 뒤 full floating
scan 위반 0으로 수렴했다. 최종 certificate는 35,224,647 exact constraints 위반 0,
minimum slack 0이며 total upper bound를 `436001550591586306`으로 낮췄다. 이 약 0.7195%
count 개선은 absolute candidate mapping이나 search acceleration을 증명하지 않는다.

P010B direct candidate-cover verifier는 작은 half-open integer universe에서 각 start를 candidate,
exact composite factor rejection, strict window-prime rejection 중 하나로 누락 없이 분류한다.
`q=c+H`는 제거 witness가 아니며 equality `gap=H`는 candidate에 남긴다. `[1000,10000)`,
`H=20` toy에서는 candidate 69개가 exact 위험 start 69개와 일치했고 나머지 8,931개 witness
coverage도 PASS했다. 그러나 generator가 exhaustive truth를 사용하므로 acceleration은
BLOCKED다. 실제 승격에는 non-circular absolute generator, compressed coverage, PARI
certificate adapter, survivor search와 동일 baseline의 5회 이상 total-cost 비교가 필요하다.

P011은 P006 recurrence count를 leave-plateau-out binomial reference와 비교하는 경험적
진단이다. exact binomial, 고정 seed Monte Carlo, BH 보정을 사용하지만 record 선택편향,
비독립성, nonstationarity 때문에 theorem evidence로 해석하지 않는다. 실제 pilot은
terminal/saved PASS했지만 primary 관측 9 대 기대 109.079로 enrichment를 지지하지 않고
global stationary null의 부적합을 드러냈다. 두 figure는 사용자 시각 QA PASS다. P012는
log-bin별 gap 발생 수를 고정하고 forced first record를 제거한 stratified hypergeometric
null이다. 사용자는 `[2,10^9]` 개발/`[10^9,10^10]` holdout 분리, 0.5-decade primary와
두 shifted sensitivity, two-sided family max-abs-z primary, seed `20260827`, 100,000회를
사전 승인했다. 첫 P012-A actual은 조건부 분산 0인 7개 primary row의 올바른
`standardized_residual_z=None`을 plotting이 `float`로 강제해 실패했다. 이 값은 z=0이
아니므로 통계 계산은 바꾸지 않는다. r2 residual figure는 P011 bar를 유지하면서 해당 P012
bar를 생략하고 `variance=0; z undefined` x marker를 표시한다. r2 actual과 saved full
recomputation은 PASS했다. primary 관측 9 대 stratified 기대 8.5874, family p 0.21945이고
shifted family p도 0.71354·0.49280으로 P011 stationary 과대예측이 크게 줄었다. 모든 scheme의
enrichment BH q는 1.0이다. 거의 모든 row가 LOW_INFORMATION이므로 이는 recurrence 구조
부재나 null 정당성 증명이 아니다. 사용자는 r2 figure 시각 QA도 PASS했다. P012 계약은
`test_plan/P012_statistical_contract_v1.json`의 SHA-256
`1c79316de685bbc40ba3c5fc49e23b1abec328bbf07dfc218e27d74e5d82000d`로 동결했다.

P012-B는 P006/P011 개발 table을 재사용하지 않고 `[10^9,10^10)`의 모든 consecutive gap
start를 range-only segmented sieve로 생성한다. canonical record metadata에서 record start와
다음 record start가 모두 holdout 안인 complete records `31–34`만 선택하고 왼쪽 continuation과
오른쪽 censored plateau를 제외한다. pinned gap-start 수는
`pi(10^10)-pi(10^9)=404204977`이며 오른쪽 boundary prime 하나로 마지막 gap을 닫는다.
사용자 실행 `20260827T121734Z_p012b_stratified_null_holdout`은 분석과 saved full recomputation,
사후 독립 산술과 100,000회 Monte Carlo replay를 issue 0으로 통과했다. 4개 complete plateau에서
recurrence는 1건이고 primary 기대 0.497022, family p 0.093939, 최소 enrichment BH q
0.275957로 5% 기준 enrichment를 검출하지 못했다. 12/12 row가 LOW_INFORMATION이고 3개는
zero variance이므로 null 채택이나 recurrence 구조 부재로 해석하지 않는다. 자동 figure QA는
PASS했고 사용자 시각 QA는 대기 중이다. 정본 결과보고서는
`test_result/202608280019_P012B_holdout_result_analysis.md`다.

coverage-preserving compression의 finite soundness 정본은
`docs/method/theory/10_coverage_preserving_compression_정식화.md`다.
modulus 배수 exact-lift 정본은
`docs/method/theory/11_residue_certificate_modulus_lift.md`다.

이론·가설·폐기된 연결의 정본 지도는 `docs/method/theory/00_이론_가설_방법론_색인.md`다. 신규 네 이론 초안의 오류와 채택 범위는 `docs/review/17_20260826_prime-gap_통합이론_비판적_타당성검토.md`에 기록한다.

완료된 특정 실험 runner는 `test_done/`에 SHA-256과 함께 보존하고 재실행하지 않는다. 재사용 공통 runner·logging·test는 각각 `scripts/runners/`, `scripts/common/`, `scripts/tests/`에 둔다.
