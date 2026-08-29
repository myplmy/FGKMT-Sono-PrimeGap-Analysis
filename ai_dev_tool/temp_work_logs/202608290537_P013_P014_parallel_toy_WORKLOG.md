# P013 segment·P014 exact-scan 병렬 toy 작업로그

- 시작: 2026-08-29 05:37 KST
- 사용자 승인 범위: P013 유사 실험 재사용 가능성 판단, segment 병렬화 toy 구현·검증,
  P014 새 revision toy 구현·검증
- 금지 범위: P013/P014 actual 계산, 기존 정본 runner의 병렬판 승격, 데이터 재분석,
  외부 다운로드·설치·commit·push
- 정확성 원칙: serial 정본과 exact 결과가 다르면 즉시 FAIL하며 속도 때문에 근사·샘플링 축소·
  constraint 생략을 허용하지 않는다.

## 단계 현황

1. **완료 — 저장소·실행 상태·승인 경계 확인**
   - 작업 시작 시 Git tracked/untracked 상태는 clean.
   - P013-B Python process는 더 이상 실행 중이지 않지만 기존 main log는
     `p013b-saved-full-recomputation` 시작에서 끝나 terminal PASS는 확인되지 않았다.
   - 현재 작업은 P013-B 결과 판정과 분리한다.
2. **완료 — 영향도 분석과 실험계획 작성**
   - 영향도: `docs/method/20260829_P013_P014_parallelization_impact_analysis.md`
   - P013 toy 계획: `test_plan/P016_P013_segment_parallel_toy.md`
   - P014-R2 toy 계획: `test_plan/P014R2_parallel_exact_scan_toy.md`
3. **완료 — P013 segment 병렬 toy 구현·검증**
   - 별도 모듈 `source/parallel_segment_statistics.py`와 worker 1/2/4/8 exact-equivalence
     테스트를 작성했다.
   - 68,906 gap starts·32 segments 통합 toy에서 serial exact equality와 worker 8개 관측 PASS.
4. **완료 — P014 exact constraint-scan 병렬 revision toy 구현·검증**
   - 별도 모듈 `source/finite_gap_parallel_exact_scan.py`와 feasible/infeasible serial 대조,
     worker 1/2/4/8, top-k tie 결정성 테스트를 작성했다.
   - synthetic modulus 30030·threshold 1856·35,224,647 constraints 통합 toy에서
     serial exact equality와 worker 8개 관측 PASS.
   - worker immutable arrays는 process당 1회 초기화하고 8-worker 시작 barrier·참여 fail-closed를
     적용했다.
5. **완료 — 전체 회귀검증·문서·핸드오프**
   - targeted 7/7 (`17.099s`), 통합 toy PASS, 전체 unittest 158/158 (`24.422s`),
     py_compile PASS.
   - 검증 보고서: `test_result/202608290552_P013_P014_parallel_toy_local_validation.md`.
   - 최신 handoff: `handoff/202608291417_HANDOFF.md`.

## 재개 규칙

- 이 파일에서 첫 `진행 중` 또는 `대기` 단계를 찾는다.
- 새 병렬 구현은 기존 serial 함수를 대체하지 않고 별도 모듈에 둔다.
- toy exact-equivalence와 worker-count invariance가 모두 PASS하기 전에는 actual runner에 연결하지 않는다.
