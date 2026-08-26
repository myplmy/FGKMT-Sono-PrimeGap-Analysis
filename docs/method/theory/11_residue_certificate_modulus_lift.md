# Residue-state certificate의 배수 modulus exact lift

## 상태

`THEOREM / MOD30030_EXACT_ACTUAL_PASS / STRICT_IMPROVEMENT_FALSE`

## 명제

threshold를 `H`, source modulus를 `M`, target modulus를 `M'=kM`이라 하자. `M`과
`M'`은 이 프로젝트의 even-squarefree wheel 계약을 만족한다고 가정한다. source
certificate가 모든 source transition에 대해

\[
\lambda d+\mu+\phi(r)-\phi(s)\ge w,
\qquad \lambda\ge0
\]

를 만족하면 target potential을

\[
\phi'(r')=\phi(r'\bmod M)
\]

로 두어 같은 `lambda`, `mu`, `t`와 finite-range objective를 갖는 target certificate를
만들 수 있다.

## 증명 요지

target unit residue는 reduction 후 source unit residue다. target transition의 차이
대표 `d'`는 대응 source 차이와 modulo `M`에서 같다. small transition이면 source의
최소 양의 대표가 `d'`보다 크지 않고 source에서도 검사된다. large transition이면 target에서 허용되는 최소 대표는
source congruence class에서 허용되는 최소 대표보다 작을 수 없다. `lambda>=0`이므로
대표가 커져도 좌변은 감소하지 않는다. potential 차이는 reduction 정의로 동일하다.
따라서 모든 target inequality가 source inequality에서 따라온다.

## 중요한 한계

- lift는 modulus 30030에서 **기존 상한이 적어도 재현 가능함**을 보인다.
- objective 계수가 같으므로 lift 자체는 상한을 strict하게 낮추지 않는다.
- 더 좋은 modulus-30030 certificate가 존재하는지는 별도 cutting-plane discovery 문제다.
- count certificate는 gap 위치나 search acceleration을 자동으로 제공하지 않는다.

## 구현 검증

`source.finite_gap_replay.lift_certificate_exact_to_modulus`가 정수 potential을 lift한다.
`source.finite_gap_separation.scan_exact_certificate_constraints`는 full matrix를 저장하지
않고 모든 target transition을 signed-int64 overflow 사전증명 뒤 exact scan한다.
modulus-30030 actual은 2026-08-26 사용자 bounded queue에서 수행됐다. 5,760 states와
35,224,647 constraints에서 floating violation 0, exact violation 0, minimum integer slack
0을 확인했다. total bound는 `439161464927854179`로 source와 같아 strict improvement는
없다. 다음 질문은 별도 G4 cutting-plane이 더 좋은 potential을 찾는지 여부다.
