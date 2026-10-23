import csv

from src.constants import DATASET_MAX_VALUE
from src.types import Dataset


class DatasetManager:
	def __init__(self, path: str):
		self.path = path

	def fetch(self) -> Dataset:
		'''
		Cherche le jeu de données à partir du fichier système et le retourne normalisé.
		'''
		dataset = self.__load_csv_dataset_from_file()
		return self.__normalize_dataset(dataset, DATASET_MAX_VALUE)

	def __load_csv_dataset_from_file(self) -> Dataset:
		'''
		Lit un jeu de données CSV à partir d'un fichier et le retourne sous forme de tuple de tuples de floats.
		'''
		with open(self.path, 'r', encoding='utf-8', newline = '') as file:
			reader = csv.reader(file)
			return tuple(
				tuple(float(digit) for digit in line)
				for line in reader
			)

	def __normalize_dataset(self, dataset: Dataset, cap: float) -> Dataset:
		'''
		Normalise un jeu de données en divisant tous les chiffres par une valeur `cap` fournie.
		'''
		return tuple(
			tuple(float(digit / cap) for digit in line)
			for line in dataset
		)
