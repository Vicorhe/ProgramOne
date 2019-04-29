from Algorithms.AdaBoost import get_classifier
from Algorithms.Bagging import get_classifier
from Algorithms.DecisionTree import get_classifier
from Algorithms.ExtraTrees import get_classifier
from Algorithms.GradientBoost import get_classifier
from Algorithms.KNeighbors import get_classifier
from Algorithms.LinearKernelSVC import get_classifier
from Algorithms.LinearSVC import get_classifier
from Algorithms.LogisticSGD import get_classifier
from Algorithms.Pasting import get_classifier
from Algorithms.PolynomialKernelSVC import get_classifier
from Algorithms.RandomForest import get_classifier
from Algorithms.RandomPatches import get_classifier
from Algorithms.RandomSubspaces import get_classifier
from Algorithms.RBFKernelSVC import get_classifier
from FetchDataSet import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()

# get classifier
for name, clf_constructor in clf_constructors:
    clf = clf_constructor()

    print(name + ':')

    # cross validation
    cross_validation_report(clf, train_data, train_labels)
