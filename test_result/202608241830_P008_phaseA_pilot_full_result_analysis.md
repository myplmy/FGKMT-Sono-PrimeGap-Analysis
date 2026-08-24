# P008 local residue-state certificate phase-A 결과 분석

## 최종 판정

`EXPERIMENT_PASS / DIRECT_LOCAL_SKIP_NEGATIVE`

P008 toy pilot, exact prime-count 입력 준비, phase-A full이 모두 정상 종료됐고 저장 산출물의 독립 `Fraction` 재계산과 hash 검증도 issue 0으로 통과했다. 구현의 안전장치는 의도대로 작동했다.

그러나 실제 `x=10^20` 네 block에서는 certified-zero가 한 건도 없었다. 가장 작은 길이 1,000 block만 internal bound가 0이었지만 오른쪽 경계 gap이 미해결이라 total upper bound는 1이었다. 따라서 현재 modulus-2310 인증서로 직접 block을 건너뛸 수 있다는 증거는 얻지 못했다.

## 실행 증거

### Toy pilot

- log: `test_result/logs/run_20260824T053954Z_p008_pilot.log`
- log SHA-256: `43cf808ca9d681daaa18b0f7712019effc20e55dcfdc9746bd33be128aafa9c8`
- result: `test_result/run_20260824T053954Z_p008_pilot`
- blocks: 4
- internal-zero candidates: 3
- certified zero: 3
- unresolved right boundary: 0
- direct prime search: 미수행
- saved verification: PASS, issue 0

Toy fixture에서는 boundary를 exact하게 해결했기 때문에 3개 zero 인증이 정상적으로 나왔다. 이는 코드가 “internal zero”와 “전체 block zero”를 구분한다는 기능검사이지 실제 `10^20` 결과가 아니다.

### Exact prime-count 준비

- log: `test_result/logs/run_20260824T054725Z_p008_primecount_prepare.log`
- log SHA-256: `61ed7dd2da374e1b7bd48224f208d0b0cb3688e8f7c251a4b97dc3770338f59c`
- root: `tmp/p008-primecounts/20260824T054725Z_p008_primecount_prepare`
- five unique endpoints: PASS
- Gourdon vs. Deleglise–Rivat: 5/5 exact integer 일치
- 두 알고리즘 누적 wall time: 약 57분 55초
- 최대 RSS: 216,848 KiB, 약 212 MiB
- GPU/search: 미사용

| endpoint | exact prime count |
|---:|---:|
| `10^20-1` | 2,220,819,602,560,918,840 |
| `10^20+999` | 2,220,819,602,560,918,864 |
| `10^20+999,999` | 2,220,819,602,560,940,472 |
| `10^20+999,999,999` | 2,220,819,602,582,629,266 |
| `10^20+999,999,999,999` | 2,220,819,624,275,680,733 |

### Phase-A full

- log: `test_result/logs/run_20260824T064748Z_p008_full.log`
- log SHA-256: `1ae74f8986f5ca0ac4b66a3aa5090c2be130fa8029ced6ef8d5b18c8d4c8f51e`
- result: `test_result/run_20260824T064748Z_p008_full`
- blocks: 4
- internal-zero candidates: 1
- certified zero: 0
- unresolved right boundary: 4
- saved verification: PASS, issue 0
- direct acceleration proved: false

| block length L | start-prime K | raw internal q | tight internal floor | unresolved crossing 포함 total |
|---:|---:|---:|---:|---:|
| 1,000 | 24 | 0.499300014467527 | 0 | 1 |
| 1,000,000 | 21,632 | 486.369964055189447 | 486 | 487 |
| 1,000,000,000 | 21,710,426 | 486,149.337346680925757 | 486,149 | 486,150 |
| 1,000,000,000,000 | 21,714,761,893 | 486,138,172.074728280481962 | 486,138,172 | 486,138,173 |

## 왜 작은 block도 건너뛰지 못했는가

길이 1,000에서는 internal bound가 0이다. 즉 block 안에서 시작하고 block 안에서 끝나는 1,856 이상 gap은 없다는 상한이다. 하지만 block 안의 마지막 소수에서 오른쪽 바깥의 다음 소수로 넘어가는 gap 한 개가 남는다. 그 gap이 1,856보다 작다는 exact 증거가 없으므로 안전한 total upper bound는 1이고 `CERTIFIED_ZERO`로 바꿀 수 없다.

이 경계 문제는 단순 구현 누락이 아니라 필요한 추가 증명이다. 마지막 소수 `p<B`와 그 다음의 증명된 소수 `q`를 찾아 `q-p<1856`임을 보이면 충분하다. `p`와 `q` 사이에 다른 소수가 있더라도 실제 consecutive gap들은 더 짧아지므로 이 증명은 안전하다.

## 알고리즘 후보가 되기 위한 정량 기준

전체 폭은 `9×10^20`이다. 길이 L의 block으로 완전히 나누면 필요한 block 수는 `9×10^20/L`이다.

| L | 필요한 block 수 | 현재 q | q<1에 필요한 상한 개선 배수 |
|---:|---:|---:|---:|
| `10^3` | `9×10^17` | 0.4993 | 내부는 이미 0, 경계 해결 필요 |
| `10^6` | `9×10^14` | 486.37 | 486배 초과 |
| `10^9` | `9×10^11` | 486,149 | 약 48.6만 배 |
| `10^12` | `9×10^8` | 486,138,172 | 약 4.86억 배 |

168시간 안에 끝내려면 비현실적으로 빠른 `1 microsecond/block`을 가정해도 block 길이가 약 `1.49×10^9` 이상이어야 한다. 관측된 비율 `q/L≈4.86138×10^-4`를 적용하면 그 길이에서 q는 약 72만이다. 즉 계산속도만 맞추려 해도 local upper bound를 대략 70만 배 이상 낮춰야 하고, 각 block의 crossing도 해결해야 한다.

저장공간 100 GB를 지키려면 block당 단 1 byte만 저장해도 L이 `9×10^9` 이상이어야 하며, 현실적인 100 bytes/block이면 L이 `9×10^11` 이상이어야 한다. 후자의 현재 q는 약 4.38억이므로 4억 배 이상의 개선이 필요하다.

위 break-even은 고정 FGKMT Python의 40-digit `Decimal`로 별도 재계산했다. `1 microsecond/block` 시간문턱의 L은 `1,488,095,238.095...`, 대응 q는 `723,419.899...`; 1 byte/block 저장문턱 q는 `4,375,243.549...`; 100 bytes/block 저장문턱 q는 `437,524,354.867...`였다.

따라서 “정밀도를 소수점 몇 자리 더 계산”해서 해결되는 문제가 아니다. 새로운 certificate/cover 정리가 q의 크기 차수를 크게 낮추거나, zero block 대신 모든 실제 gap start를 포함하는 매우 희소한 candidate cover를 직접 만들어야 한다.

## 쉬운 해석

P008은 넓은 지역마다 “큰 gap이 몇 개 이하인지”라는 천장을 붙여 본 실험이다. 작은 1,000칸 지역에서는 내부에 큰 gap이 없다는 데까지 갔지만, 지역 경계를 가로지르는 한 건을 지우지 못했다. 더 큰 지역에서는 천장이 수백, 수십만, 수억으로 커졌다.

따라서 실험은 정상적으로 성공했지만, 기대한 직접 건너뛰기 방법은 현재 형태로는 실패했다. 이는 코드 실패가 아니라 중요한 음성 연구결과다.

## 다음 게이트

1. 한두 개 block에서 exact crossing witness를 싼 비용으로 만들 수 있는지 증명·pilot한다.
2. 단일 block zero보다 전체시간·메모리·disk break-even을 먼저 계산한다.
3. modulus 확대는 dense LP가 아니라 separation-oracle/cutting-plane 설계가 있을 때만 검토한다.
4. 위 조건을 통과하지 못하면 P008 direct-tiling은 종료하고 candidate-cover 정리 연구로 전환한다.
