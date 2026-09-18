# DEP-R09 sparse divisor-conductor source 감사 작업원장

- 시작: 2026-09-18 21:01 KST
- 루트: <code>Z:\FGKMT-Sono-PrimeGap-Analysis</code>
- WSL 작업경로: <code>/mnt/z/fgkmt-sono-primegap-analysis</code>
- 기준 commit: <code>27025219714f601fe7df1d1e6c1525e5c7ec85af</code>
- 선행 정본: Theory 82--83, review 90--92, handoff 202609150726
- 목표: Theory 83 뒤에 남은 divisor-conductor sparse character family를 원문과 actual
  normalization에서 감사하여, Theory 82 식 (82.3)에 대입 가능한 fully numerical
  fixed-primorial energy bound가 있는지 판정한다. 없다면 full variance보다 약한 최소
  same-law weighted-correlation 또는 conditional-variance 입력을 정확히 명시한다.
- 사용자 승인:
  1. 76개 EOL-only working-tree 변경의 exact allowlist 복구.
  2. sparse divisor-conductor source audit과 관련 문서·코드·Lean 검증.
  3. 필요한 AGENTS.md·스킬의 WSL 적응 패치.
  4. 로컬 commit.
- 금지 범위: actual maximal-gap 실험, dataset 취득, 패키지 설치, threshold calculator,
  장시간 prime 계산, push, PR, 외부 게시.
- 중단 조건:
  1. 새 bounded <code>X_cert</code> 범위가 생기면 즉시 사용자에게 인라인 보고.
  2. 필수 원문이 손상됐거나 다른 논문이면 정확한 서지·경로를 요청.
  3. 추가 패키지 설치나 장시간 계산이 필요하면 실행하지 않고 사용자에게 보고.
  4. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>은 도입하지 않음.

## 입력과 provenance

| 입력 | 현재 증거 | 상태 |
|---|---|---|
| <code>article/Montgomery-Vaughan 2001.pdf</code> | 320,668 bytes, SHA-256 <code>e4d6a5fae3a41b9b50fe34355b0ea098e852bd84384bba7e1e83dbb083af0c9b</code>, PDF 1.4, 16 pages | Montgomery--Vaughan, <em>Mean Values of Multiplicative Functions</em>; 요청 Vaughan variance 논문과 다름 |
| <code>article/friedlander1996.pdf</code> | 679,866 bytes, SHA-256 <code>4981fe4eb38f8788a74082d031063e4dd9e98c63411fbb31d761e346b8a01bd9</code>, PDF 1.2, 24 pages | Friedlander--Goldston 1996 원문 일치; scan+OCR·rendered page 대조 완료 |
| 사용자 source commit | <code>27025219714f601fe7df1d1e6c1525e5c7ec85af</code>, 두 PDF만 추가 | 확인 완료 |

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| (F,G,H), iterated log, end-bounded interval | 영향 없음 | empirical 정본·dataset·결과를 변경하지 않음 |
| DEP-R09 proof DAG | 영향 있음 | Theory 82--83의 열린 analytic input만 successor로 분리 |
| actual character family | 영향 있음 | conductor (r\mid q), primitive core, induced character multiplicity를 분리 |
| source provenance | 영향 있음 | title·author·journal·page·theorem·equation·range·hash를 원문에서 고정 |
| numerical certificate | 확인 필요 | modulus average나 asymptotic을 prescribed primorial bound로 승격하지 않음 |
| Lean | 후속 판단 | dependency-critical finite implication만 형식화; source theorem은 공리화하지 않음 |
| WSL 운영 | 영향 있음 | Windows 절대경로와 WSL bridge, Lean cwd, EOL 경계를 AGENTS/스킬에 명시 |
| actual 실험 | 영향 없음 | 사용자 금지 범위를 유지하고 runner·result를 만들지 않음 |
| 문서·검증 | 영향 있음 | theory/review/data ledger/index/METHODS/AGENTS/handoff를 증거에 맞게 동기화 |

## 접근 비교

| 접근 | 정확성 | 비용 | 핵심 위험 | 우선순위 |
|---|---:|---:|---|---:|
| 추가된 Friedlander--Goldston·Vaughan 원문 직접 감사 | 높음 | 낮음 | source range가 current (q=Y^{1/d})와 불일치할 수 있음 | 1 |
| conductor (r\mid q)별 primitive decomposition 후 sparse large sieve 적용 | 높음 | 중간 | induced multiplicity와 imprimitive correction을 누락할 위험 | 1 |
| full (V) 대신 actual same-law weighted correlation 직접 제어 | 잠재적으로 높음 | 중간--높음 | final output 의존 complex weight의 moment theorem이 필요 | 2 |
| prime-specific conditional variance 새 정리 | 잠재적으로 높음 | 높음 | fully numerical multiplier·cutoff가 없을 수 있음 | 3 |
| actual prime computation으로 (V) 추정 | theorem 증거로 부적합 | 매우 높음 | 유한 계산을 무한범위 증명으로 오용 | 금지 |

## 단계 현황

1. **DONE — 세션 재개·승인·Git/EOL 경계 고정**
2. **DONE — WSL 운영 규약과 관련 스킬 감사·최소 패치**
3. **DONE — 추가 PDF 2편의 서지·text layer·정리 locator·hash 검증**
4. **DONE — actual conductor decomposition과 source theorem 범위 대조**
5. **DONE — analytic 판정 및 theory/review/machine ledger 구현**
6. **DONE — Python·Lean·문서 정합성 검증**
7. **IN PROGRESS — 완료 handoff·원장 종료·로컬 commit**

## 단계별 기록

### 2026-09-18 21:01 KST — 세션 착수와 환경 복구

- WSL2 Ubuntu, bash, repository root의 read-write mount를 실제 확인했다.
- 프로젝트 Lean pin은 <code>leanprover/lean4:v4.34.0-rc2</code>, kernel commit
  <code>6a10ac8c22beadecabdbb0919c2b50214762f91d</code>, Mathlib commit
  <code>85e3a25e006c35636f0e53b0e9296caca2685bc0</code>이며 설치 binary·checkout과 일치했다.
- 승인된 76개 working-tree 변경은 모두 CRLF/mixed EOL뿐이고 non-EOL diff가 0임을
  확인한 뒤 exact allowlist로 복구했다. 복구 뒤 working tree는 clean이었다.
- 사용자가 두 PDF를 commit <code>2702521</code>로 추가했고 worktree blob과 commit blob이
  일치함을 확인했다. 논문 정체와 theorem 내용은 아직 판정하지 않았다.
- 다음 재개점: WSL에서 잘못된 Python/Lean 경로·cwd·EOL 변환이 재발하지 않도록
  AGENTS.md와 직접 관련된 스킬만 최소 패치한 뒤 두 PDF를 원문 대조한다.

### 2026-09-18 21:12 KST — WSL 규약 최소 패치

- <code>AGENTS.md</code>에 WSL2 runtime 확인, canonical Windows Python bridge,
  Lean project cwd, EOL-only diff 분리 규칙을 추가했다.
- 직접 관련된 <code>exp-preflight</code>, <code>check-and-verify</code>,
  <code>run-batch</code>, <code>pr-workflow</code>, <code>session-handoff</code>만
  같은 원칙으로 갱신했다. 새 skill이나 package는 만들거나 설치하지 않았다.
- <code>lean/README.md</code>에 WSL bridge 명령과 repository root에서 Lake를
  호출하지 말아야 하는 이유를 고정했다.

### 2026-09-18 21:20 KST — 추가 PDF 원문 감사

- Montgomery--Vaughan PDF는 native text와 rendered printed pp.199, 202, 212, 214를
  대조했다. 실제 논문은 16쪽짜리 <em>Mean Values of Multiplicative Functions</em>이고,
  printed p.202 Theorem 5는 signed truncated Möbius sum의 implicit upper다.
- Friedlander--Goldston PDF는 300-dpi scan+OCR이며 rendered printed pp.314--317,
  333, 335를 대조했다. 식 (1.5)의 fixed-\(q\) upper는 GRH·implicit constant이고,
  Theorem 1은 large-\(Q\) average, Theorem 2는 lower bound라 current unconditional
  numerical upper가 아니다.
- 요청 Vaughan 2001 variance 논문의 title·DOI·pages는 공식 metadata로 확인했지만,
  해당 전문은 새 로컬 PDF 두 편에 포함되지 않았다.

### 2026-09-18 21:27 KST — sparse divisor-conductor 판정

- \(\varphi^*(r)=\sum_{e\mid r}\mu(r/e)\varphi(e)\)와
  \(\sum_{r\mid q}\varphi^*(r)=\varphi(q)\)를 exact helper로 검사했다.
- sample \(q=3,30,210,2310,30030,510510\)의 positive conductor level은 각각
  2, 4, 8, 16, 32, 64지만 총 character 수는 2, 8, 48, 480, 5,760, 92,160이다.
- Baier Theorem 2의 sparse-modulus form은 길이 \(N\) 항을 보존한다. 한-frequency
  extremizer로 coefficient-agnostic sampled inequality의 전체 coefficient가 \(N\)
  이상이어야 함을 확인했고, Theory 83과 합쳐 \(YS_2(Y)>V_{\rm gate}\)를 얻었다.
- 판정은
  <code>GENERIC_SPARSE_LARGE_SIEVE_CERTIFICATE_REJECTED</code>다. actual \(V\)의
  하한이나 prime-specific·actual-weight cancellation의 불가능성은 주장하지 않는다.

### 2026-09-18 21:32 KST — 구현·검증

- Theory 84, review 93, machine ledger, exact Python helper·10개 단위시험과 Lean
  terminal 2개를 추가하고 METHODS·색인·T1 원장·종합보고서·Lean 원장을 동기화했다.
- canonical Python으로 Theory 83--84 회귀시험 19개가 PASS했다.
- 고정 Lean 4.34.0-rc2 direct compile exit 0, 전체
  <code>Build completed successfully (8765 jobs)</code>, exit 0을 확인했다.
- 전수 ledger refresh/validation은 theory 85개, display 1,586식, declaration 302개,
  금지 proof escape 0건으로 PASS했다. 이는 analytic source theorem PASS가 아니다.
- 새 bounded \(X_{\rm cert}\) 범위는 없고 threshold calculator·actual prime 계산은
  NOT READY / NOT RUN이다.

## 완료 전 점검

- [x] 승인 범위·금지 범위 고정
- [x] EOL-only exact allowlist 복구와 clean worktree 확인
- [x] 두 PDF의 존재·크기·SHA-256·commit blob 확인
- [x] PDF 서지·page·theorem·equation locator 확인
- [x] prescribed \(q\), divisor conductor, modulus average 분리
- [x] primitive/imprimitive·exceptional character·finite cutoff 확인
- [x] exact reduction과 analytic source theorem의 증거수준 분리
- [x] WSL AGENTS/skill 최소 패치 및 회귀 위험 확인
- [x] Python·Lean·verification ledger 검증
- [x] 새 bounded \(X_{\rm cert}\)·장시간 계산 필요 여부 판정
- [ ] 최신 완료 handoff·로컬 commit
- [ ] 완료 시 파일명을 <code>-done.md</code>로 변경
