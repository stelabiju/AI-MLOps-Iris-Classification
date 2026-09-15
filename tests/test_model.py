import joblib
from sklearn.datasets import load_iris


def test_model_exists():
    model = joblib.load("model.pkl")
    assert model is not None


def test_model_prediction():
    model = joblib.load("model.pkl")
    data = load_iris()

    predictions = model.predict(data.data)

    assert len(predictions) == len(data.target)
    assert all(prediction in [0, 1, 2] for prediction in predictions)

