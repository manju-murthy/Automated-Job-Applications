# Automated Job Applications

Phase 1 MVP: upload one or more resume versions, synthesize a candidate profile, and find matching jobs posted in the last 24 hours.

## What is implemented

- Multi-resume upload endpoint (`/phase1/search-jobs`) using FastAPI.
- Resume parsing for `.pdf`, `.docx`, `.txt`, `.md`.
- Profile synthesis from all uploaded resumes (skills, likely titles, experience estimate).
- Live web job discovery from Remotive's public jobs API.
- 24-hour freshness filter and basic skill matching for relevance ranking.

## Architecture (Phase 1)

1. `ResumeParser` extracts text from each file.
2. `ProfileBuilder` merges all resumes into a normalized profile.
3. `RemotiveJobSource` queries the web and keeps only jobs from the last 24 hours.
4. `JobDiscoveryPipeline` composes profile + job search and returns unified JSON.

## API

### `POST /phase1/search-jobs`

`multipart/form-data` with one or more `files` fields.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/phase1/search-jobs" \
  -F "files=@resume_v1.pdf" \
  -F "files=@resume_v2.docx"
```

Response includes:

- `profile`: AI-ready synthesized candidate profile.
- `jobs`: relevant postings from the last 24h.
- `searched_at`: UTC timestamp.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## Phase 2 plan (apply on behalf of user)

1. **User consent & compliance layer**
   - explicit per-application approvals
   - ToS-aware adapter policy (block unsupported automation)

2. **Application adapters**
   - Greenhouse / Lever / Workday structured form fillers
   - fallback semi-automated browser assist for unsupported flows

3. **Material generation**
   - role-specific cover letters and answer drafts
   - traceable source snippets from resume/profile

4. **Execution controls**
   - queue, retries, rate limits, anti-duplication
   - dry-run mode before live submissions

5. **Auditability**
   - per-job action logs
   - artifacts: submitted payloads, timestamps, status transitions

6. **Human-in-the-loop UI**
   - approve/edit/skip job applications
   - confidence flags for low-quality mappings

