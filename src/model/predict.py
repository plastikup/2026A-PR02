import joblib

from constants import TRAINED_MODEL_PATH

model = joblib.load(TRAINED_MODEL_PATH)

def predict(*data: list[float]) -> int:
	predictions = model.predict(data)
	return predictions
