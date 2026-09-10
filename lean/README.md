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
독립 검증에 사용하지 않는다.

원문 theory를 수정한 뒤에는 생성기와 검증기를 차례로 실행한다. 생성기는 display 수식의
원문 경로·행·SHA-256을 다시 고정하며, 검증기는 전수 coverage, 선언 연결, 금지된 proof
escape, toolchain pin을 검사한다. `.lake/`는 로컬 build cache이므로 Git에 포함하지 않는다.
