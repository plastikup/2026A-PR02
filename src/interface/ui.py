import pygame

from interface.scenes import Scenes


def ui() -> None:
	# Initialize pygame
	pygame.init()
	window = pygame.display.set_mode((768, 768))
	clock = pygame.time.Clock()

	# Setup the scenes manager
	scenes = Scenes()
	scenes.active_scene = 'view_dataset' # for testing purposes only, other test is: view_dataset

	# Main loop
	while True:
		#* compile all events
		events = pygame.event.get()

		#* update screen
		scenes.refresh_animation_frame(window, events)
		pygame.display.flip()
		clock.tick(30)

		#* exit if applicable
		if pygame.QUIT in tuple(e.type for e in events): break

	# exit
	pygame.display.quit()
	pygame.quit()
