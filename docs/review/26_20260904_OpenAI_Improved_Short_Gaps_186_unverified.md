# OpenAI, *Improved Short Gaps Between Primes* 비판적 검토

- 검토일: 2026-09-04 KST
- PDF 표시 저자: OpenAI; 본문은 “GPT 6 Astra”의 증명이라고 서술
- 원문: `article/unverified/Improved short gaps between primes.pdf`
- 원문 날짜: 2026-08-30
- 페이지: 39
- PDF SHA-256: `456f05e0a3ef589ebb0e9abcfd31f140f3c945adbf6950e00ef371a3c88b0930`
- 공식 공개 코드: `openai/PrimeGaps186`, 확인 commit
  `61340d0b74163003b32756bb16e91d9209a5e330`
- 심사 상태 판정: `UNVERIFIED MANUSCRIPT / PEER REVIEW NOT CONFIRMED`
- 연구 채택 판정: `HIGH-IMPACT CLAIM / STRONG ARTIFACT DESIGN / NOT INDEPENDENTLY VERIFIED`

## 1. 한 줄 결론

이 원고는 \(\mathrm{DHL}[40,2]\)와 직경 186의 admissible 40-tuple을 결합해

\[
H_1\le186
\]

을 주장한다. 공개 저장소에는 큰 Python numerical certificate와 Lean 형식화가 있어
Stadlmann 원고보다 재현성 준비가 훨씬 구체적이다. 하지만 Lean 결과는 세 개의 핵심 project
axiom에 조건부이고, Python certificate는 numerical integral/cap 입력만 검사하며 analytic
finite-field 추정까지 증명하지 않는다. 또한 요구되는 corrected custom FLINT build가 저장소에
함께 들어 있지 않고 이번 검토에서 독립 실행도 하지 않았다. 따라서 186을 검증된 정리로 채택할
수는 없다.

## 2. 기호와 주장의 정확한 뜻

이 논문의 \(H_1\)은 프로젝트 내부의 “H1 good-sieve-weight 감사 단계”가 아니다. 소수열에 대해

\[
H_1=\liminf_{n\to\infty}(p_{n+1}-p_n)
\]

을 뜻한다. 핵심 주장은 다음 두 단계다.

1. 새로운 signed-prime-minorant와 분포 입력으로 \(\mathrm{DHL}[40,2]\)를 증명한다.
2. 명시한 admissible 40-tuple의 직경이 186이므로 \(H_1\le186\)을 얻는다.

이는 작은 소수간격 정리다. 우리 연구의 maximal **large** gaps 또는 Sono의
\(2\times10^{-17}F(X)\) 하한을 직접 개선하는 결과가 아니다.

## 3. 논증 구조

### 3.1 Polymath/Maynard sieve framework

기본 뼈대는 적절한 40개의 admissible shifts와 test function을 골라 sieve-weighted 평균에서
두 소수가 동시에 존재하도록 만드는 것이다.

### 3.2 더 넓은 prime minorant support

원고는 Stadlmann의 smooth-moduli equidistribution을 출발점으로 삼되, complementary
factorization과 triply-densely-divisible support를 추가해 사용할 수 있는 minorant 영역을
넓힌다고 주장한다. 일부 기존 minorant region의 보정도 명시한다.

### 3.3 signed minorant와 cap control

positive minorant 하나가 아니라 signed 조합을 쓰고, 음의 부분이 sieve 평균을 망치지 않도록
local cap bound와 restoration term을 둔다. Theorem 4.5와 Lemma 4.8이 이 연결의 핵심이다.

### 3.4 numerical bridge

대표적으로 Lemma 4.8은 다음과 같은 유리수 bound를 제시한다.

\[
\rho_*\frac{J^-_{\lambda,H}}{I^+_H}>\frac{500103}{500000},
\qquad
\frac{L^+_H}{I^-_H}\le\frac{696075110}{10^{12}}<\frac{697}{10^6}.
\]

이들을 결합해 최종 식 (4.45)에 \(1/50000\)보다 큰 margin을 만든다고 한다. 다만 이 수치
bound의 상세 증거는 companion numerical 자료와 공개 certificate에 의존한다.

### 3.5 analytic appendix

Appendix는 prime-field exponential sums, dispersion, dense divisibility 관련 estimate를
제시한다. 여기에는 Vinogradov 표기, sufficiently large 조건과 power-saving 형태가 다수 남아
있다. 이 층은 코드 certificate와 별개로 전문가의 독립 증명 검토가 필요하다.

## 4. 공개 저장소에서 확인한 것

공식 저장소 [openai/PrimeGaps186](https://github.com/openai/PrimeGaps186)의 위 commit을
README, `formalization.yaml`, certificate source를 source-level로 확인했다. 이번에는
clone·dependency 설치·certificate 실행을 하지 않았고, 저장소의 companion
`short_gaps_numerics.pdf`도 별도 취득·렌더링하지 않았다. 따라서 companion PDF에만 있는
세부 수치 증거까지 검토했다는 뜻은 아니다.

### 4.1 Lean 형식화

`formalization.yaml`은 총 여섯 axiom을 보고하며, 표준 Lean axiom 세 개 외에 다음 project
input 세 개가 남아 있다.

1. `kloosterman3_bound`
2. `kloosterman2_correlation_bound`
3. `physical_integral_bounds`

따라서 Lean의 `dhl_40_2`, tuple theorem, `primeGapLiminf_le_186`은 이 입력들을 전제로 한
**조건부 형식화**다. 저장소도 cited estimates와 numerics가 Lean 안에서 증명되지 않았음을
명시한다. `sorry`가 없다는 사실만으로 세 입력이 참이라는 증명이 되지는 않는다.

또한 공개 metadata의 review status는 self-assessment이며, 모든 auxiliary declaration의 의미와
원문 대응을 독립 전문가가 완전히 감사했다는 증거는 아니다.

### 4.2 Python numerical certificate

`prime_gap_186_certificate.py`는 약 2,736줄이며 다음을 포함한다.

- Python `Fraction`을 사용한 exact coefficient
- python-flint/Arb를 이용한 outward interval
- binary64 directed-bound regression check
- 98,304 intervals, 160-bit Arb precision의 production policy
- 104개 outer와 45개 inner physical-integral upper bound, 3개 cap bound
- 11개 coefficient signature와 degree 0–6의 coefficient data
- 97개 source component와 149개 raw form 검증
- 최종 \(\rho(\text{numerator}-\text{loss})/\text{upper}-1>1/50000\) 판정
- worker 1 또는 4, 진행 출력, 비덮어쓰기 output

이는 단순 floating 결과 파일보다 훨씬 강한 certificate 설계다. 그러나 다음 한계가 있다.

1. 성공 JSON은 Lean의 세 project axiom 전부를 제거하지 않는다.
2. signed polynomial convolution의 오류를 고친 custom FLINT 3.6.0 build가 필요하지만 그 고정
   binary/patch 전체가 저장소에 bundled돼 있지 않다.
3. receipt에 전체 source/dependency SHA-256을 묶는 기능은 확인되지 않았다.
4. 이번 연구에서는 해당 환경을 설치하거나 certificate를 독립 실행하지 않았다.

## 5. 강점

1. 논문의 수치 주장을 공개 코드·조건부 형식화와 연결했다.
2. exact rational과 directed interval을 분리해 쓰고 low-level arithmetic regression을 둔다.
3. 형식화가 조건부임을 숨기지 않고 axiom 목록을 공개한다.
4. 최종 판정 margin을 유리수로 고정해 “그림상 좋아 보임”을 증거로 쓰지 않는다.
5. source component, raw form, cap을 세분화해 fail-closed 검증이 가능하도록 설계했다.

## 6. 독립 채택을 막는 문제

### 6.1 형식화는 조건부다

Lean이 최종 정리를 도출하는 경로가 있더라도 핵심 exponential-sum 두 개와 physical-integral
input이 axiom이다. 이는 “논리적 접착부가 기계검사됐다”는 강한 장점이지만 “전체 수학 정리가
Lean으로 무조건 증명됐다”는 뜻은 아니다.

### 6.2 numerical certificate와 analytic proof의 범위가 다르다

Python은 수치 적분과 cap margin을 검증한다. Appendix의 finite-field estimate, dispersion,
support transfer가 맞는지는 코드 성공만으로 확인되지 않는다. 두 증거층을 합쳐 말하면 안 된다.

### 6.3 재현 환경이 완전히 self-contained하지 않다

README는 Python 3.12.13, NumPy 2.2.6, python-flint 0.9.0과 corrected FLINT 3.6.0을 지정한다.
특히 수정 FLINT는 표준 설치와 동일하지 않다. exact patch·build recipe·binary hash가 없으면 다른
환경의 PASS가 원 저자의 PASS와 같은 산술 경로인지 입증하기 어렵다.

### 6.4 새 analytic 아이디어의 위험도가 높다

complementary factorization, triple dense divisibility, signed minorant/cap argument는 결과를 크게
개선하는 바로 그 새 부분이다. 따라서 선행 정리 인용만 확인하는 것으로 부족하고, support cover,
부호, uniformity, endpoint를 줄 단위로 독립 검토해야 한다.

### 6.5 심사·독립 검증 상태

PDF에서 확인되는 저널 게재나 동료심사 표시는 없다. 공개 저장소의 self-review와 코드 공개는
동료심사나 독립 재현을 대신하지 않는다. GitHub issue 네 건은 내용상 수학 검토가 아니었다.

## 7. 우리 연구에서 사용할 수 있는 내용

### 현재 직접 사용할 수 없음

- \(H_1\le186\), \(\mathrm{DHL}[40,2]\)를 검증된 theorem으로 전제
- 조건부 Lean theorem을 무조건부 formal proof라고 서술
- Python PASS를 analytic appendix까지 검증한 것으로 서술
- 이 결과를 FGKMT/Sono large-gap coefficient나 \(X_{\mathrm{cert}}\)에 대입

### 지금 바로 참고할 수 있는 방법론

1. machine-readable axiom/obligation inventory
2. symbolic/exact/interval layer의 분리
3. numerical margin의 rational threshold 고정
4. source component와 최종 form을 동시에 검증하는 certificate 구조
5. low-level library bug를 겨냥한 regression test
6. formal proof가 의존하는 외부 수치·해석 입력을 숨기지 않는 fail-closed metadata

이는 H1b/T1 원장의 hardening에 유용하지만, 논문의 수학 결과 자체를 가져오는 것은 아니다.

### Sono/FMT threshold와의 제한적 관련성

새 equidistribution·factorization 기술이 장기적으로 H1c/PAP의 후보가 될 수는 있다. 그러나
현재 원고의 목표 parameter, minorant 부호, modulus 구조는 FGKMT/Sono chain과 다르고,
numerical \(X_{\mathrm{cert}}\)에 필요한 finite constants도 제공하지 않는다. 따라서 새로운 별도
proof-obligation audit 없이 “더 강한 분포 정리이므로 threshold가 낮아진다”고 추론하지 않는다.

## 8. 독립 재현을 진행한다면

이번 1차 문헌·정적 코드 검토에는 사용자의 로컬 다운로드가 필요하지 않았다. 다음 단계에서
실제 재현성을 조사하기로 별도 승인하면 다음 자료가 필요하다.

1. commit `61340d0b74163003b32756bb16e91d9209a5e330`의 repository archive
2. companion `short_gaps_numerics.pdf`
3. corrected FLINT 3.6.0의 정확한 patch/build recipe 또는 hash가 고정된 binary
4. 실행 host·compiler·dependency version

그 뒤에도 검증 단계를 분리한다.

```text
certificate environment reproduced
!= numerical certificate PASS
!= Lean conditional build PASS
!= three project axioms discharged
!= theorem independently peer reviewed
```

## 9. 최종 판정

```text
논문 주장: DHL[40,2], hence H_1 <= 186
코드/형식화 공개: yes
Lean proof: conditional on 3 project axioms
numerical certificate design: strong, but not locally reproduced
analytic new inputs: independent expert review required
peer review: not confirmed
우리 연구의 theorem input: prohibited at present
우리 연구의 certificate methodology: useful
```

공식 자료는 [PrimeGaps186 저장소](https://github.com/openai/PrimeGaps186),
[`formalization.yaml`](https://github.com/openai/PrimeGaps186/blob/main/formalization.yaml),
[`prime_gap_186_certificate.py`](https://github.com/openai/PrimeGaps186/blob/main/prime_gap_186_certificate.py)다.
