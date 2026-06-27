# Operator Pre-flight Runbook

## A. Local Environment Start Commands

Backend:

```bat
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
.venv\Scripts\activate
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Frontend:

```bat
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

## B. Mandatory Pre-flight Checks

Check:

- `http://127.0.0.1:8000/docs` opens
- `http://127.0.0.1:5173` opens
- `/#/demo` opens
- `/#/public-events` opens
- `/#/public-events/donglu-sunjihai-youth-football` opens
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` opens
- explicit generated-run click succeeds
- `/#/reports/donglu-sunjihai-youth-football-sample` opens
- no visible 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`
- no publish / send / post / execute CTA
- no generated response text
- no raw author identifiers
- no `.env` / API keys / tokens / cookies / sessions / browser profile paths visible

## C. Optional Routes

- `/#/opinion-ecosystem`
- `/#/public-events/helldivers-psn`
- `/#/reports/helldivers-psn-sample`
- `/#/external-collector` only if explaining local package source boundary
- `/#/analysis-requests` only if backend is running and no visible 500 appears; otherwise skip

## D. Operator Checklist Before Recording Or Trusted Playtest

- Close unrelated tabs.
- Hide desktop secrets.
- Do not show terminals with `.env` or keys.
- Do not show private collector path.
- Do not use a personal browser profile.
- Do not enter private or sensitive real data.
- Prepare Chinese boundary explanation.
- Prepare stop conditions.
- Confirm this is not live crawling, not full-web coverage, not official verification, and not a production score.
- Confirm generated-run click is explicit and does not run automatically on page load.
