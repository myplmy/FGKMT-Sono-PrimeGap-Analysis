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
   Ramaré--Zuniga Alterman coefficient at Jutila's p.54 Theorem 1-prime
   tau=8/5.  Theory 66 records that this is not the p.52 equation (3.6) tau.
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

/-! ## Theory 63 — DEP-R09 Jutila Lemma 6 actual truncation tail -/

/- Theory 63, formula 63.6: the last elementary simplification in the
   endpoint-free tail bound.  The preceding divisor, pseudocharacter and
   geometric-series arguments remain direct analytic statements. -/
theorem jutila_jl6_tail_X_plus_one
    {X : ℝ} (hX : 1 ≤ X) :
    X + 1 ≤ 2 * X := by
  linarith

/- Theory 63, formula 63.5: the elementary reciprocal estimate used after
   summing the geometric tail. -/
theorem jutila_jl6_tail_geometric_reciprocal
    {X : ℝ} (hX : 0 < X) :
    (1 - Real.exp (-1 / X))⁻¹ ≤ X + 1 := by
  have hu : 0 < (1 : ℝ) / X := one_div_pos.mpr hX
  have hExpLower : 1 / X ≤ Real.exp (1 / X) - 1 := by
    nlinarith [Real.add_one_le_exp (1 / X)]
  have hExpGt : 1 < Real.exp (1 / X) := by
    simpa using (Real.exp_lt_exp.mpr hu : Real.exp 0 < Real.exp (1 / X))
  have hDen : 0 < Real.exp (1 / X) - 1 := by linarith
  have hMul := mul_le_mul_of_nonneg_left hExpLower hX.le
  have hXne : X ≠ 0 := ne_of_gt hX
  have hOne : 1 ≤ X * (Real.exp (1 / X) - 1) := by
    calc
      1 = X * (1 / X) := by field_simp
      _ ≤ X * (Real.exp (1 / X) - 1) := hMul
  have hInverse : (Real.exp (1 / X) - 1)⁻¹ ≤ X :=
    (inv_le_iff_one_le_mul₀ hDen).2 hOne
  have hExpNe : Real.exp (1 / X) ≠ 0 := ne_of_gt (Real.exp_pos _)
  have hExpSubNe : Real.exp (1 / X) - 1 ≠ 0 := ne_of_gt hDen
  have hIdentity :
      (1 - Real.exp (-1 / X))⁻¹ =
        1 + (Real.exp (1 / X) - 1)⁻¹ := by
    rw [show -1 / X = -(1 / X) by ring, Real.exp_neg]
    field_simp [hExpNe, hExpSubNe]
    ring
  rw [hIdentity]
  linarith

/- Theory 63, formula 63.13: exact exponent sum in Jutila's actual choice
   R=D^epsilon and X=D^(1+12 epsilon). -/
theorem jutila_jl6_tail_actual_exponent_identity (ε : ℝ) :
    ε + (1 + 12 * ε) = 1 + 13 * ε := by
  ring

/- Theory 63, formula 63.9: the linear cutoff converts the mixed quadratic
   exponent into pure Gaussian decay. -/
theorem jutila_jl6_tail_quadratic_decay
    {L a : ℝ} (hL : 0 ≤ L) (hLinear : 2 * a ≤ L) :
    -L ^ 2 + a * L ≤ -L ^ 2 / 2 := by
  have hProduct : 0 ≤ L * (L - 2 * a) :=
    mul_nonneg hL (sub_nonneg.mpr hLinear)
  nlinarith

/- Theory 63, formula 63.9: once the two visible real budgets are supplied,
   the parameterized exponential tail is at most eta. -/
theorem jutila_jl6_tail_budget_transfer
    {η L a : ℝ}
    (hη : 0 < η) (hL : 0 ≤ L)
    (hLinear : 2 * a ≤ L)
    (hQuadratic : 2 * Real.log (4 / η) ≤ L ^ 2) :
    4 * Real.exp (-L ^ 2 + a * L) ≤ η := by
  have hDecay := jutila_jl6_tail_quadratic_decay hL hLinear
  have hExponent :
      -L ^ 2 + a * L ≤ -Real.log (4 / η) := by
    nlinarith
  have hRatio : 0 < (4 : ℝ) / η := div_pos (by norm_num) hη
  calc
    4 * Real.exp (-L ^ 2 + a * L) ≤
        4 * Real.exp (-Real.log (4 / η)) := by
          exact mul_le_mul_of_nonneg_left
            (Real.exp_le_exp.mpr hExponent) (by norm_num)
    _ = η := by
      rw [Real.exp_neg, Real.exp_log hRatio]
      field_simp [ne_of_gt hη]

/- Theory 63, formula 63.11: the displayed max/square-root cutoff implies
   the two hypotheses of the preceding budget theorem. -/
theorem jutila_jl6_tail_sufficient_cutoff
    {η L a : ℝ}
    (hη : 0 < η) (hηUpper : η ≤ 4) (ha : 0 ≤ a)
    (hCutoff :
      max (2 * a) (Real.sqrt (2 * Real.log (4 / η))) ≤ L) :
    4 * Real.exp (-L ^ 2 + a * L) ≤ η := by
  have hRatioOne : 1 ≤ (4 : ℝ) / η := by
    exact (le_div_iff₀ hη).2 (by simpa using hηUpper)
  have hLog : 0 ≤ Real.log (4 / η) := Real.log_nonneg hRatioOne
  have hInside : 0 ≤ 2 * Real.log (4 / η) := by positivity
  have hLinear : 2 * a ≤ L :=
    (le_max_left (2 * a) (Real.sqrt (2 * Real.log (4 / η)))).trans hCutoff
  have hSqrt : Real.sqrt (2 * Real.log (4 / η)) ≤ L :=
    (le_max_right (2 * a) (Real.sqrt (2 * Real.log (4 / η)))).trans hCutoff
  have hL : 0 ≤ L := by
    have hTwoA : 0 ≤ 2 * a := by positivity
    exact hTwoA.trans hLinear
  have hSum :
      0 ≤ L + Real.sqrt (2 * Real.log (4 / η)) := by positivity
  have hProduct :
      0 ≤
        (L - Real.sqrt (2 * Real.log (4 / η))) *
          (L + Real.sqrt (2 * Real.log (4 / η))) :=
    mul_nonneg (sub_nonneg.mpr hSqrt) hSum
  have hSqrtSquare :
      (Real.sqrt (2 * Real.log (4 / η))) ^ 2 =
        2 * Real.log (4 / η) := Real.sq_sqrt hInside
  have hQuadratic : 2 * Real.log (4 / η) ≤ L ^ 2 := by
    nlinarith
  exact jutila_jl6_tail_budget_transfer hη hL hLinear hQuadratic

/-! ## Theory 64 — DEP-R09 Jutila Lemma 6 actual common budget -/

/- Theory 64, formula 64.11: Jutila's actual p.52 exponents satisfy the
   original power condition throughout 0 <= theta <= 1/21. -/
theorem jutila_jl6_actual_power_margin
    {θ : ℝ} (hθ : 0 ≤ θ) (hθUpper : θ ≤ 1 / 21) :
    (1 - θ) * (1 + 12 * θ) ≥
      (1 + θ) * (1 + 9 * θ) := by
  have hSecond : 0 ≤ 1 - 21 * θ := by
    nlinarith
  have hProduct : 0 ≤ θ * (1 - 21 * θ) :=
    mul_nonneg hθ hSecond
  nlinarith

/- Theory 64, formula 64.8: multiplying the JL5 and damping factors costs
   at most the sum of their two nonnegative losses. -/
theorem jutila_jl6_damping_product_budget
    {η5 ηX : ℝ} (hη5 : 0 ≤ η5) (hηX : 0 ≤ ηX) :
    1 - η5 - ηX ≤ (1 - η5) * (1 - ηX) := by
  nlinarith [mul_nonneg hη5 hηX]

/- Theory 64, formulas 64.3--64.9: once the source identity and all four
   normalized component bounds are supplied, the final detector coefficient
   loses no more than the allocated sum.  The analytic premises are explicit
   arguments rather than project-local axioms. -/
theorem jutila_jl6_four_part_budget_transfer
    {η5 ηX ηM ηT ηOut C M IAbs tailAbs gAbs : ℝ}
    (hC : 0 ≤ C)
    (hMain : (1 - η5 - ηX) * C ≤ M)
    (hMellin : IAbs ≤ ηM * C)
    (hTail : tailAbs ≤ ηT * C)
    (hTriangle : M - IAbs - tailAbs ≤ gAbs)
    (hBudget : η5 + ηX + ηM + ηT ≤ ηOut) :
    (1 - ηOut) * C ≤ gAbs := by
  have hLoss :
      (1 - ηOut) * C ≤
        (1 - η5 - ηX - ηM - ηT) * C := by
    exact mul_le_mul_of_nonneg_right (by linarith) hC
  nlinarith

/- Theory 64, formula 64.3: etaOut <= theta recovers Jutila's printed
   (1-theta) coefficient from the stronger common-budget output. -/
theorem jutila_jl6_output_recovers_source_coefficient
    {ηOut θ C : ℝ} (hC : 0 ≤ C) (hOut : ηOut ≤ θ) :
    (1 - θ) * C ≤ (1 - ηOut) * C := by
  exact mul_le_mul_of_nonneg_right (by linarith) hC

/- Theory 64, formulas 64.18--64.19: after the elementary B_q exponent is
   at most theta*L/6, it combines with R^(-1/3) to leave
   exp(-theta*L/6).  The prime-product and root cutoff are not asserted here. -/
theorem jutila_jl6_B_exponent_absorption
    {b θ L : ℝ} (hB : b ≤ θ * L / 6) :
    b - θ * L / 3 ≤ -θ * L / 6 := by
  linarith

/-! ## Theory 65 — DEP-R09 Jutila Lemma 8 actual local zero count -/

/- Theory 65, formula 65.3: McCurley's exact kappa is strictly below the
   rational upper 3/10 used in the local-count terminal budget. -/
noncomputable def jutilaJL8Kappa : ℝ :=
  (5 - Real.sqrt 5) / 10

theorem jutila_jl8_kappa_lt_three_tenths :
    jutilaJL8Kappa < 3 / 10 := by
  have hSqrtPos : 0 < Real.sqrt (5 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  have hSqrtSquare : (Real.sqrt (5 : ℝ)) ^ 2 = 5 :=
    Real.sq_sqrt (by norm_num)
  have hSqrtTwo : 2 < Real.sqrt (5 : ℝ) := by
    nlinarith
  rw [jutilaJL8Kappa]
  norm_num
  linarith

theorem jutila_jl8_sigma_one_gt_three_halves
    {sigma : ℝ} (hSigma : 1 < sigma) :
    3 / 2 < (1 + Real.sqrt (1 + 4 * sigma ^ 2)) / 2 := by
  have hSigmaSquare : 1 < sigma ^ 2 := by nlinarith
  have hArgument : 4 < 1 + 4 * sigma ^ 2 := by nlinarith
  have hArgumentNonneg : 0 ≤ 1 + 4 * sigma ^ 2 := by positivity
  have hSqrtNonneg : 0 ≤ Real.sqrt (1 + 4 * sigma ^ 2) :=
    Real.sqrt_nonneg _
  have hSqrtSquare : (Real.sqrt (1 + 4 * sigma ^ 2)) ^ 2 =
      1 + 4 * sigma ^ 2 := Real.sq_sqrt hArgumentNonneg
  have hSqrtTwo : 2 < Real.sqrt (1 + 4 * sigma ^ 2) := by
    nlinarith
  linarith

/- Theory 65, formula 65.12: the first pole in F(s,rho) contributes at
   least 8/(17r) throughout the local square. -/
theorem jutila_jl8_first_pole_lower
    {r a y : ℝ}
    (hr : 0 < r) (haLower : r ≤ a) (haUpper : a ≤ 2 * r)
    (hy : y ^ 2 ≤ r ^ 2 / 4) :
    8 / (17 * r) ≤ a / (a ^ 2 + y ^ 2) := by
  have haPos : 0 < a := lt_of_lt_of_le hr haLower
  have hDen : 0 < a ^ 2 + y ^ 2 := by
    nlinarith [sq_pos_of_pos haPos, sq_nonneg y]
  have hSecond : 0 ≤ 8 * a - r := by
    nlinarith
  have hFirst : 0 ≤ 2 * r - a := by
    linarith
  have hProduct : 0 ≤ (2 * r - a) * (8 * a - r) :=
    mul_nonneg hFirst hSecond
  have hNumerator : 8 * (a ^ 2 + y ^ 2) ≤ 17 * r * a := by
    nlinarith
  rw [div_le_div_iff₀ (by positivity : 0 < 17 * r) hDen]
  simpa [mul_assoc, mul_comm, mul_left_comm] using hNumerator

/- Theory 65, formula 65.13: the two shifted reciprocal components have
   total real part below 3 on the actual near-one square. -/
theorem jutila_jl8_shifted_F_coarse_upper
    {r sigmaOne beta y : ℝ}
    (hr : 0 < r) (hrUpper : r ≤ 1 / 21)
    (hSigmaOne : 3 / 2 < sigmaOne)
    (hBetaLower : 1 - r ≤ beta) (hBetaUpper : beta ≤ 1) :
    (sigmaOne - beta) /
          ((sigmaOne - beta) ^ 2 + y ^ 2) +
        (sigmaOne - 1 + beta) /
          ((sigmaOne - 1 + beta) ^ 2 + y ^ 2) < 3 := by
  let d₁ := sigmaOne - beta
  let d₂ := sigmaOne - 1 + beta
  have hd₁Half : 1 / 2 < d₁ := by
    dsimp [d₁]
    linarith
  have hd₂One : 1 < d₂ := by
    dsimp [d₂]
    linarith
  have hd₁ : 0 < d₁ := by linarith
  have hd₂ : 0 < d₂ := by linarith
  have hsq₁ : 0 < d₁ ^ 2 := sq_pos_of_pos hd₁
  have hsq₂ : 0 < d₂ ^ 2 := sq_pos_of_pos hd₂
  have hden₁ : 0 < d₁ ^ 2 + y ^ 2 := by positivity
  have hden₂ : 0 < d₂ ^ 2 + y ^ 2 := by positivity
  have hcomp₁ : d₁ / (d₁ ^ 2 + y ^ 2) ≤ 1 / d₁ := by
    rw [div_le_iff₀ hden₁]
    field_simp [ne_of_gt hd₁]
    nlinarith [sq_nonneg y]
  have hcomp₂ : d₂ / (d₂ ^ 2 + y ^ 2) ≤ 1 / d₂ := by
    rw [div_le_iff₀ hden₂]
    field_simp [ne_of_gt hd₂]
    nlinarith [sq_nonneg y]
  have hrecip₁ : 1 / d₁ < 2 := by
    rw [div_lt_iff₀ hd₁]
    linarith
  have hrecip₂ : 1 / d₂ < 1 := by
    rw [div_lt_iff₀ hd₂]
    linarith
  change d₁ / (d₁ ^ 2 + y ^ 2) + d₂ / (d₂ ^ 2 + y ^ 2) < 3
  linarith

/- Theory 65, formula 65.14: after the shifted F term costs at most 3/2,
   r<=1/21 leaves normalized Stechkin kernel at least 3/8.  The analytic
   identification of `first` and `cost` is intentionally not axiomatized. -/
theorem jutila_jl8_normalized_kernel_lower
    {r first cost : ℝ}
    (hr : 0 < r) (hrUpper : r ≤ 1 / 21)
    (hFirst : 8 / 17 ≤ r * first) (hCost : cost ≤ 3 / 2) :
    3 / 8 ≤ r * (first - cost) := by
  have hCostScaled : r * cost ≤ r * (3 / 2) :=
    mul_le_mul_of_nonneg_left hCost hr.le
  nlinarith

theorem jutila_jl8_kernel_exact_slack :
    (8 : ℝ) / 17 - 3 / 42 - 3 / 8 = 23 / 952 ∧
      0 < (23 : ℝ) / 952 := by
  norm_num

theorem jutila_jl8_kernel_reciprocal_form
    {r kernel : ℝ} (hr : 0 < r)
    (hNormalized : 3 / 8 ≤ r * kernel) :
    3 / (8 * r) ≤ kernel := by
  apply (div_le_iff₀ (by positivity : 0 < 8 * r)).2
  nlinarith

/- Theory 65, formulas 65.16--65.17: the source upper sum, once multiplied
   by r, implies N<3+rL with the printed 0.3918 gamma constant. -/
theorem jutila_jl8_local_count_transfer
    {N r L κ : ℝ}
    (hr : 0 < r) (hrUpper : r ≤ 1 / 21)
    (hL : 0 ≤ L) (hKappa : κ ≤ 3 / 10)
    (hCount :
      3 * N / 8 < 1 + κ * r * L + (1959 / 5000) * r) :
    N < 3 + r * L := by
  have hRL : 0 ≤ r * L := mul_nonneg hr.le hL
  have hKappaTerm : κ * (r * L) ≤ (3 / 10) * (r * L) :=
    mul_le_mul_of_nonneg_right hKappa hRL
  have hRemainder :
      (1959 / 5000) * r ≤ (1959 / 5000) * (1 / 21) := by
    exact mul_le_mul_of_nonneg_left hrUpper (by norm_num)
  nlinarith

theorem jutila_jl8_constant_exact_slack :
    0 <
      (3 : ℝ) - 8 / 3 -
        (8 / 3) * (1959 / 5000) * (1 / 21) := by
  norm_num

/- Theory 65, formula 65.19: the strip radius max(delta,Delta) remains in
   McCurley's near-one range once Delta<=theta^2. -/
theorem jutila_jl8_actual_radius_gate
    {θ δ Δ : ℝ}
    (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21)
    (hδ : δ ≤ θ) (hΔ : Δ ≤ θ ^ 2) :
    max δ Δ ≤ θ ∧ max δ Δ ≤ 1 / 21 := by
  have hθOne : θ ≤ 1 := by linarith
  have hSquare : θ ^ 2 ≤ θ := by
    nlinarith
  have hMax : max δ Δ ≤ θ := max_le hδ (hΔ.trans hSquare)
  exact ⟨hMax, hMax.trans hθUpper⟩

/- Theory 65, formula 65.20: the actual strip centre satisfies the stated
   height-log envelope. -/
theorem jutila_jl8_height_log_upper
    {q T t : ℝ} (hq : 0 < q) (hT : 1 ≤ T) (ht : |t| ≤ T) :
    Real.log (q * (1 + |t|)) ≤ Real.log (2 * (q * T)) := by
  have honeAbs : 0 < 1 + |t| := by positivity
  have hProductPos : 0 < q * (1 + |t|) := mul_pos hq honeAbs
  have hOnePlus : 1 + |t| ≤ 2 * T := by linarith
  have hProduct : q * (1 + |t|) ≤ 2 * (q * T) := by
    calc
      q * (1 + |t|) ≤ q * (2 * T) :=
        mul_le_mul_of_nonneg_left hOnePlus hq.le
      _ = 2 * (q * T) := by ring
  exact Real.log_le_log hProductPos hProduct

/- Theory 65, formula 65.21: at most two parity systems and a uniform
   nonnegative local bound B give the final strip-to-J factor 2BJ. -/
theorem jutila_jl8_even_odd_cell_transfer
    {N B cells J : ℝ}
    (hB : 0 ≤ B) (hN : N ≤ B * cells) (hCells : cells ≤ 2 * J) :
    N ≤ 2 * B * J := by
  calc
    N ≤ B * cells := hN
    _ ≤ B * (2 * J) := mul_le_mul_of_nonneg_left hCells hB
    _ = 2 * B * J := by ring

/-! ## Theory 66 — DEP-R09 Jutila JL7 and equation (3.6) parameter repair -/

/- Theory 66, formula 66.3: the p.52 Theorem 1 density branch has a
   theta-dependent tau.  The fixed tau=8/5 in Theory 60 belongs only to the
   separate p.54 Theorem 1-prime branch. -/
noncomputable def jutilaT1DensityTau (θ : ℝ) : ℝ :=
  (1 + 16 * θ) / (1 + 14 * θ)

theorem jutila_t1_density_tau_sub_one
    {θ : ℝ} (hθ : 0 < θ) :
    jutilaT1DensityTau θ - 1 = 2 * θ / (1 + 14 * θ) := by
  have hDen : 1 + 14 * θ ≠ 0 := by nlinarith
  rw [jutilaT1DensityTau]
  field_simp
  ring

/- Theory 66, formula 66.4: exact rational specialization of the
   Ramaré--Zuniga coefficient at the corrected theta-dependent tau. -/
theorem jutila_t1_density_bv_coefficient_identity
    {θ : ℝ} (hθ : 0 < θ) :
    jutilaBVCorollaryCoefficient (jutilaT1DensityTau θ) =
      (309 / 200) *
        ((2327 / 500) + (34421 / 250) * θ + (255149 / 250) * θ ^ 2) /
          (θ * (1 + 14 * θ)) := by
  have hθNe : θ ≠ 0 := ne_of_gt hθ
  have hDen : 1 + 14 * θ ≠ 0 := by nlinarith
  have hTau : jutilaT1DensityTau θ - 1 ≠ 0 := by
    rw [jutila_t1_density_tau_sub_one hθ]
    positivity
  rw [jutilaBVCorollaryCoefficient, jutila_t1_density_tau_sub_one hθ,
    jutilaT1DensityTau]
  field_simp [hθNe, hDen, hTau]
  ring

/- Theory 66, formulas 66.5--66.6: the corrected coefficient is strictly
   below 13/theta throughout the actual interval. -/
theorem jutila_t1_density_bv_coefficient_lt
    {θ : ℝ} (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21) :
    (309 / 200) *
          ((2327 / 500) + (34421 / 250) * θ + (255149 / 250) * θ ^ 2) /
        (θ * (1 + 14 * θ)) <
      13 / θ := by
  have hDenFactor : 0 < 1 + 14 * θ := by nlinarith
  have hDen : 0 < θ * (1 + 14 * θ) := mul_pos hθ hDenFactor
  have hSquare : θ ^ 2 ≤ θ / 21 := by
    have hProduct : 0 ≤ θ * (1 / 21 - θ) :=
      mul_nonneg hθ.le (sub_nonneg.mpr hθUpper)
    nlinarith
  have hCore :
      (309 / 200) *
          ((2327 / 500) + (34421 / 250) * θ + (255149 / 250) * θ ^ 2) <
        13 * (1 + 14 * θ) := by
    nlinarith
  calc
    (309 / 200) *
          ((2327 / 500) + (34421 / 250) * θ + (255149 / 250) * θ ^ 2) /
        (θ * (1 + 14 * θ)) <
        (13 * (1 + 14 * θ)) / (θ * (1 + 14 * θ)) :=
      div_lt_div_of_pos_right hCore hDen
    _ = 13 / θ := by field_simp

/- Theory 66, formulas 66.7--66.8: after writing ell=log(log D), the
   finite logarithmic ratio is at most 18/(7 theta). -/
theorem jutila_t1_density_log_ratio_identity
    {θ L ell : ℝ} (hθ : 0 < θ) (hL : 0 < L) :
    ((1 + 12 * θ) * L + 2 * ell) / (θ * L) =
      1 / θ + 12 + 2 * ell / (θ * L) := by
  field_simp [ne_of_gt hθ, ne_of_gt hL]

theorem jutila_t1_density_log_ratio_upper
    {θ L ell : ℝ}
    (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21)
    (hL : 0 < L) (hLog : 2 * ell ≤ L) :
    1 / θ + 12 + 2 * ell / (θ * L) ≤ 18 / (7 * θ) := by
  have hTerm : 2 * ell / (θ * L) ≤ 1 / θ := by
    rw [div_le_div_iff₀ (mul_pos hθ hL) hθ]
    nlinarith
  have hTwelve : 12 ≤ 4 / (7 * θ) := by
    rw [le_div_iff₀ (by positivity : 0 < 7 * θ)]
    nlinarith
  calc
    1 / θ + 12 + 2 * ell / (θ * L) ≤
        1 / θ + 12 + 1 / θ :=
      by
        simpa [add_assoc, add_comm, add_left_comm] using
          add_le_add_left hTerm (1 / θ + 12)
    _ = 2 / θ + 12 := by ring
    _ ≤ 2 / θ + 4 / (7 * θ) := by linarith
    _ = 18 / (7 * θ) := by field_simp; ring

/- Theory 66, formula 66.9: abstract multiplication of the two strict
   coefficient envelopes.  The analytic source corollary remains external. -/
theorem jutila_t1_density_bv_log_product_upper
    {θ K ratio : ℝ}
    (hθ : 0 < θ) (hRatio : 0 < ratio)
    (hKUpper : K < 13 / θ)
    (hRatioUpper : ratio ≤ 18 / (7 * θ)) :
    K * ratio < 34 / θ ^ 2 := by
  have hFirst : K * ratio < (13 / θ) * ratio :=
    mul_lt_mul_of_pos_right hKUpper hRatio
  have hCoeff : 0 ≤ 13 / θ := by positivity
  have hSecond : (13 / θ) * ratio ≤ (13 / θ) * (18 / (7 * θ)) :=
    mul_le_mul_of_nonneg_left hRatioUpper hCoeff
  have hExact : (13 / θ) * (18 / (7 * θ)) < 34 / θ ^ 2 := by
    have hθNe : θ ≠ 0 := ne_of_gt hθ
    field_simp
    nlinarith [sq_pos_of_pos hθ]
  exact hFirst.trans_le hSecond |>.trans hExact

/- Theory 66, formula 66.11: exact elementary exponential slacks behind
   the two-case denominator bound. -/
theorem jutila_exp_neg_half_gt_three_fifths :
    (3 : ℝ) / 5 < Real.exp (-1 / 2) := by
  have hSquare : (Real.exp (-1 / 2)) ^ 2 = Real.exp (-1) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hExpLower : (9 : ℝ) / 25 < Real.exp (-1) :=
    (by norm_num : (9 : ℝ) / 25 < 0.36787944116).trans
      Real.exp_neg_one_gt_d9
  have hPos : 0 < Real.exp (-1 / 2) := Real.exp_pos _
  nlinarith

theorem jutila_exp_neg_one_between_rationals :
    (9 : ℝ) / 25 < Real.exp (-1) ∧ Real.exp (-1) < 2 / 5 := by
  constructor
  · exact (by norm_num : (9 : ℝ) / 25 < 0.36787944116).trans
      Real.exp_neg_one_gt_d9
  · exact Real.exp_neg_one_lt_d9.trans (by norm_num)

theorem jutila_weight_denominator_two_slacks :
    (1 : ℝ) / 5 < Real.exp (-1 / 2) - Real.exp (-1) ∧
      (1 : ℝ) / 5 < Real.exp (-1) - Real.exp (-2) := by
  rcases jutila_exp_neg_one_between_rationals with ⟨hLower, hUpper⟩
  constructor
  · linarith [jutila_exp_neg_half_gt_three_fifths]
  · have hPos : 0 < Real.exp (-1) := Real.exp_pos _
    have hOneMinus : (3 : ℝ) / 5 < 1 - Real.exp (-1) := by linarith
    have hProductOne :
        (9 / 25 : ℝ) * (3 / 5) < Real.exp (-1) * (3 / 5) :=
      mul_lt_mul_of_pos_right hLower (by norm_num)
    have hProductTwo :
        Real.exp (-1) * (3 / 5) <
          Real.exp (-1) * (1 - Real.exp (-1)) :=
      mul_lt_mul_of_pos_left hOneMinus hPos
    have hExpTwo : Real.exp (-2) = (Real.exp (-1)) ^ 2 := by
      rw [pow_two, ← Real.exp_add]
      congr 1
      ring
    rw [hExpTwo]
    nlinarith

theorem jutila_weight_quotient_lt_five
    {numerator denominator : ℝ}
    (hNumerator : numerator ≤ 1)
    (hDenominator : 1 / 5 < denominator) :
    numerator / denominator < 5 := by
  have hDenPos : 0 < denominator := by linarith
  rw [div_lt_iff₀ hDenPos]
  nlinarith

/- Theory 66, formula 66.12: the normalized integration area is at least
   theta^2/2 once the displayed positive factors are supplied. -/
theorem jutila_t1_density_integration_area_lower
    {θ L ell : ℝ} (hθ : 0 < θ) (hL : 0 < L) (hEll : 0 ≤ ell) :
    θ ^ 2 / 2 ≤
      θ ^ 2 * (1 / 2 + 7 * θ) * (1 + 12 * θ + 2 * ell / L) := by
  have hThetaSquare : 0 ≤ θ ^ 2 := sq_nonneg θ
  have hFirst : 1 / 2 ≤ 1 / 2 + 7 * θ := by linarith
  have hEllTerm : 0 ≤ 2 * ell / L := div_nonneg (by positivity) hL.le
  have hSecond : 1 ≤ 1 + 12 * θ + 2 * ell / L := by linarith
  have hA : θ ^ 2 / 2 ≤ θ ^ 2 * (1 / 2 + 7 * θ) := by
    nlinarith
  have hNonneg : 0 ≤ θ ^ 2 * (1 / 2 + 7 * θ) := by positivity
  calc
    θ ^ 2 / 2 ≤ θ ^ 2 * (1 / 2 + 7 * θ) := hA
    _ ≤ θ ^ 2 * (1 / 2 + 7 * θ) *
          (1 + 12 * θ + 2 * ell / L) := by
      nlinarith [mul_nonneg hNonneg (sub_nonneg.mpr hSecond)]

/- Theory 66, formulas 66.15--66.16: exact off-diagonal exponent and its
   uniform negative margin on 0<theta<=1/21. -/
theorem jutila_t1_off_diagonal_exponent_identity (θ : ℝ) :
    2 * θ * (1 + 12 * θ) + 1 / 2 -
          (1 / 2 + 7 * θ) * (1 - θ) ^ 2 + 2 * θ =
      -2 * θ + (75 / 2) * θ ^ 2 - 7 * θ ^ 3 := by
  ring

theorem jutila_t1_off_diagonal_base_margin
    {θ : ℝ} (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21) :
    -2 * θ + (75 / 2) * θ ^ 2 - 7 * θ ^ 3 ≤
      -(29 / 126) * θ := by
  have hBracket : 0 ≤ 75 / 2 - 7 * (θ + 1 / 21) := by
    nlinarith
  have hProduct :
      0 ≤ (1 / 21 - θ) * (75 / 2 - 7 * (θ + 1 / 21)) :=
    mul_nonneg (sub_nonneg.mpr hθUpper) hBracket
  have hInner : -2 + (75 / 2) * θ - 7 * θ ^ 2 ≤ -(29 / 126) := by
    nlinarith
  have hScaled := mul_le_mul_of_nonneg_left hInner hθ.le
  nlinarith

/- Theory 66, formula 66.17: the finite log(log D)/log D gate preserves
   half of the negative exponent margin. -/
theorem jutila_t1_off_diagonal_total_margin
    {θ L ell : ℝ}
    (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21)
    (_hL : 0 < L) (hGate : 4 * ell / L ≤ 29 / 252) :
    (-2 * θ + (75 / 2) * θ ^ 2 - 7 * θ ^ 3) +
        4 * θ * ell / L ≤
      -(29 / 252) * θ := by
  have hBase := jutila_t1_off_diagonal_base_margin hθ hθUpper
  have hScaled : 4 * θ * ell / L ≤ (29 / 252) * θ := by
    have h := mul_le_mul_of_nonneg_left hGate hθ.le
    simpa [div_eq_mul_inv, mul_assoc, mul_left_comm, mul_comm] using h
  nlinarith

/- Theory 66, formula 66.19: fail-closed terminal absorption.  The source
   contour and residue multipliers must be supplied as finite A,B,E inputs;
   this theorem does not invent them. -/
theorem jutila_t1_terminal_absorption
    {A B E J Y : ℝ}
    (hGap : 0 < A - E) (hJ : 0 < J)
    (hInequality : A * J ^ 2 ≤ B * J * Y + E * J ^ 2) :
    J ≤ B * Y / (A - E) := by
  have hMultiplied : J * ((A - E) * J) ≤ J * (B * Y) := by
    nlinarith
  have hCancelled : (A - E) * J ≤ B * Y :=
    le_of_mul_le_mul_left hMultiplied hJ
  rw [le_div_iff₀ hGap]
  simpa [mul_comm] using hCancelled

/-! ## Theory 67 — DEP-R09 Jutila JL7 shifted-contour multiplier -/

/- Theory 67, formula 67.2: the actual real part on the shifted contour lies
   in (0,1/7].  This is finite real algebra, not the contour-shift theorem. -/
theorem jutila_jl7_shifted_real_part_range
    {θ u : ℝ}
    (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21)
    (hu : 0 ≤ u) (huUpper : u ≤ 2 * θ) :
    0 < θ + u ∧ θ + u ≤ 1 / 7 := by
  constructor <;> nlinarith

/- Theory 67, formula 67.4: the real triangle budget behind
   |1+z| <= (22/7)T(1+|y|).  Complex absolute-value reduction remains in the
   source/direct proof and is not introduced as a local axiom. -/
theorem jutila_jl7_vertical_argument_budget
    {θ T v y : ℝ}
    (hθ : 0 < θ) (hθUpper : θ ≤ 1 / 21)
    (hT : 1 ≤ T) (hv : |v| ≤ 2 * T) :
    1 + 3 * θ + |v + y| ≤ (22 / 7) * T * (1 + |y|) := by
  have hAbs : |v + y| ≤ |v| + |y| := abs_add_le v y
  have hy : 0 ≤ |y| := abs_nonneg y
  have hTnonneg : 0 ≤ T := by linarith
  have hTy : |y| ≤ T * |y| := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hT) hy]
  nlinarith [mul_nonneg hTnonneg hy]

/- Theory 67, formula 67.10: squared principal-character ratio.  Keeping the
   numerator and denominator together prevents a spurious extra height loss. -/
theorem jutila_jl7_principal_ratio_squared
    {σ t : ℝ} (_hσ : 0 ≤ σ) (hσUpper : σ ≤ 1 / 7) :
    9 * ((1 + σ) ^ 2 + t ^ 2) ≤
      16 * ((1 - σ) ^ 2 + t ^ 2) := by
  have hFirst : 0 ≤ 1 - 7 * σ := by nlinarith
  have hSecond : 0 ≤ 7 - σ := by nlinarith
  have hProduct : 0 ≤ (1 - 7 * σ) * (7 - σ) :=
    mul_nonneg hFirst hSecond
  nlinarith [sq_nonneg t]

/- Auxiliary kernel lemmas for Theory 67 formulas 67.7 and 67.11. -/
theorem jutila_jl7_sqrt_six_gt_twelve_fifths :
    (12 : ℝ) / 5 < Real.sqrt 6 := by
  have hSq : (Real.sqrt (6 : ℝ)) ^ 2 = 6 :=
    Real.sq_sqrt (by norm_num)
  have hNonneg : 0 ≤ Real.sqrt (6 : ℝ) := Real.sqrt_nonneg _
  nlinarith

theorem jutila_jl7_sqrt_eighteen_gt_four :
    (4 : ℝ) < Real.sqrt 18 := by
  have hSq : (Real.sqrt (18 : ℝ)) ^ 2 = 18 :=
    Real.sq_sqrt (by norm_num)
  have hNonneg : 0 ≤ Real.sqrt (18 : ℝ) := Real.sqrt_nonneg _
  nlinarith

theorem jutila_jl7_ratio_radicand_lt_nine_sixteenths :
    (11 : ℝ) / (7 * Real.pi) < 9 / 16 := by
  have hPi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have hDen : 0 < 7 * Real.pi := by positivity
  rw [div_lt_iff₀ hDen]
  nlinarith

theorem jutila_jl7_ratio_sqrt_lt_three_fourths :
    Real.sqrt ((11 : ℝ) / (7 * Real.pi)) < 3 / 4 := by
  have hInside : 0 ≤ (11 : ℝ) / (7 * Real.pi) := by positivity
  have hSq : (Real.sqrt ((11 : ℝ) / (7 * Real.pi))) ^ 2 =
      (11 : ℝ) / (7 * Real.pi) := Real.sq_sqrt hInside
  have hNonneg : 0 ≤ Real.sqrt ((11 : ℝ) / (7 * Real.pi)) :=
    Real.sqrt_nonneg _
  nlinarith [jutila_jl7_ratio_radicand_lt_nine_sixteenths]

/- Theory 67, formula 67.7: exact nonprincipal coefficient is below 9/4. -/
theorem jutila_jl7_nonprincipal_coefficient_lt :
    (4 : ℝ) / Real.sqrt 18 +
        (4 / Real.sqrt 6) * Real.sqrt (11 / (7 * Real.pi)) < 9 / 4 := by
  have hSqrt18 : 0 < Real.sqrt (18 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  have hSqrt6 : 0 < Real.sqrt (6 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  have hFirst : (4 : ℝ) / Real.sqrt 18 < 1 := by
    rw [div_lt_one hSqrt18]
    exact jutila_jl7_sqrt_eighteen_gt_four
  have hFourOverSix : (4 : ℝ) / Real.sqrt 6 < 5 / 3 := by
    rw [div_lt_iff₀ hSqrt6]
    nlinarith [jutila_jl7_sqrt_six_gt_twelve_fifths]
  have hRatioPos : 0 < Real.sqrt ((11 : ℝ) / (7 * Real.pi)) := by positivity
  have hProduct :
      (4 / Real.sqrt 6) * Real.sqrt (11 / (7 * Real.pi)) < 5 / 4 := by
    calc
      (4 / Real.sqrt 6) * Real.sqrt (11 / (7 * Real.pi)) <
          (5 / 3) * Real.sqrt (11 / (7 * Real.pi)) :=
        mul_lt_mul_of_pos_right hFourOverSix hRatioPos
      _ < (5 / 3) * (3 / 4) :=
        mul_lt_mul_of_pos_left jutila_jl7_ratio_sqrt_lt_three_fourths
          (by norm_num)
      _ = 5 / 4 := by norm_num
  nlinarith

/- Theory 67, formula 67.11: exact principal coefficient is below 12. -/
theorem jutila_jl7_principal_coefficient_lt :
    (16 : ℝ) / Real.sqrt 6 *
        (1 + Real.sqrt (11 / (7 * Real.pi))) < 12 := by
  have hSqrt6 : 0 < Real.sqrt (6 : ℝ) := Real.sqrt_pos.2 (by norm_num)
  have hFirst : (16 : ℝ) / Real.sqrt 6 < 20 / 3 := by
    rw [div_lt_iff₀ hSqrt6]
    nlinarith [jutila_jl7_sqrt_six_gt_twelve_fifths]
  have hSecondPos : 0 < 1 + Real.sqrt ((11 : ℝ) / (7 * Real.pi)) := by
    positivity
  have hSecond : 1 + Real.sqrt ((11 : ℝ) / (7 * Real.pi)) < 7 / 4 := by
    nlinarith [jutila_jl7_ratio_sqrt_lt_three_fourths]
  calc
    (16 / Real.sqrt 6) * (1 + Real.sqrt (11 / (7 * Real.pi))) <
        (20 / 3) * (1 + Real.sqrt (11 / (7 * Real.pi))) :=
      mul_lt_mul_of_pos_right hFirst hSecondPos
    _ < (20 / 3) * (7 / 4) :=
      mul_lt_mul_of_pos_left hSecond (by norm_num)
    _ < 12 := by norm_num

/- Theory 67, formula 67.12: once one of the two source branch estimates is
   supplied, the common coefficient 12 is a valid finite envelope. -/
theorem jutila_jl7_uniform_branch_composition
    {value zeta scale : ℝ}
    (hzeta : 0 ≤ zeta) (hscale : 0 ≤ scale)
    (hBranch : value ≤ (9 / 4) * zeta * scale ∨
      value ≤ 12 * zeta * scale) :
    value ≤ 12 * zeta * scale := by
  rcases hBranch with hBranch | hBranch
  · have hZS : 0 ≤ zeta * scale := mul_nonneg hzeta hscale
    have hCoeff : (9 / 4 : ℝ) ≤ 12 := by norm_num
    exact hBranch.trans (by nlinarith)
  · exact hBranch

/- Theory 67, formula 67.13: abstract triangle component of the negative-real
   power difference.  The complex-power modulus identity remains external. -/
theorem jutila_jl7_power_difference_triangle
    {small large : ℝ} (hsmall : 0 ≤ small) (hsmallLarge : small ≤ large) :
    |small - large| ≤ 2 * large := by
  rw [abs_of_nonpos (sub_nonpos.mpr hsmallLarge)]
  nlinarith

/- Theory 67, formula 67.15: finite coefficient multiplication after the
   source L-bound, power bound and Gamma integral have been supplied. -/
theorem jutila_jl7_contour_coefficient_identity
    {θ zeta : ℝ} (hθ : θ ≠ 0) :
    (1 / (2 * Real.pi)) * (12 * zeta) * 2 *
          (8 * Real.sqrt 2 * (2 / θ + 1)) =
      (96 * Real.sqrt 2 / Real.pi) * zeta * (2 / θ + 1) := by
  field_simp [Real.pi_ne_zero, hθ]
  ring

/- Theory 67, formula 67.17: the elementary calculator majorant. -/
theorem jutila_jl7_sqrt_two_over_pi_lt_half :
    Real.sqrt 2 / Real.pi < (1 : ℝ) / 2 := by
  have hSqrtSq : (Real.sqrt (2 : ℝ)) ^ 2 = 2 :=
    Real.sq_sqrt (by norm_num)
  have hSqrtNonneg : 0 ≤ Real.sqrt (2 : ℝ) := Real.sqrt_nonneg _
  have hSqrtUpper : Real.sqrt (2 : ℝ) < 3 / 2 := by nlinarith
  have hPi : (3 : ℝ) < Real.pi := Real.pi_gt_three
  have hPiPos : 0 < Real.pi := Real.pi_pos
  rw [div_lt_iff₀ hPiPos]
  nlinarith

theorem jutila_jl7_elementary_contour_majorant
    {θ zeta : ℝ}
    (hθ : 0 < θ) (hzeta : 0 ≤ zeta)
    (hzetaUpper : zeta ≤ 1 + 1 / θ) :
    (96 * Real.sqrt 2 / Real.pi) * zeta * (2 / θ + 1) ≤
      48 * (1 + 1 / θ) * (2 / θ + 1) := by
  have hFront : 96 * Real.sqrt 2 / Real.pi < (48 : ℝ) := by
    calc
      96 * Real.sqrt 2 / Real.pi =
          96 * (Real.sqrt 2 / Real.pi) := by ring
      _ < 96 * (1 / 2 : ℝ) :=
        mul_lt_mul_of_pos_left jutila_jl7_sqrt_two_over_pi_lt_half
          (by norm_num)
      _ = 48 := by norm_num
  have hScale : 0 < 2 / θ + 1 := by positivity
  have hFirst : (96 * Real.sqrt 2 / Real.pi) * zeta ≤ 48 * zeta :=
    mul_le_mul_of_nonneg_right hFront.le hzeta
  have hSecond : 48 * zeta ≤ 48 * (1 + 1 / θ) := by nlinarith
  exact mul_le_mul_of_nonneg_right (hFirst.trans hSecond) hScale.le

/- Theory 67, formula 67.18: exact elementary endpoint value at theta=1/21.
   The decimal zeta diagnostic is intentionally not claimed here. -/
theorem jutila_jl7_elementary_endpoint :
    (48 : ℝ) * (1 + 1 / (1 / 21)) * (2 / (1 / 21) + 1) = 45408 := by
  norm_num

/-! ## Theory 68 — Jutila JL7 Lemma 3 absolute-sum multiplier -/

/- Theory 68, formula 68.10: every finite reciprocal-square partial sum is
   below 5/3.  Mathlib's zeta(2) identity and pi < 3.15 are the only inputs. -/
theorem jutila_jl7_basel_partial_lt_five_thirds (S : Finset ℕ) :
    (∑ n ∈ S, (1 : ℝ) / (n : ℝ) ^ 2) < 5 / 3 := by
  have hNonneg : ∀ n : ℕ, 0 ≤ (1 : ℝ) / (n : ℝ) ^ 2 := by
    intro n
    positivity
  have hPartial :
      (∑ n ∈ S, (1 : ℝ) / (n : ℝ) ^ 2) ≤ Real.pi ^ 2 / 6 := by
    have hSum := hasSum_zeta_two.summable.sum_le_tsum S
        (fun n _hn => hNonneg n)
    have hTsum : (∑' n : ℕ, (1 : ℝ) / (n : ℝ) ^ 2) = Real.pi ^ 2 / 6 :=
      hasSum_zeta_two.tsum_eq
    rw [hTsum] at hSum
    exact hSum
  have hPi : Real.pi < 3.15 := Real.pi_lt_d2
  have hPiPos : 0 < Real.pi := Real.pi_pos
  nlinarith

/- Theory 68, formula 68.4: local absolute coefficient when p divides
   exactly one of r and r'. -/
theorem jutila_jl7_local_exclusive (p : ℝ) (hp : 0 ≤ p) :
    1 + |-p| = p + 1 := by
  rw [abs_neg, abs_of_nonneg hp]
  ring

/- Theory 68, formula 68.4: local absolute coefficient when p divides both
   r and r'.  In particular p=2 gives the exact local value 1. -/
theorem jutila_jl7_local_common (p : ℝ) (hp : 2 ≤ p) :
    1 + |p * (p - 2)| = (p - 1) ^ 2 := by
  rw [abs_of_nonneg (mul_nonneg (by linarith) (by linarith))]
  ring

/- Theory 68, formulas 68.4--68.5: the exact common-prime factor is bounded
   by the product factor printed in Jutila Lemma 3. -/
theorem jutila_jl7_local_common_le_printed (p : ℝ) (hp : 0 ≤ p) :
    (p - 1) ^ 2 ≤ (p + 1) ^ 2 := by
  nlinarith

/- Theory 68, formula 68.6: an exclusive prime forces the reciprocal local
   factor to zero. -/
theorem jutila_jl7_reciprocal_exclusive (p : ℝ) (hp : 0 < p) :
    1 + (-p) / p = 0 := by
  field_simp
  ring

/- Theory 68, formula 68.6: a common prime contributes p-1 to the reciprocal
   local factor. -/
theorem jutila_jl7_reciprocal_common (p : ℝ) (hp : 0 < p) :
    1 + (p * (p - 2)) / p = p - 1 := by
  field_simp
  ring

/- Theory 68, formulas 68.8--68.10: once the outer one-variable envelope is
   at most (5/3)K, its square is safely at most 3K^2. -/
theorem jutila_jl7_pair_envelope
    {K A H : ℝ}
    (hK : 0 ≤ K) (hA : 0 ≤ A)
    (hAUpper : A ≤ (5 / 3) * K) (hH : H ≤ A ^ 2) :
    H ≤ 3 * K ^ 2 := by
  have hSquare : A ^ 2 ≤ ((5 / 3) * K) ^ 2 := by
    nlinarith
  nlinarith

/- Theory 68, formula 68.2: floor(R) <= R preserves the final 3R^2 bound. -/
theorem jutila_jl7_floor_endpoint
    {K R : ℝ} (hK : 0 ≤ K) (hKR : K ≤ R) :
    3 * K ^ 2 ≤ 3 * R ^ 2 := by
  nlinarith

/- Theory 68, formula 68.9: finite divisor double counting. -/
theorem jutila_jl7_divisor_double_count (K : ℕ) :
    (∑ n ∈ Finset.Ioc 0 K,
        ∑ d ∈ Finset.Ioc 0 K,
          if d ∣ n then (1 : ℝ) / (d : ℝ) else 0) =
      ∑ d ∈ Finset.Ioc 0 K, ((K / d : ℕ) : ℝ) / (d : ℝ) := by
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro d hd
  rw [← Finset.sum_filter]
  rw [Finset.sum_const]
  simp only [nsmul_eq_mul]
  rw [Nat.Ioc_filter_dvd_card_eq_div]
  ring

/- Theory 68, formula 68.9: floor(K/d)/d is bounded by K/d^2 termwise. -/
theorem jutila_jl7_divisor_envelope_le_reciprocal_square (K : ℕ) :
    (∑ d ∈ Finset.Ioc 0 K, ((K / d : ℕ) : ℝ) / (d : ℝ)) ≤
      (K : ℝ) * ∑ d ∈ Finset.Ioc 0 K, (1 : ℝ) / (d : ℝ) ^ 2 := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro d hd
  have hdNat : 0 < d := (Finset.mem_Ioc.mp hd).1
  have hdReal : 0 < (d : ℝ) := by exact_mod_cast hdNat
  have hMulNat : K / d * d ≤ K := Nat.div_mul_le_self K d
  have hMulReal : ((K / d : ℕ) : ℝ) * (d : ℝ) ≤ (K : ℝ) := by
    exact_mod_cast hMulNat
  rw [show (K : ℝ) * (1 / (d : ℝ) ^ 2) =
      (K : ℝ) / (d : ℝ) ^ 2 by ring]
  rw [div_le_div_iff₀ hdReal (sq_pos_of_pos hdReal)]
  nlinarith

/- Theory 68, formulas 68.9--68.10: the finite divisor envelope is strictly
   below (5/3)K for positive K. -/
theorem jutila_jl7_divisor_envelope_lt_five_thirds
    {K : ℕ} (hK : 0 < K) :
    (∑ d ∈ Finset.Ioc 0 K, ((K / d : ℕ) : ℝ) / (d : ℝ)) <
      (5 / 3 : ℝ) * K := by
  have hPartial :=
    jutila_jl7_basel_partial_lt_five_thirds (Finset.Ioc 0 K)
  have hKReal : 0 < (K : ℝ) := by exact_mod_cast hK
  have hScaled := mul_lt_mul_of_pos_left hPartial hKReal
  exact (jutila_jl7_divisor_envelope_le_reciprocal_square K).trans_lt (by
    simpa [mul_comm] using hScaled)

/- Theory 68, formulas 68.11--68.12: the Lemma 3 multiplier 3 multiplies
   Theory 67's elementary contour coefficient exactly. -/
theorem jutila_jl7_contour_lemma3_combined_coefficient (θ : ℝ) :
    3 * (48 * (1 + 1 / θ) * (2 / θ + 1)) =
      144 * (1 + 1 / θ) * (2 / θ + 1) := by
  ring

/- Theory 68, formula 68.13: exact endpoint at theta=1/21. -/
theorem jutila_jl7_contour_lemma3_endpoint :
    (144 : ℝ) * (1 + 1 / (1 / 21)) * (2 / (1 / 21) + 1) = 136224 := by
  norm_num

/-! ## Theory 69 — Jutila JL7 principal residue and height row sum -/

/- Theory 69, formula 69.12: the xi-interval coefficient at the actual
   endpoint.  Multiplication by log D is a separate nonnegative scaling. -/
theorem jutila_jl7_residue_xi_length_coefficient
    {θ : ℝ} (hθ : 0 ≤ θ) (hθUpper : θ ≤ 1 / 21) :
    θ * (1 / 2 + 7 * θ) ≤ (5 / 6) * θ := by
  nlinarith

/- Theory 69, formula 69.12: after the finite premise 2 log L <= L has
   been supplied, the eta-interval coefficient is at most 18/7. -/
theorem jutila_jl7_residue_eta_length_coefficient
    {θ L logL : ℝ}
    (hθ : 0 ≤ θ) (hθUpper : θ ≤ 1 / 21)
    (hL : 0 ≤ L) (hLog : 2 * logL ≤ L) :
    θ * ((1 + 12 * θ) * L + 2 * logL) ≤
      (18 / 7) * θ * L := by
  have hThetaScale : 1 + 12 * θ ≤ 11 / 7 := by nlinarith
  have hMain : (1 + 12 * θ) * L ≤ (11 / 7) * L :=
    mul_le_mul_of_nonneg_right hThetaScale hL
  have hBracket : (1 + 12 * θ) * L + 2 * logL ≤ (18 / 7) * L := by
    nlinarith
  simpa [mul_assoc, mul_left_comm, mul_comm] using
    (mul_le_mul_of_nonneg_left hBracket hθ)

/- Theory 69, formulas 69.12--69.13: the three interval coefficients fit
   below the rational mass coefficient 7. -/
theorem jutila_jl7_residue_zero_mass_coefficient :
    (5 / 6 : ℝ) * (18 / 7) * 3 < 7 := by
  norm_num

/- Theory 69, formula 69.14: twice the two interval lengths fits below 7. -/
theorem jutila_jl7_residue_offdiag_kernel_coefficient :
    2 * ((5 / 6 : ℝ) + 18 / 7) < 7 := by
  norm_num

/- Theory 69, untagged Gamma-strip display: 0 <= Re z <= 2/21 implies
   19/21 <= Re(1-z) <= 1. -/
theorem jutila_jl7_residue_gamma_strip
    {u : ℝ} (hu : 0 ≤ u) (huUpper : u ≤ 2 / 21) :
    19 / 21 ≤ 1 - u ∧ 1 - u ≤ 1 := by
  constructor <;> linarith

/- Theory 69, formula 69.15: the split Euler-integral envelope for Gamma
   is strictly smaller than 3.  The complex integral comparison itself is
   an external/source analytic step. -/
theorem jutila_jl7_residue_gamma_rational_envelope :
    (21 / 19 : ℝ) + 1 = 40 / 19 ∧ (40 / 19 : ℝ) < 3 := by
  constructor <;> norm_num

/- Theory 69, formula 69.17: the two-sided Basel row coefficient. -/
theorem jutila_jl7_residue_spacing_row_coefficient :
    2 * (5 / 3 : ℝ) = 10 / 3 := by
  norm_num

/- Theory 69, untagged diagonal/off-diagonal displays: exact coefficient
   arithmetic before the one-row envelope. -/
theorem jutila_jl7_residue_diagonal_pair_identity (θ L : ℝ) :
    3 * 7 * θ ^ 2 * L ^ 3 = 21 * θ ^ 2 * L ^ 3 := by
  ring

theorem jutila_jl7_residue_offdiagonal_pair_identity (θ L : ℝ) :
    3 * 7 * θ * L * (10 / 3 * L ^ 2) = 70 * θ * L ^ 3 := by
  ring

/- Theory 69, formula 69.18: diagonal and off-diagonal pair bounds combine
   to the one-row coefficient 91 theta when 0 <= theta <= 1. -/
theorem jutila_jl7_residue_row_coefficient
    {θ : ℝ} (hθ : 0 ≤ θ) (hθUpper : θ ≤ 1) :
    3 * 7 * θ ^ 2 + 3 * 7 * θ * (10 / 3) ≤ 91 * θ := by
  nlinarith

/- Theory 69, formula 69.21: the three conservative Rankin/Euler/zeta
   rational envelopes multiply to 12. -/
theorem jutila_jl7_residue_rankin_rsum_coefficient :
    (2 : ℝ) * 3 * 2 = 12 := by
  norm_num

/- Theory 69, formula 69.22: the actual theta endpoint turns the
   pre-endpoint coefficient 1092 theta into the calculator-safe 52. -/
theorem jutila_jl7_residue_endpoint_coefficient
    {θ : ℝ} (_hθ : 0 ≤ θ) (hθUpper : θ ≤ 1 / 21) :
    12 * 91 * θ ≤ 52 := by
  nlinarith

/- Theory 69, formulas 69.2 and 69.22: conditional terminal multiplication.
   `base` is the nonnegative J*(phi(q)/q)^2*x^(2-2alpha)*L^2 factor;
   the analytic residue estimate remains an explicit premise. -/
theorem jutila_jl7_residue_final_composition
    {θ base value : ℝ}
    (hθ : 0 ≤ θ) (hθUpper : θ ≤ 1 / 21)
    (hBase : 0 ≤ base) (hValue : value ≤ (12 * 91 * θ) * base) :
    value ≤ 52 * base := by
  have hCoefficient := jutila_jl7_residue_endpoint_coefficient hθ hθUpper
  exact hValue.trans (mul_le_mul_of_nonneg_right hCoefficient hBase)

/-! ## Theory 70 — Jutila JL7 strict terminal absorption -/

/- Theory 70, formula 70.4: the weighted square-sum multiplier and the
   denominator quotient are counted exactly once. -/
theorem jutila_jl7_preterminal_multiplier
    {θ : ℝ} (hθ : θ ≠ 0) :
    5 * (34 / θ ^ 2) = 170 / θ ^ 2 := by
  field_simp
  ring

/- Theory 70, formulas 70.6--70.7: pi^2 < 10 gives a strict rational
   detector lower bound on the actual 0 < theta < 1 range. -/
theorem jutila_pi_square_lt_ten : Real.pi ^ 2 < 10 := by
  have hPi : Real.pi < 3.15 := Real.pi_lt_d2
  have hPiPos : 0 < Real.pi := Real.pi_pos
  nlinarith

theorem jutila_jl7_rational_detector_lower
    {θ : ℝ} (hθ : 0 < θ) (hθUpper : θ < 1) :
    (3 / 5) * (1 - θ) * θ <
      (1 - θ) * (6 / Real.pi ^ 2) * θ := by
  have hPiSquarePos : 0 < Real.pi ^ 2 := sq_pos_of_pos Real.pi_pos
  have hCoefficient : (3 / 5 : ℝ) < 6 / Real.pi ^ 2 := by
    rw [lt_div_iff₀ hPiSquarePos]
    nlinarith [jutila_pi_square_lt_ten]
  have hScale : 0 < (1 - θ) * θ :=
    mul_pos (sub_pos.mpr hθUpper) hθ
  simpa [mul_assoc, mul_left_comm, mul_comm] using
    (mul_lt_mul_of_pos_right hCoefficient hScale)

/- Theory 70, formula 70.16: a completely finite sufficient gate for
   4*log(L)/L <= 29/252. -/
theorem jutila_jl7_exp_eight_log_gate
    {L : ℝ} (hL : Real.exp 8 ≤ L) :
    4 * Real.log L / L ≤ 29 / 252 := by
  have hDomainEight : Real.exp 1 ≤ Real.exp 8 :=
    Real.exp_le_exp.mpr (by norm_num)
  have hDomainL : Real.exp 1 ≤ L := hDomainEight.trans hL
  have hRatio :=
    Real.log_div_self_antitoneOn hDomainEight hDomainL hL
  change Real.log L / L ≤ Real.log (Real.exp 8) / Real.exp 8 at hRatio
  rw [Real.log_exp] at hRatio
  have hExpLower :=
    Real.pow_div_factorial_le_exp (x := (8 : ℝ)) (by norm_num) 6
  norm_num at hExpLower
  have hAtEight :
      4 * (8 / Real.exp 8) ≤ (29 / 252 : ℝ) := by
    have hExpPos : 0 < Real.exp 8 := Real.exp_pos 8
    rw [show 4 * (8 / Real.exp 8) = 32 / Real.exp 8 by ring]
    rw [div_le_iff₀ hExpPos]
    nlinarith
  have hScaled :=
    mul_le_mul_of_nonneg_left hRatio (by norm_num : (0 : ℝ) ≤ 4)
  calc
    4 * Real.log L / L = 4 * (Real.log L / L) := by ring
    _ ≤ 4 * (8 / Real.exp 8) := hScaled
    _ ≤ 29 / 252 := hAtEight

/- Theory 70, formulas 70.13--70.14: the logarithmic cutoff pays one
   exponential multiplier.  This is the finite real implication only. -/
theorem jutila_jl7_exponential_cutoff_transfer
    {P γ L : ℝ}
    (hP : 0 < P) (hγ : 0 < γ)
    (hCutoff : Real.log P / γ ≤ L) :
    P * Real.exp (-γ * L) ≤ 1 := by
  apply pap_fixed_d_transfer_gate (K := P) (η := 1) (c := L) (D := γ)
  · exact hP
  · norm_num
  · exact hγ
  · simpa using hCutoff

/- Theory 70, formula 70.12: q/phi(q) <= 6L supplies the exact square
   normalization 36 after division by L^2. -/
theorem jutila_jl7_totient_square_normalization
    {u L : ℝ}
    (hL : 0 < L) (hu : 0 ≤ u) (hUpper : u ≤ 6 * L) :
    u ^ 2 / L ^ 2 ≤ 36 := by
  have hSquare : u ^ 2 ≤ (6 * L) ^ 2 := by nlinarith
  rw [div_le_iff₀ (sq_pos_of_pos hL)]
  nlinarith

/- Theory 70, formula 70.15: the exact rational fallback P/gamma is a
   stronger sufficient cutoff than log(P)/gamma. -/
theorem jutila_jl7_rational_fallback_cutoff
    {P γ L : ℝ}
    (hP : 0 < P) (hγ : 0 < γ)
    (hFallback : P / γ ≤ L) :
    Real.log P / γ ≤ L := by
  rw [div_le_iff₀ hγ] at hFallback ⊢
  exact (Real.log_le_self hP.le).trans hFallback

/- Theory 70, formulas 70.14 and 70.18: a half-margin version of the
   fail-closed terminal algebra.  A,B,E,J,Y are finite real inputs. -/
theorem jutila_jl7_half_margin_terminal
    {A B E J Y : ℝ}
    (hA : 0 < A) (hB : 0 ≤ B) (hY : 0 ≤ Y)
    (hE : E ≤ A / 2) (hJ : 0 < J)
    (hInequality : A * J ^ 2 ≤ B * J * Y + E * J ^ 2) :
    J ≤ 2 * B * Y / A := by
  have hGap : 0 < A - E := by nlinarith
  have hRaw :=
    jutila_t1_terminal_absorption hGap hJ hInequality
  have hHalfPos : 0 < A / 2 := by positivity
  have hDenominator : A / 2 ≤ A - E := by nlinarith
  have hNumerator : 0 ≤ B * Y := mul_nonneg hB hY
  have hCompare :
      B * Y / (A - E) ≤ B * Y / (A / 2) :=
    div_le_div_of_nonneg_left hNumerator hHalfPos hDenominator
  calc
    J ≤ B * Y / (A - E) := hRaw
    _ ≤ B * Y / (A / 2) := hCompare
    _ = 2 * B * Y / A := by field_simp

/- Theory 70, formula 70.18: exact simplification of the selected-system
   coefficient. -/
theorem jutila_jl7_selected_system_coefficient
    {θ : ℝ} (hθ : θ ≠ 0) (hOne : 1 - θ ≠ 0) :
    (2 * (52 * (170 / θ ^ 2))) /
        (((3 / 5) * (1 - θ) * θ) ^ 2 * (θ ^ 2 / 2)) =
      884000 / (9 * (1 - θ) ^ 2 * θ ^ 6) := by
  field_simp
  ring

/- Theory 70, formula 70.19: exact endpoint diagnostics at theta=1/21. -/
theorem jutila_jl7_absorption_ratio_endpoint :
    (72 : ℝ) * 74970 * 136224 / (4 / 147) ^ 2 =
      993089345703840 := by
  norm_num

theorem jutila_jl7_absorption_endpoint_coefficients :
    (170 : ℝ) / (1 / 21) ^ 2 = 74970 ∧
      (144 : ℝ) * (1 + 1 / (1 / 21)) *
          (2 / (1 / 21) + 1) = 136224 ∧
      (3 / 5 : ℝ) * (1 - 1 / 21) * (1 / 21) = 4 / 147 ∧
      (29 / 252 : ℝ) * (1 / 21) = 29 / 5292 := by
  norm_num

theorem jutila_jl7_selected_system_endpoint :
    (884000 : ℝ) /
        (9 * (1 - 1 / 21) ^ 2 * (1 / 21) ^ 6) =
      9287613243090 := by
  norm_num

/- Theory 70, formula 70.3: parity and local-square recovery happens only
   after the one-system bound. -/
theorem jutila_jl7_parity_local_count_composition
    {N J C Y radius : ℝ}
    (hRadius : 0 ≤ radius)
    (hN : N ≤ 2 * J * radius)
    (hJ : J ≤ C * Y) :
    N ≤ 2 * C * Y * radius := by
  have hScaled :
      2 * J * radius ≤ 2 * (C * Y) * radius := by
    exact mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left hJ (by norm_num)) hRadius
  calc
    N ≤ 2 * J * radius := hN
    _ ≤ 2 * (C * Y) * radius := hScaled
    _ = 2 * C * Y * radius := by ring

/-! ## Theory 71 — Jutila JL7 averaged primitive replay -/

/- Theory 71, formula 71.13: the phase magnitude q/phi(q) cancels the
   detector's phi(q)/q exactly.  The arithmetic variables are positive
   finite reals; the character-theoretic phase choice remains a source
   analytic premise. -/
theorem jutila_jl7_averaged_detector_phase_cancellation
    {q phiQ : ℝ} (hq : q ≠ 0) (hPhi : phiQ ≠ 0) :
    (q / phiQ) * (phiQ / q) = 1 := by
  field_simp

/- Theory 71, formula 71.16: on a principal primitive-character pair,
   the two phase weights cancel the L-residue and pseudocharacter
   totient factors.  Primitivity forcing equal conductors is deliberately
   not asserted by this scalar theorem. -/
theorem jutila_jl7_averaged_principal_residue_cancellation
    {q phiQ : ℝ} (hq : q ≠ 0) (hPhi : phiQ ≠ 0) :
    (q / phiQ) ^ 2 * (phiQ / q) ^ 2 = 1 := by
  field_simp

/- Theory 71, formula 71.18: two separate phase bounds q/phi(q) <= 6L
   cost at most 36 after the common detector L^2 is divided out. -/
theorem jutila_jl7_averaged_phase_pair_normalization
    {u v L : ℝ}
    (hL : 0 < L) (hv : 0 ≤ v)
    (huUpper : u ≤ 6 * L) (hvUpper : v ≤ 6 * L) :
    u * v / L ^ 2 ≤ 36 := by
  have hSixL : 0 ≤ 6 * L := by positivity
  have hProduct : u * v ≤ (6 * L) * (6 * L) :=
    mul_le_mul huUpper hvUpper hv hSixL
  rw [div_le_iff₀ (sq_pos_of_pos hL)]
  nlinarith

/- Theory 71, formula 71.7: abstract finite algebra behind the two
   directions of the common Mellin scale envelope.  Here `base` denotes
   D^(1/2+9 theta), `u` denotes sqrt(qT), and `sqrtD` denotes sqrt(D).
   The real-power identifications remain outside this algebraic theorem. -/
theorem jutila_jl7_averaged_mellin_scale_envelope
    {base u sqrtD : ℝ}
    (hBase : 0 ≤ base) (hLower : 1 ≤ u) (hUpper : u ≤ sqrtD) :
    base ≤ u * base ∧ u * base ≤ sqrtD * base := by
  constructor
  · simpa [one_mul] using mul_le_mul_of_nonneg_right hLower hBase
  · exact mul_le_mul_of_nonneg_right hUpper hBase

/- Theory 71, formulas 71.7 and 71.9: exact exponents used for the lower
   Mellin envelope and its negative-power decay. -/
theorem jutila_jl7_averaged_mellin_exponent_identities (theta : ℝ) :
    (1 / 2 + 9 * theta) + 1 / 2 = 1 + 9 * theta ∧
      theta * (1 / 2 + 9 * theta) / 2 =
        theta / 4 + 9 * theta ^ 2 / 2 := by
  constructor <;> ring

theorem jutila_jl7_averaged_mellin_decay_endpoint :
    (1 / 21 : ℝ) * (1 / 2 + 9 * (1 / 21)) / 2 = 13 / 588 := by
  norm_num

/- Theory 71, formulas 71.20--71.21: cancellation of the common positive
   L^2 normalization.  All analytic estimates are explicit premises. -/
theorem jutila_jl7_averaged_cancel_log_square
    {A B E J Y L : ℝ} (hL : L ≠ 0)
    (hRaw :
      (A * J ^ 2) * L ^ 2 ≤
        (B * J * Y + E * J ^ 2) * L ^ 2) :
    A * J ^ 2 ≤ B * J * Y + E * J ^ 2 := by
  exact le_of_mul_le_mul_right hRaw (sq_pos_of_ne_zero hL)

/- Theory 71, formulas 71.21--71.23: after the averaged replay has
   produced the same normalized A,B,E inequality, Theory 70's strict
   half-margin terminal applies without a new Q-dependent coefficient. -/
theorem jutila_jl7_averaged_terminal_reuse
    {A B E J Y : ℝ}
    (hA : 0 < A) (hB : 0 ≤ B) (hY : 0 ≤ Y)
    (hE : E ≤ A / 2) (hJ : 0 < J)
    (hInequality : A * J ^ 2 ≤ B * J * Y + E * J ^ 2) :
    J ≤ 2 * B * Y / A := by
  exact jutila_jl7_half_margin_terminal
    hA hB hY hE hJ hInequality

/- Theory 71, formula 71.24: the local zero-count logarithm is uniformly
   bounded by the common family scale D=Q^2*T. -/
theorem jutila_jl7_averaged_height_log_upper
    {q Q T D : ℝ}
    (hq : 0 < q) (hQ : 1 ≤ Q) (hT : 1 ≤ T)
    (hqUpper : q ≤ Q) (hD : D = Q ^ 2 * T) :
    Real.log (q * (1 + T)) ≤ Real.log (2 * Q * T) ∧
      Real.log (2 * Q * T) ≤ Real.log (2 * D) := by
  have hQPos : 0 < Q := lt_of_lt_of_le zero_lt_one hQ
  have hTPos : 0 < T := lt_of_lt_of_le zero_lt_one hT
  have hOnePlus : 1 + T ≤ 2 * T := by linarith
  have hFirst : q * (1 + T) ≤ 2 * Q * T := by
    calc
      q * (1 + T) ≤ q * (2 * T) :=
        mul_le_mul_of_nonneg_left hOnePlus hq.le
      _ ≤ Q * (2 * T) :=
        mul_le_mul_of_nonneg_right hqUpper (by positivity)
      _ = 2 * Q * T := by ring
  have hQSquare : Q ≤ Q ^ 2 := by
    nlinarith [sq_nonneg (Q - 1)]
  have hSecond : 2 * Q * T ≤ 2 * D := by
    rw [hD]
    have hQT : Q * T ≤ Q ^ 2 * T :=
      mul_le_mul_of_nonneg_right hQSquare hTPos.le
    calc
      2 * Q * T = 2 * (Q * T) := by ring
      _ ≤ 2 * (Q ^ 2 * T) :=
        mul_le_mul_of_nonneg_left hQT (by norm_num)
  constructor
  · exact Real.log_le_log (mul_pos hq (by linarith)) hFirst
  · exact Real.log_le_log (by positivity) hSecond

/-! ## Theory 72 — Gallagher--Maier PAP density-integral split -/

/- Theory 72, formulas 72.11 and 72.15: exact endpoint exponent algebra.
   These identities do not assert the analytic zero-density premises. -/
theorem gallagher_maier_pap_split_endpoint_exponents :
    (14 : ℝ) * (1 + 12 * (1 / 21)) = 22 ∧
      (1 : ℝ) - 22 / 160 = 69 / 80 ∧
      (1 : ℝ) / 21 - 7 / 160 = 13 / 3360 ∧
      0 < (13 / 3360 : ℝ) ∧
      12 / 160 = (3 / 40 : ℝ) := by
  norm_num

/- Theory 72, formulas 72.6--72.7: finite scalar composition after the
   source theorem has supplied a per-character upper bound and elementary
   character counting has supplied count <= Q^2. -/
theorem bennett_family_total_zero_composition
    {Z count U Q T logQT : ℝ}
    (hUPos : 0 ≤ U)
    (hCount : count ≤ Q ^ 2)
    (hPerCharacter : U ≤ 2 * T * logQT)
    (hTotal : Z ≤ count * U) :
    Z ≤ 2 * Q ^ 2 * T * logQT := by
  have hCountStep : count * U ≤ Q ^ 2 * U :=
    mul_le_mul_of_nonneg_right hCount hUPos
  have hEnvelopeStep : Q ^ 2 * U ≤ Q ^ 2 * (2 * T * logQT) :=
    mul_le_mul_of_nonneg_left hPerCharacter (sq_nonneg Q)
  calc
    Z ≤ count * U := hTotal
    _ ≤ Q ^ 2 * U := hCountStep
    _ ≤ Q ^ 2 * (2 * T * logQT) := hEnvelopeStep
    _ = 2 * Q ^ 2 * T * logQT := by ring

/- Theory 72, formula 72.8: the integrated far interval and Gallagher's
   endpoint term cancel the artificial X^(-1) boundary exactly.  The
   integral evaluation itself is an explicit analytic premise. -/
theorem gallagher_maier_far_endpoint_cancellation
    (Z xTheta xInv : ℝ) :
    Z * (xTheta - xInv) + xInv * Z = Z * xTheta := by
  ring

/- Theory 72, formula 72.14: exact algebraic cancellation when the near
   integral is split at delta=1/L.  The exponential antiderivatives and
   branch ordering eta <= 1/L <= theta remain analytic premises. -/
theorem gallagher_maier_near_piecewise_cancellation
    {A C B eEta eSwitch eTheta terminalLinear : ℝ}
    (hA : A ≠ 0) :
    C * (eEta - eSwitch) / A +
        eSwitch * (C / A + B / A ^ 2) -
        eTheta * (terminalLinear / A + B / A ^ 2) =
      C * eEta / A + B * eSwitch / A ^ 2 -
        eTheta * (terminalLinear / A + B / A ^ 2) := by
  field_simp
  ring

/- Theory 72, formulas 72.9--72.10: conditional real-power normalization.
   The symbols q2t and logQT represent Q^2*T and log(Q*T), respectively. -/
theorem gallagher_maier_far_power_composition
    {Z q2t logQT Xtheta target : ℝ}
    (hXTheta : 0 ≤ Xtheta)
    (hZ : Z ≤ 2 * q2t * logQT)
    (hNormalize : (2 * q2t * logQT) * Xtheta = target) :
    Z * Xtheta ≤ target := by
  calc
    Z * Xtheta ≤ (2 * q2t * logQT) * Xtheta :=
      mul_le_mul_of_nonneg_right hZ hXTheta
    _ = target := hNormalize

/-! ## Theory 73 — Jutila C_J loss-tree structural audit -/

/- Theory 73, formulas 73.1--73.2: the six displayed loss factors simplify
   to Theory 70's selected-system coefficient.  The nonzero hypotheses are
   precisely the divisions used in the identity; no analytic estimate is
   asserted here. -/
theorem jutila_cj_baseline_factorization
    {theta : ℝ} (hTheta : theta ≠ 0) (hOneMinus : 1 - theta ≠ 0) :
    2 * 52 * 5 * (34 / theta ^ 2) /
          ((3 / 5 : ℝ) * (1 - theta) * theta) ^ 2 /
          (theta ^ 2 / 2) =
      884000 / (9 * (1 - theta) ^ 2 * theta ^ 6) := by
  field_simp
  ring

/- Theory 73, formulas 73.2--73.3: exact endpoint detector and coefficient. -/
theorem jutila_cj_baseline_endpoint :
    (3 / 5 : ℝ) * (1 - 1 / 21) * (1 / 21) = 4 / 147 ∧
      884000 / (9 * (1 - (1 / 21 : ℝ)) ^ 2 * (1 / 21 : ℝ) ^ 6) =
        9287613243090 ∧
      (9287613243090 : ℝ) = 108290 * 21 ^ 6 := by
  norm_num

/- Theory 73, formula 73.11: exact specialization of the rational
   Barban--Vehov coefficient.  The analytic Corollary remains an external
   source theorem and is not asserted by this equality. -/
theorem jutila_cj_rz_endpoint_coefficient :
    (309 / 200 : ℝ) *
          (2327 / 500 + (34421 / 250) * (1 / 21) +
            (255149 / 250) * (1 / 21) ^ 2) /
          ((1 / 21) * (1 + 14 * (1 / 21))) =
      921495783 / 3500000 := by
  norm_num

/- Theory 73, formulas 73.12--73.15: once the finite logarithmic ratio
   has supplied the strict upper 34, the exact endpoint coefficient and
   denominator factor compose to the displayed preterminal rational. -/
theorem jutila_cj_weighted_preterminal_endpoint :
    (34 : ℝ) * (921495783 / 3500000) =
        15665428311 / 1750000 ∧
      (8 / 5 : ℝ) * (15665428311 / 1750000) =
        15665428311 / 1093750 := by
  norm_num

/- Theory 73, formula 73.10: exact numerical endpoint comparison used after
   the separate monotonicity argument has reduced the quotient to e/(e-1). -/
theorem jutila_cj_denominator_limit_lt_eight_fifths :
    Real.exp 1 / (Real.exp 1 - 1) < (8 / 5 : ℝ) := by
  have hExp : (8 / 3 : ℝ) < Real.exp 1 :=
    (by norm_num : (8 / 3 : ℝ) < 2.7182818283).trans Real.exp_one_gt_d9
  have hDen : 0 < Real.exp 1 - 1 := by
    linarith [Real.exp_one_gt_two]
  rw [div_lt_iff₀ hDen]
  nlinarith

theorem jutila_cj_exp_quarter_lt_four_thirds :
    Real.exp (1 / 4 : ℝ) < 4 / 3 := by
  have hExp := Real.exp_bound'
    (x := (1 / 4 : ℝ)) (by norm_num) (by norm_num)
    (n := 6) (by norm_num)
  norm_num [Finset.sum_range_succ, Nat.factorial] at hExp ⊢
  nlinarith

/- Theory 73, formulas 73.8--73.10: the full finite denominator quotient
   bound.  This proof uses order properties of exp and exact algebra rather
   than importing a new analytic source premise. -/
theorem jutila_cj_denominator_quotient_lt_eight_fifths
    {rho t : ℝ} (hRho : 4 ≤ rho) (hT : 1 / rho ≤ t) :
    Real.exp (-t) / (1 - Real.exp (-(rho - 1) * t)) < 8 / 5 := by
  have hRhoPos : 0 < rho := by linarith
  have hRhoOnePos : 0 < rho - 1 := by linarith
  have hAPos : 0 < (1 / rho : ℝ) := one_div_pos.mpr hRhoPos
  have hTPos : 0 < t := hAPos.trans_le hT
  have hProdT : 0 < (rho - 1) * t := mul_pos hRhoOnePos hTPos
  have hProdA : 0 < (rho - 1) * (1 / rho) :=
    mul_pos hRhoOnePos hAPos
  have hDenT : 0 < 1 - Real.exp (-(rho - 1) * t) :=
    sub_pos.mpr (Real.exp_lt_one_iff.mpr (by nlinarith [hProdT]))
  have hDenA : 0 < 1 - Real.exp (-(rho - 1) * (1 / rho)) :=
    sub_pos.mpr (Real.exp_lt_one_iff.mpr (by nlinarith [hProdA]))
  have hNumerator : Real.exp (-t) ≤ Real.exp (-(1 / rho)) :=
    Real.exp_le_exp.mpr (neg_le_neg hT)
  have hExponent :
      -(rho - 1) * t ≤ -(rho - 1) * (1 / rho) :=
    mul_le_mul_of_nonpos_left hT (by linarith)
  have hDenOrder :
      1 - Real.exp (-(rho - 1) * (1 / rho)) ≤
        1 - Real.exp (-(rho - 1) * t) :=
    sub_le_sub_left (Real.exp_le_exp.mpr hExponent) 1
  have hToEndpoint :
      Real.exp (-t) / (1 - Real.exp (-(rho - 1) * t)) ≤
        Real.exp (-(1 / rho)) /
          (1 - Real.exp (-(rho - 1) * (1 / rho))) := by
    rw [div_le_div_iff₀ hDenT hDenA]
    calc
      Real.exp (-t) * (1 - Real.exp (-(rho - 1) * (1 / rho))) ≤
          Real.exp (-(1 / rho)) *
            (1 - Real.exp (-(rho - 1) * (1 / rho))) :=
        mul_le_mul_of_nonneg_right hNumerator hDenA.le
      _ ≤ Real.exp (-(1 / rho)) *
            (1 - Real.exp (-(rho - 1) * t)) :=
        mul_le_mul_of_nonneg_left hDenOrder (Real.exp_nonneg _)
  let a : ℝ := 1 / rho
  let e : ℝ := Real.exp 1
  let u : ℝ := Real.exp a
  have hAUpper : a ≤ 1 / 4 := by
    dsimp [a]
    rw [div_le_iff₀ hRhoPos]
    nlinarith
  have hUPos : 0 < u := by
    dsimp [u]
    exact Real.exp_pos a
  have hUOne : 1 ≤ u := by
    dsimp [u]
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr hAPos.le
  have hUUpper : u < 4 / 3 := by
    dsimp [u]
    exact (Real.exp_le_exp.mpr hAUpper).trans_lt
      jutila_cj_exp_quarter_lt_four_thirds
  have hELower : (8 / 3 : ℝ) < e := by
    dsimp [e]
    exact (by norm_num : (8 / 3 : ℝ) < 2.7182818283).trans
      Real.exp_one_gt_d9
  have hEOnePos : 0 < e - 1 := by linarith
  have hSecondFactor : 0 ≤ e - u - 1 := by linarith
  have hProduct : 0 ≤ (u - 1) * (e - u - 1) :=
    mul_nonneg (sub_nonneg.mpr hUOne) hSecondFactor
  have hCore : e - 1 ≤ u * (e - u) := by
    nlinarith
  have hDivCore : (e - 1) / u ≤ e - u := by
    exact (div_le_iff₀ hUPos).2 (by simpa [mul_comm] using hCore)
  have hExponentA : -(rho - 1) * a = a - 1 := by
    dsimp [a]
    field_simp
    ring
  have hLeft : Real.exp (-a) * (e - 1) = (e - 1) / u := by
    simp [u, Real.exp_neg]
    ring
  have hRight : e * (1 - Real.exp (-(rho - 1) * a)) = e - u := by
    rw [hExponentA, Real.exp_sub]
    dsimp [e, u]
    field_simp [Real.exp_ne_zero]
  have hEndpointCross :
      Real.exp (-a) * (e - 1) ≤
        e * (1 - Real.exp (-(rho - 1) * a)) := by
    calc
      Real.exp (-a) * (e - 1) = (e - 1) / u := hLeft
      _ ≤ e - u := hDivCore
      _ = e * (1 - Real.exp (-(rho - 1) * a)) := hRight.symm
  have hEndpoint :
      Real.exp (-a) / (1 - Real.exp (-(rho - 1) * a)) ≤
        e / (e - 1) := by
    rw [div_le_div_iff₀ hDenA hEOnePos]
    exact hEndpointCross
  calc
    Real.exp (-t) / (1 - Real.exp (-(rho - 1) * t)) ≤
        Real.exp (-(1 / rho)) /
          (1 - Real.exp (-(rho - 1) * (1 / rho))) := hToEndpoint
    _ = Real.exp (-a) / (1 - Real.exp (-(rho - 1) * a)) := by rfl
    _ ≤ e / (e - 1) := hEndpoint
    _ = Real.exp 1 / (Real.exp 1 - 1) := by rfl
    _ < 8 / 5 := jutila_cj_denominator_limit_lt_eight_fifths

/- Theory 73, formula 73.13: the finite logarithmic ratio is strictly below
   16/21 once L>=441. -/
theorem jutila_cj_log_ratio_441
    {L : ℝ} (hL : 441 ≤ L) :
    42 * Real.log L / L < 16 / 21 := by
  have hDomain441 : Real.exp 1 ≤ (441 : ℝ) :=
    (le_of_lt Real.exp_one_lt_three).trans (by norm_num)
  have hDomainL : Real.exp 1 ≤ L := hDomain441.trans hL
  have hRatio := Real.log_div_self_antitoneOn hDomain441 hDomainL hL
  have hExpEight : (441 : ℝ) < Real.exp 8 := by
    have hSeries := Real.sum_le_exp_of_nonneg (x := (8 : ℝ)) (by norm_num) 6
    norm_num [Finset.sum_range_succ] at hSeries ⊢
    linarith
  have hLog441 : Real.log (441 : ℝ) < 8 := by
    rw [Real.log_lt_iff_lt_exp (by norm_num : (0 : ℝ) < 441)]
    exact hExpEight
  have hRatio441 : Real.log (441 : ℝ) / 441 < 8 / 441 := by
    norm_num at hLog441 ⊢
    linarith
  have hCombined : Real.log L / L < 8 / 441 := hRatio.trans_lt hRatio441
  have hScaled := mul_lt_mul_of_pos_left hCombined (by norm_num : (0 : ℝ) < 42)
  calc
    42 * Real.log L / L = 42 * (Real.log L / L) := by ring
    _ < 42 * (8 / 441 : ℝ) := hScaled
    _ = 16 / 21 := by norm_num

/- Theory 73, formulas 73.16--73.17 and 73.21: exact endpoint height-row
   and residue arithmetic after the analytic Rankin envelope is supplied. -/
theorem jutila_cj_residue_endpoint :
    (280 / 19 : ℝ) * (1 / 21) ^ 2 +
          (2800 / 57) * (1 / 21) = 2840 / 1197 ∧
      (7 / 4 : ℝ) * (2840 / 1197) = 710 / 171 := by
  norm_num

theorem jutila_cj_residue_row_monotone_endpoint
    {theta : ℝ} (hTheta : 0 ≤ theta) (hUpper : theta ≤ 1 / 21) :
    (280 / 19 : ℝ) * theta ^ 2 + (2800 / 57) * theta ≤ 2840 / 1197 := by
  have hProduct : 0 ≤ theta * ((1 / 21 : ℝ) - theta) :=
    mul_nonneg hTheta (sub_nonneg.mpr hUpper)
  nlinarith

/- Theory 73, formula 73.18: elementary averaged-scale logarithm relation.
   The positivity premise excludes the degenerate Q=T=1 denominator. -/
theorem jutila_cj_averaged_log_ratio_half
    {q Q T L : ℝ}
    (hq : 0 < q) (hQ : 1 ≤ Q) (hT : 1 ≤ T)
    (hqUpper : q ≤ Q) (hL : L = Real.log (Q ^ 2 * T))
    (hLPos : 0 < L) :
    Real.log q / L ≤ 1 / 2 := by
  have hQPos : 0 < Q := lt_of_lt_of_le zero_lt_one hQ
  have hTPos : 0 < T := lt_of_lt_of_le zero_lt_one hT
  have hLogqQ : Real.log q ≤ Real.log Q := Real.log_le_log hq hqUpper
  have hLogT : 0 ≤ Real.log T := Real.log_nonneg hT
  have hLogScale : Real.log (Q ^ 2 * T) = 2 * Real.log Q + Real.log T := by
    rw [Real.log_mul (pow_ne_zero 2 hQPos.ne') hTPos.ne', Real.log_pow]
    norm_num
  have hTwice : 2 * Real.log q ≤ L := by
    rw [hL, hLogScale]
    linarith
  rw [div_le_iff₀ hLPos]
  linarith

/- Theory 73, formula 73.20: a six-term Mathlib exponential remainder
   bound proves the rational averaged-scale envelope. -/
theorem jutila_cj_exp_endpoint_envelope :
    Real.exp (23 / 42 : ℝ) * (442 / 441) < 7 / 4 := by
  have hExp := Real.exp_bound'
    (x := (23 / 42 : ℝ)) (by norm_num) (by norm_num)
    (n := 6) (by norm_num)
  norm_num [Finset.sum_range_succ, Nat.factorial] at hExp ⊢
  nlinarith

/- Theory 73, formula 73.22: exact endpoint integration-area lower atom. -/
theorem jutila_cj_area_endpoint :
    (1 / 21 : ℝ) ^ 2 * (1 / 2 + 7 * (1 / 21)) *
        (1 + 12 * (1 / 21)) = 55 / 18522 := by
  norm_num

/- Theory 73, formula 73.23: arbitrary strict absorption margin.  All
   analytic estimates are explicit premises, so this theorem verifies only
   the terminal ordered-field implication. -/
theorem jutila_cj_arbitrary_absorption_terminal
    {A B E J Y m : ℝ}
    (hA : 0 < A)
    (hm : 1 < m) (hE : E ≤ A / m) (hJ : 0 < J)
    (hInequality : A * J ^ 2 ≤ B * J * Y + E * J ^ 2) :
    J ≤ (m / (m - 1)) * B * Y / A := by
  have hmPos : 0 < m := lt_trans zero_lt_one hm
  have hmSubPos : 0 < m - 1 := sub_pos.mpr hm
  have hALower : ((m - 1) / m) * A ≤ A - E := by
    have hScaled : E ≤ A / m := hE
    rw [div_eq_mul_inv] at hScaled
    calc
      ((m - 1) / m) * A = A - A / m := by field_simp
      _ ≤ A - E := sub_le_sub_left hScaled A
  have hAbsorbed : (A - E) * J ^ 2 ≤ B * J * Y := by
    nlinarith
  have hLowerTimes : (((m - 1) / m) * A) * J ^ 2 ≤ B * J * Y :=
    le_trans (mul_le_mul_of_nonneg_right hALower (sq_nonneg J)) hAbsorbed
  have hDenPos : 0 < ((m - 1) / m) * A * J := by positivity
  have hLowerTimes' :
      J * (((m - 1) / m) * A * J) ≤ B * J * Y := by
    calc
      J * (((m - 1) / m) * A * J) =
          (((m - 1) / m) * A) * J ^ 2 := by ring
      _ ≤ B * J * Y := hLowerTimes
  have hDivide :
      J ≤ B * J * Y / (((m - 1) / m) * A * J) :=
    (le_div_iff₀ hDenPos).2 hLowerTimes'
  calc
    J ≤ B * J * Y / (((m - 1) / m) * A * J) := hDivide
    _ = (m / (m - 1)) * B * Y / A := by field_simp

/- Theory 73, formulas 73.4 and 73.14--73.24: exact composition of the
   tightened endpoint factors with m=10^6.  Analytic premises producing the
   individual bounds remain separately classified. -/
theorem jutila_cj_tightened_endpoint_coefficient :
    (1000000 / 999999 : ℝ) * (710 / 171) * (8 / 5) *
          (15665428311 / 1750000) /
          (4 / 147) ^ 2 /
          (55 / 18522) =
      11503697604450072 / 425315 := by
  norm_num

/- Theory 73, formula 73.5: exact improvement factor before its decimal
   diagnostic is printed. -/
theorem jutila_cj_exact_improvement_factor :
    (9287613243090 : ℝ) /
        (11503697604450072 / 425315) =
      2304222695775 / 6710379548 := by
  norm_num

/- Theory 73, formulas 73.4--73.7 and 73.29: exact coarse structural
   comparisons.  They deliberately avoid treating decimal transcendental
   diagnostics as directed certificates. -/
theorem jutila_cj_tightened_still_large :
    (27000000000 : ℝ) < 11503697604450072 / 425315 := by
  norm_num

theorem jutila_cj_theta_power_endpoint :
    ((1 / 21 : ℝ) ^ 6)⁻¹ = 85766121 := by
  norm_num

/- Theory 73, formula 73.26: exact endpoint exponents entering the
   unit-C_J near kernel. -/
theorem jutila_cj_capacity_endpoint_exponents :
    (1 : ℝ) - 14 * (1 + 12 * (1 / 21)) / 186 = 82 / 93 ∧
      (82 / 93 : ℝ) * (1 / 24) * 186 / 5 = 1271 / 930 ∧
      (82 / 93 : ℝ) * 186 / 7 = 164 / 7 := by
  norm_num

/- Theory 74, formula 74.11: exact arithmetic after the Ramaré source
   theorem is specialized to Q=X^(1/d), T=Q^5, d=186 and c1=1/24.
   This does not formalize the analytic density theorem itself. -/
theorem dep_r09_modern_ramare_endpoint_arithmetic :
    (1 : ℝ) - 20 / 186 = 83 / 93 ∧
      (2 / 186 : ℝ) = 1 / 93 ∧
      (1 / 24 : ℝ) * 186 / 5 = 31 / 20 := by
  norm_num

/- Theory 74, formula 74.15 and the Friedlander--Iwaniec comparison in
   formula 74.17: integer exponent-capacity checks only. -/
theorem dep_r09_modern_exponent_gate :
    (99 : ℕ) ≤ 186 ∧
      (170 : ℕ) ≤ 186 ∧
      ¬ (198 : ℕ) ≤ 186 ∧
      ¬ (52600 : ℕ) ≤ 186 := by
  norm_num

/- Theory 74, formula 74.18 and the coefficient comparison following
   formula 74.17.  The external sieve premises remain unformalized. -/
theorem dep_r09_modern_fi_arithmetic :
    80 * 18 * 52600 = (75744000 : ℕ) ∧
      (1 / 210000 : ℝ) < 4 / 5 := by
  norm_num

/- Theory 75, formulas 75.5--75.7: elementary endpoint arithmetic for the
   first y-slice and a coarse rational separation between the computed
   certificate floor and the positive PAP budget.  The transcendental
   numerical bounds are kept outside Lean as high-precision diagnostics. -/
theorem dep_r09_transfer_endpoint_arithmetic :
    (1 / 24 : ℝ) * 186 / 5 + 1 = 51 / 20 ∧
      (21 : ℕ) ≤ 186 ∧
      (1 / 8602 : ℝ) < 1 / 7 := by
  norm_num

/- Theory 75, formula 75.4: min is monotone in both certified upper bounds.
   This only verifies the ordered-field composition, not either analytic
   density premise. -/
theorem dep_r09_hybrid_min_monotone
    {R J rLower jLower : ℝ}
    (hR : rLower ≤ R) (hJ : jLower ≤ J) :
    min rLower jLower ≤ min R J := by
  exact min_le_min hR hJ

/- Theory 75, formula 75.15: if a pre-absolute-value Cauchy estimate and the
   required second-moment budget are supplied as explicit premises, the
   residue-class normalization has exactly the desired scale.  This theorem
   does not assert that the missing analytic second-moment estimate exists. -/
theorem dep_r09_cancellation_second_moment_terminal
    {phi epsilon X z secondMoment : ℝ}
    (hPhi : 0 < phi) (hEpsilon : 0 ≤ epsilon) (hX : 0 ≤ X)
    (hCauchy : z ^ 2 ≤ phi * secondMoment)
    (hSecondMoment : secondMoment ≤ epsilon ^ 2 * X ^ 2 / phi) :
    |z / phi| ≤ epsilon * X / phi := by
  have hSquare : z ^ 2 ≤ (epsilon * X) ^ 2 := by
    calc
      z ^ 2 ≤ phi * secondMoment := hCauchy
      _ ≤ phi * (epsilon ^ 2 * X ^ 2 / phi) :=
        mul_le_mul_of_nonneg_left hSecondMoment hPhi.le
      _ = (epsilon * X) ^ 2 := by
        field_simp
  have hScale : 0 ≤ epsilon * X := mul_nonneg hEpsilon hX
  have hUpper : z ≤ epsilon * X := by
    by_contra hNot
    have hStrict : epsilon * X < z := lt_of_not_ge hNot
    nlinarith
  have hLower : -(epsilon * X) ≤ z := by
    by_contra hNot
    have hStrict : z < -(epsilon * X) := lt_of_not_ge hNot
    nlinarith
  have hAbs : |z| ≤ epsilon * X := (abs_le).2 ⟨hLower, hUpper⟩
  rw [abs_div, abs_of_pos hPhi]
  exact (div_le_div_iff_of_pos_right hPhi).2 hAbs

/-! ## Theory 76 — DEP-R09 pre-absolute-value moment and pointwise PNT audit -/

/- Theory 76, formula 76.15: once the normalized Bennett large-q cutoff and
   the elementary lower inputs sqrt(q) ≥ 300 and log(q) ≥ 10 are supplied,
   it cannot coexist with d ≤ 186.  This does not prove the analytic source
   cutoff or the logarithm/square-root lower inputs inside Lean. -/
theorem dep_r09_bennett_cutoff_capacity_terminal
    {d sqrtQ logQ : ℝ}
    (hd : d ≤ 186)
    (hSqrtQ : 300 ≤ sqrtQ)
    (hLogQ : 10 ≤ logQ)
    (hCutoff : (3 / 100 : ℝ) * sqrtQ * logQ ^ 2 ≤ d) : False := by
  have hSqrtQNonneg : 0 ≤ sqrtQ := by linarith
  have hLogQSquare : (100 : ℝ) ≤ logQ ^ 2 := by nlinarith
  have hProduct : (30000 : ℝ) ≤ sqrtQ * logQ ^ 2 := by
    calc
      (30000 : ℝ) = 300 * 100 := by norm_num
      _ ≤ sqrtQ * 100 := mul_le_mul_of_nonneg_right hSqrtQ (by norm_num)
      _ ≤ sqrtQ * logQ ^ 2 :=
        mul_le_mul_of_nonneg_left hLogQSquare hSqrtQNonneg
  have hNineHundred : (900 : ℝ) ≤ (3 / 100 : ℝ) * sqrtQ * logQ ^ 2 := by
    nlinarith
  linarith

/- Theory 76, formulas 76.22--76.23: an aggregate Cauchy estimate and the
   M-times-larger second-moment budget imply the desired aggregate residue
   error.  The character orthogonality and analytic moment estimate are
   explicit premises, not project-local axioms. -/
theorem dep_r09_aggregate_second_moment_terminal
    {phi epsilon Y M z secondMoment : ℝ}
    (hPhi : 0 < phi)
    (hEpsilon : 0 ≤ epsilon)
    (hY : 0 ≤ Y)
    (hM : 0 ≤ M)
    (hCauchy : z ^ 2 ≤ (M / phi) * secondMoment)
    (hSecondMoment : secondMoment ≤ epsilon ^ 2 * M * Y ^ 2 / phi) :
    |z| ≤ epsilon * M * Y / phi := by
  have hRatio : 0 ≤ M / phi := div_nonneg hM hPhi.le
  have hSquare : z ^ 2 ≤ (epsilon * M * Y / phi) ^ 2 := by
    calc
      z ^ 2 ≤ (M / phi) * secondMoment := hCauchy
      _ ≤ (M / phi) * (epsilon ^ 2 * M * Y ^ 2 / phi) :=
        mul_le_mul_of_nonneg_left hSecondMoment hRatio
      _ = (epsilon * M * Y / phi) ^ 2 := by
        field_simp [ne_of_gt hPhi]
  have hTarget : 0 ≤ epsilon * M * Y / phi := by positivity
  have hUpper : z ≤ epsilon * M * Y / phi := by
    by_contra hNot
    have hStrict : epsilon * M * Y / phi < z := lt_of_not_ge hNot
    nlinarith
  have hLower : -(epsilon * M * Y / phi) ≤ z := by
    by_contra hNot
    have hStrict : z < -(epsilon * M * Y / phi) := lt_of_not_ge hNot
    nlinarith
  exact (abs_le).2 ⟨hLower, hUpper⟩

/-! ## Theory 77 — DEP-R09 restricted-residue variance and spectral audit -/

/- Theory 77, formulas 77.7--77.9: after finite character orthogonality
   supplies total energy phi*M and the principal character contributes M^2,
   the nonprincipal energy is exactly M*(phi-M).  The character-theory
   premise itself is not asserted as a project-local axiom. -/
theorem dep_r09_nonprincipal_character_energy_identity
    {phi M : ℝ} :
    phi * M - M ^ 2 = M * (phi - M) := by
  ring

/- Theory 77, formulas 77.12--77.13: a principal-separated Cauchy premise
   and the stated nonprincipal moment budget imply the weighted numerator
   target.  No analytic estimate for secondMoment is asserted here. -/
theorem dep_r09_principal_separated_moment_terminal
    {epsilon delta M phi Y z secondMoment : ℝ}
    (hDelta : delta ≤ epsilon)
    (hM : 0 ≤ M)
    (hY : 0 ≤ Y)
    (hCauchy : z ^ 2 ≤ M * (phi - M) * secondMoment)
    (hMoment :
      secondMoment * (phi - M) ≤
        (epsilon - delta) ^ 2 * M * Y ^ 2) :
    |z| ≤ (epsilon - delta) * M * Y := by
  have hSquare : z ^ 2 ≤ ((epsilon - delta) * M * Y) ^ 2 := by
    calc
      z ^ 2 ≤ M * (phi - M) * secondMoment := hCauchy
      _ = M * (secondMoment * (phi - M)) := by ring
      _ ≤ M * ((epsilon - delta) ^ 2 * M * Y ^ 2) :=
        mul_le_mul_of_nonneg_left hMoment hM
      _ = ((epsilon - delta) * M * Y) ^ 2 := by ring
  have hRemaining : 0 ≤ epsilon - delta := sub_nonneg.2 hDelta
  have hTarget : 0 ≤ (epsilon - delta) * M * Y := by
    exact mul_nonneg (mul_nonneg hRemaining hM) hY
  have hUpper : z ≤ (epsilon - delta) * M * Y := by
    by_contra hNot
    have hStrict : (epsilon - delta) * M * Y < z := lt_of_not_ge hNot
    nlinarith
  have hLower : -((epsilon - delta) * M * Y) ≤ z := by
    by_contra hNot
    have hStrict : z < -((epsilon - delta) * M * Y) := lt_of_not_ge hNot
    nlinarith
  exact (abs_le).2 ⟨hLower, hUpper⟩

/- Theory 77, formulas 77.15--77.16: the scalar equality behind an error
   vector aligned with the conjugate coefficient vector.  This proves only
   that an argument using total L2 energy alone cannot improve Cauchy's
   universal constant; it does not assert alignment for prime errors. -/
theorem dep_r09_cauchy_alignment_scalar_equality
    (energy scale : ℝ) :
    (energy * scale) ^ 2 = energy * (energy * scale ^ 2) := by
  ring

/- Theory 77, formula 77.17: exact endpoint substitutions delta=1/d in
   1/2+delta/2.  Fiorilli--Martin Proposition 2.2 is an external analytic
   source statement and is not formalized by these arithmetic equalities. -/
theorem dep_r09_power_regime_zero_free_endpoint_arithmetic :
    (1 / 2 : ℝ) + 1 / (2 * 21) = 11 / 21 ∧
      (1 / 2 : ℝ) + 1 / (2 * 186) = 187 / 372 := by
  norm_num

/-! ## Theory 78 — DEP-R09 Maier/FMT CRT-shift quantifier audit -/

/- Theory 78, formulas 78.8--78.9: if the sum of the cardinalities of
   three bad sets is strictly smaller than the finite candidate family,
   one candidate lies outside all three.  This is only finite selection
   logic; it does not assert the analytic bounds on the bad sets. -/
theorem dep_r09_three_bad_finsets_leave_candidate
    {α : Type*} [Fintype α]
    (B₁ B₂ B₃ : Finset α)
    (hBudget : B₁.card + B₂.card + B₃.card < Fintype.card α) :
    ∃ candidate : α,
      candidate ∉ B₁ ∧ candidate ∉ B₂ ∧ candidate ∉ B₃ := by
  classical
  by_contra hNoCandidate
  have hCovered : ∀ candidate : α,
      candidate ∈ B₁ ∨ candidate ∈ B₂ ∨ candidate ∈ B₃ := by
    intro candidate
    by_contra hNotCovered
    have h₁ : candidate ∉ B₁ := by
      intro hMem
      exact hNotCovered (Or.inl hMem)
    have h₂ : candidate ∉ B₂ := by
      intro hMem
      exact hNotCovered (Or.inr (Or.inl hMem))
    have h₃ : candidate ∉ B₃ := by
      intro hMem
      exact hNotCovered (Or.inr (Or.inr hMem))
    exact hNoCandidate ⟨candidate, h₁, h₂, h₃⟩
  have hSubset : (Finset.univ : Finset α) ⊆ B₁ ∪ B₂ ∪ B₃ := by
    intro candidate _
    rcases hCovered candidate with h₁ | h₂ | h₃
    · simp [h₁]
    · simp [h₂]
    · simp [h₃]
  have hUniverseCard :
      Fintype.card α ≤ (B₁ ∪ B₂ ∪ B₃).card := by
    simpa using Finset.card_le_card hSubset
  have hUnionCard :
      (B₁ ∪ B₂ ∪ B₃).card ≤ B₁.card + B₂.card + B₃.card := by
    calc
      (B₁ ∪ B₂ ∪ B₃).card ≤ (B₁ ∪ B₂).card + B₃.card :=
        Finset.card_union_le (B₁ ∪ B₂) B₃
      _ ≤ (B₁.card + B₂.card) + B₃.card :=
        Nat.add_le_add_right (Finset.card_union_le B₁ B₂) B₃.card
      _ = B₁.card + B₂.card + B₃.card := rfl
  omega

/- Theory 78, formula 78.11: a singleton candidate family can satisfy the
   strict cardinal union budget only when every bad-set count is zero. -/
theorem dep_r09_singleton_bad_budget_forces_zero
    {b₁ b₂ b₃ : ℕ}
    (hBudget : b₁ + b₂ + b₃ < 1) :
    b₁ = 0 ∧ b₂ = 0 ∧ b₃ = 0 := by
  omega

/-! ## Theory 79 — DEP-R09 FMT construction-law finite mass audit -/

/- Theory 79, formula 79.7: exact algebra for the two-stage sieve-failure
   upper bound.  The analytic outer and conditional-inner bounds are inputs;
   this theorem neither asserts independence nor proves those inputs. -/
theorem dep_r09_two_stage_failure_identity
    (fOut fIn : ℝ) :
    fOut + (1 - fOut) * fIn =
      1 - (1 - fOut) * (1 - fIn) := by
  ring

/- Theory 79, formulas 79.9--79.10: a same-law correlation-failure upper
   bound strictly below the two-stage sieve-good lower bound leaves positive
   mass.  This is only the terminal real inequality. -/
theorem dep_r09_joint_correlation_budget_positive
    {fOut fIn fCorr : ℝ}
    (hCorr : fCorr < (1 - fOut) * (1 - fIn)) :
    0 < (1 - fOut) * (1 - fIn) - fCorr :=
  sub_pos.mpr hCorr

/- Theory 79, formula 79.11: the cruder three-failure union gate implies the
   product gate when the two sequential failure bounds are nonnegative. -/
theorem dep_r09_crude_union_gate_implies_product_gate
    {fOut fIn fCorr : ℝ}
    (hOutNonneg : 0 ≤ fOut)
    (hInNonneg : 0 ≤ fIn)
    (hCrude : fOut + fIn + fCorr < 1) :
    fCorr < (1 - fOut) * (1 - fIn) := by
  nlinarith [mul_nonneg hOutNonneg hInNonneg]

/- Theory 79, formula 79.12: inside one finite conditional fiber, if the
   sum of two bad-set cardinalities is smaller than the candidate fiber, one
   inner outcome avoids both. -/
theorem dep_r09_two_bad_finsets_leave_candidate
    {β : Type*}
    (Ω BIn BCorr : Finset β)
    (hBudget : BIn.card + BCorr.card < Ω.card) :
    ∃ inner ∈ Ω, inner ∉ BIn ∧ inner ∉ BCorr := by
  classical
  by_contra hNoCandidate
  have hCovered : ∀ inner ∈ Ω, inner ∈ BIn ∨ inner ∈ BCorr := by
    intro inner hInner
    by_cases hIn : inner ∈ BIn
    · exact Or.inl hIn
    by_cases hCorr : inner ∈ BCorr
    · exact Or.inr hCorr
    · exact False.elim (hNoCandidate ⟨inner, hInner, hIn, hCorr⟩)
  have hSubset : Ω ⊆ BIn ∪ BCorr := by
    intro inner hInner
    rcases hCovered inner hInner with hIn | hCorr
    · simp [hIn]
    · simp [hCorr]
  have hOmegaCard : Ω.card ≤ (BIn ∪ BCorr).card :=
    Finset.card_le_card hSubset
  have hUnionCard :
      (BIn ∪ BCorr).card ≤ BIn.card + BCorr.card :=
    Finset.card_union_le BIn BCorr
  omega

/- Theory 79, formula 79.12: first choose an outer outcome outside the outer
   bad set, then use the preceding finite lemma in its conditional fiber.
   No outer/inner independence statement is present. -/
theorem dep_r09_outer_then_two_inner_bad_finsets_leave_pair
    {α β : Type*} [Fintype α]
    (BOut : Finset α)
    (ΩInner BIn BCorr : α → Finset β)
    (hOut : BOut.card < Fintype.card α)
    (hFiber : ∀ outer, outer ∉ BOut →
      (BIn outer).card + (BCorr outer).card < (ΩInner outer).card) :
    ∃ outer, outer ∉ BOut ∧
      ∃ inner ∈ ΩInner outer,
        inner ∉ BIn outer ∧ inner ∉ BCorr outer := by
  classical
  have hOuterBudget :
      BOut.card + (∅ : Finset α).card + (∅ : Finset α).card <
        Fintype.card α := by
    simpa using hOut
  obtain ⟨outer, hOuter, _, _⟩ :=
    dep_r09_three_bad_finsets_leave_candidate
      BOut (∅ : Finset α) (∅ : Finset α) hOuterBudget
  obtain ⟨inner, hInner, hIn, hCorr⟩ :=
    dep_r09_two_bad_finsets_leave_candidate
      (ΩInner outer) (BIn outer) (BCorr outer) (hFiber outer hOuter)
  exact ⟨outer, hOuter, inner, hInner, hIn, hCorr⟩

/-! ## Theory 80 — DEP-R09 same-law weighted-correlation tower audit -/

/- Theory 80, formula 80.10: finite conditional-expectation expansion equals
   the flat joint-atom sum.  The functions are abstract finite weights; this
   proves no analytic character-sum estimate. -/
theorem dep_r09_finite_tower_sum_identity
    {α β : Type*} [Fintype α] [Fintype β]
    (pA : α → ℝ) (pN : α → β → ℝ) (W : α → β → ℝ) :
    (∑ outer : α,
      pA outer * (∑ inner : β, pN outer inner * W outer inner)) =
      ∑ outer : α, ∑ inner : β,
        (pA outer * pN outer inner) * W outer inner := by
  apply Finset.sum_congr rfl
  intro outer _hOuter
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro inner _hInner
  ring

/- Theory 80, formulas 80.13--80.14: a global outer-good normalized moment
   below the squared correlation budget times the sieve-good mass leaves
   positive terminal mass.  Markov and both analytic probability bounds are
   external premises represented by hLower and hGate. -/
theorem dep_r09_global_same_law_moment_terminal
    {fOut fIn mu tau pSuccess : ℝ}
    (hTau : 0 < tau)
    (hLower :
      (1 - fOut) * (1 - fIn) - mu / tau ^ 2 ≤ pSuccess)
    (hGate :
      mu < tau ^ 2 * ((1 - fOut) * (1 - fIn))) :
    0 < pSuccess := by
  have hTauSq : 0 < tau ^ 2 := sq_pos_of_pos hTau
  have hRatio : mu / tau ^ 2 < (1 - fOut) * (1 - fIn) := by
    apply (div_lt_iff₀ hTauSq).2
    simpa only [mul_assoc, mul_left_comm, mul_comm] using hGate
  exact lt_of_lt_of_le (sub_pos.mpr hRatio) hLower

/- Theory 80, formulas 80.16--80.17: positive outer mass and the strict
   conditional moment gate give positive product slack.  The conditional
   Markov estimate itself is not asserted. -/
theorem dep_r09_conditional_same_law_moment_terminal
    {fOut fIn muOuter tau : ℝ}
    (_hTau : 0 < tau)
    (hOut : fOut < 1)
    (hGate : fIn + muOuter / tau ^ 2 < 1) :
    0 < (1 - fOut) * (1 - fIn - muOuter / tau ^ 2) := by
  have hOuterMass : 0 < 1 - fOut := by linarith
  have hConditionalMass : 0 < 1 - fIn - muOuter / tau ^ 2 := by
    linarith
  exact mul_pos hOuterMass hConditionalMass

/- Theory 80, formula 80.21: the raw second-moment normalization uses the
   pointwise survivor floor and prime scale through the exact squared
   denominator identity. -/
theorem dep_r09_raw_moment_denominator_identity
    (rho minimumSurvivors primeScale : ℝ) :
    rho / (minimumSurvivors ^ 2 * primeScale ^ 2) =
      rho / (minimumSurvivors * primeScale) ^ 2 := by
  congr 1
  ring

/- Theory 80, formula 80.21: division by the strictly positive pointwise
   survivor-floor denominator preserves a supplied raw second-moment upper
   bound.  The raw analytic moment and survivor floor remain premises. -/
theorem dep_r09_raw_to_normalized_moment_terminal
    {rawMoment rho minimumSurvivors primeScale : ℝ}
    (hRaw : rawMoment ≤ rho)
    (hMinimum : 0 < minimumSurvivors)
    (hScale : 0 < primeScale) :
    rawMoment / (minimumSurvivors ^ 2 * primeScale ^ 2) ≤
      rho / (minimumSurvivors ^ 2 * primeScale ^ 2) := by
  have hDenominator :
      0 < minimumSurvivors ^ 2 * primeScale ^ 2 :=
    mul_pos (sq_pos_of_pos hMinimum) (sq_pos_of_pos hScale)
  exact (div_le_div_iff_of_pos_right hDenominator).2 hRaw

/-! ## Theory 81 — DEP-R09 filtration sensitivity and survivor floor -/

/- Theory 81, formula 81.4: the final sieve-good survivor floor is strictly
   positive once the source parameters A, 1-eta, and X/log X are positive.
   This theorem proves only the terminal algebra; membership in the final
   sieve-good event is the audited source premise. -/
theorem dep_r09_sieve_good_survivor_floor_positive
    {A eta xOverLogX : ℝ}
    (hA : 0 < A) (hEta : eta < 1) (hXScale : 0 < xOverLogX) :
    0 < A * (1 - eta) * xOverLogX := by
  exact mul_pos (mul_pos hA (sub_pos.mpr hEta)) hXScale

/- Theory 81, formulas 81.9--81.10: a raw second moment restricted to the
   same final sieve-good event can be normalized by its pointwise floor.
   The analytic raw-moment estimate remains an external premise. -/
theorem dep_r09_sieve_good_raw_normalization_terminal
    {rawMoment rho minimumSurvivors primeScale : ℝ}
    (hRaw : rawMoment ≤ rho)
    (hMinimum : 0 < minimumSurvivors)
    (hScale : 0 < primeScale) :
    rawMoment / (minimumSurvivors ^ 2 * primeScale ^ 2) ≤
      rho / (minimumSurvivors ^ 2 * primeScale ^ 2) := by
  exact dep_r09_raw_to_normalized_moment_terminal hRaw hMinimum hScale

/- Theory 81, formulas 81.7--81.8: the corrected sieve-good normalized
   moment gate leaves positive mass.  The probability/Markov lower bound is
   represented by hLower and is not asserted as a new analytic theorem. -/
theorem dep_r09_sieve_good_moment_terminal
    {fOut fIn muS tau pSuccess : ℝ}
    (hTau : 0 < tau)
    (hLower :
      (1 - fOut) * (1 - fIn) - muS / tau ^ 2 ≤ pSuccess)
    (hGate :
      muS < tau ^ 2 * ((1 - fOut) * (1 - fIn))) :
    0 < pSuccess := by
  exact dep_r09_global_same_law_moment_terminal hTau hLower hGate

/- Theory 81, formulas 81.15--81.16: once symmetric-difference containment
   supplies the two one-sided count inequalities, its cardinality bound
   controls the absolute survivor-count difference. -/
theorem dep_r09_survivor_count_sensitivity_terminal
    {oldCount newCount symmDiff bound : ℝ}
    (hOldNew : oldCount - newCount ≤ symmDiff)
    (hNewOld : newCount - oldCount ≤ symmDiff)
    (hSymm : symmDiff ≤ bound) :
    |oldCount - newCount| ≤ bound := by
  have hAbs : |oldCount - newCount| ≤ symmDiff := by
    rw [abs_le]
    constructor <;> linarith
  exact hAbs.trans hSymm

/- Theory 81, formulas 81.18--81.19: exact arithmetic of the P=65 toy
   witness.  Python separately evaluates the finite Dirichlet-character
   values; this theorem checks that their two sums differ by 3, exceeding
   the survivor-membership bound 2. -/
theorem dep_r09_character_phase_counterexample_arithmetic :
    |((1 : ℤ) + 0 + 1) - (1 + (-1) + (-1))| > 2 := by
  norm_num

/-! ## Theory 82 — DEP-R09 outer entropy and convolution second moment -/

/- Theory 82, formulas 82.16--82.17: once the event-and-shift atom cap
   supplies rawMoment <= shiftEnergy/Q and the finite convolution argument
   supplies shiftEnergy <= phi*N^2*V, division by positive Q preserves the
   combined raw-moment upper bound.  Neither analytic premise is asserted
   by this scalar terminal theorem. -/
theorem dep_r09_outer_entropy_raw_moment_terminal
    {rawMoment shiftEnergy phi N V Q : ℝ}
    (hQ : 0 < Q)
    (hAtom : rawMoment ≤ shiftEnergy / Q)
    (hEnergy : shiftEnergy ≤ phi * N ^ 2 * V) :
    rawMoment ≤ phi * N ^ 2 * V / Q := by
  exact hAtom.trans (div_le_div_of_nonneg_right hEnergy hQ.le)

/- Theory 82, formulas 82.3 and 82.17--82.19: the strict
   character-energy gate implies the corrected Theory-81 normalized
   moment gate.  The outer atom cap, finite Parseval/convolution estimate,
   survivor floor, and analytic estimate for V remain audited premises. -/
theorem dep_r09_outer_entropy_character_energy_gate
    {rawMoment V phi N Q minimumSurvivors primeScale tau pStar : ℝ}
    (hPhi : 0 < phi)
    (hN : 0 < N)
    (hQ : 0 < Q)
    (hMinimum : 0 < minimumSurvivors)
    (hScale : 0 < primeScale)
    (hRaw : rawMoment ≤ phi * N ^ 2 * V / Q)
    (hV :
      V <
        tau ^ 2 * pStar * Q * minimumSurvivors ^ 2 * primeScale ^ 2 /
          (phi * N ^ 2)) :
    rawMoment / (minimumSurvivors ^ 2 * primeScale ^ 2) <
      tau ^ 2 * pStar := by
  have hN2 : 0 < N ^ 2 := sq_pos_of_pos hN
  have hPhiN2 : 0 < phi * N ^ 2 := mul_pos hPhi hN2
  have hMinimum2 : 0 < minimumSurvivors ^ 2 :=
    sq_pos_of_pos hMinimum
  have hScale2 : 0 < primeScale ^ 2 := sq_pos_of_pos hScale
  have hDenominator :
      0 < minimumSurvivors ^ 2 * primeScale ^ 2 :=
    mul_pos hMinimum2 hScale2
  have hVScaled :
      V * (phi * N ^ 2) <
        tau ^ 2 * pStar * Q * minimumSurvivors ^ 2 * primeScale ^ 2 :=
    (lt_div_iff₀ hPhiN2).mp hV
  have hModelStrict :
      phi * N ^ 2 * V / Q <
        (tau ^ 2 * pStar) *
          (minimumSurvivors ^ 2 * primeScale ^ 2) := by
    apply (div_lt_iff₀ hQ).2
    simpa only [mul_assoc, mul_left_comm, mul_comm] using hVScaled
  have hRawStrict :
      rawMoment <
        (tau ^ 2 * pStar) *
          (minimumSurvivors ^ 2 * primeScale ^ 2) :=
    lt_of_le_of_lt hRaw hModelStrict
  exact (div_lt_iff₀ hDenominator).2 hRawStrict

/-! ## Theory 83 — fixed-primorial variance and large-sieve barrier -/

/- Theory 83, formula 83.19: the power-regime inequalities L >= 21t and
   log(2) < t give the strict elementary lower margin
   5t < (L-log(2))/4.  The identification of L and t with real logarithms
   and the Dusart input remain source-level premises. -/
theorem dep_r09_power_regime_large_sieve_margin
    {t L logTwo : ℝ}
    (hPower : 21 * t ≤ L)
    (hLogTwo : logTwo < t) :
    5 * t < (L - logTwo) / 4 := by
  linarith

/- Theory 83, formula 83.15a: the rational lower certificate for the
   Dusart half-interval coefficient at L=8 is strictly above one quarter.
   Monotonicity of the real-log expression and the source theta theorem are
   intentionally not asserted here. -/
theorem dep_r09_dusart_log8_rational_margin :
    (1 / 2 : ℝ) - 12323 / 80000 - (5 * 12323) / (73 * 10000) > 1 / 4 := by
  norm_num

/- Theory 83, formula 83.22: multiplying four favourable factor bounds
   preserves the maximum entropy-gate envelope.  This is only finite real
   algebra; the actual FMT probability and survivor inputs remain external. -/
theorem dep_r09_best_entropy_gate_factor_bound
    {tauSq pStar entropyRatio survivorRatio epsilonSq qOverPhi ySq : ℝ}
    (hTau0 : 0 ≤ tauSq)
    (hP0 : 0 ≤ pStar)
    (hEntropy0 : 0 ≤ entropyRatio)
    (hSurvivor0 : 0 ≤ survivorRatio)
    (hY0 : 0 ≤ ySq)
    (hTau : tauSq ≤ epsilonSq)
    (hP : pStar ≤ 1)
    (hEntropy : entropyRatio ≤ qOverPhi)
    (hSurvivor : survivorRatio ≤ 1) :
    tauSq * pStar * entropyRatio * survivorRatio * ySq ≤
      epsilonSq * qOverPhi * ySq := by
  have hEpsilon0 : 0 ≤ epsilonSq := hTau0.trans hTau
  have hQOverPhi0 : 0 ≤ qOverPhi := hEntropy0.trans hEntropy
  calc
    tauSq * pStar * entropyRatio * survivorRatio * ySq ≤
        epsilonSq * pStar * entropyRatio * survivorRatio * ySq := by
      gcongr
    _ ≤ epsilonSq * 1 * entropyRatio * survivorRatio * ySq := by
      gcongr
    _ ≤ epsilonSq * 1 * qOverPhi * survivorRatio * ySq := by
      gcongr
    _ ≤ epsilonSq * 1 * qOverPhi * 1 * ySq := by
      gcongr
    _ = epsilonSq * qOverPhi * ySq := by
      ring

/- Theory 83, formulas 83.4 and 83.22: if the sufficient gate is below its
   best-case envelope while that envelope is below a published certificate
   RHS, then the gate itself is below that RHS. -/
theorem dep_r09_large_sieve_rhs_above_gate_terminal
    {gate envelope rhs : ℝ}
    (hGate : gate ≤ envelope)
    (hEnvelope : envelope < rhs) :
    gate < rhs := by
  exact lt_of_le_of_lt hGate hEnvelope

/- Theory 83, formula 83.29: an upper certificate V <= rhs with rhs at or
   above the strict target gate does not logically imply V < gate.  The
   witness V=gate proves the exact countermodel without asserting anything
   about the actual prime-error energy. -/
theorem dep_r09_upper_certificate_above_gate_countermodel
    {gate rhs : ℝ}
    (hGateRhs : gate ≤ rhs) :
    ∃ V : ℝ, V ≤ rhs ∧ ¬ V < gate := by
  exact ⟨gate, hGateRhs, lt_irrefl gate⟩

end FGKMTSono
