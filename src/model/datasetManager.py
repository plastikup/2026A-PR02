import csv
import os

from constants import DATASET_MAX_VALUE
from customTypes import Dataset, Indices


class DatasetManager:
	def __init__(self, path: str):
		if not os.path.exists(path): raise FileNotFoundError()
		self.path = path

	def fetch(self) -> tuple[Dataset, Indices]:
		'''
		Cherche le jeu de données à partir du fichier système et le retourne normalisé.
		'''
		dataset, indices = self.__load_csv_dataset_from_file()
		return self.__normalize_dataset(dataset, DATASET_MAX_VALUE), indices

	def __load_csv_dataset_from_file(self) -> tuple[Dataset, Indices]:
		'''
		Lit un jeu de données CSV à partir d'un fichier et le retourne sous forme de tuple de tuples de floats.
		'''
		with open(self.path, 'r', encoding='utf-8', newline = '') as file:
			reader = [*csv.reader(file)]
			dataset = tuple(
				tuple(float(digit) for digit in line[:-1])
				for line in reader
			)
			indices = tuple(int(line[-1]) for line in reader)
			return dataset, indices

	def __normalize_dataset(self, dataset: Dataset, cap: float) -> Dataset:
		'''
		Normalise un jeu de données en divisant tous les chiffres par une valeur `cap` fournie.
		'''
		return tuple(
			tuple(float(digit / cap) for digit in line)
			for line in dataset
		)
