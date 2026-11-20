import joblib
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from constants import DATASET_PATH, TRAINED_MODEL_PATH
from model.datasetManager import DatasetManager


def train() -> None:
	print('Loading dataset...')
	dataset, indices = DatasetManager(DATASET_PATH).fetch()

	print('Splitting dataset...')
	X_train, X_test, y_train, y_test = train_test_split(
	    dataset, indices, test_size=0.2,
	    stratify=indices, random_state=0, shuffle=True
	)

	print('Training dummy...')
	dclf = DummyClassifier(random_state=0)
	dclf.fit(X_train, y_train)
	print('Dummy accuracy:', dclf.score(X_test, y_test))

	print('Training model...')
	mlp = MLPClassifier(
	    hidden_layer_sizes=(768, 384),
	    activation='tanh',
	    solver='adam',
	    max_iter=500,
	    early_stopping=True, # Prevents overfitting
	    random_state=0,
	    shuffle=True,
	)
	mlp.fit(X_train, y_train)
	print('Model accuracy:', mlp.score(X_test, y_test))

	joblib.dump(mlp, TRAINED_MODEL_PATH)
	print('Model saved successfully!')

	print('Plotting confusion matrix...')
	y_pred = mlp.predict(X_test)
	cm = confusion_matrix(y_test, y_pred)
	disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	disp.plot(cmap='Blues')
	plt.title('MLPClassifier Confusion Matrix')
	plt.show()
