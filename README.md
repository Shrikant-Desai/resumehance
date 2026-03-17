# Folder Structure

resume_analyzer/
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
│
└── app/
├── main.py ← FastAPI app entry point
├── config.py ← all env variables loaded here
│
├── api/
│ ├── **init**.py
│ └── v1/
│ ├── **init**.py
│ └── routes/
│ ├── **init**.py
│ ├── resume.py ← resume upload endpoints
│ ├── job.py ← job description endpoints
│ └── analysis.py ← trigger analysis, get results
│
├── core/
│ ├── **init**.py
│ ├── pdf_parser.py
│ ├── skill_extractor.py
│ ├── job_analyzer.py
│ ├── skill_matcher.py
│ ├── readiness_score.py
│ └── roadmap_generator.py
│
├── db/
│ ├── **init**.py
│ ├── connection.py
│ ├── models.py
│ └── repositories.py
│
├── embeddings/
│ ├── **init**.py
│ ├── embedder.py
│ └── similarity.py
│
├── schemas/
│ ├── **init**.py
│ ├── resume.py ← pydantic models for resume
│ ├── job.py ← pydantic models for job
│ └── analysis.py ← pydantic models for analysis
│
└── services/
├── **init**.py
├── resume_service.py ← business logic for resume flow
├── job_service.py ← business logic for job flow
└── analysis_service.py ← orchestrates entire analysis

# Docker Commands

# build and start everything

docker-compose up --build

# start without rebuilding

docker-compose up

# run in background

docker-compose up -d

# see logs

docker-compose logs -f app

# stop everything

docker-compose down

# rebuild just the app after code changes

docker-compose up --build app

# 1 — start DB container first and wait for it to be healthy

docker-compose up db -d

# 2 — verify DB is ready

docker-compose exec db psql -U resume_user -d resume_analyzer -c "\l"

# 3 — start app container

docker-compose up app -d

# 4 — now run migrations

docker-compose exec app alembic upgrade head
