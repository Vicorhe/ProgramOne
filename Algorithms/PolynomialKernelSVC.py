from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


def get_classifier():
    # polynomial kernel support vector classifier
    kernel = 'poly'
    C = 1
    degree = 3
    gamma = 'scale'
    coef0 = 0.0
    shrinking = True
    tol = 1e-3
    max_iter = -1
    polynomial_kernel_SVC = Pipeline([
        ('polynomial_kernel_svc', SVC(kernel=kernel, C=C, degree=degree,
                                      gamma=gamma, coef0=coef0,
                                      shrinking=shrinking, tol=tol,
                                      max_iter=max_iter))
    ])
    #   C = 0.001, 0.01, 0.1, 1, 10, 100
    #   degree = 2, 3, 4, 5
    #   gamma = 'scale', 'auto'
    #   coef0 = 0.0, 0.5, 1.0, 2.0
    #   shrinking = True, False
    #   tol = 1e-2, 1e-3, 1e-4
    #   max_iter = -1, 1000, 2000, 3000, 4000

    return polynomial_kernel_SVC
