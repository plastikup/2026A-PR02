import cv2
import joblib
import numpy as np

from constants import TRAINED_MODEL_PATH


class PredictionPipeline:
	def __init__(self):
		self.model = joblib.load(TRAINED_MODEL_PATH)
		self.pipe = [self.__transpose_matrix, self.__normalize_matrix, self.__center_to_subject]

	def predict(self, rgb_matrix: np.ndarray) -> list[int]:
		gray_matrix = np.dot(rgb_matrix, [0.299, 0.587, 0.114])
		data = gray_matrix
		for fn in self.pipe:
			data = fn(data)

		data = data.reshape(1, -1)
		print(*sorted(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', *self.model.predict_proba(data).tolist()), key=lambda e: -e[1]))
		predictions = self.model.predict(data)
		return predictions

	def __debug(self, matrix: np.ndarray) -> None:
		"""For internal usage only. Writes out a provided matrix."""
		with open('out.txt', 'w') as f: f.write(' '.join(str(round(num, 1)) for num in matrix))

	def __transpose_matrix(self, matrix: np.ndarray) -> np.ndarray:
		return matrix.T

	def __normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
		return matrix / 255

	def __center_to_subject(self, matrix: np.ndarray) -> np.ndarray:
		#Chercher tous les pixels qui ne sont pas blanc
		ligne, colonne = np.where(matrix < 1)
		if ligne.size == 0:
			return matrix

		#Trouver tous les bordures du dessin
		hauteur, bas = ligne.min(), ligne.max()+1
		gauche, droite = colonne.min(), colonne.max()+1
		dessin_sans_bord = matrix[hauteur:bas, gauche:droite]

		#Grandire la bordure pour que le dession etre au centre
		haut, larg = dessin_sans_bord.shape
		expand_border_vert = round(haut*0.20) #Expand border par 20%
		expand_border_hori = round(larg*0.20)
		dessin_avec_bord = np.pad(dessin_sans_bord, ((expand_border_vert,expand_border_vert),(expand_border_hori,expand_border_hori)), constant_values=1)

		#Reajust Drawing with Border to the window size
		return cv2.resize(dessin_avec_bord, (30, 30), interpolation=cv2.INTER_AREA)
