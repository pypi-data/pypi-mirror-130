from .diff import Node
from functools import wraps
import numpy as np

# To allow for importing numpy without alias np
numpy = np

def unary_operation(op, d_op, name_op):
    """unary operation

    :param op: operation
    :type op: numpy method
    :param d_op: derivative of operation
    :type d_op: numpy method
    :param name_op: name of operation
    :type name_op: function returing string
    :return: operation
    :rtype: function (callable)
    """
    @wraps(op)
    def operation(x, **kwargs):
        # Try using x as Node
        try:
            result = Node(op(x._value, **kwargs))
            result._d[x] = d_op(x._value, **kwargs)
            result._fmd = result._d[x] * x._fmd
            result._operation[x]=name_op()
        except AttributeError:
            # x is not a Node
            result = op(x, **kwargs)
        return result
    return operation

def d_cos(x):
    """derivative of cos

    :param x: input
    :type x: :class: Node
    :return: -sin(x)
    :rtype: :class: Node
    """
    return -np.sin(x)

def name_cos():
    return 'cos'

def d_sin(x):
    """derivative of sin

    :param x: input
    :type x: :class: Node
    :return: cos(x)
    :rtype: :class: Node
    """
    return np.cos(x)

def name_sin():
    return 'sin'

def d_tan(x):
    """derivative of tan

    :param x: input
    :type x: :class: Node
    :return: 1/(np.cos(x))**2
    :rtype: :class: Node
    """
    return 1/(np.cos(x))**2

def name_tan():
    return 'tan'

def d_arccos(x):
    """derivative of arccos

    :param x: input
    :type x: :class: Node
    :return: -1/np.sqrt(1-x**2)
    :rtype: :class: Node
    """
    return -1/np.sqrt(1-x**2)

def name_arccos():
    return 'arccos'

def d_arcsin(x):
    """derivative of arcsin

    :param x: input
    :type x: :class: Node
    :return: 1/np.sqrt(1-x**2)
    :rtype: :class: Node
    """
    return 1/np.sqrt(1-x**2)

def name_arcsin():
    return 'arcsin'

def d_arctan(x):
    """derivative of actan

    :param x: input
    :type x: :class: Node
    :return: 1/(1+x**2)
    :rtype: :class: Node
    """
    return 1/(1+x**2)

def name_arctan():
    return 'arctan'

def d_cosh(x):
    """derivative of cosh

    :param x: input
    :type x: :class: Node
    :return: sinh(x)
    :rtype: :class: Node
    """
    return np.sinh(x)

def name_cosh():
    return 'cosh'

def d_sinh(x):
    """derivative of sinh

    :param x: input
    :type x: :class: Node
    :return: cosh(x)
    :rtype: :class: Node
    """
    return np.cosh(x)

def name_sinh():
    return 'sinh'

def d_tanh(x):
    """derivative of tanh

    :param x: input
    :type x: :class: Node
    :return: 1-np.tanh(x)**2
    :rtype: :class: Node
    """
    return 1-np.tanh(x)**2

def name_tanh():
    return 'tanh'

def d_arccosh(x):
    """derivative of arccosh

    :param x: input
    :type x: :class: Node
    :return: 1/np.sqrt(x**2-1)
    :rtype: :class: Node
    """
    return 1/np.sqrt(x**2-1)

def name_arccosh():
    return 'arccosh'

def d_arcsinh(x):
    """derivative of arcsinh

    :param x: input
    :type x: :class: Node
    :return:  1/np.sqrt(x**2+1)
    :rtype: :class: Node
    """
    return 1/np.sqrt(x**2+1)

def name_arcsinh():
    return 'arcsinh'

def d_arctanh(x):
    """derivative of arctanh

    :param x: input
    :type x: :class: Node
    :return: 1/(1-x**2)
    :rtype: :class: Node
    """
    return 1/(1-x**2)

def name_arctanh():
    return 'arctanh'

def d_log(x):
    """derivative of log

    :param x: input
    :type x: :class: Node
    :return: 1/x
    :rtype: :class: Node
    """
    return 1/x

def name_log():
    return 'log'

def d_exp(x):
    """derivative of exp

    :param x: input
    :type x: :class: Node
    :return: exp(x)
    :rtype: :class: Node
    """
    return np.exp(x)

def name_exp():
    return 'exp'

np.cos = unary_operation(np.cos, d_cos, name_cos)
np.sin = unary_operation(np.sin, d_sin, name_sin)
np.tan = unary_operation(np.tan, d_tan, name_tan)

np.arccos = unary_operation(np.arccos, d_arccos, name_arccos)
np.arcsin = unary_operation(np.arcsin, d_arcsin, name_arcsin)
np.arctan = unary_operation(np.arctan, d_arctan, name_arctan)

np.cosh = unary_operation(np.cosh, d_cosh, name_cosh)
np.sinh = unary_operation(np.sinh, d_sinh, name_sinh)
np.tanh = unary_operation(np.tanh, d_tanh, name_tanh)

np.arccosh = unary_operation(np.arccosh, d_arccosh, name_arccosh)
np.arcsinh = unary_operation(np.arcsinh, d_arcsinh, name_arcsinh)
np.arctanh = unary_operation(np.arctanh, d_arctanh, name_arctanh)

np.log = unary_operation(np.log, d_log, name_log)
np.exp = unary_operation(np.exp, d_exp, name_exp)
