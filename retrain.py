import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def retrain_model():
    print("Fetching new data and retraining model...")
    data = load_iris()
    
    # Train new model instance
    new_model = RandomForestClassifier(n_estimators=100, random_state=42)
    new_model.fit(data.data, data.target)
    
    # Save model artifact
    joblib.dump(new_model, "model.pkl")
    print("Retraining complete. Model saved as model.pkl")

if __name__ == "__main__":
    retrain_model()