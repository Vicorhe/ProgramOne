from sklearn.metrics import accuracy_score, classification_report
from sklearn.base import clone


CENTER_TEXT = '{:^24s}'
TABLE_HEADER = '{:>24s}'
TABLE_ROW = '{:>10s}{:>14.3f}'
TABLE_BORDER = '-' * 24
TABLE_OUTER_BORDER = '*' * 24

TITLE = 'PERFORMANCE REPORT'
MACRO = 'macro avg'
PRECISION = 'precision'
RECALL = 'recall'
TRAINING = 'training'
TESTING = 'testing'
ACCURACY = 'accuracy'


def print_report(precision_macro, recall_macro, testing_set_accuracy, training_set_accuracy):
    print(TABLE_OUTER_BORDER)
    print(CENTER_TEXT.format(TITLE))
    print(TABLE_BORDER)
    print(TABLE_HEADER.format(MACRO))
    print(TABLE_BORDER)
    print(TABLE_ROW.format(PRECISION, precision_macro))
    print(TABLE_ROW.format(RECALL, recall_macro))
    print(TABLE_BORDER)
    print(TABLE_HEADER.format(ACCURACY))
    print(TABLE_BORDER)
    print(TABLE_ROW.format(TESTING, testing_set_accuracy))
    print(TABLE_ROW.format(TRAINING, training_set_accuracy))
    print(TABLE_OUTER_BORDER)


def performance_report(clf, train_feature_sets, train_labels,
                       test_feature_sets, test_labels):

    for train_feature_set, test_feature_set in zip(train_feature_sets,
                                                   test_feature_sets):
        clone_clf = clone(clf)
        clone_clf.fit(train_feature_set, train_labels)
        test_predict = clone_clf.predict(test_feature_set)
        train_predict = clone_clf.predict(train_feature_set)

        c_r = classification_report(test_labels, test_predict, output_dict=True)
        precision_macro = c_r[MACRO][PRECISION]
        recall_macro = c_r[MACRO][RECALL]
        training_set_accuracy = accuracy_score(train_labels, train_predict)
        testing_set_accuracy = accuracy_score(test_labels, test_predict)

        print_report(precision_macro, recall_macro, testing_set_accuracy, training_set_accuracy)
