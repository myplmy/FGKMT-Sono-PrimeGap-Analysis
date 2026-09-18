# DEP-R09 Vaughan 2001 variance 원문 감사 작업원장

- 시작: 2026-09-18 22:27 KST
- 루트: <code>Z:\FGKMT-Sono-PrimeGap-Analysis</code>
- WSL 작업경로: <code>/mnt/z/fgkmt-sono-primegap-analysis</code>
- 기준 commit: <code>a6ae9136bd380cc60eaf0c85982b6a689b9bb228</code>
- 선행 정본: Theory 82--84, review 90·92·93, handoff 202609182136
- 목표: 새로 추가된 R. C. Vaughan 2001 variance 원문을 page·theorem·range 단위로
  감사하고, Theory 82의 prescribed-primorial character-energy gate에 주는 exact
  reduction과 적용 불가 범위를 문서·machine ledger·Python·Lean에 고정한다.
- 사용자 승인: source audit과 관련 문서·코드·Lean 검증, 로컬 commit.
- 금지 범위: actual maximal-gap 실험, dataset 취득, 패키지 설치, threshold calculator,
  장시간 prime 계산, push, PR, 외부 게시.
- 중단 조건:
  1. 새 bounded <code>X_cert</code> 범위가 생기면 즉시 사용자에게 보고한다.
  2. 원문 identity·text layer·rendered page가 불일치하면 source를 승격하지 않는다.
  3. 추가 패키지나 실제 계산이 필요하면 실행하지 않고 사용자에게 요청한다.
  4. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>을 도입하지 않는다.

## 입력과 provenance

| 입력 | 현재 증거 | 상태 |
|---|---|---|
| <code>article/vaughan2001.pdf</code> | 180,481 bytes, SHA-256 <code>d5bc8d92c1204b09233c507b83ee185e35a54186122da1c906df87bbcb9d3ecc</code>, PDF 1.2, 21 pages | R. C. Vaughan, PLMS 82 (2001), 533--553 원문 일치; native text·rendered pp.533, 535--536 대조 |
| 사용자 source commit | <code>a6ae9136bd380cc60eaf0c85982b6a689b9bb228</code>, 위 PDF만 추가 | worktree blob과 commit blob 일치 |

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| Theory 82 character energy | 영향 있음 | Vaughan의 residue variance와 exact centering identity로만 연결 |
| source range | 결정적 | modulus-average (Q\asymp Y) 또는 GRH (Q\ge Y^{3/4+\varepsilon})를 prescribed (q=Y^{1/d})로 승격하지 않음 |
| numerical certificate | 영향 없음 | source의 implicit constants·cutoff를 숫자로 발명하지 않음 |
| Lean | 제한적 | centering reduction·power-range mismatch의 finite algebra만 형식화 |
| actual 실험 | 영향 없음 | runner·result·threshold 산출물을 만들지 않음 |
| 선행 Theory 84 | 역사 보존 | `FULL_TEXT_MISSING` 당시 판정은 successor Theory 85에서 갱신 |

## 단계 현황

1. **DONE — 세션·WSL·Git·새 PDF identity 확인**
2. **DONE — 원문 theorem·equation·range visual/text 대조**
3. **DONE — Theory 82 normalization과 exact centering reduction 구현**
4. **DONE — successor theory/review/machine ledger 작성**
5. **DONE — Python·Lean·전수 verification 검증**
6. **DONE — 정본 동기화·완료 handoff·로컬 commit**

## 단계별 기록

### 2026-09-18 22:27 KST — 원문 확인과 착수

- WSL repository에서 사용자 commit과 clean worktree를 확인했다.
- PDF metadata parser 하나의 10-page 오판 대신 MiKTeX <code>pdfinfo.exe</code>와
  실제 page rendering을 대조해 21쪽임을 확인했다.
- printed p.533의 variance 정의, p.535 Theorems 1--2, p.536 Theorem 3과
  implied-constant 주의를 native text와 original-page render로 대조했다.
- 현재 예상 판정: source는 정확한 요청 논문이지만 large-(Q) modulus-average이며,
  (q=Y^{1/d}, 21\le d\le186) prescribed primorial에 대한 unconditional fully
  numerical drop-in은 아니다. exact centering relation은 별도 finite reduction으로 남긴다.

### 2026-09-18 22:34 KST — exact bridge·successor 구현

- finite centering과 nonprincipal Parseval을 분리해
  <code>V_proj=phi(q)V_Vau-|psi(Y,chi0)-Y|^2</code>를 고정했다.
- Theory 85, review 94, machine ledger와 exact Python helper·9개 단위시험을 추가했다.
- Lean에는 source identity를 premise로 받는 character-energy upper, strict gate transfer,
  GRH power-range mismatch terminal 3개만 추가했다. source theorem은 axiom화하지 않았다.
- Theory 84의 missing-source 표시는 당시 snapshot임을 successor note로 보존했다.

### 2026-09-18 22:40 KST — 회귀·전수 검증

- canonical Python 3.11.16으로 Theory 83--85 회귀시험 28개가 PASS했다.
- pinned Lean 4.34.0-rc2 direct compile과 full build가 exit 0이었다.
- verification refresh/validation은 theory 86개, display 1,605식, declaration 305개,
  <code>KERNEL_PASS=98</code>, <code>CONDITIONAL_KERNEL_PASS=81</code>,
  <code>NOT_YET_FORMALIZED=1055</code>, 금지 proof escape 0건으로 PASS했다.
- 최초 refresh는 patch escape 한 곳의 U+000B을 fail-closed로 차단했다. 해당 제어문자를
  정상 LaTeX <code>\varepsilon</code>로 교정한 뒤 text-integrity issue 0으로 재검증했다.
- actual prime/dataset 실험, package 설치, threshold calculator, 장시간 계산은 실행하지
  않았다. 새 bounded <code>X_cert</code> 범위도 없다.

### 2026-09-18 22:47 KST — 로컬 commit·완료 핸드오프

- 검토한 19개 경로만 명시적으로 stage해 local commit
  <code>985b2f78470021d2afb1bd2a54742c51f11a705e</code>을 생성했다.
- WSL Git global/local config는 변경하지 않고 기존 저장소와 같은 author identity를
  commit 명령에만 적용했다.
- 완료 핸드오프 <code>handoff/202609182247_HANDOFF.md</code>를 새 파일로 작성했다.
- push·PR·issue·외부 게시는 수행하지 않았다.

## 완료 점검

- [x] 새 PDF identity·hash·blob·page count 확인
- [x] native text와 rendered source page 대조
- [x] exact centering·Parseval bridge와 principal correction 고정
- [x] Theorems 1--3 object·range·assumption·implicit constant 분리
- [x] current prescribed-primorial range와의 불일치 검증
- [x] Python·Lean·전수 verification regression PASS
- [x] actual 실험·설치·threshold·장시간 계산 미실행 확인
- [x] 새 bounded <code>X_cert</code> 없음 확인
- [x] 정본·원장·핸드오프·local commit 완료
