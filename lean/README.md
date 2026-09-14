# FGKMT-Sono theory verification

이 Lake 프로젝트는 `docs/method/theory/`에 정리된 FGKMT-Sono 연구 명제의 형식검증을
담는다. 연구 명제는 요청에 따라 `FGKMTSono/TheoryVerification.lean` 한 파일에 모으고,
원문 theory 번호와 식번호를 주석으로 연결한다.

## 고정된 도구chain

| 구성요소 | 고정값 |
|---|---|
| Elan | 4.2.4 (`227caca13`, 설치환경 관측값) |
| Lean | `leanprover/lean4:v4.34.0-rc2` |
| Lean kernel commit | `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` |
| 전체 dependency lock | `lake-manifest.json` |

`lean-toolchain`, `lakefile.toml`, `lake-manifest.json`을 함께 보존한다. Mathlib tag가 아니라
위 full commit을 직접 요구하므로 같은 tag가 나중에 움직이더라도 연구 dependency는 바뀌지 않는다.

## 검증

Windows PowerShell에서 다음처럼 실행한다.

```powershell
Set-Location -LiteralPath 'Z:\FGKMT-Sono-PrimeGap-Analysis\lean'
& 'C:\Users\Uranus\.elan\bin\lake.exe' env lean --version
& 'C:\Users\Uranus\.elan\bin\lake.exe' build
& 'C:\Users\Uranus\.elan\bin\lake.exe' env lean FGKMTSono\TheoryVerification.lean
& 'W:\miniforge3\envs\FGKMT\python.exe' tools\refresh_and_validate_verification_ledger.py
```

마지막 wrapper는 generator를 먼저 성공시킨 뒤에만 validator를 실행한다. theory Markdown은
후행 공백을 포함한 byte 변경만으로도 source hash가 바뀌므로, 마지막 theory 수정 뒤에는
validator를 단독 실행하지 않는다. 두 하위 도구를 진단 목적으로 따로 실행한 결과는 wrapper의
최종 exit code 0을 대신하지 않는다.

`lake build` 성공만으로 모든 논문 입력이 증명된 것은 아니다. 항목별 독립·조건부·미형식화
상태는 `VERIFICATION_LEDGER.md`를 정본으로 삼는다. `sorry`, `admit`, project-local `axiom`은
독립 검증에 사용하지 않는다. 불가피해 보이면 형식화 불가 사유, 대체 공식·방법,
외부 검증 선행연구를 먼저 감사·보고하고 사용자의 명시적 허가 전에는 절대 도입하지
않는다.

### 대수 결합형 preflight

Lean에서 수학적으로 같은 곱도 parser가 만든 결합형이 다르면 첫 적용이 실패할 수 있다.
예를 들어 `((18/7)*θ)*L`과 `θ*((18/7)*L)`은 같은 실수식이지만 정의적 등식은 아니다.
이 유형은 커널이 즉시 거부하므로 완성 증명으로 전파되지는 않지만, 반복되는 초안 오류를
줄이기 위해 다음 순서를 사용한다.

1. 스칼라 곱 단조성으로 얻은 부등식은 원래 모양으로 먼저 이름 붙인다.
2. 목표와 곱 순서만 다르면 경계 한 곳에서만
   `simpa only [mul_assoc, mul_left_comm, mul_comm]`을 사용한다.
3. 분수·다항식까지 섞인 경우 `convert ... using 1 <;> ring` 또는 작은 `calc` 등식으로
   정규화하고, 광범위한 `simp`에 의존하지 않는다.
4. 새 선언을 연속으로 추가하기 전에 위 direct `lake env lean` 명령으로 단일 파일을
   compile한다. 전체 `lake build`는 그 다음 독립 gate다.
5. 쓰이지 않는 가정은 제거한다. source domain이나 안정된 interface를 의도적으로 보존할
   때만 `_h...`로 표시하고 그 이유를 주석으로 남긴다.
6. 실패를 현재 사건으로 보고하기 전에 theorem 이름, 현재 source diff, 이번 compile의
   종료코드와 시각을 오류 원장에 대조한다. 이미 교정된 동일 theorem에 현재 실패 증거가
   없으면 역사적 시행착오라고만 기록하고 다시 고치겠다는 현재형 표현을 쓰지 않는다.

이 규칙은 첫 compile 시행착오를 줄이는 절차다. 실제 수식의 타당성은 여전히 theorem
statement, source premise, Lean kernel 결과를 각각 대조해 판정한다.

현재 Theory 01에서는 `x > exp(exp(exp(1)))`인 의도한 양의 반복로그 domain의
`F(x)>0`, strict monotonicity, end-bounded 정수 plateau의 오른쪽 끝점 minimum을
커널로 검증했다. 이는 finite record의 완전성이나 전체 Sono/FMT 증명,
`X_cert`를 인증하지 않는다.

2026-09-10--11 Theory 55 batch에서는 식 (55.24)--(55.35)의 smooth-remainder
경로를 초등 계산과 외부 해석 입력으로 분해했다. 식 (55.26)의 kernel 적분
항등식, (55.28)의 두 finite-interval 비교, untagged Ein `103/100` 상계,
(55.32), (55.34), 기존 (55.33)은 독립 `KERNEL_PASS`다. (55.29)는 이제 Ein
상계를 내부에서 커널 정리로 호출하지만 Stieltjes 입력은 여전히 premise다.
식 (55.27)의 prime-sum 정규화, `h(1)=δ`, decimal slack, 종단 합성은 형식화했으나,
Rosser--Schoenfeld `θ(t)<1.01624t`와 그 상계를 쓰는 Stieltjes/Abel 비교의
독립 Lean 증명은 없어 식 전체는 `PARTIAL_FORMALIZATION`이다. 따라서 이 batch도
smooth-number source theorem 전체나 `X_cert`를 인증하지 않는다.

2026-09-11 Theory 56 batch는 DEP-R09 numerical PAP에서 인쇄된 상수의 exact 대수,
epsilon 지수 재매개화와 낮은-alpha 지수 bridge를 검증했다. finite principal/error
합성은 analytic premise를 노출한 `CONDITIONAL_KERNEL_PASS`다. Jutila의 epsilon-의존
zero-density theorem과 finite PAP 목표는 `SOURCE_THEOREM_UNFORMALIZED`이며,
Gallagher·Maier·McCurley multiplier와 공통 cutoff는 아직 없다. Theory 56 추가 뒤
inventory는 1,015식이고 `NOT_YET_FORMALIZED`는 960식이다. 이 batch는 PAP 전체나
수치 `X_cert`를 인증하지 않는다.

2026-09-11 Theory 57 batch는 확보된 Gallagher·Maier·McCurley 전문을 반영한다.
Sono Proposition 5.3의 denominator에서 `c_ZFR/3`, 출판본의 `3c_ZFR`가 서로 다름을
확인하고, `log(T(1+T))<=3log T`, D=160 source-range gate, direct repair exponent
`1/240`, hidden multiplier의 보존·흡수 대수를 커널로 검증한다. source analytic theorem은
local axiom으로 넣지 않는다. 이 batch는 Section 5의 normalization gap을 기록하는 것이며,
PAP-11·fixed `2e-17`·`X_cert`를 인증하지 않는다. Theory 57 뒤 inventory는 1,030식이고,
새 15식을 모두 분류해 `NOT_YET_FORMALIZED`는 960식으로 유지된다.

2026-09-13 Theory 58 batch는 최신 공개 Sono판과 modern explicit PNT-in-AP·density·
Deuring--Heilbronn source의 적용성을 감사하고 fixed downstream coefficient의 capacity를
고정밀 재계산했다. 대체 analytic theorem을 채택하지 않았으므로 새 Lean 선언은 없다.
16개 display는 source theorem 7식, definition 1식, 아직 Lean으로 형식화하지 않은
coefficient/interface 진단 8식으로 분류했다. 전체 inventory는 theory 문서 59개,
1,046식이고 `NOT_YET_FORMALIZED`는 968식이다. source theorem, fixed `2e-17`, PAP-11,
`X_cert`를 Lean이 증명했다는 뜻이 아니다.

2026-09-13 Theory 59 batch는 fixed-D transfer의 순수 대수만 추가했다. 양의
`K`, `eta`, `D`에서 `(log K-log eta)/D <= c`이면 `K*exp(-D*c)<=eta`인 theorem
`pap_fixed_d_transfer_gate`가 `KERNEL_PASS`다. Thorner--Zaman·Jutila의 density/PNT theorem과
그들이 actual numerical `K`, `c`, cutoff를 준다는 명제는 형식화하거나 local axiom으로
가정하지 않았다. 새 10식 뒤 inventory는 theory 문서 60개, display 1,056식,
`NOT_YET_FORMALIZED` 970식이며 금지 proof escape는 0건이다. PAP-11과 `X_cert`는 OPEN이다.

2026-09-13 Theory 60 batch는 Jutila Lemmas 4--8의 source inventory를 추가했다. 공식
Huxley III 원문을 확보·hash 고정하고, Ramaré--Zuniga Alterman의 explicit Corollary 1.3을
p.54 Theorem 1-prime branch의 `tau=8/5`에 대입한 coefficient `18884947/500000`과
그 branch의 finite log-ratio 대수를
`KERNEL_PASS`로 검증했다. finite power correction은 exponent 대수만
`PARTIAL_FORMALIZATION`이다. 외부 Barban--Vehov·Jutila·Huxley 정리는 local axiom으로
가정하지 않았다. 새 12식 뒤 inventory는 theory 문서 61개, display 1,068식,
`NOT_YET_FORMALIZED` 971식이며 금지 proof escape는 0건이다. `JL5/JL6/JL8`, PAP-11,
fixed `2e-17`, `X_cert`는 OPEN이다. Theory 66은 이 고정값을 식 (3.6)에 적용하면
안 된다는 scope 교정을 기록한다.

원문 theory를 수정한 뒤에는 생성기와 검증기를 차례로 실행한다. 생성기는 display 수식의
원문 경로·행·SHA-256을 다시 고정하며, 검증기는 전수 coverage, 선언 연결, 금지된 proof
escape, toolchain pin을 검사한다. `.lake/`는 로컬 build cache이므로 Git에 포함하지 않는다.

2026-09-13 Theory 62 batch는 Jutila Lemma 6의 Mellin 적분 component를 추가했다.
actual `M` local factor, imprimitive correction의 유리부, vertical-line triangle budget,
Gamma split 계수, `delta=epsilon/[4(1+epsilon)]` 범위와 exponent budget을 형식화했다.
Mellin inversion·contour 이동·Rademacher convexity·complex Gamma bound는 local axiom으로
가정하지 않고 source/direct-proof 미형식화 상태로 남겼다. inventory는 theory 문서 63개,
display 1,104식이며 전체 상태는 `KERNEL_PASS=36`, `CONDITIONAL_KERNEL_PASS=20`,
`DEFINITION_ONLY=8`, `PARTIAL_FORMALIZATION=17`,
`SOURCE_THEOREM_UNFORMALIZED=34`, `NOT_YET_FORMALIZED=984`,
`PARSE_REVIEW_REQUIRED=5`다. 금지 proof escape는 0건이다. `JL6-TAIL`, JL6 전체, JL8,
PAP-11, fixed `2e-17`, `X_cert`는 OPEN이다.

2026-09-13 Theory 63 batch는 Jutila Lemma 6의 actual truncation tail을 분해했다.
`X+1<=2X`, `1/(1-exp(-1/X))<=X+1`, actual exponent
`epsilon+(1+12epsilon)=1+13epsilon`, quadratic decay와 max/square-root cutoff의
tail-budget transfer를 커널로 검증했다. 무한 geometric series, divisor pairing과
pseudocharacter 전체는 local axiom으로 넣지 않고 미형식화·부분형식화로 남겼다.
inventory는 theory 문서 64개, display 1,119식이며 전체 상태는
`KERNEL_PASS=40`, `CONDITIONAL_KERNEL_PASS=20`, `DEFINITION_ONLY=13`,
`PARTIAL_FORMALIZATION=20`, `SOURCE_THEOREM_UNFORMALIZED=34`,
`NOT_YET_FORMALIZED=987`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 143개이고 금지
proof escape는 0건이다. `JL6-TAIL-ACTUAL`은 문서상 parameterized explicit이지만,
printed general tail·JL6 common budget/전체·JL8·PAP-11·fixed `2e-17`·`X_cert`는 OPEN이다.

2026-09-13 Theory 64 batch는 Jutila 식 (2.11)의 actual common detector budget을
추가했다. 원문 identity에서 `exp(-1/X)` 감쇠를 별도 네 번째 loss로 분리하고,
actual power-condition margin
`(1-theta)(1+12theta)-(1+theta)(1+9theta)=theta(1-21theta)`,
damping product, four-part conditional transfer, source coefficient 회복과 terminal
`B_q` exponent 흡수를 형식화했다. Rosser--Schoenfeld와 Zuniga Alterman source theorem,
`B_q` product/root cutoff와 Mellin·무한합 analytic proof는 local axiom으로 넣지 않았다.
inventory는 theory 문서 65개, display 1,142식이며 전체 상태는
`KERNEL_PASS=42`, `CONDITIONAL_KERNEL_PASS=23`, `DEFINITION_ONLY=20`,
`PARTIAL_FORMALIZATION=22`, `SOURCE_THEOREM_UNFORMALIZED=36`,
`NOT_YET_FORMALIZED=994`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 148개,
금지 proof escape는 0건이다. 문서상 `JL6-ACTUAL`은 parameterized explicit이지만
printed general JL6·JL8·PAP-11·fixed `2e-17`·`X_cert`는 OPEN이다.

2026-09-13 Theory 65 batch는 McCurley의 analytic identity를 local axiom으로 만들지 않고,
actual JL8 replacement에 필요한 finite kernel·count·strip 대수만 형식화했다.
`kappa<3/10`, first-pole `8/(17r)`, normalized kernel `3/8`, local
`N<3+rL` conditional transfer, `max(delta,Delta)<=theta<=1/21`과 even/odd
`2BJ` 전달이 단일 theory 파일에서 kernel 검사된다. McCurley 식 (5), (13), Lemmas 1--4,
imprimitive Euler-factor identity는 source theorem 또는 미형식화 direct proof로 남긴다.
문서상 `JL8-ACTUAL-NEAR-ONE`만 explicit source replacement이며 printed general JL8,
Jutila terminal density, PAP-11·fixed `2e-17`·`X_cert`는 OPEN이다. Theory 65 뒤
inventory는 theory 문서 66개, display 1,163식이며 전체 상태는
`KERNEL_PASS=49`, `CONDITIONAL_KERNEL_PASS=26`, `DEFINITION_ONLY=23`,
`PARTIAL_FORMALIZATION=24`, `SOURCE_THEOREM_UNFORMALIZED=41`,
`NOT_YET_FORMALIZED=995`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 161개이고
금지 proof escape는 0건이다.

2026-09-13 Theory 66 batch는 Theory 60의 적용범위 오류를 교정했다. 고정
`tau=8/5`, `37.769894`는 p.54 Theorem 1-prime branch에만 해당하고, p.52 식
(3.6)은 `tau_theta=(1+16 theta)/(1+14 theta)`를 쓴다. 수정된 coefficient identity,
`K_BV(theta)<13/theta`, finite log-ratio와 결합 상계 `34/theta^2`, elementary
exponential slack, integration-area lower bound, off-diagonal exponent margin과
fail-closed terminal absorption을 커널 검증했다. Ramaré--Zuniga의 analytic corollary,
Jutila contour·Lemma 3·residue/well-spacing 및 Ramaré 2016 density theorem은 local
axiom으로 넣지 않았다. 따라서 식 (3.6)의 weighted call은 parameterized explicit지만
terminal multiplier, averaged density, PAP-11, DEP-R09, fixed `2e-17`, `X_cert`는 OPEN이다.
Theory 66 뒤 inventory는 theory 문서 67개, display 1,183식이며 전체 상태는
`KERNEL_PASS=58`, `CONDITIONAL_KERNEL_PASS=28`, `DEFINITION_ONLY=27`,
`PARTIAL_FORMALIZATION=27`, `SOURCE_THEOREM_UNFORMALIZED=43`,
`NOT_YET_FORMALIZED=995`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 177개이고
금지 proof escape는 0건이다.

2026-09-13 Theory 67 batch는 Jutila p.53 shifted-contour multiplier의 actual finite
대수를 추가했다. `0<Re z<=1/7`, real height budget, principal ratio의 squared `16/9`,
`C_NP<9/4`, `C_P<12`, 두 branch의 공통 coefficient 12, power-difference triangle,
contour coefficient identity, elementary majorant와 `theta=1/21` endpoint `45408`을
단일 파일에서 검사한다. Bennett et al.·Hasanalizade--Shen--Wong의 Rademacher source,
complex contour 이동, Gamma improper integral, zeta integral test 전체는 local axiom으로
가정하지 않고 source-unformalized 또는 partial로 보존한다. 따라서
`JL7-CONT=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이라는 문서 합성만 지원하며,
`JL7-LEMMA3/RES/ABSORB/AVERAGED`, terminal density, PAP-11, DEP-R09, fixed `2e-17`,
`X_cert`는 OPEN이다. Theory 67 뒤 inventory는 theory 문서 68개, display 1,208식이며
전체 상태는 `KERNEL_PASS=61`, `CONDITIONAL_KERNEL_PASS=31`, `DEFINITION_ONLY=30`,
`PARTIAL_FORMALIZATION=35`, `SOURCE_THEOREM_UNFORMALIZED=51`,
`NOT_YET_FORMALIZED=995`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 192개이고 금지
proof escape는 0건이다.

2026-09-13 Theory 68 batch는 Jutila JL7 Lemma 3의 actual finite absolute-sum
component를 추가했다. exclusive/common-prime local 계수와 공통 \(p=2\), reciprocal
local identity, finite divisor double-count, floor termwise bound, finite Basel
partial sum \(<5/3\), pair envelope \(<3R^2\), contour 결합 coefficient와
`theta=1/21` endpoint `136224`를 단일 파일에서 검사한다. Jutila Lemma 3 전체
multiplicative-function proof와 Euler-product finite-prime induction은 local axiom으로
가정하지 않고 source-unformalized 또는 partial로 보존한다. 따라서
`JL7-LEMMA3=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이라는 문서 합성만 지원하며,
`JL7-RES/ABSORB/AVERAGED`, terminal density, PAP-11, DEP-R09, fixed `2e-17`,
`X_cert`는 OPEN이다. Theory 68 뒤 inventory는 theory 문서 69개, display 1,226식이며
전체 상태는 `KERNEL_PASS=63`, `CONDITIONAL_KERNEL_PASS=35`, `DEFINITION_ONLY=35`,
`PARTIAL_FORMALIZATION=41`, `SOURCE_THEOREM_UNFORMALIZED=52`,
`NOT_YET_FORMALIZED=995`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 205개이고 금지
proof escape는 0건이다.

2026-09-13 Theory 69 batch는 Jutila printed p.53의 principal residue를
Lemma 3 대각식, pole-cancelled Gamma ladder kernel, 같은-character·같은-parity
height spacing과 diagonal \(r\)-합으로 분해했다. actual
\(0<\theta\le1/21,\ L\ge\theta^{-2}\)에서 interval coefficient,
\(40/19<3\), two-sided Basel coefficient, row coefficient \(91\),
Rankin rational multiplier 12와 최종 \(1092\theta\le52\)를 단일 파일에서
검사한다. 복소 Gamma 적분, character selection 전체와 Euler-product/Rankin analytic
전개는 local axiom으로 넣지 않고 source-unformalized·partial·not-yet 상태로 보존한다.
따라서 `JL7-RES=ACTUAL_INPUTS_PARAMETERIZED_EXPLICIT`이라는 문서 합성만 지원하며,
`JL7-ABSORB/AVERAGED`, terminal density, PAP-11, DEP-R09, fixed `2e-17`,
`X_cert`는 OPEN이다. Theory 69 뒤 inventory는 theory 문서 70개, display 1,252식이며
전체 상태는 `KERNEL_PASS=67`, `CONDITIONAL_KERNEL_PASS=37`,
`DEFINITION_ONLY=43`, `PARTIAL_FORMALIZATION=48`,
`SOURCE_THEOREM_UNFORMALIZED=54`, `NOT_YET_FORMALIZED=998`,
`PARSE_REVIEW_REQUIRED=5`다. declaration은 218개이고 금지 proof escape는 0건이다.

2026-09-13 Theory 70 batch는 Jutila actual 식 (3.6)의 strict terminal absorption을
추가했다. weighted-square-sum·denominator의 \(170/\theta^2\), rational detector lower,
\(q/\varphi(q)\) square normalization 36, \(L\ge e^8\) finite log gate,
exponential cutoff transfer, half-margin terminal algebra,
\(C_J=884000/[9(1-\theta)^2\theta^6]\)와 parity/local-count 합성을 단일 파일에서
검사한다. external complex/character source premise는 local axiom으로 넣지 않았다.
따라서 Lean 결과는 <code>JL7-ABSORB</code>와 actual fixed-modulus nonprincipal
near-one terminal 합성만 지원한다. printed Theorem 1 전체, averaged 식 (3.7),
PAP-11, DEP-R09, fixed \(2\times10^{-17}\), \(X_{\rm cert}\)는 OPEN이다.

Theory 70 뒤 inventory는 theory 문서 71개, display 1,271식이며 전체 상태는
`KERNEL_PASS=72`, `CONDITIONAL_KERNEL_PASS=42`, `DEFINITION_ONLY=48`,
`PARTIAL_FORMALIZATION=50`, `SOURCE_THEOREM_UNFORMALIZED=56`,
`NOT_YET_FORMALIZED=998`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 231개이고
금지 proof escape는 0건이다.

2026-09-14 Theory 71 batch는 Jutila 식 (3.7)의 primitive nonprincipal near-one
variable-modulus 평균을 공통 `D=Q^2*T`에서 재생했다. phase·detector와
principal residue의 totient factor cancellation, off-diagonal phase factor 36,
Mellin scale envelope 방향, common `L^2` cancellation, terminal coefficient 재사용과
local-count log upper를 단일 Lean 파일에서 검사했다. generalized Halasz
inequality, primitive-character conductor uniqueness, complex Mellin/contour와 averaged
analytic 합성 전체는 local axiom으로 넣지 않고 source-unformalized 또는 partial로
보존했다. 따라서 `JL7-AVERAGED-NP-NEAR-ONE`만 actual-input
parameterized explicit이며, printed all-alpha theorem, Gallagher--Maier PAP bridge,
PAP-11, DEP-R09, fixed `2e-17`, `X_cert`는 OPEN이다.

Theory 71 뒤 inventory는 theory 문서 72개, display 1,295식이며 전체 상태는
`KERNEL_PASS=75`, `CONDITIONAL_KERNEL_PASS=47`, `DEFINITION_ONLY=55`,
`PARTIAL_FORMALIZATION=56`, `SOURCE_THEOREM_UNFORMALIZED=58`,
`NOT_YET_FORMALIZED=999`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 240개이고
금지 proof escape는 0건이다.

2026-09-14 Theory 72 batch는 Gallagher 식 (30)의 영점 적분을 near/far로
분리했다. Bennett--Martin--O'Bryant--Rechnitzer Theorem 1.1의 전 높이 영점수를
far branch에 넣었을 때 endpoint가 정확히 소거되는 대수, family-count 합성,
endpoint 지수와 near piecewise 적분의 원시함수 소거를 단일 Lean 파일에서 검사했다.
외부 zero-count theorem과 Stieltjes identity 자체는 local axiom으로 넣지 않고
source-unformalized 또는 조건부 상태로 남겼다. 현재 near certificate의 asymptotic
상계는 d=160에서 약 2.73e13이므로 양의 PAP gate를 통과하지 못한다. 이는 실제
오차의 크기가 아니라 현재 충분 상계의 불충분성을 뜻한다.

Theory 72 뒤 inventory는 theory 문서 73개, display 1,311식이며 전체 상태는
`KERNEL_PASS=77`, `CONDITIONAL_KERNEL_PASS=49`, `DEFINITION_ONLY=58`,
`PARTIAL_FORMALIZATION=58`, `SOURCE_THEOREM_UNFORMALIZED=62`,
`NOT_YET_FORMALIZED=1002`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 245개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 OPEN이다.

2026-09-14 Theory 73 batch는 Theory 72의 selected-system coefficient를 여섯
loss factor로 exact하게 분해했다. generic baseline identity와 endpoint 정수값,
\(\rho\ge4,t\ge1/\rho\)의 full exponential denominator quotient \(<8/5\),
\(L\ge441\) finite log-ratio, averaged \(\log q/L\le1/2\), row monotonicity,
\(e^{23/42}(442/441)<7/4\), area endpoint, arbitrary absorption terminal과
tightened rational coefficient를 단일 파일에서 검사한다. Ramaré--Zuniga의 analytic
Corollary와 Rankin/Euler-product premise는 local axiom으로 넣지 않았고 해당 행은
source-unformalized 또는 partial/conditional로 유지했다.

Theory 73 뒤 inventory는 theory 문서 74개, display 1,344식이며 전체 상태는
`KERNEL_PASS=87`, `CONDITIONAL_KERNEL_PASS=51`, `DEFINITION_ONLY=62`,
`PARTIAL_FORMALIZATION=67`, `SOURCE_THEOREM_UNFORMALIZED=63`,
`NOT_YET_FORMALIZED=1009`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 264개이고
금지 proof escape는 0건이다. 이 형식화는 약 343.38배의 local tightening을 확인하지만,
\(d=186\) PAP budget보다 여전히 약 \(4.623\times10^{11}\)배 크다. PAP-11,
DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 74 batch는 modern explicit density 후보의 analytic 정리 자체를
local axiom으로 넣지 않고, source 대입 뒤 dependency-critical 유한 대수만 검사한다.
Ramaré (d=186,c_1=1/24,T=Q^5)의 exponent margin `83/93`, additive exponent
`1/93`, zero-free edge mass `31/20`, Thorner--Zaman exponent 99·170·198의
capacity 비교와 Friedlander--Iwaniec `80*18*52600=75744000`,
`1/210000<4/5`가 단일 theory 파일에서 커널 검증된다. Ramaré source theorem과
unit-slice integral, 다른 후보의 analytic theorem은 source-unformalized 또는
partial/not-yet 상태로 보존한다.

Theory 74 뒤 inventory는 theory 문서 75개, display 1,362식이며 전체 상태는
`KERNEL_PASS=90`, `CONDITIONAL_KERNEL_PASS=51`, `DEFINITION_ONLY=64`,
`PARTIAL_FORMALIZATION=70`, `SOURCE_THEOREM_UNFORMALIZED=67`,
`NOT_YET_FORMALIZED=1015`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 267개이고
금지 proof escape는 0건이다. 이 형식화는 선별 후보의 수치 drop-in 실패를 analytic
불가능성 정리로 바꾸지 않는다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 75 batch는 두 certified upper bound의 pointwise minimum에 대한
ordered-field 단조성, d=186 first-slice endpoint, coarse rational budget separation과
pre-absolute-value second-moment premise 뒤 Cauchy terminal transfer를 단일 파일에서
검사한다. Ramaré/Jutila analytic theorem, Mellin integral, actual complex character
second moment는 local axiom으로 넣지 않았다. smoothing 판정도 zero-height 정보를 쓰지
않는 source-blind gamma-uniform envelope에 한정하며 모든 oscillatory smoothing의
불가능성으로 승격하지 않는다.

Theory 75 뒤 inventory는 theory 문서 76개, display 1,381식이며 전체 상태는
`KERNEL_PASS=91`, `CONDITIONAL_KERNEL_PASS=53`, `DEFINITION_ONLY=67`,
`PARTIAL_FORMALIZATION=73`, `SOURCE_THEOREM_UNFORMALIZED=68`,
`NOT_YET_FORMALIZED=1024`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 270개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 76 batch는 Bennett large-modulus pointwise PNT의 source cutoff와
현재 `d<=186` capacity가 겹치지 않는 elementary terminal, 그리고 Maier admissible
residue 합에 필요한 character second-moment budget의 Cauchy terminal을 단일 Lean 파일에서
검사한다. character orthogonality, explicit-formula identity, Akbary--Hambrook·Sedunova·
Bennett의 analytic theorem 자체는 local axiom으로 넣지 않았다. 두 새 theorem은 모두
명시적 premise를 받는 `CONDITIONAL_KERNEL_PASS`이며, aggregate 경로를 공급할 fully
numerical individual-primorial theorem은 아직 식별되지 않았다.

Theory 76 뒤 inventory는 theory 문서 77개, display 1,406식이며 전체 상태는
`KERNEL_PASS=91`, `CONDITIONAL_KERNEL_PASS=56`, `DEFINITION_ONLY=73`,
`PARTIAL_FORMALIZATION=80`, `SOURCE_THEOREM_UNFORMALIZED=75`,
`NOT_YET_FORMALIZED=1026`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 272개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 77 batch는 total·principal character energy를 뺀 nonprincipal
identity, principal-separated moment premise에서 weighted numerator target으로 가는
terminal, Cauchy aligned-vector scalar equality와 (d=21,186)의 zero-free-line endpoint
대입을 단일 Lean 파일에서 검사한다. finite character orthogonality와
Fiorilli--Martin의 analytic implication, 실제 direct weighted-correlation theorem은 local
axiom으로 넣지 않았다.

Theory 77 뒤 inventory는 theory 문서 78개, display 1,426식이며 전체 상태는
`KERNEL_PASS=91`, `CONDITIONAL_KERNEL_PASS=58`, `DEFINITION_ONLY=80`,
`PARTIAL_FORMALIZATION=85`, `SOURCE_THEOREM_UNFORMALIZED=80`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 276개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 78 batch는 Maier/FMT CRT 이동량의 양화사를 교정하고 finite
simultaneous-selection 논리만 단일 Lean 파일에서 검사한다. 세 bad finset의 cardinality
합이 전체 finite family보다 작으면 세 집합 바깥의 candidate가 존재하며, singleton family의
strict budget은 세 bad count가 모두 0임을 강제한다. Maier CRT uniqueness, FMT randomized
construction과 analytic weighted-correlation badness 상계는 local axiom으로 넣지 않았다.

Theory 78 뒤 inventory는 theory 문서 79개, display 1,439식이며 전체 상태는
`KERNEL_PASS=94`, `CONDITIONAL_KERNEL_PASS=58`, `DEFINITION_ONLY=87`,
`PARTIAL_FORMALIZATION=86`, `SOURCE_THEOREM_UNFORMALIZED=82`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 278개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 79 batch는 FMT final construction outcome을 first-stage
\(\mathbf A\)와 conditional hypergraph output \(\mathbf N'\)의 joint pair로 교정했다.
Theory 53·55의 finite outer/inner failure를 같은 law에서 합치면 sieve-good mass가
\((1-F_{\rm out})(1-F_{\rm in})\) 이상이라는 probability bookkeeping을 문서·exact
Python으로 고정했다. Lean은 two-stage failure identity, same-law correlation strict
slack, crude union implication과 finite outer/fiber selection만 검사한다. full probability
measure proof, FMT analytic theorem과 weighted-correlation 상계는 local axiom으로 넣지 않았다.

첫 direct compile은 `Finset.card_union_le` implicit 인수 오류 3건을 잡았고 그중 두 곳은
직전 Theory 78 source에 이미 있었다. 인수를 명시한 뒤 canonical direct compile exit 0을
확인했다. 이 사건과 과거 PASS 기록의 증거 모순은 오류 원장 E130에 남겼으며, 무출력이나
session id는 앞으로 PASS로 취급하지 않는다.

Theory 79 뒤 inventory는 theory 문서 80개, display 1,452식이며 전체 상태는
`KERNEL_PASS=94`, `CONDITIONAL_KERNEL_PASS=60`, `DEFINITION_ONLY=90`,
`PARTIAL_FORMALIZATION=94`, `SOURCE_THEOREM_UNFORMALIZED=82`,
`NOT_YET_FORMALIZED=1027`, `PARSE_REVIEW_REQUIRED=5`다. declaration은 283개이고
금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed 2e-17과 X_cert는 계속 OPEN이다.

2026-09-14 Theory 80 batch는 actual FMT joint law의 normalized squared
weighted-correlation badness와 global/conditional/fiberwise finite gate를 고정했다.
Lean은 finite tower sum identity, global strict moment gate의 positive terminal,
conditional product positivity, raw second-moment denominator identity와 positive
division monotonicity를 검사한다. Markov 확률정리의 actual 적용, FMT analytic law와
Dirichlet-character moment upper는 premise도 project-local axiom으로 만들지 않았다.

Theory 80 뒤 inventory는 theory 문서 81개, display 1,473식이며 전체 상태는
<code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=64</code>,
<code>DEFINITION_ONLY=98</code>, <code>PARTIAL_FORMALIZATION=100</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=85</code>,
<code>NOT_YET_FORMALIZED=1027</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.
declaration은 288개이고 금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed
2e-17과 X_cert는 계속 OPEN이다.

2026-09-15 Theory 81 batch는 Theory 55 survivor floor의 actual event domain을
final sieve-good (S_{\rm sieve}=O\cap I_{\rm good})로 교정했다. Lean은 그 floor의
positive terminal, 같은 사건 raw-moment의 positive-denominator normalization,
strict moment gate의 positive terminal, symmetric-difference count terminal과
(P=65) counterexample의 integer arithmetic을 검사한다. FMT probability law,
Dirichlet-character evaluation 전체, martingale increment·conditional variance와
analytic second moment는 project-local axiom으로 넣지 않았다.

canonical direct compile은 최종 exit code 0, 독립 전체 build는
<code>Build completed successfully (8765 jobs)</code>와 exit code 0을 확인했다.
<code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>은 0건이다.

Theory 81 뒤 inventory는 theory 문서 82개, display 1,499식이며 전체 상태는
<code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=66</code>,
<code>DEFINITION_ONLY=107</code>, <code>PARTIAL_FORMALIZATION=108</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=88</code>,
<code>NOT_YET_FORMALIZED=1031</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.
declaration은 293개이고 금지 proof escape는 0건이다. PAP-11, DEP-R09, fixed
2e-17과 X_cert는 계속 OPEN이다.

2026-09-15 Theory 82 batch는 FMT outer residue의 uniform law와 final-coordinate
보존에서 final CRT shift atom cap \(1/Q_{\mathcal S}\)를 얻고, finite Parseval과
cyclic convolution을 actual final sieve-good raw moment에 합성했다. Lean은
<code>rawMoment <= shiftEnergy/Q</code>와 convolution energy premise를 결합하는
terminal 및 strict character-energy gate에서 Theory-81 normalized gate로 가는 실수
부등식만 검사한다. FMT probability law, finite character orthogonality, 복소수
convolution Cauchy와 analytic prime-error energy upper는 local axiom으로 넣지 않았다.

canonical direct compile은 exit code 0이었다. 전수 inventory refresh·validation도
PASS했고 <code>sorry</code>, <code>admit</code>, project-local <code>axiom</code>은
0건이다.
독립 전체 build도 <code>Build completed successfully (8765 jobs)</code>,
exit code 0으로 끝났다.

Theory 82 뒤 inventory는 theory 문서 83개, display 1,528식이며 전체 상태는
<code>KERNEL_PASS=94</code>, <code>CONDITIONAL_KERNEL_PASS=69</code>,
<code>DEFINITION_ONLY=113</code>, <code>PARTIAL_FORMALIZATION=112</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=92</code>,
<code>NOT_YET_FORMALIZED=1043</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.
declaration은 295개이고 금지 proof escape는 0건이다. fully numerical
fixed-primorial character-energy upper, PAP-11, DEP-R09, fixed 2e-17과 X_cert는
계속 OPEN이다.

2026-09-15 Theory 83 batch는 prescribed fixed-primorial variance source range와
raw classical large-sieve certificate를 감사했다. Lean은
\(L\ge21t,\log2<t\)에서 \(5t<(L-\log2)/4\)인 선형 terminal, nonnegative
factor별 상계에서 best-entropy gate envelope로 가는 곱셈 단조성, 그리고
upper RHS가 strict gate 이상이면 \(V=gate\)가 논리적 countermodel이라는 명제를
단일 파일에서 검사한다. Montgomery--Vaughan large sieve, Dusart theta bound,
Rosser--Schoenfeld phi bound와 actual character energy는 local axiom으로 넣지 않았다.

canonical direct compile과 전수 inventory refresh·validation은 exit code 0이었다.
Theory 83 뒤 inventory는 theory 문서 84개, display 1,561식이며 전체 상태는
<code>KERNEL_PASS=96</code>, <code>CONDITIONAL_KERNEL_PASS=73</code>,
<code>DEFINITION_ONLY=119</code>, <code>PARTIAL_FORMALIZATION=120</code>,
<code>SOURCE_THEOREM_UNFORMALIZED=98</code>,
<code>NOT_YET_FORMALIZED=1050</code>, <code>PARSE_REVIEW_REQUIRED=5</code>다.
declaration은 300개이고 금지 proof escape는 0건이다. raw large-sieve path의
불충분성만 닫혔고 prime-specific/sparse-divisor energy, PAP-11, DEP-R09,
fixed 2e-17과 X_cert는 계속 OPEN이다.
