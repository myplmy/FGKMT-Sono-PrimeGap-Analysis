# 실제 maximal gap의 empirical lower envelope

## 지위

`EXACT_FINITE + EMPIRICAL + HYPOTHESIS`

## 고정 결과

P003의 `3,814,280 <= x <= 10^20`에서

- end-bounded interval 64개, record jump 63개
- global minimum `H = 37.8168603967216805...`
- 위치 `x=1,346,294,311,330`, gap 540
- jump 직후 `H` 회복 63/63
- `x=10^20`에서 `G=1724`, `F=38.7144559825...`
- minimum Sono ratio 약 `1.890843 x 10^18`
- `H<1`과 `H<2 x 10^-17` 관측 0건

이다. 이후 최근-window local envelope는 40대 초반으로 회복했다. 그러므로 global
running minimum의 정체와 최근 local floor의 움직임은 구분해야 한다.

## 구조적으로 예상되는 현상

plateau 안에서는 `G`가 고정되고 `F`가 증가하므로 `H`는 감소한다. 새 record에서
gap이 커지면 `H`가 회복할 수 있다. P003의 63/63 회복은 강한 구현 진단값이지만,
그 자체를 새로운 깊은 수론 정리로 과대해석하지 않는다.

## 후속 가설

### E1 — local floor nonmonotonicity

`H`의 global running minimum은 단조 비증가하지만 decade/rolling local envelope는
장기적으로도 국소 상승과 하강을 반복한다.

반증: 더 넓고 신뢰 가능한 범위에서 사전 고정한 여러 local 정의가 모두 단조 감소.

### E2 — global minimum sparse updates

verified range가 커질수록 global minimum 갱신 record의 비율이 낮아진다.

반증: 독립적인 범위 확장에서 갱신 밀도가 안정 또는 증가.

### E3 — Sono constant와 empirical scale의 큰 finite gap

계산 가능한 범위에서는 actual `H`와 `2 x 10^-17` 사이의 배수가 여전히 매우 크다.

이는 Sono 상수의 보수성을 기술하는 finite 가설이지 그 비율의 무한 극한 가설이 아니다.

## 올바른 검증법

- 범위를 보기 전에 bin shift와 rolling window를 고정
- end/start 경계 paired 보고
- global과 local envelope를 별도 그림·표로 저장
- serial dependence 때문에 단순 회귀 p-value를 theorem처럼 사용하지 않음
- 새 source의 exhaustive limit와 record provenance를 먼저 고정
