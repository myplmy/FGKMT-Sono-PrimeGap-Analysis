# H1b-COR1 finite correlation 작업원장

- 시작: 2026-09-09 16:55 KST
- 현재 상태: COMPLETE_PENDING_RENAME
- 사용자 승인: active goal의 X_cert 전 정규화·증명, 선행증명 우선 조사, toy/회귀, 로컬 stage/commit.
- 금지·중단: actual prime/data 실험, threshold calculator, 임의 설치, push/PR. 필수 자료 다운로드/요청 또는 장시간 계산 필요시 보고 후 작업 일시 중단.
- 선행 변경: main HEAD 8c5d972, git status clean, 비완료 원장 없음.
- 직전 goal turn 분류: PROGRESS — H1b-DEP 원문·증명 의존지도, 503회귀, 2개 로컬 commit 완료. 전체 목표는 active/OPEN.

## 목적과 완료조건

FGKMT 출판 Lemma 6.1/FMT Lemma 6.1의 실제 distinct-point correlation을 finite multiplier와 cutoff로 공급한다.
필요한 기존 증명을 먼저 찾고 적용 가정·원문 버전과 대조한다. 가능한 경우 같은 elementary package가 바로 공급하는 sigma/conditioning 입력도 진전시킨다.
닫히지 않은 downstream failure/root를 자동 승격하지 않고 임계 경로의 실제 증명 부채를 줄인다.

## 영향도·불변식

| 축 | 영향 | 통제 |
|---|---|---|
| 반복로그·end-bounded G | 없음 | METHODS 유지 |
| 데이터/provenance | 없음 | datas/test_result 비수정, source 원본/hash 보존 |
| 수학·오차범위 | 있음 | distinct/collision·lower sieve cutoff·제외 B0·조건부 확률을 구분 |
| 정수·정밀도 | 있음 | exact rational toy, 전 범위 근거는 해석적 부등식 |
| 승인 경계 | 고정 | 짧은 toy/회귀만, 필요자료·설치·장시간 계산 시 중단 |
| 재현·정본 | 있음 | successor 신설, 이전 theory 48/DAG 원본 보존, current pointer 별도 |

## 단계 현황

1. **COMPLETE — 현재 Git·goal·handoff·스킬/작업규약 확인**
2. **COMPLETE — correlation 원문·선행증명·actual parameter 감사**
3. **COMPLETE — finite proof/계약·bounded helper·negative tests**
4. **COMPLETE — 표적/전체 회귀·source hash·문서 검사**
5. **COMPLETE — 정본 동기화·한국어 로컬 proof commit**
6. **COMPLETE — 새 handoff·완료 원장 본문 작성; 파일명 변경·문서 마감은 아래 절차**

## 단계별 기록

### 착수
- 새 사용자 AGENTS와 active goal을 적용했다. 이전 H1b-DEP의 완료를 전체 목표 완료로 해석하지 않는다.
- 최신 handoff 202609091648, PDF 규약 09, 작업원장 규약 08, 정적 프로젝트 참조와 5개 적용 스킬을 전체 읽었다.
- 메모리는 source/승인 경계 탐색에만 참고했고 현재 Git·원장으로 재확인했다.

## 현재 재개점

본 단계의 proof·검증·정본·handoff 본문은 완료됐다. 정확한 경로를 확인해 -done rename 후 링크를 재검사하고, handoff/완료 원장 2파일만 마감 commit한다. 성공 여부는 git log -2와 clean 상태로 확인한다. 다음 연구 재개점은 새 H1b-COR2 / DEP-R05 원장이다.

### 원문·해석적 도출

- FGKMT PDF p.27/printed 91 Lemma 6.1 및 p.29/printed 93 Lemma 6.3, FMT pp.13--14를 native text로 읽었다. source 번호는 FMT의 구판 인용과 FGKMT 출판판을 구분했다.
- RS1962 PDF p.7/printed 70은 이미지+숨은 OCR text인 scan이다. 기존 page PNG에서 Theorem 7 (3.25)--(3.26)의 부호·분모·t 범위를 대조했다. 새 OCR/다운로드는 하지 않았다.
- 표적 웹 검색에서 drop-in explicit source를 추가 확인하지 못했다. arXiv 두 정본의 metadata와 이미 로컬에 있는 증명을 사용하며 세계적 부재/novelty를 주장하지 않는다.
- pair collision을 세어 correlation 상대오차 `2/(ln X)^17 <= 1/(ln X)^16`을 도출했다.
- Mertens 곱의 lower/upper 방향을 맞춰 sigma>1/ln X, sigma^(-k)<=X^(1/100)을 도출했다. 이후 residue sparsity<=X^(-3/5), actual small-codegree도 따라온다.
- 독립 copy의 충돌 비용을 보존한 second moment에서 good-P failure<=7/(ln X)^8을 도출했다. 정확한 가정·증명은 새 theory에 기록하고 toy는 보조검산으로만 사용한다.
- 기존 child cutoff는 바꾸지 않는다. 최종 X_cert·PAP/UB·전체 covering theorem은 여전히 OPEN이다.

### 도구 실패·정정

- 옛 dependency locator 호출은 deprecated로 실패해 현재 mcp locator로 재시도했다.
- PDF text stdout이 cp949에서 UnicodeEncodeError를 냈다. bundled Python `-X utf8`로 전체 재추출해 성공했다. 원문 손상/OCR 불능이 아니다.
- theory 47 파일명을 추정해 첫 read가 FILE_NOT_FOUND였다. `rg --files`로 정확한 이름을 찾아 전체 읽었다. 실패한 read를 읽기 완료로 간주하지 않았다.
- 오류 원장/JSON 경로 추정과 rg wildcard path 오류도 실제 경로로 재조회했다. 큰 JSON stdout parse는 실패해 파일별 bounded read로 바꿨다. 오류 E077에 남겼다.
- 한 진행 안내를 일본어로 잘못 보냈다가 즉시 한국어로 재설명했다.

### 구현·증명 1차 검산

- theory 49 §§3–5의 전 범위 증명과 7개 source/predecessor hash를 고정했다. 조건부 atom을 원래 unconditioned bound와 구분한다.
- exact residue enumeration 대 곱 공식, 20점/두 shift의 독립 pair moment, 충돌확률 56/400을 대조했다.
- 첫 전용 23/23 PASS, 0.059초. 이후 parent successor 연결 시험 1개를 추가해 24개가 됐다.
- actual k diagnostic은 O(1)개 exact 부등식만 사용하며 k차원 배열·X 수 자체·소수 목록을 만들지 않는다.
- parent H1b schema 1.17.0, H1c/T1 current pointer, theory 12/14/16·색인·METHODS·AGENTS를 갱신했다. 기존 DEP/NORM/SIGMA 문서는 불변이다.

### 최종 검증

- 전용 24/24 PASS, 0.075초; 표적 137/137 PASS, 0.583초; 전체 527/527 PASS, 59.701초, exit 0.
- 전체 시험은 승인된 정상 로컬 권한에서 1차 판정했다. actual/data/runner 실험은 아니다.
- 5 Python 파일 py_compile PASS. 19파일 strict UTF-8·4 JSON·157 local links·7 source/선행 hash 검사 issue 0.
- FGKMT PDF p.29와 FMT p.14도 native text/no-image/no-hidden-Tr로 추가 확인했다. 원본 불변.
- git diff --check 단독 exit 0. LF/CRLF 안내만 있었고 수학/데이터 오류로 취급하지 않는다.
- 증명의 독립 심사·Lean 인증·actual RAM peak 측정은 하지 않았다.

## 완료 전 점검

- [x] 유한식의 가정·전 범위 증명과 실제 적용범위 확인
- [x] toy·negative·회귀와 원문 hash 검사
- [x] root OPEN/미실행/사용자 요청 여부 명시
- [x] 정본·새 handoff·proof commit
- [x] 완료 원장 본문 준비; -done 이름 변경은 본문 불변·SHA 보존 절차

### 로컬 proof commit·handoff

- 18파일 allowlist 일치, cached diff --check 단독 exit 0 후 e9f3c43 로컬 commit 완료.
- 새 handoff는 202609091722. 남은 9작업, 다음 COR2, 사용자 환경·경로·명령/불필요 절차, 한국어 commit 본문을 포함했다.
- 현재 사용자에게 필수 실행·자료·설치 요청 없음. 전체 goal은 active, 이번 단계는 PROGRESS다.

### 문서 마감 절차

- 이 원장 본문을 더 바꾸지 않고 SHA-256을 보존해 동일 폴더의 WORK_LEDGER-done.md로 이름만 변경한다.
- 새 handoff와 완료 원장의 모든 local link를 실제 파일로 검사한다.
- handoff/202609091722_HANDOFF.md와 이 완료 원장만 별도 allowlist로 commit한다.
- 마감 commit 자신의 hash는 파일에 재삽입하지 않고 git log로 확인한다. 전체 X_cert 목표 완료와 혼동하지 않는다.
