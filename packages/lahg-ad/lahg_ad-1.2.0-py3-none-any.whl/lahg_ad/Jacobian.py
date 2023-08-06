#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lahg_ad as ad
import numpy as np


class Vector:
    def __init__(self, func_list):
        """
        This is a Vector class that computes and stores multivariate functions values and derivatives. 
        
        INPUTS
        -------
        func_list : a list of function expressions
        
        ATTRIBUTES
        -------
            a 2-D numpy array representing the 
        """
        
        self.func_list = func_list
        self.vals = self._calculate_vals()
        self.jacobian = self._calculate_jacobian()

    def _calculate_jacobian(self):
        """
        Function for computing the Jacobian Matrix for vector function

        INPUTS
        ------
        self.func_list : a list of function expression passed in at initialization

        RETURNS
        -------
        numpy array
            a 2-D numpy array representing the Jacobian Matrix

        RAISES
        ------
        Exception
            if the list contains non-Variable object
            if input functions have different dimensions

        EXAMPLES
        --------
        >>> x = ad.Variable(4, np.array([1, 0]))
        >>> y = ad.Variable(3, np.array([0, 1]))
        >>> f = ad.Vector([x+y, x**3, x*y])
        >>> print(f.jacobian)
        [[ 1  1]
         [48  0]
         [ 3  4]]

        >>> x = ad.Variable(4, np.array([1, 0]))
        >>> f = Vector([x+2, x**2])
        >>> print(f.jacobian)
        [[1 0]
         [8 0]]

        """
        der = []
        expect_shape = len(self.func_list[0].der)
        for func in self.func_list:
            if not isinstance(func, ad.Variable):
                raise Exception("The input must be a list of Variable objects")
            if len(func.der) != expect_shape:
                raise Exception("The input functions have different dimensions!")
            der.append(func.der)
        return np.array(der)


    def _calculate_vals(self):
        """
        Function for computing the value of vector function

        INPUTS
        ------
        func_list : a list of function expression

        RAISES
        ------
        Exception
            if the list contains non-Variable object

        RETURENS
        -------
        TYPE
            a 1-D numpy array representing the value of the vector function

        EXAMPLES
        --------
        >>> x = ad.Variable(4, np.array([1, 0]))
        >>> y = ad.Variable(3, np.array([0, 1]))
        >>> f = ad.Vector([x+y, x**3, x*y])
        >>> print(f.vals)
        [ 7 64 12]

        >>> x = ad.Variable(4, np.array([1, 0]))
        >>> f = ad.Vector([x+2, x**2])
        >>> print(f.vals)
        [ 6 16]

        """
        vals = []
        for func in self.func_list:
            if not isinstance(func, ad.Variable):
                raise Exception("The input must be a list of Variable objects")
            vals.append(func.val)
        return np.array(vals)
    
    def __repr__(self):
        """
        Dunder method for printing Vector class attributes

        INPUTS
        ------
        None

        RETURNS
        -------
        The attributes of the Vector
        
        EXAMPLES
        --------
        >>> x, y = ad.make_variables([2, 1])
        >>> f = ad.Vector([x+y, x*y])
        >>> print(f)
        values:
        [3 2]
        jacobian:
        [[1. 1.]
         [1. 2.]]
        """
        
        return f"values:\n{self.vals}\njacobian:\n{self.jacobian}"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
