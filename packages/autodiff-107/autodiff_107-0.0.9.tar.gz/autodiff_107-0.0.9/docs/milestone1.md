# Introduction

**Describe the problem the software solves and why it's important to solve that problem.**

<p align="justify">Automatic Differentiation is able to evaluate real-valued functions of one variable and their derivative exactly. For real-valued functions of more than one variable, AD evaluates the function and its gradient. For multivariable, vector-valued functions, AD evaluates the function and its Jacobian. By extension, AD is also able to evaluate higher order derivatives (and Hessians, etc…). This is an important problem as many algorithms use derivatives of functions (eg Newton method for root finding, BFGS,  gradient descent and stochastic gradient descent…). In particular, AD is intimately linked to backpropagation in Machine Learning (backprop is a special case of AD) which has enabled engineers to train Deep Neural Network to solve a very diverse set of tasks, from image classification to solving PDEs using NNs. Other methods to obtain derivatives of functions include numerical methods and symbolic differentiation, but they are not suitable for Machine Learning. </p>

# Background

**Describe (briefly) the mathematical background and concepts as you see fit. You do not need to give a treatise on automatic differentiation or dual numbers. Just give the essential ideas (e.g. the chain rule, the graph structure of calculations, elementary functions, etc).**

Consider a function of interest f. AD computes the evaluation of the function f and ots derivative at a given point. The key idea is to use the composition of simple functions (called elementary functions) to get to f.

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

# How to use autodiff_107

We currently intend on relying on packages included with python (e.g. math) and numpy. We hope to set up the dependencies in such a way that the user will be able to just 

```bash
pip install autodiff_107
```

and the correct dependencies will just be installed.

For the end user, they should be able to just run 

```python
import autodiff_107 as ad
```

<p align="justify"> and our package will work as intended. Regardless of the dependencies of our package, we do not expect the user to have to import anything else to make any functions of our library work. This is annoying for users when certain functions require an extra import so we will avoid this. </p>

## Doing Math with Automatic Differentiation

To actually get the benefits of AD in our package, users will have to wrap their variables with the ```Var``` object. Operations for the functions the user wants to use will have to be done using these variable objects. Constants involved in the function can be inserted normally and do not need to be wrapped in ```Var``` objects.



Example:

```python
x = ad.Var(10)
y = ad.Var(17)

z = (x + y)**2 - 14
```

Because we are implementing reverse mode, the user needs to choose which value they want to calculate the gradient with respect to. We offer the ```ad.derivative(result, inputs)``` function. The user can pass in the result of their function, as well as the inputs they want the derivatives with respect to, and the function will return a list of derivatives for the inputs presented. Either `result`, `inputs`, or both can be lists of `Var` objects. Depending on the dimensions of these arguments, the result may be scalar, a vector, or a Jacobian matrix. 

Example (continued from above)

```python
ad.derivative(z, [x,y])
# The following also works
ad.derivative(z, x)
```

# Software Organization

```
cs107-FinalProject/
├── docs
│	└── ...
├── autodiff_107
│	└── __init__.py
│	└──	Node.py
│	└──	nodemath.py
│	└──	userfunctions.py
│	└── tests
│		└── ...
├── LICENSE
├── README.md
```

We plan on having one module with the same name as our package (autodiff_107). This module will include all the functionality required for automatic differentiation. Because we need math to work with our `Node` objects, this math functionality will also be included in this module.

`Node.py` will implement the nodes in our computational graph.

`nodemath.py` will implement the different mathematical functions we need to overload to work with our `Node`s

`userfunctions.py` will be any functions that operate on `Var`s that the user may want to use (e.g. `ad.derivative(result, inputs)`) that operate on Nodes but are not overloaded mathematical operators.

### Testing

Our test suite will live in the `autodiff_107/tests` folder and these tests will be run by TravisCI. We will most likely also use CodeCov to track test coverage.

### Distribution

Our package will be distributed on PyPi which is why we are currently using a name that isn't the prettiest of all time in the hopes that its not already in use.

# Implementation

The core data structure for our library will be a  `Node`. `Node`s will make up the computational graph that we will traverse for forward and backward passes of reverse mode. These are the same as `Var`s but we give them a different name that is more intuitive for users. They each have a value, a parents list, and a derivative with respect to each parent. 

`Node`s will have overloaded operators such that when they are used in a computation, new nodes are created for the result of the operation, and the resulting:

<a href="https://www.codecogs.com/eqnedit.php?latex=\dfrac{\partial&space;v_j}{\partial&space;v_i}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\dfrac{\partial&space;v_j}{\partial&space;v_i}" title="\dfrac{\partial v_j}{\partial v_i}" /></a>

are stored for each intermediate node. The result of a function is returned as one node that is the descendant of all of the inputs used in that computation.

`Node`s will look something like

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.parents = []
        self.d = dict()
        
    def __add__(self, other):
        result = Node(self.value + other.value)
        result.d[self] = 1
        result.d[other] = 1
        
    .....
```

We store derivatives as a dictionary because we need to store the derivative with respect to each parent

We will have to implement new versions of operators like cos, exp, etc. that operate on Nodes. These will also handle setting derivatives. We will depend mostly on the built in math library for these, but may turn to numpy if the need arises.

We will also have a `derivative(result, inputs)` function that will handle actually calling the backward pass on results, and calculating the derivatives of the result with respect to the inputs. We will allow both result and inputs to be either scalar or an array of `Var`s. The shape/dimension of the result will depend on the shapes of the inputs but could either be a scalar derivative, or a Jacobian in which case it will be returned as a numpy array. We aren't planning on explicitly handling variables that are vectors, but our library will support any number of inputs and outputs and will therefore handle functions of:

<a href="https://www.codecogs.com/eqnedit.php?latex=\mathbb&space;R^n&space;\rightarrow&space;\mathbb&space;R^m" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathbb&space;R^n&space;\rightarrow&space;\mathbb&space;R^m" title="\mathbb R^n \rightarrow \mathbb R^m" /></a>

Because we are only planning on using numpy to store the Jacobians here, we may simply omit the dependency and use simple 2D arrays. This is a decision we will have to make when we are closer to that point in implementation and have a better idea of the trade-offs and how much we rely on numpy in other places.

# Licensing

**Licensing is an essential consideration when you create new software. You should choose a suitable license for your project. A comprehensive list of licenses can be found here. The license you choose depends on factors such as what other software or libraries do you use in your code (copyleft, copyright), will you have to deal with patents, how can others advertise software that makes use of your code (or parts thereof)?**

<p align="justify">We will use the MIT license. It puts very few limitations on what can be done with the code (copy, modify, publish, distribute and even sell) and is compatible with many GNU General Public Licenses. The conditions only require preservations of copyright and license notices. Our License can be found in the LICENSE file. </p>

# Feedback

## Milestone 1

### Feeback received

#### Introduction: 

great Introduction, I like the way you bring AD. 

#### Background: 
I really love your Background, I understand what is at stake and how you are going to leverage the differentiation properties in order to simplify the differentiation of big and cool functions. 

#### How to use: 

Very clear, I like the way you thought through such detailed use cases in order to apprehend everything.  

#### Implementation: 

well done, I think your understanding of the problem is complete. 

You should not push directly code to the main branch; Use Pull requests. Also, you might want to make sure that the mardown renders well in your submissions.

### Step to adress the feedback

#### Changed the latex equations using https://www.codecogs.com/
#### Working on a branch for the milestone






