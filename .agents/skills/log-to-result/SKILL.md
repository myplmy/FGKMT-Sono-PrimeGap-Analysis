---
name: log-to-result
description: 사용자 승인 하에 생성된 FGKMT maximal-gap 실행 로그, validation report, 표와 그래프를 검증해 test_result 결과 문서와 계획·핸드오프를 갱신한다.
---

# Log to result

실제 실행이 승인되었고 산출물이 존재할 때만 적용한다.

## 검증

1. raw 및 normalized 입력 hash, source commit, 취득 시각을 validation report와 대조한다.
2. Python 경로, 패키지 버전, 코드 hash, precision을 확인한다.
3. rejected row와 high-watermark 불일치가 0인지 확인한다.
4. 일부 record를 독립 재계산해 start + gap = end와 H, Sono ratio를 대조한다.
5. interval minimum은 각 end-bounded record interval의 오른쪽 끝에서 계산되었는지 확인한다.
6. running minimum이 비증가인지 확인한다.
7. 기존 산출물을 덮어쓴 흔적이 없는지 확인한다.

## 결과 문서

- 연구 질문과 핵심 정의
- 원천 commit, hash, coverage 및 검증 상태
- H(x)의 interval 변화와 record jump 회복
- empirical lower envelope와 running minimum
- Wolf 계열 관찰과의 비교
- Sono 2e-17 scale 대비 ratio
- Cramér 정규화는 보조 진단으로만 분리
- 이상 구조, 민감도, 한계, 후속 연구

유한 범위에서 부등식이 관찰된 사실을 무한 범위 정리의 검증이나 재증명으로 표현하지 않는다. 결과 반영 후 test_plan과 HANDOFF.md의 상태·경로·다음 작업도 갱신한다.

