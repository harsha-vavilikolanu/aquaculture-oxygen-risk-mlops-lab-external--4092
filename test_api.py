
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction():
    data = {
        "feed_given_kg": 200,
        "shrimp_biomass_kg": 5000,
        "aeration_run_hours": 8,
        "pond_area_sq_meters": 2000,
        "water_temp_celsius": 30,
        "dissolved_oxygen_ppm": 4.2
    }

    response = client.post("/predict", json=data)

    assert response.status_code == 200

    result = response.json()

    assert result["oxygen_risk"] in ["High", "Normal"]
    assert 0 <= result["high_risk_probability"] <= 1
    assert isinstance(
        result["additional_night_aeration_required"], bool
    )


def test_invalid_input():
    data = {
        "feed_given_kg": 200,
        "shrimp_biomass_kg": -500,
        "aeration_run_hours": 8,
        "pond_area_sq_meters": 2000,
        "water_temp_celsius": 30,
        "dissolved_oxygen_ppm": 4.2
    }

    response = client.post("/predict", json=data)

    assert response.status_code == 422
