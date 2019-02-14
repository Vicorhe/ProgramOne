import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC
from Miscellaneous.imageAcquisition import get_data_set
from FeatureExtraction.moments import get_statistics
# from FeatureExtraction.meanVarSkew import get_statistics
# from FeatureExtraction.meanVarMedianMode import get_statistics
# from FeatureExtraction.meanVarMode import get_statistics
# from FeatureExtraction.meanVarStd import get_statistics
# from FeatureExtraction.meanVarMedian import get_statistics
# from FeatureExtraction.meanVar import get_statistics
# from FeatureExtraction.meanStd import get_statistics
from Utilities.utils import unison_shuffled_copies


# fetch the raw training and testing images, and respective labels
training_images, testing_images, y_train, y_test, channels = get_data_set()

# gather features
X_train = np.vstack([get_statistics(img, channels) for img, _ in training_images])
X_test = np.vstack([get_statistics(img, channels) for img, _ in testing_images])
X_train, y_train = unison_shuffled_copies(X_train, y_train)

# linear SVM Classification
poly_kernel_svm_clf = Pipeline([
    ('scaler', StandardScaler()),
    ('svm_clf', SVC(kernel='poly', degree=3, coef0=1, C=5))
])

poly_kernel_svm_clf.fit(X_train, y_train)

print(poly_kernel_svm_clf.score(X_test, y_test))
