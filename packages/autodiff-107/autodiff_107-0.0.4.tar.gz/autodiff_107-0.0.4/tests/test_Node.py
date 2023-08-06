from autodiff_107.diff.Node import Node
from autodiff_107.diff import numpy as np
import pytest

# Testing that we can instantiate nodes ad int, float that we get the correct derivatives

def test_int():
	x=Node(8)
	assert x._value==8

test_int()

def test_int_2():
	x=Node(-8)
	assert x._value==-8

test_int_2()

def test_float():
	x=Node(9.2)
	assert x._value==9.2

test_float()

def test_float_2():
	x=Node(-9.2)
	assert x._value==-9.2

test_float()

# Testing addition

def test_add_int():
	x=Node(1)
	y=Node(2)
	z=x+y
	assert z._value==3
	assert z._d[x]==1
	assert z._d[y]==1

test_add_int()

def test_add_int_2():
	x=Node(1)
	y=Node(2)
	z=Node(3)
	w=x+y+z
	assert w._value==6
	# Does x+y first
	# assert w._d[x]==1
	# assert w._d[y]==1
	assert w._d[z]==1

test_add_int_2()

def test_add_int_3():
	x=Node(1)
	y=Node(2)
	z=Node(-3)
	w=x+y+z
	assert w._value==0
	assert w._d[z]==1

test_add_int_3()

def test_substract_1():
	x=Node(1)
	y=Node(2)
	w=x-y
	assert w._value==-1
	assert w._d[x]==1
	assert w._d[y]==-1

test_substract_1()

def test_substract_2():
	x=Node(1)
	y=2
	w=x-y
	assert w._value==-1
	assert w._d[x]==1

test_substract_2()

def test_add_float():
	x=Node(1.1)
	y=Node(2.1)
	z=x+y
	assert z._value==3.2
	assert z._d[x]==1
	assert z._d[y]==1

test_add_float()

# def test_add_float_2():
# 	x=Node(1.1)
# 	y=Node(2.1)
# 	z=Node(2.1)
# 	w=x+y+z
# 	print(w._value)
# 	assert w._value==5.3

# test_add_float_2()

def test_add_float_3():
	x=Node(1.1)
	y=Node(2.1)
	z=Node(-0.1)
	w=x+y+z
	assert w._value==3.1
	assert w._d[z]==1

test_add_float_3()

# Testing multiplication

def test_multiplication_1():
	x=Node(1)
	y=2
	z=x*y
	assert z._value==2
	assert z._d[x]==2

test_multiplication_1()

def test_multiplication_2():
	x=Node(4)
	y=2
	z=x*y
	assert z._value==8
	assert z._d[x]==2

test_multiplication_2()

def test_multiplication_3():
	x=Node(6)
	y=Node(2)
	z=x*y
	assert z._value==12
	assert z._d[x]==2
	assert z._d[y]==6

test_multiplication_3()

# Testing division

def test_division_1():
	x=Node(1)
	y=2
	z=x/y
	assert z._value==1/2
	assert z._d[x]==1/2

test_division_1()

def test_division_2():
	x=Node(4)
	y=2
	z=x/y
	assert z._value==2
	assert z._d[x]==1/2

test_division_2()

def test_division_3():
	x=Node(6)
	y=Node(2)
	z=x/y
	assert z._value==3
	assert z._d[x]==1/2
	assert z._d[y]==-6/(2**2)

test_division_3()

# Testing Negation

def test_negation():
	x=Node(1)
	y=-x
	assert y._value==-1
	assert y._d[x]==-1

test_negation()

# Test power

def test_power_1():
	x=Node(2)
	y=x**3
	assert y._value==2**3
	assert y._d[x]==3*(2**2)

test_power_1()

def test_power_2():
	x=Node(2)
	y=x**x
	assert y._value==2**2
	assert y._d[x]==(2**2)*np.log(2)+2**2
test_power_2()

def test_power_3():
	x=Node(2)
	y=Node(3)
	z=x**y
	assert z._value==2**3
	assert z._d[x]==(3)*(2**2)
	assert z._d[y]==np.log(2)*(2**3)
test_power_3()

def test_rpower_1():
	x=Node(2)
	y=3
	z=y**x
	assert z._value==3**2
	assert z._d[x]==np.log(y)*(3**2)
test_rpower_1()

def test_rpower_2():
	x=Node(0)
	y=3
	z=y**x
	assert z._value==1
	assert z._d[x]==np.log(3)
test_rpower_2()


# Test binary operations on same Node
def test_binary_op_repeat_node():
    x = Node(3)
    f = x + x
    assert f._d[x] == 2
    
    f = x * x
    assert f._d[x] == 6

    f = x / x 
    assert f._d[x] == 0

    f = x - x
    assert f._d[x] == 0

test_binary_op_repeat_node()

def test_forward_mode_basic():
    x = Node(3, fm_seed = 1)
    y = Node(7)
    z = Node(5)
    f = (x * y) + (2 * x) / x + z / z
    assert f._fmd == 7

test_forward_mode_basic()

def test_forward_mode_2():
    x = Node(3, fm_seed = 1)
    y = Node(7)
    f = x-y
    assert f._fmd == 1

test_forward_mode_2()

def test_forward_mode_3():
    x = Node(3)
    y = Node(7, fm_seed=1)
    f = x-y
    assert f._fmd == -1

test_forward_mode_3()

def test_forward_mode_4():
    x = Node(3, fm_seed=1/2)
    y = Node(7, fm_seed=1/2)
    f = x-y
    assert f._fmd == 0

test_forward_mode_4()

def test_forward_mode_5():
    x = 3
    y = Node(7, fm_seed=1)
    f = x-y
    assert f._fmd == -1

test_forward_mode_5()

def test_forward_mode_mixed_seed():
    x = Node(3, fm_seed = 1/2)
    y = Node(8, fm_seed = 1/2)
    f = x * y
    assert f._fmd == 5.5

test_forward_mode_mixed_seed()

def test_forward_mode_6():
    x = Node(3, fm_seed = 1)
    f = np.cos(x)
    assert f._fmd == -np.sin(3)

test_forward_mode_6()
