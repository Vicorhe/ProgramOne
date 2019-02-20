import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.ensemble import RandomForestClassifier
from Miscellaneous.imageAcquisition import get_data_set
from FeatureExtraction.feature_set_b import get_statistics, get_feature_names
# from FeatureExtraction.feature_set_a import get_statistics, get_feature_names
from Utilities.utils import unison_shuffled_copies


# fetch the raw training and testing images, and respective labels
training_images, testing_images, y_train, y_test, channels = get_data_set()

# gather features
X_train = np.vstack([get_statistics(img, channels) for img, _ in training_images])
X_test = np.vstack([get_statistics(img, channels) for img, _ in testing_images])
X_train, y_train = unison_shuffled_copies(X_train, y_train)

# avoid data copy
assert X_train.flags['C_CONTIGUOUS']
assert X_test.flags['C_CONTIGUOUS']
assert y_train.flags['C_CONTIGUOUS']
assert y_test.flags['C_CONTIGUOUS']

# random forest ensemble classifier

n_estimators = 500
max_leaf_nodes = 16
n_jobs = -1

random_forest_clf = RandomForestClassifier(n_estimators=n_estimators,
                                           max_leaf_nodes=max_leaf_nodes,
                                           n_jobs=n_jobs)

random_forest_clf.fit(X_train, y_train)

print("training score: %f" % (random_forest_clf.score(X_train, y_train)))
print("testing score: %f" % (random_forest_clf.score(X_test, y_test)))

for name, score in zip(get_feature_names(), random_forest_clf.feature_importances_):
    print(name, score)
