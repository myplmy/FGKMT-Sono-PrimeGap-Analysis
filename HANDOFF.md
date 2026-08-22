# FGKMT-Sono Prime Gap Analysis 핸드오프

## 현재 상태

- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 단계: `P0 / PREPARATION_ONLY`
- 실제 실험: 미실행
- 외부 maximal-gap 데이터: 미취득
- 계산 결과·그래프·통계 보고서: 없음
- 다음 필수 게이트: 사용자에게 연구 이해를 설명하고 명시적 실행 허가 받기

사용자의 실행 허가 전에는 데이터 다운로드, raw/validated dataset 생성, maximal-gap 계산, fitting, envelope 계산, 그래프 생성 또는 `test_result/` 결과 작성을 하지 않는다.

## 이 연구의 목적과 방법

검증된 maximal prime-gap record를 사용해 실제 maximal gap \(G(x)\)를 FGMT/FMT large-gap scale

\[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x}
\]

로 정규화하고,

\[
H(x)=\frac{G(x)}{F(x)},\qquad
Q(x)=\frac{H(x)}{2.0\times10^{-17}}
\]

의 유한 데이터 궤적, record interval별 최소값, global running minimum과 local envelope를 계산하는 경험적 비교 연구다. Sono의 \(2.0\times10^{-17}\)은 관측 극한의 예상값이 아니라 충분히 큰 \(X\)에 대한 증명된 보수적 explicit constant다. 유한 계산은 정리를 증명하거나 반증하지 않는다.

### 핵심 수학 계약

\(\log_k\)의 아래 첨자는 밑이 아니라 자연로그의 반복 횟수다.

\[
\log_k(x)=\underbrace{\ln(\ln(\cdots\ln(x)\cdots))}_{\ln\text{을 }k\text{회 반복}}.
\]

특히

\[
\log_2(x)=\ln(\ln x),\quad
\log_3(x)=\ln(\ln(\ln x)),\quad
\log_4(x)=\ln(\ln(\ln(\ln x))).
\]

`math.log(x, 2|3|4)`와 같은 base-\(k\) 구현은 production 계산에서 금지한다. 정본은 `source/definitions.py`다.

### 두 경계 정의

- `G_end(x)`: 끝 소수 \(\le x\). Sono 직접 비교의 주 결과.
- `G_start(x)`: 시작 소수 \(\le x\). FGMT 원 논문 호환 보조 결과.

두 정의는 동일 파이프라인에서 별도 산출하며 한 envelope에 섞지 않는다. 모든 표·그래프·schema에 `boundary_mode`를 기록한다.

### 분석 시작점과 envelope

- \(x=16\): \(\log_4x\)가 실수로 정의되는 최소 정수지만 \(F(x)<0\); domain 진단 전용.
- `X_SCALE_POSITIVE_MIN = 3_814_280`: \(F(x)>0\)인 theorem-scale 비교의 최소 정수.
- record 점프 위치를 \(a_i\)라 하면 정수 interval \([a_i,a_{i+1}-1]\)의 최소값은 양의 scale 구간에서 \(g_i/F(a_{i+1}-1)\).
- 마지막 record는 확인된 exhaustive limit까지만 닫는다.
- global running minimum은 정의상 단조 비증가한다. 요동이나 상승 추세는 log-bin/rolling local envelope로 별도 분석한다.

## 완료된 준비

- `article/`의 PDF 9편(총 253쪽) 검토 및 `docs/review/`에 논문별·종합 분석 작성
- Sono 2025 원문에서 iterated-log 정의, end-bounded \(G_k\), explicit constant의 계보를 직접 확인
- Kourbatov-Wolf 2020에서 \(H=1\) empirical 참고선의 2차 문헌 근거 확인
- Feliksiak 2021 preprint의 fitted \(LB/F\) 선행 시도를 확인했으나, 비심사·논증 문제로 theorem이나 데이터 정본으로 채택하지 않음
- `docs/METHODS.md`를 이번 연구의 계산·데이터·해석 정본으로 정비
- `CLAUDE.md`를 Codex용 루트 `AGENTS.md`로 전환
- 사용자 수정에 따라 문헌 리뷰 정본 경로를 `docs/review/`로 통일
- 작업지시서에 iterated-log 중요 수정사항과 재생성 규칙 명시
- 지정 Conda 환경과 고정 버전 requirements 검증
- 데이터 비의존 정본 `source/definitions.py` 및 preflight tests 추가

## 검증 결과

사용한 executable:

```text
W:\miniforge3\envs\FGKMT\python.exe
Python 3.11.16
```

실행 명령:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -m unittest discover -s tests -v
```

결과:

```text
7 tests passed
source/ forbidden base-k log calls: 0
```

감사 시작 당시 `source/`와 `test_result/`에는 기존 파일이 각각 0개였다. 잘못된 로그 정의로 계산된 기존 결과가 없으므로 폐기 또는 재생성 대상도 없다. 현재 `test_result/`에도 실험 결과가 없다.

## 정본 파일

1. `AGENTS.md`
2. `연구 작업지시서_ FGMT-FMT 대형 소수간격 하한과 실제 maximal prime gap의 경험적 비교 분석.md`
3. `docs/METHODS.md`
4. `docs/method/환경_준비_기록.md`
5. `docs/review/00_문헌_종합_분석.md`
6. `docs/review/01_...09_...md`
7. `source/definitions.py`
8. `tests/test_iterated_logs.py`

## 사용자 확인이 필요한 방법론

실험 허가와 함께 다음 두 항목의 목적 일치를 확인한다.

1. Sono 직접 비교는 `end`를 주 정의로, FGMT 호환 비교는 `start`를 보조 정의로 동시에 산출한다.
2. \(16\le x<3,814,280\)은 domain 진단으로 분리하고, \(H\), \(Q\), interval/global envelope는 \(x=3,814,280\)부터 계산한다.

## 허가 후 첫 행동

1. preflight tests와 source 정적 감사를 다시 실행한다.
2. `test_plan/`에 데이터 출처 후보, retrieval 시각, hash, 경계 의미, exhaustive range, 성공·중단 기준을 먼저 기록한다.
3. 최신 maximal-gap 원자료 출처와 coverage를 확인하고 사용자 승인 범위 안에서 원본을 `datas/raw/`에 보존한다.
4. 산술·순서·출처 간 중첩·endpoint probable-prime·coverage 검증을 통과한 뒤에만 계산으로 이동한다.
5. `end`와 `start`를 분리해 \(F,H,Q\), interval minimum, running/local envelope를 계산한다.
6. 표를 먼저 검증한 뒤 그래프와 해석을 생성한다.

## 저장소 주의사항

- 현재 저장소는 `main`에 첫 commit이 없고 파일들이 untracked 상태다.
- 사용자 요청 없이 commit, push, PR, issue 또는 외부 게시를 하지 않는다.
- `git add .`와 `git add -A`를 사용하지 않는다.
- PDF 원본과 향후 raw dataset을 수정하지 않는다.
- 패키지 설치·제거·업그레이드는 별도 허가 없이는 하지 않는다.

## 재개용 프롬프트

```text
Z:\FGKMT-Sono-PrimeGap-Analysis에서 FGKMT-Sono maximal prime-gap 연구를 계속한다.
먼저 AGENTS.md, HANDOFF.md, docs/METHODS.md를 읽고 현재 PREPARATION_ONLY 승인 경계를 지킨다.
log_k(x)는 base-k가 아니라 ln을 k회 반복한 iterated natural logarithm이다.
W:\miniforge3\envs\FGKMT\python.exe로 tests를 재실행하고 source/의 base-k 호출 0건을 확인한다.
사용자가 실제 실험을 명시적으로 허가하지 않았다면 데이터 취득이나 본 계산을 시작하지 말고,
end-bounded 주 분석 + start-bounded 보조 분석 및 x=3,814,280 시작점에 대한 목적 일치를 먼저 확인한다.
```
