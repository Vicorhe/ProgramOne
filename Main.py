import shelve
from sklearn.metrics import confusion_matrix

import DataSetOps
from Algorithms.Bagging import bagging
from Algorithms.ExtraTrees import extra_trees
from Algorithms.LinearKernelSVC import linear_kernel_svc
from Algorithms.Pasting import pasting
from Algorithms.PolynomialKernelSVC import poly_kernel_svc
from Algorithms.RandomForest import random_forest, random_forest_grid_search
from Algorithms.RandomPatches import random_patches

from Algorithms.svc import svc

from DataFrameOps import load_pickled_data_frame


CLASSIFIERS = [linear_kernel_svc, poly_kernel_svc,
               random_forest, random_patches, extra_trees, bagging, pasting]


def add_model_to_series(series, model):
    tiles_db_path = 'tiles'
    with shelve.open(tiles_db_path) as db:
        num_shades = db[series]['num_shades']
        batch_number = db[series]['batch_number']
        db[series] = {
            'num_shades': num_shades,
            'batch_number': batch_number,
            'model': model
        }


# load data sets
batch = 'batch_0'
training_batch_df, testing_batch_df = load_pickled_data_frame(batch), load_pickled_data_frame(batch)


# training set operations
# todo mirror ignore_label operations to testing_batch_df bellow
# training_batch_df = DataSetOps.ignore_label('5', training_batch_df)


# training_batch_df = DataSetOps.make_label_ratio_equal(training_batch_df)


training_batch_df = DataSetOps.shuffle_data_set(training_batch_df)
train_data, train_labels = training_batch_df.iloc[:, :6], training_batch_df.iloc[:, 6]


# grid_search_clf = svc() # random_forest_grid_search()
# grid_search_clf.fit(train_data, train_labels)
# print(grid_search_clf.best_params_)
# print(grid_search_clf.best_estimator_.score(train_data, train_labels))


'''
for clf_constructor in CLASSIFIERS:
    clf = clf_constructor()
    print(clf_constructor.__name__ + '', end=' ')
    # cross validation
    cross_validation_report(clf, train_data, train_labels)
'''

# testing set operations
# todo mirror ignore_label operations to training_batch_df above
# testing_batch_df = DataSetOps.ignore_label('5', testing_batch_df)

DataSetOps.print_labels_distribution(testing_batch_df)
testing_batch_df = DataSetOps.shuffle_data_set(testing_batch_df)
test_data, test_labels = testing_batch_df.iloc[:, :6], testing_batch_df.iloc[:, 6]

# todo see which clf performs the best then import said clf
# for clf_constructor in CLASSIFIERS:
for clf_constructor in [linear_kernel_svc]:
    clf = clf_constructor()
    clf.fit(train_data, train_labels)
    predictions = clf.predict(test_data)
    print(clf_constructor.__name__ + ':', clf.score(test_data, test_labels))
    print(confusion_matrix(test_labels, predictions))
    # todo change series to port here
    add_model_to_series(series='newSeries', model=clf)

