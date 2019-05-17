from Algorithms.Bagging import bagging
from Algorithms.ExtraTrees import extra_trees
from Algorithms.LinearKernelSVC import linear_kernel_svc
from Algorithms.Pasting import pasting
from Algorithms.PolynomialKernelSVC import poly_kernel_svc
from Algorithms.RandomForest import random_forest
from Algorithms.RandomPatches import random_patches
from Algorithms.RBFKernelSVC import rbf_kernel_svc
from Algorithms.KNeighbors import k_neighbors

import DataSetOps
from DataFrameOps import load_pickled_data_frame
from Evaluation.crossValidation import cross_validation_report
from sklearn.metrics import confusion_matrix

from ExportModelToTileClassifier import add_model_to_series

CLASSIFIERS = [linear_kernel_svc, poly_kernel_svc, rbf_kernel_svc,
               bagging, extra_trees, pasting, random_forest, random_patches]

# load training set
batch = 'batch_0'
training_batch_df = load_pickled_data_frame(batch)

# todo mirror ignore_label operations to testing_batch_df bellow
# training_batch_df = DataSetOps.ignore_label('5', training_batch_df)

# training_batch_df = DataSetOps.make_label_ratio_equal(training_batch_df)


training_batch_df = DataSetOps.shuffle_data_set(training_batch_df)
train_data, train_labels = training_batch_df.iloc[:, :6], training_batch_df.iloc[:, 6]

'''
print('Training Labels Distribution:', training_batch_df['Labels'].value_counts(), sep='\n')
for clf_constructor in CLASSIFIERS:
    clf = clf_constructor()
    print(clf_constructor.__name__ + '', end=' ')
    # cross validation
    cross_validation_report(clf, train_data, train_labels)
'''

# load testing set
testing_batch_df = load_pickled_data_frame(batch)

# todo mirror ignore_label operations to training_batch_df above
# testing_batch_df = DataSetOps.ignore_label('5', testing_batch_df)
test_data, test_labels = testing_batch_df.iloc[:, :6], testing_batch_df.iloc[:, 6]


print('Testing Labels Distribution:', testing_batch_df['Labels'].value_counts(), sep='\n')
# todo see which clf performs the best then import said clf
# for clf_constructor in CLASSIFIERS:
for clf_constructor in [poly_kernel_svc]:
    clf = clf_constructor()
    clf.fit(train_data, train_labels)
    predictions = clf.predict(test_data)
    print(clf_constructor.__name__ + ':', clf.score(test_data, test_labels))
    print(confusion_matrix(test_labels, predictions))
    # todo change to series to port to
    add_model_to_series('test_dif', clf)

