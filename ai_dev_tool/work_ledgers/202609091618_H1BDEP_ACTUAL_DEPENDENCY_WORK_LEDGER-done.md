# H1b-DEP actual dependency 및 X_cert 진행현황 작업원장

- 시작: 2026-09-09 16:18 KST
- 현재 상태: COMPLETE — H1b-DEP bounded task 완료, 전체 X_cert OPEN
- 사용자 승인: PDF text/LaTeX/OCR 구분, X_cert 진행현황 보고, H1b-DEP 재개; 선행 승인 범위의 toy·회귀와 단계별 로컬 commit.
- 금지·보류: actual prime/data 실험, threshold calculator, 임의 설치, push/PR. 필수 새 자료·장시간 계산 필요시 요청 후 중단.
- 선행 변경: main, HEAD 76f4266, git status --short 빈 출력. 기존 비완료 원장 없음.

## 목적과 완료조건

FGKMT/FMT가 실제 호출하는 유한 weight 입력과 일반 Maynard Proposition 6.1 의무를 분리한다.
P95의 직접·간접 필요성을 원문에서 확인하고 남은 numerical proof 조건을 쉬운 보고서와 기계검사 가능한 DAG로 남긴다.
닫힌 child를 root X_cert로 승격하거나 unit-test PASS를 해석적 증명의 독립 인증으로 바꾸지 않는다.

## 영향도·불변식

| 축 | 판정 | 통제 |
|---|---|---|
| 수학 정의 | 불변 | end-bounded G, 반복로그, Sono 계수 유지 |
| 증명 의존관계 | 영향 있음 | general theorem과 실제 filtered fixed-X package를 별도 graph로 감사 |
| 데이터·provenance | 변경 없음 | datas/test_result 및 source PDF 비수정, 읽은 source hash 보존 |
| 통계·정밀도 | 실제 통계 없음 | graph·toy 검사만, 전수 소수 계산 금지 |
| 승인 경계 | 고정 | 로컬 문서/코드/toy만; 설치·actual 불가 |
| 원문 판독 | 영향 있음 | native text/대응 TeX/scan OCR 층 구분, 핵심 식·조건 원본 대조 |
| 산출물 | 비덮어쓰기 | theory 44--47 및 과거 handoff/원장 불변; successor 신설 |

## 단계 현황

1. **COMPLETE — 최신 handoff·정본·스킬과 clean Git 확인**
2. **COMPLETE — PDF 유형·실제 call 및 transitive dependency source 감사**
3. **COMPLETE — H1b-DEP 계약/증명 의존지도·진행현황 보고서·toy verifier**
4. **COMPLETE — 표적/전체 toy 회귀·hash·문서 검사**
5. **COMPLETE — 정본 동기화·명시 allowlist 로컬 commit**
6. **COMPLETE — timestamp handoff·최종 확인; 완료 원장과 handoff의 마감 commit은 git log 정본**

## 단계별 기록

### 2026-09-09 16:18 KST — 재개

- handoff/202609091606_HANDOFF.md 전체 확인: NORM 완료, 다음 H1b-DEP, 전체 X_cert OPEN.
- 5개 프로젝트 스킬과 PDF 스킬, 작업원장 규약·정적 프로젝트 참조를 전체 읽음.
- PDF 질의응답 뒤 이번 사용자 승인은 증명 의존감사 재개이며 actual 실험 승인이 아님.
- 첫 AGENTS 도구 출력이 총량 제한으로 일부 잘려 누락 구간을 별도 읽기로 보완했다.

## 현재 재개점

전체 unittest session 81070은 503/503 PASS (59.163초, exit 0)로 완료됐다.
전용 20/20 (0.272초), 표적 113/113 (0.582초), 5파일 py_compile PASS.
새 proof/review/PDF 규약·DAG·helper·tests를 작성했고 parent JSON 3개와 정본을 동기화했다.
proof commit 066d20d4c72edc9d483ffece2de2c205cccc6577에 20개 allowlist 파일을 보존했다.
handoff/202609091648_HANDOFF.md를 작성했고 이 원장을 -done으로 마감한다.
다음 작업은 새 H1b-COR1 원장에서 DEP-R01을 시작한다. 기존 완료 proof를 반복하지 않는다.

### 2026-09-09 16:30 KST — source 감사 완료

- FGKMT p.99의 P91/P92/P94/L85/L86 직접 호출, Maynard P91--P94의 증명과 L93 하위 호출을 대조했다. P95 호출은 없으며 P94는 FMT sequel에서 필요하다.
- Maynard P92 proof의 P6.1 참조는 명시된 분포 가정이지 전체 P6.1 결론의 순환 호출이 아니다. TeX의 eq:S4Bound2도 P95 호출이 아니다.
- FMT 초고 인용과 FGKMT 출판본 crosswalk: Lemma 5.1→6.1, local-count Corollary 4→5, Lemma 5.3→6.3. hypergraph Corollary 3→현재 4는 가정이 달라 단순 번호 교체 금지.
- 현재 FGKMT p.82에 codegree의 원래 divisibility 증명이 있다. 새 증명이라고 하지 않고 actual 범위에 명시화한다. post-conditioning sparsity 입력은 아직 OPEN이다.
- PDF 5개 선택 페이지를 font/image/text-rendering mode와 함께 조사: FGKMT/FMT/Maynard/Sono는 native typeset, RS1962는 full-page raster+숨은 text층. OCR 새 실행 없음. RS metadata=None의 첫 도구 실패를 교정했다.
- FGKMT p.99 및 FMT p.13을 텍스트 대조 후 필요한 부분만 렌더/확인했다. 전체 PDF를 이미지로 읽은 것이 아니다.
- 기존 source/선행 theory 43--47 원문은 수정하지 않았다. 잘못 추측한 오류 원장 경로 1건은 실제 README 경로로 정정했다.

### 2026-09-09 — 문서·구현 및 첫 회귀

- theory 48 §§5.1--5.3: admissible tuple의 유한 존재, C_h=4, distinct-point 크기·차원 적용성.
- §5.4: FGKMT p.82의 기존 codegree 논증을 actual 범위에 명시화. conditioned sparsity가 입력인 조건부 bridge이며 hypergraph 전체 PASS 아님.
- review 54: 세 threshold 구분, 6묶음/12작업의 남은 의무, 비전문 사용자 예시·권장 순서.
- PDF 규약 09와 AGENTS/README 연결. 새로운 OCR·설치 없음.
- 계약은 11개 원천/선행 hash와 5개 선택 페이지 판독 evidence를 보존한다.
- 전용 첫 20 tests 중 1건은 식 label 정의를 ref로 기대한 검사 오류. 정의/참조를 분리해 재실행 PASS. E076에 공개.
- T1 JSON 재직렬화로 불필요한 배열 줄바꿈이 바뀐 것을 diff에서 발견해, 동일 의미를 유지하며 최소 변경 patch로 줄였다.
- full suite는 승인된 정상 로컬 권한으로 시작했다. actual 실험 실행이 아니다.
- 전체 503/503 PASS (59.163초), 표적 113/113 PASS, 11개 source/선행 hash 유지.
- 21파일 strict UTF-8, 4 JSON, 155 local links, 새 수식 구분자 issue 0.
- git diff --check 단독 exit 0. LF/CRLF 변환 안내는 저장소 기존 정책이며 데이터 변경/오류가 아니다.

### 2026-09-09 16:48 KST — 로컬 proof commit 및 마감

- staged allowlist 20개 exact match, cached diff --check 단독 exit 0.
- proof commit 066d20d4c72edc9d483ffece2de2c205cccc6577; push 없음.
- 현재 source registry의 기존 pin 1a112a1387052d9ad360686313f501c01fe46b68, 기존 coverage 10^20를 읽었다. 원격 최신 검증/새 dataset 취득은 하지 않았다.
- 최신 handoff에 목적·남은 12작업·사용자 절차·예상시간·한국어 commit 제목/본문을 포함했다.

## 완료 전 점검

- [x] 사용자 요청 산출물 완료
- [x] 승인·비실행 경계 명시
- [x] 검증 증거·해석적 증명 구분
- [x] METHODS/이론 정본·PDF 판독 규약 동기화
- [x] 새 timestamp handoff 작성
- [x] git diff --check와 참조 경로 확인
- [x] 파일명을 -done.md로 변경 (마감 rename 절차)
