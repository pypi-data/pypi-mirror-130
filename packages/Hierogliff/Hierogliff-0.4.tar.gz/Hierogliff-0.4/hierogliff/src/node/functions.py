# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 12:57:39 2021

@author: Maxime Laasri
"""

from node import Power
from node import Exp
from node import Log
from node import Cos
from node import Sin
from node import Tan

def power(n, exponent):
    """
    Creates and returns a node representing the power of the expression of node
    `n` to the given `exponent`.
    
    `exponent` must be a scalar.
    
    This method is an alternative way of computing the power of an expression;
    another way is by using the usual ** operator.
    
    Returns
    -------
    Node object
        The node that corresponds to the expression represented by `n` elevated
        to the power of `exponent`.

    """
    
    return Power([n], exponent)

def exp(n):
    """
    Creates and returns a node representing the exponential of the expression
    of node `n`.
    
    Returns
    -------
    Node object
        The node that corresponds to the exponential of the expression
        represented by `n`.

    """
    
    return Exp([n])

def log(n):
    """
    Creates and returns a node representing the logarithm of the expression
    of node `n`.
    
    Returns
    -------
    Node object
        The node that corresponds to the logarithm of the expression
        represented by `n`.

    """
    
    return Log([n])

def cos(n):
    """
    Creates and returns a node representing the cosine of the expression of
    node `n`.
    
    Returns
    -------
    Node object
        The node that corresponds to the cosine of the expression represented
        by `n`.

    """
    
    return Cos([n])

def sin(n):
    """
    Creates and returns a node representing the sine of the expression of
    node `n`.
    
    Returns
    -------
    Node object
        The node that corresponds to the sine of the expression represented
        by `n`.

    """
    
    return Sin([n])

def tan(n):
    """
    Creates and returns a node representing the tangent of the expression of
    node `n`.
    
    Returns
    -------
    Node object
        The node that corresponds to the tangent of the expression represented
        by `n`.

    """
    
    return Tan([n])