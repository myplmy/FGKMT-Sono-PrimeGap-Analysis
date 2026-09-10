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

2026-09-10 Theory 55 batch에서는 식 (55.24)--(55.35)의 smooth-remainder 경로를
초등 계산과 외부 해석 입력으로 분해했다. 식 (55.32), (55.34)는 독립
`KERNEL_PASS`이고, 기존 식 (55.33)도 같은 상태다. Rankin counting, 명시적
prime-harmonic bound, Stieltjes 비교를 premise로 받는 downstream 합성은
`CONDITIONAL_KERNEL_PASS`다. 식 (55.27)은 `SOURCE_THEOREM_UNFORMALIZED`, 식
(55.28)은 유한구간 적분 비교가 남은 `PARTIAL_FORMALIZATION`이다. 따라서 이 batch도
smooth-number source theorem 전체나 `X_cert`를 인증하지 않는다.

원문 theory를 수정한 뒤에는 생성기와 검증기를 차례로 실행한다. 생성기는 display 수식의
원문 경로·행·SHA-256을 다시 고정하며, 검증기는 전수 coverage, 선언 연결, 금지된 proof
escape, toolchain pin을 검사한다. `.lake/`는 로컬 build cache이므로 Git에 포함하지 않는다.
