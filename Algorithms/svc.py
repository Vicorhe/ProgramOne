from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# {'kernel': ['linear'], 'C': [0.01, 0.1, 1, 10, 100], 'shrinking':[True, False]},
# [2, 3, 4, 5]
param_grid = [
    {'kernel': ['poly'], 'C': [1, 100], 'gamma':['scale', 'auto'], 'degree':[2, 3]}
]


def svc():
    svc = SVC()
    grid_search = GridSearchCV(svc, param_grid, cv=3, scoring='balanced_accuracy')
    return grid_search

