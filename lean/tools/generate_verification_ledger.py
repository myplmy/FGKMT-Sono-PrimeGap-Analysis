"""Generate the checked-in formula inventory and human verification ledger.

This is a deterministic repository-maintenance tool.  It does not invoke Lean
and it never upgrades dependencies.  Kernel status is read only from the
separately reviewed verification_status_v1.json mapping.
"""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

from inventory_theory_formulas import build_inventory


STATUS_MEANING = {
    "KERNEL_PASS": (
        "표시한 명제가 project-local axiom, `sorry`, `admit` 없이 Lean 커널을 통과"
    ),
    "CONDITIONAL_KERNEL_PASS": (
        "명시한 premise에서 결론으로 가는 합성은 통과했지만 premise의 source 증명은 미인증일 수 있음"
    ),
    "DEFINITION_ONLY": "표기·함수 정의의 전사이며 참·거짓 증명 대상이 아님",
    "PARTIAL_FORMALIZATION": "display 식의 핵심 일부만 형식화; 식 전체 PASS가 아님",
    "SOURCE_THEOREM_UNFORMALIZED": "source analytic theorem을 확인했지만 Lean 독립 증명은 없음",
    "NOT_YET_FORMALIZED": "inventory만 완료; Lean 선언 없음",
    "PARSE_REVIEW_REQUIRED": (
        "hash-pinned 원문의 수식 경계가 불완전해 안전 복구했지만 원문은 소급 변경하지 않음"
    ),
}


NOTES_BY_ID = {
    "T01-U001": "정의 전개·양수성·exp(exp(exp(1))) 위 strict monotonicity 커널 검증",
    "T01-U002": "finite record 표현",
    "T01-U003": "보조 start-bounded 정의",
    "T01-U004": "정수 경계만; G 상수성 premise는 후속",
    "T01-U005": "양의 end-bounded 정수 plateau의 오른쪽 끝점 minimum 커널 검증",
    "T07-U001": "D와 N의 함수 정의는 후속",
    "T07-U002": "순수 환대수 항등식",
    "T07-U003": "discrepancy lower premise 명시",
    "T07-U004": "상계 방향 커널 검증",
    "T07-U005": "Mathlib floor Galois connection",
    "T10-U001": "exact primality/next-prime는 매개변수",
    "T10-U002": "후보 superset soundness",
    "T10-U003": "witness soundness",
    "T10-U004": "total coverage",
    "T10-U005": "Nat exact arithmetic",
    "T11-U001": "source inequality와 대표 증가 premise",
    "55.4": "J,h 완료; cell I_j는 후속",
    "55.5": "Nat.ceil에서 세 bound 유도",
    "55.6": "grid-union measure premise 이후 scalar 합성",
    "55.10": "floor-log window p≤R<5p premise",
    "55.13": "pre-cover count 상계 이후 상수 합성",
    "55.14": "t=η/8을 명시적 premise로 사용",
    "55.15": "r0,e* gate를 premise로 사용",
    "55.16": "relative-error 대수 합성",
    "55.24": "Rankin counting은 source premise; rpow 지수 정규화는 커널 검증",
    "55.25": "Rosser--Schoenfeld prime harmonic 입력 이후 terminal 상계",
    "55.26": "S_delta·h(t) 정의와 t≠1의 정확한 적분 항등식 커널 검증",
    "55.27": "prime-sum 정규화·h(1)·decimal slack·종단 합성 검증; theta 1.01624 bound와 Stieltjes 비교는 미형식화",
    "T55-U002": "Ein interval-integral 정의 전사; delta L=w는 downstream premise",
    "55.28": "removable singularity, 두 finite interval 비교, improper integral·51/50 factor 커널 검증",
    "T55-U003": "Ein split과 103/100 상계 전체 커널 검증",
    "55.29": "Stieltjes premise 이후 Ein bound를 내부 호출해 actual parameter와 189/160 합성",
    "55.30": "2^(-3/4)<3/5와 terminal 대수 검증; prime/j-sum 비교는 premise",
    "55.31": "세 analytic/counting estimate 이후 product-log 합성",
    "55.32": "q>=200 actual log lower bounds 커널 검증",
    "55.33": "exact rational arithmetic",
    "55.34": "55.32 actual hypotheses에서 decay >4b 커널 검증",
    "55.35": "Rankin·Euler-product premise 이후 final exp cancellation 커널 검증",
    "55.36": "정수 상수만; smooth count chain은 후속",
    "55.39": "analytic/count premise 이후 최종 상계 대수",
    "56.1": "Sono c_ZFR=1/24에서 a=1/80 exact 대입",
    "56.2": "c_ZD=16에서 D_PAP=160 exact 대입",
    "56.3": "a*D_PAP=2와 C_PAP=1-exp(-2) exact 정의",
    "56.4": "0<C_PAP<1 exact 실수 부등식",
    "T56-U001": "Jutila Theorem 1의 source 진술; epsilon multiplier와 proof는 Lean 미형식화",
    "T56-U002": "finite error 합성의 명시적 analytic premise 쌍",
    "56.5": "principal/error premise 이후 finite slack 합성; analytic premise는 미인증",
    "56.6": "Jutila source epsilon/3 재매개화의 exact 지수 대수",
    "56.7": "alpha<=4/5의 low-alpha exponent bridge",
    "56.8": "DEP-R09 finite PAP 목표; Gallagher/Jutila/Maier rate와 cutoff 미형식화",
    "57.1": "Sono Proposition 5.3 source statement; analytic theorem은 Lean 미형식화",
    "57.2": "T>=2에서 log(T(1+T))<=3logT와 zero-free 폭 방향을 커널 검증",
    "57.3": "c_ZFR/3=1/72와 인쇄값 3c_ZFR=1/8의 불일치 exact 검증",
    "57.4": "McCurley Theorem 1 source statement; analytic theorem은 Lean 미형식화",
    "57.5": "McCurley Theorem 2 source statement; analytic theorem은 Lean 미형식화",
    "57.6": "direct c1=1/24의 R<12 수치 포함관계만 검증; family theorem 전체는 미형식화",
    "57.7": "Gallagher Theorem 7 source statement; hidden multiplier와 cutoff는 OPEN",
    "57.8": "c_ZD=16, D=160의 density-power boundary exact 검증",
    "57.9": "Q=x^(1/D)의 lower range에 필요한 D^2<=log x와 D=160 gate 검증",
    "57.10": "direct-McCurley repair exponent a0=1/240와 a0D=2/3 exact 검증",
    "57.11": "Gallagher-Maier nonprincipal error의 honest multiplier interface; rate 미형식화",
    "57.12": "같은 지수에서 multiplier 제거 iff K<=1을 커널 검증",
    "57.13": "log K budget으로 multiplier를 exponent에 흡수하는 충분조건 커널 검증",
    "57.14": "principal/error analytic premise 이후 multiplier 보존 one-sided 합성",
    "57.15": "교정 finite PAP analytic target; common cutoff와 source proof 미형식화",
    "58.1": "DEP-R09 fixed-coefficient pointwise PAP 목표; drop-in source 없음",
    "58.2": "exceptional modulus와 principal/nonprincipal/psi-to-pi를 포함한 finite target interface",
    "58.3": "D=160 coefficient-capacity 필요조건; 고정밀 Python 진단만 완료",
    "58.4": "최신 Sono arXiv v4와 journal에 그대로 인쇄된 상수 연결",
    "58.5": "Bennett et al. large-modulus cutoff source statement",
    "58.6": "Thorner-Zaman uniform PNT의 숨은 numerical multiplier interface",
    "58.7": "Thorner-Zaman fully explicit nonexceptional density source statement",
    "58.8": "Thorner-Zaman fully explicit exceptional-removed density source statement",
    "58.9": "Benli-Goel-Twiss-Zaman effective Deuring-Heilbronn source constants",
    "58.10": "Sono downstream coefficient capacity 함수 정의",
    "58.11": "D=160 최소 C_PAP 고정밀 진단; Lean 미형식화",
    "58.12": "D=160 총 상대오차 budget 고정밀 진단; Lean 미형식화",
    "58.13": "exp(-2) 이후 추가 finite-error slack 고정밀 진단; Lean 미형식화",
    "58.14": "낙관 C_PAP=1, D=186 coefficient 진단; Lean 미형식화",
    "58.15": "낙관 C_PAP=1, D=187 coefficient 진단; Lean 미형식화",
    "58.16": "현재 downstream 식의 낙관 integer-D capacity 결론; source 채택 전 Lean 미형식화",
    "59.1": "DEP-R09 Branch S의 fixed-D finite pointwise PAP 목표; analytic source package 없음",
    "59.2": "D=160 coefficient·total-error 고정밀 진단; Lean 미형식화",
    "59.3": "Thorner-Zaman Theorem 2.1 density source 진술; multiplier·cutoff 미형식화",
    "59.4": "숨은 multiplier를 보존하는 fixed-D transfer 진단 정의",
    "59.5": "positive K, eta, D의 logarithmic budget에서 exponential error 상계를 커널 검증",
    "59.6": "K별 최소 decay constant 80-dps 진단; Python 재계산",
    "59.7": "Jutila Theorem 1 density source 진술; epsilon multiplier·cutoff 미형식화",
    "59.8": "Thorner-Zaman Remark 2.4의 density exponent-to-theta source 관계",
    "59.9": "Jutila Theorem 1-prime source 진술; sufficiently large D cutoff 미수치",
    "59.10": "Jutila Theorem 2 source 진술; D0(epsilon)와 proof multiplier 미수치",
    "60.1": "Ramaré--Zuniga explicit coefficient의 p.54 Theorem 1-prime tau=8/5 exact 대입; 식 (3.6)에는 사용 금지",
    "60.2": "Graham--Jutila Lemma 4 full asymptotic source theorem; hidden O multiplier는 미형식화",
    "60.3": "Ramaré--Zuniga Corollary 1.3 source theorem; actual 호출의 analytic proof는 미형식화",
    "60.4": "Jutila Theorem 1-prime actual parameter 정의 전사",
    "60.5": "finite log-ratio의 exact 유리 대수를 커널 검증",
    "60.6": "finite power correction의 exponent 대수만 커널 검증; source real-power 합성은 미형식화",
    "60.7": "finite delta cutoff sufficient condition; 후속 JL5/6/8 예산과 함께 형식화 예정",
    "60.8": "Jutila Lemma 5 source asymptotic; uniform o(1) rate와 cutoff는 OPEN",
    "60.9": "Jutila Lemma 6 detector lower bound; Mellin과 tail 상수는 OPEN",
    "60.10": "Jutila Lemma 7 modified Halasz source statement; finite proof는 후속",
    "60.11": "Jutila Lemma 8 local zero-count source statement; implied constant는 OPEN",
    "60.12": "Huxley--Jutila exponent-2 source density; epsilon multiplier와 cutoff는 OPEN",
    "66.1": "Theory 60 고정 coefficient를 p.54 Theorem 1-prime scope로 재분류; exact 값은 커널 검증",
    "66.2": "Jutila p.52 식 (3.6)의 실제 theta-dependent parameter 정의",
    "66.3": "식 (3.6)의 tau_theta와 tau_theta-1 exact 유리 대수를 커널 검증",
    "66.4": "Ramaré--Zuniga coefficient의 theta-dependent exact 특수화를 커널 검증",
    "66.5": "0<theta<=1/21에서 K_BV(theta)<13/theta를 커널 검증",
    "66.6": "coefficient 끝점 slack을 포함한 유리 부등식 proof를 식 66.5와 함께 커널 검증",
    "66.7": "finite log-ratio exact 유리 대수를 커널 검증; real log/power source 연결은 별도",
    "66.8": "2 log L<=L premise 아래 18/(7 theta) transfer를 조건부 커널 검증",
    "66.9": "analytic weighted sum source는 미형식화; 두 explicit multiplier 합성만 커널 검증",
    "66.10": "Lemma 7 weight quotient 정의",
    "66.11": "elementary exp slack과 abstract quotient<5는 커널 검증; actual M,N monotonic transfer는 부분형식화",
    "66.12": "integration area lower algebra는 커널 검증; source integration identification은 부분형식화",
    "66.13": "Theory 64 detector coefficient 재사용 정의",
    "66.14": "terminal left coefficient 정의; analytic detector source proof는 Theory 64 경계 유지",
    "66.15": "off-diagonal D-exponent 전개를 커널 검증",
    "66.16": "0<theta<=1/21의 uniform negative exponent margin을 커널 검증",
    "66.17": "finite log gate premise 아래 total exponent margin을 조건부 커널 검증",
    "66.18": "Jutila p.53 terminal qualitative inequality; hidden multipliers 미형식화",
    "66.19": "A-E>0인 fail-closed terminal absorption algebra를 커널 검증",
    "66.20": "Ramaré 2016 explicit density의 additive source term; drop-in transfer는 없음",
    "T67-U001": "Jutila p.53 shifted-contour 정성 상계; source complex proof는 Lean 미형식화",
    "67.15": "source L·Gamma·contour premise 이후 exact contour coefficient 곱셈을 조건부 커널 검증",
    "T67-U002": "C_CONT(theta)의 계산기용 정의",
    "67.17": "zeta integral-test 상계를 premise로 받아 elementary contour majorant를 조건부 커널 검증",
    "T67-U003": "Jutila 식 (3.6)의 q,T,theta actual 범위 전사",
    "T67-U004": "Jutila 식 (3.6)의 s=u+iv actual 범위 전사",
    "67.1": "Jutila shifted-contour 적분 identity; complex contour 이동은 Lean 미형식화",
    "67.2": "actual contour에서 0<Re z<=1/7인 범위 대수를 커널 검증",
    "T67-U005": "primitive conductor에서 imprimitive product character로의 Euler-factor identity; Lean 미형식화",
    "67.3": "4/sqrt(6) 보정의 제곱 유리값만 커널 검증; finite prime-product inequality 전체는 부분형식화",
    "67.4": "22/7 real triangle budget은 커널 검증; complex absolute-value reduction은 미형식화",
    "67.5": "Bennett et al. Lemma 5.6 (5.3) source Rademacher bound; Lean 미형식화",
    "67.6": "nonprincipal branch의 coefficient envelope만 커널 검증; analytic source 합성 전체는 부분형식화",
    "67.7": "C_NP<9/4를 pi·sqrt 유리 상계에서 커널 검증",
    "67.8": "principal-character Dirichlet L과 zeta의 Euler-factor identity; Lean 미형식화",
    "67.9": "Hasanalizade--Shen--Wong Proposition 3.8 source zeta bound; Lean 미형식화",
    "67.10": "principal ratio의 squared cross-multiplied 16/9 상계를 커널 검증; complex quotient identity는 부분형식화",
    "T67-U006": "principal branch coefficient C_P<12는 커널 검증; source analytic 합성 전체는 부분형식화",
    "67.11": "C_P<12를 pi·sqrt 유리 상계에서 커널 검증",
    "67.12": "두 source branch 중 하나를 premise로 받아 공통 coefficient 12 합성을 조건부 커널 검증",
    "67.13": "비음수 크기의 triangle·monotonicity 합성만 커널 검증; complex-power modulus는 부분형식화",
    "T67-U007": "Gamma recurrence·Euler integral의 pointwise complex bound; Lean 미형식화",
    "67.14": "Gamma split의 finite coefficient identity만 커널 검증; complex improper integral은 부분형식화",
    "67.16": "Riemann zeta 급수 integral-test 상계; source/direct proof는 Lean 미형식화",
    "67.18": "elementary endpoint 45408은 커널 검증; zeta 포함 decimal은 비구간 수치진단이라 부분형식화",
    "68.1": "actual primed outer absolute-sum 함수 정의",
    "68.2": "Jutila Lemma 3와 one-variable envelope를 premise로 받은 3R^2 종단 대수는 조건부 커널 검증",
    "68.3": "Jutila Lemma 2의 h Euler-product 정의 전사",
    "T68-U001": "actual f(p)=mu(p)phi(p)=-(p-1) 특수화 전사",
    "T68-U002": "squarefree lcm support와 floor endpoint는 문서·exact Python 검산; 전체 prime-factor induction 미형식화",
    "68.4": "exclusive/common local 절댓값 대수는 커널 검증; 전체 Euler-product 곱셈은 부분형식화",
    "68.5": "공통소수 local printed bound는 커널 검증; Jutila Lemma 3 전체는 source theorem 미형식화",
    "68.6": "exclusive/common reciprocal local factor는 커널 검증; delta identity 전체 prime-factor induction은 부분형식화",
    "68.7": "one-variable outer weight와 합의 정의",
    "68.8": "Jutila printed product bound를 premise로 한 Cartesian-square 합성; finite family 전체는 Lean 미형식화",
    "T68-U003": "squarefree divisor identity는 문서·exact Python 검산; prime-factor induction 미형식화",
    "68.9": "finite divisor double-count와 floor(K/d)/d 상계는 커널 검증; actual subset-extension은 부분형식화",
    "68.10": "Mathlib zeta(2) identity와 pi<3.15에서 finite reciprocal-square sum<5/3을 커널 검증",
    "T68-U004": "one-variable 5K/3 premise에서 pair 3K^2 및 floor endpoint 합성을 조건부 커널 검증",
    "T68-U005": "Theory 67 shifted-contour source/conditional 결과의 재사용",
    "68.11": "contour와 Lemma 3 multiplier 합성 정의",
    "68.12": "Theory 67 elementary contour 상계 이후 factor 3 coefficient 항등식을 조건부 커널 검증",
    "68.13": "theta=1/21의 exact endpoint 136224를 커널 검증",
    "69.1": "JL7-RES actual theta,D,L 범위 전사",
    "69.2": "analytic residue bound를 premise로 받은 endpoint coefficient 52 합성을 조건부 커널 검증",
    "69.3": "Jutila 식 (3.6)의 R,z1,x actual parameter 전사",
    "69.4": "선택 shifted zero의 actual real·height 범위 전사",
    "69.5": "Jutila printed p.53 principal residue source 식; complex·character 합은 Lean 미형식화",
    "69.6": "Lemma 3 reciprocal local factor는 Theory 68에서 부분형식화; full diagonal product identity는 source theorem",
    "69.7": "대각화 뒤 actual finite r-sum 정의",
    "69.8": "xi·eta interval endpoint와 길이 정의",
    "69.9": "Gamma recurrence에 의한 removable-pole identity; complex integral 전체는 Lean 미형식화",
    "69.10": "pole-cancelled ladder kernel 정의",
    "69.11": "closed-form은 Python 독립 quadrature로 검산; Lean 형식화 대기",
    "69.12": "xi·eta rational coefficient는 커널 검증; d-a와 실제 log 연결은 부분형식화",
    "69.13": "interval coefficient product<7은 커널 검증; triple-integral identification은 부분형식화",
    "69.14": "off-diagonal coefficient<7은 커널 검증; complex modulus transfer는 부분형식화",
    "T69-U001": "0<=Re z<=2/21에서 19/21<=Re(1-z)<=1을 커널 검증",
    "69.15": "40/19<3 rational endpoint는 커널 검증; complex Gamma Euler-integral 비교는 부분형식화",
    "69.16": "Jutila selected-system spacing Delta=1/L 정의",
    "69.17": "two-sided Basel coefficient 10/3은 커널 검증; character-height ordering은 source theorem 미형식화",
    "T69-U002": "diagonal pair coefficient 21의 exact 항등식 커널 검증",
    "T69-U003": "off-diagonal pair coefficient 70의 exact 항등식 커널 검증",
    "69.18": "theta<=1에서 row coefficient 91 합성을 커널 검증; analytic pair premise는 조건부",
    "69.19": "Rankin·Euler-product actual r-sum direct proof; Lean 전체 형식화 대기",
    "69.20": "excluded-prime local ratio의 exponential 상계; Python 검산, Lean 형식화 대기",
    "69.21": "Rankin·excluded-prime·zeta rational multipliers 2*3*2=12만 부분형식화",
    "T69-U004": "Jutila p.53 바깥 residue prefactor 전사",
    "69.22": "12*91*theta<=52 endpoint와 nonnegative-base 합성을 커널 검증",
    "70.1": "JL7-ABSORB actual nonprincipal near-one fixed-modulus 범위 전사",
    "70.2": "half-margin premise 아래 selected-system bound와 exact C_J 계수 합성을 조건부 커널 검증",
    "70.3": "한 parity system bound에서 even/odd local zero-count로의 비음수 합성을 조건부 커널 검증",
    "70.4": "weighted call 34/theta^2와 denominator quotient 5의 exact 단일 곱을 커널 검증",
    "70.5": "Theory 68 contour-plus-Lemma3 multiplier 재사용 정의",
    "70.6": "detector·integration-area 정의와 lower 일부는 선행 Lean 선언; analytic identification은 미형식화",
    "70.7": "pi^2<10과 rational detector strict lower를 커널 검증",
    "70.8": "Jutila Lemma 7 detector left side의 source analytic 식; Lean 미형식화",
    "70.9": "predecessor source estimates를 합친 actual terminal analytic inequality; 전체 Lean 미형식화",
    "70.10": "A,B,E 정규화와 generic terminal algebra 일부를 조건부 형식화",
    "70.11": "normalized off-diagonal coefficient E 정의",
    "70.12": "q/phi(q)<=6L premise에서 exact square factor 36을 조건부 커널 검증",
    "70.13": "half-margin ratio P와 logarithmic cutoff 정의",
    "70.14": "exponential cutoff와 E<=A/2 premise에서 strict terminal 합성을 조건부 커널 검증",
    "70.15": "log P<=P를 사용한 rational fallback implication을 커널 검증",
    "70.16": "L>=exp(8)에서 4logL/L<=29/252 finite gate를 커널 검증",
    "70.17": "JL6·finite-log·absorption cutoff의 공통 maximum 정의",
    "70.18": "half-margin terminal algebra와 exact selected-system coefficient를 조건부 커널 검증",
    "70.19": "theta=1/21의 Cpre,Cbar,cbar,gamma,P,C_J exact endpoint를 커널 검증",
    "71.1": "가변 modulus 평균의 공통 D=Q^2*T와 L=log D 정의",
    "71.2": "averaged terminal과 even/odd local-count premise 이후 near-one primitive nonprincipal count를 조건부 커널 검증",
    "71.3": "x와 local square radius r의 actual averaged 정의",
    "71.4": "Jutila 식 (3.7) generalized Halasz source inequality; complex/character proof는 Lean 미형식화",
    "71.5": "modulus-dependent pseudocharacter detector 정의 전사",
    "71.6": "각 primitive conductor의 Mellin scale과 common R,z2 정의",
    "71.7": "상·하 envelope 방향의 비음수 곱 대수와 exponent identity만 커널 검증; real-rpow/source identification은 부분형식화",
    "71.8": "0<=theta<=1/21의 common power-condition exponent margin을 선행 커널 정리로 검증",
    "71.9": "Mellin exponent 대수와 theta=1/21 endpoint는 커널 검증; complex Mellin bound와 real-rpow transfer는 부분형식화",
    "71.10": "four-loss common averaged detector cutoff의 기호적 maximum 정의",
    "71.11": "source detector identity를 제외한 four-part loss budget과 (1-theta) 회복만 부분형식화",
    "71.12": "phase magnitude·alignment 중 scalar totient cancellation만 커널 검증",
    "71.13": "phase-weighted complex sum과 finite-family 합은 미형식화; 항별 scalar cancellation만 커널 검증",
    "71.14": "primitive product가 principal인 정확한 character 조건은 source theorem으로 보존",
    "71.15": "phase-residue-pseudocharacter totient factor의 exact scalar cancellation을 커널 검증",
    "71.16": "same-character residue analytic premise 이후 multiplier 52와 phase cancellation을 조건부 커널 검증",
    "71.17": "product conductor lcm<=q_j*q_k<=Q^2의 표준 유한 정수식; Lean 형식화 대기",
    "71.18": "두 q/phi(q)<=6L premise에서 normalized phase-pair factor<=36을 조건부 커널 검증",
    "71.19": "Theory 70 terminal coefficient의 averaged 재사용 정의",
    "71.20": "averaged generalized-Halasz analytic 합성은 미형식화; common L^2 cancellation만 부분형식화",
    "71.21": "positive common L^2를 나눈 normalized A,B,E 식을 analytic raw premise 아래 조건부 커널 검증",
    "71.22": "averaged detector·log gate·half-margin cutoff의 공통 maximum 정의",
    "71.23": "half-margin premise 아래 Theory 70 selected-system coefficient를 raw Q 손실 없이 조건부 커널 검증",
    "71.24": "q<=Q, Q,T>=1, D=Q^2*T에서 두 logarithmic upper bound를 커널 검증",
    "72.1": "Gallagher zero-density integral의 far/near alpha 구간 정의",
    "72.2": "Gallagher 식 (30)의 explicit-formula 평균 구조; 숨은 multiplier와 cutoff는 OPEN",
    "72.3": "Gallagher 식 (30)의 Stieltjes zero-density identity; analytic identity 전체는 미형식화",
    "72.4": "Bennett et al. Theorem 1.1 source statement; peer-reviewed analytic theorem은 Lean 미형식화",
    "72.5": "T=Q^5의 elementary logarithm envelope; Lean 순차 형식화 대기",
    "72.6": "Bennett source theorem에서 per-character coarse upper로 가는 analytic 합성",
    "72.7": "per-character와 character-count premise에서 family total-zero upper를 조건부 커널 검증",
    "72.8": "far integral 평가를 premise로 받은 endpoint X^-1 cancellation만 커널 검증",
    "72.9": "PAP X,Q,T와 common family scale D의 정의",
    "72.10": "total-zero와 real-power 정규화를 premise로 받은 far upper 합성을 조건부 커널 검증",
    "72.11": "theta=1/21,d=160의 far exponent와 coefficient를 exact 유리수로 커널 검증",
    "72.12": "y<=exp(y/2)를 통한 far budget cutoff; Lean 순차 형식화 대기",
    "72.13": "near integral의 L,C_J,kappa,lambda,A,B,eta,delta0 정의",
    "72.14": "두 exponential antiderivative를 premise로 받고 switch 항의 exact cancellation을 부분형식화",
    "72.15": "theta=1/21,d=160의 kappa=22와 lambda=69/80을 커널 검증",
    "72.16": "near certificate의 asymptotic limit; calculus와 고정밀 진단은 Lean 미형식화",
    "73.1": "selected-system coefficient 정의; 여섯 factor의 generic identity는 식 73.2와 함께 커널 검증",
    "73.2": "nonzero theta premises 아래 여섯 loss factor와 baseline coefficient의 exact 항등식을 커널 검증",
    "73.3": "theta=1/21의 detector와 baseline coefficient exact 정수 산술을 커널 검증",
    "73.4": "tightened exact rational composition은 커널 검증; decimal과 analytic factor premises는 별도",
    "73.5": "baseline/tightened exact 개선비는 커널 검증; decimal은 비구간 진단",
    "73.6": "exp(-2) PAP budget에서 얻은 120-dps coefficient cap; directed interval certificate 아님",
    "73.7": "tightened coefficient의 PAP budget 초과비 120-dps 진단; exact source ledger로 재계산",
    "T73-U001": "Lemma 7 denominator weight 정의 전사",
    "73.8": "M,N 단조 transfer는 문서 proof; reduced exponential quotient는 식 73.10과 함께 커널 검증",
    "73.9": "문서의 derivative proof 대신 더 짧은 exp order proof로 식 73.10 결론을 커널 검증",
    "73.10": "rho>=4, t>=1/rho에서 full quotient<8/5를 커널 검증; displayed limit identity 자체는 부분형식화",
    "73.11": "Ramaré--Zuniga coefficient의 endpoint exact rational은 커널 검증; source analytic theorem은 미형식화",
    "73.12": "Theory 66 source parameter에서 나온 finite log-ratio identity; 이번 Lean batch에서는 미형식화",
    "73.13": "L>=441에서 log(L)/L antitonicity와 exp(8)>441을 이용한 strict rational upper를 커널 검증",
    "73.14": "source weighted inequality는 미형식화; endpoint rational multiplication은 커널 검증",
    "73.15": "denominator 8/5와 weighted endpoint rational의 exact preterminal 합성을 커널 검증",
    "73.16": "height-row coefficient 정의 전사",
    "73.17": "0<=theta<=1/21의 row monotonic upper와 endpoint exact rational을 커널 검증",
    "73.18": "q<=Q, L=log(Q^2T)>0의 averaged log-ratio<=1/2를 커널 검증",
    "73.19": "Theory 69 Rankin Euler-product 계산의 sharpened analytic 합성; Lean 독립 proof는 없음",
    "73.20": "Mathlib six-term exp remainder로 e^(23/42)*(442/441)<7/4를 커널 검증",
    "T73-U002": "six-term exponential upper의 rational 계산은 73.20 proof 내부에서 커널 검증",
    "T73-U003": "7/4와 rational upper의 exact positive slack은 73.20 proof 내부에서 커널 검증",
    "73.21": "7/4와 exact height row의 residue rational 합성을 커널 검증; Rankin premise는 식 73.19 경계",
    "73.22": "endpoint area rational equality는 커널 검증; A_int analytic lower identification은 선행 premise",
    "73.23": "E<=A/m과 normalized terminal premise에서 arbitrary strict absorption을 조건부 커널 검증",
    "73.24": "exponential remainder에서 E<=A/m으로 가는 symbolic cutoff; Lean 순차 형식화 대기",
    "73.25": "m=10^6 cutoff의 120-dps diagnostic; directed interval certificate 아님",
    "T73-U004": "normalized terminal inequality의 재사용 정의",
    "73.26": "d=186,c1=1/24,theta=1/21의 lambda와 두 exponent를 exact rational로 커널 검증",
    "73.27": "unit-C_J near kernel의 transcendental 120-dps 진단; directed interval certificate 아님",
    "73.28": "baseline/tightened near upper의 120-dps 진단; directed interval certificate 아님",
    "73.29": "theta=1/21의 theta^-6 exact integer를 커널 검증; proof-architecture 불가능성 정리는 아님",
    "74.1": "선별 후보 집합의 source-screen 결론; 문헌 전수 불가능성 명제가 아니며 Lean 형식화 대상 아님",
    "74.2": "현재 downstream pointwise PAP target 계약의 정의 전사",
    "74.3": "D=160 minimum C_PAP 100-dps 선행 진단; directed interval certificate 아님",
    "74.4": "Ramaré 2016 Theorem 1.1 source analytic statement; Lean 독립 proof 없음",
    "74.5": "Ramaré direct-insertion 변수 정규화 정의",
    "74.6": "main-term 일반 변환은 문서·Python 검산; d=186 rational exponent만 커널 검증",
    "74.7": "additive-term 일반 변환은 문서·Python 검산; d=186 rational exponent만 커널 검증",
    "74.8": "zero-free edge의 d=186,c1=1/24 exact mass만 커널 검증",
    "74.9": "Ramaré source RHS의 unit-slice main certificate 하한; 문서 직접 proof와 Python 범위검사",
    "74.10": "Ramaré additive certificate 하한; 문서 직접 proof와 Python 범위검사",
    "74.11": "d=186 Ramaré exponent margins와 zero-free edge mass exact rational 커널 검증",
    "74.12": "Ramaré printed source-range max의 100-dps 진단; directed interval certificate 아님",
    "74.13": "direct slice certificate의 100-dps 진단; 실제 prime error 하한이 아님",
    "74.14": "Thorner--Zaman explicit Bombieri source statements; analytic theorem은 Lean 미형식화",
    "74.15": "99,170,198의 d=186 integer capacity 비교를 커널 검증",
    "74.16": "Chen--Gupta--Li arXiv v2 asymptotic source statement; o(1)과 analytic proof 미형식화",
    "74.17": "Friedlander--Iwaniec Lemma 7.1 source sieve statement; analytic premise는 미형식화",
    "74.18": "80*18*52600과 coefficient comparison의 exact arithmetic을 커널 검증",
    "75.1": "세 transfer 후보의 좁은 feasibility 판정; analytic 불가능성 정리가 아니며 Lean 형식화 대상 아님",
    "75.2": "Maier--Gallagher actual PAP 변수와 family scale 정의 전사",
    "75.3": "first y-slice 정의 중 d=186,c1=1/24의 두 endpoint 산술을 부분 커널 검증",
    "75.4": "두 analytic upper premise가 주어졌을 때 pointwise min의 ordered-field 단조성을 조건부 커널 검증",
    "75.5": "Ramaré/Jutila first-slice lower는 문서·Python 검산; edge rational만 부분 형식화",
    "75.6": "Theory 73의 tightened exact coefficient kernel proof를 재사용",
    "75.7": "source 최소점에서의 두 transcendental lower 함수; Python 120-dps와 문서 미분 proof",
    "75.8": "finite d endpoint reduction의 elementary calculus; Lean 순차 형식화 대기",
    "75.9": "8602 decimal은 고정밀 diagnostic; endpoint와 coarse 1/8602<1/7만 커널 검증",
    "75.10": "exp(-2) 대비 required attenuation 120-dps diagnostic; directed interval certificate 아님",
    "75.11": "normalized nonnegative zero-frequency Mellin factor 정의",
    "75.12": "support와 positivity에서 오는 elementary integral bound; 문서 직접 proof, Lean 미형식화",
    "75.13": "zero-frequency support lower와 attenuation 비의 고정밀 diagnostic",
    "75.14": "support expansion 필요조건의 고정밀 diagnostic; original interval 보존 불가를 뜻함",
    "75.15": "signed weight Mellin continuity의 elementary integral inequality; 문서 직접 proof, Lean 미형식화",
    "75.16": "target attenuation에서 signed condition-number necessary lower; Lean 순차 형식화 대기",
    "75.17": "Gallagher 식 (30)의 positive zero-count integral 구조; source analytic identity 미형식화",
    "75.18": "pre-absolute-value residue-class zero contribution 정의",
    "75.19": "complex Cauchy와 second-moment를 explicit premise로 받은 terminal scale만 조건부 커널 검증",
    "76.1": "explicit 후보 실패와 aggregate moment open 경로의 source-screen 판정; 전역 불가능성 명제가 아님",
    "76.2": "residue-class von Mangoldt error 정의",
    "76.3": "현재 coefficient capacity와 near budget 정의",
    "76.4": "기존 pointwise PAP 목표 정의",
    "76.5": "Maier aggregate admissible-column error 목표 정의",
    "76.6": "Maier printed Lemma 2 적용과 최종 aggregate prime count; source analytic proof 미형식화",
    "76.7": "Akbary--Hambrook Theorem 1.2 source statement; Lean 미형식화",
    "76.8": "published RHS의 positive floor와 120-dps diagnostic; actual error 하한이 아님",
    "76.9": "Sedunova Theorem 1.2 source statement; Lean 미형식화",
    "76.10": "Sedunova source의 F(x,Q,Q1) 정의",
    "76.11": "Q1=1 direct certificate floor의 120-dps diagnostic; actual error 하한이 아님",
    "76.12": "Bennett et al. Theorem 1.1 pointwise source statement; Lean 미형식화",
    "76.13": "Bennett large-q source constants와 cutoff; Lean 미형식화",
    "76.14": "Y=q^d cutoff normalization은 문서 대수와 Python 검산; transcendental source range 미형식화",
    "76.15": "normalized cutoff와 sqrt/log lower premises에서 d<=186 모순을 조건부 커널 검증",
    "76.16": "first large-q boundary와 primorial checkpoint의 120-dps cutoff diagnostic",
    "76.17": "Bennett error를 PAP relative scale로 옮긴 elementary normalization; Python 검산",
    "76.18": "q=510510,d=186 checkpoint의 120-dps diagnostic; directed interval certificate 아님",
    "76.19": "character explicit-formula residue error 표현 정의",
    "76.20": "admissible residue aggregate character identity; character theory 전체 미형식화",
    "76.21": "finite character orthogonality source theorem; Lean 미형식화",
    "76.22": "aggregate Cauchy premise를 받은 scalar terminal implication을 조건부 커널 검증",
    "76.23": "M-times second-moment budget에서 aggregate error 목표로의 종단 합성을 조건부 커널 검증",
    "76.24": "필요한 hypothetical individual-primorial natural-order variance theorem; 현재 source 없음",
    "76.25": "hypothetical variance에서 필요한 scale condition으로의 대수; analytic premise 미확보",
    "77.1": "restricted-residue variance source-screen 결론; 전역 불가능성 명제가 아님",
    "77.2": "Maier printed matrix 정의 전사",
    "77.3": "Maier admissible residue 집합 정의 전사",
    "77.4": "Maier p.267 formula (I) source lower bound; Lean 독립 proof 없음",
    "77.5": "Maier p.267 formula (II) source pair upper bound; R10에서 별도 명시화 필요",
    "77.6": "admissible-set character coefficient 정의",
    "77.7": "finite character orthogonality source theorem; Lean 미형식화",
    "77.8": "principal-character coefficient M의 finite character fact; Lean 미형식화",
    "77.9": "total과 principal energy에서 nonprincipal energy를 빼는 실수대수만 커널 검증",
    "77.10": "Theory 76 character explicit-formula normalization 재사용 정의",
    "77.11": "principal relative-error 입력 계약 정의",
    "77.12": "nonprincipal Cauchy premise 이후 scalar terminal 합성을 조건부 커널 검증",
    "77.13": "principal-separated moment budget에서 weighted target으로의 합성을 조건부 커널 검증",
    "77.14": "두 충분 budget의 exact ratio; Python exact/high-precision 검산",
    "77.15": "Cauchy equality를 만드는 abstract aligned error-vector 정의",
    "77.16": "alignment equality의 scalar 항등식만 커널 검증; actual prime-error alignment 주장이 아님",
    "77.17": "Fiorilli--Martin source implication은 미형식화; d=21,186 endpoint 대입만 커널 검증",
    "77.18": "현재 필요한 direct weighted-correlation analytic target 정의",
    "77.19": "Dirichlet character의 nonunit zero convention에서 오는 shifted-sum identity; Lean 미형식화",
    "77.20": "Maier U 정의와 q^(o(1)) scale; analytic asymptotic 미형식화",
    "78.1": "Maier Lemma 6의 fixed congruence pair 원문 전사",
    "78.2": "fixed pairwise-coprime partition에서 CRT residue가 하나라는 source/direct 수론 사실; Lean 미형식화",
    "78.3": "Sono/FMT sieve residue vector 정의",
    "78.4": "Maier prime-product 삼분할 정의",
    "78.5": "Sono/FMT survivor set 정의 전사",
    "78.6": "각 sieve vector가 정하는 CRT m congruence 정의 전사",
    "78.7": "동일 construction family 위 세 bad set 정의",
    "78.8": "세 bad-set cardinality 합이 family보다 작다는 finite selection premise",
    "78.9": "finite union bound로 simultaneous good candidate 존재를 커널 검증",
    "78.10": "finite Markov count 식은 exact Python 검산; analytic badness 합은 입력",
    "78.11": "singleton family의 strict bad-count budget이 세 count 0을 강제함을 커널 검증",
    "78.12": "Sono/FMT vector별 direct weighted-correlation 목표 정의",
    "78.13": "vector-dependent character coefficient 정의; analytic 상계는 OPEN",
    "62.1": "Jutila 식 (2.11)의 source Mellin identity; complex analytic theorem은 Lean 미형식화",
    "62.2": "우측 contour line 선택; residue·수평변 complex analysis는 Lean 미형식화",
    "62.3": "actual M bound의 두 local 실수부등식만 커널 검증; 전체 character polynomial은 미형식화",
    "62.4": "n/phi(n) 합과 Euler-product multiplier 3은 문서·exact Python 검산; Lean 부분형식화",
    "62.5": "4/sqrt(6) 보정의 제곱 유리값만 커널 검증; primitive 유도식은 미형식화",
    "62.6": "Bennett et al. Lemma 5.6 (5.3)의 Rademacher convexity source theorem",
    "62.7": "vertical L bound 중 real triangle budget만 커널 검증",
    "62.8": "Gamma recurrence·integral에서 얻는 pointwise source/direct-proof bound",
    "62.9": "Gamma 적분 split의 유한 계수 합성만 커널 검증",
    "62.10": "직접 Mellin 상수 합성은 문서·100-dps Python 검산; full complex integral 미형식화",
    "62.11": "delta_epsilon 정의와 0<delta<1/4를 커널 검증",
    "62.12": "alpha>=1/2, beta>=alpha에서 exponent <=-epsilon/2를 커널 검증",
    "62.13": "source power condition에서 최종 real-power transfer; exponent만 커널 검증",
    "T63-U001": "Jutila의 finite cut 정의",
    "T63-U002": "actual D,R,X parameter 전사",
    "63.10": "actual tail 결론 중 exponent 합만 커널 검증; coefficient·무한합은 문서 직접 proof",
    "63.11": "0<eta<=4와 epsilon>0에서 max/sqrt cutoff의 tail-budget transfer 커널 검증",
    "63.1": "Jutila 식 (2.11)에서 분리한 tail 정의",
    "63.2": "divisor pairing과 actual pseudocharacter 점별 상계; 문서 proof·작은 Python 검산",
    "63.3": "beta>=1/2와 유한 r-count의 analytic 합성; Lean 순차 형식화 대기",
    "63.4": "첫 생략 정수 floor(x)+1의 geometric tail identity; Lean 순차 형식화 대기",
    "63.5": "exp(u)-1>=u에서 얻는 reciprocal bound를 커널 검증",
    "63.6": "reciprocal bound와 X+1<=2X는 커널 검증; 앞선 coefficient·tail 합성은 부분형식화",
    "63.7": "general upper-envelope 조건 정의",
    "63.8": "R,X upper envelope 이후 actual exponential bound; 문서·Python 검산",
    "63.9": "linear/quadratic cutoff에서 exponential budget으로 가는 실수대수 커널 검증",
    "63.12": "Jutila 인쇄 p.52 actual parameter 전사",
    "63.13": "actual exponent epsilon+(1+12epsilon)=1+13epsilon 커널 검증",
    "64.1": "Jutila 인쇄 p.52 actual parameter와 theta 범위 전사",
    "64.2": "네 positive loss 합과 source loss 사이 budget 정의",
    "64.3": "source analytic component를 premise로 받은 네 loss 종단 합성과 source coefficient 회복을 커널 검증",
    "64.4": "Jutila 식 (2.11)의 source detector identity; complex/Dirichlet identity 자체는 미형식화",
    "64.5": "source identity 이후 triangle 방향을 premise로 받은 종단 합성만 커널 검증",
    "64.6": "C_phi 정규화 정의",
    "64.7": "Zuniga Alterman source error와 Euler-product bridge 이후 lower transfer; analytic source는 미형식화",
    "64.8": "두 multiplicative loss가 additive sum 이하임을 커널 검증",
    "64.9": "Mellin·tail relative budget 목표 정의",
    "64.10": "actual A=D^(1+9theta) parameter 전사",
    "64.11": "0<=theta<=1/21의 exact exponent margin을 커널 검증",
    "64.12": "원래 log 조건의 square-root transfer; 문서 proof·Python 범위검사",
    "64.13": "Rosser--Schoenfeld Theorem 15과 small-q exact check의 source-backed 합성; source theorem 미형식화",
    "64.14": "64.13에서 C_phi inverse로 가는 대수는 문서 합성; source theorem 미형식화",
    "64.15": "Zuniga Alterman B_q 정의 전사",
    "64.16": "소인수 순서와 elementary integral bound의 직접 proof; Lean 순차 형식화 대기",
    "64.17": "finite Euler-product envelope의 직접 proof; Lean 순차 형식화 대기",
    "64.18": "root cutoff 전체는 미형식화; terminal exponent absorption만 커널 검증",
    "64.19": "B exponent premise 이후 negative exponent 흡수를 커널 검증",
    "64.20": "여덟 component sufficient cutoff 정의; exp/log implication은 문서·Python 검산",
    "64.21": "delta와 Mellin multiplier 정의 전사",
    "64.22": "theta=1/100 equal-split high-precision diagnostic; directed interval certificate 아님",
    "64.23": "theta=1/100 sufficient cutoff high-precision diagnostic; 최소 threshold 아님",
    "27.9": "원문 display 종료기호 누락; hash 보존",
    "27.10": "원문 display 종료기호 누락; hash 보존",
    "27.11": "원문 display 종료기호 누락; hash 보존",
    "27.12": "원문 display 종료기호 누락; hash 보존",
    "27.13": "원문 display 종료기호 누락; hash 보존",
}


def preview(latex: str, limit: int = 220) -> str:
    compact = " ".join(latex.split())
    if len(compact) > limit:
        compact = compact[: limit - 1] + "…"
    return html.escape(compact, quote=False).replace("|", "&#124;")


def doc_link(source_file: str) -> str:
    name = Path(source_file).name
    return f"[{name}](../{source_file})"


def build_ledger(inventory: dict[str, object], status_doc: dict[str, object]) -> str:
    status_by_id = {entry["formula_id"]: entry for entry in status_doc["formulae"]}
    default_status = status_doc["default_status"]
    formulae = inventory["formulae"]
    counts = Counter(
        status_by_id.get(item["formula_id"], {}).get("status", default_status)
        for item in formulae
    )
    reviewed_by_theory = Counter(
        item["theory"]
        for item in formulae
        if status_by_id.get(item["formula_id"], {}).get("status", default_status)
        != default_status
    )

    lines = [
        "# FGKMT-Sono Lean 전수 수식·정리 검증 원장",
        "",
        "- 생성 기준: 2026-09-14 KST",
        f"- inventory schema: `{inventory['schema_version']}`",
        f"- 원문 범위: `docs/method/theory/*.md` {inventory['theory_count']}개",
        f"- 전수 단위: Markdown fenced code 밖 display math {inventory['formula_count']:,}개",
        (
            f"- 원래 식번호: {inventory['tagged_formula_count']:,}개, 합성 ID 무번호식: "
            f"{inventory['untagged_formula_count']:,}개"
        ),
        f"- 안전 복구 표시: hash-pinned Theory 27의 누락 display 종료기호 {len(inventory['recoveries'])}개",
        "- 기계 정본: [formula_inventory_v1.json](verification/formula_inventory_v1.json)",
        "- 상태 정본: [verification_status_v1.json](verification/verification_status_v1.json)",
        "- Lean 정본: [TheoryVerification.lean](FGKMTSono/TheoryVerification.lean)",
        "- 현재 결론: 초기 dependency-critical batch만 형식화했다. 전체 Sono/FMT analytic theorem 또는",
        "  수치 `X_cert`가 Lean으로 증명됐다는 뜻이 아니다.",
        "",
        "## 1. 목적과 범위",
        "",
        "이 원장은 수식을 빠짐없이 식별하는 **전수 inventory**와 Lean이 실제 검사한 증거 수준을",
        "분리한다. inline math는 문장 안의 기호·매개변수 설명이므로 개별 proof obligation으로 세지",
        "않고, 모든 display math를 하나의 안정 항목으로 등록했다. 원래 `\\tag{...}`가 없는 display",
        "수식에는 `T<theory>-U<ordinal>` 합성 ID를 부여했다.",
        "",
        "원문 수식 자체는 각 source line과 SHA-256으로 고정한다. 표의 수식은 탐색용 preview이며,",
        "줄임 없는 LaTeX는 JSON inventory와 원문에 있다.",
        "",
        "## 2. 증거 수준",
        "",
        "| 상태 | 정확한 의미 |",
        "|---|---|",
    ]
    for status, meaning in STATUS_MEANING.items():
        lines.append(f"| `{status}` | {meaning} |")
    lines.extend(
        [
            "",
            "현재 `KERNEL_PASS`도 Lean/Mathlib의 표준 논리 기반 위의 검증이다. 외부 논문 명제를",
            "매개변수로 받은 정리는 반드시 `CONDITIONAL_KERNEL_PASS`로 낮춰 표시한다.",
            "",
            "## 3. 고정된 설치·dependency",
            "",
            "| 구성요소 | 고정값 | 검증 |",
            "|---|---|---|",
            "| Elan | 4.2.4, commit `227caca13` | 관측 |",
            "| Lean | `leanprover/lean4:v4.34.0-rc2` | `lean-toolchain` |",
            "| Lean kernel | `6a10ac8c22beadecabdbb0919c2b50214762f91d` | `lake env lean --version` |",
            "| Mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` | lakefile·manifest·local HEAD 3중 일치 |",
            "| transitive dependencies | `lake-manifest.json`의 full commit | manifest lock |",
            "",
            "## 4. 영향도와 검증 한계",
            "",
            "| 축 | 판정 |",
            "|---|---|",
            "| 반복로그·end-bounded 정의 | 정의를 Lean에 분리해 base-log 및 start/end 혼동을 방지 |",
            "| 유한 대수·floor·ceil·집합 논리 | Lean 독립 검증의 우선 대상 |",
            "| 적분·소수분포·sieve·hypergraph source theorem | Mathlib에 drop-in proof가 없으면 장기 source 형식화가 필요 |",
            "| 수치 근사 | exact rational theorem과 분리; decimal 출력만으로 PASS 금지 |",
            "| `X_cert` | DEP-R09–R12가 OPEN이므로 계속 OPEN |",
            "| actual experiment | 이번 원장은 새 prime 계산이나 `test_result`를 만들지 않음 |",
            "",
            "## 5. 현재 상태 집계",
            "",
            "| 상태 | 항목 수 |",
            "|---|---:|",
        ]
    )
    for status in STATUS_MEANING:
        lines.append(f"| `{status}` | {counts.get(status, 0):,} |")
    lines.extend(
        [
            "",
            "집계는 display 수식 행 기준이다. 하나의 Lean theorem이 여러 display 식의 합성을 검증하거나,",
            "한 display 식이 여러 Lean 선언으로 나뉠 수 있다.",
            "",
            "## 6. theory별 전수 현황",
            "",
            "| Theory | 원문 | SHA-256 | display | tagged | untagged | 현재 형식화·review 행 |",
            "|---:|---|---|---:|---:|---:|---:|",
        ]
    )
    for theory in inventory["theories"]:
        lines.append(
            f"| {theory['theory']} | {doc_link(theory['source_file'])} | "
            f"`{theory['source_sha256'][:16]}…` | {theory['display_formula_count']:,} | "
            f"{theory['tagged_formula_count']:,} | {theory['untagged_formula_count']:,} | "
            f"{reviewed_by_theory[theory['theory']]:,} |"
        )
    lines.extend(
        [
            "",
            "## 7. 추가 Lean 정리(문단 논증)",
            "",
            "| 원문 | Lean 선언 | 상태 | 범위 |",
            "|---|---|---|---|",
        ]
    )
    supplemental_scope = {
        "sequential_positive_probability_choice": "독립성이나 두 실패율 합 조건이 불필요하다는 순수 논리",
    }
    for item in status_doc.get("supplemental_theorems", []):
        declarations = "; ".join(f"`{name}`" for name in item["declarations"])
        scope = "; ".join(supplemental_scope.get(name, "보조 exact 정리") for name in item["declarations"])
        lines.append(f"| {item['source']} | {declarations} | `{item['status']}` | {scope} |")
    lines.extend(
        [
            "",
            "## 8. 수식별 전수 검증 표",
            "",
            "| # | 수식 ID | Theory·원문 | line | 수식 preview | Lean 선언 | 상태 | 한계·근거 |",
            "|---:|---|---|---:|---|---|---|---|",
        ]
    )
    for ordinal, item in enumerate(formulae, start=1):
        entry = status_by_id.get(item["formula_id"], {})
        status = entry.get("status", default_status)
        declarations = entry.get("declarations", [])
        declaration_text = "; ".join(declarations) if declarations else "—"
        if declarations:
            declaration_text = f"`{declaration_text}`"
        note = NOTES_BY_ID.get(
            item["formula_id"],
            "순차 형식화 대기" if status == default_status else STATUS_MEANING[status],
        )
        line_range = (
            str(item["start_line"])
            if item["start_line"] == item["end_line"]
            else f"{item['start_line']}–{item['end_line']}"
        )
        lines.append(
            f"| {ordinal} | `{item['formula_id']}` | T{item['theory']} "
            f"{doc_link(item['source_file'])} | {line_range} | "
            f"<code>{preview(item['latex'])}</code> | {declaration_text} | `{status}` | {note} |"
        )
    lines.extend(
        [
            "",
            "## 9. 발견된 원문·작업 오류",
            "",
            "1. hash-pinned Theory 27 식 (27.9)–(27.13)에 display 종료 `\\]` 5개가 빠져 있다.",
            "   원문 SHA 계약을 보존하기 위해 소급 변경하지 않고 inventory에서만 안전 분리했으며",
            "   다섯 행을 `PARSE_REVIEW_REQUIRED`로 남겼다.",
            "2. Theory 01 plateau 식의 `qquad` 앞 backslash 누락을 확인해 `\\qquad`로 교정했다.",
            "3. 단일 Lean target을 import한 뒤 target 생성 전에 최초 build를 시작해 한 차례",
            "   `no such file ... TheoryVerification.lean`이 발생했다. 작업 순서 오류로 기록하고",
            "   target 생성 뒤 직접 kernel 검사와 전체 build를 다시 수행한다.",
            "",
            "## 10. 순차 형식화 우선순위",
            "",
            "1. 초기 batch의 declaration–원장 연결과 no-sorry 검증을 고정한다.",
            "2. 현재 root DEP-R09의 exact source 진술과 finite-rate 의무를 먼저 고정한다.",
            "3. DEP-R09에서 실제 사용할 상수·부등식·endpoint 합성을 사용 전에 형식화한다.",
            "4. 이후 DEP-R10, R11, R12를 같은 source-first·역의존 순서로 처리한다.",
            "5. Theory 55의 잔여 source theorem과 Theories 10–11의 별도 finite-set 구조는",
            "   해당 DAG에서 다시 필요해질 때 독립 batch로 처리한다.",
            "6. 960개라는 총개수를 선행 gate로 쓰지 않는다. empirical·역사적·대체 식은 root-critical 식 뒤로 미룬다.",
            "7. source analytic theorem은 먼저 Mathlib/선행 형식화를 찾고, 없으면",
            "   `SOURCE_THEOREM_UNFORMALIZED`로 차단한 뒤 별도 장기 증명 단위로 분해한다.",
            "8. DEP-R09–R12와 end-to-end composition이 닫힌 뒤 비임계 잔여 coverage를 순차 처리한다.",
            "",
            "새 theory가 추가되면 inventory와 원장을 재생성하고 기존 source SHA가 움직였는지 먼저 검사한다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    lean_root = repo_root / "lean"
    inventory = build_inventory(repo_root)
    if inventory["issues"]:
        raise ValueError(f"cannot generate from parse issues: {inventory['issues']}")
    status_path = lean_root / "verification" / "verification_status_v1.json"
    status_doc = json.loads(status_path.read_text(encoding="utf-8"))
    inventory_path = lean_root / "verification" / "formula_inventory_v1.json"
    ledger_path = lean_root / "VERIFICATION_LEDGER.md"
    inventory_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    ledger_path.write_text(
        build_ledger(inventory, status_doc),
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "GENERATED",
                "theory_count": inventory["theory_count"],
                "formula_count": inventory["formula_count"],
                "recoveries": len(inventory["recoveries"]),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
