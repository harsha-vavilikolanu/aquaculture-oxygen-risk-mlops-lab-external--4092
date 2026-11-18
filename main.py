
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(
    title="Aquaculture Oxygen Risk Prediction API",
    description="Predicts high-risk aquaculture ponds and recommends night-time aeration.",
    version="1.0"
)

# Load trained model and feature configuration
model = joblib.load("aquaculture_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")


class PondInput(BaseModel):

    feed_given_kg: float = Field(gt=0)
    shrimp_biomass_kg: float = Field(gt=0)
    aeration_run_hours: float = Field(ge=0, le=24)
    pond_area_sq_meters: float = Field(gt=0)
    water_temp_celsius: float
    dissolved_oxygen_ppm: float = Field(ge=0)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Aquaculture Oxygen Risk Prediction API"
    }


@app.post("/predict")
def predict_oxygen_risk(data: PondInput):

    # Feature engineering
    feed_per_unit_biomass = (
        data.feed_given_kg / data.shrimp_biomass_kg
    )

    aeration_hours_per_area = (
        data.aeration_run_hours / data.pond_area_sq_meters
    )

    # Prepare model input
    input_data = pd.DataFrame([{
        "feed_per_unit_biomass": feed_per_unit_biomass,
        "aeration_hours_per_area": aeration_hours_per_area,
        "water_temp_celsius": data.water_temp_celsius,
        "dissolved_oxygen_ppm": data.dissolved_oxygen_ppm
    }])

    input_data = input_data[feature_columns]

    # Prediction
    prediction = int(model.predict(input_data)[0])

    # Probability of high risk
    probability = float(model.predict_proba(input_data)[0][1])

    oxygen_risk = "High" if prediction == 1 else "Normal"

    # Recommendation
    additional_aeration_required = oxygen_risk == "High"

    recommendation = (
        "Increase or extend night-time aeration and monitor oxygen levels."
        if additional_aeration_required
        else "Continue scheduled aeration and routine oxygen monitoring."
    )

    return {
        "oxygen_risk": oxygen_risk,
        "high_risk_probability": round(probability, 4),
        "additional_night_aeration_required": additional_aeration_required,
        "recommendation": recommendation
    }
