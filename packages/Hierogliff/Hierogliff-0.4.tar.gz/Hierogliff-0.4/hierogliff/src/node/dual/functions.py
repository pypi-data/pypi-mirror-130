# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:41:41 2021

@author: Maxime Laasri, Kishan Venkataramu
"""

def apply(z, function, derivative):
    """
    Applies the given function to the dual number `z` and returns the result.
    
    Both `function` and `derivative` must take a 1D numpy array or scalar
    as input. `derivative` must correspond to the exact derivative of
    `function`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to f(z) where f is the given function.

    """
    
    return z.apply(function, derivative)

def power(z, exponent):
    """
    Computes the power of the dual number `z` to the given `exponent`.
    
    `exponent` must be a scalar.
    
    This method is an alternative way of computing the power of a dual
    number; another way is by using the usual ** operator.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to `z` elevated to the power of
        `exponent`.

    """
    
    return z.power(exponent)

def exp(z):
    """
    Computes the exponential of the dual number `z`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to the exponential of `z`.

    """
    
    return z.exp()

def log(z):
    """
    Computes the natural logarithm of the dual number `z`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to the natural logarithm of `z`.

    """
    
    return z.log()

def cos(z):
    """
    Computes the cosine of the dual number `z`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to the cosine of `z`.

    """
    
    return z.cos()

def sin(z):
    """
    Computes the sine of the dual number `z`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to the sine of `z`.

    """
    
    return z.sin()

def tan(z):
    """
    Computes the tangent of the dual number `z`.
    
    Returns
    -------
    Dual object
        The dual number that corresponds to the tangent of `z`.

    """
    
    return z.tan()
