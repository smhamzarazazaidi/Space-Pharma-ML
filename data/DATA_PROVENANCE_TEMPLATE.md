# Dataset Provenance Card Template

Use this template to record the complete provenance of every raw dataset downloaded and saved to `data/raw/`. Copy this block into `docs/RESEARCH_DOCUMENT.md` (Section 8) or the relevant dataset documentation.

---

```yaml
Dataset ID: UNKNOWN
Dataset Name: UNKNOWN
Original Source: UNKNOWN # e.g. NASA OSDR, PubMed, ALSDA, PubChem
Study ID: UNKNOWN        # e.g. OSDR-###, JSC-Study-###
Paper: UNKNOWN           # Full bibliographic citation
DOI: UNKNOWN             # e.g. 10.xxxx/xxxxx
Original URL: UNKNOWN    # Direct persistent URL or repository landing page
Download Date: UNKNOWN   # YYYY-MM-DD
Original Filename: UNKNOWN
Local Filename: UNKNOWN  # Path in data/raw/...
File Type: UNKNOWN       # e.g. CSV, XLSX, TSV, SDF
License: UNKNOWN         # e.g. NASA Open Data, CC-BY-4.0, Public Domain
Description: UNKNOWN     # Summary of experiment, organisms, drugs, assays
Variables: UNKNOWN       # List of observed raw variables / column headers
Sample Count: UNKNOWN    # Total number of observations / assay rows
Experimental Conditions: UNKNOWN # Flight mission, location, temperature, packaging
Ground Controls: UNKNOWN # Matched 1g ground control availability
Radiation Information: UNKNOWN # Dosimetry data, cumulative dose, sensor type
Spaceflight Duration: UNKNOWN  # Number of days / months in orbit
Potential Target: UNKNOWN      # Target candidate (e.g., % API Remaining, k_deg)
Known Limitations: UNKNOWN     # Missing metadata, batch confounding, small n
Preprocessing Performed: NONE  # Raw files must remain unmodified in data/raw/
Notes: UNKNOWN
```
