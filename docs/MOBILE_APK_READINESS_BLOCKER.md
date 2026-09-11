# Mobile / APK Readiness Blocker

## Date

2026-09-10

## Requested scope

Prepare the existing React application for Capacitor-based mobile/APK delivery while preserving the validated TANTU flows.

## Inspection result

The current checkout is `feature/M-ai-nlp` at `8734f98`. Its `frontend/` directory contains only `README.md`; it has no React/Vite source, `package.json`, `vite.config.*`, Capacitor configuration, or Android project.

The available `origin/feature/P-frontend` ref does contain the React/Vite frontend (`frontend/package.json`, `frontend/vite.config.js`, and `frontend/src/`). It is not integrated into the active checkout.

The supplied validated checkpoint `bbdaea3` is not present in the local repository history.

## Why no implementation was made

Adding Capacitor files here would create a new, disconnected application rather than prepare the existing frontend. Merging or selecting the frontend branch, or obtaining the validated integrated checkpoint, changes integration state and must be directed by the project owner.

## Required next step

Provide or check out the validated integrated revision that includes both the current backend/AI modules and the React/Vite frontend (including `frontend/package.json`). Once available, mobile readiness can be evaluated with a minimal Capacitor configuration change and a real frontend build verification.

## Validation performed

- Confirmed a clean working tree before this documentation change.
- Inspected the active branch, tracked remote refs, and frontend tree.
- No frontend build was run because the active checkout has no frontend build manifest.
