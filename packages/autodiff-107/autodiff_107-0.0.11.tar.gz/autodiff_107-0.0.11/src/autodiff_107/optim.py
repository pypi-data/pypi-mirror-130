from numpy.core.defchararray import center
from .diff import variable, derivative, value
from .math import numpy as np

def gradient_descent(f, x0, lr=0.1, max_iter=1000):
    """Simple gradient descent
    
    :param f: function to minimize
    :type f: function (callable)
    :param x0: initial starting point for gradient descent, if x0 is too far from the minimum, algorithm might not converge
    :type x0: list or np.array w/ dtype float or int
    :param lr: learning rate, default to 0.1
    :type lr: float
    :param max_iter: number of iterations to run gradient descent, default to 1000
    :type max_iter: int
    :return: function minimum after `max_iter` steps
    :rtype: np.array
    """
    xn = variable(x0)
    for i in range(max_iter):
        func = f(xn)
        grad = derivative(func, xn)
        xn = xn-lr*grad

    return value(xn)

def adagrad(f, x0, lr=0.1, lr_decay=0., weight_decay=0., eps=1e-10, max_iter=1000):
    """ Adagrad algorithm: Adaptive Subgradient Methods for Online Learning and Stochastic Optimization.

    :param f: objective function to minimize
    :type f: function (callable)
    :param x0: initial parameters
    :type x0: list or np.array w/ dtype float or int
    :param lr: learning rate, defaults to 0.1
    :type lr: float, optional
    :param lr_decay: learning rate decay, defaults to 0.
    :type lr_decay: float, optional
    :param weight_decay: weight decay (L2 penalty), defaults to 0.
    :type weight_decay: float, optional
    :param eps: term added to the denominator to improve numerical stability, defaults to 1e-10
    :type eps: float, optional
    :param max_iter: maximum number of iterations, defaults to 1000
    :type max_iter: int, optional

    :return: function minimum after `max_iter` steps
    :rtype: np.array
    """
    xn = variable(x0)
    count = 0
    state_sum = 0
    for i in range(max_iter):
        fi = f(xn)
        gi = derivative(fi, xn)
        gamma = lr/(1+(1+i)*lr_decay)
        if weight_decay != 0:
            gi += weight_decay*xn
        state_sum += gi**2
        xn -= gamma*gi/(np.sqrt(state_sum)+eps)
    return value(xn)
