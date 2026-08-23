# 데이터 영역

P002/P003 승인 실행으로 canonical 원본·검증자료와 독립 대조 원본이 생성됐다. 정본 입력은 Prime Gap List Project의 GitHub 저장소에 있는 commit-pinned `allgaps.sql`이며, canonical 웹 표는 사람이 coverage를 확인하는 참고 화면으로만 사용한다.

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
  raw/independent/oeis/<run-id>/
    A002386_b.txt
    A005250_b.txt
    metadata.json
  raw/independent/oliveira/<run-id>/
    t0.txt.gz
    metadata.json
```

- `raw/` 파일은 commit별 불변 원본이다. 같은 경로를 덮어쓰지 않는다.
- metadata.json에는 commit과 두 파일 각각의 commit 고정 raw URL, 취득 UTC, byte 수, SHA-256을 기록한다.
- OEIS는 full-range 독립 공개 표현이며 계산 계보의 완전 독립성은 주장하지 않는다.
- Oliveira e Silva 표는 별도 exhaustive computation 자료로 `4e18`까지 중첩 대조한다.
- independent 원본도 run별 불변 경로에 저장하고 URL, 취득 UTC, SHA-256, 경계·coverage 의미를 기록한다.
- `validated/`의 큰 정수 열은 부동소수점 손실을 막기 위해 CSV에 10진 문자열로 쓴다.
- 실제 (G(x)) 복원 범위는 별도 exhaustive-limit 출처로 제한한다. 최신 발견 목록과 완전 탐색 범위를 같은 것으로 취급하지 않는다.

현재 authoritative pin, P003 run, independent source URL·hash·coverage는 [source_registry.json](source_registry.json)에 있다. future acquisition은 기존 경로를 덮어쓰지 않고 새 commit 또는 run ID 디렉터리를 만든다.
