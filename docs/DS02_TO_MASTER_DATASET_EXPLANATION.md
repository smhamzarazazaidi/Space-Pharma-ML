# Scientific Explanation: Linking DS-02 Space Radiation to the Master Dataset

## 1. What is DS-02?
**DS-02** is the real-world ambient ionizing radiation telemetry collected aboard the International Space Station (ISS) by the **DOSIS 3D** experiment (ESA/DLR) located in the European Columbus orbital module. The data was acquired through NASA's Open Science Data Repository (OSDR) RadLab system.

## 2. What Does DosTel Measure?
DosTel consists of two semiconductor silicon telescope detectors (**DosTel1** and **DosTel2**) that measure the **absorbed dose rate** ($\mu\text{Gy/hour}$) with high temporal resolution ($\sim 1-2\ \text{minutes}$). It captures both background Galactic Cosmic Radiation (GCR) and energetic proton passes through the South Atlantic Anomaly (SAA).

## 3. Why Radiation Exposure Matters to Drug Stability
Ionizing radiation can induce:
- Direct radiolytic cleavage of covalent bonds in drug molecules.
- Generation of reactive oxygen species (ROS) and free radicals in liquid solutions.
- Alteration of polymer packaging and excipient matrices, potentially destabilizing active pharmaceutical ingredients (APIs).

## 4. Why We Use the Medication's Actual ISS Residence Period
Medications flown to the ISS did not return immediately with the cargo vehicle that delivered them. Instead, they remained stored on the station for durations ranging from **132 days (NG-11 Diphenhydramine)** up to **972 days (SpX-20 Diazepam)**. Integrating radiation across the specific calendar window of each lot ensures that temporal variations in solar activity and geomagnetic shielding are accurately represented.

## 5. How Radiation is Integrated Over Time
For each medication lot $j$ with start date $t_{\text{start}}$ and return date $t_{\text{end}}$:
$$\text{Estimated Cumulative Dose (mGy)} = \frac{1}{1000} \int_{t_{\text{start}}}^{t_{\text{end}}} \dot{D}(t)\, dt$$
Using the high-resolution discrete readings:
$$\text{Estimated Cumulative Dose (mGy)} \approx \frac{1}{1000} \sum_{i} \dot{D}_i \cdot \Delta t_i$$

## 6. Environmental Estimate vs. Direct Medication Dosimetry
> [!IMPORTANT]
> **Key Scientific Distinction:**
> The medication packages did not contain embedded individual radiation dosimeters. Therefore, `estimated_cumulative_iss_dose_mGy` is an **environmental ISS radiation estimate** representative of the ambient exposure in the Columbus module during that timeframe, rather than a direct measurement of each pill or vial.

## 7. Concrete Example from the Master Dataset

Consider sample **`DS01_01`** (Caffeine oral tablets, SpX-15):
* **Mission:** SpX-15
* **Delivered to ISS:** 2018-07-02
* **Returned to Earth:** 2019-01-17
* **Duration (`days_in_space`):** 199 days (4,776 hours)
* **Radiation Measurements Sampled:** 138,421 discrete readings
* **Mean Dose Rate:** $29.77\ \mu\text{Gy/hour}$ ($714.48\ \mu\text{Gy/day}$)
* **Estimated Cumulative ISS Dose:** $142.28\ \text{mGy}$
* **Physicochemical Properties Linked (DS-03):** Molecular Weight $194.19\ \text{g/mol}$, XLogP $-0.1$, TPSA $58.4\ \text{Å}^2$, 0 rotatable bonds, 0 H-bond donors, 3 H-bond acceptors.
