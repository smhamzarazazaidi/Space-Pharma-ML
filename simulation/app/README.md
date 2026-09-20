# Orbital Pharmaceutics

Run `simulation/START_SIMULATOR.ps1`, then visit http://127.0.0.1:8765.

Build offline research artifacts with `python simulation/src/build_phase_d.py`.
Test with `python simulation/tests/test_phase_d.py`.

The existing project has no frontend framework. This app uses browser-native ES modules, CSS and locally vendored Three.js 0.170.0 (MIT), avoiding a build system and large framework dependency tree. Python serves whitelisted app assets and a local-only JSON API. No external network is required at runtime.

Historical replay supports every flown lot and any of the 28 two-API exclusions. Prepare, play/pause, scrub, restart and change speed. AUTO maps the selected flight window to 60 seconds; numerical dose integration is independent of playback. A paired replay synchronizes normalized mission progress, with each API's own historical dates and stream. The main telemetry scene shows the first selected lot; both endpoint predictions appear below.

Orbit and geographic artwork are schematic. WebGL failure shows a 2D fallback. Reduced-motion preferences suppress decorative rotation and radiation motion. The scientific endpoint predictor is provisional. Published outcomes are excluded from replay responses until the separate reveal action; the clearly labeled Validation Lab is an intentional exception for analysis.

All runs save locally under `results/simulation_runs/`. Raw telemetry and private outcomes are never served as static files. Historical timestamp uncertainty and incomplete sensor coverage remain visible. See `docs/HISTORICAL_SIMULATOR_METHOD.md` and `docs/PHASE_D_SIMULATOR_REPORT.md`.
