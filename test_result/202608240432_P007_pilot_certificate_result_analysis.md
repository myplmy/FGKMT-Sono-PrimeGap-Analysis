# P007 supplied-certificate pilot 결과 분석

## 최종 판정

`EXPERIMENT_PASS — supplied certificate exact audit`

사용자 실행 `20260823T185624Z_p007_pilot`은 preflight, 전체 61 tests, 제공된 modulus-2310 certificate의 415,223개 전이 정수검사, saved-artifact 재검증을 모두 통과했다. 이전 PowerShell 빈 stderr 처리 오류는 재발하지 않았다.

이 PASS의 범위는 **제공된 유한범위 개수 상한 certificate의 검증**이다. `[10^20,10^21)`의 소수를 생성하거나 gap 위치를 탐색하지 않았고, 탐색 알고리즘이 빨라졌다는 결과도 아니다.

## 실행 증거

- log: `test_result/logs/run_20260823T185624Z_p007_pilot.log`
- log SHA-256: `6d1bb5e777b367d223f5d200b35d08e2b90a1ac2b65860118d3cb29e80456e82`
- result: `test_result/run_20260823T185624Z_p007_pilot`
- Python: `W:\miniforge3\envs\FGKMT\python.exe`
- GPU: 미사용
- actual prime search: 미수행
- runner wall-clock: 파일 UTC 시각 기준 약 10초
- unit tests: 61/61 PASS, 4.647초

| 단계 | 판정 |
|---|---|
| preflight | PASS |
| unit-tests | PASS |
| approved supplied-certificate audit | PASS |
| saved-artifact verification | PASS, issue 0 |
| terminal marker | PASS |

산출물 hash도 manifest와 일치했다.

- copied certificate: `44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb`
- verification report: `b68eb09527fcfe5a8daf3b5dc98014ffeac72f4cac3b5a39d98e2ecf0bf31c92`
- manifest: `a7095e96bd266673e4b2efaf50113cb73da05cbc2d72f0264f21c7007912b651`

## 검증된 정리 범위와 수치

대상 함수는 canonical end-bounded `G(x)`가 아니라 다음 start-bounded count다.

\[
N_{\ge1856}(10^{20},10^{21})
=\#\{p:\ 10^{20}\le p<10^{21},\ p^+-p\ge1856\}.
\]

실행 산출물은 다음을 확인했다.

- modulus: 2310
- unit residue states: 480
- transition constraints: 415,223
- minimum integer slack: 0
- `pi(10^20)`: 2,220,819,602,560,918,840
- `pi(10^21)`: 21,127,269,486,018,731,928
- internal gap count: 18,906,449,883,457,813,087
- saved internal upper bound: 439,161,464,927,854,178
- right-boundary allowance: 1
- saved total upper bound: 439,161,464,927,854,179
- corrected packing total: 484,913,793,103,448,276
- packing 대비 감소: 약 9.435146788%
- saved heuristic `C`: 약 `1.102803437542279×10^15`

따라서 실행이 선언한 다음 상한은 exact certificate 검사에 의해 유효하다.

\[
N_{\ge1856}(10^{20},10^{21})
\le439{,}161{,}464{,}927{,}854{,}179.
\]

## 사후 수학 감사에서 확인한 1단위 보정

기존 P007 코드는 certificate 합산값에 `ceil`을 적용했다. 이는 상한으로 안전하지만 정수 개수에는 한 단위 약할 수 있다. 이번 certificate의 실제 유리수 내부 상한은

\[
439161464927854177.594632421806887
\]

이다. 정수 `N_internal`에는 `floor`를 적용할 수 있으므로 certificate가 더 날카롭게 주는 값은

\[
N_{internal}\le439{,}161{,}464{,}927{,}854{,}177
\]

이고 right-boundary 1을 더하면

\[
\boxed{
N_{\ge1856}(10^{20},10^{21})
\le439{,}161{,}464{,}927{,}854{,}178
}
\]

이다. 대응 heuristic `C`는 약 `1.1028034375422789845×10^15`다.

이 보정은 기존 실행의 PASS를 취소하지 않는다. `ceil`로 보고한 값도 참인 상한이기 때문이다. 다만 향후 P008 local 계산은 tight `floor`와 historic conservative `ceil`을 함께 저장하도록 교정했다. 기존 P007 run directory는 provenance 보존을 위해 수정하지 않는다.

## 쉬운 해석

이 실험은 “큰 gap이 실제로 4.39경 개 있다”고 센 것이 아니다. 가능한 모든 residue-state 이동에 대해 하나의 계산 인증서가 거짓말하지 않는지 검사한 뒤, 실제 개수는 그 숫자를 넘지 못한다는 매우 넓은 천장을 얻은 것이다.

천장을 약 9.4% 낮춘 것은 수학적으로 유효하지만 위치를 하나도 알려주지 않는다. 따라서 이 결과만으로 CPU가 건너뛸 구간은 아직 0개다. P008이 조사하는 것은 이 전역 천장을 block별 0개 인증으로 바꿀 수 있는지 여부다.

## 한계와 다음 게이트

- 실제 large gap count와 위치는 알 수 없다.
- `C`는 비교용 normalization이지 FGKMT/Sono 상수가 아니다.
- right-boundary crossing이 남아 있다.
- direct search acceleration은 증명되지 않았다.
- modulus 30030 LP는 resource guard에 의해 별도 설계 전까지 금지된다.
- 다음 P007 단계인 small-modulus full comparison은 별도 사용자 승인과 실행이 필요하다.
