import numpy as np


class RD:
    def __init__(self, value):
        """
        Initialize a RD object.

        INPUTS
        ------
        value : A numpy array
            A numpy array that stores the value of RD object
            vector input: np.array([1, 2, 3])
            scalar input: np.array([1.5])

        RAISES
        ------
        Exception
            if value is not a numpy array
            if input is a multidimentional array
            if input is not a numpy array of int or float

        EXAMPLES
        --------
        >>> x = RD(np.array([1, 2, 3]))
        >>> x.val
        array([1, 2, 3])
        >>> x.grad
        array([1., 1., 1.])
        >>> x.children
        []
        """

        if not isinstance(value, np.ndarray):
            raise Exception("Input must be a numpy array!")

        if len(value.shape) != 1:
            raise Exception("Input cannot be a multidimentional array")

        for i in range(len(value)):
            if not isinstance(value[i], (np.int_, np.double)):
                raise Exception("Input must be a numpy array of int or float!")

        self.val = value
        self.grad = np.ones(len(value))
        self.children = []

    def sin(self):
        """
        Method to perform sin operation for reverse mode.

        RETURNS
        -------
        child : A RD object

        EXAMPLES
        --------
        # vector input
        >>> x = RD(np.array([2,3,4]))
        >>> f = x.sin()
        >>> x.get_derivative()
        array([-0.41614684, -0.9899925 , -0.65364362])

        # scalar input
        >>> x = RD(np.array([2]))
        >>> f = x.sin()
        >>> x.get_derivative()
        array([-0.41614684])
        """
        child = RD(np.sin(self.val))
        self.children.append((np.cos(self.val), child))
        self.grad = None
        return child

    def cos(self):
        """
        Method to perform cos operation for reverse mode.

        RETURNS
        -------
        child : A RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([2,3,4]))
        >>> f = x.cos()
        >>> x.get_derivative()
        array([-0.90929743, -0.14112001,  0.7568025 ])
        """
        child = RD(np.cos(self.val))
        self.children.append((-np.sin(self.val), child))
        self.grad = None
        return child

    def tan(self):
        """
        Method to perform cos operation for reverse mode.

        NOTES
        -----
        The tan function tan doesn't exist at odd multiple of pi/2, however, due to machine precision, the input will
        never be exactly equal to odd multiple of pi/2. Therefore no ValueError will be raised.

        RETURNS
        -------
        child : A RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([2,3,4]))
        >>> f = x.cos()
        >>> x.get_derivative()
        array([-0.90929743, -0.14112001,  0.7568025 ])
        """
        child = RD(np.tan(self.val))
        self.children.append((1 / (np.cos(self.val) ** 2), child))
        self.grad = None
        return child

    def __add__(self, other):
        """
        Overload addition operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        child : RD object

        RAISES
        ------
        Exception
            if two vectors have different lengths

        EXAMPLE
        -------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = x + y
        >>> x.get_derivative()
        array([1., 1., 1.])

        >>> x = RD(np.array([1]))
        >>> y = 3
        >>> f = x + y
        >>> x.get_derivative()
        array([1.])
        """
        if isinstance(other, (float, int)):
            child = RD(self.val + other)
            self.children.append((np.ones(len(self.val)), child))
            self.grad = None
            return child
        else:
            if len(self.val) != len(other.val):
                raise Exception("Two vectors have different lengths!")
            child = RD(self.val + other.val)
            self.children.append((np.ones(len(self.val)), child))
            other.children.append((np.ones(len(self.val)), child))
            self.grad = None
            other.grad = None
            return child

    def __radd__(self, other):
        """
        Overload reverse addition operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        RD object

        RAISES
        ------
        Exception
            if two vectors have different lengths

        EXAMPLE
        -------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = y + x
        >>> y.get_derivative()
        array([1., 1., 1.])

        >>> x = RD(np.array([1]))
        >>> y = 3
        >>> f = y + x
        >>> x.get_derivative()
        array([1.])
        """
        return self.__add__(other)

    def get_derivative(self):
        """
        Method to get the reverse mode derivative of RD objects.
        The result will be stored in grad attribute of the RD object.

        RETURNS
        -------
        int or float
            derivative of the RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([2]))
        >>> f = x ** 2
        >>> x.get_derivative()
        array([4.])
        """
        if self.grad is None:
            grad = 0
            for der, node in self.children:
                grad += der * node.get_derivative()
            self.grad = grad
        return self.grad

    def __mul__(self, other):
        """
        Overload multiplication operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        child : RD object

        RAISES
        ------
        Exception
            if two vectors have different lengths

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([3,2,1]))
        >>> f = x * y
        >>> x.get_derivative()
        array([3., 2., 1.])
        >>> y.get_derivative()
        array([1., 2., 3.])

        >>> x = RD(np.array([1,2,3]))
        >>> f = x * 3
        >>> x.get_derivative()
        array([3., 3., 3.])
        """
        if isinstance(other, (float, int)):
            child = RD(self.val * other)
            self.children.append((np.ones(len(self.val)) * other, child))
            self.grad = None
            return child
        else:
            if len(self.val) != len(other.val):
                raise Exception("Two vectors have different lengths!")
            child = RD(self.val * other.val)
            self.children.append((other.val, child))
            other.children.append((self.val, child))
            self.grad = None
            other.grad = None
            return child

    def __rmul__(self, other):
        """
        Overload reverse multiplication operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        RD object

        RAISES
        ------
        Exception
            if two vectors have different lengths

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([3,2,1]))
        >>> f = y * x
        >>> x.get_derivative()
        array([3., 2., 1.])

        >>> x = RD(np.array([1,2,3]))
        >>> f = 3 * x
        >>> x.get_derivative()
        array([3., 3., 3.])
        """
        return self.__mul__(other)

    def __neg__(self):
        """
        Overload the negation operation for RD objects.

        Returns
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> f = - x
        >>> x.get_derivative()
        array([-1., -1., -1.])

        """
        child = RD(-self.val)
        self.children.append((-np.ones(len(self.val)), child))
        self.grad = None
        return child

    def __sub__(self, other):
        """
        Overload subtraction operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([3,2,1]))
        >>> f = x - y
        >>> x.get_derivative()
        array([1., 1., 1.])

        >>> x = RD(np.array([1,2,3]))
        >>> f = x - 3
        >>> x.get_derivative()
        array([1., 1., 1.])
        """
        if isinstance(other, (float, int)):
            child = RD(self.val - other)
            self.children.append((np.ones(len(self.val)), child))
            self.grad = None
            return child
        else:
            if len(self.val) != len(other.val):
                raise Exception("Two vectors have different lengths!")
            child = RD(self.val - other.val)
            self.children.append((np.ones(len(self.val)), child))
            other.children.append((-np.ones(len(self.val)), child))
            self.grad = None
            other.grad = None
            return child

    def __rsub__(self, other):
        """
        Overload reverse subtraction operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([3,2,1]))
        >>> f = y - x
        >>> x.get_derivative()
        array([-1., -1., -1.])

        >>> x = RD(np.array([1,2,3]))
        >>> f = 3 - x
        >>> x.get_derivative()
        array([-1., -1., -1.])
        """
        if isinstance(other, (float, int)):
            child = RD(other - self.val)
            self.children.append((-np.ones(len(self.val)), child))
            self.grad = None
            return child
        else:
            if len(self.val) != len(other.val):
                raise Exception("Two vectors have different lengths!")
            child = RD(other.val - self.val)
            self.children.append((-np.ones(len(self.val)), child))
            other.children.append((np.ones(len(self.val)), child))
            self.grad = None
            other.grad = None
            return child

    def __pow__(self, other):
        """
        Overload the power operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RAISES
        ------
        Exception
            if take derivative of the root of a non-positive number
            if raise the negative power of 0
            if two vector inputs have different lengths

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([3, 4]))
        >>> y = RD(np.array([1, 2]))
        >>> f = x ** y
        >>> x.get_derivative()
        array([1., 8.])

        >>> x = RD(np.array([2]))
        >>> f = x ** 3
        >>> x.get_derivative()
        array([12.])
        """
        self.val = self.val.astype(float)
        if isinstance(other, (float, int)):
            if (other - np.floor(other) != 0) and any(self.val <= 0):
                raise Exception(
                    "Cannot take derivative of the root of a non-positive number"
                )
            if any(self.val == 0) and other < 0:
                raise Exception("Cannot raise the negative power of 0")

            child = RD(self.val ** other)
            self.children.append((other * (self.val ** (other - 1)), child))
            self.grad = None
            return child
        else:
            if len(self.val) != len(other.val):
                raise Exception("Two vectors have different lengths!")
            child = RD(self.val ** other.val)
            self.children.append((other.val * (self.val ** (other.val - 1)), child))
            self.grad = None
            other.children.append(((self.val ** other.val) * np.log(self.val), child))
            other.grad = None
            return child

    def sqrt(self):
        """
        Method to perform sqrt operation for RD objects.

        RETURNS
        -------
        RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([5,6]))
        >>> f = x.sqrt()
        >>> x.get_derivative()
        array([0.2236068 , 0.20412415])

        >>> x = RD(np.array([2]))
        >>> f = x.sqrt()
        >>> x.get_derivative()
        array([0.35355339])
        """
        return self.__pow__(0.5)

    def __repr__(self):
        """
        Dunder method for printing output

        INPUTS
        ------
        None

        RETURNS
        -------
        The attributes of the RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([2]))
        >>> print(x)
        value = [2], derivative = [1.]
        """

        return f"value = {self.get_value()}, derivative = {self.get_derivative()}"

    def get_value(self):
        """
        Method to get value of a RD object.

        RETURNS
        -------
        numpy array

        EXAMPLES
        --------
        >>> x = RD(np.array([1, 2, 3]))
        >>> x.get_value()
        array([1, 2, 3])
        """
        return self.val

    def reset(self):
        """
        Method to reset the derivative and children list of a RD object without re-initiating.

        RETURNS
        -------
        None

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([3,2,1]))
        >>> f = x * y
        >>> x.get_derivative()
        array([3., 2., 1.])
        >>> x.reset()
        >>> x.get_derivative()
        array([1., 1., 1.])
        """
        self.children = []
        self.grad = np.ones(len(self.val))

    def arcsin(self):
        """
        Method to perform arcsin operation for RD objects.

        RETURNS
        -------
        child : RD object

        RAISES:
        ------
        Exception
            if the input array has elements bigger than 1 or smaller than -1

        EXAMPLES
        --------
        >>> x = RD(np.array([0.5]))
        >>> f = x.arcsin()
        >>> x.get_derivative()
        array([1.15470054])
        """
        for i in range(len(self.val)):
            if self.val[i] > 1 or self.val[i] < -1:
                raise Exception("The domian of arcsin is between 1 and -1")

        child = RD(np.arcsin(self.val))
        self.children.append((1 / (1 - (self.val ** 2)) ** 0.5, child))
        self.grad = None
        return child

    def arccos(self):
        """
        Method to perform arccos operation for RD objects.

        RETURNS
        -------
        child : RD object

        RAISES:
        ------
        Exception
            if the input array has elements bigger than 1 or smaller than -1

        EXAMPLES
        --------
        >>> x = RD(np.array([0.5]))
        >>> f = x.arccos()
        >>> x.get_derivative()
        array([-1.15470054])
        """
        for i in range(len(self.val)):
            if self.val[i] > 1 or self.val[i] < -1:
                raise Exception("The domian of arcsin is between 1 and -1")

        child = RD(np.arccos(self.val))
        self.children.append((-1 / (1 - (self.val ** 2)) ** 0.5, child))
        self.grad = None
        return child

    def arctan(self):
        """
        Method to perform arctan operation for RD objects.

        Returns
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1, 2, 3]))
        >>> f = x.arctan()
        >>> x.get_derivative()
        array([0.5, 0.2, 0.1])
        """
        child = RD(np.arctan(self.val))
        self.children.append((1 / (1 + (self.val ** 2)), child))
        self.grad = None
        return child

    def __eq__(self, other):
        """
        Overload the operation to compare if two RD objects are equal.

        INPUTS
        ----------
        other : any type

        Returns
        -------
        bool
            True if the derivative and value of self and other are equal.

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = x * y
        >>> x == y
        True

        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = x ** y
        >>> x == y
        False

        >>> x = RD(np.array([1,2,3]))
        >>> x == 3
        False
        """
        if not isinstance(other, RD):
            return False
        if len(self.val) != len(other.val):
            return False
        if all(np.equal(self.val, other.val)) and all(
            np.equal(self.get_derivative(), other.get_derivative())
        ):
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Overload the operation to compare if two RD objects are not equal.

        INPUTS
        ------
        other : any type

        Returns
        -------
        bool
            True if any of the derivative and value of self and other are not equal.

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = x ** y
        >>> x != y
        True

        >>> x = RD(np.array([1,2,3]))
        >>> y = RD(np.array([1,2,3]))
        >>> f = x * y
        >>> x != y
        False

        >>> x = RD(np.array([1,2,3]))
        >>> x != 3
        True
        """
        if self.__eq__(other):
            return False
        else:
            return True

    def exp(self, base=None):
        """
        Method to perform exponential operation for RD objects.

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> f = x.exp()
        >>> x.get_derivative()
        array([ 2.71828183,  7.3890561 , 20.08553692])

        >>> x = RD(np.array([1,2,3]))
        >>> f = x.exp(2)
        >>> x.get_derivative()
        array([1.38629436, 2.77258872, 5.54517744])
        """
        if base == None:
            child = RD(np.exp(self.val))
            self.children.append((np.exp(self.val), child))
            self.grad = None
            return child
        elif isinstance(base, (int, float)):
            return self.__rpow__(base)
        else:
            raise Exception("Exponential base must be int or float !")

    def sinh(self):
        """
        Method to perform sinh operation for RD objects.

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> f = x.sinh()
        >>> x.get_derivative()
        array([ 1.54308063,  3.76219569, 10.067662  ])
        """
        child = RD(np.sinh(self.val))
        self.children.append((np.cosh(self.val), child))
        self.grad = None
        return child

    def cosh(self):
        """
        Method to perform cosh operation for RD objects.

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> f = x.cosh()
        >>> x.get_derivative()
        array([ 1.17520119,  3.62686041, 10.01787493])
        """
        child = RD(np.cosh(self.val))
        self.children.append((np.sinh(self.val), child))
        self.grad = None
        return child

    def tanh(self):
        """
        Method to perform tanh operation for RD objects.

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1,2,3]))
        >>> f = x.tanh()
        >>> x.get_derivative()
        array([0.41997434, 0.07065082, 0.00986604])
        """
        child = RD(np.tanh(self.val))
        self.children.append((1 / (np.cosh(self.val) ** 2), child))
        self.grad = None
        return child

    def log(self, base=10):
        """
        Method to perform log operation for RD objects, the base is 10 by default.

        Parameters
        ----------
        base : int or float
            base of the log function, by default to be 10.

        RAISES
        ------
        Exception
            if base is not a number
            if base is not a positive number
            if any element in the input vector is non-positive

        RETURNS
        -------
        child : RD object


        EXAMPLES
        --------
        >>> x = RD(np.array([1, 2, 3]))
        >>> f = x.log(0.5)
        >>> x.get_derivative()
        array([-1.44269504, -0.72134752, -0.48089835])
        """
        if not isinstance(base, (int, float)):
            raise Exception("The log base must be a number!")
        if base <= 0 or (not isinstance(base, (int, float))):
            raise Exception("The log base must be a positive number (int or float)")
        if any(self.val <= 0):
            raise Exception("The input vector must be positive")
        child = RD(np.log(self.val) / np.log(base))
        self.children.append((1 / (self.val * np.log(base)), child))
        self.grad = None
        return child

    def __rpow__(self, other):
        """
        Overload reverse power operation for RD objects.

        INPUTS
        ----------
        other : RD object or int or float

        Raises
        ------
        Exception
            if raise the negative power of 0
            if take derivative of the root of a non-positive number
            if two vector inputs have different lengths

        RETURNS
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([5,6]))
        >>> f = 2 ** x
        >>> x.get_derivative()
        array([22.18070978, 44.36141956])
        """
        other = float(other)
        if isinstance(other, (float, int)):
            if other == 0 and any(self.val < 0):
                raise Exception("Cannot raise the negative power of 0")
            if other < 0 and any(self.val - np.floor(self.val) != 0):
                raise Exception(
                    "Cannot take derivative of the root of a non-positive number"
                )
            child = RD(other ** self.val)
            self.children.append(((other ** self.val) * np.log(other), child))
            self.grad = None
            return child
        else:
            if len(other.val) != len(self.val):
                raise Exception("Two vectors have different lengths!")
            child = RD([other.val ** self.val])
            other.children.append((self.val * (other.val ** (self.val - 1)), child))
            other.grad = None
            self.children.append(((other.val ** self.val) * np.log(other.val), child))
            self.grad = None
            return child

    def __truediv__(self, other):
        """
        Overload the division operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RAISES
        ------
        Exception
            if the denominator is 0

        RETURNS
        -------
        RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([5,6]))
        >>> f = x / 3
        >>> x.get_derivative()
        array([0.33333333, 0.33333333])

        >>> x = RD(np.array([5,6]))
        >>> y = RD(np.array([1,2]))
        >>> f = x / y
        >>> x.get_derivative()
        array([1. , 0.5])
        """
        if isinstance(other, (float, int)):
            if other == 0:
                raise Exception("Cannot divide by 0")
            child = RD(self.val / other)
            self.children.append((1 / other * np.ones(len(self.val)), child))
            self.grad = None
            return child
        else:
            if any(other.val == 0):
                raise Exception("Cannot divide by 0")
            return self * (other ** (-1))

    def __rtruediv__(self, other):
        """
        Overload the reverse division operation for RD objects.

        INPUTS
        ------
        other : RD object or int or float

        RAISES
        ------
        Exception
            if the denominator is 0

        RETURNS
        -------
        RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([5,6]))
        >>> f = 2 / x
        >>> x.get_derivative()
        array([-0.08      , -0.05555556])

        >>> x = RD(np.array([5,6]))
        >>> y = RD(np.array([1,2]))
        >>> f = x / y
        >>> x.get_derivative()
        array([1. , 0.5])
        """
        if any(self.val == 0):
            raise Exception("Cannot divide by 0")
        return other * (self ** (-1))

    def logistic(self):
        """
        Method to perform logistic operation for RD objects

        Returns
        -------
        child : RD object

        EXAMPLES
        --------
        >>> x = RD(np.array([1, 2, 3]))
        >>> f = x.logistic()
        >>> x.get_derivative()
        array([0.19661193, 0.10499359, 0.04517666])

        >>> x = RD(np.array([2]))
        >>> f = x.logistic()
        >>> x.get_derivative()
        array([0.10499359])
        """
        child = RD(1 / (1 + np.exp(-self.val)))
        self.children.append(
            (np.exp(-self.val) / ((1 + np.exp(-self.val)) ** 2), child)
        )
        self.grad = None
        return child


if __name__ == "__main__":
    import doctest

    doctest.testmod()
