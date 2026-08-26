# P009 — P008 boundary witness와 알고리즘 break-even 게이트

## 1. 상태

`G1_TOY_PASS / G2_PARI_INSTALL_PASS / G2.5_ADAPTER_PASS / G3_RUNNER_READY / P010A_PASS_REQUIRED`

P008 phase-A는 정상 PASS했지만 실제 네 block의 certified zero는 0개였고, current modulus-2310 certificate의 direct tiling은 시간·저장공간 문턱에 수십만–수억 배 부족했다. P009는 더 큰 sweep을 바로 실행하지 않고, 길이 1,000에서 남은 right-boundary 1개를 exact하고 싼 증거로 없앨 수 있는지와 그 방법이 전체 알고리즘 후보가 될 자원 조건을 만족하는지 분리해 판정한다.

## 2. 연구 질문

1. P008의 `x1e20_L1000` block에서 internal bound 0과 결합할 exact crossing witness를 만들 수 있는가?
2. witness 생성·독립검증의 시간, RAM, disk 비용은 얼마인가?
3. 같은 방법을 여러 block에 적용할 때 168시간·32 GB·100 GB 제한을 만족할 수 있는가?
4. single-block zero가 가능하더라도 전체 탐색 후보가 되려면 bound 또는 candidate count가 얼마나 더 줄어야 하는가?

## 3. 비목적

- `[10^20,10^21)` 전체를 tiling하거나 탐색하지 않는다.
- 한 block의 zero를 전체 범위 가속 증명으로 부르지 않는다.
- probable-prime만으로 endpoint를 인증하지 않는다.
- PARI/GP를 사용자 승인 없이 설치하지 않는다.
- modulus 30030 dense LP를 실행하지 않는다.
- GPU를 사용하지 않는다.

## 4. 입력과 provenance

- P008 certificate: `ai_dev_tool/temp_prime_gap_count_algorithm/source/C2310_certificate.txt`
- certificate SHA-256: `44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb`
- P008 full log: `test_result/logs/run_20260824T064748Z_p008_full.log`
- P008 full log SHA-256: `1ae74f8986f5ca0ac4b66a3aa5090c2be130fa8029ced6ef8d5b18c8d4c8f51e`
- P008 exact counts: `tmp/p008-primecounts/20260824T054725Z_p008_primecount_prepare/prime_counts.csv`
- target block: `[10^20,10^20+1000)`
- threshold H: 1856
- saved internal exact bound: `q=0.499300014467527`, `floor(q)=0`
- current boundary status: `UNRESOLVED`, total bound 1

## 5. 수학 계약

block의 마지막 소수를 `p<B`라고 하자. 다음 조건을 machine-checkable하게 증명한다.

1. `p`는 소수다.
2. 모든 정수 `n`에 대해 `p<n<B`이면 `n`은 합성수다. 따라서 `p`는 block의 마지막 소수다.
3. `q≥B`인 증명된 소수 `q`가 존재하고 `q-p<1856`이다.

그러면 실제 `p` 다음 소수 `p^+`에 대해 `p^+≤q`이므로

\[
p^+-p\le q-p<1856.
\]

따라서 unresolved crossing도 large gap이 아니며, P008의 internal bound 0과 결합해 해당 block의 total large-gap count가 0임을 증명한다.

`q`가 바로 다음 소수임을 별도로 증명할 필요는 없지만 `p`가 block의 마지막 소수라는 증명은 생략할 수 없다.

## 6. 알고리즘 후보 정량 게이트

전체 폭 `W=9×10^20`에 대해 다음을 동시에 만족해야 한다.

\[
n_{blocks}=\lceil W/L\rceil,
\quad n_{blocks}t_{block}\le604800\text{ s},
\quad n_{blocks}b_{block}\le10^{11}\text{ bytes}.
\]

### Gate A — 과학적 feasibility

- selected block에 exact `CERTIFIED_ZERO`를 1개 이상 생성
- 독립 verifier issue 0
- probable-prime 의존 0

Gate A는 수학적 가능성만 판정한다. 알고리즘 후보 통과가 아니다.

### Gate B — 최소 throughput

- `1 microsecond/block`이라는 이상적 가정에서도 L은 `1.488×10^9` 이상이어야 한다.
- 관측 `q/L≈4.86138×10^-4`이면 이 길이의 q는 약 723,000이다.
- 따라서 현재 certificate의 bound를 적어도 약 70만 배 낮추거나, zero 대신 매우 희소한 sound candidate cover를 내야 한다.

### Gate C — 저장공간

- 1 byte/block이면 L은 `9×10^9` 이상, 현재 q는 약 4.38 million이다.
- 100 bytes/block이면 L은 `9×10^11` 이상, 현재 q는 약 437.5 million이다.
- ledger는 100 GB 미만이어야 한다.

### Gate D — 실제 baseline 비교

\[
T_{certificate}+T_{ledger}+T_{survivor}
<T_{baseline}
\]

를 동일 coverage 계약과 CPU-only 조건에서 실측해야 한다. false negative가 한 건이라도 있거나 coverage mapping이 없으면 시간 비교를 하지 않고 중단한다.

## 7. 단계와 승인 게이트

### G0 — P008 결과와 자원 문턱 고정 (`PASS`)

- actual block four rows audited
- direct certified zero 0개 확인
- 168시간·100 GB break-even 계산 완료
- 근거: `test_result/202608241830_P008_phaseA_pilot_full_result_analysis.md`

### G1 — boundary witness generator/verifier 구현 (`IMPLEMENTED / TARGETED_TEST_PASS`)

ChatGPT가 수행할 작업:

1. toy small-integer generator와 exact re-verifier
2. proven-prime/composite evidence schema
3. non-overwrite manifest와 hash
4. FGKMT Python preflight와 toy PowerShell runner
5. probable-prime 결과만 주어지면 FAIL하는 unit test
6. PARI/GP 설치 helper와 ECPP adapter 자리 계약

구현 파일:

- `source/boundary_witness.py`
- `source/boundary_witness_cli.py`
- `tests/test_boundary_witness.py`
- `scripts/experiments/p009/run_p009_boundary_witness_toy.ps1`
- `test_done/install_pari_gp_wsl-20260826T084156Z-done.sh`
- `source/pari_certificate.py`, `source/pari_certificate_cli.py`
- `source/boundary_witness_pari.py`, `source/boundary_witness_pari_cli.py`
- `scripts/experiments/p009/run_p009_single_block_actual.ps1`

2026-08-26 targeted 8 tests와 fixed-Python preflight는 PASS했다. toy verifier는
`[100,120)`에서 마지막 소수 113, 오른쪽 증명 소수 127, 정수 114–119의
nontrivial factor coverage를 재검증한다. coverage hole, 잘못된 factor,
`q-p=threshold`, probable-prime label, overwrite는 모두 거부한다.

현재 “독립 verifier”는 생성 결과를 다시 계산하는 별도 verification path라는
뜻이다. 완전히 독립적인 두 번째 구현 또는 proof assistant 검증은 아직 없다.
실제 `10^20` 입력은 이 단계에서 실행하지 않았다.

### G2 — PARI/GP 환경 확인·설치 (`PASS`)

사용자가 Ubuntu WSL에 PARI/GP 2.15.4를 설치했고 `primecert`/
`primecertisvalid` smoke test가 PASS했다.

- 설치 log: `tmp/setup/install_pari_gp_20260826T084156Z.log`
- 설치 helper 보존본:
  `test_done/install_pari_gp_wsl-20260826T084156Z-done.sh`

### G2.5 — certificate adapter (`EXPERIMENT_PASS`)

Codex가 사용자 승인 범위에서 `101`과
`1000000000000000000000000000057`의 certificate를 생성하고 각각 새 GP 프로세스로
검증했다. small integer/ECPP vector, subject binding, wrong-subject 음성대조, 저장 hash와
saved recheck가 모두 PASS했다. actual `10^20` block은 실행하지 않았다.

- run: `test_result/run_20260826T090950Z_p009_pari_adapter_validation`
- log: `test_result/logs/run_20260826T090950Z_p009_pari_adapter_validation.log`
- 분석: `test_result/202608261823_P009_pari_adapter_validation_analysis.md`

### G3 — single-block exact crossing pilot (`RUNNER_READY / P010A_PASS_REQUIRED`)

- 대상: `x1e20_L1000` 한 block
- 예상시간: 2–20분의 초기 추정
- 예상 RAM: 1 GiB 미만
- 예상 disk: 1 GiB 미만
- 성공: exact certified zero, independent verification issue 0, terminal PASS
- 중단: witness 생성 30분 초과, proof evidence 누락, probable-only endpoint, RAM 4 GiB 초과

### G4 — 10-block boundary cost sample (`CONDITIONAL`)

G3가 PASS할 때만 서로 다른 endpoint 10개를 사전 고정해 실행한다.

- 예상시간: 약 10–120분
- 목적: crossing witness wall time 분포와 artifact bytes/block 실측
- 결과로 168시간·100 GB gate를 다시 계산
- 95th-percentile 비용으로도 break-even이 불가능하면 종료

### G5 — algorithm-candidate 승격 (`BLOCKED`)

다음 중 하나가 추가로 증명돼야 한다.

1. L≥`1.49×10^9` 규모에서 zero certificate와 crossing을 충분히 싸게 생성, 또는
2. 모든 실제 gap start를 포함하면서 survivor 수와 ledger 비용이 baseline보다 작은 candidate cover

어느 쪽도 없으면 P009는 mathematical feasibility 결과로만 종료한다.

## 8. 필수 산출물

- `test_result/logs/run_<UTC>_p009_boundary_<mode>.log`
- `test_result/run_<UTC>_p009_boundary_<mode>/boundary_witness.json`
- `composite_evidence.csv`
- `verification_report.json`
- `resource_metrics.json`
- `manifest.json`
- 결과 분석보고서

각 증거는 p, B, q, primality proof method, composite interval coverage, threshold, elapsed, peak RSS, artifact SHA-256을 저장한다.

## 9. 성공·경고·중단 기준

성공:

- P008 saved internal floor 0 재검증
- last-prime property exact proof
- q의 proven primality와 `q-p<1856`
- independent verifier issue 0
- stdout/stderr/traceback 전체 로그
- GPU 미사용, resource cap 준수

경고:

- single block PASS는 direct algorithm speedup이 아님
- PARI/GP 버전 차이
- 10-block sample의 대표성 한계

즉시 중단:

- probable-prime만 사용
- block 내부 합성수 coverage hole
- 32 GB RAM, 100 GB disk 또는 168시간 예상 초과
- full `[10^20,10^21)` tiling 시도
- 결과 폴더 덮어쓰기

## 10. 현재 사용자 수행절차

먼저 `test_plan/P010A_P007_count-upper-bound.md`의 replay를 실행한다. 그 결과의
`manifest.json`을 `<P010A_MANIFEST>`로 넣어 아래 P009 명령을 실행한다. 같은 폴더의
`saved_verification_report.json`이 해당 manifest hash에 묶인 PASS여야 한다. P010A가
PASS하기 전에는 P009 actual을 실행하지 않는다.

환경: Windows PowerShell 또는 FGKMT Conda Prompt

```powershell
cd Z:\FGKMT-Sono-PrimeGap-Analysis
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiments\p009\run_p009_single_block_actual.ps1 -ConfirmP009Actual -P010AReplayManifest '<P010A_MANIFEST>'
```

예상시간: 2–20분. 완료 후 terminal marker, log 경로, result directory를 회신한다.

## 11. 참고문헌·도구

1. PARI/GP official documentation: https://pari.math.u-bordeaux.fr/doc.html
2. PARI/GP `primecert` and `primecertisvalid`:
   https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Arithmetic_functions.html
3. Seth Troisi `prime-gap`: https://github.com/sethtroisi/prime-gap
4. Oliveira e Silva, Herzog, Pardi, DOI https://doi.org/10.1090/S0025-5718-2013-02787-1
5. Ziller–Morack, arXiv:1611.03310, https://arxiv.org/abs/1611.03310
