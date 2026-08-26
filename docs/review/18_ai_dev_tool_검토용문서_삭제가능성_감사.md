# `ai_dev_tool` 검토용 문서 삭제 가능성 감사

## 판정 원칙

삭제 가능성은 “코드가 지금 읽지 않는다”만으로 정하지 않았다. 다음 세 조건을 모두 본다.

1. canonical review·plan·method 문서가 내용을 충분히 흡수했는가
2. live code/test가 해당 파일을 입력으로 읽는가
3. 원 제안서 provenance를 보존할 연구상 가치가 남았는가

이번 보고서는 삭제 허가가 아니라 목록과 권고다. 실제 파일은 삭제하지 않았다.

## A. 내용 이관 완료 — 삭제 가능

다음 파일은 runtime 입력이 아니고, 핵심 내용·오류·채택사항이 canonical 문서에
반영됐다. 관련 변경을 먼저 commit한 뒤 사용자가 원하면 삭제할 수 있다.

| 삭제 가능 파일 | SHA-256 | 대체 정본 |
|---|---|---|
| `ai_dev_tool/temp_1854 Maximal Prime Gap 이후 Exhaustive 탐색범위 확장을 위한 실험계획서·타당성 검토서·Codex 작업 지시서(검토용).md` | `F0AB63FFAC51C5C89FF7010A6462C4299270D060B2906A0FEDD728388DFEE790` | `docs/review/12_...`, `test_plan/P005_...` |
| `ai_dev_tool/temp_Maximal Prime Gap Plateau·Recurrence 통계 분석 실험 타당성 검증 및 실행 준비 문서(검토용).md` | `5B50DB92E47ADF74D39535484945800A4FA79975BCD2BCFA6B1BAE1F694C5F38` | `docs/review/13_...`, `test_plan/P006_...` |
| `ai_dev_tool/temp_P005b — Rank 85 이후 Exhaustive Prime-Gap 확장 가능성 실측 제안서 및 타당성 검토 요청서(검토용).md` | `44B97BFE278F3510363FAD0B5377CB08C1F70DD598032E627049604EA26782C6` | `docs/review/14_...` |
| `ai_dev_tool/temp_prime_gap_count_algorithm/P008_local_residue_state_certificate_experiment_review(검토용).md` | `FF42435F6628AB6D08FCDEB8C136D1AEC09F10BD113FCCE27014D9630C7A444A` | `docs/review/16_...`, `test_plan/P008_...`, P009 |
| `ai_dev_tool/temp_theories_20260826/01_certified_prime_gap_certificate_compression.md` | `854A3EA7665809870E5458397E2D0877D3BA997C961B368C39DBA62BF1F4DBA1` | `docs/review/17_...`, `docs/method/theory/06_...` |
| `ai_dev_tool/temp_theories_20260826/02_coverage_preserving_block_compression.md` | `5B08C2A1A517D6BED5D097FAB91B4FF108B385B85C0D01D839B9105CF7A1CF9A` | `docs/review/17_...`, `docs/method/theory/06_...` |
| `ai_dev_tool/temp_theories_20260826/03_local_li_pi_prime_count_certification.md` | `0DBB4D1977B66D2BBB7A92AB70442DDEE389EB8C64FE3468C67EF9D24736AAFD` | `docs/review/17_...`, `docs/method/theory/07_...` |
| `ai_dev_tool/temp_theories_20260826/integrated_prime_gap_theory_1856.md` | `09102741BFF37C0B4463BF3832974A9F61C9F7D3F88E1241E86A8B5EEA3F2FF8` | `docs/review/17_...`, `docs/method/theory/00_...`–`09_...` |

권고는 즉시 영구삭제보다 `ai_dev_tool/archive/review_inputs/`로 한 번 옮기고 한 commit
동안 두는 것이다. 그래야 정본 누락을 발견했을 때 되돌리기 쉽다.

## B. 조건부 삭제 — 지금은 유지 권고

| 파일 | 이유 |
|---|---|
| `ai_dev_tool/temp_prime_gap_count_algorithm/C_1856_finite_range_research_memo(검토용).md` | review 15가 결론을 흡수했지만 P007 원 수식·명칭 provenance로 직접 참조됨 |
| `ai_dev_tool/temp_prime_gap_count_algorithm/PrimeGap_FiniteRange_Theory_Nomenclature_and_Certification(검토용).md` | review 15가 참조하는 원 이론 명세이며 source bundle과 한 세트 |

이 두 파일도 runtime 입력은 아니므로 기술적으로 삭제 가능하다. 다만 다음을 먼저 해야 한다.

1. review 15에 두 SHA-256과 필요한 원 명제를 충분히 인용
2. P007 source bundle의 provenance README 작성
3. 문서 링크를 archive 또는 canonical method로 교체

## C. 삭제하면 안 됨

다음은 P007/P008 live test와 CLI가 직접 읽거나, exact certificate 재현에 필요하다.

| 유지 파일 | 이유 |
|---|---|
| `ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt` | live certificate 입력; pinned SHA-256 `44C6...92FB` |
| `ai_dev_tool/temp_prime_gap_count_algorithm/source/C_2310_certificate.py` | supplied certificate 생성 provenance |
| `ai_dev_tool/temp_prime_gap_count_algorithm/source/verify_C2310.py` | 원 독립검증 경로 provenance |

장기적으로는 이 세 파일을 `datas/reference/p007_mod2310/<hash>/` 또는
`docs/method/certificates/` 아래 immutable bundle로 옮기는 편이 이름상 더 정확하다.
그 이관은 import·test·plan 경로를 함께 바꾸는 별도 작업으로 수행해야 하며 현재는
삭제하지 않는다.

## D. 삭제 대상이 아닌 `ai_dev_tool` 정본

- `01_계측함정_원장.md`
- `02_핸드오프_규약.md`
- `03_실험착수_절차.md`
- `04_사용자실행_로그_완료이관_규약.md`
- `project_reference/`

이들은 현재 작업 규약과 정적 참조이므로 유지한다.
