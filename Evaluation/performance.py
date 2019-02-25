from numpy import array2string
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


CENTER_TEXT = '{:^38s}'
TABLE_HEADER = '{:>24s}{:>14s}'
TABLE_ROW = '{:>10s}{:>14.3f}{:>14.3f}'
TABLE_BORDER = '-' * 38

TITLE = 'PERFORMANCE REPORT'
CONFUSION = 'CONFUSION MATRIX'
MACRO = 'macro avg'
MICRO = 'micro avg'
PRECISION = 'precision'
RECALL = 'recall'
F1 = 'f1-score'
TRAINING = 'training set'
TESTING = 'testing set'
ACCURACY = 'accuracy'


# USE CASE
###################################################################
# train_predict = k_nearest_neighbors_clf.predict(X_train)        #
# test_predict = k_nearest_neighbors_clf.predict(X_test)          #
#                                                                 #
# performance_report(y_train, train_predict, y_test, test_predict)#
###################################################################
def performance_report(training_truth, training_prediction,
                       testing_truth, testing_prediction):

    training_set_accuracy = accuracy_score(training_truth, training_prediction)
    testing_set_accuracy = accuracy_score(testing_truth, testing_prediction)

    c_r = classification_report(testing_truth, testing_prediction, output_dict=True)

    precision_micro = c_r[MICRO][PRECISION]
    recall_micro = c_r[MICRO][RECALL]
    f1_micro = c_r[MICRO][F1]

    precision_macro = c_r[MACRO][PRECISION]
    recall_macro = c_r[MACRO][RECALL]
    f1_macro = c_r[MACRO][F1]

    print(TABLE_BORDER)
    print(CENTER_TEXT.format(TITLE))
    print(TABLE_BORDER)

    print(TABLE_HEADER.format(MICRO, MACRO))
    print(TABLE_BORDER)
    print(TABLE_ROW.format(PRECISION, precision_micro, precision_macro))
    print(TABLE_ROW.format(RECALL, recall_micro, recall_macro))
    print(TABLE_ROW.format(F1, f1_micro, f1_macro))

    print(TABLE_BORDER)

    print(TABLE_HEADER.format(TRAINING, TESTING))
    print(TABLE_BORDER)
    print(TABLE_ROW.format(ACCURACY, training_set_accuracy, testing_set_accuracy))

    print(TABLE_BORDER)
    print(CENTER_TEXT.format(CONFUSION))
    print(TABLE_BORDER)

    for row in confusion_matrix(testing_truth, testing_prediction):
        print(CENTER_TEXT.format(array2string(row)))
        
    print(TABLE_BORDER)
