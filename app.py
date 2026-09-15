import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Iris Classification API", version="1.0.0")

# Load model (or train a default one on startup if model.pkl doesn't exist yet)
try:
    model = joblib.load("model.pkl")
except Exception:
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    data = load_iris()
    model = RandomForestClassifier()
    model.fit(data.data, data.target)
    joblib.dump(model, "model.pkl")

class IrisInput(BaseModel):
    features: list[float]  # e.g., [5.1, 3.5, 1.4, 0.2]

@app.post("/predict")
def predict(input_data: IrisInput):
    if len(input_data.features) != 4:
        raise HTTPException(status_code=400, detail="Exactly 4 features required.")
    
    prediction = model.predict([input_data.features])
    return {
        "model_version": "1.0.0",
        "prediction": int(prediction[0])
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
