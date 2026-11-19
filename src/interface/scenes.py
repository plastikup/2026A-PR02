import math
import sys
from typing import get_args

import pygame

from constants import DATASET_PATH
from customTypes import ScenesNames
from model.datasetManager import DatasetManager
from model.predict import PredictionPipeline

predictionPipeline = PredictionPipeline()


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
		self.history = []
		self._globals = {
			'previously_mousedown': False
		}
		self._scenes = {
			'main': self.__main,
			'sandbox': self.__sandbox,
			"view_dataset": self.__view_dataset

		}
		self.scenes_data = {
			'sandbox': {
				'MIN_PIXELS_DISTANCE': 1,
				'drawn_pixels': [],
				'pencil': generate_fake_pencil_surface(4)
			},
			'main': {
				'MIN_PIXELS_DISTANCE': 1,
				'drawn_pixels': [],
				'ui': None,
				'pencil': generate_fake_pencil_surface(50)
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

		#self._globals['previously_mousedown'] = pygame.mouse.get_pressed()[0]


	@staticmethod
	def __build_ui(window: pygame.Surface):
		"""Les parametres et les positions des dashboards du UI design"""
		largeur, hauteur = window.get_size()
		espace_marge =	1/50 #Espace de marge vide entre les dashboard et les bouttons
		longueur_sous_fenetre = (1-espace_marge*4)/3 #la largeur des dashboards et des bouttons sous le canvas de dessins
		hauteur_sous_fenetre = (1-0.6-espace_marge*3) #l'hauteur total du dashboard sous le canvas de dessins
		hauteur_sous_fenetre_bouton = (hauteur_sous_fenetre-espace_marge*2)/3 #hauteur de chaque bouton
		hauteur_fenetre_predire = hauteur_sous_fenetre - hauteur_sous_fenetre_bouton - espace_marge #hauteur du dashboard prediction

		def rect(x,y,larg,haut): #dessiner
					return pygame.Rect(round(x*largeur),round(y*hauteur),round(larg*largeur),round(haut*hauteur))

		#position des dashboards
		fenetre_pos = {
			"canvas_dessin": rect(espace_marge, espace_marge, (1-espace_marge*2), 0.6),
			"graphe": rect(espace_marge, espace_marge*2 + 0.6, longueur_sous_fenetre, hauteur_sous_fenetre),
			"boutton_predire": rect(espace_marge*2 + longueur_sous_fenetre, espace_marge*2 + 0.6, longueur_sous_fenetre, hauteur_sous_fenetre_bouton),
			"boutton_eff": rect(espace_marge*2 + longueur_sous_fenetre, espace_marge*3 + 0.6 + hauteur_sous_fenetre_bouton, longueur_sous_fenetre, hauteur_sous_fenetre_bouton),
			"quitter": rect(espace_marge*2 + longueur_sous_fenetre, espace_marge*4 + 0.6 + hauteur_sous_fenetre_bouton*2, longueur_sous_fenetre, hauteur_sous_fenetre_bouton),
			"predire": rect(espace_marge*3 + longueur_sous_fenetre*2, espace_marge*2 + 0.6, longueur_sous_fenetre, hauteur_fenetre_predire),
			"historique": rect(espace_marge*3 + longueur_sous_fenetre*2, espace_marge*3 + 0.6 + hauteur_fenetre_predire, longueur_sous_fenetre, hauteur_sous_fenetre_bouton)
		}

		return fenetre_pos

	@staticmethod
	def __dessiner_UI(window: pygame.Surface, dict_fenetre, mouse_position, histoire):
		"""Dessiner tous sur le window pygame"""
		#parametre couleur
		blanc = (255,255,255)
		cyan = (82, 214, 244)
		#parametre des textes
		font = pygame.font.SysFont("Open Sans", 60)
		font_petit = pygame.font.SysFont("Open Sans", 36)
		textes = {
			"boutton_predire": "Prédire",
			"boutton_eff": "Effacer",
			"quitter": "Quitter"
		}

		#Dessiner ou le backgound du windows
		window.fill((23, 35, 61, 255))

		#Le canvas de dessins
		pygame.draw.rect(window, (255,255,255), dict_fenetre["canvas_dessin"], border_radius= 12)

		#Assigner tous les positions d'interface humaine (boutons)
		for items in dict_fenetre: #Change color depending if mouse if hover or not on the specific buttons
			if items == mouse_position:
				pygame.draw.rect(window, blanc, dict_fenetre[items], width=2, border_radius=12)
			else:
				pygame.draw.rect(window, cyan, dict_fenetre[items], width=2, border_radius=12)

		#Assigner tous les positions des textes
		for nom in textes: #Same thing here about color changes
			if nom == mouse_position:
				ecrire = font.render(textes[nom], True, blanc)
				window.blit(ecrire, ecrire.get_rect(center=dict_fenetre[nom].center))
			else:
				ecrire = font.render(textes[nom], True, cyan)
				window.blit(ecrire, ecrire.get_rect(center=dict_fenetre[nom].center))

		#Texte d'historique des predictions
		tous_lettres = " ".join(str(lettre) for lettre in reversed(histoire[-7:]))
		text_histoire = font_petit.render(" Historique: " + tous_lettres, True, cyan)
		position_hist = dict_fenetre["historique"]
		window.blit(text_histoire, text_histoire.get_rect(midleft=(position_hist.left, position_hist.centery)))

		#Texte du titre de la case de prediction
		text_prediction = font_petit.render("Votre lettre est", True, cyan)
		position_prediction = dict_fenetre["predire"]
		window.blit(text_prediction, text_prediction.get_rect(midtop= (position_prediction.centerx, position_prediction.top + 10)))

		#Texte du lettre predit
		Lettre_predic = "".join(str(lettre) for lettre in histoire[-1]) if histoire else None
		text_predire = font.render(Lettre_predic, True, cyan)
		position_pred = dict_fenetre["predire"]
		window.blit(text_predire, text_predire.get_rect(center=position_pred.center))


	def __main(self, window: pygame.Surface, events: list[pygame.event.Event]):
		"""Real Interface to present to the public"""
		#Parametre et settings
		selected_button = None
		data = self.scenes_data['main']

		# update ui objs
		if data['ui'] == None: data['ui'] = self.__build_ui(window)

		#Detecter la position de souris et change le couleur du case si la sourie est dedant
		pos_souris = pygame.mouse.get_pos()
		for item in ("boutton_predire","boutton_eff","quitter"):
			if data['ui'][item].collidepoint(pos_souris):
				selected_button = item
				break

		###Registering drawing###
		mousedown = any(e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 for e in events)
		dessiner = pygame.mouse.get_pressed()[0] and data['ui']["canvas_dessin"].collidepoint(pygame.mouse.get_pos())
		predict = mousedown and data['ui']["boutton_predire"].collidepoint(pos_souris) and any(self.scenes_data['main']['drawn_pixels'])
		erase = mousedown and data['ui']["boutton_eff"].collidepoint(pos_souris)
		quit = mousedown and data['ui']["quitter"].collidepoint(pos_souris)
		if dessiner:
			# create a new line array if new mousedown
			if not self._globals['previously_mousedown']:
				self.scenes_data['main']['drawn_pixels'].append([])

			# create an easy-access reference to the line array
			line = self.scenes_data['main']['drawn_pixels'][-1]

			# register the pixel if the distance is greater than the minimum required
			if not len(line) or math.dist(pygame.mouse.get_pos(), line[-1]) > self.scenes_data['main']['MIN_PIXELS_DISTANCE']:
				line.append(pygame.mouse.get_pos())


		###Les boutons###
		#Validation du dessin
		elif predict:
			rgb_matrix = pygame.surfarray.pixels3d(window.subsurface(data['ui']["canvas_dessin"]))
			prediction_index = predictionPipeline.predict(rgb_matrix)
			del rgb_matrix # pygame locks surface unless explicitly deleting reference
			prediction = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[prediction_index[0]-1]

			self.history.append(prediction)
			self.scenes_data['main']['drawn_pixels'].clear()

		#Effacer le canvas de dessin sans valider
		elif erase:
			self.scenes_data['main']['drawn_pixels'].clear()

		#Quitter l"interface
		elif quit:
			sys.exit(0)

		###Reset l'ecran / Update l'ecran###
		self.__dessiner_UI(window, data['ui'], selected_button, self.history)

		#Refresh le canvas de dessin.
		for line in self.scenes_data['main']['drawn_pixels']:
			for coords in line:
				window.set_clip(data['ui']["canvas_dessin"]) #Ne pas dessiner en dehors de la case a dessin
				window.blit(self.scenes_data['main']['pencil'], coords)
				window.set_clip(None)

		self._globals['previously_mousedown'] = dessiner


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
			rgb_matrix = pygame.surfarray.pixels3d(window)
			prediction = predictionPipeline.predict(rgb_matrix)
			del rgb_matrix # pygame locks surface unless explicitly deleting reference
			print('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[prediction[0]-1])
			# data = predictionPipeline.predict(rgb_matrix)
			# del rgb_matrix # pygame locks surface unless explicitly deleting reference
			# with open('out.txt', 'w') as f: f.write('\n'.join(' '.join(str(round(num, 1)) for num in line) for line in data))
			# self.scenes_data['view_dataset']['dataset'] = data
			# self.scenes_data['view_dataset']['posligne'] = 0
			# self.__view_dataset(window, events)

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
