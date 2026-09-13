# DEP-R09 현대 명시적 zero-density 대체자료 선별 타당성 검토

- 작성일: 2026-09-14 KST
- 기술 정본: [Theory 74](../method/theory/74_Sono_FMT_DEPR09_modern_explicit_density_source_screen.md)
- 기계 원장: [modern density source screen v1](../method/theory/data/Sono_FMT_DEPR09_modern_density_source_screen_v1.json)
- 최종 판정: **선별 후보 중 현재 (X_{\rm cert}) 증명에 바로 넣을 수 있는 공개 수치 정리는 없음**

## 1. 이번 조사의 질문

직전 단계에서는 Jutila 계수의 불필요한 여유를 약 343배 줄였다. 그래도 허용 예산보다
약 4,620억 배 컸다. 그래서 이번에는 계산식을 조금 더 다듬는 대신 다음을 물었다.

> 최근 논문에 더 강한 영점밀도 정리나 소수분포 정리가 있다면, 그 정리를 그대로 넣어
> Sono의 계수와 (X_{\rm cert})를 수치 인증할 수 있는가?

답은 현재 선별한 후보에 한해서 **아직 아니다**이다.

## 2. 왜 “더 좋은 지수”만으로 부족한가

증명용 정리는 자동차 부품과 비슷하다. 엔진 출력이라는 한 숫자만 좋아도 실제 차에 바로
장착할 수 있는 것은 아니다. 크기, 연결 규격, 냉각, 안전시험이 모두 맞아야 한다.

이번 연구에서 필요한 연결 규격은 다음 네 가지다.

1. 우리가 쓰는 modulus와 character 범위를 정확히 덮어야 한다.
2. 숨은 상수 없이 multiplier가 숫자로 나와야 한다.
3. “충분히 큰 수부터”가 아니라 그 시작점도 숫자로 나와야 한다.
4. 평균적인 영점 개수에서 각 산술진행의 실제 소수 개수로 가는 전달이 수치적이어야 한다.

Chen--Gupta--Li 원고의 (7/3) 같은 exponent 개선은 이론적으로 흥미롭다. 그러나
((qT)^{o(1)})의 실제 값과 시작점이 없기 때문에 지금의 유한 계산기에는 넣을 수 없다.

## 3. Ramaré 정리는 왜 숫자가 모두 있는데도 통과하지 못했나

Ramaré 2016은 이번 후보 중 가장 완전하게 숫자가 적힌 averaged zero-density 정리다.
그래서 현재 Gallagher 적분에 실제로 대입했다.

(d=186)이고 현재 보수적 zero-free constant (c_1=1/24)일 때, 정리의 적용이 시작되는
최소 범위에서도 direct upper-certificate의 아주 작은 한 조각만

| 부분 | certificate 값의 하한 |
|---|---:|
| main term slice | (8602.03) 초과 |
| additive term slice | (64912.22) 초과 |
| 허용하려는 전체 예산 | (e^{-2}\approx0.1353) 이하 |

였다. 게다가 이 두 값은 (X)가 커질수록 감소하지 않고 증가한다.

쉽게 말하면 실제 오차를 재어 보니 크다는 뜻이 아니다. 이 정리가 주는 “안전한 최악의
견적서” 자체가 예산보다 너무 커서, 그 견적서만으로 합격 도장을 찍을 수 없다는 뜻이다.

## 4. 매우 중요한 과대해석 방지

이번 결과가 증명하는 것:

- Ramaré 정리의 오른쪽을 현재 식에 그대로 넣고 모든 항을 양수로 더하는 방법은 실패한다.
- Friedlander--Iwaniec의 수치 범위 (q^{52600})은 현재 허용범위 (q^{186})보다 훨씬 나쁘다.
- 이름만 “effective”인 정리는 숫자를 복원하기 전까지 (X_{\rm cert}) 입력이 아니다.

이번 결과가 증명하지 않는 것:

- 실제 소수분포 오차가 8602보다 크다는 주장,
- Ramaré 정리를 다른 방식으로 결합해도 반드시 실패한다는 주장,
- 공개 문헌 전체에 적합한 정리가 절대로 없다는 주장,
- 새로운 정리나 cancellation을 이용한 증명이 불가능하다는 주장.

따라서 판정은 “연구 종료”가 아니라 “단순 drop-in 문헌교체는 현재 실패”다.

## 5. 후보별 쉬운 판정

| 후보 | 쉬운 해석 | 지금 쓸 수 있나 |
|---|---|---|
| Ramaré 2016 | 숫자는 모두 있지만 현재 조립법에서 견적이 너무 큼 | 아니오 |
| Thorner--Zaman explicit density | 지수 일부는 맞지만 고정 상수와 마지막 전달이 너무 거침 | 아니오 |
| Thorner--Zaman uniform PNT | 우리 목표와 가장 비슷하지만 핵심 숫자가 미인쇄 | 아직 아니오 |
| Kaneko--Thorner / Thorner--Zhang | 이론적 연결은 좋지만 “계산 가능”에서 실제 숫자로 복원해야 함 | 아직 아니오 |
| Friedlander--Iwaniec | 다른 공법이지만 필요한 지수·계수가 현재 목표와 크게 어긋남 | 아니오 |
| Chen--Gupta--Li | 최신 exponent 개선이지만 미검증 원고이며 (o(1))이 남음 | 인증에는 아니오 |
| Bellotti--Castillo | 제목은 정확히 필요한 내용이나 아직 공개 원문이 없음 | 감시만 가능 |

## 6. 사용자가 추가한 세 고전 논문의 처리

`article/gallagher1970.pdf`, `article/Maier 1981.pdf`, `article/McCurley 1984.pdf`는
새로 무시된 것이 아니다. 이미 Theory 57의 full-source 감사, Theory 65의 local zero-count,
Theory 72의 density-integral split에서 원문 페이지와 수식을 대조했고 hash도 기계 원장에
고정했다. 이번 보고서는 이들을 baseline으로 삼아 현대 후보가 실제로 대체 가능한지만
비교했다.

PDF는 native text가 있으면 텍스트를 먼저 사용하고 핵심 수식 페이지를 이미지 렌더로
대조했다. native text가 없는 경우에만 OCR을 위치 찾기에 쓰며, OCR 결과만으로 수식을
확정하지 않는 기존 규칙을 유지했다.

## 7. (X_{\rm cert})와 CPU 투자에 미치는 영향

현재 numerical (X_{\rm cert})의 상한은 새로 얻지 못했다. 따라서 다음은 하지 않았다.

- threshold calculator 제작·실행,
- 큰 소수 범위 sweep,
- 사용자 CPU를 오래 쓰는 검증.

이유는 병목이 “(X)를 더 많이 계산하지 않아서”가 아니라 “정리의 수치 상계가 현재
proof budget에 맞지 않아서”이기 때문이다. 지금 100시간을 계산해도 이 증명 의무는
닫히지 않는다.

## 8. 다음 연구방향의 우선순위

### 1순위: numerical PNT source watch

Bellotti--Castillo 원고가 공개되거나, Thorner--Zaman형 정리의 실제 상수·cutoff가
공개되면 즉시 같은 gate에 넣는다. 비용이 가장 작고 성공하면 직접적인 경로다.

### 2순위: transfer 구조 재설계의 작은 타당성 감사

다음 가능성을 수식 수준에서 먼저 검사한다.

- Ramaré의 additive term을 다른 bound와 minimum으로 잘라낼 수 있는가,
- smoothing이 log power를 상쇄하는가,
- exceptional/nonexceptional branch의 cancellation을 보존할 수 있는가,
- averaged density를 pointwise PAP로 옮길 때 현재보다 훨씬 적은 손실이 가능한가.

이 단계는 먼저 coefficient의 필요조건만 계산한다. 통과 전망이 없으면 긴 증명 복원으로
가지 않는다.

### 3순위: 나머지 PAP 종단 복원

앞 coefficient gate가 통과할 후보를 얻은 뒤에 principal character, exceptional modulus,
prime powers, endpoint, (\psi\to\pi)와 공통 cutoff를 닫는다.

## 9. 최종 판정

이번 단계는 성공적으로 “쓸 수 없는 후보를 정확한 이유와 함께 제외”했다. 연구의 숫자
결론은 다음처럼 보수적으로 유지한다.

- `PAP-11`: `OPEN`
- `DEP-R09`: `OPEN`
- Sono fixed (2\times10^{-17}): 프로젝트 독립 인증 전
- numerical (X_{\rm cert}): `OPEN`
- 실제 finite empirical threshold (X_{\rm emp}(10^{20})=3{,}814{,}280): 별개의 기존 결과

이 구분을 유지해야 유한 데이터 관찰을 무한 범위 정리의 검증으로 잘못 말하지 않게 된다.

## 10. 참고문헌

상세 source statement, 페이지, DOI·arXiv 링크와 hash는 Theory 74 §11 및 machine ledger에
기록했다. 핵심 공개 원문은 Ramaré
[DOI 10.1090/mcom/2991](https://doi.org/10.1090/mcom/2991),
Thorner--Zaman [arXiv:2208.11123](https://arxiv.org/abs/2208.11123)과
[arXiv:2108.10878](https://arxiv.org/abs/2108.10878),
Friedlander--Iwaniec [arXiv:2303.06122](https://arxiv.org/abs/2303.06122)이다.
Chen--Gupta--Li [arXiv:2507.08296](https://arxiv.org/abs/2507.08296)는
미검증 후보로만 보존한다.
