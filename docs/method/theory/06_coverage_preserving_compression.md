# Coverage-preserving candidate·certificate compression

## 지위

`OPEN RESEARCH PROGRAM + REJECTED_AS_STATED COMPONENTS`

## 목표

고정 `G`와 finite range에서 실제 모든 `gap>=G` start를 포함하는 candidate family
`C`를 만들고,

\[
\forall p\text{ with }p^+-p\ge G,\quad p\in C
\]

를 증명한다. 그 뒤 각 candidate를 exact rejection witness로 제거한다.

## 필요한 네 정리

1. **Coverage:** 실제 candidate 누락 0
2. **Soundness:** 각 rejection witness가 실제로 candidate를 제거
3. **Compression:** `|C|` 또는 certificate bytes가 baseline보다 충분히 작음
4. **Verification cost:** 생성비용까지 포함한 총비용이 baseline보다 작음

## 유지할 원자 witness

각 integer start `p`를 다음 중 하나로 제거할 수 있다.

- Type I: `p`가 합성수라는 exact factor/proof
- Type II: `(p,p+G-1]` 안에 증명된 소수 존재

모든 `p`에 대한 union coverage가 있으면 gap 부재가 따른다. 그러나 candidate를 전부
나열하면 sound하지만 compression은 아니다.

## 폐기한 주장

- `B=2` block union이 `[p+1,q-1]`: 실제 union은 `[p+1,q-2]`
- 미지의 실제 `p`로 `S=p-1`을 정의한 뒤 이를 compression theorem으로 부름
- `S=2^k+2j`, unrestricted `j`가 후보를 줄임: 모든 짝수를 중복 표현할 뿐
- 같은 wheel residue가 같은 actual prime witness 위치를 가짐

wheel state는 작은 소수 divisibility geometry만 재사용한다. absolute primality evidence는
translation되지 않는다.

## 연구 가능한 개선 방향

- 엄밀한 phase cover와 작은 canonical representative family
- composite-cover/Jacobsthal certificate를 absolute interval에 매핑
- repeated witness를 DAG·range proof로 압축하되 verifier soundness 유지
- certificate bytes per covered candidate와 verification operations 측정
- 별도 구현 또는 proof assistant로 verifier theorem 확인

## 중단 기준

- coverage proof가 결국 모든 start exact test를 요구
- certificate 생성+검증이 baseline보다 느림
- ledger가 100 GB 또는 runtime이 168시간을 넘음
- compression이 아니라 좌표만 바꾼 tautology
