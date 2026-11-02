# LocalBiz AI Campaign Studio - Backend

Modular, production-grade FastAPI backend architected following Clean Architecture and SOLID principles.

## Structure
```
app/
├── api/v1/endpoints/campaign.py     # Clean REST controllers
├── core/config.py                  # Pydantic Settings
├── schemas/campaign.py             # Pydantic schemas & DTOs
└── services/
    ├── ai_agent_service.py         # Google Gemini LLM Agent
    ├── template_rule_service.py    # Zero-token deterministic rule engine
    ├── poster_render_service.py    # Pillow dynamic graphics engine
    └── orchestration_service.py   # Business logic orchestrator
```

## Setup & Deployment

1. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Copy environment file:
```bash
cp .env.example .env
# Add GEMINI_API_KEY
```

3. Run locally:
```bash
uvicorn app.main:app --reload --port 8000
```
Swagger UI available at: `http://localhost:8000/api/v1/docs`

4. Run tests:
```bash
pytest tests/
```
