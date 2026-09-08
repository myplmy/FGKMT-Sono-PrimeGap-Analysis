# H1c-1b.1a.1 sigma-y explicit cutoff 작업원장

- 시작: 2026-09-09 05:25 KST
- 현재 상태: COMPLETE
- 사용자 승인: `X_cert` 계산기 전 정규화·증명 작업을 권장 순서대로 진행하고,
  필요한 lemma는 선행연구를 먼저 대조한 뒤 빠진 연결만 직접 증명한다. 검증 뒤 이번 작업과
  직전 미커밋 작업을 명시 경로로 로컬 stage·commit한다.
- 금지·보류: actual prime/maximal-gap 계산, P018-B, 장시간 runner, package 설치,
  push·PR·외부 게시는 수행하지 않는다. 새 PDF·Lean·package 또는 장시간 계산이 실제로
  필요하면 사용자에게 요청하고 중단한다.
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090508_HANDOFF.md`
- 시작 Git 상태: branch `main`, HEAD
  `c54ce09572cd2e5bc518204465c6d357625192e1`; 직전 H1c-1b.1a의 검증 완료 미커밋
  변경 29개가 있으며 이번 단계에서 보존·동기화·최종 명시 stage 대상으로 다룬다.

## 목적과 완료조건

- 목적: FMT/FGKMT/Sono의 정확한 `sigma`, `y` 정의를 복원하고, endpoint-safe dimension
  coefficient transfer가 요구한
  `sigma*y <= (26/25)*80*c*x*log_2(x)`를 실제 제외-prime 규약까지 포함해 명시적으로
  보장하는 cutoff가 선행정리로 가능한지 판정한다.
- 완료조건:
  1. source page·equation·hash와 explicit Mertens 선행정리의 가정·endpoint·상수를 대조한다.
  2. 적용 가능하면 rigorous finite inequality와 machine-checkable contract를 작성한다.
     불가능하면 정확한 누락 입력과 가장 가까운 conditional gate를 fail-closed로 남긴다.
  3. T1/H1/H1b/H1c/H1c-1b.1a·METHODS·AGENTS·색인을 근거 범위에서 동기화한다.
  4. FGKMT Python 표적·전체 회귀시험, JSON·링크·정적 검사를 통과한다.
  5. 새 timestamp handoff를 작성하고, 검토한 명시 경로만 stage·commit한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated log·end-bounded empirical 정의 | 영향 없음 | empirical dataset·`F/G/H`를 실행하거나 변경하지 않는다 |
| theorem/empirical 구분 | 영향 있음 | `sigma-y` 하위 gate만 판정하고 `X_cert` 전체를 닫지 않는다 |
| proof dependency | 영향 있음 | `SIV-03`과 coefficient-transfer successor만 증거 범위에서 갱신한다 |
| source provenance | 영향 있음 | FMT·FGKMT·Sono와 explicit prime-product source의 판본·식·hash/URL을 고정한다 |
| endpoint·제외 prime | 확인 필요 | product interval의 strict/inclusive endpoint와 exceptional `B` factor를 별도 감사한다 |
| 정밀도 | 영향 있음 | proof는 exact/rational·outward-safe bound로 하고 부동소수점은 보조검산만 쓴다 |
| 승인 경계 | 영향 있음 | 정적 문헌·증명·toy scalar 검산만 수행한다 |
| 재현성 | 영향 있음 | JSON contract와 positive/negative 회귀시험을 작성한다 |
| Git | 영향 있음 | 직전 29개와 이번 명시 변경만 stage; `git add .`/`-A` 금지; push 없음 |

## 단계 현황

1. **DONE — source 식·선행 explicit Mertens 정리 감사**
2. **DONE — finite sigma-y cutoff 정식화 또는 blocker 판정**
3. **DONE — machine contract·보조 코드·회귀시험**
4. **DONE — 정본·색인·오류 원장 동기화**
5. **DONE — 전체 검증·handoff·명시 stage·local commit**

## 단계별 기록

### 2026-09-09 05:25 KST — 상태·범위 고정

- 수행: AGENTS, 최신 handoff, 직전 완료 원장, 작업원장 규약, 관련 프로젝트 스킬과 Git 상태를
  현재 workspace에서 다시 확인했다.
- 파일: 이 원장 신규 작성.
- 명령·검증: `git status --short`, `git branch --show-current`, `git rev-parse HEAD`,
  최신 handoff/ledger 열람.
- 결과: 활성 비-`done` 원장 0개, branch `main`, 직전 검증 완료 미커밋 변경 29개 확인.
- 문제·결정: PDF 스킬 경로를 최초 `.../pdfs/...`로 잘못 추정해 read-only 실패했다.
  정확한 `.../pdf/...` 경로로 즉시 재읽었고 저장소 변경은 없었다. 오류 원장에도 반영한다.
- 다음 재개점: FMT (6.12), FGKMT (6.11), Sono p.542의 `sigma`, `y`, prime-product
  endpoint와 exceptional `B` 취급을 원문에서 추출한다.

### 2026-09-09 05:42 KST — 원문 식·선행정리 적용성 대조 완료

- 원문 복원:
  - FMT (3.1), (4.1)--(4.2), (6.12)와 FGKMT 대응식에서
    `a=(log x)^20`, `z=x^(log_3 x/(4 log_2 x))`,
    `sigma=prod_{a<p<=z,p!=B0}(1-1/p)`를 확인했다.
  - `y=c*x*log(x)*log_3(x)/log_2(x)`이고 명목 주항은 정확히
    `80*c*x*log_2(x)`다.
- 선행정리: Rosser--Schoenfeld 1962 Theorem 7(인쇄 p.70, PDF p.7)의
  `P(t)=prod_{p<=t}(1-1/p)` 양측 명시식을 주 근거로 채택했다. 위쪽은 `t>1`, 아래쪽은
  `t>=285`에서 유효하다. DOI `10.1215/ijm/1255631807`, 공식 Project Euclid PDF hash
  `8e37b06f82e09421bce...ac556`을 확인했다.
- 독립 대조: Dusart 2010 Theorem 6.12의 `0.2/log^2(t)` 형태도 충분하지만 preprint라
  보조검산으로만 둔다. Axler 2018 p.19는 Rosser--Schoenfeld 식을 재인용한다.
- 비판적 배제: Axler 출판 PDF Proposition 9 식 (6.3)의 위쪽 식은 주항 1 또는 지수 표기가
  빠진 것으로 보이며 그대로는 점근식과 모순된다. 이 식은 채택하지 않고 원 Rosser--Schoenfeld
  정리를 직접 사용한다.
- 적용성: `B0`가 `(a,z]` 안에서 제외될 때 `B0>a`이므로
  `(1-1/B0)^-1 <= (1-1/a)^-1`; 미지 exceptional-prime 상수가 필요 없다.
- 도구 오류:
  - PowerShell regex 따옴표를 한 번 잘못 구성했으나 읽기 전용 실패였고 즉시 교정했다.
  - Windows `rg`에 Unix식 `*.txt` 경로 glob을 넘겨 한 번 `os error 123`이 났다. `--glob`
    방식으로 재실행했고 연구 파일 영향은 없다.
  - Springer landing HTML 3,038 bytes가 `.pdf` 이름으로 저장된 것을 signature·`pdfinfo`로
    발견했다. 증거로 사용하지 않는다.
- 다음 재개점: `x>=2*exp(36^5)`에서 Rosser 오차 두 개와 exceptional-prime 보정을 exact
  rational로 합성해 `sigma*y<(1001000/998001)*80*c*x*log_2(x)<(26/25)*...`를 정식화한다.

### 2026-09-09 06:10 KST — finite proof·contract·초기 회귀시험

- 증명: `x>=2*exp(36^5)`에서 `log(a)>300`, `log(z)>log(a)`, 두 Rosser error가
  `1/1000` 미만이고 exceptional-prime factor가 `1000/999` 미만임을 보였다.
- exact 결론:
  `sigma*y<(1001000/998001)*80*c*x*log_2(x)<(26/25)*80*c*x*log_2(x)`.
  이 cutoff는 약 26,260,127자리인 sufficient sublemma cutoff이며 최소 cutoff나
  `X_cert`가 아니다.
- 신규 파일: theory 35, review 41, JSON contract, 보조 Python module, unit test.
- 상태 전이: T1 `SIV-03`만 `PARTIAL -> EXPLICIT`; `AN-02`, `UB-05`는 별도 application이라
  `RATE_MISSING`, `SIV-07/08`은 `HARD_BLOCKER`, `X_cert`는 `OPEN`으로 유지했다.
- 1차 검증: `py_compile` PASS. 표적 54개 중 53 PASS, 1 FAIL.
- 실패 원인: H1c-1b.1a test 한 곳이 승격 전 asymptotic `explicit_bound` 문자열을 기대한
  stale oracle였다. 수학·코드 오류가 아니며 새 finite 식과 `EXPLICIT` 상태를 검사하도록
  교정했다. 오류 원장 E056에 기록했다.
- 기타 교정: download HTML 오인, Windows glob, source hash 전사와 Axler 표시식 위험을
  오류 원장 E052--E055에 공개했다.
- 다음 재개점: 교정한 표적시험을 재실행한 뒤 모든 상위 정본의 과거 next-gate 문구를 현재
  H1c-1b.2로 동기화한다.

### 2026-09-09 06:31 KST — 정본 동기화·자동 검증 완료

- 정본 동기화: T1/H1/H1b/H1c/H1c-1b.1/1a JSON·문서, METHODS, AGENTS,
  이론 색인과 review에 `SIV-03=EXPLICIT`, successor `H1c-1b.2`, 상위 blocker 유지 상태를
  반영했다.
- 표기 교정: 새 Markdown 작성 과정에서 빠진 인라인 수식 구분자, 두 `\qquad`, 한 닫는
  display 구분자와 U+000B 제어문자를 commit 전에 발견해 복구했다. 오류 원장 E057에 기록했다.
- 표적 검증: 관련 9개 module의 **55 tests PASS**.
- 구조 검증: strict JSON **8/8 PASS**, changed Markdown local link
  **150/150 PASS**, Markdown delimiter/control scan **PASS**, `py_compile` **4/4 PASS**,
  `git diff --check` **PASS**.
- 전체 회귀:
  - restricted sandbox 첫 실행은 `PermissionError` 82건으로 무효 처리했다. 기존에 알려진
    validation-environment 규칙을 첫 실행에 적용하지 않은 실수이며 오류 원장 E058에 기록했다.
  - 사용자가 허가한 정상 로컬 권한에서 같은 명령을 재실행해
    **364 tests PASS (`Ran 364 tests in 34.254s`, `OK`)**를 확인했다.
- 과학적 영향: 표기·검증환경 오류 모두 문서/실행 환경 오류이며 수학 결론·empirical artifact
  오염은 없다.
- 다음 재개점: 새 timestamp handoff 작성, 최종 정적검사, 원장을 `-done`으로 바꾼 뒤
  명시 경로만 stage·audit·local commit한다.

### 2026-09-09 06:40 KST — handoff·명시 stage·로컬 commit 완료

- 새 handoff: `handoff/202609090633_HANDOFF.md`.
- 최종 정적검사: changed Markdown 21개, local link 150개, 수식 delimiter와 control
  character issue 0, vocabulary 1/1 PASS, `git diff --check` PASS.
- Git allowlist: 현재 변경 39개와 명시 경로 39개가 정확히 일치했고
  `git diff --cached --check`를 통과했다.
- 로컬 commit: 한국어 제목
  “Sono/FMT H1c-1b.1 계수 전달과 sigma-y cutoff를 명시화”로 성공했다.
  이 원장의 완료 이름 변경을 같은 commit에 amend하므로 최종 hash는 `git log -1`에서 확인한다.
- 완료 이관: 옛 경로에서 `-done.md`로 이동했고 Git은 정확한 old→new pair를
  `R087`로 인식했다. 최초 감사에서 두 경로가 별도 출력될 것으로 잘못 예상한 조건은
  오류 원장 E059에 기록했고, `name-status`·`summary`·cached diff로 다시 확인했다.
- 미수행: push·PR·외부 게시, actual prime/maximal-gap 계산, P018-B, threshold calculator.
- 다음 재개점: H1c-1b.2 common exceptional `B`와 Bordignon full remainder의
  source·composition 감사.

## 현재 재개점

H1c-1b.1/1a/1a.1은 재수행하지 않는다. 다음 단계는 새 작업원장을 만든 뒤
H1c-1b.2 common exceptional `B`와 Bordignon full remainder를 원문에서 감사하는 것이다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 선행정리 우선 조사와 적용성 대조 완료
- [x] 승인·비실행 경계 명시
- [x] 자동 검증과 실제 실험 상태 분리
- [x] 결과 색인·METHODS/이론 정본 동기화
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 명시 경로 stage·local commit
- [x] 파일명을 `-done.md`로 변경
