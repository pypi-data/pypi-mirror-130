from autodiff_107.diff.Node import Node
from autodiff_107.diff import variable
from autodiff_107.diff import numpy
from autodiff_107.diff import numpy as np
import pytest

# Testing logarithm

def test_logarithm():
	x=Node(10)
	y=np.log(x)
	assert y._value==np.log(10)
	assert y._d[x]==1/10

test_logarithm()


###############################
### Trigonometric functions ###
###############################

# Testing cos

def test_cos():
	x=Node(10)
	y=np.cos(x)
	assert y._value==np.cos(10)
	assert y._d[x]==-np.sin(10)

test_cos()

# Testing sin

def test_sin():
	x=Node(10)
	y=np.sin(x)
	assert y._value==np.sin(10)
	assert y._d[x]==np.cos(10)

test_sin()

# Testing tan

def test_tan():
	x=Node(10)
	y=np.tan(x)
	assert y._value==np.tan(10)
	assert y._d[x]==1/(np.cos(10))**2

test_tan()


# Testing arccos
# The domain is [-1,1]

def test_arccos():
	x=Node(.1)
	y=np.arccos(x)
	assert y._value==np.arccos(.1)
	assert y._d[x]==-1/np.sqrt(1-.1**2)

test_arccos()

# Testing arcsin
# The domain is [-1,1]

def test_arcsin():
	x=Node(.1)
	y=np.arcsin(x)
	assert y._value==np.arcsin(.1)
	assert y._d[x]==1/np.sqrt(1-.1**2)

test_arcsin()

# Testing arctan
# The domain is R

def test_arctan():
	x=Node(10)
	y=np.arctan(x)
	assert y._value==np.arctan(10)
	assert y._d[x]==1/(1+10**2)

test_arctan()

# Testing cosh

def test_cosh():
	x=Node(10)
	y=np.cosh(x)
	assert y._value==np.cosh(10)
	assert y._d[x]==np.sinh(10)

test_cosh()

# Testing sinh

def test_sinh():
	x=Node(10)
	y=np.sinh(x)
	assert y._value==np.sinh(10)
	assert y._d[x]==np.cosh(10)

test_sinh()

# Testing tanh

def test_tanh():
	x=Node(10)
	y=np.tanh(x)
	assert y._value==np.tanh(10)
	assert y._d[x]==1-(np.tanh(10))**2

test_tanh()

# Testing arccosh
# The domain is [1,+∞)

def test_arccosh():
	x=Node(1.1)
	y=np.arccosh(x)
	assert y._value==np.arccosh(1.1)
	assert y._d[x]==1/np.sqrt(1.1**2-1)

test_arccosh()

# Testing arcsinh
# The domain is R


def test_arcsinh():
	x=Node(1)
	y=np.arcsinh(x)
	assert y._value==np.arcsinh(1)
	assert y._d[x]==1/np.sqrt(1**2+1)

test_arcsinh()

# Testing arctanh
# The domain is (-1,1)

def test_arctanh_1():
	x=Node(.1)
	y=np.arctanh(x)
	assert y._value==np.arctanh(.1)
	assert y._d[x]==1/(1-.1**2)

test_arctanh_1()

def test_arctanh_2():
	x=Node(.2)
	y=np.arctanh(x)
	assert y._value==np.arctanh(.2)
	assert y._d[x]==1/(1-.2**2)

test_arctanh_2()

# Testing exp

def test_exp():
	x=Node(.2)
	y=np.exp(x)
	assert y._value==np.exp(.2)
	assert y._d[x]==np.exp(.2)

test_exp()

# Testing backward:

def test_backward_1():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	w._backward()
	# Ie what do z._df and x._df represent?
	# I think they are meant to represent the derivative of w wrt to z and z,
	# respectively, but I don't like the way it looks cause we don't have reference
	# to w.
	# Would be better to have something like w._df[z] and w._df[x]
	assert z._df==np.exp(3*2)
	assert x._df==3*np.exp(3*2)

test_backward_1()

def test_backward_2():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	f._backward()
	assert w._df==-np.sin(np.exp(3*2))
	assert z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
	assert x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3

test_backward_2()

def test_backward_3():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	w._backward()
	# Now, we have z._df and x._df different from the ones
	# in test_backward_2()
	# But what we really want are derivates of w wrt to z, x (here)
	# and derivatives of f wrt to z,x (in test_backward_2)
	assert z._df==np.exp(3*2)
	assert x._df==np.exp(3*2)*3

test_backward_3()


# Test clear derivative

def test_clear_derivative():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	f._backward()
	assert w._df==-np.sin(np.exp(3*2))
	assert z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
	assert x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3
	f._clear_df()
	assert w._df==0
	assert z._df==0
	assert x._df==0


test_clear_derivative()


# Test clear derivative

def test_clear_derivative():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	f._backward()
	assert w._df==-np.sin(np.exp(3*2))
	assert z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
	assert x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3
	f._clear_df()
	assert w._df==0
	assert z._df==0
	assert x._df==0
	w._backward()
	assert z._df==np.exp(3*2)
	assert x._df==3*np.exp(3*2)

test_clear_derivative()

def test_clear_derivative_2():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	f._backward()
	assert w._df==-np.sin(np.exp(3*2))
	assert z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
	assert x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3
	# f._clear_df()
	# assert w._df==0
	# assert z._df==0
	# assert x._df==0
	w._backward()
	assert z._df!=np.exp(3*2)
	assert x._df!=3*np.exp(3*2)

test_clear_derivative_2()

# Testing variable function

def test_variable_1():
	x=variable([1,2])
	assert x[0]._value==1
	assert x[1]._value==2

test_variable_1()

def test_variable_2():
	x=variable([[1,2],[3,4]])
	assert x[0,0]._value==1
	assert x[0,1]._value==2
	assert x[1,0]._value==3
	assert x[1,1]._value==4

test_variable_2()

# Testing derivatives


def test_derivative_1():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._derivative(z)==np.exp(3*2)
	assert w._derivative(x)==3*np.exp(3*2)

test_derivative_1()

def test_derivative_2():
	x=Node(2)
	y=3
	z=y*x
	assert z._value==3*2
	assert z._d[x]==3
	w=np.exp(z)
	assert w._value==np.exp(3*2)
	assert w._d[z]==np.exp(3*2)
	f=np.cos(w)
	assert f._value==np.cos(np.exp(3*2))
	assert f._d[w]==-np.sin(np.exp(3*2))
	f._backward()
	assert w._df==-np.sin(np.exp(3*2))
	assert z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
	assert x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3
	# f._clear_df()
	# assert w._df==0
	# assert z._df==0
	# assert x._df==0
	w._backward()
	assert z._df!=np.exp(3*2)
	assert x._df!=3*np.exp(3*2)
	assert w._derivative(z)==np.exp(3*2)
	assert w._derivative(x)==3*np.exp(3*2)


test_derivative_2()

# Forward mode with cos

def test_forward_mode_7():
    x = Node(3, fm_seed = 1/2)
    y = Node(2, fm_seed=1/2)
    f = np.cos(x*y)
    assert f._fmd == -(1+3/2)*np.sin(6)

test_forward_mode_7()
