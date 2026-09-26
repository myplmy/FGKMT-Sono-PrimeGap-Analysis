# DEP-R09 weighted survivor-moment source 감사 작업원장

- 시작: 2026-09-27 07:19 KST
- 기준 commit: <code>8aee8ba</code>
- 목표: FGKMT fixed 1·2-point survival theorem이 arbitrary complex blind weights에
  주는 exact second-moment upper를 도출하고, weighted Rödl-nibble 선행정리의
  actual-law 적용 가능성을 감사한다.
- 승인·금지 범위: 이전 ledger와 동일.

## 영향도

| 축 | 판정 | 통제 |
|---|---|---|
| same-law weighted moment | 직접 영향 | complex fixed weights와 survival indicators를 동일 law에서 평균 |
| source theorem | 영향 있음 | 2025 Gould--Kelly weighted nibble 원문 추가 |
| quantifier | 결정적 | preselected weights와 output-dependent weights 구분 |
| numerical rate | 결정적 | qualitative hierarchy를 explicit cutoff로 승격 금지 |
| construction | 유지 | matching theorem을 current covering law로 자동 교체하지 않음 |
| empirical/actual | 영향 없음 | 계산·dataset 미사용 |

## 접근 비교

| 접근 | 장점 | 한계 | 선택 |
|---|---|---|---|
| FGKMT 1·2-point weighted second moment | same law, exact finite derivation | pair-error spectral loss \(\beta M\) | **우선 도출** |
| Gould--Kelly pseudorandom matching | weighted functions 명시 | uniform regular matching·nonnegative·qualitative | source applicability 감사 |
| martingale bounded difference | general | Theory 81 phase increment \(2N\), variance 입력 없음 | 보류 |
| direct prime-specific mean/L2 | analytic target에 밀착 | 새 number-theory theorem 필요 | 다음 gate |

## 단계 현황

1. **DONE — weighted nibble primary source 다운로드·hash 고정**
2. **DONE — arbitrary complex weighted second-moment exact reduction**
3. **DONE — \(\beta M\) loss와 finite sharpness witness**
4. **DONE — Gould--Kelly applicability 판정**
5. **DONE — Theory 91·review 100·Python·Lean·verification**
6. **DONE — Theory 92 successor로 stopping condition 재판정**

### 2026-09-27 07:47 KST — Theory 91 완료

- fixed complex weights의 exact second moment와 entrywise pair-error certificate를
  도출했다.
- latent common-shock law가 \(\beta M\) operator scaling을 exact하게 달성함을 finite
  rational 전수로 확인했다.
- Gould--Kelly 2025 Theorem 1.4는 weighted matching source지만 current variable-size
  indexed covering actual law의 numerical second moment에는 drop-in하지 않는다.
- 새 helper 8 tests, Lean scalar terminals, verification inventory가 PASS했다.
- successor Theory 92는 blind-specific pointwise envelope를 써 success-scale pair
  factor를 \(\beta\)로 정규화했다. 따라서 이 ledger의 arbitrary-weight operator
  진단은 유지되지만 최신 root gate는 sparse centered mean이다.
- actual prime/dataset 실험, package 설치, threshold calculator, long computation,
  GRH branch, push/PR은 수행하지 않았다.
