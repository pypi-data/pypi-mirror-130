from .diff import variable, value, derivative
from .math import numpy as np

def newton(f, x0, tol=1e-5, maxiter=50):
    """ Newton's root finding algorithm for single variable functions

    :param f: function of a single variable x
    :type f: function (callable)
    :param x0: initial starting point estimate
    :type x0: float or int
    :param tol: root tolerance, defaults to 1e-5
    :type tol: float, optional
    :param maxiter: maximium number of iterations, defaults to 50
    :type maxiter: int, optional
    :return: root of f
    :rtype: float
    """
    xn = variable(x0)
    count = 0
    while np.abs(value(xn)) > tol and count<maxiter:
        func = f(xn)
        grad = derivative(func, xn)
        xn = xn - value(func/grad)
        count += 1
    return value(xn)
