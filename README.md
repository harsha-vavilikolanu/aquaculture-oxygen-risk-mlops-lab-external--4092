# MLOps Lab External

## Predicting Night-Time Oxygen Depletion in Shrimp Aquaculture Ponds

---

### Student Details

| Field | Details |
||---|
| **Name** | Sri Harsha |
| **Registration Number** | 231FA04092 |
| **Section** | 15 |
| **Subject** | MLOps Lab External |
| **Question** | Question 3 |
| **Domain** | Machine Learning / Aquaculture |

---

## 1. Aim

To develop an end-to-end MLOps pipeline that predicts whether dissolved oxygen levels in shrimp aquaculture ponds may fall below **4 mg/L by 5:00 AM**, using measurements recorded at 8:00 PM, and implement dataset versioning, feature engineering, model training, MLflow tracking, FastAPI model serving, automated testing, and GitHub Actions CI/CD.

---

## 2. Problem Statement

Shrimp aquaculture ponds near Kakinada may experience nighttime dissolved oxygen depletion due to high stocking density, feeding activity, high water temperature, insufficient aeration, and rainfall.

The farm requires an early-warning application that analyzes pond conditions recorded at 8:00 PM and predicts whether oxygen levels may fall below 4 mg/L by 5:00 AM.

The system classifies pond-night conditions into:

- **High** – Increased oxygen depletion risk.
- **Normal** – Relatively lower oxygen depletion risk.

The predicted risk is used to provide an aeration-related recommendation to support pond management.

---

## 3. Objectives

- Generate a synthetic dataset containing at least 250 pond-night observations.
- Create and manage Dataset Version 1 and Version 2.
- Simulate rainy-period conditions in Version 2.
- Validate and preprocess the dataset.
- Engineer reusable features.
- Store and reuse engineered features.
- Train Logistic Regression and Random Forest models.
- Compare models using Precision, Recall, and F1-score.
- Track experiments using MLflow.
- Register the selected model in MLflow Model Registry.
- Develop a FastAPI prediction application.
- Implement `/predict` and `/health` endpoints.
- Automate data validation and prediction testing.
- Implement CI using GitHub Actions.

---

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data manipulation |
| NumPy | Numerical computation |
| Scikit-learn | Machine learning |
| Logistic Regression | Classification model |
| Random Forest | Ensemble classifier |
| MLflow | Experiment tracking and model registry |
| FastAPI | Model serving and REST APIs |
| Uvicorn | API server |
| Pytest | Automated testing |
| HTTPX | API testing |
| Joblib | Model serialization |
| GitHub | Version control |
| GitHub Actions | Continuous integration |
| Google Colab | Development environment |

---

## 5. System Architecture

```text
          Pond Data / Synthetic Dataset
                     |
                     v
         Dataset Versioning and Validation
                     |
                     v
           Data Preprocessing Pipeline
                     |
                     v
             Feature Engineering
                     |
                     v
          Reusable Feature File / Store
                     |
                     v
         Logistic Regression & Random Forest
                     |
                     v
             Model Evaluation
                     |
                     v
           MLflow Tracking & Registry
                     |
                     v
              FastAPI Model Serving
                     |
          +----------+----------+
          |                     |
          v                     v
       /health                /predict
          |                     |
          v                     v
     API Status           Oxygen Risk Prediction
                                |
                                v
                    Night-time Aeration Advice
                                |
                                v
                    GitHub Actions CI Testing
```

---

## 6. Dataset Creation and Versioning

### Dataset Features

| Feature | Description |
|---|---|
| Pond Area | Total area of the aquaculture pond |
| Stocking Density | Shrimp density per square meter |
| DO at 8 PM | Dissolved oxygen concentration at 8 PM |
| Water Temperature | Pond temperature in Celsius |
| Daily Feed | Feed quantity supplied |
| Planned Aeration Hours | Planned aerator operating time |
| Expected Rainfall | Expected rainfall in millimeters |
| Oxygen Risk | Target variable: High or Normal |

### Dataset Versions

**Version 1 – Baseline Dataset**

Represents initial pond operating conditions.

**Version 2 – Rainy Period Dataset**

Represents rainy-period environmental conditions with increased rainfall and oxygen depletion risk.

Dataset versioning allows comparison of different environmental conditions and supports reproducible model development.

---

## 7. Data Preprocessing and Feature Engineering

Data preprocessing includes:

- Checking required columns.
- Validating dataset size.
- Checking missing values.
- Validating numerical values.
- Checking target labels.
- Preparing model features.

### Engineered Features

#### Feed per Unit Biomass

\[
FeedRatio = \frac{FeedQuantity}{EstimatedBiomass}
\]

This feature represents feeding intensity relative to shrimp biomass.

#### Aeration Hours per Area

\[
AerationRatio = \frac{AerationHours}{PondArea}
\]

This feature represents aeration duration relative to pond area.

The engineered features are stored in reusable feature files and loaded separately during model training.

---

## 8. Machine Learning Models

Two classifiers are implemented.

### Logistic Regression

Logistic Regression is a supervised classification algorithm that estimates the probability of a data point belonging to a class.

It is used as a baseline model because it is simple, computationally efficient, and interpretable.

### Random Forest

Random Forest is an ensemble machine learning algorithm that combines predictions from multiple decision trees.

It can capture nonlinear relationships and complex interactions among environmental and operational features.

### Model Evaluation Metrics

Models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-score

Recall for the High Risk class is particularly important because failing to identify a high-risk pond may result in missing a potential oxygen depletion event.

### Model Comparison

| Model | Precision | Recall | F1-score |
|---|---|---|---|
| Logistic Regression | Measured | Measured | Measured |
| Random Forest | Measured | Measured | Measured |

The selected model is registered in MLflow based on the evaluation results.

---

## 9. MLflow Experiment Tracking

MLflow is used to manage machine learning experiments and model artifacts.

### Features

- Experiment tracking
- Parameter logging
- Metric logging
- Model artifact storage
- Model registration
- Model version management

### Workflow

```text
Train Models
     |
     v
Evaluate Models
     |
     v
Log Parameters and Metrics
     |
     v
Compare Experiments
     |
     v
Select Best Model
     |
     v
Register Model in MLflow
```

The selected model is registered under:

`Aquaculture_Risk_Classifier_Best`

---

## 10. FastAPI Model Serving

FastAPI provides REST endpoints to interact with the trained model.

### Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Checks application health |
| `/predict` | POST | Predicts oxygen depletion risk |

### Health Endpoint

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Aquaculture Oxygen Risk Prediction API"
}
```

### Prediction Endpoint

```http
POST /predict
```

Example request:

```json
{
  "feed_given_kg": 200,
  "shrimp_biomass_kg": 5000,
  "aeration_run_hours": 8,
  "pond_area_sq_meters": 2000,
  "water_temp_celsius": 30,
  "dissolved_oxygen_ppm": 4.2
}
```

Example response:

```json
{
  "oxygen_risk": "Normal",
  "high_risk_probability": 0.39,
  "additional_night_aeration_required": false,
  "recommendation": "Continue scheduled aeration and routine oxygen monitoring."
}
```

The API provides a prediction, risk probability, aeration indication, and recommendation.

---

## 11. Automated Testing

Pytest is used to test API functionality.

### Test Cases

| Test | Purpose | Expected Result |
|---|---|---|
| Health Test | Check API health | HTTP 200 |
| Prediction Test | Submit valid pond data | Valid prediction |
| Invalid Input Test | Submit invalid values | HTTP 422 |

### Test Command

```bash
pytest test_api.py -v
```

### Test Results

```text
test_health PASSED
test_prediction PASSED
test_invalid_input PASSED

3 passed
```

The tests verify the health endpoint, prediction functionality, and input validation.

---

## 12. CI/CD Using GitHub Actions

GitHub Actions automates testing when code is pushed to the repository or when a pull request is created.

### CI Pipeline Steps

1. Checkout repository.
2. Configure Python 3.11.
3. Install dependencies.
4. Validate model artifacts.
5. Execute Pytest tests.
6. Report the workflow status.

### Workflow File

Location:

```text
.github/workflows/ci.yml
```

### GitHub Actions Configuration

```yaml
name: Aquaculture Oxygen Risk CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Validate model files
        run: |
          test -f aquaculture_model.pkl
          test -f feature_columns.pkl
          echo "Model files validated successfully"

      - name: Run automated tests
        run: pytest test_api.py -v
```

### CI Result

The GitHub Actions workflow was executed successfully.

The workflow automatically installed dependencies, validated model files, and executed automated tests.

**Status: Successful**

---

## 13. Results

The project successfully implemented the main MLOps components.

| Component | Status |
|---|---|
| Dataset creation | Completed |
| Dataset Version 1 | Completed |
| Dataset Version 2 | Completed |
| Data validation | Implemented |
| Feature engineering | Implemented |
| Feature storage and reuse | Implemented |
| Logistic Regression | Implemented |
| Random Forest | Implemented |
| Model evaluation | Implemented |
| MLflow tracking | Implemented |
| Model registration | Implemented |
| FastAPI application | Implemented |
| `/health` endpoint | Tested |
| `/predict` endpoint | Tested |
| Input validation | Tested |
| Pytest | 3 tests passed |
| GitHub repository | Created |
| GitHub Actions CI | Successful |

---

## 14. Conclusion

This project demonstrates an end-to-end MLOps workflow for predicting night-time oxygen depletion risk in shrimp aquaculture ponds.

Synthetic datasets were created and versioned, preprocessing and feature engineering were implemented, and machine learning models were trained and compared.

MLflow was used for experiment tracking and model registration. FastAPI was implemented to serve model predictions through REST endpoints. Pytest was used to validate the application, while GitHub Actions automated the testing process.

The project demonstrates the integration of data management, machine learning, model lifecycle management, model serving, testing, and continuous integration.

---

## 15. Future Scope

- Integration with real-time dissolved oxygen sensors.
- IoT-based pond monitoring.
- Real aquaculture dataset collection.
- Cloud deployment of the API.
- Farmer dashboard.
- Automated aerator control.
- Model drift monitoring.
- Automated retraining.
- Risk alert notifications.
- Model explainability.

---

## 16. Project Structure

```text
aquaculture-oxygen-risk-mlops/
│
├── main.py
├── test_api.py
├── requirements.txt
│
├── aquaculture_model.pkl
├── feature_columns.pkl
│
├── pond_dataset_v1.csv
├── pond_dataset_v2.csv
├── features_v1.csv
├── features_v2.csv
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── README.md
```

---

## 17. Sample Prediction

### Input

| Parameter | Value |
|---|---:|
| Feed | 200 kg |
| Shrimp Biomass | 5000 kg |
| Aeration Hours | 8 |
| Pond Area | 2000 m² |
| Water Temperature | 30°C |
| Dissolved Oxygen | 4.2 mg/L |

### Output

| Field | Prediction |
|---|---|
| Oxygen Risk | Normal |
| High Risk Probability | 0.39 |
| Additional Aeration | False |
| Recommendation | Continue scheduled aeration and routine oxygen monitoring |

---

## 18. Evidence

Screenshots of dataset versions, feature engineering, model training, MLflow, API testing, Pytest, GitHub repository, and successful GitHub Actions execution are included in the project report.

---

## 19. Repository

**GitHub Repository:**  
[Insert your repository link here]

---

### Submitted By

**Name:** Sri Harsha  
**Registration Number:** 231FA04092  
**Section:** 15  
**Subject:** MLOps Lab External
