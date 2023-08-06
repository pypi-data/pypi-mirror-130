from autodiff_107.diff.Node import Node
from autodiff_107.optim import gradient_descent
from autodiff_107.diff import numpy as np
import pytest


def test_gradient_descent_1():
	# find min of (x-3)**2+3, which occurs at 3 with value 3
	x0 = 1
	f = lambda x: (x-3)**2+1
	tol = 1e-3
	alpha=.9
	max_iter=20000
	mini = gradient_descent(f, x0,alpha, tol, max_iter)
	#print("The minimum is achieved at {} with function value {}".format(mini, f(mini)))
	assert np.abs(mini-3)<tol

test_gradient_descent_1()

