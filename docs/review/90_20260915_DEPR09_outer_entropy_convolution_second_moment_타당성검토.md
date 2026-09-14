# DEP-R09 outer entropy·convolution second moment 타당성검토

- 검토일: 2026-09-15
- 대상: Theory 82
- 판정:
  <code>FINITE REDUCTION VALID /
  ANALYTIC PRIME-ERROR ENERGY STILL OPEN /
  NO NUMERICAL X_CERT YET</code>

## 1. 쉬운 설명

지금 필요한 것은 “좋은 residue 선택이 실제로 나올 확률”과 “그 선택에서 prime-count
오차가 너무 크지 않을 확률”을 같은 무작위 실험 안에서 동시에 확보하는 것이다.

FMT의 첫 단계는 여러 작은 소수마다 주사위를 하나씩 던지는 것과 같다. 나중 단계가 앞선
주사위 결과를 보고 적응적으로 행동하더라도, 최종 CRT 번호 하나를 미리 지정하면 첫 단계
주사위들의 면은 전부 강제된다. 따라서 그 번호가 나올 확률은 첫 단계의 모든 면을 맞출
확률 \(1/Q_{\mathcal S}\)보다 클 수 없다.

이 사실로 “나쁜 번호 하나에 확률이 몰리는 현상”을 제한할 수 있다. 이어 모든 CRT 번호에서
prime error의 제곱을 합한 유한 Fourier identity를 사용하면, 실제 FMT law의 평균제곱을
character prime-error energy 하나로 줄일 수 있다.

## 2. 맞는 부분

### 2.1 adaptive inner output에서도 atom cap이 유지된다

최종 residue \(r\)는 각 outer prime \(s\)에서 \(A_s=-r\pmod s\)를 강제한다.
inner output의 조건부분포가 무엇이든 그 조건부확률은 1 이하이므로

\[
 \Pr(m_\omega=r)\le Q_{\mathcal S}^{-1}
\]

이다. 이는 outer와 inner의 독립성을 잘못 가정하지 않는다.

### 2.2 event indicator를 버리지 않았다

Theory 81에서 교정한 정확한 사건은 \(S_{\rm sieve}\)다. 이번 reduction은

\[
 \Pr(S_{\rm sieve},m_\omega=r)\le Q_{\mathcal S}^{-1}
\]

를 사용하므로 분모 floor와 분자 moment의 probability law가 다시 어긋나지 않는다.

### 2.3 finite Fourier 정규화가 일치한다

Theory 80의 \(C_\chi\)가 conjugated character sum이라는 점을 보존하면
\(R(m)=\varphi(q)\sum_{s\in I}e(m+s)\)다. 이 \(\varphi(q)\)를 빠뜨리면 최종 gate가
완전히 달라지는데, Theory 82는 Parseval의 \(1/\varphi(q)\)와 함께 정확히 상쇄해
\(\varphi(q)N^2V/Q_{\mathcal S}\)를 얻었다.

### 2.4 strict boundary가 유지된다

확률질량을 양수로 남기려면 equality가 아니라

\[
 V<
 \tau^2p_*Q_{\mathcal S}M_{\min}^2Y^2/
 \{\varphi(q)N^2\}
\]

가 필요하다. 코드와 Lean terminal도 이 strict inequality를 보존한다.

## 3. 아직 증명되지 않은 부분

가장 중요한 미해결 입력은

\[
 V(Y,q)=\sum_{\chi\ne\chi_0}|Z_\chi(Y)|^2
\]

의 fully numerical upper bound다. 다음 중 어느 것도 이번 결과가 자동으로 주지 않는다.

- 실제 primes가 natural variance scale을 만족한다는 finite theorem.
- 한 prescribed growing primorial에 대한 uniform cutoff.
- primitive character 결과를 모든 characters modulo \(q\)로 옮기는 명시적 손실.
- PAP-11, DEP-R09, fixed \(2\times10^{-17}\).

따라서 이 단계는 “필요한 정리가 무엇인지 정확히 줄였다”는 진전이지 “그 정리를
증명했다”는 진전은 아니다.

## 4. 선행연구 검토 결과

- Davenport--Erdos의 exact moving-shift identity는 수학적 구조를 확인하는 좋은
  benchmark다. 그러나 prime modulus·uniform shift이므로 actual FMT drop-in이 아니다.
- Friedlander--Goldston과 Vaughan은 fixed modulus의 prime variance와 직접 관련되지만,
  이번에 확인한 공개 source만으로 numerical multiplier와 공통 cutoff를 복원하지 못했다.
- BDH형 정리는 modulus 평균을 사용하므로 한 predetermined primorial을 보장하지 않는다.
- 현대 moving-interval character-sum 결과도 prime modulus와 uniform random shift라는
  quantifier 차이가 있다.

그러므로 “variance라는 단어가 같다”는 이유로 source theorem을 끼워 넣지 않은 판정은
타당하다.

## 5. 수치적 의미

outer entropy는 gate를 \(Q_{\mathcal S}\)배 완화한다. 그러나 full primorial의 크기는
대략 \(e^x\), outer product는 대략 \(e^z\)이고 \(z=o(x)\)다. trivial character별
상계를 제곱합하면 여전히 대략 \(\varphi(q)^2/Q_{\mathcal S}\)에 해당하는 큰 certificate
손실이 남는다.

반면 genuine variance 규모 \(V\ll\varphi(q)Y\log q\)를 fully numerical하게 얻으면
\(Y=q^d\)의 거대한 \(Y\) factor 덕분에 gate 통과 가능성이 높다. 즉 앞으로 필요한
연구는 더 큰 prime 범위를 무작정 계산하는 일이 아니라 fixed-primorial variance를
명시화하는 일이다.

## 6. \(X_{\rm cert}\) 영향

| 질문 | 답 |
|---|---|
| 기존보다 강한 bounded \(X_{\rm cert}\) 범위를 얻었나? | 아니오 |
| fixed \(2\times10^{-17}\)을 독립 인증했나? | 아니오 |
| threshold calculator를 만들 단계인가? | 아니오 |
| 장시간 CPU 계산이 필요한가? | 현재 아니오 |
| 무엇이 진전됐나? | actual FMT law의 same-law moment를 식 (82.3) 하나로 정확히 축약 |

## 7. 권장 다음 단계

1. Friedlander--Goldston·Vaughan류 fixed-\(q\) variance proof의 upper-bound 방향,
   modulus 범위와 숨은 상수를 원문 단위로 감사한다.
2. 그 정리가 prescribed primorial에 적용되지 않으면, large sieve/explicit formula로
   식 (82.3)에 필요한 더 약한 weighted energy만 직접 증명할 수 있는지 본다.
3. source normalization과 finite cutoff가 확보된 뒤에만 Lean 형식화와 numerical
   threshold calculator로 넘어간다.

현재 사용자에게 실행을 요청할 계산은 없다.
