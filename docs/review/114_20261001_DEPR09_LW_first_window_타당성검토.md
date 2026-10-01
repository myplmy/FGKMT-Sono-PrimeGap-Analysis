# 2026-10-01 DEP-R09 Liu--Wang first-window·full-modulus hybrid 타당성 검토

## 1. 판정과 root 경계

[Theory 105](../method/theory/105_Sono_FMT_DEPR09_LW_first_window_full_modulus.md)은
published first-window source에서 conservative count144를 independently 증명하고,
original full modulus와 D=160의 nonprincipal near-zero nonvanishing kernel을
3/1000 미만으로 줄였다. 기존 C_J를 첫 band 전체에 쓰던 비용을 피하는 source-route 진전이다.
Principal channel, numerical EF, full PNT/PAP·X_cert는 OPEN이다.
핵심 analytic result가2002년 선행논문에 있으므로 새로운 학술 발견이라고 주장하지 않는다.

## 2. Primary source와 실제 대조

M.-C. Liu·T. Wang, Acta Arithmetica102.3 (2002),261--293,
[DOI 10.4064/aa102-3-5](https://doi.org/10.4064/aa102-3-5).
Official33-page PDF SHA:
50c6b5d628a07cfb216078571a846ef658aa7db29515d21bb8dbb4f20dc5055d.
Native text와 rendered pp.273--274·277--278를 대조했다.
Previous pp.278--279·288--289 확인 기록은 보존한다.
이번에는 기존 PDF hash를 재확인했고 새 다운로드·OCR·설치는 하지 않았다.
표적 correction 검색에서 수정본을 찾지 못했지만 전 문헌 부재를 주장하지 않는다.

| 의무 | 개별 확인 | 채택 경계 |
|---|---|---|
| Section3 | q<=x_src, z>=max(x_src*y,10^11) | x_src=q,y=t>=1,z=q*t,log z>=30000만 사용 |
| Character family | fixed-q all characters·nontrivial zeros | conductor lift·multiplicity 보존; Re(s)=0 Euler zeros 제외 |
| (3.6) local branch | lambda=.45, local a=3.12,b=1.9039 | numerator<3/5, denominator>1/5에서 n<=2 직접 검산 |
| (3.18) | C>=0 및 C^2-AB>0 | exact lower2221/15625>1/8 |
| (3.22) | a0=.34, lambda=.45, whole large-log domain | safe quotient<=72, count<=144 |
| Printed table/prose | p.278의364와 p.279의182 차이 | 둘 다 미채택; 독립144 terminal 사용 |
| Theorem8 | polylog modulus/height | 1.3804는 current q,T coefficient가 아님 |

144는 source 최소 log 시작점의 table182보다 강한 주장을 하는 것이 아니다.
더 큰 log>=30000 영역의 independently conservative bound다.
Source y=0·z<x_src 확장을 local log 비교에 쓰지 않는다.

## 3. Hybrid proof의 안전 조건

At each fixed height t, cumulative weighted count의 delta 적분 안에서만
lambda0/log(q*t)를 split한다. Individual zeros를 height에 따라 바뀌는 두 fixed class로
나누어 각각 height layer cake를 적용하는 방식은 채택하지 않았다.
첫 piece는144, tail은 Theory103의 numerical Jutila density다.
Lambda0=9/20에 맞춰 tail coefficient24를 재검산했다.
Height cost3/2와 inverse-rho factor21/20도 보존한다.

LW count는 principal을 포함하지만 target cumulative count와 Jutila tail은
nonprincipal family만이다. Positive subset upper라고 해서 tail을 principal에 확대하지 않는다.
Possible one real zero는 full-P gap의 별도21/20 contribution으로 복원했다.
Original D=160·law·fixed coefficients는 변경하지 않았다.

## 4. Lean과 source proof 분리

- Kernel: actual sqrt5 enclosure, whole L>=30000 scalar bounds, denominator,
  exact height-field identity, displayed real exponential hybrid inequality.
- Conditional kernel: source analytic floor-count premise에서 safe144 terminal.
- Partial: source count identification, local sequence selection, count/height integrals의 계수 부분.
- Source/unformalized: Dirichlet log derivative·zero spacing·counting measure identities·density mapping.

Local axiom/sorry/admit로 analytic gaps를 채우지 않았다.
Scalar proof가 actual PNT 또는 measured prime-error PASS는 아니다.

## 5. 관측 검증

New10 tests·0.035s·exit0, DEP-R09 regression472건·5.671s·exit0.
Source helper의3 pins·exact rational terminals·false root gates는 PASS다.
Direct Lean compile·generator→validator exit0, full build8765 jobs·exit0.
Inventory:106 theory documents·2085 display equations·443 declarations.
KERNEL126·CONDITIONAL142·DEFINITION231·PARTIAL196·SOURCE210·NOT_YET1175·PARSE5,
proof escape0. Whole unittest·actual 계산·calculator·설치·장시간 연산·push/PR은 NOT RUN.

## 6. 다음 최소 입력

Actual full q,T=q^(3/2),U=q^160의 uniform numerical EF를 먼저 감사한다.
Primitive/imprimitive, principal pole, closed endpoints와 positive/negative good heights를
각각 확인하고 LW proof의 CW2 dependency가 필수인지 판정한다.
필요 primary source가 직접 입수 불가하면 정확한 서지와 요청 이유를 보고하고 중단한다.
Numerical EF 후에만 principal/far/PAP·R10--R12·fixed coefficient를 합성한다.
