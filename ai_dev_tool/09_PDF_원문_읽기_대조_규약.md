# PDF·LaTeX·OCR 원문 판독 규약

- 적용: 2026-09-09, 사용자 지시 반영
- 목적: 읽기 비용을 줄이되 식의 부호·지수·양화·범위·원천 버전을 보존한다.
- PDF 원본과 기존 TeX를 덮어쓰거나 임의로 OCR PDF로 교체하지 않는다.

## 1. 페이지 유형부터 분류

| 유형 | 판단 근거 | 기본 판독 | 추가 대조 |
|---|---|---|---|
| NATIVE_TEXT | 문자·수식 font 및 text drawing, 대응하는 본문 텍스트 | 직접 텍스트 추출·검색 | 핵심 수식의 배열·의심 글자만 원본 화면 |
| MATCHED_TEX | PDF와 출판/개정 버전의 일치 근거가 있는 TeX | TeX로 수식·참조 탐색 | 최종 채택 식은 해당 PDF 위치와 대조 |
| SCAN_WITH_TEXT_LAYER | 전면 raster와 숨은 text rendering 등 | 기존 OCR/보조 텍스트로 탐색 | 채택하는 정리·식·조건을 스캔 원본과 대조 |
| SCAN_NO_USABLE_TEXT | 스캔이며 텍스트 없음/판독 불가 | 해당 쪽만 OCR 필요 여부 판단 | OCR 결과를 원본과 대조; 불명확하면 미확인 |
| MIXED_OR_UNKNOWN | 페이지별 유형이 다르거나 증거 부족 | 필요한 페이지별 분류 | 문서 전체를 한 유형으로 단정하지 않음 |

텍스트가 추출된다고 반드시 원래 문자 PDF는 아니다. 스캔 위에 OCR 텍스트층이 있을 수 있다.
반대로 수식의 줄배치가 깨진다고 반드시 OCR이 필요한 것도 아니다.
메타데이터 producer가 없거나 특정 도구명을 포함하는 것만으로 유형을 결정하지 않는다.

## 2. 실제 절차

1. 기존 source registry, PDF/TeX 경로, SHA-256, 출판/개정일을 먼저 확인한다.
2. 페이지의 텍스트, font, image object, 필요하면 text rendering mode를 확인한다.
3. native PDF는 텍스트 우선, TeX는 버전 일치 여부를 적고 보조 탐색에 쓴다.
4. 사용할 lemma의 가정·정의·끝점·상수·오류항·인용 선행정리를 함께 읽는다.
5. 추출이 애매한 수식, scan/OCR의 중요한 식, 표·도식은 필요한 원본 페이지만 대조한다.
6. 대응이 확인되지 않은 TeX의 식을 출판본 정리처럼 쓰지 않는다. 번호뿐 아니라 내용도 대조한다.
7. OCR이 실제 필요한 경우에만 수행한다. 설치가 필요하면 사용자에게 이유·절차를 요청한다.
8. 교정 사항과 미확인 부분을 review/원장에 남긴다. OCR 결과만으로 새 수학 주장을 확정하지 않는다.

순수 텍스트 조회에 전체 페이지 렌더링을 강제하지 않는다. 의미를 확인할 수 없는 문자는
그럴듯한 수식으로 복원하지 말고 원문 재확인 또는 사용자 요청으로 넘긴다.
사용자에게 맡기는 실험 figure 시각 QA와 논문 수식의 원문 대조는 별개다.

## 3. 기록 양식

~~~text
source_id / PDF path / SHA-256 / source version
PDF page (1-based) / printed page / theorem or equation
page_type / evidence (text, fonts, raster, hidden layer)
TeX path/hash/version_match (matched / older_or_unconfirmed / absent)
text_or_TeX_read / original_comparison / discrepancy
new_OCR_performed (yes/no) / unresolved
adopted claim and scope
~~~

현재 사례: FGKMT p.99, FMT p.13, Maynard p.1546, Sono p.542의 확인 페이지는 native
typeset이고 OCR 불필요다. RS1962 p.69는 전면 스캔과 숨은 텍스트층이 있다.
기존 텍스트의 plus/minus·pi 오독을 **모든 native PDF의 추출 실패**로 일반화하지 않는다.
이번에는 새 OCR을 수행하지 않았다. PDF 일부 페이지 검사로 전체 파일의 모든 페이지가
동일 유형이라고 선언하지 않는다.

## 4. 도구·안전

- 사용 가능한 PDF 도구 경로부터 확인한다. 존재하지 않는 Poppler 경로를 추측하지 않는다.
- PDF 읽기/렌더링 도구 내부는 번들 runtime을 쓸 수 있다. 연구 검산은 FGKMT 환경만 쓴다.
- 큰 출력이 잘리면 필요한 범위를 나누어 끝까지 읽는다. 잘린 내용은 검토 완료가 아니다.
- tmp의 source PDF/TeX와 hash-pinned evidence는 정리 대상이 아니라 RETAIN일 수 있다.
- PDF 도구 오류는 논문 오류와 구분해 오류 원장에 기록한다.
