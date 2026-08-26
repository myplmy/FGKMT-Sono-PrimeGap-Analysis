# Local block count와 right-boundary witness

## 지위

`THEOREM + EXACT_FINITE + IMPLEMENTED_TOY + OPEN_ACTUAL`

## P008 local count 분해

start-bounded block `[a,b)`에서 두 endpoint가 block 안에 있는 large gap 수의 상한을
`U_internal`이라 하자. block 마지막 소수에서 `b` 밖으로 넘어가는 gap은 최대 1개다.
경계가 미해결이면

\[
U_{total}\le U_{internal}+1
\]

이고 nonempty block을 zero라고 부를 수 없다.

P008 actual 네 block은 exact prime-count 입력과 저장 검증을 PASS했지만 certified zero가
0개였다. `L=1000`만 internal floor가 0이고 crossing 때문에 total 1이었다.

## boundary witness lemma

`p`가 `[a,b)`의 마지막 소수이고, 증명된 소수 `q>=b`가 있으며

\[
q-p<H
\]

이면 실제 다음 소수 `p^+<=q`이므로 `p^+-p<H`다. 따라서 crossing은 large gap이 아니다.
`q`가 바로 다음 소수임을 증명할 필요는 없지만 다음은 모두 필요하다.

1. `p`의 primality proof
2. 모든 `p<n<b`의 compositeness evidence
3. `q`의 primality proof
4. exact inequality `q-p<H`

이 witness와 `U_internal=0`을 결합할 때만 block 전체 `CERTIFIED_ZERO`가 된다.

## P009 G1 구현

toy `[100,120)`에서 `p=113`, `q=127`, 114–119 factor coverage를 검증했다. 다음 오류를
모두 거부하는 tests가 PASS했다.

- composite coverage hole
- 나누어떨어지지 않는 factor
- `q-p=H` equality
- probable-prime label
- 기존 result overwrite

실제 `10^20` endpoint에는 PARI/GP ECPP certificate를 계획한다. 동일 PARI verifier로
재검사하면 machine-checkable이지만 완전한 독립 구현은 아니다.

## 알고리즘 한계

길이 1,000 block 하나가 zero여도 전체 폭 `9 x 10^20`에는 `9 x 10^17` blocks가
필요하다. boundary witness 성공은 soundness feasibility이지 전체 가속 성공이 아니다.
