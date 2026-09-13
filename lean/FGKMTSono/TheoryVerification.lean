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

/- Theory 55, formula 55.24: the exact exponential normalization inside
   Rankin's inequality.  The counting inequality itself remains a named source
   premise in `rankin_bound_after_normalization`. -/
theorem rankin_power_normalization
    {Y L u w δ α : ℝ}
    (hY : 0 < Y) (hL : L ≠ 0)
    (hu : u = Real.log Y / L) (hδ : δ = w / L) (hα : α = 1 - δ) :
    Y ^ α = Y * Real.exp (-u * w) := by
  rw [Real.rpow_def_of_pos hY, hα, hδ, hu]
  calc
    Real.exp (Real.log Y * (1 - w / L)) =
        Real.exp (Real.log Y) * Real.exp (-(Real.log Y / L) * w) := by
      rw [← Real.exp_add]
      congr 1
      field_simp
      ring
    _ = Y * Real.exp (-(Real.log Y / L) * w) := by rw [Real.exp_log hY]

theorem rankin_bound_after_normalization
    {psi Y L u w δ α product : ℝ}
    (hY : 0 < Y) (hL : L ≠ 0)
    (hu : u = Real.log Y / L) (hδ : δ = w / L) (hα : α = 1 - δ)
    (hRankin : psi ≤ Y ^ α * product) :
    psi ≤ Y * Real.exp (-u * w) * product := by
  rw [rankin_power_normalization hY hL hu hδ hα] at hRankin
  exact hRankin

/- Theory 55, formula 55.25: the elementary terminal comparison after the
   Rosser--Schoenfeld prime-harmonic estimate supplied as `hPrimeSource`. -/
theorem prime_harmonic_terminal_bound
    {primeSum L B : ℝ}
    (hL : 2000 ≤ L) (hB : B < 1)
    (hPrimeSource : primeSum < Real.log L + B + 1 / (2 * L ^ 2)) :
    primeSum < Real.log L + B + 1 / (2 * L ^ 2) ∧
      Real.log L + B + 1 / (2 * L ^ 2) < Real.log L + 3 / 2 := by
  have hLpos : 0 < L := by linarith
  have hden : 0 < 2 * L ^ 2 := by positivity
  have hfrac : 1 / (2 * L ^ 2) < (1 / 2 : ℝ) := by
    rw [div_lt_iff₀ hden]
    nlinarith [sq_nonneg (L - 1)]
  exact ⟨hPrimeSource, by linarith⟩

/- Theory 55, formula 55.26: the scalar kernel used in the Stieltjes step. -/
noncomputable def smoothStieltjesKernel (δ t : ℝ) : ℝ :=
  (t ^ δ - 1) / (t * Real.log t)

/- Theory 55, formula 55.26: exact integral representation of the scalar
   kernel away from the removable endpoint `t = 1`.  The endpoint value is
   handled separately in formula 55.27. -/
theorem smoothStieltjesKernel_integral {δ t : ℝ} (ht : 0 < t) (ht1 : t ≠ 1) :
    smoothStieltjesKernel δ t = ∫ v in (0 : ℝ)..δ, t ^ (v - 1) := by
  unfold smoothStieltjesKernel
  have hlog : Real.log t ≠ 0 := Real.log_ne_zero_of_pos_of_ne_one ht ht1
  have hderiv : ∀ v : ℝ,
      HasDerivAt (fun u : ℝ ↦ t ^ (u - 1) / Real.log t) (t ^ (v - 1)) v := by
    intro v
    simpa [hlog] using
      (((hasDerivAt_id v).sub_const 1).const_rpow ht).div_const (Real.log t)
  have hint : IntervalIntegrable (fun v : ℝ ↦ t ^ (v - 1)) MeasureTheory.volume 0 δ :=
    (Real.continuous_const_rpow ht.ne').comp
      (continuous_id.sub continuous_const) |>.intervalIntegrable 0 δ
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun v _ ↦ hderiv v) hint]
  rw [Real.rpow_sub_one ht.ne']
  norm_num [Real.rpow_neg_one]
  field_simp

/- Theory 55, formulae 55.26--55.27: endpoint extension and the finite prime
   sum whose exact Stieltjes interpretation is the remaining source-level
   obligation. -/
noncomputable def smoothStieltjesKernelExtended (δ t : ℝ) : ℝ :=
  if t = 1 then δ else smoothStieltjesKernel δ t

noncomputable def smoothPrimeIncrement (δ z : ℝ) : ℝ :=
  ∑ p ∈ Finset.Icc 0 ⌊z⌋₊ with p.Prime,
    (((p : ℝ) ^ δ - 1) / (p : ℝ))

theorem smoothStieltjesKernelExtended_one (δ : ℝ) :
    smoothStieltjesKernelExtended δ 1 = δ := by
  simp [smoothStieltjesKernelExtended]

theorem smoothPrimeKernel_term (δ : ℝ) {p : ℕ} (hp : p.Prime) :
    smoothStieltjesKernelExtended δ p * Real.log p =
      ((p : ℝ) ^ δ - 1) / (p : ℝ) := by
  have hpPos : (0 : ℝ) < p := by exact_mod_cast hp.pos
  have hpOne : (p : ℝ) ≠ 1 := by exact_mod_cast hp.ne_one
  have hlog : Real.log (p : ℝ) ≠ 0 := Real.log_ne_zero_of_pos_of_ne_one hpPos hpOne
  simp only [smoothStieltjesKernelExtended, hpOne, ↓reduceIte]
  unfold smoothStieltjesKernel
  field_simp

theorem smoothPrimeIncrement_kernel_sum (δ z : ℝ) :
    smoothPrimeIncrement δ z =
      ∑ p ∈ Finset.Icc 0 ⌊z⌋₊ with p.Prime,
        smoothStieltjesKernelExtended δ p * Real.log p := by
  unfold smoothPrimeIncrement
  apply Finset.sum_congr rfl
  intro p hpMem
  rw [Finset.mem_filter] at hpMem
  exact (smoothPrimeKernel_term δ hpMem.2).symm

theorem rosserSchoenfeld_constant_slack :
    (1.01624 : ℝ) < 21 / 20 := by
  norm_num

/- Theory 55, untagged formula T55-U002: the entire exponential integral.
   Its value at the removable singularity `v = 0` is irrelevant to the
   interval integral. -/
noncomputable def smoothEin (w : ℝ) : ℝ :=
  ∫ v in (0 : ℝ)..w, (Real.exp v - 1) / v

/- Theory 55, formula 55.27: exact downstream endpoint and Ein substitution.
   `hPartialSummation` deliberately remains a premise: it contains the
   Rosser--Schoenfeld theta estimate and Stieltjes/Abel comparison that are not
   independently formalized by the pinned Mathlib. -/
theorem smoothStieltjes_terminal_composition
    {δ w z kernelIntegral : ℝ}
    (hPartialSummation : smoothPrimeIncrement δ z ≤
      (21 / 20 : ℝ) * (smoothStieltjesKernelExtended δ 1 + kernelIntegral))
    (hKernelIntegral : kernelIntegral = smoothEin w) :
    smoothPrimeIncrement δ z ≤ (21 / 20 : ℝ) * (δ + smoothEin w) := by
  rw [smoothStieltjesKernelExtended_one, hKernelIntegral] at hPartialSummation
  exact hPartialSummation

/- Theory 55, formula 55.28: continuous extension of `(exp v - 1) / v`
   through its removable singularity.  The raw quotient differs only at the
   null singleton `{0}`, so it has the same interval integrals. -/
noncomputable def expm1DivContinuous (v : ℝ) : ℝ :=
  Function.update (fun x : ℝ ↦ (Real.exp x - Real.exp 0) / (x - 0)) 0 1 v

theorem continuous_expm1DivContinuous : Continuous expm1DivContinuous := by
  rw [continuous_iff_continuousAt]
  intro v
  by_cases hv : v = 0
  · subst v
    unfold expm1DivContinuous
    simpa using (Real.hasDerivAt_exp 0).continuousAt_div
  · unfold expm1DivContinuous
    rw [continuousAt_update_of_ne hv]
    fun_prop (disch := aesop)

theorem expm1DivContinuous_eq {v : ℝ} (hv : v ≠ 0) :
    expm1DivContinuous v = (Real.exp v - 1) / v := by
  simp [expm1DivContinuous, hv]

theorem raw_expm1_intervalIntegrable (a b : ℝ) :
    IntervalIntegrable (fun v : ℝ ↦ (Real.exp v - 1) / v) MeasureTheory.volume a b := by
  have hcont : IntervalIntegrable expm1DivContinuous MeasureTheory.volume a b :=
    continuous_expm1DivContinuous.intervalIntegrable a b
  have hae : (fun v : ℝ ↦ (Real.exp v - 1) / v) =ᵐ[MeasureTheory.volume]
      expm1DivContinuous := by
    filter_upwards [MeasureTheory.Measure.ae_ne MeasureTheory.volume (0 : ℝ)] with v hv
    exact (expm1DivContinuous_eq hv).symm
  exact hcont.congr_ae (MeasureTheory.ae_restrict_of_ae hae.symm)

theorem raw_expm1_div_le_exp {v : ℝ} (hv : 0 < v) :
    (Real.exp v - 1) / v ≤ Real.exp v := by
  rw [div_le_iff₀ hv]
  have hbase := Real.add_one_le_exp (-v)
  have hmul := mul_le_mul_of_nonneg_left hbase (Real.exp_pos v).le
  rw [← Real.exp_add] at hmul
  norm_num at hmul
  nlinarith

theorem raw_expm1_lower_half_bound {w : ℝ} (hw : 0 ≤ w) :
    (∫ v in (0 : ℝ)..w / 2, (Real.exp v - 1) / v) ≤ Real.exp (w / 2) := by
  have hhalf : 0 ≤ w / 2 := by positivity
  have hmono :
      (∫ v in (0 : ℝ)..w / 2, (Real.exp v - 1) / v) ≤
        ∫ v in (0 : ℝ)..w / 2, Real.exp v := by
    apply intervalIntegral.integral_mono_on_of_le_Ioo hhalf
      (raw_expm1_intervalIntegrable 0 (w / 2)) intervalIntegral.intervalIntegrable_exp
    intro v hv
    exact raw_expm1_div_le_exp hv.1
  rw [integral_exp] at hmono
  norm_num at hmono
  linarith

/- Theory 55, formula 55.28 and untagged Ein bound: exact scalar constants
   after the two integral pieces have been bounded. -/
theorem ein_split_upper_composition
    {einValue lowerPiece upperPiece scale : ℝ}
    (hSplit : einValue = lowerPiece + upperPiece)
    (hLower : lowerPiece ≤ (1 / 100 : ℝ) * scale)
    (hUpper : upperPiece ≤ (51 / 50 : ℝ) * scale) :
    einValue ≤ (103 / 100 : ℝ) * scale := by
  rw [hSplit]
  nlinarith

theorem smooth_exp_w_identity
    {u w : ℝ} (hu : 1 < u)
    (hw : w = Real.log u + Real.log (Real.log u)) :
    Real.exp w = u * Real.log u := by
  have hupos : 0 < u := zero_lt_one.trans hu
  have hlogupos : 0 < Real.log u := Real.log_pos hu
  rw [hw, Real.exp_add, Real.exp_log hupos, Real.exp_log hlogupos]

theorem exponential_linear_integral_factor {w : ℝ} (hw : 100 ≤ w) :
    1 + 2 / w ≤ (51 / 50 : ℝ) := by
  have hwpos : 0 < w := by linarith
  have hquot : 2 / w ≤ (1 / 50 : ℝ) := by
    rw [div_le_iff₀ hwpos]
    nlinarith
  linarith

theorem exponential_linear_improper_integral {w : ℝ} :
    (∫ t in Set.Ioi (0 : ℝ), Real.exp (-t) * (1 + 2 * t / w)) =
      1 + 2 / w := by
  have hExp : MeasureTheory.IntegrableOn
      (fun t : ℝ ↦ Real.exp (-t)) (Set.Ioi 0) :=
    integrableOn_exp_neg_Ioi 0
  have hMoment : MeasureTheory.IntegrableOn
      (fun t : ℝ ↦ t * Real.exp (-t)) (Set.Ioi 0) := by
    simpa only [show (2 : ℝ) - 1 = 1 by norm_num, Real.rpow_one, mul_comm] using
      (Real.GammaIntegral_convergent (s := (2 : ℝ)) (by norm_num))
  have hMomentIntegral :
      (∫ t in Set.Ioi (0 : ℝ), t * Real.exp (-t)) = 1 := by
    have h := integral_rpow_mul_exp_neg_rpow
      (p := (1 : ℝ)) (q := (1 : ℝ)) (by norm_num) (by norm_num)
    have hGamma : Real.Gamma (2 : ℝ) = 1 := by
      norm_num [Real.Gamma_ofNat_eq_factorial]
    rw [show ((1 : ℝ) + 1) / 1 = 2 by norm_num, hGamma] at h
    norm_num [Real.rpow_one] at h
    exact h
  have hFunction :
      (fun t : ℝ ↦ Real.exp (-t) * (1 + 2 * t / w)) =
        (fun t : ℝ ↦ Real.exp (-t) + (2 / w) * (t * Real.exp (-t))) := by
    funext t
    ring
  rw [hFunction, MeasureTheory.integral_add hExp (hMoment.const_mul (2 / w)),
    MeasureTheory.integral_const_mul, integral_exp_neg_Ioi_zero, hMomentIntegral]
  ring

theorem exponential_linear_integrableOn {w : ℝ} :
    MeasureTheory.IntegrableOn
      (fun t : ℝ ↦ Real.exp (-t) * (1 + 2 * t / w)) (Set.Ioi 0) := by
  have hExp : MeasureTheory.IntegrableOn
      (fun t : ℝ ↦ Real.exp (-t)) (Set.Ioi 0) :=
    integrableOn_exp_neg_Ioi 0
  have hMoment : MeasureTheory.IntegrableOn
      (fun t : ℝ ↦ t * Real.exp (-t)) (Set.Ioi 0) := by
    simpa only [show (2 : ℝ) - 1 = 1 by norm_num, Real.rpow_one, mul_comm] using
      (Real.GammaIntegral_convergent (s := (2 : ℝ)) (by norm_num))
  have hFunction :
      (fun t : ℝ ↦ Real.exp (-t) * (1 + 2 * t / w)) =
        (fun t : ℝ ↦ Real.exp (-t) + (2 / w) * (t * Real.exp (-t))) := by
    funext t
    ring
  rw [hFunction]
  exact hExp.add (hMoment.const_mul (2 / w))

theorem exponential_linear_interval_le_improper {w M : ℝ}
    (hw : 0 < w) (hM : 0 ≤ M) :
    (∫ t in (0 : ℝ)..M, Real.exp (-t) * (1 + 2 * t / w)) ≤
      ∫ t in Set.Ioi (0 : ℝ), Real.exp (-t) * (1 + 2 * t / w) := by
  rw [intervalIntegral.integral_of_le hM]
  apply MeasureTheory.setIntegral_mono_set exponential_linear_integrableOn
  · filter_upwards [MeasureTheory.ae_restrict_mem measurableSet_Ioi] with t ht
    have hquot : 0 ≤ 2 * t / w := div_nonneg (mul_nonneg (by norm_num) ht.le) hw.le
    exact mul_nonneg (Real.exp_pos (-t)).le (by linarith)
  · exact Set.Ioc_subset_Ioi_self.eventuallyLE

theorem reciprocal_half_interval_bound {w t : ℝ}
    (hw : 0 < w) (ht0 : 0 ≤ t) (htHalf : t ≤ w / 2) :
    1 / (w - t) ≤ (1 / w) * (1 + 2 * t / w) := by
  have hden : 0 < w - t := by linarith
  rw [div_le_iff₀ hden]
  rw [one_div]
  field_simp
  nlinarith [mul_nonneg ht0 (show 0 ≤ w - 2 * t by linarith)]

theorem raw_expm1_upper_transform {w t : ℝ}
    (hw : 100 ≤ w) (ht0 : 0 ≤ t) (htHalf : t ≤ w / 2) :
    (Real.exp (w - t) - 1) / (w - t) ≤
      (Real.exp w / w) * (Real.exp (-t) * (1 + 2 * t / w)) := by
  have hwpos : 0 < w := by linarith
  have hden : 0 < w - t := by linarith
  have hnum : Real.exp (w - t) - 1 ≤ Real.exp (w - t) := by linarith
  have hfirst : (Real.exp (w - t) - 1) / (w - t) ≤ Real.exp (w - t) / (w - t) :=
    (div_le_div_iff_of_pos_right hden).2 hnum
  have hrecip := reciprocal_half_interval_bound hwpos ht0 htHalf
  have hmul := mul_le_mul_of_nonneg_left hrecip (Real.exp_pos (w - t)).le
  calc
    (Real.exp (w - t) - 1) / (w - t) ≤ Real.exp (w - t) / (w - t) := hfirst
    _ = Real.exp (w - t) * (1 / (w - t)) := by ring
    _ ≤ Real.exp (w - t) * ((1 / w) * (1 + 2 * t / w)) := hmul
    _ = (Real.exp w / w) * (Real.exp (-t) * (1 + 2 * t / w)) := by
      rw [show w - t = w + (-t) by ring, Real.exp_add]
      ring

theorem raw_expm1_upper_half_bound {w : ℝ} (hw : 100 ≤ w) :
    (∫ v in w / 2..w, (Real.exp v - 1) / v) ≤
      (Real.exp w / w) *
        (∫ t in Set.Ioi (0 : ℝ), Real.exp (-t) * (1 + 2 * t / w)) := by
  have hwpos : 0 < w := by linarith
  have hhalf : 0 ≤ w / 2 := by positivity
  have htransform :
      (∫ v in w / 2..w, (Real.exp v - 1) / v) =
        ∫ t in (0 : ℝ)..w / 2, (Real.exp (w - t) - 1) / (w - t) := by
    symm
    convert intervalIntegral.integral_comp_sub_left
      (fun v : ℝ ↦ (Real.exp v - 1) / v) w using 1
    ring_nf
  have hleft : IntervalIntegrable
      (fun t : ℝ ↦ (Real.exp (w - t) - 1) / (w - t)) MeasureTheory.volume 0 (w / 2) := by
    have hraw := raw_expm1_intervalIntegrable (w / 2) w
    have hcomp := hraw.comp_sub_left w
    convert hcomp.symm using 1 <;> ring_nf
  have hright : IntervalIntegrable
      (fun t : ℝ ↦ (Real.exp w / w) *
        (Real.exp (-t) * (1 + 2 * t / w))) MeasureTheory.volume 0 (w / 2) := by
    apply Continuous.intervalIntegrable
    fun_prop (disch := exact hwpos.ne')
  have hmono :
      (∫ t in (0 : ℝ)..w / 2, (Real.exp (w - t) - 1) / (w - t)) ≤
        ∫ t in (0 : ℝ)..w / 2, (Real.exp w / w) *
          (Real.exp (-t) * (1 + 2 * t / w)) := by
    apply intervalIntegral.integral_mono_on_of_le_Ioo hhalf hleft hright
    intro t ht
    exact raw_expm1_upper_transform hw ht.1.le ht.2.le
  have hfinite := exponential_linear_interval_le_improper hwpos hhalf
  have hscale : 0 ≤ Real.exp w / w := by positivity
  calc
    (∫ v in w / 2..w, (Real.exp v - 1) / v) =
        ∫ t in (0 : ℝ)..w / 2, (Real.exp (w - t) - 1) / (w - t) := htransform
    _ ≤ ∫ t in (0 : ℝ)..w / 2, (Real.exp w / w) *
        (Real.exp (-t) * (1 + 2 * t / w)) := hmono
    _ = (Real.exp w / w) *
        (∫ t in (0 : ℝ)..w / 2, Real.exp (-t) * (1 + 2 * t / w)) := by
      rw [intervalIntegral.integral_const_mul]
    _ ≤ (Real.exp w / w) *
        (∫ t in Set.Ioi (0 : ℝ), Real.exp (-t) * (1 + 2 * t / w)) :=
      mul_le_mul_of_nonneg_left hfinite hscale

theorem exponential_half_tail_bound {w : ℝ} (hw : 100 ≤ w) :
    Real.exp (w / 2) ≤ (1 / 100 : ℝ) * Real.exp w / w := by
  have hwpos : 0 < w := by linarith
  have hhalf : 50 ≤ w / 2 := by linarith
  have hhalfDomain : 1 ≤ w / 2 := by linarith
  have hratioMono :
      Real.exp 50 / 50 ≤ Real.exp (w / 2) / (w / 2) :=
    exp_div_self_strictMonoOn.monotoneOn (by norm_num) hhalfDomain hhalf
  have hexp50 : (10000 : ℝ) < Real.exp 50 := by
    have hseries := Real.sum_le_exp_of_nonneg (x := (50 : ℝ)) (by norm_num) 4
    norm_num [Finset.sum_range_succ] at hseries ⊢
    linarith
  have hratio50 : (200 : ℝ) < Real.exp 50 / 50 := by
    rw [lt_div_iff₀ (by norm_num : (0 : ℝ) < 50)]
    rw [show (200 : ℝ) * 50 = 10000 by norm_num]
    exact hexp50
  have hratio : (200 : ℝ) < Real.exp (w / 2) / (w / 2) :=
    hratio50.trans_le hratioMono
  have hcore : 100 * w < Real.exp (w / 2) := by
    rw [lt_div_iff₀ (by linarith : (0 : ℝ) < w / 2)] at hratio
    nlinarith
  have hsq : Real.exp (w / 2) * Real.exp (w / 2) = Real.exp w := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hcross :
      Real.exp (w / 2) * w < (1 / 100 : ℝ) * Real.exp w := by
    have hmul := mul_lt_mul_of_pos_right hcore (Real.exp_pos (w / 2))
    rw [mul_assoc, mul_comm w (Real.exp (w / 2)), hsq] at hmul
    nlinarith
  exact (le_div_iff₀ hwpos).2 hcross.le

theorem smoothEin_split {w : ℝ} :
    smoothEin w =
      (∫ v in (0 : ℝ)..w / 2, (Real.exp v - 1) / v) +
        ∫ v in w / 2..w, (Real.exp v - 1) / v := by
  unfold smoothEin
  exact (intervalIntegral.integral_add_adjacent_intervals
    (raw_expm1_intervalIntegrable 0 (w / 2))
    (raw_expm1_intervalIntegrable (w / 2) w)).symm

/- Theory 55, formula 55.28: both finite-interval comparisons and the final
   `103/100` bound, including the removable singularity at zero. -/
theorem smoothEin_upper_bound {w : ℝ} (hw : 100 ≤ w) :
    smoothEin w ≤ (103 / 100 : ℝ) * (Real.exp w / w) := by
  have hwpos : 0 < w := by linarith
  have hscale : 0 ≤ Real.exp w / w := by positivity
  have hLowerRaw := raw_expm1_lower_half_bound hwpos.le
  have hHalfTail := exponential_half_tail_bound hw
  have hLower :
      (∫ v in (0 : ℝ)..w / 2, (Real.exp v - 1) / v) ≤
        (1 / 100 : ℝ) * (Real.exp w / w) := by
    calc
      (∫ v in (0 : ℝ)..w / 2, (Real.exp v - 1) / v) ≤ Real.exp (w / 2) :=
        hLowerRaw
      _ ≤ (1 / 100 : ℝ) * Real.exp w / w := hHalfTail
      _ = (1 / 100 : ℝ) * (Real.exp w / w) := by ring
  have hUpperRaw := raw_expm1_upper_half_bound hw
  rw [exponential_linear_improper_integral] at hUpperRaw
  have hFactor := exponential_linear_integral_factor hw
  have hUpperScale :
      (Real.exp w / w) * (1 + 2 / w) ≤
        (Real.exp w / w) * (51 / 50 : ℝ) :=
    mul_le_mul_of_nonneg_left hFactor hscale
  have hUpper :
      (∫ v in w / 2..w, (Real.exp v - 1) / v) ≤
        (51 / 50 : ℝ) * (Real.exp w / w) := by
    calc
      (∫ v in w / 2..w, (Real.exp v - 1) / v) ≤
          (Real.exp w / w) * (1 + 2 / w) := hUpperRaw
      _ ≤ (Real.exp w / w) * (51 / 50 : ℝ) := hUpperScale
      _ = (51 / 50 : ℝ) * (Real.exp w / w) := by ring
  exact ein_split_upper_composition smoothEin_split hLower hUpper

/- Theory 55, formula 55.30: the elementary constant
   `2 ^ (-3/4) < 3/5`.  The proof compares fourth powers and then reverses the
   inequality under positive inversion. -/
theorem two_rpow_neg_three_quarters_lt_three_fifths :
    (2 : ℝ) ^ (-(3 / 4 : ℝ)) < 3 / 5 := by
  have hFourthPower :
      (5 / 3 : ℝ) ^ (4 : ℕ) <
        ((2 : ℝ) ^ (3 / 4 : ℝ)) ^ (4 : ℕ) := by
    rw [← Real.rpow_mul_natCast (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num [Real.rpow_natCast]
  have hRoot :
      (5 / 3 : ℝ) < (2 : ℝ) ^ (3 / 4 : ℝ) :=
    lt_of_pow_lt_pow_left₀ 4 (Real.rpow_nonneg (by norm_num) _) hFourthPower
  have hInverse :
      ((2 : ℝ) ^ (3 / 4 : ℝ))⁻¹ < ((5 / 3 : ℝ))⁻¹ :=
    inv_strictAnti₀ (by norm_num) hRoot
  rw [Real.rpow_neg (by norm_num : (0 : ℝ) ≤ 2)]
  norm_num at hInverse ⊢
  exact hInverse

/- Theory 55, formula 55.30: the exact terminal arithmetic after the geometric
   comparison and p-series estimate are supplied explicitly. -/
theorem euler_tail_terminal_bound
    {tail base : ℝ}
    (hbaseUpper : base < 2)
    (hTail : tail ≤
      (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) * base) :
    tail < 3 := by
  have htwoUpper := two_rpow_neg_three_quarters_lt_three_fifths
  have hden : 0 < 1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)) := by linarith
  have hInv : 1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ))) < (5 / 2 : ℝ) := by
    rw [div_lt_iff₀ hden]
    nlinarith
  have hMid :
      (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) * base <
        (1 / 2 : ℝ) * (5 / 2) * 2 := by
    have hFirst :
        (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) <
          (1 / 2 : ℝ) * (5 / 2) :=
      mul_lt_mul_of_pos_left hInv (by norm_num)
    have hAtBase :
        (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) * base <
          (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) * 2 :=
      mul_lt_mul_of_pos_left hbaseUpper (by positivity)
    have hAtTwo :
        (1 / 2 : ℝ) * (1 / (1 - (2 : ℝ) ^ (-(3 / 4 : ℝ)))) * 2 <
          (1 / 2 : ℝ) * (5 / 2) * 2 :=
      mul_lt_mul_of_pos_right hFirst (by norm_num)
    exact hAtBase.trans hAtTwo
  exact hTail.trans_lt (hMid.trans (by norm_num))

/- Theory 55, formula 55.31: Euler-product logarithm composition, conditional
   only on the three preceding analytic/counting estimates and the exact log
   decomposition. -/
theorem euler_product_log_composition
    {productLog primeSum increment tail L u : ℝ}
    (hDecompose : productLog = primeSum + increment + tail)
    (hPrime : primeSum < Real.log L + 3 / 2)
    (hIncrement : increment < (189 / 160 : ℝ) * u)
    (hTail : tail < 3) :
    productLog < Real.log L + 7 + (189 / 160 : ℝ) * u := by
  rw [hDecompose]
  linarith

/- Theory 55, formula 55.32: all logarithmic estimates from the actual
   hypotheses `q ≥ 200`, `b = exp q`, and `u > 4b/q`. -/
theorem log_le_one_twentieth_of_ge_200 {q : ℝ} (hq : 200 ≤ q) :
    Real.log q ≤ q / 20 := by
  have h200Domain : Real.exp 1 ≤ (200 : ℝ) :=
    (le_of_lt Real.exp_one_lt_three).trans (by norm_num)
  have hqDomain : Real.exp 1 ≤ q := h200Domain.trans hq
  have hLog200 : Real.log (200 : ℝ) < 6 := by
    rw [Real.log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 200)]
    have hseries := Real.sum_le_exp_of_nonneg (x := (6 : ℝ)) (by norm_num) 8
    norm_num [Finset.sum_range_succ] at hseries ⊢
    linarith
  have hRatio200 : Real.log (200 : ℝ) / 200 ≤ (1 / 20 : ℝ) := by
    norm_num at hLog200 ⊢
    linarith
  have hRatio := Real.log_div_self_antitoneOn h200Domain hqDomain hq
  have hqpos : 0 < q := by linarith
  calc
    Real.log q = (Real.log q / q) * q := by field_simp
    _ ≤ (1 / 20 : ℝ) * q :=
      mul_le_mul_of_nonneg_right (hRatio.trans hRatio200) hqpos.le
    _ = q / 20 := by ring

theorem log_nineteen_twentieth_gt_neg_one_nineteenth :
    Real.log (19 / 20 : ℝ) > -(1 / 19 : ℝ) := by
  have h := Real.log_lt_sub_one_of_pos (x := (20 / 19 : ℝ)) (by norm_num) (by norm_num)
  rw [show (19 / 20 : ℝ) = (20 / 19 : ℝ)⁻¹ by norm_num, Real.log_inv]
  norm_num at h ⊢
  linarith

theorem log_four_gt_four_thirds : Real.log (4 : ℝ) > 4 / 3 := by
  rw [show (4 : ℝ) = 2 * 2 by norm_num, Real.log_mul (by norm_num) (by norm_num)]
  nlinarith [Real.log_two_gt_d9]

theorem smooth_log_lower_bounds
    {q b u : ℝ}
    (hq : 200 ≤ q) (hb : b = Real.exp q) (hu : 4 * b / q < u) :
    q + Real.log 4 - Real.log q < Real.log u ∧
      Real.log q - 1 / 19 < Real.log (Real.log u) := by
  have hqpos : 0 < q := by linarith
  have hbpos : 0 < b := by rw [hb]; positivity
  have hlowerPos : 0 < 4 * b / q := by positivity
  have hupos : 0 < u := hlowerPos.trans hu
  have hFirst : Real.log (4 * b / q) < Real.log u :=
    Real.log_lt_log hlowerPos hu
  have hFirstRewrite : Real.log (4 * b / q) = q + Real.log 4 - Real.log q := by
    rw [Real.log_div (by positivity) hqpos.ne', Real.log_mul (by norm_num) hbpos.ne', hb,
      Real.log_exp]
    ring
  have hlogq := log_le_one_twentieth_of_ge_200 hq
  have hloguLower : (19 / 20 : ℝ) * q < Real.log u := by
    rw [hFirstRewrite] at hFirst
    have hlog4pos : 0 < Real.log (4 : ℝ) := Real.log_pos (by norm_num)
    nlinarith
  have hnineteenPos : 0 < (19 / 20 : ℝ) * q := by positivity
  have hSecondRaw :
      Real.log ((19 / 20 : ℝ) * q) < Real.log (Real.log u) :=
    Real.log_lt_log hnineteenPos hloguLower
  have hSecondRewrite :
      Real.log ((19 / 20 : ℝ) * q) =
        Real.log q + Real.log (19 / 20 : ℝ) := by
    rw [Real.log_mul (by norm_num) hqpos.ne']
    ring
  constructor
  · rwa [← hFirstRewrite]
  · rw [hSecondRewrite] at hSecondRaw
    nlinarith [log_nineteen_twentieth_gt_neg_one_nineteenth]

/- Theory 55, formula 55.29: the complete numerical composition from the
   remaining Stieltjes premise.  The Ein upper bound is discharged internally
   by the kernel proof of formula 55.28 and T55-U003. -/
theorem smooth_increment_terminal_bound
    {q b u w δ increment : ℝ}
    (hq : 200 ≤ q) (hb : b = Real.exp q) (hu : 4 * b / q < u)
    (hw : w = Real.log u + Real.log (Real.log u))
    (hδ : δ ≤ 1 / 20)
    (hStieltjes : increment ≤ (21 / 20 : ℝ) * (δ + smoothEin w)) :
    increment < (189 / 160 : ℝ) * u := by
  obtain ⟨hlogu, hloglogu⟩ := smooth_log_lower_bounds hq hb hu
  have hqpos : 0 < q := by linarith
  have hbpos : 0 < b := by rw [hb]; positivity
  have hupos : 0 < u := (div_pos (mul_pos (by norm_num) hbpos) hqpos).trans hu
  have hlogqLarge : (1 / 19 : ℝ) < Real.log q := by
    have htwoq : (2 : ℝ) < q := by linarith
    have hlogtwoq := Real.log_lt_log (by norm_num : (0 : ℝ) < 2) htwoq
    nlinarith [Real.log_two_gt_d9]
  have hloglogupos : 0 < Real.log (Real.log u) := by
    linarith
  have hwlog : Real.log u < w := by rw [hw]; linarith
  have hwLarge : 100 < w := by
    rw [hw]
    nlinarith [log_four_gt_four_thirds]
  have hEin : smoothEin w ≤ (103 / 100 : ℝ) * (Real.exp w / w) :=
    smoothEin_upper_bound hwLarge.le
  have hwpos : 0 < w := by linarith
  have hexpRatio : 1 < Real.exp w / w := by
    rw [lt_div_iff₀ hwpos]
    linarith [Real.add_one_lt_exp hwpos.ne']
  have hδexp : δ < (1 / 20 : ℝ) * (Real.exp w / w) := by
    nlinarith
  have hCombined :
      δ + smoothEin w < (27 / 25 : ℝ) * (Real.exp w / w) := by
    nlinarith
  have hFirst :
      increment < (567 / 500 : ℝ) * (Real.exp w / w) := by
    calc
      increment ≤ (21 / 20 : ℝ) * (δ + smoothEin w) := hStieltjes
      _ < (21 / 20 : ℝ) * ((27 / 25 : ℝ) * (Real.exp w / w)) :=
        mul_lt_mul_of_pos_left hCombined (by norm_num)
      _ = (567 / 500 : ℝ) * (Real.exp w / w) := by ring
  have huOne : 1 < u := by
    have hbOne : 1 < b := by rw [hb]; exact Real.one_lt_exp_iff.mpr hqpos
    have hLowerOne : 1 < 4 * b / q := by
      have hqUpper : q < b := by
        rw [hb]
        linarith [Real.add_one_lt_exp hqpos.ne']
      rw [one_lt_div hqpos]
      nlinarith
    exact hLowerOne.trans hu
  have hexpIdentity := smooth_exp_w_identity huOne hw
  have hRatioU : Real.exp w / w < u := by
    rw [div_lt_iff₀ hwpos, hexpIdentity]
    exact mul_lt_mul_of_pos_left hwlog hupos
  have hCoeff : (567 / 500 : ℝ) < 189 / 160 := by norm_num
  calc
    increment < (567 / 500 : ℝ) * (Real.exp w / w) := hFirst
    _ < (567 / 500 : ℝ) * u := mul_lt_mul_of_pos_left hRatioU (by norm_num)
    _ < (189 / 160 : ℝ) * u := mul_lt_mul_of_pos_right hCoeff hupos

/- Theory 55, formula 55.33: exact rational slack. -/
theorem smooth_rational_slack_identity :
    (4 / 3 : ℚ) - 1 / 19 - 189 / 160 = 907 / 9120 := by
  norm_num

theorem smooth_rational_slack_positive :
    (0 : ℚ) < 907 / 9120 := by
  norm_num

/- Theory 55, formula 55.34: the full elementary implication from formula
   55.32 and the exact rational slack. -/
theorem smooth_decay_exceeds_four_b
    {q b u w : ℝ}
    (hq : 200 ≤ q) (hb : b = Real.exp q) (hu : 4 * b / q < u)
    (hw : w = Real.log u + Real.log (Real.log u)) :
    4 * b < u * (w - 189 / 160) := by
  obtain ⟨hlogu, hloglogu⟩ := smooth_log_lower_bounds hq hb hu
  have hqpos : 0 < q := by linarith
  have hbpos : 0 < b := by rw [hb]; positivity
  have hupos : 0 < u := (div_pos (mul_pos (by norm_num) hbpos) hqpos).trans hu
  have hcore : q < w - 189 / 160 := by
    rw [hw]
    nlinarith [log_four_gt_four_thirds,
      (show (0 : ℝ) < 907 / 9120 by norm_num)]
  have hmul : u * q < u * (w - 189 / 160) :=
    mul_lt_mul_of_pos_left hcore hupos
  have hbase : 4 * b < u * q := by
    rw [div_lt_iff₀ hqpos] at hu
    nlinarith
  exact hbase.trans hmul

/- Theory 55, formula 55.35: final smooth-count composition.  Rankin's
   counting bound and the Euler-product logarithm bound are explicit premises;
   the exponential cancellation and `a⁻³` conclusion are kernel-checked. -/
theorem smooth_count_terminal_bound
    {psi Y a b L u w product : ℝ}
    (hY : 0 < Y) (hL : 0 < L) (hProduct : 0 < product)
    (haExp : a = Real.exp b)
    (hRankin : psi ≤ Y * Real.exp (-u * w) * product)
    (hProductLog :
      Real.log product < Real.log L + 7 + (189 / 160 : ℝ) * u)
    (hLogL : Real.log L < b)
    (hDecay : 4 * b < u * (w - 189 / 160)) :
    psi < Real.exp 7 * Y / a ^ 3 := by
  have hProductExp :
      product < Real.exp (Real.log L + 7 + (189 / 160 : ℝ) * u) :=
    (Real.log_lt_iff_lt_exp hProduct).mp hProductLog
  have hRankinFactorPos : 0 < Y * Real.exp (-u * w) := by positivity
  have hFirst :
      psi < Y * Real.exp (-u * w) *
        Real.exp (Real.log L + 7 + (189 / 160 : ℝ) * u) :=
    hRankin.trans_lt (mul_lt_mul_of_pos_left hProductExp hRankinFactorPos)
  have hExpCombine :
      Real.exp (-u * w) *
          Real.exp (Real.log L + 7 + (189 / 160 : ℝ) * u) =
        L * Real.exp 7 * Real.exp (-u * (w - 189 / 160)) := by
    rw [← Real.exp_add]
    calc
      Real.exp (-u * w + (Real.log L + 7 + (189 / 160 : ℝ) * u)) =
          Real.exp (Real.log L + 7 + (-u * (w - 189 / 160))) := by
        congr 1
        ring
      _ = L * Real.exp 7 * Real.exp (-u * (w - 189 / 160)) := by
        rw [show Real.log L + 7 + (-u * (w - 189 / 160)) =
          (Real.log L + 7) + (-u * (w - 189 / 160)) by ring,
          Real.exp_add, Real.exp_add, Real.exp_log hL]
  have hFirstReshaped :
      psi < (Real.exp 7 * Y) *
        (L * Real.exp (-u * (w - 189 / 160))) := by
    calc
      psi < Y * Real.exp (-u * w) *
          Real.exp (Real.log L + 7 + (189 / 160 : ℝ) * u) := hFirst
      _ = (Real.exp 7 * Y) *
          (L * Real.exp (-u * (w - 189 / 160))) := by
        rw [mul_assoc, hExpCombine]
        ring
  have hExponent : -u * (w - 189 / 160) < -4 * b := by
    nlinarith
  have hExpDecay :
      Real.exp (-u * (w - 189 / 160)) < Real.exp (-4 * b) :=
    Real.exp_lt_exp.mpr hExponent
  have hLExp : L < Real.exp b := (Real.log_lt_iff_lt_exp hL).mp hLogL
  have hCoreFirst :
      L * Real.exp (-u * (w - 189 / 160)) < L * Real.exp (-4 * b) :=
    mul_lt_mul_of_pos_left hExpDecay hL
  have hCoreSecond :
      L * Real.exp (-4 * b) < Real.exp b * Real.exp (-4 * b) :=
    mul_lt_mul_of_pos_right hLExp (Real.exp_pos _)
  have hCoreExp :
      L * Real.exp (-u * (w - 189 / 160)) < Real.exp (-3 * b) := by
    calc
      L * Real.exp (-u * (w - 189 / 160)) < L * Real.exp (-4 * b) := hCoreFirst
      _ < Real.exp b * Real.exp (-4 * b) := hCoreSecond
      _ = Real.exp (-3 * b) := by
        rw [← Real.exp_add]
        congr 1
        ring
  have hExpA : Real.exp (-3 * b) = 1 / a ^ 3 := by
    calc
      Real.exp (-3 * b) = (Real.exp (3 * b))⁻¹ := by
        rw [show -3 * b = -(3 * b) by ring, Real.exp_neg]
      _ = (Real.exp b ^ 3)⁻¹ := by
        rw [show (3 : ℝ) * b = (3 : ℕ) * b by norm_num, Real.exp_nat_mul]
      _ = 1 / a ^ 3 := by rw [haExp]; simp [one_div]
  have hCore :
      L * Real.exp (-u * (w - 189 / 160)) < 1 / a ^ 3 := by
    rwa [← hExpA]
  have hMultiplier : 0 < Real.exp 7 * Y := by positivity
  calc
    psi < (Real.exp 7 * Y) *
        (L * Real.exp (-u * (w - 189 / 160))) := hFirstReshaped
    _ < (Real.exp 7 * Y) * (1 / a ^ 3) :=
      mul_lt_mul_of_pos_left hCore hMultiplier
    _ = Real.exp 7 * Y / a ^ 3 := by ring

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

/-! ## Theory 56 — DEP-R09 numerical PAP source and constant audit -/

/- Theory 56, formula 56.1: Sono's explicit zero-free constant and the
   short-interval exponent selected from it. -/
noncomputable def papCZFR : ℝ := 1 / 24

noncomputable def papShortIntervalExponent : ℝ := (3 / 10) * papCZFR

theorem pap_short_interval_exponent_value :
    papShortIntervalExponent = 1 / 80 := by
  norm_num [papShortIntervalExponent, papCZFR]

/- Theory 56, formula 56.2: the zero-density exponent and PAP power. -/
noncomputable def papCZD : ℝ := 16

noncomputable def papDPAP : ℝ := 10 * papCZD

theorem pap_dpap_value : papDPAP = 160 := by
  norm_num [papDPAP, papCZD]

/- Theory 56, formula 56.3: exact exponent product and coefficient. -/
noncomputable def papCoefficient : ℝ := 1 - Real.exp (-2)

theorem pap_exponent_product :
    papShortIntervalExponent * papDPAP = 2 := by
  rw [pap_short_interval_exponent_value, pap_dpap_value]
  norm_num

theorem pap_coefficient_identity :
    papCoefficient = 1 - Real.exp (-2) := rfl

/- Theory 56, formula 56.4: the printed coefficient lies strictly between
   zero and one. -/
theorem pap_coefficient_pos_lt_one :
    0 < papCoefficient ∧ papCoefficient < 1 := by
  constructor
  · exact sub_pos.mpr (Real.exp_lt_one_iff.mpr (by norm_num))
  · have hexp : 0 < Real.exp (-2) := Real.exp_pos _
    dsimp [papCoefficient]
    linarith

/- Theory 56, formula 56.5: finite one-sided error composition.  The analytic
   principal and nonprincipal estimates remain explicit premises. -/
theorem pap_finite_error_composition
    {mainTerm principal error η : ℝ}
    (hPrincipal : (1 - η) * mainTerm ≤ principal)
    (hError : |error| ≤ Real.exp (-2) * mainTerm) :
    (papCoefficient - η) * mainTerm ≤ principal + error := by
  have hErrorLower : -(Real.exp (-2) * mainTerm) ≤ error :=
    (abs_le.mp hError).1
  dsimp [papCoefficient]
  nlinarith

/- Theory 56, formula 56.6: after Q=T, source epsilon/3 produces Sono's
   renamed exponent 6+epsilon.  This does not remove the epsilon-dependent
   implied multiplier. -/
theorem jutila_epsilon_reparameterization (ε : ℝ) :
    3 * (2 + ε / 3) = 6 + ε := by
  ring

/- Theory 56, formula 56.7: the elementary low-alpha exponent bridge. -/
theorem jutila_low_alpha_exponent_bridge
    {α : ℝ} (hα : α ≤ 4 / 5) :
    3 ≤ 15 * (1 - α) := by
  linarith

/-! ## Theory 57 — DEP-R09 Gallagher-Maier-McCurley source recovery -/

/- Theory 57, formula 57.2: the denominator normalization that follows from
   Sono Proposition 5.3 after setting Q=T and restricting |t|<=T.  This is an
   elementary real inequality, not a formalization of the source theorem. -/
theorem pap_source_log_denominator_bound
    {T : ℝ} (hT : 2 ≤ T) :
    Real.log (T * (1 + T)) ≤ 3 * Real.log T := by
  have hTpos : 0 < T := by linarith
  have honeTpos : 0 < 1 + T := by linarith
  have hquadratic : 1 + T ≤ T ^ 2 := by
    nlinarith [sq_nonneg (T - 1)]
  have hproduct : T * (1 + T) ≤ T ^ 3 := by
    calc
      T * (1 + T) ≤ T * T ^ 2 :=
        mul_le_mul_of_nonneg_left hquadratic hTpos.le
      _ = T ^ 3 := by ring
  have hlog := Real.log_le_log (mul_pos hTpos honeTpos) hproduct
  simpa [Real.log_pow] using hlog

theorem pap_source_zero_free_width_bound
    {T : ℝ} (hT : 2 ≤ T) :
    papCZFR / (3 * Real.log T) ≤
      papCZFR / Real.log (T * (1 + T)) := by
  have hTgtOne : 1 < T := by linarith
  have hlogTpos : 0 < Real.log T := Real.log_pos hTgtOne
  have hproductGtOne : 1 < T * (1 + T) := by nlinarith
  have hlogProductPos : 0 < Real.log (T * (1 + T)) :=
    Real.log_pos hproductGtOne
  rw [div_le_div_iff₀ (mul_pos (by norm_num) hlogTpos) hlogProductPos]
  exact mul_le_mul_of_nonneg_left
    (pap_source_log_denominator_bound hT) (by norm_num [papCZFR])

/- Theory 57, formula 57.3: the source-compatible conservative bridge and
   Sono's printed bridge are not the same constant. -/
theorem pap_printed_bridge_constants :
    papCZFR / 3 = 1 / 72 ∧
      3 * papCZFR = 1 / 8 ∧
      papCZFR / 3 ≠ 3 * papCZFR := by
  norm_num [papCZFR]

/- Theory 57, formula 57.6: only the exact numerical part of the direct
   McCurley bridge is checked here.  McCurley's zero-free theorems remain
   source analytic inputs and are not asserted as local axioms. -/
noncomputable def papMcCurleyR : ℝ := 9645908801 / 1000000000

noncomputable def papDirectBridgeC1 : ℝ := 1 / 24

theorem pap_mccurley_R_lt_twelve : papMcCurleyR < 12 := by
  norm_num [papMcCurleyR]

theorem pap_direct_bridge_within_theorem_one :
    2 * papMcCurleyR * papDirectBridgeC1 < 1 := by
  norm_num [papMcCurleyR, papDirectBridgeC1]

/- Theory 57, formula 57.8: the density-power boundary at c_ZD=16 and
   D_PAP=160. -/
theorem pap_density_power_boundary :
    5 * papCZD / papDPAP = 1 / 2 := by
  norm_num [papCZD, papDPAP]

/- Theory 57, formula 57.9: the lower Gallagher range after Q=x^(1/D),
   written with L=log x. -/
theorem pap_log_range_gate
    {L D : ℝ} (hD : 0 < D) (hL : D ^ 2 ≤ L) :
    Real.sqrt L ≤ L / D := by
  have hLnonneg : 0 ≤ L := (sq_nonneg D).trans hL
  have hsqrtNonneg : 0 ≤ Real.sqrt L := Real.sqrt_nonneg L
  have hsqrtSq : (Real.sqrt L) ^ 2 = L := Real.sq_sqrt hLnonneg
  have hDtoSqrt : D ≤ Real.sqrt L := by
    nlinarith
  apply (le_div_iff₀ hD).2
  have hmul := mul_le_mul_of_nonneg_right hDtoSqrt hsqrtNonneg
  nlinarith

theorem pap_log_range_gate_160
    {L : ℝ} (hL : 25600 ≤ L) :
    Real.sqrt L ≤ L / 160 := by
  apply pap_log_range_gate (D := 160)
  · norm_num
  · norm_num
    exact hL

/- Theory 57, formula 57.10: repaired conservative zero-free exponent. -/
noncomputable def papRepairedExponent : ℝ := papDirectBridgeC1 / 10

theorem pap_repaired_exponent_value :
    papRepairedExponent = 1 / 240 := by
  norm_num [papRepairedExponent, papDirectBridgeC1]

theorem pap_repaired_exponent_product :
    papRepairedExponent * papDPAP = 2 / 3 := by
  rw [pap_repaired_exponent_value, pap_dpap_value]
  norm_num

/- Theory 57, formula 57.12: an unnamed Vinogradov multiplier cannot be
   removed while retaining the same exponent unless it is at most one. -/
theorem pap_same_exponent_multiplier_iff (K a D : ℝ) :
    K * Real.exp (-a * D) ≤ Real.exp (-a * D) ↔ K ≤ 1 := by
  have hexp : 0 < Real.exp (-a * D) := Real.exp_pos _
  constructor <;> intro h <;> nlinarith

/- Theory 57, formula 57.13: a positive multiplier can instead be absorbed
   by spending exponent or D budget. -/
theorem pap_multiplier_absorption
    {K a₀ a D : ℝ}
    (hK : 0 < K) (hBudget : Real.log K ≤ (a₀ - a) * D) :
    K * Real.exp (-a₀ * D) ≤ Real.exp (-a * D) := by
  calc
    K * Real.exp (-a₀ * D) =
        Real.exp (Real.log K) * Real.exp (-a₀ * D) := by
          rw [Real.exp_log hK]
    _ = Real.exp (Real.log K + (-a₀ * D)) := by
      rw [← Real.exp_add]
    _ ≤ Real.exp (-a * D) := by
      apply Real.exp_le_exp.mpr
      nlinarith

/- Theory 57, formula 57.14: finite one-sided composition with the source
   multiplier left visible.  Both analytic estimates are explicit premises. -/
theorem pap_finite_error_with_multiplier
    {mainTerm principal error η K a D : ℝ}
    (hPrincipal : (1 - η) * mainTerm ≤ principal)
    (hError : |error| ≤ K * Real.exp (-a * D) * mainTerm) :
    (1 - η - K * Real.exp (-a * D)) * mainTerm ≤ principal + error := by
  have hErrorLower :
      -(K * Real.exp (-a * D) * mainTerm) ≤ error :=
    (abs_le.mp hError).1
  nlinarith

/-! ## Theory 59 — DEP-R09 Branch S fixed-D quantitative transfer audit -/

/- Theory 59, formula 59.5: a numerical decay constant that pays the visible
   logarithmic multiplier budget is sufficient for the fixed-D exponential
   diagnostic. This is elementary algebra only; it does not assert that the
   Thorner--Zaman or Jutila analytic source supplies K, c, or a cutoff. -/
theorem pap_fixed_d_transfer_gate
    {K η c D : ℝ}
    (hK : 0 < K) (hη : 0 < η) (hD : 0 < D)
    (hBudget : (Real.log K - Real.log η) / D ≤ c) :
    K * Real.exp (-D * c) ≤ η := by
  have hBudget' : Real.log K - Real.log η ≤ c * D :=
    (div_le_iff₀ hD).mp hBudget
  calc
    K * Real.exp (-D * c) =
        Real.exp (Real.log K) * Real.exp (-D * c) := by
          rw [Real.exp_log hK]
    _ = Real.exp (Real.log K + (-D * c)) := by
      rw [← Real.exp_add]
    _ ≤ Real.exp (Real.log η) := by
      apply Real.exp_le_exp.mpr
      nlinarith
    _ = η := Real.exp_log hη

/-! ## Theory 60 — DEP-R09 Jutila Lemma 4--8 source inventory -/

/- Theory 60, formula 60.1: exact specialization of the explicit
   Ramaré--Zuniga Alterman coefficient at Jutila's actual tau=8/5.
   The external analytic corollary itself is not asserted as a local axiom. -/
noncomputable def jutilaBVActualTau : ℝ := 8 / 5

noncomputable def jutilaBVCorollaryCoefficient (τ : ℝ) : ℝ :=
  (309 / 100) *
    ((1084 / 1000) * (τ + 1) +
      (1301 / 1000) * (1 + τ ^ 2) -
      116 / 1000) / (τ - 1)

theorem jutila_bv_actual_coefficient_value :
    jutilaBVCorollaryCoefficient jutilaBVActualTau =
      18884947 / 500000 := by
  norm_num [jutilaBVCorollaryCoefficient, jutilaBVActualTau]

/- Theory 60, formula 60.5: rational algebra in the finite logarithmic
   ratio. Here u represents log(log D)/log D; no logarithmic source theorem
   is asserted. -/
theorem jutila_bv_actual_log_ratio_identity (u : ℝ) :
    ((11 / 2 : ℝ) + 2 * u) / (4 - 5 / 2) =
      11 / 3 + (4 / 3) * u := by
  ring

/- Theory 60, formula 60.6: the exponent simplification after the source
   definitions are supplied. This checks only the algebraic exponent, not the
   analytic weighted-square-sum corollary or real-power normalization. -/
theorem jutila_bv_actual_power_exponent_identity
    {lam L ell : ℝ} (hL : L ≠ 0) :
    2 * (lam / L) * ((11 / 2) * L + 2 * ell) =
      11 * lam + 4 * lam * ell / L := by
  field_simp
  ring

/-! ## Theory 61 — DEP-R09 Jutila Lemma 5 finite harmonic lower bound -/

/- Theory 61, formula 61.10: the decimal source error coefficient is stored
   as an exact rational. -/
noncomputable def jutilaJL5SourceErrorCoefficient : ℝ := 1277 / 500

theorem jutila_jl5_source_error_coefficient_value :
    jutilaJL5SourceErrorCoefficient = 2554 / 1000 := by
  norm_num [jutilaJL5SourceErrorCoefficient]

/- Theory 61, formula 61.4: drop the nonnegative source constant term and
   retain the adverse sign of the explicit absolute error.  The analytic
   source identity remains a premise rather than a project-local axiom. -/
theorem jutila_jl5_source_lower_transfer
    {S c logR b err E : ℝ}
    (hc : 0 ≤ c) (hb : 0 ≤ b)
    (hIdentity : S = c * (logR + b) + err)
    (hErrorLower : -E ≤ err) :
    c * logR - E ≤ S := by
  nlinarith

/- Theory 61, formula 61.5: a lower bound on the cube-root scale together
   with log R >= 1 pays the requested relative error budget. -/
theorem jutila_jl5_error_budget
    {E rootR η c logR : ℝ}
    (hRoot : 0 < rootR) (hEtaC : 0 < η * c)
    (hRatio : E / (η * c) ≤ rootR)
    (hLog : 1 ≤ logR) :
    E / rootR ≤ η * c * logR := by
  have hE : E ≤ rootR * (η * c) := (div_le_iff₀ hEtaC).mp hRatio
  have hFirst : E / rootR ≤ η * c := by
    apply (div_le_iff₀ hRoot).2
    nlinarith
  calc
    E / rootR ≤ η * c := hFirst
    _ ≤ η * c * logR := by nlinarith

/- Theory 61, formula 61.7: compose the one-sided source estimate with the
   relative error budget. -/
theorem jutila_jl5_relative_lower_transfer
    {S c logR E η : ℝ}
    (hLower : c * logR - E ≤ S)
    (hBudget : E ≤ η * c * logR) :
    (1 - η) * c * logR ≤ S := by
  nlinarith

/- Theory 61, formula 61.8: the local prime factor in Jutila's harmonic
   coefficient dominates the corresponding phi(q)/q factor.  The finite
   Euler-product induction is kept separate from this local kernel fact. -/
theorem jutila_jl5_prime_factor_phi_bridge
    {p : ℝ} (hp : 0 < p) :
    (p - 1) / p ≤ p / (p + 1) := by
  have hp1 : 0 < p + 1 := by linarith
  rw [div_le_div_iff₀ hp hp1]
  nlinarith

theorem jutila_jl5_finite_product_phi_bridge
    (s : Finset ℝ) (hTwo : ∀ p ∈ s, 2 ≤ p) :
    (∏ p ∈ s, (p - 1) / p) ≤
      ∏ p ∈ s, p / (p + 1) := by
  refine Finset.prod_le_prod (fun p hp => ?_) (fun p hp => ?_)
  · have h := hTwo p hp
    exact div_nonneg (by linarith) (by linarith)
  · exact jutila_jl5_prime_factor_phi_bridge (by
      have h := hTwo p hp
      linarith)

/- Theory 61, formula 61.9: once the finite Euler-product bridge and the
   JL5 relative lower bound are supplied, transfer to Jutila's weaker
   phi(q)/q coefficient loses no additional constant. -/
theorem jutila_jl5_downstream_coefficient_transfer
    {S η weak c logR : ℝ}
    (hEta : 0 ≤ 1 - η) (hLog : 0 ≤ logR)
    (hCoefficient : weak ≤ c)
    (hJL5 : (1 - η) * c * logR ≤ S) :
    (1 - η) * weak * logR ≤ S := by
  have hFirst : (1 - η) * weak ≤ (1 - η) * c :=
    mul_le_mul_of_nonneg_left hCoefficient hEta
  exact (mul_le_mul_of_nonneg_right hFirst hLog).trans hJL5

/-! ## Theory 62 — DEP-R09 Jutila Lemma 6 Mellin integral -/

/- Theory 62, formula 62.3: the two real local-factor inequalities used in
   the actual M-polynomial bound.  The complex character factors and finite
   Dirichlet polynomial remain outside this local algebraic statement. -/
theorem jutila_jl6_local_factor_bounds
    {p : ℝ} (hp : 2 ≤ p) :
    p - 1 ≤ p ^ 2 / (p - 1) ∧
      p + 1 ≤ p ^ 2 / (p - 1) := by
  have hpDen : 0 < p - 1 := by linarith
  constructor
  · apply (le_div_iff₀ hpDen).2
    nlinarith [sq_nonneg (p - 1)]
  · apply (le_div_iff₀ hpDen).2
    nlinarith

/- Theory 62, formula 62.5: the squared rational value behind the exceptional
   p=2,3 conductor-to-modulus correction 4/sqrt(6).  This does not formalize
   the external primitive-character factorization. -/
theorem jutila_jl6_imprimitive_correction_squared_rational :
    (4 : ℝ) ^ 2 / 6 = 8 / 3 := by
  norm_num

/- Theory 62, formula 62.7: the real triangle-budget component in
   |1+delta+i(t+u)| <= (9/4)T(1+|u|).  Complex absolute-value reduction is
   deliberately not asserted as an axiom. -/
theorem jutila_jl6_vertical_argument_budget
    {T δ uAbs : ℝ}
    (hT : 1 ≤ T) (hδUpper : δ ≤ 1 / 4)
    (hu : 0 ≤ uAbs) :
    1 + δ + T + uAbs ≤ (9 / 4) * T * (1 + uAbs) := by
  have hTu : uAbs ≤ T * uAbs := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hT) hu]
  have hTnonneg : 0 ≤ T := by linarith
  nlinarith [mul_nonneg hTnonneg hu]

/- Theory 62, formula 62.9: exact algebra in the elementary split of the
   weighted Gamma integral.  The analytic Gamma pointwise bounds themselves
   remain source/direct-proof statements, not local axioms. -/
theorem jutila_jl6_gamma_integral_budget_identity
    {δ rootTwo : ℝ} (hδ : δ ≠ 0) :
    2 * (8 * rootTwo / δ) + 8 * rootTwo =
      8 * rootTwo * (2 / δ + 1) := by
  field_simp

/- Theory 62, formula 62.11: the right-shift chosen for epsilon>0 lies
   strictly between zero and one quarter. -/
noncomputable def jutilaJL6ShiftDelta (ε : ℝ) : ℝ :=
  ε / (4 * (1 + ε))

theorem jutila_jl6_shift_delta_range
    {ε : ℝ} (hε : 0 < ε) :
    0 < jutilaJL6ShiftDelta ε ∧
      jutilaJL6ShiftDelta ε < 1 / 4 := by
  have hOneEps : 0 < 1 + ε := by linarith
  have hDen : 0 < 4 * (1 + ε) := mul_pos (by norm_num) hOneEps
  constructor
  · exact div_pos hε hDen
  · rw [jutilaJL6ShiftDelta, div_lt_iff₀ hDen]
    nlinarith

/- Theory 62, formula 62.12: the finite exponent budget after the source
   power condition is supplied.  This is real algebra only and does not
   formalize Mellin inversion, Rademacher's theorem, or real-power transfer. -/
theorem jutila_jl6_mellin_exponent_budget
    {ε α β : ℝ}
    (hε : 0 < ε) (hα : 1 / 2 ≤ α) (hBeta : α ≤ β) :
    1 - (1 + ε) * (β - jutilaJL6ShiftDelta ε) / α ≤
      -ε / 2 := by
  have hαpos : 0 < α := by linarith
  have hOneEps : 0 < 1 + ε := by linarith
  have hDeltaIdentity :
      (1 + ε) * jutilaJL6ShiftDelta ε = ε / 4 := by
    rw [jutilaJL6ShiftDelta]
    field_simp [ne_of_gt hOneEps]
  have hDeltaOverAlpha :
      (1 + ε) * jutilaJL6ShiftDelta ε / α ≤ ε / 2 := by
    rw [hDeltaIdentity]
    apply (div_le_iff₀ hαpos).2
    nlinarith
  have hNumerator :
      (1 + ε) * (α - jutilaJL6ShiftDelta ε) ≤
        (1 + ε) * (β - jutilaJL6ShiftDelta ε) := by
    exact mul_le_mul_of_nonneg_left
      (sub_le_sub_right hBeta _) hOneEps.le
  calc
    1 - (1 + ε) * (β - jutilaJL6ShiftDelta ε) / α ≤
        1 - (1 + ε) * (α - jutilaJL6ShiftDelta ε) / α := by
          have hDiv := div_le_div_of_nonneg_right hNumerator hαpos.le
          linarith
    _ = -ε + (1 + ε) * jutilaJL6ShiftDelta ε / α := by
      field_simp [ne_of_gt hαpos]
      ring
    _ ≤ -ε / 2 := by linarith

end FGKMTSono
