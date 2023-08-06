Usage
=====

.. _installation:

Installation
------------

Create a virtual environment, for example *autodiff_107-env*, but you are free to name it as you wish!

.. code-block:: console

    $ python3 -m venv /path/to/autodiff_107-env

Activate it!

.. code-block:: console

    $ source autodiff_107-env/bin/activate

pip install **autodiff_107**

.. code-block:: console

    $ pip install autodiff_107
   
Congrats! You are now all set to use the package.

.. _getting_started:

Getting Started
---------------

Importing the package

.. code-block:: python3

    import autodiff_107 as ad

To actually get the benefits of AD in our package, users will wrap their variables with the ```variable``` method. Operations for the functions the user wants to use will have to be done using this object. Constants involved in the function can be inserted normally and do not need to be wrapped.

Example:

.. code-block:: python3

    from autodiff_107.diff import variable as var
    x = var(10)
    y = var(17)
    z = (x + y)**2 - 14

This package handily integrates all numpy functions that the user can call with the commonly used ``np`` alias:

.. code-block:: python3

    from autodiff_107.diff import numpy as np
    x=var(2)
    z=3*x
    w=np.exp(z)
    f=np.cos(w)

Taking derivatives

.. code-block:: python3

    x = var(3)
    f = lambda x: 3*x+4
    df = derivative(f(x), x)

Example: **Gradient Descent**

.. code-block:: python3

    x0 = [1, 2]
	f = lambda x: x[0]**2 + x[1]**2 + 3
	alpha=.1
	max_iter=1000
	x_min = gradient_descent(f, x0, alpha, max_iter)