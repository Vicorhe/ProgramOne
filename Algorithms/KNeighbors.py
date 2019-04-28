from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier


def get_classifier():
    # k nearest neighbors classifier
    n_neighbors = 3
    weights = 'uniform'

    k_nearest_neighbors_clf = Pipeline([
        ('k_nearest_neighbors_clf', KNeighborsClassifier(n_neighbors=n_neighbors,
                                                         weights=weights))
    ])
    #   n_neighbors: 3, 5, 7, 9, 11
    #   weights: 'uniform', 'distance'

    return k_nearest_neighbors_clf
