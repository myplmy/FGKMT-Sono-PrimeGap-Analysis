# DEP-R09 blind residue-discrepancy·Brun--Titchmarsh 작업원장

- 시작: 2026-09-27 07:48 KST
- 기준 commit: <code>8aee8ba</code> + uncommitted Theory 91 batch
- 목표: blind character weight를 fixed-modulus residue-class prime discrepancy로
  exact 역변환하고, explicit pointwise upper와 Theory 91 moment를 합쳐 실제로 필요한
  centered mean gate를 분리한다.
- 승인·금지 범위: 문헌 다운로드·문서·Python·Lean·local commit 허용. actual prime
  실험·패키지 설치·threshold calculator·장시간 계산·GRH branch·push/PR 금지.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| blind same-law moment | 직접 영향 | fixed outer fiber와 actual inner covering law 유지 |
| character normalization | 직접 영향 | full character orthogonality에서 principal term을 정확히 뺌 |
| analytic source | 영향 있음 | Montgomery--Vaughan 1973 Theorem 2 원문 대조 |
| pointwise upper | 보조 입력 | centered asymptotic으로 승격하지 않음 |
| prime-pair structure | 새 경계 | sparse selected residue mean과 full variance를 구별 |
| empirical/actual | 영향 없음 | prime/dataset 계산 미실행 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| finite character 역변환 | exact, source-independent | analytic smallness 자체는 안 줌 | **우선 증명** |
| Montgomery--Vaughan Brun--Titchmarsh | prescribed residue에 fully explicit | one-sided constant 2, centered mean은 못 닫음 | pointwise L∞에 채택 |
| full residue Parseval | exact L2 | φ(f) 전체 energy를 다시 지불 | 비교 기준 |
| sparse selected-residue discrepancy | mean term에 정확히 밀착 | prime-pair/selected-set theorem 필요 | 새 root gate |
| construction redesign | weighted theorem 가능성 | current proof architecture 변경 | 별도 승인 전 보류 |

## 단계 현황

1. **DONE — 관련 primary source 검색**
2. **DONE — Montgomery--Vaughan 1973 저자 공개본 hash·printed p.121 대조**
3. **DONE — blind inverse transform·real-valued discrepancy 증명**
4. **DONE — explicit Brun--Titchmarsh L∞ envelope와 prime-power 보정**
5. **DONE — Theory 91 moment의 normalized sufficient gate**
6. **DONE — Theory 92·review 101·Python·Lean·verification**
7. **DONE — handoff 작성·local commit 준비·중단조건 판정**

## source provenance

- H. L. Montgomery and R. C. Vaughan, *The large sieve*, 저자 공개 PDF:
  <code>tmp/pdfs/depr09_blind_residue_20260927/Montgomery_Vaughan_1973_large_sieve.pdf</code>
- SHA-256:
  <code>720058876b871e8d1fef22acb285550a227ae9e3b1bedaa042f6d62f3299e8b9</code>
- PDF 16 pages. printed p.121 Theorem 2, 식 (1.10)을 rendered original page에서
  확인했다:
  \(\pi(x+y;k,l)-\pi(x;k,l)<2y/[\varphi(k)\log(y/k)]\), \(y>k\).
- Wiley direct URL은 HTTP 403으로 실패했고 빈 PDF는 생성되지 않았다. 저자 공개본은
  이전 Theory 83 source hash와 정확히 일치한다.

### 2026-09-27 08:06 KST — analytic reduction 완료

- finite character orthogonality로 blind weight를
  \(B_h(v)=\varphi(f)A_h(v;U)-S_h(U)\)인 real discrepancy로 고정했다.
- Montgomery--Vaughan Theorem 2, elementary prime-power bound와 existing theta upper를
  합쳐 \(|B_h(v)|<11U/5\)를 얻었다.
- Theory 91 moment를 \((\rho MU)^2\)로 나누면 pair factor가
  \(\Gamma_M\to\beta\)임을 exact하게 도출했다.
- 남은 최소 gate는 outer-sieved prime vertex set의 signed centered mean이다. 이는
  shifted prime-pair형 sparse discrepancy이며 checked source로는 아직 fully numerical
  양측 upper가 없다.
- Python targeted 11 tests와 combined 19 tests PASS. DEP-R09 canonical 337 tests PASS.
- pinned Lean direct compile exit 0, full build 8,765 jobs exit 0.
- verification refresh/validation PASS: theory 93, formulas 1,814, declarations 338,
  forbidden proof escape 0.
- canonical full Python 1,005 tests 중 이번 변경과 무관한 기존 Windows PowerShell 5.1
  runner test 1건이 <code>$LASTEXITCODE</code> undefined로 FAIL했다. 해당 파일은 현재
  diff가 없고 단독 재현됐다. 이를 전체 PASS로 표시하지 않는다.
- actual prime/dataset 실험, package 설치, threshold calculator, long computation,
  GRH branch, push/PR은 수행하지 않았다.

## 중단 판정

- bounded \(X_{\rm cert}\) range는 아직 없다.
- 다만 full-energy/inner-dimension 장벽을 sparse signed mean 하나로 축약한 큰 구조
  진전이므로 사용자 지시의 보고·일시중단 조건을 적용한다.
- 다음 세션은 식 (92.25)의 outer-law mean/variance를 source-first로 감사한다.
- 완료 handoff는 <code>handoff/202609270808_HANDOFF.md</code>다.
