import pygame

from interface.scenes import Scenes


def ui() -> None:
	# Initialize pygame
	pygame.init()
	window = pygame.display.set_mode((1024, 1024), pygame.SCALED | pygame.RESIZABLE | pygame.SRCALPHA)
	window.fill((255, 255, 255, 255))
	clock = pygame.time.Clock()

	# Setup the scenes manager
	scenes = Scenes()
	# for testing purposes only
	#scenes.active_scene = 'sandbox'
	# scenes.active_scene = 'view_dataset'
	scenes.active_scene = "main"

	# Main loop
	while True:
		#* compile all events
		events = pygame.event.get()

		#* update screen
		scenes.refresh_animation_frame(window, events)
		pygame.display.flip()
		clock.tick(180)

		#* exit if applicable
		if pygame.QUIT in tuple(e.type for e in events): break

	# exit
	pygame.display.quit()
	pygame.quit()
