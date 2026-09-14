# DEP-R09 restricted-residue·individual-primorial variance source 감사 작업원장

- 시작: 2026-09-14 16:42 KST
- 현재 상태: COMPLETE
- 사용자 승인: \(X_{\rm cert}\)를 좁히는 권장 우선순위의 source-first 정규화·증명,
  필요한 짧은 수치·Lean 검증, 문서 동기화와 로컬 staging·commit
- 금지·보류: actual prime sweep·threshold calculator·장시간 연산, source theorem의
  project-local axiom화, `sorry`·`admit`, 외부 연락·게시·push/PR
- 선행 변경: 시작 commit `649e1c8`; `git status --short` 출력 없음

## 목적과 완료조건

- 목적: Theory 76 식 (76.23)의 aggregate second-moment budget을 실제로 공급할 수 있는
  restricted-residue 또는 individual-primorial variance 정리가 기존 문헌에 있는지 원문
  범위·상수·cutoff까지 감사하고, 없으면 정확한 missing theorem과 다음 증명 경로를 좁힌다.
- 완료조건:
  1. Maier의 실제 admissible residue 집합과 downstream quantifier를 원문 식으로 고정한다.
  2. peer-reviewed primary source 후보를 theorem 단위로 선별하고 적용범위를 판정한다.
  3. 후보를 \(Y=q^d,21\le d\le186\) 및 식 (76.23)에 정확히 정규화한다.
  4. drop-in, conditional redesign, wrong regime, nonnumerical을 구분한다.
  5. 새 bounded \(X_{\rm cert}\) 범위가 생기면 즉시 중단해 사용자에게 인라인 보고한다.
  6. 필요한 새 대수만 Lean에 premise-explicit 형태로 넣고 source theorem을 가정하지 않는다.
  7. theory/review/data·색인·Lean 원장·handoff를 검증하고 로컬 commit한다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 영향 있음 | end-bounded \(G\), iterated log 불변; R09 aggregate quantifier만 세분화 |
| 데이터·provenance | 영향 없음 | maximal-gap dataset 미사용; 논문 URL·hash·page/equation만 등록 |
| 통계·정밀도 | 영향 있음 | asymptotic/O·GRH 조건을 numerical unconditional bound로 승격 금지 |
| 승인 경계 | 영향 있음 | 문헌·짧은 검증만; 장시간 계산·새 bounded range 발생 시 즉시 중단·보고 |
| 산출물·비덮어쓰기 | 영향 있음 | 새 theory/review/data/handoff; 기존 Theory 76은 predecessor로 보존 |
| 형식검증 | 확인 필요 | source theorem은 미형식화, dependency-critical terminal만 단일 Lean 파일에 추가 |

## 접근 비교

| 접근 | 적합성 | 비용 | 핵심 위험 | 우선순위 |
|---|---|---:|---|---:|
| fixed-q residue variance 정리 | 식 (76.23)에 가장 직접적 | 문헌감사 1--3주 | 알려진 asymptotic regime가 q≈Y 또는 GRH일 수 있음 | 1 |
| restricted admissible-set large sieve | 필요한 subset만 직접 제어 | 문헌·구조분석 2--6주 | 평균 modulus와 특정 good primorial의 quantifier 불일치 | 2 |
| admissible-set character energy 직접 개선 | project 고유 구조 활용 | 새 증명 가능성 | 일반 orthogonality의 M보다 실제로 개선되지 않을 수 있음 | 3 |
| 새 individual-primorial moment theorem | 정확한 missing input | 6--24개월 이상 | 신규 해석적 수론 정리 필요·성공 불확실 | 4 |

## 단계 현황

1. **COMPLETE — Maier residue 집합·필요 inequality 원문 재구성**
2. **COMPLETE — primary-source 후보 inventory·theorem 판정**
3. **COMPLETE — current PAP 계약으로 정규화·feasibility 판정**
4. **COMPLETE — missing theorem·character-energy 대안 정식화**
5. **COMPLETE — theory/review/data·필요 Lean·종합 정본 동기화**
6. **COMPLETE — 전수 검증·handoff·`-done`·로컬 commit 준비**

## 단계별 기록

### 2026-09-14 16:42 KST — 재개·영향도 preflight

- 수행: 최신 handoff, Theory 76·review 84, 작업원장 규약, 적용 skills와 현재 git 상태를
  확인했다. 이전 goal turn은 authoritative commit `649e1c8`과 새 검증 증거를 만든 progress다.
- 파일: `handoff/202609141635_HANDOFF.md`,
  `docs/method/theory/76_Sono_FMT_DEPR09_preabsolute_moment_pointwise_PNT_source_audit.md`
- 결과: tree clean. 다음 source-first 감사는 승인 범위이며 actual 계산은 필요하지 않다.
- 문제·결정: 문헌 평균정리의 “어떤 good modulus”를 Maier의 nested primorial로 바꾸지 않는다.
- 다음 재개점: Maier printed pp.266--268에서 admissible column residue set의 정확한 정의와
  총량 소비식을 추출하고, fixed-q variance 문헌 후보의 theorem regime를 표로 만든다.

### 2026-09-14 16:55 KST — Maier consumer·PDF reading mode 고정

- 수행: `article/Maier 1981.pdf`의 native text layer를 우선 추출하고 printed pp.266--267
  렌더와 대조했다. formula (I)는 admissible columns의 aggregate prime mass이고,
  formula (II)는 close-pair upper bound임을 분리했다.
- 결과: aggregate theorem은 formula (I)만 대체할 수 있다. formula (II)는 R10에 남는다.
  평균 translate에서 good (y)를 얻는 것만으로 Lemma 6-selected (y)가 보장되지는 않는다.
- PDF 정책: OCR 불필요. 원문 text + 핵심 페이지 visual comparison 사용.

### 2026-09-14 17:00 KST — variance primary-source screen

- 수행: Friedlander--Goldston 1996, Fiorilli 2013/2015, Fiorilli--Martin 2023,
  Vaughan 2001, Maynard large-moduli III, Montgomery--Vaughan 1986을 fixed primorial,
  (Y=q^d, 21\le d\le186), numerical multiplier/cutoff 계약으로 대조했다.
- 결과: unconditional fully numerical fixed-primorial drop-in 0개. modulus 평균과
  large-moduli 평균은 양화사·범위가 다르다. Fiorilli--Martin Proposition 2.2는 power-regime
  full natural variance가 zero-free strip을 함의해 과도하게 강한 목표임을 보여 준다.
- 제한: 문헌 전수 불가능성은 주장하지 않는다. 더 약한 Maier-weighted target은 반증되지 않았다.

### 2026-09-14 17:05 KST — exact character energy·minimal target

- 수행: finite character orthogonality에서 total, principal, nonprincipal energy를 분리하고
  principal error (delta_0)를 보존한 budget과 Cauchy equality witness를 유도했다.
- 결과:
  (sum_\chi|C_\chi|^2=\varphi M),
  (sum_{\chi\ne\chi_0}|C_\chi|^2=M(\varphi-M)). Maier 구조로 unweighted total energy를
  낮추는 경로는 `REJECTED_AS_STATED`. 최소 열린 입력은 direct weighted correlation이다.
- 새 bounded (X_{\rm cert}): 없음. 장시간 사용자 계산 필요 없음.

### 2026-09-14 17:10 KST — 정본·코드·Lean 동기화

- 작성: Theory 77, review 85, machine JSON, exact Python helper·9개 unit tests.
- 동기화: 종합 review 83, `docs/METHODS.md`, theory/review index, T1 원장, `AGENTS.md`,
  Lean README와 오류 원장 E125.
- Lean: 단일 `TheoryVerification.lean`에 4개 premise-explicit declaration 추가.
  finite character theorem과 analytic source theorem은 local axiom으로 넣지 않았다.
- 전수원장: theory 78개, display 1,426식, declarations 276개,
  `KERNEL_PASS=91`, `CONDITIONAL_KERNEL_PASS=58`, `NOT_YET_FORMALIZED=1027`,
  금지 proof escape 0.

### 2026-09-14 17:15 KST — 검증

- 첫 targeted test: 9개 중 8개 PASS, 1개는 100-dps 마지막 자리 직접 equality가
  약 (10^{-99}) 반올림 차이로 실패. 수학식은 유지하고 float test를 `mp.almosteq`로 교정했다.
- 재검증: targeted 9/9 PASS, Lean kernel PASS, ledger validator PASS,
  JSON parse PASS, `git diff --check` PASS.
- 전체 unittest: sandbox 밖에서 851개, 88.798초, PASS. sandbox 내부 첫 시도에서 OS temp
  접근을 쓰는 기존 artifact tests가 오류였으나 외부 재실행으로 회귀가 아님을 확인했다.
- 결론: actual prime computation·threshold calculator는 실행하지 않았다.

## 현재 재개점

완료. 다음 세션은 Theory 77 식 (77.18)의 Maier-selected direct weighted correlation을
construction-family/simultaneous-selection 양화사부터 분해한다. full natural variance를
가정하지 않으며, 새 numerical source가 생기기 전에는 threshold calculator를 만들지 않는다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 정리·조건부·수치 실험 상태 분리
- [x] 결과 색인·계획·METHODS/이론 정본 동기화
- [x] 필요한 Lean 검증과 금지 proof escape 0 확인
- [x] 새 timestamp handoff 작성
- [x] `git diff --check`와 참조 경로 확인
- [x] 파일명을 `-done.md`로 변경
