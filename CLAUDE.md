# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Factorio Blueprint Manager** - A web application for storing, organizing, and sharing Factorio blueprints with search and metadata parsing capabilities. This is a learning project for AWS, Docker, Kubernetes, and Infrastructure as Code.

**Current Phase:** Phase 0 - Project & Repository Setup
**Full Project Plan:** See `PROJECT_OUTLINE.md` for detailed phase breakdown

**Tech Stack:** Python 3.9+, FastAPI, PostgreSQL, SQLAlchemy, Docker, Kubernetes, AWS (EKS, RDS, ECR), Terraform

## Architecture Overview

### Application Structure (Planned)

```
factorio-blueprint-manager/
├── app/                     # FastAPI application
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration management
│   ├── database.py         # Database connection and sessions
│   ├── models/             # SQLAlchemy database models
│   ├── schemas/            # Pydantic validation schemas
│   ├── api/                # API route handlers
│   ├── services/           # Business logic
│   │   ├── blueprint_parser.py  # Core: decode blueprint strings
│   │   └── blueprint_service.py # Blueprint CRUD operations
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JavaScript, images
├── tests/                   # Pytest test suite
├── docker/                  # Dockerfiles and configs
├── kubernetes/              # K8s manifests
├── terraform/               # Infrastructure as Code
└── alembic/                # Database migrations
```

### Key Components

**Blueprint Parser** (`app/services/blueprint_parser.py`):
- Decodes Factorio blueprint strings: base64 → zlib decompress → JSON
- Extracts metadata: name, description, entities, dimensions, version
- See "Factorio Blueprint Format" section below for details

## Development Commands

### Local Development (Once Implemented)

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest                        # All tests
pytest tests/test_parser.py   # Specific test file
pytest -v                     # Verbose output
pytest --cov=app              # With coverage report

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Code quality
black app/ tests/             # Format code
flake8 app/ tests/            # Lint code
```

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build
docker-compose down

# View logs
docker-compose logs -f app
docker-compose logs -f db

# Run tests in container
docker-compose exec app pytest
```

### Kubernetes (Local)

```bash
# Apply manifests
kubectl apply -f kubernetes/base/

# Check status
kubectl get pods
kubectl get services
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Port forward for local access
kubectl port-forward service/factorio-app 8000:80
```

## Factorio Blueprint Format

**Critical Implementation Detail:** Factorio blueprint strings use a specific encoding:

1. Version prefix "0" + base64(zlib_compress(JSON))
2. To decode: Remove "0" prefix → base64 decode → zlib decompress → parse JSON

**Example:** `0eNqdkltugzAQRfc8BS...`

**Key JSON fields to extract:**
- `blueprint.label` - Blueprint name
- `blueprint.description` - User description
- `blueprint.entities[]` - Array of all entities
  - `entities[].name` - Entity type (assembling-machine-2, transport-belt, etc.)
  - `entities[].position` - {x, y} coordinates
- Calculate dimensions from min/max entity positions
- Count entity occurrences for search/filtering

## Database Schema

### Core Tables

**blueprints** - Main blueprint storage
- `id`, `name`, `description`, `blueprint_string` (original encoded)
- `width`, `height`, `entity_count` (calculated from parsed data)
- `created_at`, `updated_at`
- Indexes on `name`, `created_at`

**blueprint_entities** - Entity counts per blueprint
- `blueprint_id` (FK), `entity_name`, `entity_count`
- Used for filtering (e.g., "show blueprints using assembling-machine-2")

**tags + blueprint_tags** - Tagging system
- Many-to-many relationship for categorization

## API Endpoints

**API Routes:**
- `POST /api/blueprints` - Upload blueprint (body: `{"blueprint_string": "0eNq..."}`)
- `GET /api/blueprints?page=1&limit=20&entity=assembling-machine` - List with filters
- `GET /api/blueprints/{id}` - Get specific blueprint details
- `DELETE /api/blueprints/{id}` - Delete blueprint

**Page Routes:**
- `GET /` - Home page with recent blueprints
- `GET /upload` - Upload form
- `GET /blueprints/{id}` - Blueprint detail view (HTML)

## Development Practices

### Git Workflow
- **Always use feature branches:** `feature/descriptive-name`
- **Commit message format:** `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
  - Example: `feat(parser): implement blueprint string decoder`
- **Create PRs for all changes** - even in solo development for learning

### Code Style
- **Python:** Follow PEP 8, use type hints (Python 3.9+ syntax)
- **Docstrings:** Google style for all functions and classes
- **Async/await:** Use for all FastAPI endpoints
- **Testing:** Write tests alongside features, >80% coverage goal

### Security
- Never commit secrets (.env files in .gitignore)
- Use environment variables for all configuration
- Validate all API inputs (Pydantic schemas)
- Handle malformed blueprint strings gracefully

## Project Phases

**Phase 0** - Repository Setup (Current)
**Phase 1** - Local Application Development (FastAPI, PostgreSQL, Blueprint Parser)
**Phase 2** - Containerization (Docker, Docker Compose)
**Phase 3** - Local Kubernetes
**Phase 4** - AWS Infrastructure (VPC, RDS, EKS, ECR)
**Phase 5** - Infrastructure as Code (Terraform)
**Phase 6** - CI/CD (GitHub Actions)
**Phase 7** - Production Readiness (Monitoring, Security, Backups)
**Phase 8** - Advanced Features (Optional)

See `PROJECT_OUTLINE.md` for detailed breakdown of each phase.

## Initial Dependencies (requirements.txt)

```
fastapi
uvicorn[standard]
sqlalchemy
alembic
psycopg2-binary
pydantic
jinja2
python-multipart

# Dev dependencies (requirements-dev.txt)
pytest
pytest-asyncio
pytest-cov
black
flake8
```

## Important Design Decisions

1. **Jinja2 Templates** - Server-side rendering, not a separate frontend framework (keep it simple)
2. **PostgreSQL** - Relational database for structured blueprint metadata
3. **Blueprint Parser** - Core complexity is in decoding/parsing; invest time in robust implementation
4. **No Authentication Initially** - Focus on core features first, add auth in Phase 8
