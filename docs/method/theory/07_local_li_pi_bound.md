# Local li-pi 항등식과 올바른 증명 방향

## 지위

`THEOREM + REJECTED_AS_STATED ALGORITHM LINK + OPEN`

## 정확한 항등식

\[
D(x)=\operatorname{li}(x)-\pi(x),\qquad
N(x,h)=\pi(x+h)-\pi(x)
\]

이면

\[
D(x+h)-D(x)=\Delta_h\operatorname{li}(x)-N(x,h).
\]

## infimum 하한이 주는 것

\[
Q(X,h)=\inf_x[D(x+h)-D(x)]\ge-q
\]

이면

\[
N(x,h)\le\Delta_h\operatorname{li}(x)+q.
\]

즉 prime count **상한**이다. 우변이 1보다 작으면 `N=0`을 증명해 empty interval과
gap 발견을 돕는다. 이는 gap 부재를 증명하는 방향이 아니다.

## gap 후보를 배제하려면

candidate가 요구하는 empty interval 안에 소수가 있다는 `N>=1`이 필요하다. 이
항등식만 쓴다면 `Delta D`의 **상한**과 `Delta li`의 하한을 결합해야 한다. 기존
`Q=inf` 하한을 더 높이는 연구로는 이 목적을 달성하지 못한다.

## 반올림

비엄격 `N<=R`과 integer `N`에서

\[
N\le\lfloor R\rfloor.
\]

`ceil(R)-1`은 `N<R`을 별도로 증명한 경우에만 맞다.

## 현재 판정

- `Q` 하한 → 1856-gap absence accelerator: `REJECTED_AS_STATED`
- `Q` 하한 → empty-window discovery: `OPEN`
- `sup Delta D` 상한 → nonempty certificate: `OPEN`, 기존 문헌으로 fixed 1856 전범위
  보장은 없음
- provenance 없는 `Q=-280.6166400756`: 정본 사용 금지

## 후속 연구 선택지

1. 이 층을 본 탐색에서 제거하고 heuristic priority로만 사용
2. empty block 발견용 별도 P011로 재정의
3. rigorous `Delta D` upper bound가 실제 1856 scale에 닿는 새 정리가 있을 때만
   absence path 재개
