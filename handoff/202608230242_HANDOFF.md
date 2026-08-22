# FGKMT-Sono Prime Gap Analysis 핸드오프

## 1. 현재 상태

- 작업 루트: Z:\FGKMT-Sono-PrimeGap-Analysis
- 상태: P0 / PREPARATION_ONLY / WAITING_FOR_USER_APPROVAL
- 실제 dataset 다운로드: 0건
- validated dataset: 0건
- 실제 maximal-gap 분석: 0건
- test_result 결과 run: 0건
- commit, push, PR: 수행하지 않음

코드·문서·합성 fixture 검증은 준비되었다. 사용자가 연구 목적·정의·데이터 범위·수행방법을 확인하고 실제 실행을 명시적으로 허가하기 전에는 allgaps.sql 취득, 실제 validation, 분석, 결과 표·그래프 생성을 시작하지 않는다.

## 2. ChatGPT가 이해한 연구

검증된 maximal prime-gap records로

[
G(x)=\max_{p_{n+1}\le x}(p_{n+1}-p_n)
]

를 복원한다. canonical jump는 gap의 시작 소수가 아니라 끝 소수 p_(n+1)에서 발생한다.

[
F(x)=\frac{\log x\,\log_2x\,\log_4x}{\log_3x},
\qquad
H(x)=\frac{G(x)}{F(x)}
]

이며 log_k(x)는 자연로그를 k회 반복한 값이다. 밑이 k인 로그가 아니다. F(x)>0인 최소 정수 3,814,280부터 theorem-scale 비교를 시작한다.

분석 대상은 다음과 같다.

- 고정 maximal-gap record interval에서 F가 증가함에 따라 H가 감소하는 궤적
- 새 record end에서 H가 회복하는 크기와 recovery factor
- interval별 정확한 최소 H와 global running minimum
- interval minima의 장기 descriptive log-log trend
- Wolf 계열 H=1 경험적 참고선과 실제 데이터의 관계
- Sono explicit constant 2e-17에 대한 H/(2e-17) 배수와 그 변화
- 보조적인 gap/ln(x)^2 Cramér 정규화
- 특이 구조와 후속 추측·explicit-threshold 연구 후보

이 연구는 유한 계산으로 FGKMT 또는 Sono의 무한 범위 정리를 재증명·검증·반증하려는 것이 아니다. Sono의 수치는 empirical limit가 아니라 보수적인 explicit lower-bound constant다. 또한 Sono는 Ford–Maynard–Tao의 Chains 정리를 explicit화했으며, k=1에서 FGKMT와 같은 함수형 scale이 나타나더라도 다섯 저자 논문의 숨은 상수를 그대로 산출한 것으로 표현하지 않는다.

## 3. 완료한 작업

### 수학·문서

- 저자 약칭을 저장소 전체에서 FGKMT로 통일
- 연구 작업지시서 파일명을 FGKMT-Sono로 변경하고 사용자 지정 목적과 end-bounded G를 정본화
- iterated-log 정의, 잘못된 base-k 구현 금지, 재생성 규칙 반영
- docs/METHODS.md를 source provenance, end-bounded interval, 승인 gate, 산출물 구조와 일치시킴
- article의 현재 PDF 9편에 대한 문헌별 분석과 종합 분석을 docs/review에 유지·정합화
- README.md, datas/README.md, test_plan/P001 문서 작성

### 코드

- source/definitions.py: iterated log, F, H, Sono bound와 ratio
- source/provenance.py: 승인 gate, 원격 HEAD resolve, commit-pinned allgaps.sql·schema.sql 취득, 파일별 hash metadata
- source/prime_gap_list.py: SQL 비실행 제한 parser, upstream 6종 start-prime 표현, schema 열 순서 검증, eligible first occurrence와 ismax 독립 대조, consecutive-prime 검증
- source/analysis.py: end-bounded interval, exact interval minimum, running minimum, record jump recovery, Sono/Cramér ratio, descriptive log-log trend
- source/pipeline.py: 큰 정수 문자열 보존, validation report, input/code/environment provenance, 비덮어쓰기 CSV·JSON·plot pipeline
- source/plots.py: H trajectory, interval minima, running minimum, Sono ratio, Cramér ratio, record recovery를 PNG와 PDF로 생성
- source/cli.py: preflight, status, fetch, validate, analyze, run 하위 명령과 mutating-stage 승인 gate
- run_experiment.ps1: 지정 Python, Approved switch, run-id별 stdout/stderr log, 실패 코드 보존

### Codex 작업 환경

- 루트 정본은 AGENTS.md로 유지
- .claude/project.json과 16개 기존 스킬 폴더를 이번 연구에 맞게 수정
- .claude 스킬과 보조 자료를 삭제하지 않고 Codex 발견 경로 .agents/skills에 미러링
- ai_dev_tool을 계산 함정, 핸드오프, 실험 착수 규약으로 축약
- ai_dev_tool/verify_skill_mirror.ps1 추가

## 4. 실제로 하지 않은 일

- allgaps.sql 또는 schema.sql 다운로드
- datas/raw와 datas/validated 실제 산출물 생성
- 실제 maximal-gap record count, H, minimum, trend, Sono ratio 계산
- test_result의 실제 표, 그림, summary 생성
- 연구 결론 또는 새로운 수론적 추측 확정
- 패키지 설치·제거·업그레이드
- git commit, push, PR, issue 생성

합성 fixture 테스트는 운영체제 임시 디렉터리에서만 수행되어 저장소 연구 결과를 만들지 않았다.

## 5. 데이터 원천 상태

- canonical repository: https://github.com/primegap-list-project/prime-gap-list
- 승인 후 입력: 같은 40자리 commit의 allgaps.sql과 schema.sql
- 읽기 전용으로 재확인한 master HEAD: 1a112a1387052d9ad360686313f501c01fe46b68
- 확인 시각: 2026-08-22T17:37:48Z
- high-watermark 참고: https://primegap-list-project.github.io/lists/prime-gaps-high-watermarks/
- exhaustive coverage 참고: https://primegap-list-project.github.io/fully-analyzed/
- 현재 문서화한 exhaustive 상한: 10^20, 2026-05-08

웹페이지는 입력 dataset으로 사용하지 않는다. master는 이동하므로 승인된 실행 직전에 다시 resolve하고 실제 SHA를 metadata에 고정한다. 최신 발견 목록과 exhaustive coverage는 서로 다른 개념이다.

## 6. 검증 증거

연구 코드와 테스트 executable:

    W:\miniforge3\envs\FGKMT\python.exe

전체 suite:

    & 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest discover -s tests -v

결과: 31 tests PASS.

추가 확인:

- source.cli preflight: PASS, exact Python 일치, mpmath dps 50, iter_log_4 직접 중첩값 일치
- source.cli status: raw 0, validated 0, completed analysis 0
- source.cli fetch --dry-run: network false, files_written false
- run_experiment.ps1 구문: PASS
- Approved 없는 runner: 쓰기 전에 차단, test_result 파일 0
- skill-creator quick_validate.py: 16개 SKILL.md PASS
- .claude와 Codex mirror: project JSON 유효, 46개 비바이너리 파일 SHA-256 일치
- 프로젝트 텍스트·파일명에서 금지된 네 글자 오기: 0
- source의 base-2/3/4 로그 호출: 0

스킬 검증기는 PyYAML이 필요한 도구라 FGKMT 환경을 변경하지 않고 기존 p018 Python을 UTF-8 도구 실행에만 사용했다. 연구 코드·수치·그래프 테스트는 모두 지정 FGKMT Python으로 수행했다.

## 7. 남은 위험과 해석 주의

- canonical source는 하나다. ismax 독립 재도출과 endpoint 검증은 하지만 별도 기관 dataset과의 독립 교차검증을 완료했다고 주장하지 않는다.
- record completeness는 next-prime 검사만으로 증명되지 않고 external exhaustive-search provenance에 의존한다.
- 실행 시 master가 현재 관측 SHA에서 바뀔 수 있으므로 다시 pin해야 한다.
- verified limit를 넘는 row가 source에 있어도 1차 분석은 10^20을 넘지 않는다.
- running minimum은 정의상 비증가한다. 장기 상승·하강은 interval minima와 descriptive trend에서만 논한다.
- descriptive slope와 correlation은 record intervals가 독립 표본이 아니므로 추론 통계나 asymptotic exponent로 해석하지 않는다.
- H가 Sono constant 아래로 내려가더라도 sufficiently-large threshold 이전의 유한 관측일 수 있으며 theorem 반례로 부르지 않는다.

## 8. 다음 사용자에게 요청할 사항

1. 위 2절의 연구 목적, end-bounded 정의, iterated-log 정의, source 범위, 해석 한계가 사용자 의도와 같은지 확인
2. 같은 목적과 방법이면 실제 dataset 취득·검증·분석 실행을 명시적으로 허가
3. commit 정책 확인
   - 권장: 실행 시 master를 다시 resolve하고 그 SHA를 자동 고정
   - 대안: 현재 관측 SHA 1a112a1387052d9ad360686313f501c01fe46b68을 명시 고정

명시적 허가 문장 예시:

    위 목적·정의·데이터 범위·수행방법으로 실제 실험 수행을 허가함

## 9. 권장 작업 우선순위와 근거

1. 사용자 도메인 정합 확인과 실행 허가
   - 정의나 목적이 다르면 모든 후속 수치가 의미를 잃으므로 가장 먼저 확인한다.
2. 실행 시점 master 재조회, commit pin, 두 source 취득
   - 최신성과 재현성을 동시에 확보하고 웹 표 스크레이핑을 피한다.
3. schema·row·high-watermark·endpoint·coverage validation
   - 잘못된 record 하나가 이후 전체 계단함수와 envelope를 바꾸므로 분석 전에 fail-closed한다.
4. end-bounded tables와 non-interpretive summary 계산
   - 그래프보다 먼저 CSV와 hash를 확인해 수치 정본을 만든다.
5. PNG/PDF 시각 QA와 독립 spot calculation
   - 축·cutoff·ratio·interval endpoint 오류를 결과 해석 전에 잡는다.
6. Wolf·Sono·문헌과 비교 해석
   - provenance와 계산이 통과한 뒤에만 경험적 패턴, 특이 구조, 후속 추측을 논한다.

## 10. 승인 후 첫 명령

현재 master를 실행 시점에 다시 pin하는 권장 경로:

    .\run_experiment.ps1 -Approved

현재 관측 SHA를 그대로 고정하려면:

    .\run_experiment.ps1 -Approved -Commit '1a112a1387052d9ad360686313f501c01fe46b68'

실행 전 전체 unit test를 한 번 더 수행한다.

## 11. 한국어 commit 메시지 제안

제목:

    feat: FGKMT maximal-gap 실험 파이프라인과 Codex 작업 환경 준비

본문:

    - 저자 약칭과 연구 목적을 FGKMT 및 end-bounded G(x) 정의로 정정
    - iterated natural logarithm 정본과 base-k 오구현 방지 테스트 추가
    - Prime Gap List Project의 commit-pinned data/schema 취득 및 provenance gate 구현
    - SQL 제한 parser, high-watermark 재도출, endpoint 검증 파이프라인 추가
    - H, interval minimum, running minimum, record recovery, Sono/Cramér 분석과 plot 준비
    - .claude 스킬을 Codex용 .agents/skills로 이식하고 ai_dev_tool 규약 정비
    - METHODS, test plan, review, README, handoff와 합성 end-to-end 테스트 갱신
    - 실제 dataset 다운로드와 본 실험은 사용자 승인 전까지 미실행

## 12. 재개용 지시

    Z:\FGKMT-Sono-PrimeGap-Analysis에서 계속한다.
    먼저 AGENTS.md, HANDOFF.md, 연구 작업지시서, docs/METHODS.md를 읽는다.
    canonical G(x)는 p_(n+1) <= x인 end-bounded 함수이고 log_k는 ln의 k회 반복이다.
    실제 dataset과 결과는 아직 없으며 사용자 명시 승인 전에는 fetch/validate/analyze를 실행하지 않는다.
    지정 Python으로 31개 tests와 preflight/status를 다시 확인한 뒤 사용자 도메인 정합과 실행 허가를 받는다.
