import math
from typing import get_args

import pygame

from constants import DATASET_PATH
from customTypes import ScenesNames
from model.datasetManager import DatasetManager
from model.predict import predict
from utils.coordsToMatrix import coords_to_matrix


def generate_fake_pencil_surface(size: int) -> pygame.Surface:
	'''
	Generate a fake pencil surface with a fading effect
	'''
	pencil = pygame.Surface((size, size), pygame.SRCALPHA)
	center = size // 2
	for j in range(size):
		for i in range(size):
			dist = math.dist((i, j), (center, center))
			normalized_dist = min(dist / center, 1)
			alpha = 255 - round(normalized_dist * 255)
			pencil.set_at((i, j), (0, 0, 0, alpha))
	return pencil


class Scenes:
	def __init__(self):
		self._scene = 'splashscreen'
		self._switched_scene = True
		self._globals = {
			'previously_mousedown': False
		}
		self._scenes = {
			'splashscreen': self.__splashscreen,
			'main': self.__main,
			'sandbox': self.__sandbox,
			"view_dataset": self.__view_dataset

		}
		self.scenes_data = {
			'sandbox': {
				'MIN_PIXELS_DISTANCE': 1,
				'drawn_pixels': [],
				'pencil': generate_fake_pencil_surface(16)
			},
			"view_dataset": {
			}
		}

	@property
	def active_scene(self):
		return self._scene

	@active_scene.setter
	def active_scene(self, next_scene: ScenesNames):
		if next_scene not in get_args(ScenesNames): raise ValueError('Unexpected scene name')
		self._scene = next_scene

	def refresh_animation_frame(self, window: pygame.Surface, events: list[pygame.event.Event]):
		# call the scene function
		self._scenes[self._scene](window, events)

		# clear ephemeral flags and update globals
		self._switched_scene = False
		self._globals['previously_mousedown'] = pygame.mouse.get_pressed()[0]

	def __splashscreen(self, window: pygame.Surface, events: list[pygame.event.Event]):
		pass

	def __main(self, window: pygame.Surface, events: list[pygame.event.Event]):
		pass

	def __sandbox(self, window: pygame.Surface, events: list[pygame.event.Event]):
		'''For internal testing and debugging purposes only.'''
		refresh_screen = False

		# registering
		if pygame.mouse.get_pressed()[0]:
			# create a new line array if new mousedown
			if not self._globals['previously_mousedown']:
				self.scenes_data['sandbox']['drawn_pixels'].append([])

			# create an easy-access reference to the line array
			line = self.scenes_data['sandbox']['drawn_pixels'][-1]

			# register the pixel if the distance is greater than the minimum required
			if not len(line) or math.dist(pygame.mouse.get_pos(), line[-1]) > self.scenes_data['sandbox']['MIN_PIXELS_DISTANCE']:
				line.append(pygame.mouse.get_pos())
				refresh_screen = True

		# submitting
		elif any(e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN for e in events):
			print(self.scenes_data['sandbox']['drawn_pixels'])
			matrix = coords_to_matrix(self.scenes_data['sandbox']['drawn_pixels'], window.get_size(), (30, 30))
			# print('\n'.join(' '.join(str(cell) for cell in line) for line in matrix))
			prediction = predict([val for line in matrix for val in line])
			# prediction = predict(matrix)
			print(prediction)

			self.scenes_data['sandbox']['drawn_pixels'].clear()
			refresh_screen = True

		# drawing
		if refresh_screen:
			window.fill((255, 255, 255, 255))
			for line in self.scenes_data['sandbox']['drawn_pixels']:
				for coords in line:
					window.blit(self.scenes_data['sandbox']['pencil'], coords)

	def __view_dataset(self, window: pygame.Surface, events: list[pygame.event.Event]):
		'''Viewing the dataset for testing purposes with LEFT/RIGHT arrow keys.'''
		data = self.scenes_data['view_dataset']
		Screen_size = 30
		refresh_screen = False

		#Préparation du montrage du Data
		if "dataset" not in data:
			dataset, indice = DatasetManager(DATASET_PATH).fetch()
			data["dataset"] = dataset
			data["indice"] = indice
			data["posligne"] = 0

		#Interface Humain pour voir le data de chaque ligne
		Keys = pygame.key.get_pressed()
		if Keys[pygame.K_RIGHT]:
			data["posligne"] = data["posligne"] +1 % len(data["dataset"])
			refresh_screen = True
		if Keys[pygame.K_LEFT]:
			data["posligne"] = data["posligne"] -1 % len(data["dataset"])
			refresh_screen = True

		#Dessiner et rafraichissement d'écran
		if refresh_screen:
			window.fill((255, 255, 255))

			pixeldraw = data["dataset"][data["posligne"]]
			Petit_ecran = pygame.Surface((Screen_size, Screen_size)) #Dessin d'écran selon les valeurs dans le Data

			#Dessin du Data
			for i, valeur in enumerate(pixeldraw):
				# value has been normalized to 0-1
				Petit_ecran.set_at((i % Screen_size, i // Screen_size), (valeur*255,valeur*255,valeur*255))

			#Aggrandir l'écran pour mieux voir
			Grandeur_ecran = min(window.get_size())// Screen_size
			window.blit(pygame.transform.scale(Petit_ecran, (Screen_size*Grandeur_ecran, Screen_size*Grandeur_ecran)),(0,0))
