# MedLens — AI Clinical Insight (MVP)

Quick demo of a secure, portable Flask app that ingests report text, extracts structured findings with reference-range awareness, stores provenance, and offers an AI-powered summary (requires OpenAI key).

Setup

1. Create a Python venv and install:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Set environment variables:

```bash
export MEDLENS_API_TOKEN="your-secret"
export OPENAI_API_KEY="sk-..."
```

3. Run the app:

```bash
python app.py
```

API

- `POST /api/patients` JSON body `{name,age,sex}` — creates patient.
- `POST /api/patients/<id>/reports` form field `text` or file `file` — ingests report and returns structured findings.
- `GET /api/reports/<id>/summary` — returns AI summary (requires `OPENAI_API_KEY`).

Security & Notes

- Simple API token auth via `MEDLENS_API_TOKEN`; for production replace with proper auth.
- Parser is conservative and does not invent reference ranges.
- This is an MVP scaffold. Extend with PDF parsing, user management, and audit logging for production.
