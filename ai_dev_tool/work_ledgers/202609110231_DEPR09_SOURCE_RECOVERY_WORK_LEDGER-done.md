# DEP-R09 Gallagher·Maier·McCurley 원문 복원 작업원장

- 시작: 2026-09-11 02:31 KST
- 상태: IN_PROGRESS
- 시작 HEAD: `5cddbf9130a99241a48393d8f3b6d5a2ef9e038f`
- 사용자 입력: `article/Maier 1981.pdf`, `article/McCurley 1984.pdf`,
  `article/gallagher1970.pdf` 추가 및 다음 우선순위 착수 승인
- 목표: DEP-R09 R09-01·02·05를 원문 기준으로 감사하고, Jutila와 결합되는
  R09-03·04의 유효 상수·범위를 갱신하며, 가능한 finite child만 Lean으로 형식화한다.
- 금지: `sorry`, `admit`, project-local `axiom`, 숨은 `O/≪/o(1)` 상수를 임의의 숫자로
  치환, threshold calculator·actual prime sweep·dataset 변경, `X_cert` 확정, push·PR
- 중단 조건: 원문이 읽히지 않음, 추가 폐쇄 source·dependency 필요, 장시간 계산 필요,
  또는 finite cutoff를 source에서 복원할 수 없어 새 정량 재증명이 필요한 경우

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의·end-bounded G/F/H | 영향 없음 | empirical 정의·산출물은 변경하지 않는다. |
| `X_cert` proof DAG | 핵심 영향 | R09 source leaf만 갱신하고 R10--R12는 승격하지 않는다. |
| provenance | 핵심 영향 | 세 PDF의 SHA-256, 페이지, 정리·식 locator와 판독 방식을 기록한다. |
| Lean | 조건부 영향 | source theorem 전체와 finite algebra/interface를 분리한다. |
| 데이터·실험 | 영향 없음 | actual dataset·prime 계산·test_result를 만들지 않는다. |
| 승인 | 범위 내 | 사용자가 제공한 PDF의 read-only 분석과 로컬 문서·Lean 검증만 수행한다. |

## 단계 현황

1. **COMPLETE — 시작 상태·PDF 무결성·텍스트층 판별**
2. **COMPLETE — Gallagher Theorems 6--7 및 Sono (5.2) 상수·범위 감사**
3. **COMPLETE — Maier Lemma 2 density-to-PNT transfer 전수 감사**
4. **COMPLETE — McCurley Theorems 1--2 zero-free·exceptional-zero 범위 감사**
5. **COMPLETE — R09 원장·Theory 56 successor 및 Lean critical child 갱신**
6. **COMPLETE — 전체 검증·새 handoff·명시 경로 로컬 commit 준비**

## 단계별 기록

### 2026-09-11 02:31 KST — 착수

- `git status --short`는 출력 0건이었다. 세 PDF는 저장소에 존재하지만 현재 Git status에
  나타나지 않아 ignore/tracking 상태를 별도로 확인해야 한다.
- 최신 handoff는 `handoff/202609110152_HANDOFF.md`다.
- 다음 재개점: 세 PDF의 SHA-256·page count·metadata·native text 추출 가능 여부를
  기계적으로 검사한다. OCR이 필요한 경우에만 OCR을 탐색 보조로 사용한다.

### 2026-09-11 02:46 KST — 단계 1 완료

- 세 PDF는 모두 Git commit `5cddbf9130a99241a48393d8f3b6d5a2ef9e038f`에 이미 추적되어
  있었고, 원본은 수정하지 않았다.
- `Maier 1981.pdf`: 13쪽, SHA-256
  `ca6f2425b850dd5f9d81340d8a4a4c76faf6a947d7486ebf87ff072adbf0a3eb`.
- `McCurley 1984.pdf`: 26쪽, SHA-256
  `6035c9e290ba4a8bb31ed4afef0e014f49324f33cd978b82450c1bdba204d8ac`.
- `gallagher1970.pdf`: 11쪽, SHA-256
  `ecac1c9470521e410ac8731d2f57b77eb364f1fdc0bbd1f71813205afe84adcf`.
- 세 파일 모두 `Encrypted: no`이고 native text 추출이 가능했다. OCR은 사용하지 않았다.
  정리 위치는 `pdftotext -layout`으로 찾고 Gallagher PDF 7--11쪽, Maier PDF 4--5쪽,
  McCurley PDF 2--3쪽을 144-dpi 이미지로 렌더링해 수식·부등호·첨자를 원 페이지와 대조했다.
- MiKTeX `pdftotext`가 사용자 프로필 아래 자체 log 파일을 열지 못했다는 경고를 냈지만,
  세 출력은 각각 30,222/51,246/24,748 문자로 정상 생성되었다. PDF 판독 실패가 아니다.
- 다음 재개점: Gallagher Theorems 5--7의 숨은 상수와 Maier Lemma 2에서 필요한
  `Q=x^(1/D)` 범위를 식별한다.

### 2026-09-11 KST — 단계 2–4 완료: full-source 핵심 판정

- Sono Proposition 5.3은 `1-sigma >= c_ZFR/log(Q(1+|t|))`다. `Q=T`, `|t|<=T`에서
  `log(T(1+T))<=3log T`이므로 이 proposition에서 직접 오는 Gallagher constant는
  `c_ZFR/3=1/72`다. Sono p.536의 `3c_ZFR=1/8`은 이 방향에서 나오지 않는다.
- McCurley Theorems 1–2의 full statement를 p.8–9에서 확인했다. T>=13에서
  `M,M1<=T^2`, `R,R1<12`를 사용하면 family region `c1=1/24`를 보수적으로 직접
  복원할 수 있다. 더 날카로운 bottleneck은 `1/(2R)=0.0518354...`지만 `1/8`은 아니다.
- Gallagher Theorem 7의 source range는 `exp(sqrt(log x))<=Q<=x^b`다. T=Q^5와
  density exponent 16을 합치면 `D>=160`; Q=x^(1/D)의 lower range는 `log x>=D^2`를
  추가로 요구해 D=160에서 `x>=exp(25600)`이다. 이는 source-range gate 하나이지
  u_PAP나 X_cert가 아니다.
- Gallagher 결론은 hidden multiplier를 가진 `≪`이고 Maier Lemma 2도 “approximately”,
  `D large`만 제공한다. fixed D=160에서 이를 exact multiplier 1로 바꾸는 근거가 없다.
  same-exponent 소거에는 K_G<=1, exponent 흡수에는 log K_G<=(a0-a)D가 필요하다.
- Sono p.536의 첫 Q lower range 표기는 같은 페이지 후속 식과 Gallagher 원문에 비추어
  typographical inconsistency다. source-consistent `exp(sqrt(log x))`를 채택했다.
- 최종계수 민감도는 80-dps FGKMT mpmath로 재계산했다. direct c1=1/24, a0=1/240,
  D=M=160, 낙관적 K_G=1에서 약 6.34579e-18이다. a0D=2를 위해 D=M=480이면
  약 2.42576e-18이다. 이는 대체 theorem이 아닌 diagnostic이다.
- 다음 재개점: Theory 57·review 64·machine JSON과 Lean critical scalar/interface를
  동기화한 뒤 inventory 생성기와 validator를 실행한다.

### 2026-09-11 KST — 단계 5 진행

- `docs/method/theory/57_*`, `docs/review/64_*`, source-recovery JSON을 신설했다.
- 단일 Lean 정본에 Theory 57을 추가했다. `log(T(1+T))<=3log T`, reciprocal direction,
  bridge constants, D=160 source-range gate, repaired exponent, multiplier 제거 iff,
  exponent absorption과 one-sided error composition을 proof escape 없이 직접 compile했다.
- direct Lean 실행은 exit 0이었다. 아직 inventory 재생성·원장 validator·전체 회귀·handoff가
  남아 단계 5와 작업 전체는 완료로 표시하지 않는다.
- 상위 정본 AGENTS, METHODS, theory/review 종합, Lean README와 오류 원장 E088–E089에
  최신 fail-closed 판정을 반영했다.

### 2026-09-11 03:19 KST — 단계 5 완료·단계 6 검증 진행

- canonical 문서의 오래된 “`2e-17` proved” 표현을 최신 successor 판정으로 교정했다.
  fixed `2e-17`은 출판본 주장이고 이 프로젝트의 독립 인증은 미완료다.
- `lake build`: `Build completed successfully (8765 jobs)`.
- formula inventory 재생성: theory 58개, formula 1,030개. validator는 declaration 116,
  `KERNEL_PASS` 28, `CONDITIONAL_KERNEL_PASS` 17, `SOURCE_THEOREM_UNFORMALIZED` 8,
  `NOT_YET_FORMALIZED` 960, banned proof escape 0, local link 1,091로 PASS했다.
- 새 source-recovery test 5/5, 표적 문서 구조 test 1/1, sandbox 외부 전체 unittest
  669/669가 PASS했다. 첫 sandbox 전체 실행의 82개 `PermissionError`는 임시폴더 권한
  차단이었으며 정상 권한 재실행에서는 재현되지 않았다.
- strict UTF-8/control scan 19파일, 표적 local path 7건, JSON 3파일 parse,
  `py_compile`, stale canonical wording 검색, `git diff --check`가 모두 PASS했다.
- 발견·교정한 문서 구조·명령·timestamp 실수는 오류 원장 E090–E092에 추가했다.
- 남은 재개점: 새 handoff를 작성하고, 완료 원장으로 이름을 바꾼 뒤 exact allowlist만
  stage·감사·로컬 commit한다.

### 2026-09-11 03:21 KST — 단계 6 완료

- `handoff/202609110319_HANDOFF.md`를 새 파일로 작성했다. 연구 목적의 쉬운 설명,
  source hash·페이지, 수학 판정, Lean 경계, 검증 결과, 다음 우선순위·예상시간,
  사용자 수행절차와 한국어 commit 제목·본문을 포함했다.
- handoff를 포함한 최종 strict UTF-8/control scan은 20파일, 필수 신규 산출물은 5/5,
  `git diff --check`는 PASS했다. LF→CRLF 메시지는 repository의 기존 Windows line-ending
  설정 안내이며 whitespace 오류가 아니다.
- exact staging allowlist는 AGENTS/METHODS, 오류·작업원장·handoff, Theory 57·기계 원장,
  관련 theory/review 정본, Lean 단일 파일·inventory·generator와 새 회귀시험으로 제한한다.
  사용자가 제공한 PDF는 시작 HEAD에 이미 추적되어 현재 diff에 포함되지 않는다.
- sandbox 내부 첫 `git add`는 `.git/index.lock` 권한 거부로 partial stage 없이 실패했다.
  같은 exact allowlist를 기존 사용자 승인 범위의 Git 권한으로 다시 실행해 성공했으며,
  오류 원장 E093에 환경 오류와 영향 범위를 기록했다.
- 첫 staged-path 비교는 Git의 기본 한글 quoting을 고려하지 않아 false mismatch였고,
  `core.quotePath=false`로 교정했다. 정확한 20경로가 일치했으며, 함께 발견한 review 64의
  EOF 빈 줄도 제거했다. 오류 원장 E094에 기록했다.

## 완료 전 점검

- [x] 세 PDF SHA-256·page count·판독방식 기록
- [x] 필요한 모든 원문 페이지를 text와 page image로 대조
- [x] exact source statement와 project 재증명을 구분
- [x] source theorem·conditional algebra·kernel proof 상태 분리
- [x] R09-01--10 상태와 다음 blocker 동기화
- [x] proof escape 0건·Lean·원장·전체 회귀 PASS
- [x] handoff 작성·원장 `-done` 이름 변경·exact allowlist commit 준비
