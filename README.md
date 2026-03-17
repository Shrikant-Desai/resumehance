# Resumehance — AI-Powered Resume Analyzer

**Resumehance** is a FastAPI backend that compares a candidate's resume against a job description using Google Gemini AI and vector embeddings. It produces a job readiness score, skill gap analysis, and a personalised week-by-week learning roadmap.

Designed to work for **both technical** (software engineering) **and non-technical** (finance, healthcare, marketing, operations) resumes and job descriptions.

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [How the Score Is Calculated](#how-the-score-is-calculated)
5. [API Flow](#api-flow)
6. [Environment Variables](#environment-variables)
7. [Running Locally (without Docker)](#running-locally-without-docker)
8. [Running with Docker](#running-with-docker)
9. [API Reference](#api-reference)
10. [Project Structure](#project-structure)

---

## What It Does

1. **Upload a Resume (PDF)** → Gemini extracts structured data (skills, experience, education, personal info).
2. **Submit a Job Description (text)** → Gemini parses it into structured requirements (required skills, priorities, seniority).
3. **Run Analysis** → The system vector-embeds every skill from both sides, computes cosine similarity, and classifies each JD skill as `matched`, `partial`, or `missing`.
4. **Get Results:**
   - **Job Readiness Score** (0–100) with verdict (Strong / Good / Fair / Needs Work)
   - **Skill gap report** with priority tiers (critical / important / good_to_have)
   - **Experience gap** analysis
   - **Personalised learning roadmap** (week-by-week, AI-generated)

---

## Architecture

```
┌──────────────┐   PDF bytes     ┌─────────────────┐   raw text    ┌──────────────────┐
│  HTTP Client │ ─────────────▶  │  /resume/upload  │ ──────────▶  │ Gemini (extract) │
└──────────────┘                 └─────────────────┘               └──────────────────┘
                                         │ ParsedResume JSON                │
                                         ▼                                  ▼
                                 ┌───────────────┐              ┌────────────────────┐
                                 │  PostgreSQL DB │◀─────────── │ Gemini Embeddings  │
                                 │  (pgvector)   │  skill       │ (per-skill vectors)│
                                 └───────────────┘  vectors     └────────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │  /analysis/run       │
                              │  (resume_id, jd_id)  │
                              └──────────────────────┘
                                         │
                     ┌───────────────────┼───────────────────┐
                     ▼                   ▼                   ▼
              Vector Similarity    Readiness Score    Gemini Roadmap
              (cosine distance)    (weighted formula) (week-by-week)
                     │                   │                   │
                     └───────────────────┴───────────────────┘
                                         │
                                  AnalysisRunResponse
                                  (saved to DB + returned)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI 0.135 |
| AI / LLM | Google Gemini (`google-genai` SDK) |
| Embeddings | `gemini-embedding-2-preview` (768-dim) |
| Database | PostgreSQL 16 with pgvector extension |
| ORM | SQLAlchemy 2.0 (async-compatible) |
| Migrations | Alembic |
| Schema Validation | Pydantic v2 |
| PDF Parsing | pdfplumber |
| Containerisation | Docker + Docker Compose |

---

## How the Score Is Calculated

The **Job Readiness Score** (0–100) is a weighted formula:

```
Score = Critical Skill Score (40 pts)
      + Important Skill Score (25 pts)
      + Good-to-Have Score   (15 pts)
      + Experience Score     (20 pts)
```

### Skill Scoring (per bucket)

Skills are grouped by the JD's `skill_priority_map`. Each skill in a bucket is scored:
- **Full match** (cosine similarity ≥ 0.85) → 1.0 credit
- **Partial match** (cosine similarity ≥ 0.65) → 0.5 credit
- **Missing** (below 0.65) → 0 credit

```
Bucket Score = (Σ credits / total skills in bucket) × bucket weight
```

> If a bucket has **no required skills**, full credit is awarded for that bucket automatically.

### Experience Scoring

```
Experience Score = min(candidate_years / minimum_years, 1.0) × 20
```

> If the JD has no minimum experience requirement, full 20 points are awarded.

### Verdict Thresholds

| Score | Verdict |
|-------|---------|
| ≥ 75 | **Strong** — ready to apply |
| ≥ 55 | **Good** — apply with preparation |
| ≥ 35 | **Fair** — significant gaps, plan learning |
| < 35 | **Needs Work** — foundational gaps |

---

## API Flow

### Step 1 — Upload Resume
```
POST /api/v1/resume/upload
Content-Type: multipart/form-data
Body: file=<resume.pdf>
```
Returns: `resume_id`, structured `ParsedResume`

### Step 2 — Submit Job Description
```
POST /api/v1/job/create
Content-Type: application/json
Body: { "jd_text": "...", "job_title": "optional", "company": "optional" }
```
Returns: `jd_id`, structured `ParsedJob`

### Step 3 — Run Analysis
```
POST /api/v1/analysis/run
Content-Type: application/json
Body: { "resume_id": 1, "jd_id": 1 }
```
Returns: full `AnalysisRunResponse` with score, skill gaps, roadmap

---

## Environment Variables

Create a `.env` file in the project root:

```env
# App
APP_NAME=Resumehance
ENVIRONMENT=development
DEBUG=True

# Database (used by SQLAlchemy + Alembic)
DATABASE_URL=postgresql://postgres:password@localhost:5432/resumehance
# For Docker Compose, use the service name:
# DATABASE_URL=postgresql://postgres:password@db:5432/resumehance

# Docker Compose Postgres config
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=resumehance

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
```

> Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Running Locally (without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 16 with [pgvector extension](https://github.com/pgvector/pgvector) installed
- Gemini API key

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Enable pgvector in your PostgreSQL database
psql -U postgres -d resumehance -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 4. Set up environment variables
cp .env.example .env   # edit with your values

# 5. Run database migrations
alembic upgrade head

# 6. Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: `http://localhost:8000/docs`

---

## Running with Docker

Docker Compose handles everything — PostgreSQL with pgvector is pre-configured via the `pgvector/pgvector:pg16` image.

```bash
# 1. Create your .env file (see Environment Variables above)
# Use DATABASE_URL=postgresql://postgres:password@db:5432/resumehance

# 2. Start all services
docker-compose up --build

# 3. Run migrations (in a separate terminal or add to docker entrypoint)
docker-compose exec app alembic upgrade head
```

The app will be available at: `http://localhost:8000`

> ⚠️ The pgvector extension is **automatically enabled** during migrations via `alembic/env.py`. The `pgvector/pgvector:pg16` image includes the compiled extension; the migration just activates it.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/resume/upload` | Upload a PDF resume |
| `POST` | `/api/v1/job/create` | Submit a job description |
| `POST` | `/api/v1/analysis/run` | Run full analysis (resume vs JD) |
| `GET` | `/api/v1/analysis/{id}` | Get full analysis result |
| `GET` | `/api/v1/analysis/{id}/summary` | Get summary (score + verdict only) |

Full interactive docs: `http://localhost:8000/docs` (only when `DEBUG=True`)

---

## Project Structure

```
resumehance/
├── app/
│   ├── api/v1/routes/          # FastAPI route handlers
│   │   ├── analysis.py
│   │   ├── job.py
│   │   ├── resume.py
│   │   └── health.py
│   ├── core/                   # Business logic
│   │   ├── ai_engine.py        # Gemini client wrapper
│   │   ├── pdf_parser.py       # PDF text extraction
│   │   ├── skill_extractor.py  # LLM prompt: resume → ParsedResume
│   │   ├── job_analyzer.py     # LLM prompt: JD text → ParsedJob
│   │   ├── readiness_score.py  # Score calculation (pure logic, no LLM)
│   │   ├── roadmap_generator.py # LLM prompt: gaps → learning roadmap
│   │   └── exceptions.py       # Custom exception classes
│   ├── db/
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   ├── connection.py       # Engine, session, pgvector init
│   │   └── repositories.py     # DB read/write functions
│   ├── embeddings/
│   │   ├── embedder.py         # Gemini embedding API calls
│   │   └── similarity.py       # Cosine similarity + match classification
│   ├── schemas/
│   │   ├── resume.py           # Pydantic models: ParsedResume, etc.
│   │   ├── job.py              # Pydantic models: ParsedJob, etc.
│   │   └── analysis.py         # Pydantic models: AnalysisRunResponse, etc.
│   ├── services/
│   │   ├── resume_service.py   # Orchestrates upload → extract → embed → save
│   │   ├── job_service.py      # Orchestrates JD → analyze → embed → save
│   │   └── analysis_service.py # Orchestrates analysis → score → roadmap → save
│   ├── middleware/
│   │   └── logging.py          # Request/response logging middleware
│   ├── config.py               # Pydantic settings (reads .env)
│   └── main.py                 # FastAPI app factory
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── a4b06fee94c1_initial_tables.py
│   └── env.py                  # Migration config (enables pgvector ext.)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Understanding Key Design Decisions

### Why Vector Embeddings Instead of Simple String Matching?
String matching would fail for semantically equivalent skills (e.g. `"ML"` vs `"Machine Learning"`, `"React.js"` vs `"React"`). By embedding every skill with Gemini's semantic model, we compute **meaning similarity**, not just text similarity.

### Why is pgvector Used?
Skill vectors are stored in PostgreSQL using the `pgvector` extension (768-dim per skill). This enables future scaling to direct SQL-based approximate nearest neighbour (ANN) search using `<=>` operator — without needing a separate vector database.

### Why Is the Score Computed Without LLM?
The readiness score is a deterministic weighted formula (no LLM call). This makes it:
- **Reproducible** — same inputs always produce the same score
- **Explainable** — the `breakdown` field shows exactly how it was computed
- **Fast** — no API latency for this step

### Caching
If `analysis/run` is called again with the same `resume_id` + `jd_id` pair, the full result is returned from the DB without re-running Gemini or computing vectors.
