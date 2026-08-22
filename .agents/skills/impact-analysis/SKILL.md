---
name: impact-analysis
description: 비자명한 구현이나 연구 방법 변경 전에 프로젝트 수학, 데이터, provenance, 승인, 재현성에 미치는 영향을 분석한다. 영향도 검토나 접근법 비교 요청에 사용한다.
---

# Impact analysis

프로젝트 설정은 ../../project.json에서 읽는다.

## 변경 전 확인 축

- 수학 정의와 iterated logarithm
- end-bounded record 의미론
- dataset provenance, commit pin, 완전성
- 큰 정수와 고정밀도 수치
- 사용자 승인 경계
- 검증, 통계, 그래프 재현성
- 정리와 경험적 결론의 구분
- 문서, 테스트, 핸드오프 파급

각 축을 영향 있음, 영향 없음, 확인 필요로 판정하고 근거 파일을 적는다. 실제 선택지가 존재할 때만 최소 3개 접근을 정확성, 재현성, 비용, 위험으로 비교해 권장안을 제시한다. 이미 canonical 문서가 결정한 사항에는 불필요한 대안을 만들지 않는다.

