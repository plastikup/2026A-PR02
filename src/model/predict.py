import joblib
import numpy as np
import cv2

"""Junyi type this in your terminal: python -m pip install opencv-python """

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

		data = data.reshape(1, -1)
		predictions = self.model.predict(data)
		return predictions

	def __reverse_alpha(self, matrix: np.ndarray) -> np.ndarray:
		return 255 - matrix
	
	def __normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
		return matrix / 255
	
	def __center_to_subject(self, matrix: np.ndarray) -> np.ndarray: 
		Grandeur_window = matrix.shape

		#Chercher tous les pixels qui ne sont pas blanc
		ligne, colonne = np.where(matrix < 1)
		if ligne.size == 0:
			return matrix

		#Trouver tous les bordures du dessin
		Hauteur, Bas = ligne.min(), ligne.max()+1
		Gauche, Droite = colonne.min(), colonne.max()+1
		Dessin_sans_Bord = matrix[Hauteur:Bas, Gauche:Droite]

		#Grandire la bordure pour que le dession etre au centre
		Haut, Larg = Dessin_sans_Bord.shape
		Expand_border_vert = int(round(Haut*0.15)) #Expand border par 15%
		Expand_border_Hori = int(round(Larg*0.15))
		Dessin_avec_Bord = np.pad(Dessin_sans_Bord, ((Expand_border_vert,Expand_border_vert),(Expand_border_Hori,Expand_border_Hori)), constant_values=1)

		#Reajust Drawing with Border to the window size
		return cv2.resize(Dessin_avec_Bord.astype(np.float32), (30, 30), interpolation=cv2.INTER_AREA)


