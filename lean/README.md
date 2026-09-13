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
actual `tau=8/5`에 대입한 coefficient `18884947/500000`과 finite log-ratio 대수를
`KERNEL_PASS`로 검증했다. finite power correction은 exponent 대수만
`PARTIAL_FORMALIZATION`이다. 외부 Barban--Vehov·Jutila·Huxley 정리는 local axiom으로
가정하지 않았다. 새 12식 뒤 inventory는 theory 문서 61개, display 1,068식,
`NOT_YET_FORMALIZED` 971식이며 금지 proof escape는 0건이다. `JL5/JL6/JL8`, PAP-11,
fixed `2e-17`, `X_cert`는 OPEN이다.

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
