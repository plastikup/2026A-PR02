import os

import joblib
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from constants import TRAINED_MODEL_PATH
from model.datasetManager import DatasetManager


def train() -> None:
    print('Loading dataset...')
    datasetPath = os.path.join('data', 'dataset.csv')
    dataset, indices = DatasetManager(datasetPath).fetch()

    print('Splitting dataset...')
    X_train, X_test, y_train, y_test = train_test_split(
        dataset, indices, test_size=0.2,
        stratify=indices, random_state=42, shuffle=True
    )

    print('Training model...')
    clf = MLPClassifier(
        hidden_layer_sizes=(512, 256),
        activation='relu',
        solver='adam',
        max_iter=500,
        early_stopping=True, # Prevents overfitting
        random_state=42
    )
    clf.fit(X_train, y_train)

    print('Accuracy:', clf.score(X_test, y_test))

    joblib.dump(clf, TRAINED_MODEL_PATH)
    print('Model saved successfully!')
