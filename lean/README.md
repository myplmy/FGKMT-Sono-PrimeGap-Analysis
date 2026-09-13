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
& 'W:\miniforge3\envs\FGKMT\python.exe' tools\generate_verification_ledger.py
& 'W:\miniforge3\envs\FGKMT\python.exe' tools\validate_verification_ledger.py
```

`lake build` 성공만으로 모든 논문 입력이 증명된 것은 아니다. 항목별 독립·조건부·미형식화
상태는 `VERIFICATION_LEDGER.md`를 정본으로 삼는다. `sorry`, `admit`, project-local `axiom`은
독립 검증에 사용하지 않는다. 불가피해 보이면 형식화 불가 사유, 대체 공식·방법,
외부 검증 선행연구를 먼저 감사·보고하고 사용자의 명시적 허가 전에는 절대 도입하지
않는다.

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
