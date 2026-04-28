# Homework 7: Breast Cancer Classification API

A FastAPI application that provides breast cancer classification using an XGBoost model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Run the application with:
```bash
python homework_7.py
```

Or using uvicorn directly:
```bash
uvicorn homework_7:app --reload
```

The API will be available at: `http://localhost:8000`

## Endpoints

### 1. GET `/metrics`
Returns model performance metrics including:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC Score
- Dataset information

**Example:**
```bash
curl http://localhost:8000/metrics
```

### 2. POST `/predict`
Makes predictions on breast cancer features (30 features required).

**Example:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471,
      0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904,
      0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0,
      0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
    ]
  }'
```

**Response:**
```json
{
  "prediction": 0,
  "probability": 0.99,
  "class_probabilities": {
    "malignant (0)": 0.99,
    "benign (1)": 0.01
  }
}
```

### 3. GET `/feature-names`
Returns the list of 30 feature names expected by the model.

## Interactive Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- **Automatic Model Training**: The XGBoost model is trained on the breast cancer dataset when the application starts
- **Input Validation**: Uses Pydantic models to validate input data
- **Comprehensive Metrics**: Provides detailed model performance metrics
- **Interactive Docs**: Built-in Swagger UI for easy testing
