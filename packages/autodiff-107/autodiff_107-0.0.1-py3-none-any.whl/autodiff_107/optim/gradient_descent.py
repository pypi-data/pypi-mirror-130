from autodiff_107.diff import numpy as np
from autodiff_107.diff import Node

def gradient_descent(f, x0, alpha, tol, max_iter):
    '''
    f is the function to optimize
    assume that the funciton is from Euclidean space of dim 1 to Eucl. sp. of dim 1
    x0 is the starting point
    tol is the tolerance
    '''
    xn = Node(x0)
    xprev=Node(1000)

    count=0

    while np.abs(xn._value-xprev._value) > 1/5*tol and count<max_iter:
        xprev=xn
        f_eval = f(xn)
        df_eval = f_eval._derivative(xn)
        xn = xn-alpha*df_eval
        count+=1

    if count==max_iter:
        print("Reached the maximum number of iterations")

    return xn._value
