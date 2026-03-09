# TrackBite

AI-powered food tracking and meal planning agent — built with Gemini 3.0 Flash, FastAPI, and Next.js.

> **Hackathon**: Google Labs AI Hackathon 2026  
> **Submission deadline**: March 16, 2026 17:00 PT

---

## Architecture Overview

```
Frontend (Next.js 14)
      │  HTTP / Axios
      ▼
Backend (FastAPI on Cloud Run)
      │  Google GenAI SDK
      ▼
Vertex AI — Gemini 3.0 Flash
      │
      ├── Firestore  (inventory + health profile)
      ├── Cloud Storage  (receipt images)
      └── Playwright  (local UI Navigator)
```

---

## Project Structure

```
2026GLA_TrackBite/
├── backend/
│   ├── main.py                   # FastAPI app entry, CORS, routes
│   ├── routers/
│   │   ├── ocr.py                # /parse-receipt, /recommend  (Iteration 1)
│   │   ├── inventory.py          # /inventory CRUD              (Iteration 2)
│   │   └── navigator.py          # /navigate-search             (Iteration 4)
│   ├── models/
│   │   └── schemas.py            # Pydantic models
│   ├── services/
│   │   ├── gemini_service.py     # Google GenAI SDK wrapper
│   │   ├── firestore_service.py  # Firestore read/write         (Iteration 2)
│   │   └── playwright_service.py # Browser automation           (Iteration 4)
│   ├── .env.example              # Environment variable template
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # Gemini connection test page
│   │   └── globals.css
│   ├── .env.local.example        # Frontend env template
│   └── package.json
├── .gitignore
└── README.md
```

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- A GCP project with **Vertex AI API** enabled
- `gcloud` CLI authenticated (`gcloud auth application-default login`)

---

## Local Development

### 1. Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env — fill in GOOGLE_CLOUD_PROJECT

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Backend available at: `http://localhost:8080`  
API docs: `http://localhost:8080/docs`

### 2. Frontend

```bash
cd frontend

# Configure environment variables
cp .env.local.example .env.local
# NEXT_PUBLIC_API_URL is already set to http://localhost:8080

# Start the dev server
npm run dev
```

Frontend available at: `http://localhost:3000`

---

## Environment Variables

### `backend/.env`

| Variable | Description | Example |
|---|---|---|
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | `trackbite-prod` |
| `GOOGLE_CLOUD_LOCATION` | Vertex AI region | `us-central1` |
| `GEMINI_MODEL` | Gemini model name | `gemini-3.0-flash` |
| `APP_HOST` | Server bind host | `0.0.0.0` |
| `APP_PORT` | Server port | `8080` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000` |

### `frontend/.env.local`

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8080` |

---

## API Endpoints

### Iteration 0 (current)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `POST` | `/gemini-test` | Send a prompt to Gemini, returns raw text response |

```bash
# Health check
curl http://localhost:8080/health

# Gemini test
curl -X POST http://localhost:8080/gemini-test \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say hello from Gemini!"}'
```

---

## Deployment (Cloud Run)

```bash
# Build and deploy
gcloud run deploy trackbite-backend \
  --source ./backend \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=<your-project-id>
```

---

## Iteration Roadmap

| Iteration | Status | Deliverable |
|---|---|---|
| 0 — Foundation | ✅ Done | GCP + Hello Gemini |
| 1 — OCR + Receipt | 🔜 | Receipt → Ingredients → Meal suggestion |
| 2 — Health + Inventory | 🔜 | Firestore, health profile |
| 3 — Schedule awareness | 🔜 | Google Calendar integration |
| 4 — Gemini sees screen | 🔜 | Single-step UI Navigator |
| 5 — Full auto navigation | 🔜 | Multi-step shopping automation |
| 6 — Polish + Deploy | 🔜 | Cloud Run, demo video, Devpost |
