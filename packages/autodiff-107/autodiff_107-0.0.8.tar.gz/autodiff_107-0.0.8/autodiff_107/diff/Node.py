import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
# from NetworkViz import draw_graph_without_edge_labels
# from NetworkVizExpensive import draw_graph_expensive
# from ReverseModeViz import draw_reverse_graph
# import nodemath

class Node:
    """
    This is the main object for variables used for Automatic Differentiation.
    Operations for the functions the user wants 
    to use will have to be done using this object. 
    Constants involved in the function can be inserted normally 
    and do not need to be wrapped in Node objects.

    :param value: Value of the variable
    :type value: int, float 
    :param fm_seed: Seed to use in forward mode. Most likely this will be 1 for one input
        and 0 for all others, but specific use cases may warrant different
        weights. Default: 0
    :type fm_seed: int, float
    :ivar _value: Value at which the variable is evaluated
    :ivar _d: Value of the derivative of this Node with respect to each 
        parent at the point where this Node is evaluated.
    :ivar _fmd: Forward mode derivative. At any point after the forward pass,
        this should store the derivative of any node with respect
        to some input as defined by the fm_seed. This could actually be
        the sum of derivatives of the node with respect to some weighting
        of inputs. If that is your use case, you likely know what you are doing.
    """
    def __init__(self, value, fm_seed=0):
        """
        Constructor method
        """
        # Value at which we evaluate the variable
        self._value = value
        self._fmd = fm_seed
        # Derivative of the variable with respect to each parent
        self._d = dict()
        # Keep track of parent/child relations (for the graph)
        self._operation = dict()

    def __str__(self):
        return str(self._value)

    def __add__(self, other):
        # Try treating both as Nodes
        try:
            result = Node(self._value + other._value)
            result._d[self] = 1
            # Need to handle case where other == node
            result._d[other] = result._d.get(other, 0) + 1
            # Handle forward mode
            # General idea: v2=f(v0,v1)->Dpv2=f_0(v0,v1)*Dpv0+f_1(v0,v1)*Dpv1 where f_0 
            # and f_1 are partial derivatives of f
            # v2=v1+v0 -> Dpv2=Dpv1+Dpv0
            result._fmd = self._fmd + other._fmd
            # operation
            result._operation[self]='add'
            result._operation[other]='add'
            if self==other:
                result._operation[self]='time 2'
        except AttributeError:
            # This is necessary to make sure numpy broadcasting works as expected
            if type(other) == np.ndarray:
                return NotImplemented
            # other is a number (or unsupported object)
            # error will get thrown for unsupported objects
            result = Node(self._value + other)
            result._d[self] = 1
            # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
            # v1=v0+cst-> Dpv1=Dpv0
            result._fmd = self._fmd
            # operation
            result._operation[self]='add {}'.format(other)
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other, swapped=False):
        # Try treating both as Nodes
        try:
            # RAPH: I DONT THINK SWAP NECESSARY HERE: BOTH NODES
            result = Node(self._value - other._value)
            result._d[self] = 1 if not swapped else -1
            result._d[other] = result._d.get(other, 0) + (-1 if not swapped else 1)
            # General idea: v2=f(v0,v1)->Dpv2=f_0(v0,v1)*Dpv0+f_1(v0,v1)*Dpv1 where f_0 
            # and f_1 are partial derivatives of f
            # v2=v0-v1-> Dpv2=Dpv0-Dpv1
            result._fmd = result._d[other] * other._fmd + result._d[self] * self._fmd
            # operation
            result._operation[self]='add' if not swapped else 'add the opposite'
            result._operation[other]='add the opposite' if not swapped else 'add'
            if self==other:
                result._operation[self]='cancelling itself'
        except AttributeError:
            if type(other) == np.ndarray:
                return NotImplemented
            # other is a number (or unsupported object)
            # error will get thrown for unsupported objects
            result = Node(self._value - other if not swapped else other - self._value)
            result._d[self] = 1 if not swapped else -1
            # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
            # v1=v0-cst-> Dpv1=Dpv0
            # v1=cst-v0-> Dpv1=-Dpv0
            result._fmd = result._d[self] * self._fmd
            # operation
            result._operation[self]='substract {}'.format(other)
        return result

    def __rsub__(self, other):
        # RAPH: I THINK BOTH NODES HANDLED ABOVE
        return self.__sub__(other, swapped=True)

    def __mul__(self, other):
        # Try treating both as Nodes
        try:
            result = Node(self._value * other._value)
            result._d[self] = other._value
            result._d[other] = result._d.get(other, 0) + self._value
            # General idea: v2=f(v0,v1)->Dpv2=f_0(v0,v1)*Dpv0+f_1(v0,v1)*Dpv1 where f_0 
            # and f_1 are partial derivatives of f
            # v2=v0*v1-> Dpv2=v1*Dpv0+v0*Dpv1
            result._fmd = result._d[self] * self._fmd + result._d[other] * other._fmd
            # operation
            result._operation[self]='times'
            result._operation[other]='times'
            if self==other:
                result._operation[self]='time itself'
        except AttributeError:
            if type(other) == np.ndarray:
                return NotImplemented
            # other is a number (or unsupported object)
            # error will get thrown for unsupported objects
            result = Node(self._value * other)
            result._d[self] = other
            # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
            # v1=v0*cst-> Dpv1=cst*Dpv0
            result._fmd = result._d[self] * self._fmd
            # operation
            result._operation[self]='times {}'.format(other)
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        # Try treating both as Nodes
        try:
            result = Node(self._value / other._value)
            result._d[self] = 1 / other._value
            result._d[other] = result._d.get(other, 0) + -(self._value/other._value**2)
            # General idea: v2=f(v0,v1)->Dpv2=f_0(v0,v1)*Dpv0+f_1(v0,v1)*Dpv1 where f_0 
            # and f_1 are partial derivatives of f
            # v2=v0/v1= -> Dpv2=1/v1*Dpv0-(v0/v1**2)*Dpv1
            result._fmd = result._d[self] * self._fmd + result._d[other] * other._fmd
            # operation
            result._operation[self]='times' 
            result._operation[other]='times the inverse' 
            if self==other:
                result._operation[self]='divide by itself'
        except AttributeError:
            if type(other) == np.ndarray:
                return NotImplemented
            # other is a number (or unsupported object)
            # error will get thrown for unsupported objects
            result = Node(self._value / other)
            result._d[self] = 1 / other
            # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
            # v1=v0/cst= -> Dpv1=1/cst*Dpv0
            result._fmd = result._d[self] * self._fmd
            # operation
            result._operation[self]='times 1/{}'.format(other)
        return result

    def __rtruediv__(self, other):
        # If both are nodes, division will be handled by __truediv__
        # other is a number (or unsupported object)
        # error will get thrown for unsupported objects
        if type(other) == np.ndarray:
            return NotImplemented
        result = Node(other / self._value)
        result._d[self] = -other / self._value ** 2
        # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
        # v1=cst/v0= -> Dpv1=-cst/(v0**2)*Dpv0
        result._fmd = result._d[self] * self._fmd
        # operation
        result._operation[self]='inverse times {}'.format(other)
        return result

    def __neg__(self):
        # Negations
        result=Node(-self._value)
        result._d[self]=-1
        # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
        # v1=-v0-> Dpv1=-Dpv0
        result._fmd = -self._fmd
        # operation
        result._operation[self]='negate' 
        return result

    def __pow__(self, other):
        # Try treating both as Nodes
        try:
            # partial derivatives of x**y not defined at x=0
            if not self._value!=0: raise Exception("Not differentiable")
            result = Node(self._value**other._value)
            result._d[self] = other._value*(self._value**(other._value-1))
            # Need to handle case where other == node ie x**x
            # x**x is e**xln(x). The derivative is ln(x)x**x+x**x
            # the derivative of x**y wrt to y i ln(x)*(x**y)
            # if result._d[other] exists, it is x*(x**(x-1)) ie x**x
            result._d[other] = result._d.get(other,0)+np.log(self._value)*(self._value**other._value)
            # General idea: v2=f(v0,v1)->Dpv2=f_0(v0,v1)*Dpv0+f_1(v0,v1)*Dpv1 where f_0 
            # and f_1 are partial derivatives of f
            # v2=v1**v0=exp(v0*ln(v1))-> Dpv2=ln(v1)*(v1**v0)*Dpv0+v0*(v1**v0)*(1/v1)*Dpv1
            result._fmd = result._d[self] * self._fmd + result._d[other] * other._fmd
            # operation
            result._operation[self]='to the power of {}'.format(other._value) 
            result._operation[other]='Used as a power' 
            if self==other:
                result._operation[self]='to the power of itself'
        except AttributeError:
            if type(other) == np.ndarray:
                return NotImplemented
            # other is a number (or unsupported object)
            # error will get thrown for unsupported objects
            # x**0 is not differentiable at 0:
            if self._value==0 and other==0: raise Exception("Not differentiable")
            else:
                result = Node(self._value**other)
                result._d[self] = other*(self._value**(other-1))
                # General idea: v1=f(v0,cst)->Dpv1=f'(v0,cst)*Dpv0
                # v1=v0**cst-> Dpv1=(cst)*(v0**(cst-1))*Dpv0
                result._fmd = result._d[self] * self._fmd
                # operation
                result._operation[self]='to the power of {}'.format(other) 
        return result

    def __rpow__(self, other):
        # both as Nodes will be handled by pow
        # other is a number (or unsupported object)
        # error will get thrown for unsupported objects
        # x**0 is not differentiable at 0:
        if type(other) == np.ndarray:
            return NotImplemented
        if other==0 and self._value==0: raise Exception("Not differentiable")
        else:
            result = Node(other**self._value)
            result._d[self] = np.log(other)*(other**(self._value))
            # v1=cst**v0=exp(v0*ln(cst))-> Dpv1=ln(cst)*(cst**v0)*Dpv0
            result._fmd = result._d[self] * self._fmd
            # operation
            result._operation[self]='{} raised to the power of {}'.format(other, self._value) 
        return result

    def _backward(self):
        '''
        This method does a backward pass in the computational graph
        starting from current node.
        '''
        self._df = 1
        nodequeue = [self]
        visited = set()

        while len(nodequeue) > 0:
            node = nodequeue.pop(0)
            visited.add(node)
            
            # Add this childs contribution to all parents derivatives
            for parent, derivative in node._d.items():
                try:
                    parent._df += node._df * derivative
                except AttributeError:
                    # This is the first contribution to the parent
                    parent._df = node._df * derivative
                if parent not in visited:
                    nodequeue.append(parent)

    def _clear_df(self):
        """
        This method clears the partial deribatives after _backward has been called. 
        """
        nodequeue = [self]
        visited = set()

        while len(nodequeue) > 0:
            node = nodequeue.pop(0)
            visited.add(node)
            node._df = 0

            for parent, _ in node._d.items():
                nodequeue.append(parent)

    def _derivative(self, X):
       '''
       This function computes the derivative of this variable :class:`autodiff_107.Node` with respect to X.
       :param X: parameter to compute the derivative with respect to. 
       :type X: :class:`autodiff_107.Node`

       :return: np.array
       '''
       # We only use this internally so we guarantee X is a Node or an ndarray of Nodes
       self._clear_df()
       # Handle elements in X that may not have been used to compute self
       clear_X_dfs = np.vectorize(lambda x: x._clear_df())
       clear_X_dfs(X)
       self._backward()
       nd_to_df = np.vectorize(lambda x: x._df)
       return nd_to_df(X)

    
class Var(Node):
    """
    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------
    """
    def __init__(self, *args, **kwargs):
        super(Var, self).__init__(*args, **kwargs)

    @property
    def value(self):
        '''This holds the value of this variable'''
        return self._value

def variable(x):
    '''
    This function takes a number or numpy array of numbers and returns a "variable" which
    is a numpy array of Node objects that will handle automatic differentiation
    :param x: variables that will be used for automatic differentiation
    :type x: numeric or np.array
    
    :return: np.array w/ dtype = autodiff_107.Node.Node
    '''
    val_to_node = np.vectorize(lambda x: Node(x))
    X = val_to_node(x)
    return X

def value(x):
    '''
    This function takes in a numpy array returned by variable() or the result of a calculation
    using a numpy array from variable() and returns a numpy array of the numeric values of x
    :param x: np.array w/ dtype = autodiff_107.Node.Node
    :return: np.array
    '''
    node_to_val = np.vectorize(lambda x: x._value)
    return node_to_val(x)

def set_fm_seed(X, seed):
    '''
    This function sets the forward mode seed for the variable X to be used in the forward pass in
    any following calculations. X and seed should have matching shapes.
    :param X: np.array w/ dtype = autodiff_107.Node.Node
    :param seed: np.array
    :return: None
    '''
    if not X.shape == seed.shape:
        raise ValueError("X and seed shapes do not match")
    for idx, x in np.ndenumerate(X):
        x._fmd = seed[idx]

def get_fm_derivative(Y):
    '''
    If a forward mode seed was set using set_fm_seed, this function will return the derivative
    calculated using forward mode with the set seed.
    :param Y: nd.array w/ dtype = autodiff_107.Node.Node
    :return: np.array
    '''
    node_to_fmd = np.vectorize(lambda x: x._fmd)
    return node_to_fmd(Y)

def get_fm_seed(X):
    '''
    This function will return the current seed of X to be used in forward mode
    :param X: np.array w/ dtype = autodiff_107.Node.Node
    :return: np.array
    '''
    return get_fm_derivative(X)

def derivative(f : np.ndarray, X : np.ndarray):
    '''
    This function will return the derivative of f with respect to X. f and X must both be one dimensional but their
    lengths need not match. If f is a vector, the jacobian will be returned
    :param f: np.array w/ dtype = autodiff_107.Node.Node or autodiff_107.Node.Node
    :param X: np.array w/ dtype = autodiff_107.Node.Node
    :return: np.array
    '''
    try:
        if not f.ndim == 1 or not X.ndim == 1:
            raise ValueError("f and X must both be 1-dimensional")
    except AttributeError:
        return f._derivative(X)
    jacobian = []
    for fval in f:
        jacobian.append(fval._derivative(X))
    return np.array(jacobian)

if __name__ == "__main__":
    x = Node(8)
    y = Node(3)
    z = Node(11)
    w=Node(10)
    f = y-z*np.sin(x)+np.cos(w)+np.tanh(w*x)
    g=x+x+y+z
    #draw_graph_without_edge_labels(np.array(f))
    #plt.cla()
    #draw_graph_expensive(np.array(f))
    #plt.cla()
    f_reverse=x+y+z*x
    #draw_graph_expensive(np.array(f_reverse))
    #plt.cla()
    #draw_reverse_graph(np.array(f_reverse))
    #plt.cla()
    #draw_graph(np.array(f))
    #draw_graph_without_edge_labels(np.array(f))
    g1=Node(1)
    g2=Node(2)
    g3=g1+g2
    g4=-g3
    g4._backward()
    #draw_graph(np.array(g4))
