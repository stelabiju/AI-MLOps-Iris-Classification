import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score


def validate_model():
    print("Validating model...")

    model = joblib.load("model.pkl")

    data = load_iris()
    predictions = model.predict(data.data)

    accuracy = accuracy_score(data.target, predictions)

    print(f"Model accuracy: {accuracy:.4f}")

    if accuracy < 0.90:
        print("Model validation failed.")
        return False

    print("Model validation passed.")
    return True


if __name__ == "__main__":
    if not validate_model():
        raise SystemExit(1)

