# 2026-10-01 DEP-R09 fixed-modulus height-weighted density 타당성 검토

## 1. 판정

[Theory 103](../method/theory/103_Sono_FMT_DEPR09_fixed_modulus_height_weighted_density.md)은
실제 fixed-\(f\) family에서 averaged \(f^2t\) 대신 source의 \(ft\) branch를 회복했다.
Height weight를 보존하고 one real exception을 분리하면 \(d_f\ge333\)의 fixed regime에서
nonvanishing kernel을 \(1/100\) 아래로 제어할 수 있다.

이것은 현재 실제 law에 대한 인증이 아니다. Uniform \(d_f\ge333\), downstream outer
parameter admissibility, numerical \(K_{\rm EF}\), remaining same-law correlation이 OPEN이다.
Conditional numeric kernel과 actual project gate를 구분하는 조건 아래
<code>SOURCE_NORMALIZATION_AND_CONDITIONAL_KERNEL_PASS</code>다.

## 2. 원문·선행정리 대조

| source | 실제 대조 | 적용·한계 |
|---|---|---|
| Jutila p.46·51·53 | rendered scans; fixed all-character (1.7), D=qT, nonprincipal setup | imprimitive lift 포함; arbitrary modulus average와 구별 |
| McCurley p.8 Thm.1 | native text locator·rendered scan | M=max(f,f abs(gamma),10), at most one simple real zero |
| Bennett et al. audit p.2 Thm.1.1 | native text·rendered page | primitive conductor>1, t>=5/7; repaired zero-count source |
| Theory 64·70 | detector·finite cutoff·strict terminal | actual fixed-modulus near-one package |
| Theory 69·73 | Rankin product·source-tight factors | local t<f에서는 old 7/4 envelope 적용 불가 |
| Cambridge primary Prop.3.10 | publisher HTML statement·Jutila (1.7) citation | qualitative cross-check only; numerical input 아님 |

McCurley pinned PDF는 *Explicit Zero-Free Regions for Dirichlet L-Functions*다.
일부 이전 registry의 별도 AP error-term 논문 제목 오기는 이번 source identification에서
교정했으며 PDF 또는 historical numeric evidence는 변경하지 않았다.

Fixed-modulus density와 height partial summation은 선행연구의 표준 구조다.
적합한 source가 이미 있으므로 새 qualitative density theorem을 만들지 않는다.
새로 증명한 bridge는 all-height Rankin scalar·source factor composition·height cost
algebra와 fixed exponential budget이다. 학술 novelty를 이 표적 감사만으로 주장하지 않는다.

## 3. Detector·residue·finite 조건

\(D=ft\)에서 fixed-modulus detector \(A=D^{1+9/21}\)는 original power condition을
equality margin으로 만족한다. \(\ell=\log f\)를 source cutoff 최대값 이상으로 요구하면
모든 \(1\le t\le f^{3/2}\)의 \(L=\log(ft)\)도 조건을 만족한다.

Old tightened Rankin cap은 \(\log q/L\le1/2\)를 필요로 한다.
Local t=1이면 이 ratio는 1이다. 따라서 cap을 3으로 교체하고
\(C_{J,\rm all}=19720624464771552/425315<5\cdot10^{10}\)를 다시 합성했다.
Low-height source에 old \(7/4\) constant를 가져온 test는 fail-closed로 거부된다.
Strong \(m=10^6\) absorption cutoff도 동시에 포함했다.

## 4. Zero-free·exception·height kernel

Source standard width \(c_M/\log(ft)\)는 one native-f exceptional real zero를 제외한
family에만 쓴다. Actual \(B_0\)는 그 zero의 부재를 의미하지 않는다.
Possible real channel은 \(c_{B_0}/\log f\)로 separately 보존한다.

Height layer cake는 \(A(T)/T+\int_1^T A(t)t^{-2}dt\)이며 low-height packet을
terminal term만으로 억누르지 않는다. Supplied rational fixtures에서 repeated atoms·
terminal atom·empty packet·negative premise를 점검했다.

Density-count integral은 upper endpoint가 정확히 남고, explicit evaluation 뒤 nonpositive
coefficient만 버린다. Source-normalized ratios는 full parameter rectangle에서 Lean proof다.
Height cost inequality는 differential approximation이 아니라 field identity로 증명했다.

Far beta에서는 1/abs(rho)<=21/20를 쓰지 않는다. Near-zero rho의 singularity는 endpoint
kernel integral로 처리한다. High gamma에만 reciprocal-height saving을 적용한다.
Lower endpoint의 near packet은 f>Y>X와 total zero count로 separately vanishing한다.

## 5. d333 비교의 정확한 뜻

Real-exponential expression \({\cal B}_{\rm nv}(d)<1/100\)을 Lean으로 증명했다.
Fixed constants·\(e>27/10\)·rational powers를 사용하는 statement이지 observed PNT error가 아니다.
333은 최적화 grid나 \(X_{\rm cert}\) root search에서 나온 값이 아니다.

실제 law가 \(d_f\ge333\)을 모든 relevant outcome에서 만족하는지는 아직 미확인이다.
Theo90의 기존 \(21\le d_f<416\)을 하한 333으로 조용히 바꾸지 않았다.
Large-endpoint outer d를 바꾸려면 Pprime support mass와 fixed coefficient capacity까지
같이 검증해야 한다. 조건을 만족하는 것처럼 endpoint나 construction law를 변경하지 않았다.

## 6. 검증 범위

- New finite tests 11건 PASS·0.010s·exit 0.
- Lean direct compile exit 0: divisibility·log specialization·Rankin exponential·factor coefficient,
  normalized ratios·finite scalar layer cake·height cost·real exponential budget·final allocation.
- 식 (103.6), (103.15)--(103.18)은 scalar/normalization 부분과 analytic integral/source
  identification을 분리한다. Entire density proof를 kernel PASS로 올리지 않는다.
- Numerical \(K_{\rm EF}\), full character/zero mapping·counting-measure integrals의 Lean
  formalization은 미완료다. Local axiom·sorry/admit 사용 없음.

DEP-R09 regression 451건·10.730s·exit 0, full lake build 8765 jobs·exit 0도 PASS다.
Inventory는 theory 104개·2043식·declaration 410개·proof escape 0이다.
최종 handoff·정본 동기화 증거는 새 작업원장에 기록한다.
Actual prime/zero 계산·calculator·설치·장시간 계산·push/PR은 NOT RUN이다.

## 7. 다음 최소 gate

1. Theory 49의 \(P'\)는 fixed raw-prime set이고 \(P(\mathbf A)\)는 good subset임을 유지한다.
   Theory 89의 primorial split로 native lower를 증명하고 원래 outer D=160의 실제 budget부터
   판정한다. d333을 필요조건으로 만들거나 만족하게 outer parameter를 바꾸지 않는다.
2. Corrected endpoint의 numerical \(K_{\rm EF}\), common vanishing cutoff를 복원한다.
3. Blind component의 conditional bound를 same-law moment에 연결하되 nonblind characters를
   누락하지 않는다. 다른 character family 전체가 이 bound로 닫히는 것은 아니다.
4. DEP-R09--R12와 최종 변수 전달 전에 calculator는 NOT READY다.

이번 결과는 root로 가는 certificate의 전망을 바꾸지만, verified new academic discovery나
actual \(X_{\rm cert}\) range는 아니다. 의미 있는 학술 발견·장시간 연산이 필요해지면
사용자에게 보고하고 해당 단계에서 중단한다.
