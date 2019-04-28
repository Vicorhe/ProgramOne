from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def get_classifier():
    # rbf kernel support vector classifier
    kernel = 'rbf'
    C = 1
    gamma = 'scale'
    shrinking = True
    tol = 1e-3
    max_iter = -1
    rbf_kernel_SVC = Pipeline([
        ('rbf_kernel_svc', SVC(kernel=kernel, C=C, gamma=gamma, shrinking=shrinking,
                               tol=tol, max_iter=max_iter))
    ])
    #   C = 0.001, 0.01, 0.1, 1, 10, 100
    #   gamma = 'scale', 'auto'
    #   shrinking = True, False
    #   tol = 1e-2, 1e-3, 1e-4
    #   max_iter = -1, 1000, 2000, 3000, 4000

    return rbf_kernel_SVC
