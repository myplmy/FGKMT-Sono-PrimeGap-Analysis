# 2026-10-01 DEP-R09 numerical EF source audit·CW2 원문 요청

## 1. 판정

Theory105의 full-q D160 nonprincipal near-zero kernel<3/1000는 보존한다.
다음 numerical EF source leaf는 아직 닫지 않았다.
Liu--Wang Theorem8의1.3804와 Bordignon Theorem3.4의 printed remainder를 그대로 채택하지 않는다.
Required CW2 primary 원문은 이번 표적 검색에서 직접 취득하지 못했다.
Source 조건을 임의로 보충하지 않고 원문 요청 단계에서 연구를 일시 중단한다.
현재 numerical EF/PAP/X_cert OPEN; calculator·actual 실험은 NOT RUN이다.

정본 machine guard:
[EF scope audit v1](../method/theory/data/Sono_FMT_DEPR09_numerical_EF_scope_audit_v1.json).

## 2. Primary 대조·취득

| 자료 | 실제 확인 | 현재 증거 |
|---|---|---|
| Liu--Wang2002 | native pp.288--293, rendered pp.289--292 | Section4 source calls·actual range 불일치 |
| Bordignon2021 | official NYJM PDF24pages, native pp.1419--1429, rendered pp.1425--1428 | unrestricted printed Thm3.4 후보; 아래 의무는 미채택 |
| CW2 Chen--Wang1990 | LW referenceCW2·Bordignon reference6, institutional author bibliography | 제목·권호·쪽 확인; primary PDF·lemma 조건 미확인 |

LW SHA:
50c6b5d628a07cfb216078571a846ef658aa7db29515d21bb8dbb4f20dc5055d.
새 Bordignon PDF SHA:
4bd7adf499ba667647b612a61399f0f86c272bc684718630fcde42983c014029.
이후 existing cache tmp/pdfs/h1c1b1/Bordignon2021_NYJM_final.pdf와 동일 hash임을 확인했다.
두 ignored copies를 보존했으며 package·OCR 설치는 하지 않았다.

Primary URLs:

- [Liu--Wang](https://www.impan.pl/shop/publication/transaction/download/product/83843)
- [Bordignon publication](https://nyjm.albany.edu/j/2021/27-54.html),
  [official PDF](https://nyjm.albany.edu/j/2021/27-54v.pdf)

Journal landing과 arXiv2101.08610v1를 확인했으나 최신 correction을 식별하지 못했다.
전 문헌에서 correction이 없다는 주장은 아니다.

## 3. 적용범위와 네 source leaf

LW Section4는 N>=exp2000, t in[.001N,N], q<=log(N)^6, T=log(N)^15다.
Actual q,T=q^(3/2),U=q^160에는 printed parameter choice를 대입할 수 없다.
이는 source choice의 거부이지 일반 truncated EF가 불가능하다는 정리가 아니다.

| CW2 호출 | 공급 내용 | 현재 의무 |
|---|---|---|
| Lemma1 | half-integer Perron | LW Lemma4.1에 statement가 재인쇄됨; full proof 독립 검증 아님 |
| Lemma8 | local zero count | Bennett absolute-height count 대체 가능; 원래 조건은 미확인 |
| Lemma9 | horizontal log derivative | primitive/conductor·sigma·height/margin·uniform-q 조건 원문 필요 |
| Lemma9' | left vertical log derivative | signed height·q dependence·contour regularizer 조건 원문 필요 |

LW p.289의 “Lemma4.2”는 바로 앞4.1과 내용이 대응하는 번호 문제다.
상수와 assumptions까지 다르게 전사하지 않는다.
핵심 요청은 CW2 Lemma9·9'의 조건이며 full paper가 가장 안전하다.

## 4. 후속 source를 즉시 drop-in으로 쓰지 않은 이유

### 4.1 양측 good heights

LW(4.3)--(4.4), Bordignon(13)--(14)는 positive T와 gamma를 적는다.
Complex character의 zero set이 자기 자신 안에서 gamma↦-gamma에 대칭이라고 가정하지 않는다.
가능한 repair는 Bennett의 absolute-height N(T+1)-N(T-1) upper로
양쪽 absolute ordinates를 동시에 피하거나 두 contour heights를 따로 선택하는 것이다.
Bordignon r4는 absolute count 차이이므로 이 repair 후보를 지원한다.
하지만 선택·margin·로그미분 bounds와 negative branch의 source 합성을 아직 인증하지 않았다.

### 4.2 Imprimitive correction의 printed step

Bordignon printed p.1427(12)는 endpoint-independent log(q)/log2를 적는다.
이를 actual lift correction으로 채택하지 않는다.
Primitive quadratic character mod3를 q=21로 유도하고 x=7^4=2401로 두면,
새 Euler exclusion은7 하나이며 chi*(7)=1이므로 exact correction은4log7다.
log2>1/2와 log3<log7에서 log21/log2<4log7다.
이것은 fixed prime-power identity의 algebraic witness이며 actual prime-error 실험을 돌린 것이 아니다.
Printed(12) 자체가 이 witness를 덮지 않는다는 판정이다.
다른 remainder slack을 포함한 최종 PNT 정리 전체의 반례라고 주장하지 않는다.

Theory90의 endpoint-dependent omega(q)log U correction을 보존하는 repair는 이미 있다.
그렇다고 다른 contour source gaps까지 함께 닫혔다고 표시하지 않는다.

### 4.3 contour·boundary·argument order

Printed p.1427 left vertex는+1/2, p.1428 integrals는-1/2다.
Source z(chi)는 beta>1/2지만 discarded block은 beta<1/2이므로 beta=1/2 channel을
명시적으로 보존하거나 별도 bound가 필요하다.
R2/R3와 r1/r6의 argument ordering도 defining expression과 calls를 대조해야 한다.
이들은 direct transcription을 막는 의무이지 academic novelty 또는 전체 theorem refutation이 아니다.

## 5. 사용자에게 필요한 자료

J.R.Chen·T.Z.Wang,
*On distribution of primes in an arithmetical progression*,
Science in China Series A33(4)(1990),397--408.

Full PDF 또는 합법적으로 접근 가능한 download URL을 요청한다.
권장 저장명은 article/chen_wang1990.pdf다. Lemma1·8·9·9'가 포함된 전체12쪽이 좋다.
중문1989 대응본도 후보로 받을 수 있으나 lemma 번호·영문판과의 내용 동일성은 재확인해야 한다.
사용자에게 package/Lean 설치나 계산 실행은 요청하지 않는다.

Exact English title·author/year/pages·Chinese title variants·publisher-focused queries와
author institutional list, LW/NYJM primary references를 확인했으나 full CW2 원문을 얻지 못했다.
추측한 DOI10.1360/ya1990-33-4-397도 resolve되지 않았으므로 verified DOI로 전사하지 않는다.
“public copy가 없다”는 전역 주장은 하지 않는다.

## 6. 검증·재개 경계

새 tests는 source SHA·미취득 상태·false root gates를 확인하는 metadata guards다.
Analytic EF proof가 아니다. 실행 결과는 active work ledger와 최신 handoff에 기록한다.
Theory105의472 regression tests·Lean8765jobs 결과는 그대로 보존한다.
추가 mathematical Lean source 변경·actual data/zeros 접근은 하지 않았다.

새5 guards·0.002s·exit0, latest DEP-R09 regression477건·5.155s·exit0,
generator→validator·exit0. Inventory106 문서·2085식·443 declarations·proof escape0.
이 수치를 numerical EF analytic PASS로 승격하지 않는다.

CW2 제공 후 hash·native/scan 확인 → Lemma9/9' 조건 → signed-height repair →
corrected imprimitive/boundary/contour → 보수적 numerical EF의 순서로 재개한다.
일단 필수 원문 요청으로 중단하며 source premise를 axiom으로 보충하지 않는다.
