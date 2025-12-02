# Grimoire - Factorio Blueprint Manager

A web application for storing, organizing, and sharing Factorio blueprints with intelligent search and metadata parsing capabilities.

> **Note:** This is a learning project focused on mastering AWS, Docker, Kubernetes, and Infrastructure as Code principles through building a real-world application.

## Project Overview

**Grimoire** helps Factorio players manage their blueprint collection by:
- Uploading and storing blueprint strings
- Automatically parsing blueprint metadata (entities, dimensions, resources)
- Providing search and filtering capabilities
- Organizing blueprints with tags
- Making blueprints easily shareable

### Why "Grimoire"?

A grimoire is a book of knowledge and formulas - much like a collection of Factorio blueprints that contain the "recipes" for building efficient factories!

## Tech Stack

- **Backend:** Python 3.9+, FastAPI, SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Jinja2 templates (server-side rendering)
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (local and AWS EKS)
- **Cloud:** AWS (VPC, RDS, EKS, ECR, CloudWatch)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions

## Project Status

**Current Phase:** Phase 2 - Containerization

See [PROJECT_OUTLINE.md](PROJECT_OUTLINE.md) for the complete development roadmap.

### Development Phases

- [x] **Phase 0:** Repository Setup ✅
- [x] **Phase 1:** Local Application Development ✅
- [ ] **Phase 2:** Containerization with Docker
- [ ] **Phase 3:** Local Kubernetes
- [ ] **Phase 4:** AWS Infrastructure
- [ ] **Phase 5:** Infrastructure as Code (Terraform)
- [ ] **Phase 6:** CI/CD Pipeline
- [ ] **Phase 7:** Production Readiness
- [ ] **Phase 8:** Advanced Features

## Quick Start

```bash
# Clone the repository
git clone https://github.com/chayde/grimoire.git
cd grimoire

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run the application
uvicorn app.main:app --reload

# Open in browser
# http://localhost:8000
```

The application uses SQLite by default for local development. See `.env` file to configure database settings.

## Documentation

- [CLAUDE.md](CLAUDE.md) - Context for Claude Code development sessions
- [PROJECT_OUTLINE.md](PROJECT_OUTLINE.md) - Complete project roadmap and learning objectives

## About Factorio Blueprints

Factorio blueprints are base64-encoded, zlib-compressed JSON strings that contain:
- Blueprint name and description
- Entities (machines, belts, inserters, etc.)
- Entity positions and configurations
- Game version information

This application decodes these strings and extracts useful metadata for search and organization.

## Learning Goals

This project is designed to teach:
- Building production-ready REST APIs with FastAPI
- Database design and optimization with PostgreSQL
- Containerization and orchestration
- Cloud infrastructure on AWS
- Infrastructure as Code with Terraform
- CI/CD automation with GitHub Actions
- DevOps best practices

## License

This project is for educational purposes.

## Contributing

This is a personal learning project, but feedback and suggestions are welcome via issues!
