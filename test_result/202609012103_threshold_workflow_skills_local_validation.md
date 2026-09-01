# Sono threshold 연구목표·작업규약 skill 개선 로컬검증

최종 갱신: 2026-09-01 21:03 KST

## 1. 범위와 판정

이번 작업은 문서·skill·절차 개선이며 actual 연구 계산을 수행하지 않았다.

```text
P018-A run directories/logs = 0 / 0
P018-A runner/READY         = present / present
cleanup candidate path      = absent after user deletion
project vocabulary test     = PASS
skill validation            = 3/3 PASS
git diff --check            = PASS
```

## 2. threshold 연구목표 검증

`docs/review/19_20260901_연구진행현황_가설이론_실험종합리뷰.md`와
`docs/METHODS.md`에 다음을 분리해 기록했다.

1. finite observed threshold \(X_{\mathrm{emp}}(B)\)
2. proof가 보장하는 numerical threshold \(X_{\mathrm{proof}}\)
3. 실제 부등식의 가장 작은 전역 threshold

기존 P003 정본 결과는 scale-positive 정수 정의역 `[3,814,280,10^20]`의 최소
\(H\approx37.8168604\)가 \(2\times10^{-17}\)보다 크므로
\(X_{\mathrm{emp}}(10^{20})=3{,}814{,}280\)임을 준다. 이 값은 Sono 정리의 proof threshold로
승격하지 않았다. Sono 출판본의 numerical \(X_0\)와 실제 전역 최소 threshold는 `OPEN`이다.

## 3. 적용한 workflow 개선

- `log-to-result`: empirical-envelope, recurrence, finite-certificate, information-probe profile
- `runner-retirement`: 실제 실행 file만 hash 보존 이관, 공통·downstream 입력 보존
- `research-status-synthesis`: evidence level·쉬운 설명·파일 section 참조·threshold 구분
- AGENTS: revision metadata, runtime 세 구분, negative outcome, tmp lifecycle, peak memory,
  artifact 불변, process-state 판정의 7개 불변식
- `ai_dev_tool` 01–04 갱신, 07 임시파일 격리·삭제 절차 신설
- 자동 삭제 skill은 만들지 않음

## 4. validator 기록

공식 `skill-creator/scripts/quick_validate.py` 첫 실행은 FGKMT와 Codex 번들 Python 모두
`ModuleNotFoundError: yaml`로 시작 전 실패했다. 패키지는 설치하지 않았다. validator source를
확인해 이번 두 줄짜리 flat frontmatter에만 적용되는 in-memory `safe_load` shim을 주입했다.

두 번째 실행은 Windows 기본 CP949 때문에 UTF-8 한국어를 읽지 못했다. Python `-X utf8`을
추가해 공식 validator의 이름·허용 key·description·TODO·fence 검사를 그대로 실행했고 다음 세
skill 모두 `Skill is valid!`를 반환했다.

- `.agents/skills/log-to-result`
- `.agents/skills/runner-retirement`
- `.agents/skills/research-status-synthesis`

중첩 YAML을 추가할 경우 이 shim을 확대하지 않고 정식 PyYAML 환경을 별도 승인받아야 한다.

## 5. 관련 회귀검증

고정 FGKMT Python:

```powershell
& 'W:\miniforge3\envs\FGKMT\python.exe' -B -m unittest tests.test_project_vocabulary -v
```

결과: 1 test PASS. `git diff --check`도 exit 0이다. Python 연구 source·actual artifact를
수정하지 않았으므로 P018-A와 전체 actual 계산은 실행하지 않았다.
