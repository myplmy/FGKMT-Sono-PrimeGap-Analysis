# DEP-R09 fixed-primorial variance source 감사 작업원장

- 시작: 2026-09-15 01:34 KST
- 루트: <code>Z:\FGKMT-Sono-PrimeGap-Analysis</code>
- 선행 정본: Theory 76--82, review 84--91, handoff 202609150125
- 목표: Theory 82 식 (82.3)의
  \(V(Y,q)=\sum_{\chi\ne\chi_0}|Z_\chi(Y)|^2\)에 실제로 대입 가능한
  prescribed-growing-primorial upper theorem이 기존 문헌에 있는지 확인하고,
  없다면 필요한 최소 새 정리와 대체 entropy 경로를 정확히 좁힌다.
- 중단 조건:
  1. 기존보다 강한 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 사용자에게 인라인 보고.
  2. 접근 불가능한 필수 원문, 추가 Python library 또는 장시간 계산이 필요하면
     정확한 사용자 절차를 요청하고 일시 중단.
  3. <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>은
     사용자 허가 없이 도입하지 않음.
- 비목적: actual prime sweep, threshold calculator, 경험적 maximal-gap 재계산,
  fixed \(2\times10^{-17}\) 또는 \(X_{\rm cert}\)의 조기 인증.

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| \(F,G,H\), iterated log, end-bounded interval | 영향 없음 | empirical 정본과 결과를 변경하지 않음 |
| DEP-R09 proof DAG | 영향 있음 | Theory 82 analytic input만 successor로 분리 |
| probability law | 영향 있음 | fixed \(q=P(x)/B_0\), actual FMT law와 같은 \(Z_\chi\) normalization을 강제 |
| source provenance | 영향 있음 | 원 논문의 theorem, range, 평균변수, 숨은 상수와 cutoff를 page/equation 단위로 고정 |
| numerical certificate | 확인 필요 | average-asymptotic을 prescribed \(q\) bound로 바꾸지 않음 |
| Lean | 후속 판단 | dependency-critical finite implication만 필요 시 형식화; source theorem을 local axiom으로 넣지 않음 |
| 사용자 연산 | 현재 없음 | source·증명 feasibility가 먼저이며 장시간 prime 계산은 금지 |
| 문서·검증 | 영향 있음 | theory/review/machine ledger/색인/METHODS/handoff를 증거에 맞춰 동기화 |

## 접근 비교

| 접근 | 정확성 | 비용 | 핵심 위험 | 우선순위 |
|---|---:|---:|---|---:|
| Friedlander--Goldston·Vaughan 원 정리 직접 감사 | 높음 | 낮음--중간 | \(q\)가 \(Y\)에 가까운 평균 regime일 수 있어 \(q=Y^{1/d}\)에 미적용 | 1 |
| explicit BDH·large sieve를 fixed \(q\)에 보수적으로 특수화 | 높음 | 중간 | \(Y^2\) 규모의 bound가 \(Q_{\mathcal S}/\varphi(q)\) gate보다 지수적으로 클 수 있음 | 2 |
| primitive/imprimitive conductor decomposition과 explicit formula | 높음 | 높음 | exceptional character·zero density·finite cutoff가 기존 PAP blocker를 되살릴 수 있음 | 3 |
| FMT inner construction의 atom/collision entropy 강화 | 잠재적으로 높음 | 높음 | sequential dependence와 deterministic coordinates 때문에 full uniformity를 잘못 가정할 위험 | 3 병행 |
| actual prime computation으로 \(V\) 추정 | theorem 증거로 부적합 | 매우 높음 | 거대한 modulus·character family, 유한 sample을 무한 정리에 오용 | 기각 |

## 단계 현황

1. **DONE — 변수·normalization·필요량 재고정**
2. **DONE — Friedlander--Goldston·Vaughan 및 accessible primary source theorem 감사**
3. **DONE — large-sieve/BDH 보수상계의 asymptotic·수치 feasibility**
4. **DONE — inner entropy·collision 대체 경로 feasibility**
5. **DONE — theorem/review/helper·Lean 필요성 판단과 구현**
6. **DONE — 전체 검증·handoff·완료원장·로컬 commit 준비**

## 단계별 기록

### 2026-09-15 01:34 KST — 재개와 첫 판정

- 직전 batch는 Theory 82와 종합보고서 91을 commit
  <code>1b36e94b7d7bc8f454a84c2ccc06c1d81678f9ee</code>로 닫았고 worktree는 clean이다.
- Theory 82는 outer min-entropy만 사용한다. fully numerical \(V(Y,q)\) theorem은
  계속 OPEN이며 bounded \(X_{\rm cert}\) range는 없다.
- 원문이 확보되지 않았다는 사실을 정리 부재로 바꾸지 않는다. official abstract로
  theorem의 exact range나 numerical constant를 채택하지 않는다.
- 다음 재개점: Theory 76--82의 \(q,Y,d,Z_\chi,V,Q_{\mathcal S}\) normalization과
  Friedlander--Goldston/Vaughan의 평균 대상·\(q/Y\) range를 한 표에서 대조한다.

### 2026-09-15 02:15 KST — source range와 large-sieve certificate 판정

- Friedlander--Goldston 1996, Vaughan 2001, Fiorilli 2013과
  Fiorilli--Martin 2023을 <code>q=Y^(1/d)</code>, <code>21&lt;=d&lt;=186</code>에
  대조했다. 확인된 asymptotic upper는 <code>q</code>가 <code>Y</code>에 가깝거나
  modulus 평균을 취하며, prescribed primorial과 현재 power range를 동시에 덮는
  fully numerical theorem은 식별되지 않았다.
- Montgomery--Vaughan 1973 저자 공개 PDF를 새로 확보해 printed p.119,
  Theorem 1의 exact additive large-sieve constant <code>N+delta^(-1)</code>를
  native text와 rendered original page로 교차 확인했다. SHA-256은
  <code>720058876b871e8d1fef22acb285550a227ae9e3b1bedaa042f6d62f3299e8b9</code>다.
- primitive Gauss-sum/Bessel 전달을 가장 낙관적으로 적용해도 published RHS는
  <code>B_LS=(Y+q^2) sum_(n&lt;=Y) Lambda(n)^2</code>다. Dusart theta bound로
  <code>B_LS/Y^2 &gt; (log Y-log 2)/4 &gt; 5 log q</code>를 얻는다.
- 반면 final shift가 가능한 <code>q</code>개 residue에 완전 균등하다고 가정하는
  최선의 atom cap에서도 Theory 82 gate는
  <code>exp(-4)(q/phi(q))Y^2</code> 이하다. Rosser--Schoenfeld의 explicit
  <code>q/phi(q)</code> 상계를 쓰면 모든 <code>q&gt;=3,d&gt;=21</code>에서 앞의
  large-sieve RHS가 이 최대 gate보다 엄격히 크다.
- 판정 범위: 실제 character energy의 하한이 아니다. 오직
  <code>V&lt;=B_LS</code>라는 그 직접 certificate만으로 <code>V&lt;gate</code>를
  논리적으로 추론할 수 없다는 판정이다. sparse divisor family, prime-specific
  cancellation, direct weighted correlation 또는 다른 zero-density route는 배제하지 않는다.
- bounded <code>X_cert</code> range는 여전히 없고 장시간 계산도 필요하지 않다.
- 다음 재개점: 이 판정을 Theory 83, review 92, fail-closed JSON/Python tests와
  dependency-critical Lean terminal에 반영한다.

### 2026-09-15 03:10 KST — 구현·형식화·전수 회귀 검증

- Theory 83, review 92, fail-closed JSON 원장, Python helper와 9개 표적 단위시험을
  작성했다. Theory 82와 결합한 22개 시험, DEP-R09 전체 245개 시험도 PASS했다.
- Lean에는 source theorem을 공리화하지 않고 식 (83.19), (83.22), (83.29)의
  dependency-critical 유한 함의만 넣었다. `lake build`는 8,765 jobs를 성공했고,
  금지 proof escape는 0건이다.
- 검증원장 재생성 결과는 theory 84개, 수식 1,561개, Lean declaration 300개,
  `KERNEL_PASS=96`, `CONDITIONAL_KERNEL_PASS=73`,
  `NOT_YET_FORMALIZED=1050`이며 validator는 PASS했다.
- 처음 문자 무결성 검사를 `lean` 전체에 걸어 `.lake` 외부 의존성의 정상 탭을
  오류로 잡았다. 추적 대상 340개 파일로 범위를 고쳐 issue 0을 확인했다.
- `lake`는 저장소 로컬 실행파일이 아니라
  `C:\Users\Uranus\.elan\bin\lake.exe`임을 확인했고 정식 `lake build`로
  재검증했다. 첫 명령 실패는 빌드 실패나 수학 오류가 아니다.
- 전체 unittest의 첫 sandbox run은 알려진 `TemporaryDirectory` 권한 제약으로
  82개 환경 오류가 나서 무효 처리했다. 같은 913개를 사용자 승인 범위의 정상
  로컬 권한에서 다시 실행해 913/913 PASS, 80.842초를 확인했다.
- 새 bounded `X_cert` 범위는 없으며, 실제 prime sweep·threshold calculator·
  장시간 계산은 실행하지 않았다.

## 완료 전 점검

- [x] source hash·page·theorem·equation locator
- [x] prescribed \(q\), modulus average, random shift를 분리
- [x] \(q=Y^{1/d}\), \(21\le d\le186\)와 source range 대조
- [x] primitive/imprimitive·exceptional character·endpoint 확인
- [x] exact reduction과 analytic theorem의 증거수준 분리
- [x] Lean 필요성·금지 proof escape 확인
- [x] 새 bounded \(X_{\rm cert}\)·장시간 계산 필요 여부 판정
- [x] 정본·검증·handoff·local commit 준비
- [x] 파일명을 <code>-done.md</code>로 변경
