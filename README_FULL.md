# MedLens — Full Project Scaffold

This repository is a scaffold for the MedLens application (monorepo).

Structure

- `client/` — React + Vite + TypeScript + Tailwind frontend
- `server/` — Fastify + TypeScript backend
- `.env.example` — example env values
- `Dockerfile` — multi-stage build for Cloud Run

Quick start (development)

1. Install Node.js (>=18) and npm.
2. From the repo root, install server and client dependencies separately:

```bash
cd client
npm install
npm run dev

cd ../server
npm install
npm run dev
```

3. Set env vars from `.env.example` before running server. Use Firebase service account JSON and Google Cloud credentials for Firestore and Storage.

Building for production

```bash
docker build -t medlens:latest .
```

Cloud Run deployment notes

- Use Artifact Registry to store container image.
- Provide secrets (Firebase service account, Gemini API key) using Secret Manager and mount or set as env vars in Cloud Run.
- Ensure Firestore and Cloud Storage are in the same GCP project.

Security & Responsible AI

- All AI requests must be made from the server. Do not put API keys in frontend code.
- The AI assistant is advisory only. See `server/src/services/ai.ts` for the interface to implement Vertex AI calls.

Next steps (recommended)

- Implement Firestore security rules.
- Implement detailed PDF parsing and structured extraction.
- Add tests and CI.
- Harden headers, CORS, rate-limits, and logging.
