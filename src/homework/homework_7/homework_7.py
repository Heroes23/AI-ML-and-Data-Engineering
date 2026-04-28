"""
FastAPI application for breast cancer classification using XGBoost
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import xgboost as xgb
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import numpy as np 
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Breast Cancer Classification API", version="1.0.0")

# Global variables for model and metrics
model = None
metrics = {}
feature_names = []


class PredictionInput(BaseModel):
    """Input features for breast cancer prediction"""
    features: List[float] = Field(
        ...,
        description="30 features from breast cancer dataset",
        min_items=30,
        max_items=30
    )

    class Config:
        schema_extra = {
            "example": {
                "features": [
                    17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471,
                    0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904,
                    0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0,
                    0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
                ]
            }
        }


class PredictionOutput(BaseModel):
    """Output prediction results"""
    prediction: int = Field(..., description="Predicted class: 0 (malignant) or 1 (benign)")
    probability: float = Field(..., description="Probability of the predicted class")
    class_probabilities: Dict[str, float] = Field(..., description="Probabilities for both classes")


class MetricsOutput(BaseModel):
    """Model performance metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    dataset_info: Dict[str, int]


def train_model():
    """Train XGBoost model on breast cancer dataset"""
    global model, metrics, feature_names

    # Load breast cancer dataset
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train XGBoost classifier
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )

    model.fit(X_train, y_train)

    # Calculate metrics on test set
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1_score": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
        "dataset_info": {
            "total_samples": int(len(X)),
            "training_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "n_features": int(X.shape[1])
        }
    }

    print("Model trained successfully!")
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")


@app.on_event("startup")
async def startup_event():
    """Train model when the application starts"""
    print("Training XGBoost model on breast cancer dataset...")
    train_model()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Breast Cancer Classification API",
        "endpoints": {
            "/metrics": "GET - View model performance metrics",
            "/predict": "POST - Make predictions on breast cancer features",
            "/docs": "GET - Interactive API documentation"
        }
    }


@app.get("/metrics", response_model=MetricsOutput)
async def get_metrics():
    """
    Get model performance metrics

    Returns metrics calculated on the test set:
    - Accuracy
    - Precision
    - Recall
    - F1 Score
    - ROC AUC Score
    - Dataset information
    """
    if not metrics:
        raise HTTPException(status_code=503, detail="Model not trained yet")

    return MetricsOutput(**metrics)


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Make predictions on breast cancer features

    Expects 30 features as input:
    - Mean radius, texture, perimeter, area, smoothness, compactness,
      concavity, concave points, symmetry, fractal dimension
    - Standard error of the above features
    - "Worst" or largest values for the above features

    Returns:
    - prediction: 0 (malignant) or 1 (benign)
    - probability: Confidence of the prediction
    - class_probabilities: Probabilities for both classes
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not trained yet")

    try:
        # Convert input to numpy array
        features = np.array(input_data.features).reshape(1, -1)

        # Make prediction
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]

        # Get probability of predicted class
        probability = float(probabilities[prediction])

        return PredictionOutput(
            prediction=prediction,
            probability=probability,
            class_probabilities={
                "malignant (0)": float(probabilities[0]),
                "benign (1)": float(probabilities[1])
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.get("/feature-names")
async def get_feature_names():
    """Get the list of feature names expected by the model"""
    if not feature_names:
        raise HTTPException(status_code=503, detail="Model not trained yet")

    return {
        "feature_names": feature_names,
        "count": len(feature_names),
        "description": "30 features from the breast cancer dataset"
    }


if __name__ == "__main__":
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
