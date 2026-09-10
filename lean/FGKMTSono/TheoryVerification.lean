import Mathlib

/-!
# FGKMT-Sono theory verification

All project theory statements are formalized in this single file.  Each section
names the source Markdown theory and equation identifier.  A theorem whose
premises contain a source result verifies only the downstream implication; it
does not certify that analytic source premise.

The checked-in ledger at `../VERIFICATION_LEDGER.md` is the status authority.
No project-local axiom, `sorry`, or `admit` is permitted.
-/

set_option linter.style.header false

namespace FGKMTSono

/-! ## Theory 01 — FGKMT/Sono normalization and end-bounded boundary -/

/- Theory 01, formula T01-U001: `log_k` means k-fold natural logarithm. -/
noncomputable def iterLog : ℕ → ℝ → ℝ
  | 0, x => x
  | n + 1, x => Real.log (iterLog n x)

@[simp] theorem iterLog_zero (x : ℝ) : iterLog 0 x = x := rfl

theorem iterLog_one (x : ℝ) : iterLog 1 x = Real.log x := rfl

theorem iterLog_two (x : ℝ) : iterLog 2 x = Real.log (Real.log x) := rfl

theorem iterLog_three (x : ℝ) :
    iterLog 3 x = Real.log (Real.log (Real.log x)) := rfl

theorem iterLog_four (x : ℝ) :
    iterLog 4 x = Real.log (Real.log (Real.log (Real.log x))) := rfl

/- Theory 01, formula T01-U001: the canonical FGKMT/Sono scale. -/
noncomputable def fgkmtScale (x : ℝ) : ℝ :=
  iterLog 1 x * iterLog 2 x * iterLog 4 x / iterLog 3 x

theorem fgkmtScale_unfold (x : ℝ) :
    fgkmtScale x =
      Real.log x * Real.log (Real.log x) *
        Real.log (Real.log (Real.log (Real.log x))) /
          Real.log (Real.log (Real.log x)) := rfl

/- Theory 01, formula T01-U001: a continuous lower boundary above which all
   nested-log factors used by the scale are in their intended positive domain. -/
noncomputable def scaleThreshold : ℝ := Real.exp (Real.exp (Real.exp 1))

/- Auxiliary theorem for Theory 01: `exp(t) / t` is strictly increasing for
   `t ≥ 1`.  The proof uses Mathlib's strict exponential lower bound and ordered-field
   algebra, not an analytic assumption or project-local axiom. -/
theorem exp_div_self_strictMonoOn :
    StrictMonoOn (fun t : ℝ ↦ Real.exp t / t) (Set.Ici 1) := by
  intro a ha b hb hab
  have ha0 : 0 < a := zero_lt_one.trans_le ha
  have hb0 : 0 < b := ha0.trans hab
  have hd : 0 < b - a := sub_pos.mpr hab
  have hd_nonneg : 0 ≤ b - a := hd.le
  have hscale : 0 ≤ (a - 1) * (b - a) :=
    mul_nonneg (sub_nonneg.mpr ha) hd_nonneg
  have hexp : (b - a) + 1 < Real.exp (b - a) :=
    Real.add_one_lt_exp hd.ne'
  have hba : b < a * Real.exp (b - a) := by
    have hmul := mul_lt_mul_of_pos_left hexp ha0
    nlinarith
  apply (div_lt_div_iff₀ ha0 hb0).2
  have hmul := mul_lt_mul_of_pos_left hba (Real.exp_pos a)
  calc
    Real.exp a * b < Real.exp a * (a * Real.exp (b - a)) := hmul
    _ = (Real.exp a * Real.exp (b - a)) * a := by ring
    _ = Real.exp (a + (b - a)) * a := by rw [Real.exp_add]
    _ = Real.exp b * a := by ring_nf

/- Theory 01, formula T01-U001: positivity of the successive iterated logs on
   the continuous project domain. -/
theorem scale_domain_chain {x : ℝ} (hx : scaleThreshold < x) :
    0 < x ∧
      0 < iterLog 1 x ∧
      0 < iterLog 2 x ∧
      1 < iterLog 3 x ∧
      0 < iterLog 4 x := by
  have ht0 : 0 < scaleThreshold := Real.exp_pos _
  have hx0 : 0 < x := ht0.trans hx
  have h1 : Real.exp (Real.exp 1) < Real.log x := by
    apply (Real.lt_log_iff_exp_lt hx0).2
    simpa [scaleThreshold]
  have h1pos : 0 < Real.log x := (Real.exp_pos _).trans h1
  have h2 : Real.exp 1 < Real.log (Real.log x) := by
    apply (Real.lt_log_iff_exp_lt h1pos).2
    simpa using h1
  have h2pos : 0 < Real.log (Real.log x) := (Real.exp_pos _).trans h2
  have h3 : 1 < Real.log (Real.log (Real.log x)) := by
    apply (Real.lt_log_iff_exp_lt h2pos).2
    simpa using h2
  have h4 : 0 < Real.log (Real.log (Real.log (Real.log x))) :=
    Real.log_pos h3
  simpa [iterLog_one, iterLog_two, iterLog_three, iterLog_four] using
    ⟨hx0, h1pos, h2pos, h3, h4⟩

/- Theory 01, formula T01-U001: positive-factor representation used for the
   monotonicity proof. -/
theorem fgkmtScale_factorization {x : ℝ} (hx : scaleThreshold < x) :
    fgkmtScale x =
      iterLog 1 x * (Real.exp (iterLog 3 x) / iterLog 3 x) *
        Real.log (iterLog 3 x) := by
  have hchain := scale_domain_chain hx
  have hexp : Real.exp (iterLog 3 x) = iterLog 2 x := by
    rw [iterLog_three, iterLog_two]
    exact Real.exp_log hchain.2.2.1
  unfold fgkmtScale
  change
    iterLog 1 x * iterLog 2 x * Real.log (iterLog 3 x) / iterLog 3 x = _
  rw [← hexp]
  ring

/- Theory 01, formula T01-U001: strict order propagation through the first four
   iterated natural logarithms. -/
theorem iterLog_strictMono_up_to_four {x y : ℝ}
    (hx : scaleThreshold < x) (hxy : x < y) :
    iterLog 1 x < iterLog 1 y ∧
      iterLog 2 x < iterLog 2 y ∧
      iterLog 3 x < iterLog 3 y ∧
      iterLog 4 x < iterLog 4 y := by
  have hxchain := scale_domain_chain hx
  have h1 : Real.log x < Real.log y := Real.log_lt_log hxchain.1 hxy
  have h2 : Real.log (Real.log x) < Real.log (Real.log y) :=
    Real.log_lt_log hxchain.2.1 h1
  have h3 : Real.log (Real.log (Real.log x)) <
      Real.log (Real.log (Real.log y)) :=
    Real.log_lt_log hxchain.2.2.1 h2
  have h4 : Real.log (Real.log (Real.log (Real.log x))) <
      Real.log (Real.log (Real.log (Real.log y))) :=
    Real.log_lt_log (zero_lt_one.trans hxchain.2.2.2.1) h3
  simpa [iterLog_one, iterLog_two, iterLog_three, iterLog_four] using
    ⟨h1, h2, h3, h4⟩

/- Theory 01, formula T01-U001: positivity of the FGKMT/Sono scale on the
   continuous project domain. -/
theorem fgkmtScale_pos {x : ℝ} (hx : scaleThreshold < x) :
    0 < fgkmtScale x := by
  rw [fgkmtScale_factorization hx]
  have hchain := scale_domain_chain hx
  exact mul_pos
    (mul_pos hchain.2.1 (div_pos (Real.exp_pos _) (zero_lt_one.trans hchain.2.2.2.1)))
    (Real.log_pos hchain.2.2.2.1)

/- Theory 01, formulae T01-U001 and T01-U005: the FGKMT/Sono scale is strictly
   increasing above `exp(exp(exp(1)))`. -/
theorem fgkmtScale_strictMonoOn :
    StrictMonoOn fgkmtScale (Set.Ioi scaleThreshold) := by
  intro x hx y hy hxy
  have hlogs := iterLog_strictMono_up_to_four hx hxy
  have hxchain := scale_domain_chain hx
  have hychain := scale_domain_chain hy
  have hcquot :
      Real.exp (iterLog 3 x) / iterLog 3 x <
        Real.exp (iterLog 3 y) / iterLog 3 y :=
    exp_div_self_strictMonoOn hxchain.2.2.2.1.le hychain.2.2.2.1.le hlogs.2.2.1
  rw [fgkmtScale_factorization hx, fgkmtScale_factorization hy]
  calc
    iterLog 1 x * (Real.exp (iterLog 3 x) / iterLog 3 x) *
          Real.log (iterLog 3 x) <
        iterLog 1 y * (Real.exp (iterLog 3 x) / iterLog 3 x) *
          Real.log (iterLog 3 x) := by
      exact mul_lt_mul_of_pos_right
        (mul_lt_mul_of_pos_right hlogs.1
          (div_pos (Real.exp_pos _) (zero_lt_one.trans hxchain.2.2.2.1)))
        (Real.log_pos hxchain.2.2.2.1)
    _ < iterLog 1 y * (Real.exp (iterLog 3 y) / iterLog 3 y) *
          Real.log (iterLog 3 x) := by
      exact mul_lt_mul_of_pos_right
        (mul_lt_mul_of_pos_left hcquot hychain.2.1)
        (Real.log_pos hxchain.2.2.2.1)
    _ < iterLog 1 y * (Real.exp (iterLog 3 y) / iterLog 3 y) *
          Real.log (iterLog 3 y) := by
      exact mul_lt_mul_of_pos_left hlogs.2.2.2
        (mul_pos hychain.2.1
          (div_pos (Real.exp_pos _) (zero_lt_one.trans hychain.2.2.2.1)))

/- Theory 01, formulae T01-U002 and T01-U003: a gap becomes eligible at the
   end prime in the canonical function, not at its start prime. -/
structure PrimeGapDatum where
  startPrime : ℕ
  gap : ℕ
deriving DecidableEq

def PrimeGapDatum.endPrime (record : PrimeGapDatum) : ℕ :=
  record.startPrime + record.gap

def endBoundedMaxGap (records : Finset PrimeGapDatum) (x : ℕ) : ℕ :=
  records.sup fun record => if record.endPrime ≤ x then record.gap else 0

def startBoundedMaxGap (records : Finset PrimeGapDatum) (x : ℕ) : ℕ :=
  records.sup fun record => if record.startPrime ≤ x then record.gap else 0

def endEligible (endPrime x : ℕ) : Prop := endPrime ≤ x

def startEligible (startPrime x : ℕ) : Prop := startPrime ≤ x

theorem endEligible_at_endpoint (endPrime : ℕ) : endEligible endPrime endPrime := le_rfl

theorem endEligible_false_before {x endPrime : ℕ} (h : x < endPrime) :
    ¬ endEligible endPrime x := by
  exact Nat.not_le_of_lt h

/- Theory 01, formula T01-U004: integer end-bounded plateau. -/
def onEndBoundedPlateau (endPrime nextEnd x : ℕ) : Prop :=
  endPrime ≤ x ∧ x < nextEnd

theorem plateau_integer_upper {endPrime nextEnd x : ℕ}
    (h : onEndBoundedPlateau endPrime nextEnd x) : x ≤ nextEnd - 1 := by
  exact Nat.le_sub_one_of_lt h.2

/- Theory 01, formula T01-U005: the exact integer interval-minimum expression.
   Monotonicity of the scale is a separate analytic premise. -/
noncomputable def intervalMinimum (gap nextEnd : ℕ) : ℝ :=
  (gap : ℝ) / fgkmtScale ((nextEnd - 1 : ℕ) : ℝ)

/- Theory 01, formula T01-U005: on every positive-scale integer point in an
   end-bounded plateau, the right-end expression is no larger. -/
theorem intervalMinimum_is_minimum
    {gap endPrime nextEnd x : ℕ}
    (hplateau : onEndBoundedPlateau endPrime nextEnd x)
    (hx : scaleThreshold < (x : ℝ)) :
    intervalMinimum gap nextEnd ≤ (gap : ℝ) / fgkmtScale x := by
  have hupperNat : x ≤ nextEnd - 1 := plateau_integer_upper hplateau
  have hupper : (x : ℝ) ≤ ((nextEnd - 1 : ℕ) : ℝ) := by
    exact_mod_cast hupperNat
  have hend : scaleThreshold < ((nextEnd - 1 : ℕ) : ℝ) := hx.trans_le hupper
  have hscale : fgkmtScale x ≤ fgkmtScale ((nextEnd - 1 : ℕ) : ℝ) :=
    fgkmtScale_strictMonoOn.monotoneOn hx hend hupper
  unfold intervalMinimum
  apply (div_le_div_iff₀ (fgkmtScale_pos hend) (fgkmtScale_pos hx)).2
  exact mul_le_mul_of_nonneg_left hscale (Nat.cast_nonneg gap)

/-! ## Theory 07 — local `li - pi` identity and inequality direction -/

/- Theory 07, formulae T07-U001 and T07-U002. -/
theorem local_discrepancy_identity (li₀ li₁ pi₀ pi₁ : ℝ) :
    (li₁ - pi₁) - (li₀ - pi₀) = (li₁ - li₀) - (pi₁ - pi₀) := by
  ring

/- Theory 07, formulae T07-U003 and T07-U004: a lower bound on the discrepancy
   increment gives an upper, not lower, bound on the local prime count. -/
theorem local_count_upper_of_discrepancy_lower
    {deltaLi localCount q : ℝ}
    (h : -q ≤ deltaLi - localCount) :
    localCount ≤ deltaLi + q := by
  linarith

/- Theory 07, formula T07-U005: a non-strict real upper bound on an integer is
   rounded with floor. -/
theorem integer_upper_bound_uses_floor {n : ℤ} {R : ℝ}
    (h : (n : ℝ) ≤ R) : n ≤ ⌊R⌋ := by
  exact (Int.le_floor).2 h

/-! ## Theory 10 — coverage-preserving finite compression -/

/- Theory 10, formula T10-U001: abstract exact-primality form of the risk predicate. -/
def riskyStart (isPrime : ℕ → Prop) (nextPrime : ℕ → ℕ) (H p : ℕ) : Prop :=
  isPrime p ∧ H ≤ nextPrime p - p

/- Theory 10, formulae T10-U001 and T10-U002: candidate superset theorem. -/
theorem candidate_superset_eliminates
    {α : Type*} {U C : Set α} {Bad : α → Prop}
    (coverage : ∀ p, p ∈ U → Bad p → p ∈ C)
    (verified : ∀ c, c ∈ C → ¬ Bad c) :
    ∀ p, p ∈ U → ¬ Bad p := by
  intro p hpU hpBad
  exact verified p (coverage p hpU hpBad) hpBad

/- Theory 10, formulae T10-U003 and T10-U004: a sound witness family whose
   coverage is total eliminates every bad point. -/
theorem witness_family_eliminates
    {α ι : Type*} {U : Set α} {W : Set ι} {Cov : ι → Set α} {Bad : α → Prop}
    (coverage : ∀ c, c ∈ U → ∃ w, w ∈ W ∧ c ∈ Cov w)
    (sound : ∀ w, w ∈ W → ∀ c, c ∈ Cov w → ¬ Bad c) :
    ∀ c, c ∈ U → ¬ Bad c := by
  intro c hcU
  obtain ⟨w, hwW, hcCov⟩ := coverage c hcU
  exact sound w hwW c hcCov

/- Theory 10, formula T10-U005: the arithmetic content of a shared prime
   witness interval. -/
theorem shared_prime_witness_is_strict {c q H : ℕ}
    (hlower : q - H + 1 ≤ c) (hupper : c ≤ q - 1) (hH : H ≤ q) :
    c < q ∧ q < c + H := by
  constructor
  · omega
  · omega

/-! ## Theory 11 — exact modulus-lift inequality core -/

/- Theory 11, formulae T11-U001 and T11-U002: once potential differences are
   preserved, increasing a transition representative cannot hurt when λ ≥ 0. -/
theorem modulus_lift_transition_monotone
    {lambda mu phiR phiS sourceD targetD w : ℝ}
    (hlambda : 0 ≤ lambda)
    (hd : sourceD ≤ targetD)
    (hsource : w ≤ lambda * sourceD + mu + phiR - phiS) :
    w ≤ lambda * targetD + mu + phiR - phiS := by
  nlinarith [mul_le_mul_of_nonneg_left hd hlambda]

/-! ## Theory 55 — latest COV2 post-covering finite composition -/

/- Theory 55, formula 55.4: endpoint-safe equal-grid parameters. -/
noncomputable def equalGridJ (ε : ℝ) : ℕ := ⌈(2 : ℝ) / ε⌉₊

noncomputable def equalGridH (ε : ℝ) : ℝ := 1 / (equalGridJ ε : ℝ)

/- Theory 55, formula 55.5: the full ceil-derived width bounds. -/
theorem equalGrid_width_bounds {ε : ℝ} (hε : 0 < ε) (hεone : ε ≤ 1) :
    ε / (2 + ε) ≤ equalGridH ε ∧
      equalGridH ε ≤ ε / 2 ∧
      ε / 3 ≤ equalGridH ε := by
  have hratio_pos : 0 < (2 : ℝ) / ε := div_pos (by norm_num) hε
  have hJnat : 0 < equalGridJ ε := by
    simpa [equalGridJ] using (Nat.ceil_pos.2 hratio_pos)
  have hJpos : 0 < (equalGridJ ε : ℝ) := by exact_mod_cast hJnat
  have hJlower : (2 : ℝ) / ε ≤ (equalGridJ ε : ℝ) := by
    simpa [equalGridJ] using (Nat.le_ceil ((2 : ℝ) / ε))
  have hJupper : (equalGridJ ε : ℝ) < (2 : ℝ) / ε + 1 := by
    simpa [equalGridJ] using (Nat.ceil_lt_add_one hratio_pos.le)
  have hratio_eq : (2 : ℝ) / ε + 1 = (2 + ε) / ε := by
    field_simp [ne_of_gt hε]
  have hJupper' : (equalGridJ ε : ℝ) ≤ (2 + ε) / ε := by
    rw [hratio_eq] at hJupper
    exact hJupper.le
  have hlower : ε / (2 + ε) ≤ equalGridH ε := by
    have hrecip := one_div_le_one_div_of_le hJpos hJupper'
    have hrewrite : ε / (2 + ε) = 1 / ((2 + ε) / ε) := by
      field_simp [ne_of_gt hε, ne_of_gt (by linarith : 0 < 2 + ε)]
    calc
      ε / (2 + ε) = 1 / ((2 + ε) / ε) := hrewrite
      _ ≤ 1 / (equalGridJ ε : ℝ) := hrecip
      _ = equalGridH ε := rfl
  have hupper : equalGridH ε ≤ ε / 2 := by
    have hrecip := one_div_le_one_div_of_le hratio_pos hJlower
    have hrewrite : 1 / ((2 : ℝ) / ε) = ε / 2 := by
      field_simp [ne_of_gt hε]
    calc
      equalGridH ε = 1 / (equalGridJ ε : ℝ) := rfl
      _ ≤ 1 / ((2 : ℝ) / ε) := hrecip
      _ = ε / 2 := hrewrite
  have heps_three : ε / 3 ≤ ε / (2 + ε) := by
    rw [div_le_div_iff₀ (by norm_num : (0 : ℝ) < 3) (by linarith : 0 < 2 + ε)]
    nlinarith
  exact ⟨hlower, hupper, heps_three.trans hlower⟩

/- Theory 55, formula 55.6: scalar part after the grid-union length premise. -/
theorem grid_cover_length_budget {width h ε : ℝ}
    (hwidth : 0 ≤ width) (hcell : 2 * h ≤ ε) :
    width + 2 * h ≤ width + ε ∧ width + ε ≤ 2 * width + ε := by
  constructor <;> linarith

/- Theory 55, formulae 55.8--55.10: algebraic rescaling once the floor-log
   window `p ≤ R < 5p` has been established. -/
theorem floor_log_rescaling_window
    {A R p Aprime : ℝ}
    (hA : 0 < A) (hp : 0 < p)
    (hwindowLower : p ≤ R) (hwindowUpper : R < 5 * p)
    (hAprime : Aprime = A * (R / p)) :
    A ≤ Aprime ∧ Aprime < 5 * A := by
  have hratioLower : 1 ≤ R / p := (le_div_iff₀ hp).2 (by simpa using hwindowLower)
  have hratioUpper : R / p < 5 := (div_lt_iff₀ hp).2 (by simpa using hwindowUpper)
  rw [hAprime]
  constructor
  · nlinarith [mul_le_mul_of_nonneg_left hratioLower hA.le]
  · nlinarith [mul_lt_mul_of_pos_left hratioUpper hA]

/- Theory 55, formula 55.13: the explicit exception-restoration constant. -/
theorem exception_restoration_bound
    {r0 A h b ε e : ℝ}
    (hr0small : r0 < 1 / 100)
    (hA : 0 < A) (hb : 0 < b) (hε : 0 < ε)
    (hh : ε / 3 ≤ h)
    (he : e ≤ 2 / ((1 - r0) * A * h * b)) :
    e < 7 / (A * ε * b) := by
  have hone : 99 / 100 < (1 - r0 : ℝ) := by linarith
  have hhpos : 0 < h := lt_of_lt_of_le (div_pos hε (by norm_num)) hh
  have hprod : (99 / 100 : ℝ) * (ε / 3) < (1 - r0) * h := by
    exact mul_lt_mul hone hh (by positivity) (by positivity)
  have hcore : 2 * ε < 7 * ((1 - r0) * h) := by
    nlinarith
  have hAb : 0 < A * b := mul_pos hA hb
  have hcross := mul_lt_mul_of_pos_right hcore hAb
  have hdenLeft : 0 < (1 - r0) * A * h * b := by positivity
  have hdenRight : 0 < A * ε * b := by positivity
  have hfrac : 2 / ((1 - r0) * A * h * b) < 7 / (A * ε * b) := by
    rw [div_lt_div_iff₀ hdenLeft hdenRight]
    nlinarith [hcross]
  exact he.trans_lt hfrac

/- Theory 55, formulae 55.14--55.16: relative-error composition. -/
theorem relative_error_budget
    {r0 t estar η : ℝ}
    (hr0 : 0 ≤ r0) (hetastar : 0 ≤ estar) (hη : 0 < η) (hηquarter : η ≤ 1 / 4)
    (hr0max : r0 ≤ η / 8) (ht : t = η / 8) (hestar : estar ≤ η / 8) :
    r0 + (1 + r0) * (t + estar) ≤ (49 / 128) * η ∧
      (49 / 128) * η < η := by
  have hsum_nonneg : 0 ≤ t + estar := by rw [ht]; positivity
  have hsum : t + estar ≤ η / 4 := by rw [ht]; linarith
  have hfactor : 0 ≤ 1 + r0 := by linarith
  have hfactorUpper : 1 + r0 ≤ 1 + η / 8 := by linarith
  have hfactorUpperNonneg : 0 ≤ 1 + η / 8 := by positivity
  have hprod : (1 + r0) * (t + estar) ≤ (1 + η / 8) * (η / 4) :=
    mul_le_mul hfactorUpper hsum hsum_nonneg hfactorUpperNonneg
  have hηsq : η * η ≤ η / 4 := by nlinarith
  constructor
  · nlinarith
  · nlinarith

/- Theory 55, formulae 55.17--55.21: sequential existence does not require
   independence or a sum of the two failure bounds. -/
theorem sequential_positive_probability_choice
    {Outer Inner : Type*} {outerGood : Outer → Prop} {innerGood : Outer → Inner → Prop}
    (hOuter : ∃ a, outerGood a)
    (hInner : ∀ a, outerGood a → ∃ b, innerGood a b) :
    ∃ a b, outerGood a ∧ innerGood a b := by
  obtain ⟨a, ha⟩ := hOuter
  obtain ⟨b, hb⟩ := hInner a ha
  exact ⟨a, b, ha, hb⟩

/- Theory 55, formula 55.33: exact rational slack. -/
theorem smooth_rational_slack_identity :
    (4 / 3 : ℚ) - 1 / 19 - 189 / 160 = 907 / 9120 := by
  norm_num

theorem smooth_rational_slack_positive :
    (0 : ℚ) < 907 / 9120 := by
  norm_num

/- Theory 55, formula 55.36: exact elementary constant used after `e < 3`. -/
theorem smooth_remainder_integer_constant :
    4 * 3 ^ 7 * 17 < (153600 : ℕ) := by
  norm_num

/- Theory 55, formulae 55.37--55.39: the final upper-bound algebra, conditional
   on the analytic/counting premises listed explicitly below. -/
theorem final_interval_upper_composition
    {A Aprime η ε width scale starCount remainderCount : ℝ}
    (hA : 0 ≤ A) (hη : 0 ≤ η)
    (hε : 0 ≤ ε) (hwidth : 0 ≤ width) (hscale : 0 ≤ scale)
    (hAprimeUpper : Aprime ≤ 5 * A)
    (hStar : starCount ≤ Aprime * (1 + η) * (2 * width + ε) * scale)
    (hRemainder : remainderCount ≤ A * η * ε * scale) :
    starCount + remainderCount ≤
      5 * A * (1 + 2 * η) * (2 * width + ε) * scale := by
  have hLength : 0 ≤ 2 * width + ε := by linarith
  have hOneEta : 0 ≤ 1 + η := by linarith
  have hStar' :
      Aprime * (1 + η) * (2 * width + ε) * scale ≤
        (5 * A) * (1 + η) * (2 * width + ε) * scale := by
    gcongr
  have hRem' :
      A * η * ε * scale ≤ (5 * A) * η * (2 * width + ε) * scale := by
    gcongr <;> nlinarith
  calc
    starCount + remainderCount ≤
        (5 * A) * (1 + η) * (2 * width + ε) * scale +
          (5 * A) * η * (2 * width + ε) * scale :=
      add_le_add (hStar.trans hStar') (hRemainder.trans hRem')
    _ = 5 * A * (1 + 2 * η) * (2 * width + ε) * scale := by ring

end FGKMTSono
