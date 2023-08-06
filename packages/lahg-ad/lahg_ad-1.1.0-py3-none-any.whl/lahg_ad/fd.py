#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the Variable class for performing forward mode automatic differentiation.
It also contains function for making scalar/vector inputs.
"""

import numpy as np


class Variable:
    """
    This is the Variable class with basic methods and operation overloading.
    It is used to perform forward mode automatic differentiation for scalar/vector input of scalar function.

    EXAMPLES
    ========
    # scalar input
    >>> x = Variable(6, 1)
    >>> f = 15 / (x * 3 + 10)
    >>> print(f)
    value = 0.5357142857142857, derivative = -0.05739795918367347

    # vector input
    >>> import numpy as np
    >>> x = Variable(5, np.array([1, 4]))
    >>> y = Variable(7, np.array([3, 1]))
    >>> f = np.cos(x*y) + x * y + 3*np.log(x)
    >>> print(f)
    value = 36.19321780791655, derivative = [31.68059542 48.17233485]
    """

    def __init__(self, value, derivative_seed=1):
        """
        Variable class constructor

        INPUTS
        ------
        value : int or float
            Give the value of the variable
        derivative_seed : int or float, optional
            Give the derivative seed of the variable. The default is 1.

        EXAMPLES
        --------
        >>> x = Variable(2, 1)
        >>> print(x)
        value = 2, derivative = 1

        >>> import numpy as np
        >>> x = Variable(np.array([5, 6]), np.array([6, 2]))
        >>> print(x)
        value = [5 6], derivative = [6 2]
        """
        # check type for value and derivative_seed
        if not isinstance(value, (int, float, np.ndarray)) or not isinstance(derivative_seed, (int, float, np.ndarray)):
            raise Exception("The value and derivative seed must be int, float, or np.ndarray")
        
        # if value is numpy array, the derivative seed must be a numpy array as well
        if isinstance(value, np.ndarray):
            if not isinstance(derivative_seed, np.ndarray):
                raise Exception("value array has different length with derivative array")
            elif len(value) != len(derivative_seed):
                raise Exception("value array has different length with derivative array")

        if isinstance(value, np.ndarray) or isinstance(derivative_seed, np.ndarray):
            try:
                if isinstance(value, np.ndarray):
                    # Check to see whether value can be converted to float
                    value.astype(float)
                if isinstance(derivative_seed, np.ndarray):
                    # Check to see whether derivative can be converted to float
                    derivative_seed.astype(float)
                self.val = value
                self.der = derivative_seed
            except ValueError:
                raise ValueError(
                    "Not all elements in the value numpy array are int or float"
                )
        elif isinstance(value, (int, float)) and isinstance(
            derivative_seed, (int, float)
        ):
            try:
                self.val = value
                self.der = derivative_seed
            except TypeError:
                raise TypeError(
                    "Type of value and derivative seed must be int or float!"
                )
        else:
            raise TypeError("Type of value and derivative seed must be int or float!")

    def __repr__(self):
        """
        Dunder method for printing output

        INPUTS
        ------
        None

        RETURNS
        -------
        The attributes of the Variable object

        EXAMPLES
        --------
        >>> x = Variable(2, 1)
        >>> print(x)
        value = 2, derivative = 1

        >>> import numpy as np
        >>> x = Variable(np.array([5, 6]), np.array([6, 2]))
        >>> print(x)
        value = [5 6], derivative = [6 2]
        """

        return f"value = {self.val}, derivative = {self.der}"

    def get_value(self):
        """
        Method for getting the value of a Variable object

        INPUTS
        ------
        None

        RETURNS
        -------
        int or float
            give the value of a Variable object.

        EXAMPlES
        --------
        >>> x = Variable(2, 1)
        >>> print(x.get_value())
        2

        >>> import numpy as np
        >>> x = Variable(np.array([2, 1]), np.array([3, 3]))
        >>> print(x.get_value())
        [2 1]
        """

        return self.val

    def get_derivative(self):
        """
        Method for getting the value of a Variable object

        INPUTS
        ------
        None

        RETURNS
        -------
        int or float
            give the derivative of a Variable object.

        EXAMPLES
        --------
        >>> x = Variable(2, 1)
        >>> print(x.get_derivative())
        1

        >>> import numpy as np
        >>> x = Variable(3, np.array([2, 1]))
        >>> print(x.get_derivative())
        [2 1]

        """
        return self.der

    def __neg__(self):
        """
        Method for taking negative (-) of a Variable object

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object

        EXAMPLES:
        --------
        >>> x = Variable(2, 7)
        >>> print(- x)
        value = -2, derivative = -7

        >>> import numpy as np
        >>> x = Variable(np.array([2, 7]), np.array([8, 7]))
        >>> print(- x)
        value = [-2 -7], derivative = [-8 -7]
        """

        value = -self.val
        derivative = -self.der
        return Variable(value, derivative)

    def sin(self):
        """
        Value and derivative computation of sin function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the sin function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(5, 1)
        >>> f = x.sin()
        >>> print(f)
        value = -0.9589242746631385, derivative = 0.2836621854632263

        >>> import numpy as np
        >>> x = Variable(np.array([np.pi/2, np.pi/2]), np.array([0, 0]))
        >>> f = x.sin()
        >>> print(f)
        value = [1. 1.], derivative = [0. 0.]
        """

        value = np.sin(self.val)
        derivative = np.cos(self.val) * self.der
        return Variable(value, derivative)

    def cos(self):
        """
        Value and derivative computation of cos function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the cos function.

        EXAMPLES
        --------
        >>> x = Variable(5, 2)
        >>> f = x.cos()
        >>> print(f)
        value = 0.2836621854632263, derivative = 1.917848549326277

        >>> import numpy as np
        >>> x = Variable(np.array([0, 0]), np.array([np.pi/2, np.pi/2]))
        >>> f = x.cos()
        >>> print(f)
        value = [1. 1.], derivative = [-0. -0.]
        """

        value = np.cos(self.val)
        derivative = (-1) * np.sin(self.val) * self.der
        return Variable(value, derivative)

    def tan(self):
        """
        Value and derivative computation of tan function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the tan function.

        NOTES
        -----
        The function tan doesn't exist at odd multiple of pi/2, however, due to machine precision, the input will
        never be exactly equal to odd multiple of pi/2. Therefore no ValueError will be raised.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(np.pi, 1)
        >>> f = x.tan()
        >>> print(f)
        value = -1.2246467991473532e-16, derivative = 1.0

        >>> import numpy as np
        >>> x = Variable(np.array([np.pi/4, 0]), np.array([0, 1]))
        >>> f = x.tan()
        >>> print(f)
        value = [1. 0.], derivative = [0. 1.]
        """

        value = np.tan(self.val)
        derivative = (1 / (np.cos(self.val) ** 2)) * self.der
        return Variable(value, derivative)

    def arcsin(self):
        """
        Value and derivative computation of arcsin function

        INPUTS
        ------
        None

        RAISES
        ------
        ValueError
            When the input value is larger than 1 or smaller than -1.

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the arcsin function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(0.5, 1)
        >>> f = x.arcsin()
        >>> print(f)
        value = 0.5235987755982988, derivative = 1.1547005383792517

        >>> import numpy as np
        >>> x = Variable(np.array([0.31059631345545935, 0.4060878077968675]), np.array([0.6009880861257652, 0.45357678626893605]))
        >>> f = x.arcsin()
        >>> print(f)
        value = [0.31582031 0.41816889], derivative = [0.63225838 0.4963448 ]
        """

        if isinstance(self.val, np.ndarray):
            if not (np.absolute(self.val) < 1).all():
                raise ValueError(f"arcsin doesn't exist at {self.val}")
        elif abs(self.val) >= 1:
            raise ValueError(f"arcsin doesn't exist at {self.val}")
        value = np.arcsin(self.val)
        derivative = 1 / np.sqrt(1 - self.val ** 2) * self.der
        return Variable(value, derivative)

    def arccos(self):
        """
        Value and derivative computation of arccos function

        INPUTS
        ------
        None

        RAISES
        ------
        ValueError
            When the input value is larger than 1 or samller than -1.

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the arccos function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(0.5, 1)
        >>> f = x.arccos()
        >>> print(f)
        value = 1.0471975511965976, derivative = -1.1547005383792517

        >>> import numpy as np
        >>> x = Variable(np.array([0.1909541009109912, 0.008621310230472745]), np.array([0.44260489479900333, 0.9877402928856399]))
        >>> f = x.arccos()
        >>> print(f)
        value = [1.37866229 1.56217491], derivative = [-0.45090196 -0.987777  ]
        """

        if isinstance(self.val, np.ndarray):
            if not (abs(self.val) < 1).all():
                raise ValueError(f"arccos doesn't exist at {self.val}")
        elif abs(self.val) >= 1:
            raise ValueError(f"arccos doesn't exist at {self.val}")
        value = np.arccos(self.val)
        derivative = -1 / np.sqrt(1 - self.val ** 2) * self.der
        return Variable(value, derivative)

    def arctan(self):
        """
        Value and derivative computation of arctan function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the arctan function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(2, 1)
        >>> f = x.arctan()
        >>> print(f)
        value = 1.1071487177940906, derivative = 0.2

        >>> import numpy as np
        >>> x = Variable(np.array([0.9282013587973279, 0.31536005198518047]), np.array([0.11859177022622125, 0.343703622628477]))
        >>> f = x.arctan()
        >>> print(f)
        value = [0.74817929 0.30548834], derivative = [0.06370566 0.31261359]
        """

        value = np.arctan(self.val)
        derivative = 1 / (1 + self.val ** 2) * self.der
        return Variable(value, derivative)

    def sinh(self):
        """
        Value and derivative computation of sinh function

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        >>> x = Variable(2, 5)
        >>> f = x.sinh()
        >>> print(f)
        value = 3.6268604078470186, derivative = 18.81097845541816

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> f = x.sinh()
        >>> print(f)
        value = [1.17520119 3.62686041], derivative = [ 4.6292419  15.04878276]
        """

        val = np.sinh(self.val)
        der = np.cosh(self.val) * self.der
        return Variable(val, der)

    def cosh(self):
        """
        Value and derivative computation of cosh function

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        >>> x = Variable(6, 1)
        >>> f = x.cosh()
        >>> print(f)
        value = 201.7156361224559, derivative = 201.71315737027922

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> f = x.cosh()
        >>> print(f)
        value = [1.54308063 3.76219569], derivative = [ 3.52560358 14.50744163]
        """

        val = np.cosh(self.val)
        der = np.sinh(self.val) * self.der
        return Variable(val, der)

    def tanh(self):
        """
        Value and derivative computation of tanh function

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        >>> x = Variable(2, 1)
        >>> f = x.tanh()
        >>> print(f)
        value = 0.9640275800758169, derivative = 0.07065082485316447

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> f = x.tanh()
        >>> print(f)
        value = [0.76159416 0.96402758], derivative = [1.25992302 0.2826033 ]
        """

        val = np.tanh(self.val)
        der = (1 / (np.cosh(self.val) ** 2)) * self.der
        return Variable(val, der)

    def exp(self, base=None):
        """
        Value and derivative computation of exp function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the exp function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(5, 2)
        >>> f = x.exp()
        >>> print(f)
        value = 148.4131591025766, derivative = 296.8263182051532

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> f = x.exp()
        >>> print(f)
        value = [2.71828183 7.3890561 ], derivative = [ 8.15484549 29.5562244 ]

        >>> x = Variable(np.array([1, 2, 3]), np.array([1, 1, 1]))
        >>> f = x.exp(base = 2)
        >>> print(f)
        value = [2 4 8], derivative = [1.38629436 2.77258872 5.54517744]

        """
        if base == None:
            value = np.exp(self.val)
            derivative = np.exp(self.val) * self.der
            return Variable(value, derivative)
        elif isinstance(base, (int, float)):
            return self.__rpow__(base)
        else:
            raise ValueError("Exponential base must be int or float !")

    def __eq__(self, other):
        """
        Method for checking if two Variable objects are equal, overloads ==

        INPUTS
        ------
        other : A Variable object

        RETURNS
        -------
        bool
            if the values and derivatives of them are equal, it returns True, otherwise it returns False.

        EXAMPLES
        --------
        >>> x = Variable(3, 5)
        >>> y = Variable(3, 5)
        >>> x == y
        True

        >>> x = Variable(3, 5)
        >>> y = Variable(3, 6)
        >>> x == y
        False

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> y = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> x == y
        True

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> y = Variable(np.array([3, 2]), np.array([3, 4]))
        >>> x == y
        False
        """
        try:
            val_equal = False
            der_equal = False

            if isinstance(self.val, np.ndarray) or isinstance(other.val, np.ndarray):
                if np.array_equal(self.val, other.val):
                    val_equal = True
                else:
                    return False
            else:
                if self.val == other.val:
                    val_equal = True
                else:
                    return False
            if isinstance(self.der, np.ndarray) or isinstance(other.der, np.ndarray):
                if np.array_equal(self.der, other.der):
                    der_equal = True
                else:
                    return False
            else:
                if self.der == other.der:
                    der_equal = True
                else:
                    return False

            if val_equal and der_equal:
                return True
            else:
                return False
        except:
            return False

    def __ne__(self, other):
        """
        Method for checking if two Variable objects are not equal, overloads !=

        INPUTS
        ------
        other : A Variable object

        RETURNS
        -------
        bool
            if the values and derivatives of them are equal, it returns False, otherwise it returns True.

        EXAMPLES:
        --------
        >>> x = Variable(3, 5)
        >>> y = Variable(3, 5)
        >>> x != y
        False

        >>> import numpy as np
        >>> x = Variable(np.array([1, 2]), np.array([1, 2]))
        >>> y = Variable(np.array([1, 2]), np.array([3, 4]))
        >>> x != y
        True
        """

        try:
            if (self.val == other.val) and (self.der == other.der):
                return False
            else:
                return True
        except:
            return True

    def __add__(self, other):
        """
        Method for adding two quantities, overloads +

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object
            This Variable object has the sum of the value and derivative of the two Variable objects.

        EXAMPLES
        --------
        # addition of two Variable objects
        >>> x = Variable(5, 2)
        >>> y = Variable(4, 4)
        >>> f = x + y
        >>> print(f)
        value = 9, derivative = 6

        # addition of one Variable object and a real number
        >>> x = Variable(5, 1)
        >>> y = 10
        >>> f = x + y
        >>> print(f)
        value = 15, derivative = 1

        # addition of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,2]))
        >>> y = Variable(np.array([2,2]), np.array([3,3]))
        >>> f = x + y
        >>> print(f)
        value = [3 4], derivative = [6 5]

        # addition of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([1,2]))
        >>> y = 1
        >>> f = x + y
        >>> print(f)
        value = [2 3], derivative = [1 2]
        """

        try:
            new_val = self.val + other.val
            new_der = self.der + other.der
            return Variable(new_val, new_der)
        except AttributeError:
            new_val = self.val + other
            new_der = self.der
            return Variable(new_val, new_der)

    def __sub__(self, other):
        """
        Method for subtracting one quantity from another, overloads -

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object
            This Variable object has the difference of the value and derivative of the two Variable objects.

        EXAMPLES
        --------
        # subtraction of two Variable objects
        >>> x = Variable(5, 6)
        >>> y = Variable(4, 4)
        >>> f = x - y
        >>> print(f)
        value = 1, derivative = 2

        # subtraction of one Variable object and a real number
        >>> x = Variable(5, 1)
        >>> y = 5
        >>> f = x - y
        >>> print(f)
        value = 0, derivative = 1

        # subtraction of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,2]))
        >>> y = Variable(np.array([2,2]), np.array([3,3]))
        >>> f = x - y
        >>> print(f)
        value = [-1  0], derivative = [ 0 -1]

        # subtraction of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([1,2]))
        >>> y = 1
        >>> f = x - y
        >>> print(f)
        value = [0 1], derivative = [1 2]
        """

        try:
            new_val = self.val - other.val
            new_der = self.der - other.der
            return Variable(new_val, new_der)
        except AttributeError:
            new_val = self.val - other
            new_der = self.der
            return Variable(new_val, new_der)

    def __mul__(self, other):
        """
        Method for multiplying two quantities, overloads *

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object
            This Variable object has the product of the value and derivative of the two Variable objects.

        EXAMPLES
        --------
        # multiplication of two Variable objects
        >>> x = Variable(5, 6)
        >>> y = Variable(4, 4)
        >>> f = x * y
        >>> print(f)
        value = 20, derivative = 44

        # multiplication of a Variable object and a real number
        >>> x = Variable(5, 6)
        >>> y = 10
        >>> f = x * y
        >>> print(f)
        value = 50, derivative = 60

        # test multiplication of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = Variable(np.array([2,2]), np.array([2,2]))
        >>> f = x * y
        >>> print(f)
        value = [2 4], derivative = [ 8 12]

        # test multiplication of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([6,8]))
        >>> y = 2
        >>> f = x * y
        >>> print(f)
        value = [2 4], derivative = [12 16]
        """

        try:
            new_val = self.val * other.val
            new_der = self.val * other.der + other.val * self.der
            return Variable(new_val, new_der)
        except AttributeError:
            new_val = self.val * other
            new_der = self.der * other
            return Variable(new_val, new_der)

    def __truediv__(self, other):
        """
        method for division of two quantities, overloads /

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object
            This Variable object has the quotient of the value and derivative of the two Variable objects.

        EXAMPLES
        --------
        # test division of two Variable object
        >>> import numpy as np
        >>> x = Variable(5, 6)
        >>> y = Variable(5, 4)
        >>> f = x / y
        >>> print(f)
        value = 1.0, derivative = 0.4

        # test division of a Variable object and a real number
        >>> import numpy as np
        >>> x = Variable(5, 6)
        >>> y = 5
        >>> f = x / y
        >>> print(f)
        value = 1.0, derivative = 1.2

        # test division of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = Variable(np.array([2,2]), np.array([5,6]))
        >>> f = x / y
        >>> print(f)
        value = [0.5 1. ], derivative = [ 0.25 -1.  ]

        # test division of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = 2
        >>> f = x / y
        >>> print(f)
        value = [0.5 1. ], derivative = [1.5 2. ]
        """

        try:
            if isinstance(other.val, np.ndarray):
                if (other.val == 0).any():
                    raise ZeroDivisionError("Cannot divide by zero!")
            elif other.val == 0:
                raise ZeroDivisionError("Cannot divide by zero!")
            new_val = self.val / other.val
            new_der = (self.der * other.val - self.val * other.der) / (other.val ** 2)
            return Variable(new_val, new_der)
        except AttributeError:
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero!")
            new_val = self.val / other
            new_der = self.der / other
            return Variable(new_val, new_der)

    def __pow__(self, other):

        """
        Method for raising one quantity to the power of another, overloads **

        INPUTS
        ------
        other : a real number

        RAISES
        ------
        TypeError
            When other is a non-real number input
        ValueError
            When trying to raise a negative number to a fraction of a power (ex. (-2)**.2)


        RETURNS
        -------
        A Variable object
            This Variable object has the value raised to the power specified and new derivative.

        EXAMPLES
        --------
        # Raising a Variable object to the power of a positive int
        >>> x = Variable(5, 1)
        >>> y = 2
        >>> f = x ** y
        >>> print(f)
        value = 25, derivative = 10

        # Raising a Variable object to the power of a negative float
        >>> x = Variable(5, 1)
        >>> y = -2.5
        >>> f = x ** y
        >>> print(f)
        value = 0.01788854381999832, derivative = -0.00894427190999916

        # Raising a Variable object with vector input to the power of a positive int
        >>> import numpy as np
        >>> x = Variable(np.array([0,2]), np.array([5,6]))
        >>> y = 2
        >>> f = x ** y
        >>> print(f)
        value = [0 4], derivative = [ 0 24]

        # Raising a Variable object with vector input to the power of a negative float
        >>> import numpy as np
        >>> x = Variable(np.array(np.array([5,2]), np.array([5,6]))
        >>> y = -3.5
        >>> f = x ** y
        >>> print(f)
        value = [0.00357771 0.08838835], derivative = [-0.01252198 -0.92807765]

        # Raising a Variable object with vector input to the power of another Variable object with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([3,2]), np.array([5,6]))
        >>> y = Variable(np.array([2,1]), np.array([1,2]))
        >>> f = x ** y
        >>> print(f)
        value = [9, 2], derivative = [39.8875106, 8.77258872]
        """

        if not (isinstance(other, (int, float)) or isinstance(other, Variable)):
            raise TypeError("Can only raise to the power of a real number or variable!")

        try:
            value = self.val ** other.val
            if isinstance(self.val, np.ndarray):
                if (self.val <= 0).any():
                    derivative = other.val * self.val ** (other.val - 1) * self.der
                else:
                    derivative = (
                        other.val * self.val ** (other.val - 1) * self.der
                        + np.log(self.val) * self.val ** other.val * other.der
                    )
            else:
                if self.val <= 0:
                    derivative = other.val * self.val ** (other.val - 1) * self.der
                else:
                    derivative = (
                        other.val * self.val ** (other.val - 1) * self.der
                        + np.log(self.val) * self.val ** other.val * other.der
                    )
            return Variable(value, derivative)
        # If multiplying Variable object with real number
        except AttributeError:
            if isinstance(self.val, np.ndarray):
                if (self.val <= 0).any() and ((other - int(other)) != 0):
                    raise ValueError(
                        "Cannot take derivative of the root of a non-positive number"
                    )
            elif (self.val <= 0) and ((other - int(other)) != 0):
                raise ValueError(
                    "Cannot take derivative of the root of a non-positive number"
                )

            if isinstance(self.val, np.ndarray):
                if (self.val == 0).any() and other < 0:
                    raise ValueError("Cannot raise the negative power of 0")
            elif self.val == 0 and other < 0:
                raise ValueError("Cannot raise the negative power of 0")

            value = self.val ** other
            derivative = other * self.val ** (other - 1) * self.der
            return Variable(value, derivative)

    def __rpow__(self, other):
        """
        Method for performing reverse power, e.g. 3 ** x

        INPUTS
        ----------
        other : A int or float

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        >>> x = Variable(5, 1)
        >>> print(3 ** x)
        value = 243, derivative = 266.96278614635065

        >>> import numpy as np
        >>> x = Variable(np.array([0,2]), np.array([5,6]))
        >>> print(2 ** x)
        value = [1 4], derivative = [ 3.4657359  16.63553233]
        """

        value = other ** self.val
        derivative = np.log(other) * other ** self.val * self.der
        return Variable(value, derivative)

    def log(self, base=10):
        """
        Value and derivative computation of the log function (base 10 by default)

        INPUTS
        ------
        None

        RAISES
        ------
        ValueError
            When the input value is less than or equal to 0
            When base is not a number
            When base is not a positive number

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the log function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(5, 1)
        >>> f = x.log(base = np.e)
        >>> print(f)
        value = 1.6094379124341003, derivative = 0.2

        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> f = x.log(base = np.e)
        >>> print(f)
        value = [0.         0.69314718], derivative = [3. 2.]

        >>> x = Variable(np.array([1, 2, 3]), np.array([1, 1, 1]))
        >>> f = x.log(0.5)
        >>> print(f)
        value = [-0.        -1.        -1.5849625], derivative = [-1.44269504 -0.72134752 -0.48089835]
        """
        if not isinstance(base, (int, float)):
            raise ValueError("The log base must be a number!")
        if base <= 0 or (not isinstance(base, (int, float))):
            raise ValueError("The log base must be a positive number (int or float)")

        if isinstance(self.val, np.ndarray):
            if (self.val <= 0).any():
                raise ValueError("Cannot take the log of a non-positive number")
        elif self.val <= 0:
            raise ValueError("Cannot take the log of a non-positive number")

        value = np.log(self.val) / np.log(base)
        derivative = 1 / (self.val * np.log(base)) * self.der
        return Variable(value, derivative)

    def sqrt(self):
        """
        Value and derivative computation of the square root function

        INPUTS
        ------
        None

        RETURNS
        -------
        A Variable object
            This Variable object has the value and derivative of the square root function.

        EXAMPLES
        --------
        >>> import numpy as np
        >>> x = Variable(5, 1)
        >>> f = x.sqrt()
        >>> print(f)
        value = 2.23606797749979, derivative = 0.22360679774997896

        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([4,4]))
        >>> f = x.sqrt()
        >>> print(f)
        value = [1.         1.41421356], derivative = [2.         1.41421356]
        """
        return self.__pow__(0.5)

    def __radd__(self, other):
        """
        Method for performing right side addition

        INPUTS
        ------
        other : A Variable object


        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        # addition of a Variable object and a number
        >>> x = Variable(2, 5)
        >>> f = 3 + x
        >>> print(f)
        value = 5, derivative = 5

        # addition of two Variable objects
        >>> x = Variable(1, 2)
        >>> y = Variable(2 ,3)
        >>> f = x + y
        >>> print(f)
        value = 3, derivative = 5

        # addition of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,2]))
        >>> y = Variable(np.array([2,2]), np.array([3,3]))
        >>> f = y + x
        >>> print(f)
        value = [3 4], derivative = [6 5]

        # addition of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([1,2]))
        >>> y = 1
        >>> f = y + x
        >>> print(f)
        value = [2 3], derivative = [1 2]
        """

        return self.__add__(other)

    def __rsub__(self, other):
        """
        Method for performing right side subtraction

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        # subtraction of a Variable object and a real number
        >>> x = Variable(0)
        >>> y = 10
        >>> f = y - x
        >>> print(f)
        value = 10, derivative = -1

        # subtraction of two Variable objects
        >>> x = Variable(3, 5)
        >>> y = Variable(2, 3)
        >>> f = y - x
        >>> print(f)
        value = -1, derivative = -2

        # subtraction of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,2]))
        >>> y = Variable(np.array([2,2]), np.array([3,3]))
        >>> f = x - y
        >>> print(f)
        value = [-1  0], derivative = [ 0 -1]

        # subtraction of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([1,2]))
        >>> y = 1
        >>> f = y - x
        >>> print(f)
        value = [ 0 -1], derivative = [-1 -2]
        """

        return other + (-self)

    def __rmul__(self, other):
        """
        Method for performing right side multiplication

        INPUTS
        ----------
        other : A Variable object

        RETURNS
        -------
        A Variable object

        EXAMPLES:
        --------
        # multiplication of two Variable objects
        >>> x = Variable(2, 3)
        >>> y = Variable(3, 4)
        >>> f = x * y
        >>> print(f)
        value = 6, derivative = 17

        # multiplication of a Variable object and a number
        >>> x = Variable(5, 6)
        >>> y = 3
        >>> f = x * y
        >>> print(f)
        value = 15, derivative = 18

        # test multiplication of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = Variable(np.array([2,2]), np.array([2,2]))
        >>> f = x * y
        >>> print(f)
        value = [2 4], derivative = [ 8 12]

        # test multiplication of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([6,8]))
        >>> y = 2
        >>> f = y * x
        >>> print(f)
        value = [2 4], derivative = [12 16]
        """

        return self.__mul__(other)

    def __rtruediv__(self, other):
        """
        Method for performing right side division

        INPUTS
        ------
        other : A Variable object or a real number

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        # division of two Variable objects
        >>> x = Variable(2, 3)
        >>> y = Variable(1, 2)
        >>> f = y / x
        >>> print(f)
        value = 0.5, derivative = 0.25

        # division of a Variable object and a number
        >>> x = Variable(2, 3)
        >>> y = 10
        >>> f = y / x
        >>> print(f)
        value = 5.0, derivative = -7.5

        # 0 divides a Variable object
        >>> y = 0
        >>> x = Variable(1, 2)
        >>> f = 0 / x
        >>> print(f)
        value = 0.0, derivative = 0.0

        # test division of two Variable objects with vector input
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = Variable(np.array([2,2]), np.array([5,6]))
        >>> f = x / y
        >>> print(f)
        value = [0.5 1. ], derivative = [ 0.25 -1.  ]

        # test division of one Variable object with vector input and a real number
        >>> import numpy as np
        >>> x = Variable(np.array([1,2]), np.array([3,4]))
        >>> y = 2
        >>> f = y / x
        >>> print(f)
        value = [2. 1.], derivative = [-6. -2.]
        """

        if isinstance(self.val, np.ndarray):
            if (self.val == 0).any():
                raise ZeroDivisionError("Cannot divide by zero!")
        elif self.val == 0:
            raise ZeroDivisionError("Cannot divide by zero!")
        try:
            new_val = other.val / self.val
            new_der = (other.der * self.val - other.val * self.der) / (self.val ** 2)
            return Variable(new_val, new_der)
        except AttributeError:
            new_val = other / self.val
            new_der = -other / (self.val ** 2) * self.der
            return Variable(new_val, new_der)

    def logistic(self):
        """
        Method to perform logistic operation.

        RETURNS
        -------
        A Variable object

        EXAMPLES
        --------
        >>> x = Variable(5, 1)
        >>> f = x.logistic()
        >>> print(f)
        value = 0.9933071490757153, derivative = 0.006648056670790156

        >>> x = Variable(np.array([1, 2, 3]), np.array([1, 1, 1]))
        >>> f = x.logistic()
        >>> print(f)
        value = [0.73105858 0.88079708 0.95257413], derivative = [0.19661193 0.10499359 0.04517666]
        """
        new_val = 1 / (1 + np.exp(-self.val))
        new_der = np.exp(-self.val) / ((1 + np.exp(-self.val)) ** 2) * self.der
        return Variable(new_val, new_der)


      
def make_variables(var_list, der_list=None):
    """
    Function to create a list of Variable objects

    INPUTS
    ------
    var_list : list of int or float
        input values of these new Variable objects.
    der_list : list of int or float
        input derivative seeds of these new Variable objects. 

    RAISES
    ------
    ValueError
        if the input values and input derivative seeds are of different lengths.

    RETURNS
    -------
    variables : list of new Variable objects created.

    EXAMPLES
    --------
    >>> x = make_variables([1, 2], [1, 0])
    >>> print(x[0])
    value = 1, derivative = 1
    >>> print(x[1])
    value = 2, derivative = 0

    >>> import numpy as np
    >>> x = make_variables([np.array([3, 4]), np.array([1, 5])], [np.array([1, 2]), np.array([1, 5])])
    >>> print(x[0])
    value = [3 4], derivative = [1 2]
    >>> print(x[1])
    value = [1 5], derivative = [1 5]
    """
    if not der_list:
       der_list = np.eye(len(var_list))
        
    if len(var_list) != len(der_list):
        raise ValueError(
            "The value list and derivative list should be of the same length"
        )

    variables = []
    for val, der in zip(var_list, der_list):
        variables.append(Variable(val, der))

    return variables


def make_variable(var, der):
    """
    Function to create a Variable object

    INPUTS
    ------
    var : int or float
        input value of the Variable object.
    der : int or float
        input derivative seed of the Variable object.

    RETURNS
    -------
    A new Variable object

    EXAMPLES
    --------
    >>> x = make_variable(1, 1)
    >>> print(x)
    value = 1, derivative = 1

    >>> import numpy as np
    >>> x = make_variable(np.array([1, 2]), np.array([3,3]))
    >>> print(x)
    value = [1 2], derivative = [3 3]
    """
    return Variable(var, der)


exp = Variable.exp
cos = Variable.cos
sin = Variable.sin
tan = Variable.tan
logistic = Variable.logistic
sqrt = Variable.sqrt
log = Variable.log
arcsin = Variable.arcsin
arccos = Variable.arccos
arctan = Variable.arctan
sinh = Variable.sinh
cosh = Variable.cosh
tanh = Variable.tanh




if __name__ == "__main__":
    import doctest
    doctest.testmod()
