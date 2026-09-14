# DEP-R09 제한 잔여류 분산·spectral 경로 타당성검토

- 작성일: 2026-09-14
- 기술 정본: [Theory 77](../method/theory/77_Sono_FMT_DEPR09_restricted_residue_variance_spectral_optimality_audit.md)
- 선행 검토: [review 84](84_20260914_DEPR09_preabsolute_moment_pointwise_PNT_source_타당성검토.md)
- 판정: `부분 타당 / 기존 full-variance source는 drop-in 아님 / unweighted energy 개선안은 기각 / direct weighted correlation은 열린 유망 경로`

## 1. 쉬운 결론

Maier 행렬을 극장 좌석에 비유하면, admissible residue classes는 “사람이 앉을 수 있는 열”이다.
원래 증명은 각 열마다 사람이 충분히 있는지 검사했다. Theory 76은 마지막 단계가 실제로 쓰는
것은 **모든 허용 열의 사람 수 합계**라는 점을 확인했다. 그래서 각 열을 따로 증명하는 대신
합계만 직접 증명하는 더 약한 목표를 만들 수 있었다.

이번에는 “허용 열들이 특별한 모양이므로 Fourier/character 에너지가 보통보다 작지 않을까?”를
검사했다. 답은 **아니다**. 허용 열이 (M)개라는 사실이 고정되면 전체 character energy는
집합 모양과 상관없이 정확히 (arphi(q)M)이다. 이 방향은 더 계산해도 좋아지지 않는다.

다만 연구 경로 전체가 막힌 것은 아니다. 총에너지 대신

> Maier의 허용 열들이 강하게 반응하는 characters와, 실제 소수 분포 오차가 큰 characters가
> 서로 같은 방향으로 정렬되지 않는다는 것

을 증명하면 된다. 이것이 새로 좁힌 **direct weighted correlation 문제**다.

## 2. 무엇이 엄밀히 확인됐나

### 2.1 Maier 원문 소비식

Maier 1981 pp.266--267의 formula (I)는 모든 admissible columns에 있는 소수의 총수를
하한한다. 이후 dense row 제거는 이 합계를 사용한다. 그러므로 aggregate lower bound로 formula
(I)를 교체하는 아이디어는 논리적으로 타당하다.

반면 formula (II)는 가까운 두 열에 동시에 소수가 생기는 pair 수를 따로 상계한다. aggregate
variance가 formula (II)까지 자동으로 대신하지 않는다. 이 부분은 후속 R10의 별도 의무다.

### 2.2 Character energy

(M)개 reduced residues 집합 (mathcal A)에는

\[
 \sum_\chi|C_\chi(\mathcal A)|^2=\varphi(q)M
\]

이 정확히 성립한다. 주지표가 (M^2)를 차지하므로 비주지표 energy도

\[
 M\{\varphi(q)-M\}
\]

으로 고정된다. 이는 finite character orthogonality의 직접 결과이며 새 해석적 가정이 아니다.

### 2.3 Cauchy 경로의 한계

소수 오차 vector가 character coefficient vector와 같은 방향이면 Cauchy--Schwarz가 equality를
이룬다. 따라서 두 vector의 총 (L^2) 크기만 쓰는 어떤 증명도 보편 상수를 더 낮출 수 없다.
실제 소수 오차가 그런 나쁜 방향이라는 뜻은 아니다. **상관 또는 spectral 위치에 관한 추가
정리 없이는 개선할 수 없다**는 뜻이다.

## 3. 기존 문헌은 왜 바로 쓸 수 없나

| 후보 | 장점 | 탈락·보류 이유 |
|---|---|---|
| Friedlander--Goldston | fixed-(q) variance를 직접 연구 | 필요한 power range의 unconditional numerical multiplier·cutoff를 동시에 주지 않음 |
| Fiorilli | natural variance scale을 정교하게 분석 | GRH·linear independence 조건 또는 heuristic 성격 |
| Fiorilli--Martin | full variance의 한계를 엄밀히 밝힘 | 반례 regime는 현재와 다르지만, full natural variance가 일반 정리가 아님을 경고 |
| Vaughan/BDH | 강한 평균 결과 | 여러 moduli 평균이지 Maier가 고른 한 nested primorial이 아님 |
| Maynard large-moduli III | residue class에 uniform한 평균 | (q>Y^{1/2}) 계열이고 현재 (q\le Y^{1/21})와 범위가 반대 |
| reduced-residue 통계 | 허용 열 자체의 분포를 설명 | 그 열과 prime-error vector의 상관은 설명하지 않음 |

가장 중요한 경고는 Fiorilli--Martin Proposition 2.2다. (q\asymp Y^\delta)에서 Hooley
크기의 full variance bound를 uniform하게 증명하면 Dirichlet (L)-functions의 zero-free
half-plane까지 따라온다. 현재 (delta=1/d)이므로 이것은 생각보다 강한 해석적 정리다.
따라서 “평균적으로 오차가 자연 크기일 것”이라는 직관을 수치 증명의 입력으로 놓으면 안 된다.

그렇지만 이 문헌은 현재의 더 약한 weighted correlation 목표를 반증하지 않는다. 그 차이가
이번 감사에서 얻은 실제 진전이다.

## 4. 프로젝트 고유 학술가치

이번 단계의 고유 기여 후보는 새 소수정리를 증명한 것이 아니라, 기존 proof architecture의
정확한 최소 입력을 찾아낸 데 있다.

1. Maier formula (I)는 pointwise PNT보다 aggregate prime mass만 필요함을 source 단위로 고정.
2. full character variance는 충분하지만 과도하게 강한 목표임을 분리.
3. Maier 집합의 unweighted energy 개선 가설을 exact identity로 기각해 불필요한 연구를 제거.
4. 남은 목표를
   (sum C_\chi(\mathcal A_y)Z_\chi(Y))의 direct weighted correlation으로 축소.
5. Maier Lemma 6과 같은 (y)를 골라야 한다는 simultaneous-selection 양화사를 명시.

이 패키지는 문헌에서 같은 Sono coefficient와 (d\le186) 계약으로 정리된 형태를 이번 검색에서
찾지 못했다. 따라서 `PROJECT-DERIVED PROOF TARGET / NOVELTY NOT PEER-VALIDATED`로 분류한다.

## 5. 무엇을 주장하면 안 되나

- fixed (2\times10^{-17})이 틀렸다고 결론내리지 않는다.
- Sono의 asymptotic theorem이 거짓이라고 결론내리지 않는다.
- 모든 variance·cancellation 방법이 불가능하다고 말하지 않는다.
- Fiorilli--Martin의 작은-(q) 반례를 현재 (q=Y^{1/d})에 그대로 옮기지 않는다.
- 평균 (y)에서 좋다는 결과를 Maier Lemma 6이 선택한 (y)에 자동 적용하지 않는다.
- Theory 77의 exact algebra를 numerical (X_{\rm cert})로 확대 해석하지 않는다.

## 6. 남은 연구와 예상량

| 작업 | 내용 | 예상량 | 성공 시 효과 |
|---|---|---:|---|
| construction-family 정식화 | Maier가 허용하는 (y)들의 집합과 동시 선택 조건 고정 | 1--2주 | 잘못된 평균 양화사 방지 |
| spectral profile 감사 | ultra-short shifted character sums를 conductor·height별 분해 | 2--6주 | 기존 정리 적용 가능성 판정 |
| weighted source 특수화 | 적합한 정리가 있으면 numerical multiplier·cutoff 복원 | 1--3개월 | R09 close 후보 |
| 신규 correlation 정리 | 적합 source가 없을 때 직접 증명 | 6--24개월 이상, 불확실 | 가장 큰 이론적 진전 가능 |
| R10--R12 | pair bound, 전 error 합성, arbitrary-(X) 전달 | R09 뒤 3--8개월 이상 | (X_{\rm cert}) 계산기 준비 |

현재 사용자의 장시간 CPU가 필요한 단계는 아니다. 이 병목은 큰 소수표를 더 만드는 문제가 아니라
새 해석적 부등식을 확보하는 문제다. 작은 exact/high-precision 계산과 Lean terminal 검증만으로
오류를 줄일 수 있으며, 실제 prime sweep은 R09--R12가 닫힌 뒤에만 가치가 생긴다.

## 7. 최종 판정

Theory 76의 aggregate redesign은 타당하다. 그러나 “특별한 Maier 집합이면 total character
energy가 작다”는 후속 아이디어는 정확한 orthogonality 때문에 기각된다. 기존 fixed-(q)
variance 문헌도 현재 수치 계약의 drop-in이 아니다.

따라서 다음 연구는 full natural variance를 무리하게 증명하는 대신, Maier-selected short
residue block과 actual prime-error vector 사이의 weighted correlation만 직접 상계하는 쪽이
가장 정확하고 경제적이다. 이 정리가 확보되기 전까지 `PAP-11`, `DEP-R09`, fixed coefficient와
numerical (X_{\rm cert})는 `OPEN`이다.
