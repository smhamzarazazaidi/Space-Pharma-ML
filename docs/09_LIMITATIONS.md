# 09. Research Limitations & Domain Boundaries

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Primary Reference:** [`docs/RESEARCH_DOCUMENT.md`](file:///d:/Space%20medicne/docs/RESEARCH_DOCUMENT.md) (Section 17)

---

## 1. Experimental & Dataset Limitations
* **Small Sample Regime ($n$):** Due to strict launch mass, volume, and cost constraints, historical spaceflight pharmaceutical experiments feature small sample sizes ($n < 1000$).
* **Environmental Confounding:** Differences in stowage lockers, microgravity quality, and temperature fluctuations across historical missions introduce unmeasured variance.
* **Scarcity of In-Flight Human PK/PD:** Most available datasets measure in vitro chemical stability (% active ingredient remaining) rather than dynamic human pharmacokinetics or pharmacodynamics.

## 2. Modeling & Extrapolation Boundaries
* **Low Earth Orbit (LEO) vs. Deep Space:** ISS radiation profiles (dominated by trapped protons and low-dose GCR under geomagnetic shielding) do not fully replicate the heavy-ion Galactic Cosmic Ray (GCR) flux of deep-space transit to Mars.
* **Empirical Nature of Discovered Formulas:** Formulas derived via symbolic regression represent empirical model-derived approximations rather than fundamental physical constants.
* **No Regulatory/Clinical Certification:** This research provides computational hypotheses and risk prioritization frameworks; it does not replace official pharmacopeial stability testing.
