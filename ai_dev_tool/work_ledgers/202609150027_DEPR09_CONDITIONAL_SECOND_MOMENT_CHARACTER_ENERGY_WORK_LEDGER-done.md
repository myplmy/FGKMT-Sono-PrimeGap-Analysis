# DEP-R09 conditional second moment·character energy 작업원장

- 시작: 2026-09-15 00:27 KST
- 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 목표: Theory 81 이후 actual final sieve-good law에서
  \(1_{S_{\rm sieve}}|R|^2\)의 조건부 2차 모멘트 또는 character \(L^2\)-energy 경로를
  source-first로 복원해 DEP-R09의 다음 analytic gate를 좁힌다.
- 중단 조건:
  1. 기존 진척보다 강한 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 사용자에게 인라인 보고.
  2. 장시간 계산, 추가 라이브러리 설치 또는 확보할 수 없는 원문이 필요하면 정확한 절차를
     요청하고 일시 중단.
  3. `sorry`, `admit`, project-local `axiom`이 필요해 보이면 도입하지 않고 사용자에게 보고.
- 비목적: actual prime sweep, threshold calculator, 경험적 maximal-gap 재계산,
  fixed \(2\times10^{-17}\)의 조기 인증.

## 영향도 분석

| 축 | 판정 | 통제 |
|---|---|---|
| FGKMT scale·iterated log | 영향 없음 | \(F,G,H\) 정의와 end-bounded empirical 결과는 변경하지 않음 |
| analytic proof DAG | 영향 있음 | DEP-R09의 same-law numerator input만 새 successor theory로 분리 |
| 확률법칙·정규화 | 영향 있음 | final sieve-good indicator, survivor floor와 같은 law를 강제 |
| source provenance | 영향 있음 | FMT·FGKMT·Sono·후보 2차 모멘트 정리의 exact locator·hash·가정을 고정 |
| 수치 정밀도 | 영향 있음 | finite identity는 exact integer/rational arithmetic으로만 검산 |
| Lean | 확인 필요 | dependency-critical finite Fourier·Cauchy·terminal gate만 무공리 형식화 후보 |
| 사용자 연산 | 현재 없음 | analytic source·증명 감사가 먼저이며 새 bounded range 전 장시간 계산 금지 |
| 문서·재현성 | 영향 있음 | theory/review/machine ledger/색인/METHODS/Lean 원장/handoff 동기화 |

## 접근 비교

| 접근 | 정확성 | 재현성 | 비용 | 핵심 위험 | 판정 |
|---|---:|---:|---:|---|---|
| final sieve-good law의 raw conditional second moment 직접 전개 | 높음 | 높음 | 중간~높음 | event conditioning과 CRT shift가 character coefficient와 상관 | 1차 |
| character orthogonality·Parseval 후 prime-error \(L^2\) 결합 | 높음 | 높음 | 중간 | modulus family와 character primitivity·weights가 source theorem과 불일치 가능 | 1차 병행 |
| nibble Doob martingale | 조건부 높음 | 중간 | 높음 | increment·predictable variance가 앞 두 경로 없이는 닫히지 않음 | 2차 |
| pointwise \(L^1\) PAP 복귀 | 높음 | 높음 | 매우 높음 | Theory 73--75의 큰 상수 병목을 그대로 복원 | 현재 기각 |
| reserve randomization 구조변경 | 미확정 | 낮음~중간 | 높음 | covering success mass와 denominator floor를 재증명해야 함 | 후순위 |

## 단계 현황

1. **DONE — exact source·변수·law inventory**
2. **DONE — finite character orthogonality와 normalization identity 감사**
3. **DONE — 적용 가능한 analytic second-moment 선행정리 source screen**
4. **DONE — actual FMT conditional law 합성과 blocker/성공 gate 판정**
5. **DONE — exact helper·tests·dependency-critical Lean**
6. **DONE — 정본·색인·METHODS·검증원장 동기화**
7. **DONE — timestamp handoff·`-done` 전환·로컬 staging/commit 준비**

## 단계별 기록

### 2026-09-15 00:27 KST — 재개·영향도 분석

- 직전 Theory 81 batch와 commit `b223b59`를 current worktree에서 확인했다.
- worktree는 clean이며 branch는 `origin/main`보다 35 commit 앞서 있다.
- 가장 직접적인 다음 질문을 “같은 final sieve-good law에서 raw weighted error의
  2차 모멘트를 어느 source theorem으로 묶을 수 있는가”로 고정했다.
- 먼저 기존 Theory 78--81과 source PDF locator를 식 단위로 대조하고, 그 뒤에만 외부
  large-sieve/Barban--Davenport--Halberstam 계열 후보를 검색한다.
- 다음 재개점: Theory 78--81의 \(R,C_\chi,Z_\chi,M_\omega,S_{\rm sieve}\) 정의와
  conditioning 순서를 표로 고정한다.

## 현재 재개점

outer atom cap, finite convolution energy와 strict terminal gate를 exact helper·tests로
고정하고, dependency-critical scalar implication만 Lean에서 무공리로 형식화한다.
character Parseval과 convolution Cauchy는 Python 유한 전수검산과 수학 증명을 분리해
증거수준을 과장하지 않는다.

### 2026-09-15 00:55 KST — source law·finite Fourier·analytic screen 완료

- FMT printed pp. 9, 12와 native text를 대조했다. outer primes
  \(s\in\mathcal S\)의 \(A_s\bmod s\)는 서로 독립인 균등변수이고 final extension에서도
  \(a_s=A_s\)가 보존된다. 따라서 \(Q_{\mathcal S}=\prod_{s\in\mathcal S}s\)이면
  adaptive inner output과 상관없이 각 final CRT shift 원자는
  \(\Pr(m_\omega=r)\le Q_{\mathcal S}^{-1}\)이다.
- \(e(a;Y)=\varphi(q)^{-1}\sum_{\chi\ne\chi_0}\overline{\chi(a)}Z_\chi(Y)\)와
  \(R(m)=\varphi(q)\sum_{s\in I}e(m+s)\)를 exact normalization으로 고정했다.
  finite Parseval과 Cauchy를 합치면
  \(\sum_m|R(m)|^2\le\varphi(q)|I|^2V\),
  \(V=\sum_{\chi\ne\chi_0}|Z_\chi(Y)|^2\)이다.
- 같은 final sieve-good indicator를 그대로 보존해
  \(\rho_S\le\varphi(q)|I|^2V/Q_{\mathcal S}\)를 얻었다. 따라서 새 충분조건은
  \(V<\tau^2p_*Q_{\mathcal S}M_{\min}^2Y^2/[\varphi(q)|I|^2]\)이다.
- 이는 actual law의 정확한 reduction이지만 analytic \(V\) 상계가 아직 없다.
  Davenport--Erdos의 prime-modulus uniform-shift identity는 benchmark일 뿐이고,
  fixed-q variance, BDH와 moving-interval 정리들은 modulus·평균법칙·explicit cutoff가
  actual FMT 계약과 맞지 않아 drop-in source가 아니다.
- Dusart Theorem 5.2로 \(\log Q_{\mathcal S}\)의 계산 가능한 하한은 얻었지만,
  crude fixed-modulus character bound는 대략 \(q/Q_{\mathcal S}\)의 지수적 손실을 남긴다.
  따라서 bounded \(X_{\rm cert}\)는 새로 생기지 않았고 장시간 계산도 아직 정당화되지 않는다.
- source retrieval 기록: Davenport--Erdos 1952 원문은 확보·hash 고정했다.
  Friedlander--Goldston PDF 후보 URL 하나는 Wayback 404 HTML로 실패해 파일이 생성되지
  않았으며, 해당 실패 출력은 source evidence로 사용하지 않았다.

### 2026-09-15 01:13 KST — 구현·Lean·정본 동기화 완료

- 새 exact helper와 13개 targeted unittest를 추가했고 모두 PASS했다. adaptive inner
  modulo-5 rule을 쓰는 modulo-30 toy, Gaussian-rational cyclic convolution, strict
  character-energy boundary와 Davenport--Erdos small-prime identity를 포함한다.
- 단일 Lean 정본에 raw-moment upper의 합성과 strict character-energy gate에서
  Theory-81 normalized gate로 가는 theorem 2개를 추가했다. analytic V 상계,
  finite character orthogonality와 complex convolution theorem은 local axiom으로
  넣지 않았다.
- direct Lean compile exit code 0과 독립 `lake build`
  `Build completed successfully (8765 jobs)`, exit code 0을 확인했다.
- 전수 verification wrapper는 theory 83개, display 1,528식, declaration 295개,
  금지 proof escape 0건으로 PASS했다.
- 정상 로컬 권한 전체 Python 회귀시험은 `Ran 904 tests in 76.067s`,
  `OK`, exit code 0이었다.
- Theory 82, review 90, machine ledger, T1 successor, METHODS, review index,
  연구현황 review, AGENTS와 Lean 안내문을 동기화했다.
- 오류 원장에는 이번 batch의 read-only locator·source retrieval·patch 실패와 즉시
  재발한 Windows wildcard·patch transport 실수와 source retrieval 실패를
  E146--E154로 숨김없이 기록했다. 과학 결과 오염은 없다.
- 다음 theorem-level source 감사에 필요한 Vaughan 2001 공식 PDF는 Cloudflare challenge로
  확보하지 못했고 파일도 생성되지 않았다. 사용자가 접근 가능한 원문을 제공하기 전까지
  이 논문의 exact theorem·상수·cutoff를 채택하지 않는다.

### 2026-09-15 01:26 KST — 종합보고서·최종 재검증·handoff 완료

- P002--P020 actual과 Theory 01--82를 증거등급별로 다시 종합한
  `docs/review/91_20260915_연구진행현황_목표도달도_학술가치_종합보고서.md`를 작성했다.
- 유한 empirical 성과, recurrence 음성결과, certificate와 acceleration의 차이,
  Sono/FMT proof blocker, project-derived 학술가치 후보와 분야별 잔여 연구량을 분리했다.
- 새 보고서 local link 26개는 missing 0, UTF-8/control character issue 0이었다.
- verification wrapper를 repository root와 absolute script path 형식으로 다시 실행해
  generator·validator·wrapper exit code 0을 확인했다.
- 첫 wrapper 호출에서 이미 lean workdir인데 `lean\tools`를 다시 붙인 알려진 경로 오류가
  재발했다. generator 시작 전 실패해 결과 영향은 없으며 E155와 AGENTS 단일 경로 규칙에
  기록했다.
- 첫 마감 원장 patch도 checklist의 실제 LaTeX 문맥을 다르게 추정해 원자적으로 거부됐다.
  exact EOF를 다시 읽고 작은 patch로 나눴으며 E156에 기록했다. 파일·과학 결과 영향은 없다.
- 첫 Git staging은 sandbox의 알려진 index.lock 권한 경계로 exit 128이었고, 정확한
  21-file allowlist를 승인된 외부 권한으로 다시 실행해 정상 stage했다. E157에 기록했다.
- intended 21-file cached diff의 whitespace 검사도 출력 없이 exit code 0으로 통과했다.
- cached-diff 완료기록 동기화 중 exact bullet 문맥을 빠뜨린 atomic patch 거부와
  raw-template/backtick parser 오류가 이어졌다. 둘 다 파일 변경 전 실패했고 E158--E159에
  기록한 뒤 single-file double-quoted patch로 교정했다.
- 새 timestamp handoff `handoff/202609150125_HANDOFF.md`를 작성했다.
- 다음 단계는 승인된 Korean-message local commit뿐이다.

## 완료 전 점검

- [x] source/page/equation/hash 고정
- [x] 같은 probability law와 event indicator 확인
- [x] pointwise, average, conditional average를 분리
- [x] finite identity와 analytic source theorem 증거수준 분리
- [x] Lean 필요성·금지 proof escape 확인
- [x] 새 bounded \(X_{\rm cert}\) 또는 장시간 계산 필요 여부 판단
- [x] 정본·색인·METHODS·handoff 동기화
- [x] 전체 검증과 cached diff check exit code 0
- [x] 파일명을 `-done.md`로 변경
