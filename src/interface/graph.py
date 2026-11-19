import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pygame


def create_best_predictions_graph(predictions: list[tuple[str, float]], rect: pygame.Rect) -> pygame.Surface:
	x = [p[0] for p in predictions[:5]]
	y = [p[1] for p in predictions[:5]]

	# plot into matplotlib and set labels
	dpi = 100
	fig, _ = plt.subplots(figsize=(rect.width/dpi, rect.height/dpi), dpi=100)
	plt.bar(x, y, log=True)
	plt.subplots_adjust(left=0.25, bottom=0.15)
	plt.xlabel("Lettres")
	plt.ylabel("Probabilitité (%)")
	plt.title("Estimation des lettres")

	# extract raw data from the graph
	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	raw_data = canvas.get_renderer().buffer_rgba()
	size = canvas.get_width_height()

	# convert raw data onto a pygame surface
	graph_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
	return graph_surface
