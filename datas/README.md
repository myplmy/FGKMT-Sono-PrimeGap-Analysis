# 데이터 영역

이 디렉터리는 실제 실험 승인 전에는 데이터 파일을 포함하지 않는다. 정본 입력은 Prime Gap List Project의 GitHub 저장소에 있는 `allgaps.sql`이며, 웹 표는 사람이 확인하는 참고 화면으로만 사용한다.

승인 후 파이프라인은 다음 구조를 만든다.

```text
datas/
  raw/prime-gap-list-project/<40자 commit>/
    allgaps.sql
    schema.sql
    metadata.json
  validated/prime-gap-list-project/<40자 commit>/
    maximal_gap_records.csv
    validation_report.json
```

- `raw/` 파일은 commit별 불변 원본이다. 같은 경로를 덮어쓰지 않는다.
- metadata.json에는 commit과 두 파일 각각의 commit 고정 raw URL, 취득 UTC, byte 수, SHA-256을 기록한다.
- `validated/`의 큰 정수 열은 부동소수점 손실을 막기 위해 CSV에 10진 문자열로 쓴다.
- 실제 (G(x)) 복원 범위는 별도 exhaustive-limit 출처로 제한한다. 최신 발견 목록과 완전 탐색 범위를 같은 것으로 취급하지 않는다.

현재 source 설정과 사전 확인값은 [source_registry.json](source_registry.json)에 있다. 실제 취득 시에는 `master`를 다시 resolve한 뒤 그 40자 commit으로 URL을 고정한다.
