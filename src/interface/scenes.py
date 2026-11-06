from math import dist
from typing import get_args

import pygame

from customTypes import ScenesNames
from model.predict import predict
from utils.coordsToMatrix import coords_to_matrix


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
		}
		self.scenes_data = {
			'sandbox': {
				'MIN_PIXELS_DISTANCE': 1,
				'drawn_pixels': []
			},
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
			print(self.scenes_data['sandbox']['drawn_pixels'])
			matrix = coords_to_matrix(self.scenes_data['sandbox']['drawn_pixels'], window.get_size(), (30, 30))
			# print('\n'.join(' '.join(str(cell) for cell in line) for line in matrix))
			prediction = predict([[val for line in matrix for val in line]])
			# prediction = predict(matrix)
			print(prediction)

			self.scenes_data['sandbox']['drawn_pixels'].clear()
			refresh_screen = True

		# drawing
		if refresh_screen:
			window.fill((255, 255, 255))
			for line in self.scenes_data['sandbox']['drawn_pixels']:
				if len(line) > 2: pygame.draw.lines(window, (0, 0, 0), False, line, width=6)
