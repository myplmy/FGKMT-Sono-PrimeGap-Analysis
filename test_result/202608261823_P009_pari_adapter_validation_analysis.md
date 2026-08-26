# P009 PARI/GP certificate adapter 검증 결과

## 1. 판정

`EXPERIMENT_PASS — ADAPTER_ONLY / ACTUAL_1E20_NOT_RUN`

PARI/GP 2.15.4에서 작은 정수 certificate 경로와 64-bit를 넘는 ECPP vector 경로를
실제로 생성하고, 각각을 새 GP 프로세스의 `primecertisvalid`로 다시 검증했다. 저장
artifact hash 재검증과 wrong-subject 음성 대조도 PASS했다.

이 결과는 P009 production adapter가 의도한 형식으로 작동한다는 뜻이다. 아직
`[10^20,10^20+1000)`의 경계 소수·합성수 증거를 생성하지 않았고, single-block
`CERTIFIED_ZERO`나 탐색 가속을 증명한 결과가 아니다.

## 2. 실행 증거

- 성공 run: `test_result/run_20260826T090950Z_p009_pari_adapter_validation`
- 성공 log: `test_result/logs/run_20260826T090950Z_p009_pari_adapter_validation.log`
- log SHA-256:
  `ed0414653e66f98f105cd3d428913b159e9a57c42ca4740770c4ab50de1b7284`
- manifest SHA-256:
  `025fd56c6c4712dea099cdb9a2dc805351c2811e07a304e031505f1d2e9da841`
- hash-bound saved verification report SHA-256:
  `09f7aa36dce61d4472988f948aa1d84fb3e8e83c8db0da741ce3d3e724af1ca7`
- GP: `GP/PARI CALCULATOR Version 2.15.4 (released)`
- fixed Python: `W:\miniforge3\envs\FGKMT\python.exe`
- terminal marker: `[PASS] P009 PARI adapter validation completed.`
- actual `10^20` experiment: `false`
- GPU: `false`

## 3. 검증 결과

| 대상 | certificate 형식 | 생성 시간 | 생성 peak RSS | 새 프로세스 검증 시간 | 검증 peak RSS | 판정 |
|---|---|---:|---:|---:|---:|---|
| `101` | small integer | 0.111 s | 7,680 KiB | 0.119 s | 7,424 KiB | PASS |
| `1000000000000000000000000000057` | ECPP vector | 0.114 s | 22,036 KiB | 0.109 s | 8,448 KiB | PASS |

중간 정수 certificate는 132 bytes이며 SHA-256은
`b31794629bb9a3e71bb37bc20f2cd9fb366438583804db26551763484b2c664d`다.
저장 형식은 integer와 list만 허용하는 canonical JSON이고, 같은 문자열이 GP vector
문법으로도 유효하도록 제한했다. certificate의 첫 subject가 요청 정수와 일치하는지
Python에서 먼저 검사한 뒤 GP verifier를 호출한다.

wrong-subject 대조에서는 같은 ECPP artifact를 다른 정수에 결합하려는 시도가 GP 호출
전에 거부되었다. saved verifier는 두 subject를 다시 검증했고 issue는 0개였다.
추가 report는 원 manifest의 SHA-256을 보존하므로 P009 actual prerequisite가 단순
`status`가 아니라 저장 후 재검증 완료까지 확인한다.

## 4. 첫 실행 실패와 교정

첫 run `20260826T090908Z`는 certificate 생성 전에 preflight에서 중단됐다.

- 실패 log SHA-256:
  `620edfa77a12580a4ac1840596876a703a5e42423ed374d5f03a42277d2b23a8`
- 원인: Ubuntu의 GP banner가 stdout이 아니라 stderr에 출력됐는데 version probe가
  stdout만 검사함
- 교정: exit code 0을 요구하면서 stdout과 stderr 양쪽에서 공식 banner prefix를 검색
- 회귀시험: stderr banner fixture 추가, targeted 14 tests PASS

실패 run은 실제 certificate 생성 단계에 도달하지 않았으며 결과 directory도 만들지
않았다. 로그는 교정 provenance로 보존한다.

## 5. 경고와 한계

- WSL이 오래된 Windows `D:\...` PATH 항목 일부를 번역하지 못한다는 warning을 매 GP
  호출 때 출력했다. GP exit code와 certificate 검증은 모두 0/PASS였으므로 이번 결과를
  무효화하지 않지만 로그 노이즈로 남긴다.
- 생성기와 verifier는 서로 다른 GP 프로세스지만 같은 PARI 구현을 사용한다. 이는
  fresh-process exact recheck이지 완전히 독립된 두 번째 ECPP 구현 검증은 아니다.
- 약 `10^30` 한 소수의 빠른 결과를 실제 P009 경계 두 소수의 비용 보장으로 일반화하지
  않는다. actual single-block에서 wall time·RSS·artifact bytes를 다시 측정해야 한다.
- P010A modulus-2310 replay PASS manifest가 생기기 전에는 P009 actual runner가
  prerequisite gate에서 중단되도록 준비했다.

## 6. 다음 판정 게이트

1. 사용자가 P010A modulus-2310 replay를 실행하고 terminal/saved PASS를 제공한다.
2. 그 manifest를 P009 actual runner에 입력한다.
3. actual block에서 last-prime certificate, `(p,b)` 전 정수 factor coverage, right-prime
   certificate, `q-p<1856`을 함께 exact 검증한다.
4. single-block zero가 나와도 전체 search acceleration이라고 부르지 않고 비용과
   coverage 확장 가능성을 별도 평가한다.
