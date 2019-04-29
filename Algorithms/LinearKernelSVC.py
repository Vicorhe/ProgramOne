from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def linear_kernel_svc():
    # linear kernel support vector classifier
    kernel = 'linear'
    C = 1
    shrinking = True
    tol = 1e-3
    max_iter = -1
    linear_kernel_SVC = Pipeline([
        ('linear_kernel_svc', SVC(kernel=kernel, C=C, shrinking=shrinking,
                                  tol=tol, max_iter=max_iter))
    ])
    #   C = 0.001, 0.01, 0.1, 1, 10, 100
    #   shrinking = True, False
    #   tol = 1e-2, 1e-3, 1e-4
    #   max_iter = -1, 1000, 2000, 3000, 4000

    return linear_kernel_SVC
