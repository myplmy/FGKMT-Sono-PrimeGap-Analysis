# H1c-1b.1a dyadic dimension-to-coefficient transfer 작업원장

- 시작: 2026-09-09 04:08 KST
- 현재 상태: COMPLETE
- 사용자 승인: \(X_{\mathrm{cert}}\) 계산기 전 정규화·증명 작업을 권장 순서대로 진행.
  현재 turn의 commit 요청은 메시지 제안이며 실제 commit 승인은 아님
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090254_HANDOFF.md`
- 시작 Git 상태: branch `main`, clean worktree

## 1. 목표

Sono/FMT가 원래 scale \(x\)에서 고른
\[
r_s=\lfloor(\log x)^{1/5}\rfloor
\]
를 actual Maynard 호출 scale \(T=x/2\)에 맞춘
\[
r_T=\lfloor(\log(x/2))^{1/5}\rfloor\in\{r_s-1,r_s\}
\]
로 교체했을 때 다음을 원문 식에 따라 판정한다.

1. FMT Theorem 6과 Sono Proposition 6.2의 \(r\)-dependent main term·weight·확률식이
   그대로 유효한가.
2. \(r\to r-1\) 손실을 finite exact ratio로 묶을 수 있는가.
3. 최종 \(\log_4x/\log_3x\) 정규화와 Sono의 \(2\times10^{-17}\) 계수를 보존할 수 있는가.
4. 보존되지 않으면 가장 가까운 보수적 계수와 추가 slack 의무를 fail-closed로 제시한다.

필요 lemma는 원 논문·교정본·후속 선행증명에서 먼저 찾고, 실제 가정·변수·endpoint·오류항을
대조한다. 적합한 선행정리가 없는 연결부만 project finite lemma로 직접 증명한다.

## 2. 비목표·승인 경계

- H1c-1b.2 common exceptional \(B\), H1c-1b.3 exact count transfer,
  H1c-1b.4 density·common cutoff는 이번 단계에서 닫지 않는다.
- P91/P92/L93/P95 전체 moment budget을 소급해 완료 처리하지 않는다.
- actual prime/maximal-gap sweep, P018-B, threshold calculator, 장시간 runner는 실행하지 않는다.
- package·Lean 설치는 필요성이 확인되기 전 수행하지 않는다.
- push, PR, 외부 게시는 수행하지 않는다.
- 로컬 stage·commit은 검증·handoff 뒤 이번 변경의 명시 경로만 대상으로 한다.

## 3. 변경 전 영향 분석

| 축 | 판정 | 근거·통제 |
|---|---|---|
| iterated log·end-bounded empirical 정의 | 영향 없음 | empirical dataset·\(G,H,F\) 계산을 실행·변경하지 않음 |
| theorem/empirical 구분 | 영향 있음 | coefficient transfer만 판정하고 \(X_{\mathrm{cert}}\)를 계산하지 않음 |
| proof dependency | 영향 있음 | H1c-1b.1 successor와 T1/H1/H1b/H1c 상태를 근거 범위에서 갱신 |
| source provenance | 영향 있음 | FMT·Sono·FGKMT·Maynard의 실제 식·페이지·hash를 고정 |
| 큰 수·정밀도 | 확인 필요 | symbolic ratio 뒤 scalar endpoint만 FGKMT Python으로 보조검산 |
| 승인 경계 | 영향 있음 | 정적 증명·toy 검산만 수행; heavy/actual 계산 없음 |
| 재현성 | 영향 있음 | JSON proof contract와 positive/negative regression 작성 |
| Git | 영향 있음 | 29개 allowlist staged audit 뒤 commit 미승인 판정으로 index 복원; push 없음 |

## 4. 단계별 진행 기록

### 단계 0 — 상태·범위 고정

- [x] 최신 AGENTS·handoff·완료 H1c-1b.1 원장 확인
- [x] branch `main`, clean worktree, 활성 작업원장 0개 확인
- [x] 영향 분석·비목표·승인 경계 기록
- 다음 재개점: FMT/Sono의 \(r\)-dependent 최종 계수 경로를 source 식 단위로 복원한다.

### 단계 1 — 선행증명·source 식 감사

- [x] FMT Theorem 6 proof의 \(r,u,c_0\), weight와 final interval-length 식 추적
- [x] Sono Proposition 6.2의 explicit constants와 \(r\)-선택 식 추적
- [x] FGKMT actual \(x/2\) 호출과 Maynard dimension 가정 재대조
- [x] \(r\to r-1\) transfer를 이미 다룬 선행 lemma 표적 조사

완료 증거:

- FMT Theorem 6 (6.1), (6.3), (6.8)과 Theorem 4/5의
  \(C\ge(5/4)\log5\) 경로를 원문에서 재대조했다.
- Sono Proposition 6.2 (6.5), pp.541--542에서
  \(160\) 대 \(150\) 선택이 limiting lower value
  \((4/3)\log5\)와 요구치 \((5/4)\log5\) 사이 정확히 \(16/15\)의
  비율 여유를 만든다는 것을 복원했다.
- FGKMT Section 8의 실제 선택은 \(R=(x/4)^{\theta/3}\)이고 prime-weighted
  moment는 \(T=x/2\)에서 호출됨을 확인했다. 따라서 차원 보정 외에도
  \(\log R/\log x=(\theta/3)(1-\log4/\log x)\)를 유한식에 포함해야 한다.
- H1a project theorem이 모든 정수 \(r\ge36\)에서
  \(J_r/I_r>\log r/(4r)\)를 이미 exact하게 제공함을 확인했다.
- arXiv의 FMT v1, FGKMT v3 metadata와 표적 검색을 확인했으나, 이 dyadic floor
  보정과 Sono의 explicit coefficient를 함께 처리한 선행 lemma·erratum은 찾지 못했다.
  이는 전 세계 비존재 주장이 아니다.
- 기존 T1 JSON의 `SIV-03`에서 \(\sigma y\) main term을
  `80c*x*log_2 x/log x`로 잘못 적은 provenance 오류를 발견했다. 원문 (6.11)/(6.12)와
  Sono p.542의 정확한 값은 `80c*x*log_2 x`이며, `/log x`는 survivor count
  \(\sigma y/\log x\)에만 나타난다. 정본 동기화 단계에서 교정한다.

다음 재개점: endpoint-safe
\(r=\lfloor(\log(x/2))^{1/5}\rfloor\)를 쓰고, dimension·실제 \(R\)·Mertens
upper slack을 합친 exact coefficient-transfer lemma를 정식화한다.

### 단계 2 — finite coefficient-transfer lemma

- [x] source main-term ratio의 정확한 \(r\)-의존성 도출
- [x] floor transition strip 전체에서 worst-case ratio 인증
- [x] \(\log_4x/\log_3x\) normalization과 explicit coefficient 보존 판정
- [x] 열린 입력을 분리하고 parent gate를 fail-closed 유지

완료 증거:

- endpoint-safe \(r=\lfloor(\log(x/2))^{1/5}\rfloor\ge36\)에서
  \(5\log r/\log_2x>63/64\)를
  \(36^{64}>38^{63}\)으로 exact 인증했다.
- 실제 \(R=(x/4)^{\theta/3}\) factor는
  \(1-\log4/\log x>104/105\)이고, 두 factor의 곱은
  \((63/64)(104/105)=39/40\)이다.
- \(\sigma y\le(26/25)80cx\log_2x\)이면 net factor가 \(15/16\)이고,
  Sono의 원래 \(16/15\) slack과 합성해
  \(C>(5/4)\log5\)를 얻는다.
- 따라서 endpoint repair 때문에 \(2\times10^{-17}\) 계수를 낮출 필요는 없지만,
  \(26/25\) gate의 explicit cutoff, `SIV-07/08`과
  \(X_{\mathrm{cert}}\)는 OPEN으로 유지했다.

### 단계 3 — 기계 계약·회귀시험

- [x] theory/review/JSON 작성
- [x] exact·고정밀도 보조검산 모듈 작성
- [x] positive/negative assertion 단위시험 작성

완료 증거:

- 정본 `34_Sono_FMT_H1c1b1a_dyadic_dimension_coefficient_transfer.md`,
  비판적 검토 `40_20260909_H1c1b1a_dyadic_coefficient_transfer_타당성검토.md`,
  machine contract `Sono_FMT_H1c1b1a_dimension_coefficient_transfer_v1.json`을 작성했다.
- `source/h1c1b1a_dimension_coefficient_transfer.py`는 정수·유리수 certificate와
  high-precision sample check를 분리한다.
- 새 시험 6개는 endpoint, strict slack, fail-closed status, source hash와 T1 교정을 검사한다.
- 표적 48개 최초 실행은 옛 `next_gate` 기대값 2건으로 실패했다. 이를 새 successor와
  실제 JSON key에 맞춰 고친 뒤 48/48 PASS를 확인했다. 해당 실수는 오류 원장 E047에 남겼다.

### 단계 4 — 정본 동기화

- [x] H1c-1b.1 predecessor와 H1c/H1b/H1/T1 갱신
- [x] METHODS·이론 색인·AGENTS를 근거 범위에서 갱신
- [x] 오류·교정 원장 갱신

완료 증거:

- predecessor·H1c·H1b·H1·T1 JSON의 successor와 next gate를 동기화했다.
- T1 `SIV-03`의 잘못된 \(\sigma y\) 주항 `/log x`를 제거했다.
- AGENTS, METHODS, 이론 색인, threshold/H1 review까지 현재 상태와
  다음 `H1c-1b.1a.1 / SIV-03` gate를 반영했다.
- 도구·경로·schema·provenance 오류 E044--E050을 오류 원장에 기록했다.

### 단계 5 — 검증·handoff·commit

- [x] py_compile·표적 unittest
- [x] 전체 unittest
- [x] JSON strict parse·Markdown links·control chars·오탈자·`git diff --check`
- [x] 새 timestamp handoff 작성
- [x] 명시 경로만 stage하고 staged diff 감사한 뒤 index 복원
- [x] 로컬 commit 미수행·한국어 메시지 제안만 제공
- [x] 모든 완료조건 뒤 작업원장을 `-done.md`로 전환

현재 검증 증거:

- py_compile: 변경 Python 4개 PASS
- 새 H1c-1b.1a 및 직접 영향 표적: 48/48 PASS
- project vocabulary 보정 시험: 1/1 PASS
- 전체 suite 정상 로컬 권한:
  `test_[a-m]*.py` 264/264 PASS,
  `test_[n-z]*.py` 94/94 PASS,
  합계 358/358 PASS
- 최초 sandbox 전체 실행은 임시 디렉터리 권한으로 82개 `PermissionError`가 발생해
  코드 판정에서 제외했고, 정상 로컬 권한에서 같은 suite를 재검증했다.
- JSON strict parse: 24/24 PASS
- exact certificate:
  `39/40`, `26/25`, `15/16`, 최종 \(C\) multiplier `5/4`,
  `X_CERT_READY=False`
- 최종 변경 Markdown 17개 local link 139개 PASS, control character issue 0
- 최초 정적검사 명령의 배열 결함은 결과를 폐기하고 교정 실행했다. 오류 원장 E049 참조.
- `git diff --check`: exit 0, line-ending 안내만 있음
- 명시 29개 staged path와 staged `diff --check`를 감사했다.
- 승인 검토가 현재 turn의 commit 실행을 거부했고 우회하지 않았다. 29개 경로를
  `git restore --staged`로 해제해 staged count 0을 확인했다. 오류 원장 E051 참조.

## 5. 현재 재개점

이번 작업은 완료됐다. 다음 정적 연구 gate는 H1c-1b.1a.1 / `SIV-03` explicit
\(\sigma y\) cutoff다. actual prime 계산이나 추가 설치는 하지 않는다.
