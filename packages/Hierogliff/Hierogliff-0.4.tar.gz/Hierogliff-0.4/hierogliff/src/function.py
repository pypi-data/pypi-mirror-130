# -*- coding: utf-8 -*-
"""
Created on Thu Dec 09 15:44:22 2021

@author: Maxime Laasri
"""

from node import *

class Function:
    
    def __init__(self, root, optimize = True):
        """
        Creates a Function object that represents a mathematical expression to
        derivate.

        Parameters
        ----------
        root : Node
            The node representing the expression to derivate. Must inherit from
            one of the Node class' derived classes.

        Returns
        -------
        None.

        """
        
        self._root = root
        if optimize:
            self._optimize()
    
    def _optimize(self):
        """
        Re-optimize the computational graph of the function to avoid duplicate
        computations. For example, in the expression x + y + exp(x + y), the
        sum x + y is present twice; calling this function will optimize the
        computational graph to ensure the value and gradient of x + y is only
        computed once.
        
        This method is automatically called upon creation of a Function object,
        except if the 'optimize' argument is set to False in the initializer.
        
        For example

        Returns
        -------
        None.

        """
        self._optimize_recursive(self._root, {})
        
    def _optimize_recursive(self, node, table):
        
        for i, parent in enumerate(node._parents):
            
            self._optimize_recursive(parent, table)
            
            parent_id = str(parent)
            
            if parent_id in table:
                node._parents[i] = table[parent_id]
            
            else:
                table[parent_id] = parent
    
    def grad(self, value, direction):
        """
        Computes the gradient of the function at the given value and in the
        given direction.
        
        Both value and direction must be a dictionary that associates a
        numerical value to all input variables. An error will be thrown if a
        value is missing for one particular input variable.

        Parameters
        ----------
        value : dictionary {string: float or int}
            Dictionary of values to assign to each individual input variable.
            Each entry of the dictionary correspond to one input variable: the
            key is the variable's name, and the value its numeric value.
        direction : dictionary {string: float or int}
            Dictionary of values to assign to each individual input variable.
            Each entry of the dictionary correspond to one input variable: the
            key is the variable's name, and the value of the step taken in the
            direction of the variable.

        Returns
        -------
        None.

        """
        
        return self._root.forward(value, direction)