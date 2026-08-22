---
name: run-batch
description: FGKMT-Sono 실험용 PowerShell 실행기를 작성·수정·검증한다. 고정 Conda Python, 사용자 승인 플래그, 단계별 실패 처리와 비덮어쓰기 규칙을 강제한다.
---

# Run batch

이 프로젝트의 표준 실행기는 run_experiment.ps1이다.

## 규칙

- Python은 W:\miniforge3\envs\FGKMT\python.exe로 고정한다.
- 실제 dataset 취득이나 분석은 명시적 Approved 매개변수 없이 시작할 수 없어야 한다.
- 실행기 내부에서도 Python CLI의 --approved-by-user 게이트를 통과해야 한다.
- source commit, analysis limit, run id를 명시적으로 전달하고 출력한다.
- fetch, validate, analyze 단계의 실패 코드를 보존하며 후속 단계를 실행하지 않는다.
- raw, validated, results 경로는 불변 commit/run-id 디렉터리를 사용하고 기존 파일을 덮어쓰지 않는다.
- stdout와 stderr를 실행별 로그에 보존하도록 설계한다.
- 승인 전에는 구문 검사와 dry-run, 합성 테스트만 수행한다.

여러 독립 실험이 필요하면 한 실험당 하나의 실행기나 run id를 쓰고, orchestration과 분석 코드를 분리한다.

