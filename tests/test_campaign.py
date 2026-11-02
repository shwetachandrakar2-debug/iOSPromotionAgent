from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_orchestrate_template_mode():
    payload = {
        "business": {
            "name": "Test Salon",
            "phone": "+91 98765 43210",
            "whatsapp": "+91 98765 43210",
            "category": "Salon",
            "city": "Raipur"
        },
        "objective": "Test",
        "offer_headline": "Flat 50% Off",
        "language": "hinglish",
        "execution_mode": "TEMPLATE_RULE",
        "theme_palette": "gold_dark"
    }
    response = client.post("/api/v1/campaign/orchestrate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["mode_used"] == "TEMPLATE_RULE"
    assert "data:image/jpeg;base64," in data["poster_base64"]
