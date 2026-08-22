# FGMT/FMT-Sono maximal prime gap 비교 방법론

## 0. 문서 상태와 실행 경계

이 문서는 `Z:\FGKMT-Sono-PrimeGap-Analysis`에서 수행할 대형 소수간격 비교 실험의 방법론 정본이다.

- 현재 단계: 문헌 검토, 수학적 정의 교정, 폴더 및 Python 환경 점검
- 현재 허용 범위: 문서 작성, 정적 준비, 환경 import 확인, 데이터 비의존 수학 정의와 preflight 단위시험
- 현재 금지 범위: 외부 maximal-gap 데이터 취득, 데이터 변환, 본 계산, 통계 추정, 그래프 생성, 결과 해석
- 실제 실험 시작 조건: 사용자의 명시적 실행 허가

실행 허가 전에는 결과처럼 보이는 시험 계산도 `test_result/`에 남기지 않는다.

## 1. 연구 목적

검증된 maximal prime-gap record를 이용해 실제 maximal gap과 FGMT/FMT 계열의 large-gap scale을 경험적으로 비교한다. 정리를 재증명하거나 유한 계산으로 무한 범위의 정리를 검증하려는 연구가 아니다.

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

FGMT/FMT scale은

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

로 둔다. 주 분석량은 경계 정의별

\[
H_b(x)=\frac{G_b(x)}{F(x)},\qquad
Q_b(x)=\frac{H_b(x)}{c_{\mathrm{Sono}}},\qquad
c_{\mathrm{Sono}}=2.0\times10^{-17}
\]

이다. 아래 첨자 \(b\)는 `start` 또는 `end`이다.

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

### 2.1 FGMT와 FMT를 구분한다

- Ford-Green-Konyagin-Maynard-Tao(2018)는 `LONG GAPS BETWEEN PRIMES`에서 start-bounded \(G(X)\)에 대해 \(G(X)\gg F(X)\)를 증명했다.
- Sono가 수치화한 \(c_{\mathrm{LG}}\)는 Ford-Maynard-Tao의 `Chains of large gaps between primes`에 제시된 \(G_k(X)\) 정리의 explicit constant이다.
- \(k=1\)이면 동일한 함수형 scale을 갖지만, “Sono가 FGMT 5인 논문의 숨은 상수를 그대로 계산했다”고 쓰지 않는다.

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

### 3.1 start-bounded 정의

FGMT 2018의 정의와 맞춘다.

\[
G_{\mathrm{start}}(x)=\max_{p_n\le x}(p_{n+1}-p_n).
\]

record \(i\)의 점프 위치는 \(a_i=s_i\)이다.

### 3.2 end-bounded 정의

Sono의 \(G_1(X)\), Kourbatov-Wolf 2019의 정의와 맞춘다.

\[
G_{\mathrm{end}}(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n).
\]

record \(i\)의 점프 위치는 \(a_i=e_i\)이다.

### 3.3 분석 원칙

- Sono 상수와의 직접 비교는 `end`를 주 분석으로 사용한다.
- FGMT 원 논문 및 start-prime 기반 record table과의 비교를 위해 `start`도 동일 파이프라인에서 산출한다.
- 모든 결과 파일과 그래프 제목에 `boundary_mode=start|end`를 기록한다.
- 두 정의를 혼합해 하나의 running minimum을 만들지 않는다.

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

경계 모드에 맞는 점프 위치를 \(a_i\)라 하면

\[
a_i\le x<a_{i+1}\quad\Longrightarrow\quad G_b(x)=g_i.
\]

정수 구간을 양의 scale 시작점으로 자른다.

\[
\ell_i=\max(a_i, X_{\mathrm{scale+}}),\qquad
r_i=a_{i+1}-1.
\]

\(\ell_i\le r_i\)이고 \(F\)가 증가하는 구간에서 정확한 interval minimum은

\[
H_{b,i}^{\min}=\frac{g_i}{F(r_i)}
\]

이다. 마지막 record는 다음 record가 없으므로 `verified_exhaustive_limit` 또는 사용자가 승인한 분석 상한까지만 닫는다. 검증범위를 넘어 무한히 연장하지 않는다.

running minimum은

\[
M_b(X)=\min_{X_{\mathrm{scale+}}\le x\le X}H_b(x)
\]

로 정의한다. 정의상 \(M_b(X)\)는 단조 비증가한다. 따라서 “증가”나 “상하 요동”은 global running minimum의 가능한 패턴이 아니다. 그런 장기 변화를 보려면 별도로 다음을 산출한다.

- log-bin별 minimum
- 고정 record-window rolling minimum
- interval minima \(H_{b,i}^{\min}\) 자체의 궤적

global running minimum에서는 새 최저치와 plateau만 해석한다.

## 6. 데이터 정책

### 6.1 우선순위

1. 원 출처가 명시된 최신 maximal-gap record dataset
2. exhaustive verification limit가 명시된 자료
3. Oliveira e Silva-Herzog-Pardi 자료와의 중첩 범위 교차검증
4. 독립적인 record table과의 count, 값, 범위 대조

전체 소수를 상한까지 다시 생성하지 않는다. 이 연구의 1차 데이터 단위는 record gap이다.

### 6.2 원본 보존

승인 후 사용할 구조는 다음과 같다.

```text
datas/
  raw/             # 다운로드 원본, 수정 금지
  validated/       # 정규화 및 검증 데이터
  metadata/        # 출처, checksum, 범위, 정의, 취득 시각
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
verified_exhaustive_limit
```

큰 정수는 float로 변환하지 않는다. CSV/Parquet 입력 시 문자열 또는 임의정밀도 정수로 읽은 뒤 Python `int`로 검증한다.

### 6.4 검증 항목

- `end_prime == start_prime + gap`
- `start_prime` 엄격 증가
- record `gap` 엄격 증가
- gap parity와 초기 예외 처리
- `start_prime`, `end_prime`의 probable-prime 검사(gmpy2)는 보조 검증으로 사용
- 중첩 출처 간 `(start_prime, gap, end_prime)` 일치
- source가 주장한 record 수와 exhaustive limit 일치
- 시작점/끝점 경계 의미를 metadata와 결과에 보존
- 미검증 확장 record와 exhaustive verified 범위를 별도 표시

probable-prime 검사만으로 exhaustive completeness를 주장하지 않는다.

## 7. 계산 정밀도

- 모든 로그의 밑은 \(e\)이다.
- record 소수는 Python `int`로 유지한다.
- 반복로그와 비율은 `mpmath`로 계산하고 작업 정밀도(`mp.dps`)를 결과 metadata에 기록한다.
- 현재 데이터 범위에서 float64와 고정밀 결과를 교차검증하되, float64 값을 정본으로 삼지 않는다.
- CSV에는 표시용 반올림 값과 재계산 가능한 고정밀 문자열을 구분한다.
- Sono 대비 배수 \(Q\)는 매우 크므로 선형축과 로그축을 혼동하지 않는다.

## 8. 재현 가능한 단계

각 단계는 독립적으로 재실행 가능해야 하며, 이전 단계의 hash를 입력 metadata에 기록한다.

### P0 - 준비(현재 단계)

- 작업지시서 검토
- PDF 9편 분석
- 정의 충돌과 도메인 교정
- Conda 환경 검증
- iterated-log 정본 모듈과 negative-control 단위시험 검증
- 기존 코드와 결과의 base-\(k\) 오염 여부 정적 감사
- 실행 허가 대기

### P1 - 데이터 취득(허가 후)

- 출처 및 최신성 확인
- 원본 다운로드
- hash와 retrieval metadata 기록

### P2 - 데이터 검증

- schema 정규화
- record 및 endpoint 산술 검증
- 출처 간 교차검증
- exhaustive coverage 표 작성

### P3 - 수학 계산

- `log1`-`log4`, `F`, `H_start`, `H_end`, `Q_start`, `Q_end`
- 경계 모드별 interval minimum
- global running minimum과 log-bin local envelope

### P4 - 산출물

- 핵심 통계 CSV/Parquet
- 정의별 trajectory와 envelope 그래프
- Sono 및 `H=1` 참고선
- Cramér/Wolf 계열 \(\log^2x\) trend와 보조 비교

### P5 - 해석과 중복성 검토

- observed, heuristic, conditional, proved를 분리
- 9편 corpus 안의 중복 여부와 추가 문헌검색 결과를 분리
- 새 패턴은 재현 결과와 독립 가설로 구분

## 9. 예상 산출물 위치

```text
source/                 # 사전검증 정의 모듈; 데이터 의존 모듈은 승인 후
tests/                  # 데이터 비의존 preflight 단위시험
test_plan/              # 실행 전 계획, 입력 hash, 성공/중단 기준
test_result/
  tables/
  figures/
  logs/
  summary/
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
7. start/end 점프 위치 toy record 정답
8. interval minimum이 brute-force 정수 열거와 일치하는 소형 사례
9. running minimum 단조 비증가
10. 마지막 record가 verified limit에서 정확히 잘림
11. 임의정밀도와 float64 교차검증 허용오차
12. 입력 row 순서 변경에도 정규화 결과 hash가 동일
13. 경계 모드가 모든 결과 schema와 그래프에 표시됨

## 11. 해석 금지사항

- Sono 상수를 실제 극한 또는 예상 계수로 부르지 않는다.
- `H=1`을 증명된 Wolf bound로 부르지 않는다.
- 유한 계산을 무한 범위의 증명으로 표현하지 않는다.
- unknown \(X_0\) 아래 관측을 정리 위반으로 표현하지 않는다.
- start-bounded와 end-bounded 결과를 섞지 않는다.
- `x=16`부터 계산 가능하다는 사실을 양의 lower-bound 비교 가능성과 혼동하지 않는다.
- global running minimum이 증가하거나 상하 요동한다고 해석하지 않는다.
- 최신 record와 exhaustive verified coverage를 같은 뜻으로 쓰지 않는다.
- 9편에서 동일한 검증 pipeline이 없다는 사실을 전 세계 문헌 novelty 확정으로 확대하지 않는다.
- Feliksiak preprint의 fitted \(LB/F\) 비교를 무시하고 “FGMT scale과 record의 최초 비교”라고 주장하지 않는다.

## 12. 실행 승인 체크포인트

실험 허가 요청 시 사용자가 확인할 핵심 선택은 다음 두 가지다.

1. Sono 직접 비교의 주 정의를 `end`, FGMT 호환 보조 정의를 `start`로 두는 이중 산출
2. theorem-scale envelope 시작점을 `3_814_280`으로 두고 `16`부터의 구간은 domain 진단으로 분리

사용자가 이 방법을 승인한 뒤에만 P1 이후를 수행한다.
