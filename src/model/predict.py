import joblib
import numpy as np

from constants import TRAINED_MODEL_PATH


class PredictionPipeline:
	def __init__(self):
		self.model = joblib.load(TRAINED_MODEL_PATH)
		self.pipe = [self.__reverse_alpha, self.__normalize_matrix, self.__center_to_subject]

	def predict(self, transparency_matrix: np.ndarray) -> list[int]:
		# transparency_matrix is a 2d numpy array of alpha=[0,255]
		data = transparency_matrix
		for fn in self.pipe:
			data = fn(data)

		predictions = self.model.predict(data)
		return predictions

	def __reverse_alpha(self, matrix: np.ndarray) -> np.ndarray: pass
	def __normalize_matrix(self, matrix: np.ndarray) -> np.ndarray: pass
	def __center_to_subject(self, matrix: np.ndarray) -> np.ndarray: pass
