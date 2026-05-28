# Sentigraph v6.28 Operation Guide

Last updated: 2026-05-28

Status: local operation and presentation guide for the v6.28 demo-ready MVP.
This guide includes the Vendor Sample POC utilities as an offline supporting
path. It does not authorize vendor API calls, live adapters, scraping, URL
fetching, MediaCrawler, cookies, real search/RSS/GDELT providers, real LLM
calls, or secret storage.

## Real / Offline / Mock Boundary

| Area | Current state | Do not claim |
| --- | --- | --- |
| YouTube data | Optional real public video/comment demo when a local ignored `.env` has `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY`. | Do not claim automated tests call YouTube or that other platforms are real. |
| Analysis / report / forecast / Simulation Lab | Offline deterministic and local. | Do not claim predictions are guaranteed or actions are executed. |
| CSV/Excel and Manual URL evidence | User-provided normalized evidence, no URL fetching. | Do not claim imported/manual evidence is automatically verified. |
| Search Discovery / RSS / GDELT | Mock/static URL-title-snippet fixtures only. | Do not claim live search, RSS, or GDELT providers are active. |
| Vendor Sample POC | Offline CSV/JSON sample mapping, scoring, and review. | Do not claim live vendor API integration or official platform verification. |
| LLM | Mock provider only. | Do not claim real LLM calls are enabled. |
| MediaCrawler | Not integrated. | Do not claim crawler-source integration exists. |

## Step 1: Validate The Project

What you can do:

- Confirm backend tests, offline benchmarks, and frontend production build work
  from the repository root.

How to do it:

```powershell
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

Why this step exists:

- It proves the local MVP is healthy before a demo or vendor POC walkthrough.
- It keeps validation local and avoids GitHub Actions CI, which is
  intentionally disabled.

Success signs:

- `python -m pytest` reports all tests passed.
- Offline benchmarks report `no_regression`.
- Frontend build completes; the existing large chunk warning is non-blocking.

What not to claim:

- Do not claim these commands call real APIs, live search providers, or real
  LLMs.
- Do not claim this is production readiness.

## Step 2: Start Backend And Frontend

What you can do:

- Run the local FastAPI backend and Vite frontend for a browser demo.

How to do it:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

In another terminal:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

Why this step exists:

- It gives a presenter access to the full local desktop web UI.

Success signs:

- Backend health endpoint is reachable at `/api/v1/health`.
- Frontend opens without a React/Vite error overlay.
- Sidebar pages render.

What not to claim:

- Do not show `.env`, API keys, shell history, or private browser tabs.
- Do not start real platform providers unless intentionally running the
  optional YouTube local demo.

## Step 3: Run The Optional YouTube Real-Data Demo

What you can do:

- Demonstrate the only current optional real platform data path: public YouTube
  video/comment data through the official YouTube Data API v3.

How to do it:

- Configure a local ignored `.env` outside the recording frame:

```text
YOUTUBE_ADAPTER_MODE=real
YOUTUBE_API_KEY=
```

- Start the app.
- Open `Keyword Search`.
- Select YouTube only.
- Create the YouTube real-data case.
- Crawl and attach raw data.
- Run case analysis.

Why this step exists:

- It proves Sentigraph can attach real public YouTube comments as
  `case_raw_data` and run offline deterministic analysis on them.

Success signs:

- UI shows `Data: YouTube Real`, `Analysis: Offline`, and `LLM: Mock`.
- Analysis Result shows `analysis_input_source=case_raw_data`.
- Summary Report uses YouTube-derived representative comments.

What not to claim:

- Do not claim automated tests call YouTube.
- Do not show the API key.
- Do not claim Douyin, Bilibili, RSS, GDELT, or vendor APIs are live.
- Do not claim YouTube comments are moderated or acted on automatically.

## Step 4: Run CSV / Excel Evidence Import Demo

What you can do:

- Import lawful user-provided evidence datasets when platform APIs are
  unavailable or intentionally not used.

How to do it:

- Open `Cases`.
- Select or create a case with no attached raw comments.
- Open the Evidence Import panel.
- Download the CSV template if needed.
- Upload a CSV/XLSX sample.
- Preview rows and warnings.
- Commit the import.
- Run analysis after import.

Why this step exists:

- It shows the source-neutral Evidence Layer: uploaded records become
  normalized `EvidenceItem` objects with provenance, warnings, deduplication,
  and local job metadata.

Success signs:

- `evidence_count > 0`.
- `acquisition_mode=user_upload`.
- Evidence Scale / Coverage shows latest import job.
- Case run shows `analysis_input_source=case_evidence_items` when no raw
  comments exist.

What not to claim:

- Do not claim uploaded datasets are automatically verified.
- Do not claim uploaded raw files are persisted by default.
- Do not claim full-platform or full-web coverage.

## Step 5: Run Manual URL Evidence Demo

What you can do:

- Attach a single article, video, post, comment, reply, or metric manually.

How to do it:

- Open `Cases`.
- Select a target case.
- Open `Manual Evidence`.
- Enter URL, source/platform label, evidence type, title/body/comment text, and
  optional metrics.
- Check the lawful-source attestation when appropriate.
- Add evidence, then run analysis.

Why this step exists:

- It supports human-curated public evidence without any crawler behavior.

Success signs:

- Evidence preview appears.
- `acquisition_mode=manual_url`.
- Missing URL or missing attestation produces review warnings.
- Analysis can use manual evidence as `case_evidence_items`.

What not to claim:

- Do not claim Sentigraph opened or scraped the URL.
- Do not claim screenshots or pasted text are verified.

## Step 6: Run Search Discovery Mock / RSS Mock / GDELT Mock Demo

What you can do:

- Show the candidate-review UX for future discovery providers using static
  local fixtures.

How to do it:

- Open `Search Discovery`.
- Select `Mock Static`, `RSS Mock`, or `GDELT Mock`.
- Generate mock candidates.
- Accept one candidate and reject another.
- Attach accepted candidates to a case.

Why this step exists:

- It demonstrates how future discovery providers may surface URL/title/snippet
  candidates for human review without fetching full content.

Success signs:

- Provider card says mock/static, no live fetching, candidate metadata only.
- Accepted candidates attach as `provenance_type=search_discovery_candidate`.
- Attached candidates appear in Evidence Review Queue and Evidence Scale /
  Coverage.

What not to claim:

- Do not claim real search, RSS, or GDELT APIs are called.
- Do not claim candidate URLs are fetched.
- Do not claim title/snippet metadata is full source content.

## Step 7: Run Evidence Review / Audit Demo

What you can do:

- Review low-trust, unverified, duplicated, missing-source, or suspicious
  evidence.

How to do it:

- Open `Cases`.
- Use the Evidence Review Queue.
- Apply actions such as approve, reject, mark weak, request source, merge
  duplicate, or reset.
- Open the Review Audit Timeline.

Why this step exists:

- It proves evidence governance is human-reviewable and append-only, rather
  than hidden or automatic.

Success signs:

- Queue counts and review status update.
- Rejected evidence remains stored but is excluded from default analysis.
- Audit timeline records previous status, new status, reviewer label, note, and
  analysis effect.

What not to claim:

- Do not claim AI verifies evidence authenticity.
- Do not call screenshots/transcriptions verified unless a trusted source
  confirms them.

## Step 8: Run Evidence Scale / Coverage Demo

What you can do:

- Show counts, unique/duplicate distribution, trust/review distribution, source
  distribution, acquisition modes, latest jobs, and time coverage.

How to do it:

- Open `Cases`.
- Select a case with imported/manual/search evidence.
- Open Evidence Scale / Coverage.

Why this step exists:

- It explains what evidence is available in the current case and what limits
  still exist.

Success signs:

- Total/unique/duplicate evidence counts are visible.
- Latest ingestion jobs are visible.
- Coverage note is visible:
  `This is coverage of imported/available evidence, not full platform coverage.`

What not to claim:

- Do not claim full-platform, full-web, or exhaustive coverage.
- Do not claim repeated submissions directly inflate risk or sentiment.

## Step 9: Run Vendor Sample POC Flow

What you can do:

- Evaluate a third-party vendor sample offline before considering any live
  adapter.

How to do it:

1. Open `docs/data_vendor_intake_checklist.md`.
2. Open `docs/vendor_sample_data_schema.md`.
3. Ask the vendor for a secret-free CSV/JSON sample and data dictionary.
4. Map the local sample with:

```powershell
python scripts/map_vendor_sample_to_evidence.py backend/app/tests/fixtures/evidence/vendor_sample_minimal.csv --vendor-name ExampleVendor --platform news_site --query "Tesla QA" --output mapped_vendor_sample.jsonl
```

5. Review mapping warnings and confirm no secret-like values are exposed.
6. Use `docs/vendor_scoring_rubric.md` and
   `docs/vendor_poc_scorecard_template.md` to classify the vendor:
   `approved_poc`, `limited_poc`, `internal_research_only`, or `reject`.
7. If the sample is acceptable, import the mapped CSV/Excel-compatible sample
   through the Evidence Import flow and review it like any other evidence.

Why this step exists:

- Vendor data can help all-web public-opinion monitoring, but only after source
  rights, retention, deletion sync, personal-data handling, and cost are
  understood.

Success signs:

- Mapper reads only local files.
- Output uses `acquisition_mode=data_vendor`.
- `trust_label=medium_low` at most.
- `verification_status=vendor_attested` appears only when attestation is
  documented; otherwise evidence remains `needs_review` / `unverified`.
- Risk flags identify unclear source, deletion-sync unknown, personal-data
  unknown, self-crawled public web, unsupported platform claims, invalid
  metrics, formula-like text, or possible secret redaction when applicable.

What not to claim:

- Do not claim vendor sample data is official API data.
- Do not claim Sentigraph has a live vendor adapter.
- Do not claim vendor evidence is high trust by default.
- Do not claim a future adapter is approved before POC, contract/DPA, security,
  deletion-sync, quota, mocked-fixture, and credential-handling gates pass.

## Step 10: Run Analysis / Summary / Forecast / Simulation Lab

What you can do:

- Run deterministic offline analysis from raw data, normalized evidence, or mock
  fallback.

How to do it:

- Open a completed case.
- Run analysis from `Cases` or the relevant case action.
- Open `Analysis Result`.
- Open `Summary Report` and Markdown export.
- Open `Risk Monitor / Forecast`.
- Open `Simulation Lab`, initialize from case, compare strategies, and export
  the strategy report.

Why this step exists:

- It shows the end-to-end public-opinion intelligence workflow after evidence
  enters the case.

Success signs:

- `analysis_input_source` is visible:
  `case_raw_data`, `case_evidence_items`, or `mock_data_fallback`.
- Summary Report contains representative evidence with caveats.
- Forecast and Simulation Lab show deterministic, non-guaranteed outputs.

What not to claim:

- Do not claim forecasts are guaranteed.
- Do not claim Simulation Lab executes moderation or real-world actions.
- Do not claim the report was generated by a real LLM.

## Step 11: Show Benchmarks / LLM Safety / Platform Overview

What you can do:

- Close the demo by showing quality checks and safety boundaries.

How to do it:

- Open `Benchmarks`.
- Open `LLM Safety`.
- Open `Platform Integration Overview`.

Why this step exists:

- It makes the local validation, mock LLM boundary, and platform readiness
  visible to reviewers.

Success signs:

- Benchmarks show latest offline summary.
- LLM Safety shows mock provider / real-call disabled status.
- Platform Overview shows YouTube real-capable, Douyin/Bilibili/etc. pending,
  and mock/static sources clearly separated.

What not to claim:

- Do not claim all platforms are real.
- Do not claim real LLM providers are active.
- Do not claim pending platforms are integrated.

## Pre-Demo Privacy Checklist

- Hide `.env`, shell history, and terminal panes with credentials.
- Do not show real private user data.
- Do not show vendor confidential sample rows unless cleared.
- Do not print API keys, tokens, cookies, passwords, client secrets, or vendor
  credentials.
- Use safe fixtures, public samples, or intentionally selected public YouTube
  comments.
- Keep every boundary label visible: real YouTube optional, offline analysis,
  mock/static discovery, mock LLM, pending platforms, and no MediaCrawler.
