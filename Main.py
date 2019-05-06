from Algorithms.AdaBoost import ada
from Algorithms.Bagging import bagging
from Algorithms.DecisionTree import decision_tree
from Algorithms.ExtraTrees import extra_trees
from Algorithms.GradientBoost import gradient_boost
from Algorithms.KNeighbors import k_neighbors
from Algorithms.LinearKernelSVC import linear_kernel_svc
from Algorithms.LinearSVC import linear_svc
from Algorithms.LogisticSGD import logistic_sgd
from Algorithms.Pasting import pasting
from Algorithms.PolynomialKernelSVC import poly_kernel_svc
from Algorithms.RandomForest import random_forest
from Algorithms.RandomPatches import random_patches
from Algorithms.RandomSubspaces import random_subspaces
from Algorithms.RBFKernelSVC import rbf_kernel_svc
# from treat_as_two import process_data
# from treat_as_two_all_batches import process_data
# from ignore_ws import process_data
from ignore_ws_all_batches import process_data
from Evaluation.crossValidation import cross_validation_report


CLASSIFIERS = [ada, bagging, decision_tree, extra_trees, gradient_boost, k_neighbors,
               linear_kernel_svc, linear_svc, logistic_sgd, pasting, poly_kernel_svc,
               random_forest, random_patches, random_subspaces, rbf_kernel_svc
]


# load data set
train_data, train_labels = process_data()

# get classifier
for clf_constructor in CLASSIFIERS:
    clf = clf_constructor()

    print(clf_constructor.__name__ + ':', end=' ')

    # cross validation
    cross_validation_report(clf, train_data, train_labels)
