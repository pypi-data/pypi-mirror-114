.. image:: https://travis-ci.com/albertotonda/HumanModels.svg?branch=main
    :target: https://travis-ci.com/albertotonda/HumanModels

.. image:: https://readthedocs.org/projects/humanmodels/badge/?version=latest
    :target: https://humanmodels.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/humanmodels.svg
    :target: https://badge.fury.io/py/humanmodels

.. image:: https://raw.githubusercontent.com/albertotonda/HumanModels/main/img/hm.jpg
  :width: 400
  :alt: HumanModels logo
  
Human Models
============
.. inclusion-marker-for-sphinx-documentation

This package provides human-designed, scikit-learn compatible models for
classification and regression. ``humanmodels`` are initialized through a
sympy-compatible text string, describing an equation (e.g. "y = 4\ *x +
3*\ z\*\*2 + p\_0") or a rule for classification that must return True
or False (e.g. "x > 2\*y + 2"). If the string contains parameters not
corresponding to problem variables, the parameters of the model are
optimized on training data, using the ``.fit(X,y)`` method.

The objective of HumanModels is to provide a scikit-learn integrated way
of comparing human-designed models to machine learning models.

Installing the package
----------------------

On Linux, HumanModels can be installed through pip:

::

    pip install humanmodels

You can also install the package by cloning or downloading this repository, ``cd`` into the directory and then execute:

::

    python -m build
    python -m pip install dist/humanmodels*whl

On Windows, HumanModels can be installed through the Anaconda Prompt:

::

    pip install humanmodels

Examples
--------

HumanRegressor
~~~~~~~~~~~~~~

``HumanRegressor`` is a regressor, initialized with a sympy-compatible
text string describing an equation, and a dictionary mapping the
correspondance between the variables named in the equation and the
features in ``X``. Let's generate some data to test the algorithm:

.. code:: python

    import numpy as np
    print("Creating data...")
    X_train = np.zeros((100,3))
    X_train[:,0] = np.linspace(0, 1, 100)
    X_train[:,1] = np.random.rand(100)
    X_train[:,2] = np.linspace(0, 1, 100)
    y_train = np.array([0.5 + 1*x[0] + 1*x[2] + 2*x[0]**2 + 2*x[2]**2 for x in X_train])

An example of initialization:

.. code:: python

    from humanmodels import HumanRegressor
    model_string = "y = 0.5 + a_1*x + a_2*z + a_3*x**2 + a_4*z**2"
    variables_to_features = {"x": 0, "z": 2}
    regressor = HumanRegressor(model_string, variables_to_features)
    print(regressor)

Printing the model as a string will return:

::

   Model not initialized, call '.fit(X, y)' 

We can now fit the model to the data: 

.. code:: python

    print("Fitting data...")
    regressor.fit(X_train, y_train)
    print(regressor)

The code will produce:

::

    Fitting data...
    Model: y = a_1*x + a_2*z + a_3*x**2 + a_4*z**2 + 0.5
    Variables: ['x', 'z']
    Parameters: {'a_1': 1.0000001886557832, 'a_2': 1.0000004533354703, 'a_3': 2.000000577731051, 'a_4': 2.0000005553527895}
    Trained model: y = 2.0*x**2 + 1.0*x + 2.0*z**2 + 1.0*z + 0.5

As the only variables provided in the ``variables_to_features``
dictionary are named ``x``, and ``z``, all other alphabetic symbols
(``a_1``, ``a_2``, ``a_3``, ``a_4``) are interpreted as trainable
parameters. The model also shows the optimized values of its parameters.
Let's now check the performance on the training data:

.. code:: python

    y_pred = regressor.predict(X_train)
    from sklearn.metrics import mean_squared_error
    print("Mean squared error:", mean_squared_error(y_train, y_pred))

::

    Mean squared error: 7.72490931190691e-13

The regressor can also be tested on unseen data, and since in this case
the equation used to generate the data has the same structure as the one
given to the regressor, the generalization is of course satisfying:

.. code:: python

    X_test = np.zeros((100,3))
    X_test[:,0] = np.linspace(1, 2, 100)
    X_test[:,1] = np.random.rand(100)
    X_test[:,2] = np.linspace(1, 2, 100)
    y_test = np.array([0.5 + 1*x[0] + 1*x[2] + 2*x[0]**2 + 2*x[2]**2 for x in X_test])
    y_pred = regressor.predict(X_test)
    print("Mean squared error on test:", mean_squared_error(y_test, y_pred))

::

    Mean squared error on test: 1.2055817248044523e-11

HumanClassifier
~~~~~~~~~~~~~~~

``HumanClassifier`` also takes in input a sympy-compatible string (or
dictionary of strings), defining a logic expression that can be
evaluated to return ``True`` or ``False``. If only one string is
provided during initialization, the problem is assumed to be binary
classification, with ``True`` corresponding to Class 0 and ``False``
corresponding to Class 1. Let's test it on the classic ``Iris``
benchmark provided in ``scikit-learn``, transformed into a binary
classification problem.

.. code:: python

    from sklearn import datasets
    X, y = datasets.load_iris(return_X_y=True)
    for i in range(0, y.shape[0]) : if y[i] != 0 : y[i] = 1

    from humanmodels import HumanClassifier
    rule = "(sl < 6.0) & (sw > 2.7)"
    variables_to_features = {"sl": 0, "sw": 1}
    classifier = HumanClassifier(rule, variables_to_features)
    print(classifier)

::

    Model not initialized, call '.fit(X, y)' 

Even if there are no trainable parameters, the classifier must still be trained using ``.fit(X,y)``,
for compatibility with the ``scikit-learn`` package:

.. code:: python
    
   classifier.fit(X, y)
   print(classifier)

::

    Classifier: Class 0: (sw > 2.7) & (sl < 6.0); variables: sl -> 0 sw -> 1; parameters: None
    Default class (if all other expressions are False): 1

And now, let's test the classifier:

.. code:: python

    y_pred = classifier.predict(X)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y, y_pred)
    print("Final accuracy for the classifier is %.4f" % accuracy)

::

    Final accuracy for the classifier is 0.9067

For multi-class classification problems, ``HumanClassifier`` can accept
a dictionary of logic expressions in the form
``{label0 : "expression0", label1 : "expression1", ...}``. As for
``HumanRegressor``, expression can also have trainable parameters,
optimized when ``.fit(X,y)`` is called. Let's see an another example
with ``Iris``, this time using all three classes:

.. code:: python

    X, y = datasets.load_iris(return_X_y=True)
    rules =     {0: "sw + p_0*sl > p_1",
            2: "pw > p_2",
            1: ""}  # this means that a sample will be associated to class 1 if both
                    # the expression for class 0 and 2 return 'False'
    variables_to_features = {'sl': 0, 'sw': 1, 'pw': 3}
    classifier = HumanClassifier(rules, variables_to_features)

    classifier.fit(X, y)
    print(classifier)
    y_pred = classifier.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print("Classification accuracy: %.4f" % accuracy)

::

    Class 0: p_0*sl + sw > p_1; variables:sl -> 0 sw -> 1; parameters:p_0=-0.6491880968641275 p_1=-0.12490468490418744
    Class 2: pw > p_2; variables:pw -> 3; parameters:p_2=1.7073348596674072
    Default class (if all other expressions are False): 1
    Classification accuracy: 0.9400

Depends on
----------

numpy (for fast computations)

sympy (for symbolic mathematics)

scipy (for optimization)

cma (also for optimization of non-convex functions)

scikit-learn (for quality metrics, such as accuracy and mean squared
error; also, HumanClassifier and HumanRegressor have the ambition of
being compatible with scikit-learn estimators)

.. |#f03c15| image:: https://via.placeholder.com/15/f03c15/000000?text=+
