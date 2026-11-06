import os
from math import dist
from typing import Literal, get_args
from training.datasetManager import DatasetManager

import pygame

ScenesNames = Literal['splashscreen', 'main', 'sandbox', "view_dataset"]

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
				'MIN_PIXELS_DISTANCE': 4,
				'drawn_pixels': []
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
			if not len(line) or dist(pygame.mouse.get_pos(), line[-1]) > self.scenes_data['sandbox']['MIN_PIXELS_DISTANCE']:
				line.append(pygame.mouse.get_pos())
				refresh_screen = True

		# submitting
		elif any(e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN for e in events):
			# TODO: bridge draw pixels with ../classification/ logic
			print(self.scenes_data['sandbox']['drawn_pixels'])

			self.scenes_data['sandbox']['drawn_pixels'].clear()
			refresh_screen = True

		# drawing
		if refresh_screen:
			window.fill((255, 255, 255))
			for line in self.scenes_data['sandbox']['drawn_pixels']:
				if len(line) > 2: pygame.draw.lines(window, (0, 0, 0), False, line, width=6)

	def __view_dataset(self, window: pygame.Surface, events: list[pygame.event.Event]):
		'''Viewing the dataset for testing purposes with LEFT/RIGHT arrow keys.'''
		data = self.scenes_data['view_dataset']
		Screen_size = 30
		refresh_screen = False

		#Préparation du montrage du Data
		if "dataset" not in data:
			source = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			dataset, indice = DatasetManager(os.path.join(source, 'data', 'dataset.csv')).fetch()
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
				couleur = valeur if valeur == 0 else 255
				Petit_ecran.set_at((i % Screen_size, i // Screen_size), (couleur,couleur,couleur))

			#Aggrandir l'écran pour mieux voir
			Grandeur_ecran = min(window.get_size())// Screen_size
			window.blit(pygame.transform.scale(Petit_ecran, (Screen_size*Grandeur_ecran, Screen_size*Grandeur_ecran)),(0,0))
