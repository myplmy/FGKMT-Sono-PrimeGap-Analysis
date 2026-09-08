# Sono/FMT H1c-1b.3 endpoint/count transfer 작업원장

- 시작: 2026-09-09 07:55 KST
- 현재 상태: DONE
- 직전 goal turn 판정: PROGRESS — H1c-1b.2 정본·검산 코드·372개 전체 회귀와
  local commits `4e933508edc3855cceb0d4d5222950df0ac15576`,
  `d1e207f33f5a6ba6e8d04cc7956b44d7749740c7`를 확인했다.
- 사용자 승인: `X_cert` 계산기 전의 정규화·증명을 권장 순서대로 수행한다. 필요한 lemma는
  원 논문·교정·후속 선행증명을 먼저 조사하고, 실제 적용이 맞는지 개별 대조한 뒤 빠진
  연결만 직접 증명한다. 단계 완료 후 명시 경로로 local stage·commit한다.
- 중단 조건: 새 논문/학술자료를 직접 확보할 수 없거나, Lean·새 Python package 또는
  장시간 계산이 실제로 필요하면 사용자에게 요청하고 일시 중단한다.
- 금지·보류: actual prime/maximal-gap sweep, P018-B, threshold calculator, 장시간 계산,
  임의 상수 선택, package 설치, push·PR·외부 게시.
- 작업 루트: `Z:\FGKMT-Sono-PrimeGap-Analysis`
- 연구 Python: `W:\miniforge3\envs\FGKMT\python.exe`
- 직전 정본: `handoff/202609090750_HANDOFF.md`

## 목적과 완료조건

- 목적: H1c-1b.2가 준 raw \((T,2T]\) von Mangoldt discrepancy bound를 실제
  Maynard Proposition 9.2/Hypothesis 1(2)의 identity-prime target에 정확히 연결한다.
- 반드시 판정할 항목:
  1. Maynard의 integer interval이 \([T,2T)\), \((T,2T]\), 또는 다른 convention인지.
  2. target weight가 prime indicator, \(\log p\), von Mangoldt \(\Lambda\), 또는
     normalized characteristic 중 무엇인지.
  3. endpoint atom을 exact하게 어떻게 처리하는지.
  4. \(\psi\)에서 primes-only \(\theta\), unweighted \(\pi\)로 옮길 때 prime powers와
     partial summation의 방향·상수를 어떻게 보존하는지.
  5. cumulative center \(\psi(2T)-\psi(T)\)를 Maynard의 represented-prime total과
     같은 중심으로 어떻게 recenter하는지.
- 완료조건:
  1. Maynard·FGKMT·Bordignon 및 적합한 explicit prime-count 선행정리를
     page/equation/hash 단위로 대조한다.
  2. 선행정리가 실제 변수·범위·끝점·오류항에 drop-in 가능한지 판정한다.
  3. 필요한 최소 bridge를 exact/inequality proof로 정식화하고 열린 density·absorption과
     섞지 않는다.
  4. theory/review/JSON, fail-closed helper·tests와 상위 정본을 동기화한다.
  5. FGKMT Python 표적·전체 회귀와 정적검사를 통과한다.
  6. 새 timestamp handoff, 완료 원장과 한국어 local commit을 남긴다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| iterated-log·end-bounded empirical 정의 | 영향 없음 | dataset과 `F/G/H`를 실행·변경하지 않는다 |
| theorem target semantics | 핵심 영향 | 원문의 interval·weight·center를 그대로 고정한다 |
| endpoint | 핵심 영향 | 실수구간과 정수구간, 양 끝 atom을 구분한다 |
| prime powers | 핵심 영향 | \(\psi-\theta\)를 무시하거나 경험적으로 대체하지 않는다 |
| partial summation | 핵심 영향 | 부호·endpoint term·weight 최소값을 exact하게 보존한다 |
| density/remainder absorption | 후속 영향 | H1c-1b.4로 분리하고 이번 단계에서 임의 cutoff를 만들지 않는다 |
| theorem/empirical 구분 | 영향 있음 | proof normalization만 수행하고 `X_cert`를 승격하지 않는다 |
| 승인·재현성 | 영향 있음 | source hash, variable map, negative controls를 기록한다 |
| Git | 영향 있음 | 이번 단계 파일만 명시 stage; broad add, push, PR 금지 |

## 단계 현황

1. **DONE — 현재 정본·실제 target과 source inventory 재구성**
2. **DONE — endpoint/count 변환 선행정리 조사와 적용성 감사**
3. **DONE — exact endpoint·prime-power·partial-summation·recentring bridge 정식화**
4. **DONE — machine contract·helper·회귀시험 작성**
5. **DONE — H1/H1b/H1c/T1·METHODS·AGENTS·색인 동기화**
6. **DONE — 전체 검증·handoff·명시 stage·local commit**

## 단계별 기록

### 2026-09-09 07:55 KST — 상태·범위 고정

- branch `main`, HEAD `d1e207f33f5a6ba6e8d04cc7956b44d7749740c7`, clean worktree와
  활성 작업원장 0개를 확인했다.
- 직전 H1c-1b.2는 fixed-scale common `B`, 최종 12항 전사와 raw \((T,2T]\)
  \(\psi\) composition만 닫았다. count transfer·density·absorption은 열려 있다.
- 이번 단계는 실제 실험이 아니라 source/proof normalization이다.
- PDF skill 경로를 처음 `.../pdfs/...`로 잘못 조회했으나 파일 변경 없이 실패했고,
  catalog의 실제 `.../pdf/...` 경로를 찾아 전체 규약을 읽었다.
- 다음 재개점: Maynard Hypothesis 1(2), Proposition 9.2와 FGKMT actual 호출의 정확한
  interval·weight·center를 원문에서 인용 가능한 형태로 추출한다.

### 2026-09-09 08:31 KST — 실제 target과 선행 bridge 고정

- Maynard의 정의는 `A(T)={n:T<=n<2T}`이고 Hypothesis 1(2)·Proposition 9.2의 target은
  `#P_{L,A}(T;q,a)-#P_{L,A}(T)/phi_L(q)`인 **unweighted prime count**임을 원문
  pp. 1517--1518, 1539--1540에서 확인했다.
- FGKMT 식 (6.5)의 실제 호출은 `T=x/2`, identity form
  `L'_{q,i,i}(n)=n`, `P=all primes`다. 따라서 일반 affine lift는 이번 bridge에 필요 없다.
- Akbary--Hambrook Corollary 1.4 proof는
  `pi_1(y)=sum Lambda(n)/log(n)=sum_{p^k<=y}1/k`, prime-power mass
  `0<=pi_1-pi<2 sqrt(y)`와 partial summation을 이미 사용한다. 전체 정리의
  least-prime-factor modulus family는 현재 fixed-B family와 달라 drop-in하지 않고,
  이 count-transfer argument만 실제 family에 재증명한다.
- 원문의 partial-summation display에 적분 앞 minus가 보이지만 표준 Abel 항등식을 직접
  유도하면 plus다. 원문도 곧바로 triangle inequality만 사용하므로 그 논문의 최종 상계에는
  영향이 없지만, 프로젝트 증명·코드는 올바른 plus 부호를 고정한다.
- Bordignon의 fixed-Q1 조건은 lower endpoint `T`에서 고른 같은 `Q1`과 `B`로 모든
  `u in [T,2T]`에 적용 가능하다. H1c-1b.1의 `log T>2A`에서
  `sqrt(u)/(log u)^A`가 증가하고 `Q1<=(log u)^A`도 유지된다.
- source SHA-256 대조:
  Maynard `8eb9...098`, FGKMT `c312...ac8`, Akbary--Hambrook `797b...32a`,
  Bordignon final `4bd7...029`; 모두 직전 provenance와 일치했다.
- 다음 재개점: open-closed Abel identity, prime-power removal, half-open endpoint atom과
  exact total recentering을 하나의 fail-closed project lemma로 작성한다.

### 2026-09-09 08:32 KST — exact bridge·기계 계약·초기 회귀 완료

- theory 37과 review 43을 신설해 다음 parameterized upper bound를 정식화했다.
  `R(2T)/log(2T)+R(T)/log(T)+integral R(u)/(u log(u)^2)`에 prime-power
  `2sqrt(2T)(M+Phi)`와 half-open endpoint `M`을 더한다.
- exact center는 `P_T=#{p:T<=p<2T}` 그대로이며 `T/log T` 근사를 넣지 않았다.
- `source/h1c1b3_endpoint_count_transfer.py`는 component upper, log-scale normalized
  envelope와 fail-closed structural certificate를 구현했다.
- `tests/test_h1c1b3_endpoint_count_transfer.py`는 plus/minus Abel negative control,
  prime powers 직접 열거, 정수·반정수 endpoint, 독립 formula와 source hash를 검사한다.
- 초기 표적검증은 9개 중 수학·코드 8개 PASS, 1개 예상 FAIL이었다. 실패는 T1 `SIV-08`
  notes에 successor H1c-1b.3를 아직 기록하지 않았기 때문이며 이 단계의 상위 정본
  동기화 gate로 남겼다.
- 다음 재개점: T1/H1/H1b/H1c·METHODS·AGENTS·theory index와 관련 machine JSON에
  count transfer closure와 H1c-1b.4 successor를 동기화하되 root 상태는 유지한다.

### 2026-09-09 08:46 KST — 상위 정본 동기화·회귀 완료

- `AGENTS.md`, `docs/METHODS.md`, theory index, T1/H1/H1b/H1c 사람용 정본과 8개
  machine JSON을 H1c-1b.3 closure 및 H1c-1b.4 successor로 동기화했다.
- 첫 71개 영향권 회귀에서 70개가 PASS하고 1개가 `successor_endpoint_count_transfer`의
  필드명 불일치로 실패했다. 수학 계산 실패가 아니라 JSON 동기화 누락이었고,
  `unweighted_count_transfer_closed=true`를 canonical successor에 추가한 뒤 71/71 PASS했다.
- source에 기록한 explicit prime-power package의 안전한 적용범위와 맞추기 위해 공용
  upper helper를 `T>=4`에서만 작동하도록 fail-closed 강화했고 전용 9/9 시험이 다시 PASS했다.
- 변경 Markdown 16개의 relative link 검사, 27개 machine JSON parse와 `git diff --check`가
  PASS했다.
- sandbox 내부 전체 회귀는 temp directory 쓰기 차단으로 381개 중 82개가
  `PermissionError`를 냈다. 이는 코드 실패와 분리했고, 사용자 승인 범위대로 같은 명령을
  sandbox 외부에서 재실행해 **381/381 PASS (59.273s)**를 확인했다.
- 다음 재개점: `pip check`, 최종 diff/status를 확인한 뒤 새 handoff를 만들고 원장을
  `-done`으로 바꾼 다음 명시 경로만 local commit한다.

### 2026-09-09 08:49 KST — 핵심 commit·handoff 마감

- `pip check`, machine JSON 27개 parse와 최종 diff 검사를 다시 PASS했다.
- 핵심 32개 파일을 명시 경로로만 stage해 local commit
  `9b00eb8de461228f1988643575c28023430b2428`을 만들었다.
- 새 `handoff/202609090849_HANDOFF.md`에 닫힌 exact quantity transfer, 열린 H1c-1b.4,
  검증·실패 이력, 다음 우선순위와 사용자 수행절차 불필요 상태를 기록했다.
- 이 원장을 `-done`으로 바꾸고 handoff와 함께 별도 마감 commit하는 것으로 이번 단계를
  종료한다. 다음 재개점은 새 H1c-1b.4 work ledger다.

## 완료 전 점검

- [x] 사용자 요청 범위의 산출물 완료
- [x] 선행정리 우선 조사와 실제 적용성 대조
- [x] endpoint·weight·center semantics 고정
- [x] prime powers와 partial summation exact 처리
- [x] density·absorption·상위 theorem 과승격 방지
- [x] JSON·코드·시험·정본 동기화
- [x] 전체 회귀·정적검사 PASS
- [x] 새 timestamp handoff 작성
- [x] 명시 경로 stage·local commit
- [x] 파일명을 `-done.md`로 변경
