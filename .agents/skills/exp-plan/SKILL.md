---
name: exp-plan
description: FGKMT-Sono maximal prime-gap 연구의 test_plan 문서를 신설하거나 갱신한다. 실험계획, 단계 추가, 계획서 갱신 요청에 사용하며 승인 상태와 재현성 게이트를 빠뜨리지 않는다.
---

# Experiment plan

test_plan/P0NN_slug.md를 아래 순서로 작성한다.

1. 상태: PREPARATION_ONLY, WAITING_FOR_USER_APPROVAL, APPROVED, COMPLETED 중 하나
2. 연구 질문과 비목적
3. 수학 정의
   - G(x) = max over p_(n+1) <= x of p_(n+1) - p_n
   - log_k(x)는 자연로그를 k회 반복
   - F(x) = log(x) log_2(x) log_4(x) / log_3(x), H(x) = G(x) / F(x)
4. dataset 원천, pin한 commit, 파일 hash, 완전성 한계
5. 입력 필터와 record 복원 규칙
6. 사전검증 및 중단 조건
7. 승인 후 실행 명령
8. 표·그래프·요약 산출물
9. 판정 기준과 해석 제한
10. 후속 작업

실험 완료 뒤에는 원래 질문별 답, 실제 산출물 경로, 검증 결과, 실패나 편차를 같은 계획서에 갱신한다. 유한 계산으로 FGKMT/Sono의 무한 범위 정리를 검증했다고 표현하지 않는다.

