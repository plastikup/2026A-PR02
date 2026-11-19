import os
from collections import Counter

import matplotlib.pyplot as plt

from constants import DATASET_PATH
from model.datasetManager import DatasetManager


def generate_exploration_graph():
	_, indices = DatasetManager(DATASET_PATH).fetch()
	occurrences = Counter(indices).most_common()
	plt.bar(*zip(*occurrences))
	plt.xlabel('Lettres')
	plt.ylabel('Occurrences')
	plt.title("Graphe d'exploration sur l'occurence\nde chacun des lettres dans le jeu de donnée")
	plt.xticks(range(1, 27), labels='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	plt.yticks(range(0, 500, 50))
	plt.savefig(os.path.join('out', 'exploration_graph.png'))
	print('Graph saved yayayay')
