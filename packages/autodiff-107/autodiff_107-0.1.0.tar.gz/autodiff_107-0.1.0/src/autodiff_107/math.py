from .diff import Node
from functools import wraps
import numpy as np

# To allow for importing numpy without alias np
numpy = np

@np.vectorize
def op_on_node(x, op, d_op, name_op, **kwargs):
    result = Node(op(x._value, **kwargs))
    result._d[x] = d_op(x._value, **kwargs)
    result._fmd = result._d[x] * x._fmd
    result._operation[x]=name_op()
    return result

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
            result = op_on_node(x, op, d_op, name_op, **kwargs)
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

def d_log10(x):
    """derivative of log10

    :param x: input
    :type x: :class: Node
    :return: 1/(x*np.log(10))
    :rtype: :class: Node
    """
    return 1/(x*np.log(10))

def name_log10():
    return 'log10'

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

def _exp_base(x, base=np.exp(1)):
    return np.exp(x*np.log(base))

def d_exp_base(x, base=np.exp(1)):
    """derivative of exp to base 

    :param x: input
    :type x: :class: Node
    :return: np.log(base)*np.exp(x*np.log(base))
    :rtype: :class: Node
    """
    return np.log(base)*np.exp(x*np.log(base))

def name_exp_base(base=np.exp(1)):
    return 'exp_base_'+str(base)

def _log_base(x, base=np.exp(1)):
    return np.log(x)/np.log(base)

def d_log_base(x, base=np.exp(1)):
    """derivative of exp to base 

    :param x: input
    :type x: :class: Node
    :return: 1/(x*np.log(base))
    :rtype: :class: Node
    """
    return 1/(x*np.log(base))

def name_log_base(base=np.exp(1)):
    return 'log_base_'+str(base)


def _sigmoid(x):
    return np.exp(x)/(1 + np.exp(x))

def d_sigmoid(x):
    """derivative of sigmoid

    :param x: input
    :type x: :class: Node
    :return: np.exp(-x)/(1 + np.exp(-x))**2
    :rtype: :class: Node
    """
    return np.exp(-x)/(1 + np.exp(-x))**2

def name_sigmoid():
    return 'sigmoid'

'''
def _logistic(x, L=1, k=1, x_0=0):
    return L/(1 + np.exp(-k*(x-x_0)))

def d_logistic(x, L=1, k=1, x_0=0):
    """derivative of logistic

    :param x: input
    :type x: :class: Node
    :return: (Lk*np.exp(-k*(x-x_0)))/(1 + np.exp(-k*(x-x_0)))**2
    :rtype: :class: Node
    """
    return (L*k*np.exp(-k*(x-x_0)))/(1 + np.exp(-k*(x-x_0)))**2

def name_logistic():
    return 'logistic'
'''

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
np.log10 = unary_operation(np.log10, d_log10, name_log10)
np.exp = unary_operation(np.exp, d_exp, name_exp)
np.exp_base = unary_operation(_exp_base, d_exp_base, name_exp_base)
np.log_base = unary_operation(_log_base, d_log_base, name_log_base)

np.sigmoid = unary_operation(_sigmoid, d_sigmoid, name_sigmoid)
# np.logistic = unary_operation(_logistic, d_logistic, name_logistic)
