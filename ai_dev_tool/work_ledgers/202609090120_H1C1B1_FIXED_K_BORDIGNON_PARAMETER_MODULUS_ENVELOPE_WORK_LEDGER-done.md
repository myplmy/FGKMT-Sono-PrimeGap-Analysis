# H1c-1b.1 fixed-k 및 Bordignon parameter/modulus envelope 작업원장

- 시작: 2026-09-09 01:20 KST
- 현재 상태: COMPLETE
- 사용자 승인: 권장 순서에 따른 `H1c-1b.1` 착수와 필요한 학술자료 취득·검토
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090052_HANDOFF.md`

## 1. 목표

H1c-1a에서 주 합성 후보로 고른 Bordignon 2021 Theorem 1.4를 실제 FGKMT Hypothesis 1(2)와
Maynard Proposition 9.2에 연결하기 전에 다음 세 가지를 원문 기준으로 판정한다.

1. downstream Sono/FMT/FGKMT 적용에서 sieve dimension 또는 linear-form 수 `k`가 하나의
   유한 정수로 먼저 고정되는가, 아니면 `x`와 함께 증가하는 uniform 정리가 필요한가.
2. 필요한 log-saving exponent `A`를 하나의 유한 상수로 고정할 수 있는가.
3. 원래 modulus `q`, affine leading coefficient `a`, Bordignon의 `Q,Q1,q0,X0,C,E` 사이에
   누락 없는 finite coverage inequality를 만들 수 있는가.

가능하면 기존 논문의 lemma를 먼저 채택하되, 가정·정규화·유효범위·끝점·오류항을 실제 호출과
개별 대조한다. 적합한 선행정리가 없는 연결부만 project lemma 후보로 직접 증명한다.

## 2. 비목표·승인 경계

- H1c-1b.2의 common exceptional conductor/prime `B` 증명은 시작하지 않는다.
- `psi`에서 prime count로의 전체 변환, half-open endpoint 및 recentering은 H1c-1b.3에 남긴다.
- density와 common finite cutoff 합성은 H1c-1b.4에 남긴다.
- actual prime/maximal-gap sweep, P018-B, threshold calculator, 장시간 runner는 만들거나 실행하지 않는다.
- 미명시 상수나 유효범위를 추정값으로 닫지 않는다.
- package·Lean 설치, commit/push/PR/외부 게시는 별도 승인 없이 수행하지 않는다.

## 3. 변경 전 영향 분석

| 축 | 판정 | 근거·통제 |
|---|---|---|
| iterated log·end-bounded empirical 정의 | 영향 없음 | empirical 계산과 dataset을 수정·실행하지 않음 |
| theorem/empirical 구분 | 영향 있음 | parameter envelope만 닫고 `X_cert`와 root blocker는 fail-closed 유지 |
| proof dependency | 영향 있음 | H1c-1a의 R01/R02/R03/R06 일부와 H1c parent pointer를 갱신할 수 있음 |
| source provenance | 영향 있음 | Bordignon·Maynard·FGKMT 원문과 후속 교정본의 정확한 위치·hash 기록 |
| 큰 정수·수치 | 확인 필요 | symbolically 닫힌 scalar inequality만 FGKMT Python으로 보조검산 |
| 승인 경계 | 영향 있음 | 정적 문헌·증명 감사만 승인됨 |
| 재현성 | 영향 있음 | JSON proof contract와 negative-assertion 단위시험으로 상태 고정 |
| 정본 동기화 | 영향 있음 | theory 16/32, H1/H1c/T1, METHODS, 색인, AGENTS, review, handoff 점검 |

## 4. 단계별 진행 기록

### 단계 0 — 범위·상태 고정

- [x] 최신 handoff·AGENTS·승인 경계 확인
- [x] 시작 시 활성 작업원장 0개와 깨끗한 worktree 확인
- [x] 영향 분석과 H1c-1b.2 이후 비목표 기록
- 도구 오류: source 위치를 찾으면서 `tmp/` 전체에 `rg --files`를 실행해 접근 제한 경고가
  다수 발생했다. 파일 변경이나 연구 판정에는 영향이 없으며 이후에는 알려진 정확한 경로만 읽는다.
- 다음 재개점: 단계 1에서 실제 downstream `k` 선택과 quantifier 순서를 원문 식으로 복원한다.

### 단계 1 — fixed-k와 log exponent 복원

- [x] FMT/Sono/FGKMT에서 `k` 또는 `r` 선택 순서와 `x` 의존성 추적
- [x] Maynard Hypothesis 1의 `100 k^2`와 application의 정확한 의미 대조
- [x] fixed-k branch와 growing-k branch 중 실제 threshold proof에 필요한 branch 판정
- [x] 필요한 Bordignon exponent `A`의 안전한 symbolic 식 도출
- 결과:
  - outer chain parameter `k_chain=1`과 sieve/form dimension `r`는 서로 다른 매개변수다.
  - actual FGKMT Section 8에서 `k_Maynard=r`이고 `r=floor((log x)^(1/5))`이므로 필요한
    saving exponent는 고정 100이 아니라 growing `100 r^2`이다.
  - Bordignon Theorem 1.4의 quantifier는 모든 실수 `A>3`이므로 각 endpoint에서 조건을
    재검사하는 pointwise diagonal `A(r)=100 r^2+10`은 논리적으로 허용된다.
  - 표적 선행연구 검색에서 actual FGKMT `x/2` 호출과 최종 coefficient transfer까지 한 번에
    닫는 정리는 찾지 못했다. 이는 전 세계 비존재·novelty 판정이 아니다.

### 단계 2 — Bordignon parameter/modulus envelope

- [x] Bordignon Theorems 2/4의 `Q,Q1,q0,X0,C,E,A`와 유효조건 복원
- [x] affine modulus `|a|q`와 `q <= x^(1/3)`의 exact upper envelope 도출
- [x] source variable와 project variable의 scale 충돌·endpoint 위험 점검
- [x] 선행 lemma 적용 여부를 먼저 판정하고 빠진 연결부만 직접 증명
- 결과:
  - actual Proposition 9.2 호출은 식 (6.5)의 identity form `n`이므로 slope 확대가 없다.
    식 (6.4)는 prime-distribution clause를 쓰지 않고, 식 (6.6)의 actual distribution child는
    P94 경로에서 이미 별도로 닫혔다.
  - endpoint-safe `r>=36`에서 actual capacity
    `L/6 >= A(r) log L`와 보수적인 affine capacity
    `L/6 >= (A(r)+5/3) log L`를 exact rational/calculus certificate로 닫았다.
  - source `r_s=floor((log x)^(1/5))`를 actual scale `T=x/2`에 그대로 넣으면
    `r_s^5 <= log x < r_s^5+log 2`인 반복 transition strip에서 printed Maynard
    dimension 가정이 깨진다. 이는 finite cutoff로 제거할 수 없다.
  - exact repair `r_T=floor((log(x/2))^(1/5)) in {r_s-1,r_s}`와 `r_s-1`의 항상
    admissible함은 닫혔다. 그러나 한 단계 감소 뒤 FMT/Sono 정규화·최종 계수 보존은 OPEN이다.
  - Bordignon Theorem 1.4의 `C(A,A-3,X0)` 표기는 앞 정의의 세 번째 인수 `Y0=loglog X0`와
    형식상 긴장이 있어, 원문을 임의로 고치지 않고 향후 explicit constant 재유도 의무로 남겼다.

### 단계 3 — 정본·기계 계약 작성

- [x] H1c-1b.1 theory 문서와 비판적 review 작성
- [x] source/equation/dependency/status JSON 계약 작성
- [x] consistency·negative assertion 단위시험 작성
- [x] predecessor와 METHODS·색인·AGENTS를 근거 범위에서 동기화
- 산출물:
  - `docs/method/theory/33_Sono_FMT_H1c1b1_parameter_modulus_envelope.md`
  - `docs/review/39_20260909_H1c1b1_parameter_modulus_envelope_타당성검토.md`
  - `docs/method/theory/data/Sono_FMT_H1c1b1_parameter_modulus_envelope_v1.json`
  - `source/h1c1b1_parameter_modulus_envelope.py`
  - `tests/test_h1c1b1_parameter_modulus_envelope.py`
- provenance 교정:
  - H1c-1a JSON에 잘못 기록됐던 Maynard PDF 경로·SHA-256을 실제
    `Dense Clusters of Primes in Subsets` 출판본으로 교정했다.
- 정본 동기화:
  - theory 색인, T1/H1/H1b/H1c/H1c-1a, review 38, `docs/METHODS.md`, `AGENTS.md`에
    부분 성공과 다음 gate `H1c-1b.1a`를 반영했다.

### 단계 4 — 검증·handoff

- [x] FGKMT Python py_compile·표적·전체 unittest
- [x] JSON strict parse·Markdown local links·`git diff --check`
- [x] 오류·실패 원장 갱신
- [x] 새 timestamp handoff와 다음 권장 순서·예상시간·한국어 commit 메시지 작성
- [x] 모든 완료조건 뒤 작업원장을 `-done.md`로 이름 변경
- 검증:
  - py_compile: PASS
  - H1c-1b.1 및 직접 영향 표적 test: 42/42 PASS
  - JSON strict parse: 23/23 PASS
  - 수정 Markdown local links: 103/103 PASS
  - ASCII control scan: 27개 변경 파일 issue 0
  - `FGMT` 오탈자 scan: 16개 핵심 파일 issue 0
  - stale next-gate scan: issue 0
  - `tests/test_live_native_tee.py`의 기존 비결정적 stream-order 가정 수정 뒤 10/10 반복 PASS
  - 전체 suite 정상 로컬 권한: `Ran 352 tests in 35.583s / OK`
  - `git diff --check`: whitespace error 0, LF/CRLF 안내만 존재
- 검증 중 환경·시험 이력:
  - sandbox 안의 첫 전체 실행은 임시 폴더 권한으로 82개 `PermissionError`를 냈다.
    동일 명령을 승인된 정상 로컬 권한에서 재실행해 전부 통과했다.
  - live tee test는 수정 전 반복 5회 중 4 PASS·1 FAIL로 race를 재현했다. production helper는
    바꾸지 않고 stream별 재구성 oracle로 교정했다.
- 오류 원장: E039--E043에 도구 escape, Maynard provenance, dyadic 경계 누락,
  live tee flaky oracle, Bordignon theorem 번호 교정을 기록했다.
- handoff: `handoff/202609090254_HANDOFF.md`

## 5. 현재 재개점

H1c-1b.1은 완료됐다. 다음 작업은 사용자 승인 뒤 H1c-1b.1a에서 dyadic
`r_s -> r_T` 또는 `r_s-1` 교체가 FMT/Sono 최종 정규화와 explicit coefficient를
보존하는지 증명하는 것이다. actual experiment·threshold calculator는 계속 미승인이다.
