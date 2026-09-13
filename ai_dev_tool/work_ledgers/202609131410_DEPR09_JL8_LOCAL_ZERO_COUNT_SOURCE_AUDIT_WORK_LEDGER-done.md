# DEP-R09 JL8 local zero-count source 감사 작업원장

- 시작: 2026-09-13 14:10 KST
- 현재 상태: COMPLETE_READY_FOR_LOCAL_COMMIT
- 직전 commit: `19c7d4eec257fb642f40e75ba89c73865e2482b7`
- 사용자 승인: `X_cert` 계산기 전 source-first 정규화·증명, 필요 문헌 조사·확보,
  필요시 Lean 형식화·검증, 정본·handoff와 단계별 로컬 stage/commit
- 금지·보류: actual prime sweep, threshold calculator, 숨은 implied constant 임의 선택,
  30분 이상 계산, 새 package 설치, source theorem의 project-local axiom화
- 시작 상태: worktree clean, 진행 중 비 `-done` 원장 없음

## 목적과 완료조건

- 목적: Jutila 1977 Lemma 8의 local zero-count 입력을 원문 statement·proof·인용 source까지
  추적하고, actual DEP-R09 적용에서 필요한 square/rectangle, 계수, 유한 범위와 예외를
  명시적으로 복원할 수 있는지 판정한다.
- 완료조건:
  1. JL8의 정확한 원문 식, 변수 범위, 구간 끝점과 Jutila가 실제로 호출하는 위치를
     페이지·식 번호로 고정한다.
  2. 인용된 Linnik/Prachar 계열과 현대 peer-reviewed explicit 후보를 우선 조사하고,
     target 구조에 그대로 대입 가능한지 개별 검토한다.
  3. drop-in source가 있으면 multiplier·finite cutoff를 출처 그대로 고정한다. 없으면
     직접 증명에 필요한 하위 lemma를 분해하고 현재 범위에서 안전하게 닫히는 부분만
     증명한다.
  4. actual application과 printed general statement를 분리하고 JL8 하나의 진전을
     PAP-11·DEP-R09·fixed `2e-17`·`X_cert` 전체 인증으로 확대하지 않는다.
  5. dependency-critical 유한 대수는 필요한 경우 Lean 단일 파일에 형식화하되
     `sorry`, `admit`, project-local `axiom`을 사용하지 않는다.
  6. machine ledger·fail-closed tests·theory/review·정본·handoff를 동기화하고 전체 검증 뒤
     명시 경로만 stage하여 한국어 메시지로 local commit한다.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset, P002--P020 결과와 figure를 변경하지 않는다. |
| JL8/PAP proof DAG | 직접 핵심 영향 | 원문 geometry와 multiplier가 일치할 때만 상태를 올린다. |
| printed general JL8 vs actual call | 확인 필요 | 실제 square의 결과를 더 넓은 rectangle 명제로 확대하지 않는다. |
| fixed `2e-17`·`X_cert` | 간접 핵심 영향 | 뒤쪽 density/PAP 합성이 남으면 OPEN을 유지한다. |
| provenance | 직접 영향 | native text/OCR을 구분하고 페이지 image와 source hash를 대조한다. |
| Lean | 확인 필요 | analytic zero-count theorem을 local axiom으로 대체하지 않고 유한대수만 후보로 삼는다. |
| 사용자 계산자원 | 현재 영향 없음 예상 | 30분 이상 계산·새 dependency가 필요하면 실행하지 않고 요청한다. |

## 접근 비교

| 접근 | 정확성·재현성 | 비용·위험 | 판정 |
|---|---|---|---|
| A. Jutila의 인용 source에서 exact multiplier·range 직접 복원 | proof dependency와 가장 잘 맞음 | 오래된 원문이 비명시적일 수 있음 | 1순위 |
| B. 현대 peer-reviewed explicit zero-density/local-count 정리의 drop-in 대체 | 상수·범위가 인쇄돼 있으면 재현성 높음 | square/weight/exception 조건 불일치 위험 | A와 병행 비교 |
| C. argument principle·log derivative부터 직접 재증명 | 맞춤형 상수 가능 | 하위 zero-free·boundary estimate가 커지고 오류 위험 높음 | source 대체가 없을 때만 |

## 단계 현황

1. **DONE — Jutila JL8 원문 statement·actual call·인용 계보 고정**
2. **DONE — peer-reviewed explicit 대체자료 조사·drop-in 적합성 비교**
3. **DONE — McCurley source 조합으로 actual multiplier·finite range 복원**
4. **DONE — machine ledger·test·필요한 Lean 및 theory/review 작성**
5. **DONE — 정본 동기화·전수 검증·handoff·완료 원장·local commit 준비**

## 단계별 기록

### 2026-09-13 14:10 KST — 시작

- 직전 goal turn은 JL6 actual 공통 budget을 source/Python/Lean으로 닫고 commit까지 남겼으므로
  `progress`다.
- 최신 handoff와 Git 상태를 다시 확인했고 worktree가 clean임을 확인했다.
- 다음 재개점: Theory 60·64와 Jutila 원본의 Lemma 8 및 호출 위치를 대조해 target 명제의
  exact 변수·영역·숨은 `O`/`<<`와 인용 문헌을 inventory로 만든다.

### 2026-09-13 14:23 KST — 1단계 완료

- Jutila 1977 printed p.51의 Lemma 8과 p.51--52의 actual 호출을 OCR 뒤 원본 렌더링과
  대조했다. 한 Dirichlet L-function의 영점을 중복도 포함해
  `alpha <= beta <= 1`, `|gamma-T0| <= (1-alpha)/2`인 정사각형에서
  `<< (1-alpha) log(q(T0+1)) + 1`로 센다. 인쇄 명제에는 numerical multiplier와
  finite range가 없다.
- actual proof는 `D=qT`, `Delta=1/log D`로 높이 `Delta`인 띠를 만들고, 각 비어 있지 않은
  `(character, strip)`에서 영점 하나를 선택한 뒤 짝수·홀수 띠를 두 well-spaced system으로
  나눈다. 큰 쪽 cardinality가 `J`이고 Jutila는 JL8을 이용해 전체 영점수에서 `J`로 환원한다.
- `delta=1-alpha`, `delta'=max(delta,Delta)`로 두면 각 clipped strip은 중심을 띠 중점으로 한
  JL8 정사각형 하나에 포함된다. 따라서 explicit local bound
  `1 + C_loc delta' log(q(1+|T0|))`가 있으면 전체 선택 전 영점수는 두 parity class 때문에
  `2 J`와 local factor의 곱으로 제어된다. 이 기하학은 `delta<Delta`에서도 성립하므로
  별도 `1/delta` 손실을 만들 필요가 없다.
- Jutila의 인용 `[18, p.331]`은 K. Prachar, *Primzahlverteilung* (1957)다. 공개 Internet
  Archive 항목은 access-restricted이고 p.331은 scan leaf 345이지만 공개 image endpoint로는
  취득되지 않았다. 공개 metadata·scandata만 임시 폴더에 보존했다.
- P. Turan 1961 printed p.166 식 (1.2.2)는 같은 정사각형을 정확히
  `1 + a_2 delta log(A(1+|t_1|))`로 쓰고 p.331을 인용하며 `a_2`를 “about 1/2”로 택할 수
  있다고 말한다. 이는 구조와 유효 상수의 존재는 강하게 확인하지만 exact 인증 숫자는 아니다.
  공개 PDF를 내려받아 SHA-256
  `727ca060e1f6badba083e03efe827ce8b161733fd8444d75971b08a31380efb1`,
  4,633,802 bytes, 15 pages로 고정했다. native text가 있으나 수식 추출이 불완전해 p.166을
  렌더링 원문과 대조했다.
- 경미한 도구 오류: 정본 machine-ledger 이름을 처음에
  `...source_inventory_v1.json`으로 잘못 조회했으나 `rg --files`로 실제
  `Sono_FMT_DEPR09_Jutila_Lemma4_8_v1.json`을 찾아 교정했다. 과학 산출물 영향은 없다.
- 다음 재개점: Turan/Prachar 계보와 현대 explicit zero-count 자료에서 `C_loc` 숫자를
  source statement로 확보할 수 있는지 확인하고, 전 높이 `N(T,chi)` 공식은 local
  `delta` scaling을 잃는다는 점을 정량 비교한다.

### 2026-09-13 14:32 KST — 2단계 완료·3단계 착수

- Gallagher 1970 printed p.333은 Prachar p.331의 Linnik density lemma를
  `한 L-function의 반지름 r 원판 안 영점수 << r log T` 형태로 사용하지만 numerical
  multiplier를 주지 않는다. Turan 1961 식 (1.2.2)도 동일한 정사각형 형태와 유효상수의
  존재를 확인하나 `a_2 about 1/2`이므로 exact certificate 숫자로 채택하지 않았다.
- Bennett--Martin--O'Bryant--Rechnitzer의 explicit 전 높이 `N(T,chi)`를 양 끝에서
  차분하면 두 absolute remainder가 남아 작은 창 너비 `r`에 비례하지 않는다. 따라서
  JL8의 drop-in 대체가 아니다. 2026년 peer-reviewed Linnik-lemma 재진술도 여전히
  숨은 implied constant를 사용한다.
- McCurley 1984 printed pp.10--16의 식 (5), Lemmas 1--4와 식 (13)은 직접 조합 가능한
  explicit replacement를 준다. `sigma=1+r`, `0<r<=1/21`에서 local zero 하나의
  Stechkin kernel은 `3/(8r)` 이상이고, 식 (5)의 양의 Dirichlet-series coefficient와
  Lemma 3에서 `-f(t,chi)<1/r`가 나온다. Lemmas 1--2의 gamma budget과 합치면
  `N_local < 3+r log(q(1+|t|))`를 얻는다.
- imprimitive nonprincipal character는 inducing primitive character와 `Re(s)>0`의
  영점을 공유한다. 추가 Euler factor 영점은 `Re(s)=0`에 있으므로 actual
  `alpha>=1-r>0` 정사각형에 들어오지 않는다. conductor `k<=q`로 로그를 modulus `q`에
  올리는 방향도 안전하다.
- 이 경로는 McCurley의 analytic identity와 gamma/Stechkin source theorem을 전제로 한
  actual application source replacement다. 해당 analytic theorem을 Lean local axiom으로
  선언하지 않고, kernel·상수·strip-to-square·count transfer의 유한 실수대수만 Lean
  후보로 삼는다.
- 경미한 도구 오류: PowerShell `foreach` 결과를 바로 pipe하는 구문이 parser error를
  냈고 배열로 감싸 재실행했다. 또한 다중 image helper에 `forEach` index가 두 번째
  인자로 전달되어 detail type error가 나 한 번의 명시 loop로 교정했다. 파일이나
  과학 판정에는 영향이 없다.
- 다음 재개점: exact 유도를 Theory 65와 machine ledger에 고정하고 evaluator·fail-closed
  test 및 Lean finite algebra를 작성한다.

### 2026-09-13 15:04 KST — 3·4단계 완료, 5단계 착수

- Theory 65와 review 72에 McCurley 식 (5), (13), Lemmas 1--4의 actual 합성을 고정했다.
  결론은 `0<r<=1/21`에서
  `N_square<3+r log(q(1+|t0|))`, Jutila even/odd strip 뒤
  `N_nonprin<=2J{3+r log(2qT)}`다. closed `beta=1` 경계의 비주인 Dirichlet L 비소멸은
  source analytic 입력으로 명시하고 Lean 독립증명으로 과장하지 않았다.
- evaluator `source/dep_r09_jutila_jl8_local_count.py`, fail-closed test,
  machine ledger JSON을 추가했다. source hash·reading mode, exact rational slack,
  dense kernel grid, strip radius, root OPEN 상태를 검사한다.
- `TheoryVerification.lean` 한 파일에 Theory 65 유한 대수를 추가했다. shifted reciprocal
  상계와 height-log 상계까지 포함해 direct Lean check와 `lake build`가 PASS했다.
  `sorry`, `admit`, project-local `axiom`은 0건이다.
- 전수 원장을 재생성·검증했다: theory 66개, display 1,163식, declaration 161개,
  `KERNEL_PASS=49`, `CONDITIONAL_KERNEL_PASS=26`, `NOT_YET_FORMALIZED=995`,
  금지 proof escape 0건, local Markdown link 1,232개, validator PASS다.
- targeted unittest 6/6 PASS, 정상 로컬 권한 전체 unittest 733/733 PASS다. 첫 sandbox 전체
  suite는 `TemporaryDirectory` 접근거부만으로 82 errors를 냈고 수학·코드 실패가 아니었다.
  같은 명령을 사용자가 사전 허용한 sandbox 외부에서 재실행해 전부 통과했다.
- 경미한 교정: 단계 시각을 실제 file timestamp와 맞춰 `15:32` 오기에서 `14:32`로
  바로잡았다. Lean 분수 rewrite 초안 두 번은 compile error 뒤 양의 분모 `field_simp`로
  교정했다. 실행 가능한 theorem에 proof escape를 넣지 않았다.
- 현재 과학 판정: `JL8-ACTUAL-NEAR-ONE`만 explicit source replacement다. printed general
  JL8, JL7/(3.6) terminal density, PAP-11, DEP-R09, fixed `2e-17`, `X_cert`는 OPEN이다.
- 다음 재개점: UTF-8·JSON·local-link·diff 정적 감사, handoff 작성, 원장 `-done` 전환,
  명시 파일 stage와 local commit이다.

### 2026-09-13 15:14 KST — 5단계 완료

- handoff `202609131510_HANDOFF.md`를 새 파일로 작성했다. 쉬운 설명, 수식, source 판독법,
  증거 경계, 검증 결과, 사용자 절차, 다음 우선순위와 한국어 commit 메시지를 포함한다.
- machine ledger의 `Delta`/`delta` key가 PowerShell에서 대소문자 충돌을 일으키는 것을
  발견해 `strip_height`/`alpha_defect`로 고쳤다. Python strict JSON과 PowerShell
  hashtable parser 양쪽에서 3개 JSON이 PASS했다.
- 최종 검증: 표적 6/6 및 전체 733/733 unittest PASS(62.004초), direct Lean exit 0,
  `lake build` 8,765 jobs PASS, generator·validator PASS, 변경 text 20파일 strict UTF-8와
  control 문자 PASS, 변경 Markdown 14파일 local link 1,458개 PASS, `git diff --check`
  whitespace error 0이다. Git의 LF→CRLF 안내는 오류가 아니다.
- 다음 재개점: `JL7/(3.6)-TERMINAL` source-first multiplier·finite-log 감사다. actual
  prime sweep·threshold calculator는 여전히 금지한다.

## 완료 전 점검

- [x] JL8 statement·호출 위치·인용 source 고정
- [x] actual/general 적용범위 분리
- [x] peer-reviewed source-first 조사와 drop-in 판정
- [x] multiplier·finite cutoff 또는 정직한 blocker 판정
- [x] machine ledger·test·필요한 Lean 완료
- [x] PAP-11·DEP-R09·fixed coefficient·X_cert fail-closed
- [x] 정본·색인·오류 원장 동기화
- [x] 전체 unittest·Lean·UTF-8·local links·diff 검증
- [x] 새 timestamp handoff 작성
- [x] 파일명을 `-done.md`로 변경
- [x] 명시 경로 stage·local commit 준비, push 없음
