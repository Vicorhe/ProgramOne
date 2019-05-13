from Algorithms.AdaBoost import ada
from Algorithms.Bagging import bagging
from Algorithms.DecisionTree import decision_tree
from Algorithms.ExtraTrees import extra_trees
from Algorithms.GradientBoost import gradient_boost
from Algorithms.KNeighbors import k_neighbors
from Algorithms.LinearKernelSVC import linear_kernel_svc
from Algorithms.Pasting import pasting
from Algorithms.PolynomialKernelSVC import poly_kernel_svc
from Algorithms.RandomForest import random_forest
from Algorithms.RandomPatches import random_patches
from Algorithms.RandomSubspaces import random_subspaces
from Algorithms.RBFKernelSVC import rbf_kernel_svc
# from treat_as_two import process_data
# from treat_as_two_all_batches import process_data
# from SpecialLabelProcessing.ignore_ws import process_data
# from ignore_ws_all_batches import process_data
from FetchDataSet import load_tile_data_set
from ExtractFeaturesIntoDataFrame import load_pickled_data_frame
from Evaluation.crossValidation import cross_validation_report
from sklearn.metrics import confusion_matrix
import pandas as pd


CLASSIFIERS = [linear_kernel_svc, poly_kernel_svc, rbf_kernel_svc,
               bagging, extra_trees, pasting, random_forest, random_patches]

# load data set

batch = 'batch_c'
batch_df = load_pickled_data_frame(batch)

ones_df = batch_df.loc[batch_df['Labels'] == '1']
twos_df = batch_df.loc[batch_df['Labels'] == '2']
sample_size = min(len(ones_df), len(twos_df))
df_s = [ones_df[:sample_size], twos_df[:sample_size]]
new_df = pd.concat(df_s, ignore_index=True)

new_df = new_df.sample(frac=1).reset_index(drop=True)
train_data, train_labels = new_df.iloc[:, :6], new_df.iloc[:, 6]


print(new_df['Labels'].value_counts())
# get classifier
for clf_constructor in CLASSIFIERS:
    clf = clf_constructor()
    print(clf_constructor.__name__ + '', end=' ')
    # cross validation
    cross_validation_report(clf, train_data, train_labels)

for clf_constructor in CLASSIFIERS:
    clf = clf_constructor()
    clf.fit(train_data, train_labels)
    predictions = clf.predict(train_data)
    print(clf_constructor.__name__ + ':', clf.score(train_data, train_labels))
    print(confusion_matrix(train_labels, predictions))
