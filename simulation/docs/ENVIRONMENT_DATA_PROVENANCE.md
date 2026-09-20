# Environmental provenance

Acquisition dates and exact request URLs are stored beside every raw download in `*.provenance.json` and collected in `results/tables/download_manifest.json`. They include SHA-256, byte count, content type, HTTP status and UTC time. Raw downloaded bytes are preserved. No response was enriched in place.

## Radiation

The parent file `data/raw/space_radiation/RAD_ISS_Columbus_DosTel_2018_2022.csv` is reused in place. SHA-256: `89567a16c4f46303e5d7f994a7e12b0b50eab8dfe3ce5d2de19e9ce0a6200d00`. Prior manifest acquisition date: 2026-09-17; exact original query not retained there. This audit downloaded only a one-hour verification subset and preserved its full URL.

Source: NASA OSDR RadLab, ESA/DLR DosTel instruments in Columbus. [DosTel1](https://visualization.osdr.nasa.gov/radlab/gui/knowledgebase/DosTel1), [DosTel2](https://visualization.osdr.nasa.gov/radlab/gui/knowledgebase/DosTel2), [API definition](https://visualization.osdr.nasa.gov/radlab/gui/data-api/).

The API defines absorbed dose rate in µGy/hour. Do not interchange µGy and µSv or assert pharmaceutical absorbed dose. Knowledgebase cadence is 300 seconds; local observed median unique-timestamp spacing is 100 seconds. This discrepancy is recorded, not silently harmonized. Source timestamps have no timezone suffix; UTC is an audit interpretation pending explicit provider confirmation. Sensor coverage and gaps are calculated separately. Calibration and quality flags are not supplied in the local six-column export. Drug location and shielding are unknown; assign Grade D proxy relevance. Provider-specific reuse terms require review; the previous blanket public-domain statement is not independently certified here.

## Cabin telemetry

Source: [NASA OSDR Environmental Data Application](https://visualization.osdr.nasa.gov/eda/); [official API reference](https://visualization.osdr.nasa.gov/eda/api_reference); [NASA NTRS description 20240008072](https://ntrs.nasa.gov/citations/20240008072).

Archived metadata: mission catalog, API reference HTML and NASA telemetry plotting JavaScript. Archived payloads: RR-7, RR-12 and RR-19; RR-8 and RR-17 returned empty JSON arrays for the date-filtered request. Successful payloads include both flight and rodent-ground fields, preserved exactly as returned. Only ISS fields are inspected for medication-proxy availability.

Units come from the archived NASA plotting labels: degrees C, RH %, CO₂ ppm. Timestamps explicitly include Z. Median non-null unique-timestamp resolution is 300 seconds for acquired streams. Dataset time coverage, missing cells, duplicate counts, source URL and checksum are recorded per variable in `environment_source_inventory.csv`. Physical sensor ID, module, calibration and QA flags are not present in the API payload. Assign Grade E until resolved. No drug-specific environmental measurement is claimed.

Transformations for this audit only: parse UTC timestamps; inspect numeric ISS values; ignore nulls for observed support; deduplicate repeated observation times for availability; exclude conflicting same-time values if found; compute union timestamp support under a stated 10-minute gap rule. Do not average environmental values, interpolate, normalize into an exposure matrix or integrate dose in this phase. Nominal intervals between two samples are conditional temporal support, not direct measurements of every instant.

## Exposure and outcome references

- [Nowadly et al., DOI 10.1177/10806032261466966](https://doi.org/10.1177/10806032261466966): Table 1 launch dates and launch-to-landing duration; Methods for storage and expiration semantics. Existing local text extraction was consulted alongside repository extraction notes. Figures were not independently re-digitized in this phase.
- [SpX-15 berthing report](https://www.nasa.gov/blogs/spacestation/2018/07/page/2/): July 2, 2018, 09:52 EDT → 13:52 UTC.
- [SpX-16 daily report](https://www.nasa.gov/blogs/stationreport/2018/12/08/iss-daily-summary-report-12-08-2018/): December 8, 2018, approximately 09:36 CST → approximately 15:36 UTC.
- [SpX-17 installation](https://www.nasa.gov/blogs/spacestation/2019/05/06/spacex-cargo-craft-attached-to-station/): May 6, 2019, 09:32 EDT → 13:32 UTC.
- [NG-11 capture](https://www.nasa.gov/blogs/spacestation/2019/04/19/astronaut-commands-robotic-arm-to-capture-cygnus-cargo-craft-2/): April 19 arrival; capture is not berthing or medication transfer.
- [SpX-18 launch](https://www.nasa.gov/blogs/spacestation/2019/07/25/dragon-reaches-orbit-astronauts-prepare-for-saturday-capture/): July 25, 2019, 18:01 EDT → 22:01 UTC.
- [SpX-18 installation](https://www.nasa.gov/blogs/spacestation/2019/07/27/dragon-installed-to-stations-harmony-module-for-cargo-operations/): July 27, 12:01 EDT; [daily summary](https://www.nasa.gov/blogs/stationreport/2019/07/28/) reports 11:23 CDT. Minute-level inconsistency remains unresolved.
- [SpX-20 launch](https://www.nasa.gov/news-release/spacex-dragon-heads-to-space-station-with-nasa-science-cargo-2/): March 6, 2020, 23:50 EST → March 7, 04:50 UTC. [Capture](https://www.nasa.gov/blogs/spacestation/2020/03/09/robotic-arm-captures-dragon-packed-with-science/) verifies March 9 arrival; exact berthing not assigned.

Exact medication downmass/departure, return vehicle, transfer to HMS hardware and assay timestamps remain unresolved. These are not replaced with the delivery vehicle's departure.
