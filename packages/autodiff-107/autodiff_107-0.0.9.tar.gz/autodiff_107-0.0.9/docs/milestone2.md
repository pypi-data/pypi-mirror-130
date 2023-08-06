Nota Bene: The file created as milestone2.md before November 11 and submitted on November 11 has been renamed milestone2_progress.md.

# Introduction

**Describe the problem the software solves and why it's important to solve that problem.**

<p align="justify">Automatic Differentiation is able to evaluate real-valued functions of one variable and their derivative exactly. For real-valued functions of more than one variable, AD evaluates the function and its gradient. For multivariable, vector-valued functions, AD evaluates the function and its Jacobian. By extension, AD is also able to evaluate higher order derivatives (and Hessians, etc…). This is an important problem as many algorithms use derivatives of functions (eg Newton method for root finding, BFGS,  gradient descent and stochastic gradient descent…). In particular, AD is intimately linked to backpropagation in Machine Learning (backprop is a special case of AD) which has enabled engineers to train Deep Neural Network to solve a very diverse set of tasks, from image classification to solving PDEs using NNs. Other methods to obtain derivatives of functions include numerical methods and symbolic differentiation, but they are not suitable for Machine Learning. </p>

# Background

**Describe (briefly) the mathematical background and concepts as you see fit. You do not need to give a treatise on automatic differentiation or dual numbers. Just give the essential ideas (e.g. the chain rule, the graph structure of calculations, elementary functions, etc).**

Consider a function of interest f. AD computes the evaluation of the function f and of its derivatives at a given point. The key idea is to use the composition of simple functions (called elementary functions) to get to f.

### Composition of elementary functions

As in elementary mathematics, the order of operations is important. In evaluating <a href="https://www.codecogs.com/eqnedit.php?latex=(2\times&space;3)&plus;4" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(2\times&space;3)&plus;4" title="(2\times 3)+4" /></a>, the program needs to know to evaluate <a href="https://www.codecogs.com/eqnedit.php?latex=2&space;\times&space;3" target="_blank"><img src="https://latex.codecogs.com/gif.latex?2&space;\times&space;3" title="2 \times 3" /></a> first and then add the result (6) to 4 to obtain 10. In a similar fashion, when evaluating a function, eg:

<a href="https://www.codecogs.com/eqnedit.php?latex=f(x)=\sin((2x)^2)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x)=\sin((2x)^2)" title="f(x)=\sin((2x)^2)" /></a>

We first need to compute:

<a href="https://www.codecogs.com/eqnedit.php?latex=2\times&space;x=:y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?2\times&space;x=:y" title="2\times x=:y" /></a>

then:

<a href="https://www.codecogs.com/eqnedit.php?latex=(2x)^2=:z" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(2x)^2=:z" title="(2x)^2=:z" /></a>

ie <a href="https://www.codecogs.com/eqnedit.php?latex=y^2=:z" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y^2=:z" title="y^2=:z" /></a>, then finally:

<a href="https://www.codecogs.com/eqnedit.php?latex=\sin((2x)^2=:w" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sin((2x)^2=:w" title="\sin((2x)^2=:w" /></a>

ie:

<a href="https://www.codecogs.com/eqnedit.php?latex=\sin(z)=w" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sin(z)=w" title="\sin(z)=w" /></a>

Thus, we are composing the elementary functions:

<a href="https://www.codecogs.com/eqnedit.php?latex=f_1:&space;x&space;\mapsto&space;2x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_1:&space;x&space;\mapsto&space;2x" title="f_1: x \mapsto 2x" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=f_2:&space;x&space;\mapsto&space;x^2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_2:&space;x&space;\mapsto&space;x^2" title="f_2: x \mapsto x^2" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=f_3:&space;x&space;\mapsto&space;\sin(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_3:&space;x&space;\mapsto&space;\sin(x)" title="f_3: x \mapsto \sin(x)" /></a>

To get:

<a href="https://www.codecogs.com/eqnedit.php?latex=f(x)=(f_3&space;\circ&space;f_2&space;\circ&space;f_1)(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x)=(f_3&space;\circ&space;f_2&space;\circ&space;f_1)(x)" title="f(x)=(f_3 \circ f_2 \circ f_1)(x)" /></a>

We can keep track of the composition of such elementary operations with a graph, where nodes represent variables (independent or dependent) and links represent elementary operations.

Similarly, to take the derivative of our function f, we can use the chain rule. As the derivatives of elementary functions are known and easy to compute, we are able to find the derivative of our complicated function f. In particular, we use:

<a href="https://www.codecogs.com/eqnedit.php?latex=f_1':&space;x&space;\mapsto&space;2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_1':&space;x&space;\mapsto&space;2" title="f_1': x \mapsto 2" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=f_2':&space;x&space;\mapsto&space;2x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_2':&space;x&space;\mapsto&space;2x" title="f_2': x \mapsto 2x" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=f_3':&space;x&space;\mapsto&space;\cos(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_3':&space;x&space;\mapsto&space;\cos(x)" title="f_3': x \mapsto \cos(x)" /></a>

And we use the chain rule: 

<a href="https://www.codecogs.com/eqnedit.php?latex=(h&space;\circ&space;g)'=&space;g'\times&space;(h'&space;\circ&space;g)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(h&space;\circ&space;g)'=&space;g'\times&space;(h'&space;\circ&space;g)" title="(h \circ g)'= g'\times (h' \circ g)" /></a>

We can compose the chain rule multiple times to get f’:

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;f'&=(f_3&space;\circ&space;f_2&space;\circ&space;f_1)'\\&space;&&space;=((f_3&space;\circ&space;f_2)&space;\circ&space;f_1)'\\&space;&&space;=f_1'&space;\times&space;(f_3&space;\circ&space;f_2)'\circ&space;f_1\\&space;&=&space;f_1'&space;\times&space;(f_2'&space;\times&space;f_3'&space;\circ&space;f_2)&space;\circ&space;f_1&space;=&space;(f_1'&space;f_2')\times&space;(f_3'&space;\circ&space;f_2&space;\circ&space;f_1)&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;f'&=(f_3&space;\circ&space;f_2&space;\circ&space;f_1)'\\&space;&&space;=((f_3&space;\circ&space;f_2)&space;\circ&space;f_1)'\\&space;&&space;=f_1'&space;\times&space;(f_3&space;\circ&space;f_2)'\circ&space;f_1\\&space;&=&space;f_1'&space;\times&space;(f_2'&space;\times&space;f_3'&space;\circ&space;f_2)&space;\circ&space;f_1&space;=&space;(f_1'&space;f_2')\times&space;(f_3'&space;\circ&space;f_2&space;\circ&space;f_1)&space;\end{align*}" title="\begin{align*} f'&=(f_3 \circ f_2 \circ f_1)'\\ & =((f_3 \circ f_2) \circ f_1)'\\ & =f_1' \times (f_3 \circ f_2)'\circ f_1\\ &= f_1' \times (f_2' \times f_3' \circ f_2) \circ f_1 = (f_1' f_2')\times (f_3' \circ f_2 \circ f_1) \end{align*}" /></a>

Indeed, 

<a href="https://www.codecogs.com/eqnedit.php?latex=f'(x)=8x\cos((2x)^2)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f'(x)=8x\cos((2x)^2)" title="f'(x)=8x\cos((2x)^2)" /></a>

We can use the following (non-exhaustive) list of elementary functions and derivatives:


| Function    |  Derivative  |   
|-------------|--------------|
|   cos(x)    |  -sin(x)     |  
|   sin(x)    |  cos(x)      |  
|   exp(x)    |  exp(x)      |
|   const     |  0           |
|   ln(x)     |  1/x         |
|   tan(x)    |  sec(x)sec(x)|

### Computational graph

Note that we can also keep track of the calculation of derivatives using a graph structure. For example, the following graph represents the function:

<a href="https://www.codecogs.com/eqnedit.php?latex=g:&space;\mathbb{R}^2&space;\rightarrow&space;\mathbb{R}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?g:&space;\mathbb{R}^2&space;\rightarrow&space;\mathbb{R}" title="g: \mathbb{R}^2 \rightarrow \mathbb{R}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=g:&space;(x,y)^T&space;\mapsto&space;x&plus;y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?g:&space;(x,y)^T&space;\mapsto&space;x&plus;y" title="g: (x,y)^T \mapsto x+y" /></a>

where:

<a href="https://www.codecogs.com/eqnedit.php?latex=v_{-1}=x$&space;and&space;$v_0=y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?v_{-1}=x$&space;and&space;$v_0=y" title="v_{-1}=x$ and $v_0=y" /></a>

![](figs/Computational_Graph.png)

We keep track of the function evaluation and its derivative at <a href="https://www.codecogs.com/eqnedit.php?latex=(x,y)^T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(x,y)^T" title="(x,y)^T" /></a> using a table.

Reverse mode AD also uses the chain rule and the computational graph in a similar fashion.


# Installation

> The package will be uploaded on PyPi for usage with pip, until then for general usage these are the installation steps: 

Clone github repository:
```cmd
$ git clone https://github.com/cs107-errajexi/cs107-FinalProject
```
Create and activate virtual environment, for example `autodiff-107-env`:
```
$ python3 -m venv /path/to/autodiff_107-env
```
```
$ source autodiff_107-env/bin/activate
```

Install requirements using pip:
```cmd
$ pip install -r requirements.txt
```
You are now ready to use the package!

## Building Docs
> The repository is private and thus cannot host the documentation page. However you can build a working HTML page yourself.

```cmd
$ cd cs107-FinalProject/docs
$ make html
$ open build/html/index.html                      
```

# Get started

> This tutorial is valid until the package will be published. Currently only the working backend is implemented. User friendly wrappers and functions will be implemented at a later stage.

## Importing the package
```python
import autodiff_107 as ad
```

## Doing Math

To actually get the benefits of AD in our package, users will wrap their variables with the ```Node``` object. Operations for the functions the user wants to use will have to be done using this object. Constants involved in the function can be inserted normally and do not need to be wrapped in ```Node``` objects.

Example:

```python
x = ad.Node(10)
y = ad.Node(17)

z = (x + y)**2 - 14
```

This package handily integrates all numpy functions that the user can call with the commonly used `np` alias:
```python
from autodiff_107.nodemath import numpy as np

x=ad.Node(2)
z=3*x
w=np.exp(z)
f=np.cos(w)
```

## Taking derivates

> These private functions will be wrapped in user functions in a later milestone. 

### Using forward mode (by setting a seed):
```python
x = Node(3, fm_seed = 1)
y = Node(7)
z = Node(5)
f = (x * y) + (2 * x) / x + z / z
f._fwd
```
### Using backward mode:
```python
f._derivative(x)
```
### Taking partial derivatives
```python
# derive w w.r.t z
w._derivative(z)
```
## Newton's root finding example
```python
from autodiff_107.nodemath import numpy as np

def newton(f, x0, tol):
    xn = Node(x0)
    while np.abs(xn._value) > tol:
        f = f(xn)
        df = f._derivative(xn)
        xn -= f/df
    return xn._value

# find root of 3*x+1
x0 = 1
f = lambda x: 3*x+1
tol = 1e-3
root = newton(f, x0, tol)
```

# Software organization

## Directory structure
```
cs107-FinalProject
├── autodiff_107
|   ├── __init__.py
|   ├── Node.py
|   ├── nodemath.py
|   ├── NetworkVizExpensive.py
|   ├── NetworkViz.py
│   ├── test_nodemath.py
│   └── test_Node.py
├── docs
│   ├── build
|   │   └──...
│   ├── source
|   │   └──...
│   └── milestone2.md
├── requirements.txt
├── LICENCE
└── README.md
```
 - `autodiff_107` contains Node.py, which contain Node, our main class for variables. nodemath.py deals with overriding numpy functions for members of Node. NetworkVIzExpensive.py and NetworkViz.py are used for visualisation purposes. Our tests are in test_Node.py and test_nodemath.py.
 - `docs` contains the source and build code for the Sphinx powered documentation. It generates an HTML page. 
 - Our License, README and `requirements.txt` are in the base directory.

### A note on our license

As mentioned above, our License can be found in the LICENSE file

<p align="justify">We use the MIT license. It puts very few limitations on what can be done with the code (copy, modify, publish, distribute and even sell) and is compatible with many GNU General Public Licenses. The conditions only require preservations of copyright and license notices. </p>

## Basic modules

<p align="justify">Node.py contains our basic Node class, which we use to represent independent and dependent variables, as well as outputs. Instances of nodes represent variables. nodemath.py is used to overwrite bumpy functions so that we can call them on instances of class Node. </p>

<p align="justify">We have two basic modules for visualisation of the computational graph and the tangent trace (currently under development). NetworkViz.py contains the basic functions to visualise the computational graph as a graph and as a directed graph. NetworkVizExpensive.py contains functions to represent the directed graph with a nice layout and will contain our code for making gifs. </p>

## Tests

Our tests are in test_Node.py and test_nodemath.py. So far, to run them, we need to be in autodiff_107 directory and run:

```python
python3 test_Node.py
```
and

```python
python3 test_nodemath.py
```

This is integrated using TravisCI and CodeCov and is reflected with badges.

# Implementation details

## Overview

The core data structure for our library is a `Node`. `Node`s make up the computational graph that we  traverse for forward mode AD as well as for forward and backward passes of reverse mode. These are the same as `Var`s but we give them a different name that is more intuitive for users. They each have a value, a parents list, and a derivative with respect to each parent.

`Node`s have overloaded operators such that when they are used in a computation, new nodes are created for the result of the operation, and the resulting:

[![\dfrac{\partial v_j}{\partial v_i}](https://camo.githubusercontent.com/6ad166fd9961fc001980f4bc69fdff1fe6b2f60a83ef75b2a5f7924e93a832d5/68747470733a2f2f6c617465782e636f6465636f67732e636f6d2f6769662e6c617465783f5c64667261637b5c7061727469616c2673706163653b765f6a7d7b5c7061727469616c2673706163653b765f697d)](https://www.codecogs.com/eqnedit.php?latex=\dfrac{\partial&space;v_j}{\partial&space;v_i})

are stored for each intermediate node. The result of a function is returned as one node that is the descendant of all of the inputs used in that computation.

We store partial derivatives as a dictionary because we need to store the derivative with respect to each parent.

We had to implement new versions of operators like cos, exp, etc. that operate on Nodes. They also handle setting derivatives. 

We  have a `_backward` function that handles doing the reverse pass on results, and calculating the derivatives of the result with respect to the inputs. We will allow both result and inputs to be either scalar or an array of `Var`s in due course. Our library currently supports any number of inputs.

## Forward mode AD

For forward mode AD, we associate to every instance of node (ie every independent or dependent variable), a seed `self._fmd`. By default, this would be set to 0. Every time we add to nodes together, we correspondingly set the seed of the new node to the sum of the seeds of its parents. This is because if:

<img src="https://latex.codecogs.com/svg.image?v_2=v_1&plus;v_0&space;" title="v_2=v_1+v_0 " />

then:

<img src="https://latex.codecogs.com/svg.image?\dot{v_2}=\dot{v_1}&plus;\dot{v_0}&space;" title="\dot{v_2}=\dot{v_1}+\dot{v_0} " />

or using the notation from lectures:

<img src="https://latex.codecogs.com/svg.image?D_pv_2=D_pv_1&plus;D_pv_0&space;" title="D_pv_2=D_pv_1+D_pv_0 " />

Likewise, we can use the fact that if:

<img src="https://latex.codecogs.com/svg.image?v_2=f(v_0,v_1)&space;" title="v_2=f(v_0,v_1) " />

<img src="https://latex.codecogs.com/svg.image?D_pv_2=f_0(v_0,v_1)D_pv_0&plus;f_1(v_0,v_1)D_pv_1&space;" title="D_pv_2=f_0(v_0,v_1)D_pv_0+f_1(v_0,v_1)D_pv_1 " />

where <img src="https://latex.codecogs.com/svg.image?f_0(v_0,v_1)&space;" title="f_0(v_0,v_1) " /> is the partial derivative of f with respect to its first input.

So we can update the seed of every new node - this depends on how we combine the node's parent.

For example,


```python
x = Node(3, fm_seed=1/2)
y = Node(7, fm_seed=1/2)
f = x-y
# Then 
# f._fmd == 0
```
Here, we see that both x and y have seed 1/2.

## Reverse Mode AD

> This is not user facing

Our reverse mode AD is called `_backward`.

For reverse mode AD, we use the chain rule as well as our dictionary to store the partial derivatives of a child with respect to its parents (`self._d`). 

We do a traversal of our computational graph. We first visit every parent of the output, and add these as nodes to visit later (`nodequeue`). We then mark the current node as visited. We then pop elements from `nodequeue` and visit all of their parents, etc...

By starting from the output and updating the derivate of the output using the chain rule as we go, we can get the partial derivatives of the output with respect to the independent variables (the inputs). For instance, if: 

```python
x = Node(3)
y = Node(7)
z = x*y
f = z+x
```

Then:

<img src="https://latex.codecogs.com/svg.image?f=xy&plus;x&space;" title="f=xy+x " />

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f}{\partial&space;x}=y&plus;1&space;" title="\frac{\partial f}{\partial x}=y+1 " />

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f}{\partial&space;y}=x&space;" title="\frac{\partial f}{\partial y}=x " />

In our code, we start from f (the output is f). Its parents are z and x and we compute:

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f(z,x)}{\partial&space;x}=1&space;" title="\frac{\partial f(z,x)}{\partial x}=1 " />

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f(z,x)}{\partial&space;z}=1&space;" title="\frac{\partial f(z,x)}{\partial z}=1 " />

This is the first thing that would be computed using our reverse mode AD . Note that even though z is a function of f, here we take the partial derivatives of f with respect to z and x by seeing z as a variable of its own.

The parents of z are x and y. Thus we also compute:

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;z}{\partial&space;x}=y&space;" title="\frac{\partial z}{\partial x}=y " />

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;z}{\partial&space;y}=x&space;" title="\frac{\partial z}{\partial y}=x " />

Thus, the partial derivative of f with respect to the input x is:

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f}{\partial&space;x}=\frac{\partial&space;f(z,x)}{\partial&space;z}\frac{\partial&space;z}{\partial&space;x}&plus;\frac{\partial&space;f(z,x)}{\partial&space;x}=y&plus;1&space;" title="\frac{\partial f}{\partial x}=\frac{\partial f(z,x)}{\partial z}\frac{\partial z}{\partial x}+\frac{\partial f(z,x)}{\partial x}=y+1 " />

This is the last step of what's happening in our reverse mode example, as the parents of f are z and x, and we already have computed: 

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f(z,x)}{\partial&space;z}\frac{\partial&space;z}{\partial&space;x}&space;" title="\frac{\partial f(z,x)}{\partial z}\frac{\partial z}{\partial x} " />

and:

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f(z,x)}{\partial&space;x}&space;" title="\frac{\partial f(z,x)}{\partial x} " />

Likewise, the partial derivative of f with respect to the input y is:

<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;f}{\partial&space;y}=\frac{\partial&space;f(z,x)}{\partial&space;z}\frac{\partial&space;z}{\partial&space;y}=x&space;" title="\frac{\partial f}{\partial y}=\frac{\partial f(z,x)}{\partial z}\frac{\partial z}{\partial y}=x " />

Note that when we call `_backward ` on the output, we access the partial derivatives of the output with respect to the independent variables as follow:

```python
x=Node(2)
y=3
z=y*x
# z._value==3*2
# the partial derivative of z with respect to x is accessed as follows
# z._d[x]==3
w=np.exp(z)
# w._value==np.exp(3*2)
# the partial derivative of w with respect to z is accessed as follows
# w._d[z]==np.exp(3*2)
# REVERSE MODE AD
w._backward()
# z._df and x._df represent the derivatives of w wrt to z and x, respectively
assert z._df==np.exp(3*2)
assert x._df==3*np.exp(3*2)
```

We can then use the function `_clear_df` to clear those partial derivatives after `_backward`has been called. For example,

```python
x=Node(2)
y=3
z=y*x
# z._value==3*2
# the partial derivative of z with respect to x is accessed as follows
# z._d[x]==3
w=np.exp(z)
# w._value==np.exp(3*2)
# the partial derivative of w with respect to z is accessed as follows
# w._d[z]==np.exp(3*2)
f=np.cos(w)
# f._value==np.cos(np.exp(3*2))
# the partial derivative of f with respect to w is accessed as follows
# f._d[w]==-np.sin(np.exp(3*2))
# REVERSE MODE AD
f._backward()
# derivatives of f wrt to w
# w._df==-np.sin(np.exp(3*2))
# derivatives of f wrt to z
# z._df==-np.sin(np.exp(3*2))*np.exp(3*2)
# derivatives of f wrt to x
# x._df==-np.sin(np.exp(3*2))*np.exp(3*2)*3
f._clear_df()
# w._df==0
# z._df==0
# x._df==0
w._backward()
# derivatives of w wrt to z
# z._df==np.exp(3*2)
# derivatives of w wrt to x
# x._df==3*np.exp(3*2)
```

## Derivatives

The function `_derivative` computes the derivative of the variables from the class:`autodiff_107.Node` with respect to X, where both the variable and X are inputs of the function.

For example,

```python
x=Node(2)
y=3
z=y*x
# z._value==3*2
# partial derivative of z with respect to x
# z._d[x]==3
w=np.exp(z)
# derivative of w wrt to z
# w._derivative(z)==np.exp(3*2)
# derivative of w wrt to x
# w._derivative(x)==3*np.exp(3*2)
```

## Network Visualisation

We use the package NetworkX (https://networkx.org/).

We have three versions: `draw_graph_without_edge_labels`, `draw_graph` and `draw_graph_expensive`.The first one draws a graph, the other two draw a directed graph.

We start by building a graph (or a directed graph) and we add nodes to this graph (or directed graph) by first adding all the output nodes.

We then use the same idea as for reverse mode AD to traverse the graph. For every node already present, we look for its parents and add these as nodes to our graph. Instead of `self._d`, the dictionary of interest is `self._operation` which contains strings with the corresponding elementary operation expressed in word (we still need to add the trigonometric functions, the hyperbolic functions, and the inverse trigonometric functions and hyperbolic functions, along with the other bumpy functions we have overwritten). When we traverse the graph, every time we have a parent-children link, we add this edge to our graph (or we add a directed edge to out directed graph). We use the dictionary `self._operation` as a way to label or edges (or directed edges). 

<p align="justify">Depending on the function, we also colour the nodes following the convention: independent variables in red, dependent variables in blue and outputs in orange. This is as easy as checking that the in-degree is zero, that the in-degree and the out-degree are both positive, and that the out-degree is zero, respectively. </p>

# Extensions and future features

## Reverse mode AD

We have implemented reverse mode automatic differentiation. This is more efficient than forward mode for some functions (multivariate functions with one output, for example, and more generally, functions of the form:
<img src="https://latex.codecogs.com/svg.image?f:&space;\mathbb{R}^m&space;\rightarrow&space;\mathbb{R}" title="f: \mathbb{R}^m \rightarrow \mathbb{R}" />
it might also be true for functions of the form:
<img src="https://latex.codecogs.com/svg.image?f:&space;\mathbb{R}^m&space;\rightarrow&space;\mathbb{R}^n&space;" title="f: \mathbb{R}^m \rightarrow \mathbb{R}^n " />
depending on wether m>>n).

For functions of the form:
<img src="https://latex.codecogs.com/svg.image?f:&space;\mathbb{R}^m&space;\rightarrow&space;\mathbb{R}" title="f: \mathbb{R}^m \rightarrow \mathbb{R}" />
reverse mode AD is a two pass process, as opposed to the m-pass forward mode. Reverse mode computes the sensitivity with respect to the independent and intermediate variables. 

<p align="justify">Thus, compared to the forward mode, the reverse mode has a significantly smaller arithmetic operation count for functions of the form:</p>

<img src="https://latex.codecogs.com/svg.image?f:&space;\mathbb{R}^m&space;\rightarrow&space;\mathbb{R}" title="f: \mathbb{R}^m \rightarrow \mathbb{R}" />

<p align="justify"> if m is very large. Artificial neural networks have exactly this property: this is one of the reason we implemented reverse mode AD, as we want to train a neural network using our package! </p>

## Vector valued functions and more user-friendly interface

> This is not an extension, but a future feature.

We will make the interface more user friendly to be able to deal with multivariate, vector valued functions. We will have a proper Jacobian (and possibly Hessian) function(s) as, well as a gradient function.

## Training an Artificial Neural Network (ANN) using our package

We will train a neural network using our package. This will probably be a very small network, trained on MNIST. We will thus also implement the sigmoid function and the rely function.

## NetworkX visualisation


These private functions will be wrapped in user functions in a later milestone. 

<p align="justify">We use NetworkX to visualise the computational graph. This has already been implemented, but we commented it out for now as we need to fix a few details (add operations for cos, sin etc...). We have three versions. We will also need to make sure this works for functions of the form: </p>

<img src="https://latex.codecogs.com/svg.image?f:&space;\mathbb{R}^m&space;\rightarrow&space;\mathbb{R}^n&space;" title="f: \mathbb{R}^m \rightarrow \mathbb{R}^n " />

### Basic version

<p align="justify">So far, this version makes a graph where nodes are variables (independent and intermediate, plus the output). Edges between nodes represent parent-child relations. This is a "light" version, that is why it's so simple. But it can be just as light as a directed graph, so we will make our basic version a directed graph. </p>

Here is an example created the basic function, called draw_graph_without_edge_labels.

```python
x = Node(8)
y = Node(3)
z = Node(11)
w = Node(10)
f = x*x+y+z*x*w*x
draw_graph_without_edge_labels(np.array(f))
```

![](figs/Figure_3.png)

### Directed graph with colours

This is a bit better than the basic version: this is a directed graph, where edges point from parent to child. In addition, the independent variables are in red and the the intermediate variables are in blue. The output is in orange.

Here is an example of the directed graph created using draw_graph. Note that the layout is chosen by NetworkX.

```python
x = Node(8)
y = Node(3)
z = Node(11)
w = Node(10)
f = x*x+y+z*x*w*x
draw_graph(np.array(f))
```

![](figs/Figure_2.png)

### Full version

This is the same as the above, but we specify explicitly the layout of the nodes for clarity. All the independent variables, in red, have the same x-coordinate. All the output values, in orange, have the same x-coordinate.  All dependent variables, in blue, have x-coordinates comprised between the x-coordinate of the independent variables and the x-coordinate of the outputs. Right now, I've made it too complicated: it can be cleaner and will be updated in due course.

Here is an example of a directed graph created using draw_graph_expensive.

```python
x = Node(8)
y = Node(3)
z = Node(11)
w = Node(10)
f = x*x+y+z*x*w*x
draw_graph_expensive(np.array(f))
```

<p align="justify">This is the same as the above, but we specify explicitly the layout of the nodes for clarity. All the independent variables, in red, have the same x-coordinate. All the output values, in orange, have the same x-coordinate.  All dependent variables, in blue, have x-coordinates comprised between the x-coordinate of the independent variables and the x-coordinate of the outputs. Right now, I've made it too complicated: it can be cleaner and will be updated in due course. </p>

![](figs/Figure_1.png)


### Future direction for visualisation

<p align="justify">We will also add the tangent trace evaluation on the graph. We might also try to make nice visualisation as gifs. Furthermore, we could also create a table to show the independent and dependent variables along the tangent trace, as we have done in class. </p>

