Usage
=====

.. _installation:

Installation
------------

To use **autodiff_107** first clone the repository from github

.. code-block:: console

    $ git clone https://github.com/cs107-errajexi/cs107-FinalProject

Create a virtual environment, for example *autodiff_107-env*, but you are free to name it as you wish!

.. code-block:: console

    $ python3 -m venv /path/to/autodiff_107-env

Activate it!

.. code-block:: console

    $ source autodiff_107-env/bin/activate

Install the requirements using pip:

.. code-block:: console

    $ pip install -r requirements.txt

Congrats! You are now all set to use the package.

.. _getting_started:

Getting Started
---------------

.. note::
   This tutorial is valid until the package will be published. Currenlty only the working backend is implemented. User friendly wrappers and functions will be implemented at a later stage.

Importing the package

.. code-block:: python3

    import autodiff_107 as ad

To actually get the benefits of AD in our package, users will wrap their variables with the **Node** object. Operations for the functions the user wants to use will have to be done using this object. Constants involved in the function can be inserted normally and do not need to be wrapped in **Node** objects.

Example:

.. code-block:: python3

    x = ad.Node(10)
    y = ad.Node(17)
    z = (x + y)**2 - 14

This package handily integrates all numpy functions that the user can call with the commonly used ``np`` alias:

.. code-block:: python3

    from autodiff_107.nodemath import numpy as np

    x=ad.Node(2)
    z=3*x
    w=np.exp(z)
    f=np.cos(w)

Taking derivatives and partial derivatives:

.. code-block:: python3

    f._derivative(x)
    w._derivative(z)

Example: **Newton Root Finding**

.. code-block:: python3

    def newton(f, x0, tol):
    xn = ad.Node(x0)
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