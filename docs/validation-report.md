# Validation Report

## Automated Checks

- backend game-engine tests for default state, action deltas, clamping, threshold derivation, sick recovery, evolution, action-buffered evolution recovery, sub-tick sync accumulation, permanence, and invalid persisted-state repair
- API startup verification
- frontend typecheck

## Manual And Smoke Checks

- confirm the frontend loads ChuChu from the backend
- confirm vitals visibly update over time without refresh
- confirm `Feed`, `Play`, and `Rest` each apply the intended trade-offs
- confirm `Sick` can be triggered and recovered from
- confirm `Evolved` is reachable and permanent after activation
- confirm reset restarts the single global pet save

## Results

- backend logic tests: `20 passed`
- backend SQLite smoke flow: passed
- backend long-gap offline-decay smoke flow: passed
- frontend typecheck: passed
- frontend production build: passed

## Notes

- The frontend production build succeeded only after rerunning outside the sandbox because this workspace is inside a OneDrive-backed path and the sandboxed build hit a filesystem rename permission error.
- The backend test and smoke runs also required elevated access in this environment so `pytest` and `SQLite` could write their temporary and database files.
