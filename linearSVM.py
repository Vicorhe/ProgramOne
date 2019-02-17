import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import LinearSVC, SVC
from Miscellaneous.imageAcquisition import get_data_set
from FeatureExtraction.feature_set_b import get_statistics
#from FeatureExtraction.meanVar import get_statistics
from Utilities.utils import unison_shuffled_copies


# fetch the raw training and testing images, and respective labels
training_images, testing_images, y_train, y_test, channels = get_data_set()

# gather features
X_train = np.vstack([get_statistics(img, channels) for img, _ in training_images])
X_test = np.vstack([get_statistics(img, channels) for img, _ in testing_images])
X_train, y_train = unison_shuffled_copies(X_train, y_train)

# linear SVM Classification
svm_clf = Pipeline([
    ('linear_svc', SVC(kernel='linear', C=0.1, gamma='scale'))
])
#   ('linear_svc', LinearSVC(C=0.1, loss="hinge"))
#   ('scaler', StandardScaler()),
svm_clf.fit(X_train, y_train)

print("training score: %f" % (svm_clf.score(X_train, y_train)))
print("testing score: %f" % (svm_clf.score(X_test, y_test)))
