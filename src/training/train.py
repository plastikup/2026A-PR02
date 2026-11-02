import os

from sklearn import svm
from sklearn.utils.validation import joblib

from training.datasetManager import DatasetManager


def train() -> None:
	print('Loading dataset...')
	datasetPath = os.path.join('data', 'dataset.csv')
	dataset, indices = DatasetManager(datasetPath).fetch()

	print('Training model...')
	clf = svm.SVC()
	clf.fit(dataset, indices)

	joblib.dump(clf, os.path.join('out', 'trained_model.pkl'))
	print('Model saved successfully!')
