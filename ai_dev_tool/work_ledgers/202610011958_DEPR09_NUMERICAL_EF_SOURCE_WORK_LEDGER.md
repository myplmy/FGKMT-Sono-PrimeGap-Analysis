# DEP-R09 numerical EF 원문·양측 good-height 작업원장

- 시작:2026-10-01 19:58 KST
- 상태:WAITING_USER_PRIMARY_CW2
- 시작HEAD:d7e0cb6c3624ddc970438f4d540652a7fb03c22b, clean main.
- 선행 정본:Theory105·review114·handoff202610011955.
- 목적:actual full q,T=q^(3/2),U=q^160의 fully numerical EF leaf를 source-first로 감사한다.
- 승인:primary source 취득·문서·finite fixture·Lean·한국어 local commit.
- 금지:actual prime/zero/dataset·calculator/range search·설치·장시간 연산·law변경·push/PR.

## 영향도·비교

| 접근 | 적용범위·위험 | 선택 |
|---|---|---|
| LW printed1.3804 사용 | q<=log(N)^6,T=log(N)^15가 actual과 불일치 | 금지 |
| LW proof replay | CW2 Lemma1·8·9·9',양측높이·primitive·principal 조건 필요 | 우선 source 감사 |
| 이미 numerical한 EF 대체 source | 정확한 all-character range가 필요 | primary source 비교 |
| 새 직접 complex EF proof | 원문 공급 lemma 확인 없이 수행하지 않음 | source 이후 판단 |

불변식:full q·D160·actual law·fixed coefficients 유지.
N/U·half endpoints·principal/imprimitive·actual prime observation을 구분한다.
필수 원문 취득 불가·장시간 연산·추가 library가 필요하면 사용자에게 요청하고 중단한다.

## 단계

1. DONE — Theory105 commit·clean Git·canonical 환경·mutool 경로 확인.
2. DONE — LW Section4의 각 source call/range audit; CW2 필요성 판정.
3. WAITING_USER — CW2 primary 직접 취득 불가; 다른 numerical 후보도 critical 조건 미확인.
4. PENDING — 개별 source 조건·양측good heights·endpoint/imprimitive/principal 감사.
5. DONE — 이번 source scope 감사·false-gate 검증·정본 문서; 새 handoff/local commit 준비.

## 초기 source 관측

LW pp.288--292 native text를 기존 mutool로 읽었다.
Proof는 CW2 Lemma1(Perron),8(local count),9(horizontal log derivative),9'(left vertical)를 호출한다.
(4.3),(4.4)의 positive T good height만으로 complex character의 negative horizontal side를
자동 인증하지 않는다. 실제 원문과 bounds를 확인해 양측height repair를 판정해야 한다.
Section4의 principal proof는 sketch이므로 exact pole/bound 확인이 별도로 필요하다.
Source typo 'Lemma4.2'는 앞의 Lemma4.1과 연결되나 내용 대조 전 새 lemma로 읽지 않는다.

## 2026-10-01 20:13 KST — 적용범위·입수 결과와 중단

- 새 정본:review115·Sono_FMT_DEPR09_numerical_EF_scope_audit_v1.json.
- LW native pp.288--293·rendered289--292, NYJM native1419--1429·rendered1425--1428 대조.
- CW2 primary의 Lemma9/9' primitive/conductor·sigma·height/margin·uniform-q 조건이 필요하다.
  원문 없이 numerical constant를 채택하지 않는다.
- Exact English title·author/year/pages·중문title variants·publisher-focused 검색,
  institutional author list·LW/NYJM references·arXivv1를 확인했으나 원문을 취득하지 못했다.
- 추측 DOI10.1360/ya1990-33-4-397가 resolve되지 않았으며 verified DOI로 쓰지 않는다.
  원문/공개copy가 세계 어디에도 없다는 주장은 하지 않는다.
- Official NYJM2021을 curl --fail --location --connect-timeout10 --max-time40으로
  직접 취득, exit0. PDF-1.5·24pages·SHA4bd7adf499ba667647b612a61399f0f86c272bc684718630fcde42983c014029.
  기존 h1c1b1 final cache와 동일 hash였다. 두 ignored copies 보존, raw stage/설치 없음.
- Bordignon(12)의 endpoint-independent lift correction은 미채택.
  q21·quadratic primitive mod3·x=7^4의 algebraic correction4log7가 printed log21/log2를 넘는다.
  Actual prime-error 계산이나 최종 PNT theorem 전체 반례가 아니다.
- Signed heights, left-contour sign, beta=1/2와 argument ordering 의무도 별도 기록했다.
  Bennett absolute-height count의 common-height repair 가능성은 보존하지만 미인증이다.
- Theory105의 count144·full-q near kernel<3/1000·originalD160·law는 보존했다.
- Source 요청에 따라 연구를 일시 중단한다. 추가학술novelty·장시간 계산·새library는 요구되지 않았다.

## 실행 검증

~~~bash
/mnt/w/miniforge3/envs/FGKMT/python.exe -m unittest tests.test_dep_r09_numerical_ef_scope_audit -q
# 5 metadata guards,0.002s,exit0
/mnt/w/miniforge3/envs/FGKMT/python.exe -m unittest discover -s tests -p 'test_dep_r09_*.py' -q
# 477 tests,5.155s,exit0
/mnt/w/miniforge3/envs/FGKMT/python.exe lean/tools/refresh_and_validate_verification_ledger.py
# final theory-index/T1 edits 후 generate→validate,PASS,exit0
~~~

Inventory106 theory 문서·2085식·443 declarations:
KERNEL126·CONDITIONAL142·DEFINITION231·PARTIAL196·SOURCE210·NOT_YET1175·PARSE5,
proof escape0. Math Lean source/toolchain/manifest 추가 변경 없음.
Theory105 direct compile·build8765jobs exit0를 보존하며 이번 source-request batch에서
전체 Lean build/whole unittest를 다시 실행한 것처럼 쓰지 않는다.
Historical PS5.1 failure 재판정 없음. Whole-project green 주장 없음.

## 사용자 요청·완료하지 않은 것

- J.R.Chen·T.Z.Wang, On distribution of primes in an arithmetical progression,
  Science in China Series A33(4)(1990),397--408의 full PDF 또는 합법적 accessible URL.
- 권장 파일명:article/chen_wang1990.pdf. Lemma1·8·9·9' 포함 전체12쪽 권장.
- 사용자 계산/설치/Lean 변경/장시간 실행 요청 없음. 자료 첨부/저장 또는 URL 회신만 필요.
- Numeric K_EF·full PNT/PAP·X_cert·bounded range·calculator는 미완료다.
- 원장은 비-done으로 보존한다. 이번 상태 snapshot만 local commit하며 push/PR 없음.
- 최신 실제20:16 KST handoff:handoff/202610012016_HANDOFF.md.
- 제목:DEP-R09 명시공식 적용범위를 감사하고 필수 원문 요청을 기록
- 본문은 source 적용조건·미취득CW2·guards5/회귀477·root OPEN·금지항목 미실행을 적는다.
  실제 hash·post-commit clean은 Git에서 확인한다. Pending source를 완료로 기록하지 않는다.

## 현재 재개점

CW2 full PDF/합법적 URL 제공을 기다린다. 제공 후 SHA/native·scan 대조를 수행하고
Lemma9/9'의 actual q,T,U 적용조건부터 검증한다. Theory105 first-window는 다시 시작하지 않는다.
