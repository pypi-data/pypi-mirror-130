# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 09:57:27 2021

@author: Maxime Laasri, Kishan Venkataramu, Lara Zeng
"""

import numpy as np

class Dual:
    
    def __init__(self, real = 0.0, dual = 0.0):
        self.real = real
        self.dual = dual
    
    def __str__(self):
        if self.dual < 0:
            return str(self.real) + " - " + str(-self.dual) + "e"
        return str(self.real) + " + " + str(self.dual) + "e"
    
    def __repr__(self):
        if self.dual < 0:
            return "Dual: " + str(self.real) + " - " + str(-self.dual) + "e"
        return "Dual: " + str(self.real) + " + " + str(self.dual) + "e"
    
    def __eq__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            
            # Comparing a dual number with a scalar
            return self.real == other and self.dual == 0.0
        
        # Comparing a dual number with another dual number
        return self.real == other_real and self.dual == other_dual
    
    def __add__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real + other, self.dual)
            except Exception as e:
                raise TypeError("Cannot add dual number %s (class Dual) to %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real + other_real, self.dual + other_dual)
    
    # regular fn to subtract
    def __sub__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real - other, self.dual)
            except Exception as e:
                raise TypeError("Cannot subtract dual number %s (class Dual) with %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real - other_real, self.dual - other_dual)
    
    def __mul__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real * other, self.dual * other)
            except Exception as e:
                raise TypeError("Cannot multiply dual number %s (class Dual) with %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real * other_real, self.dual * other_real + self.real * other_dual)
    
    # overloading division operators
    # python uses truediv not div for division
    def __truediv__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real / other, self.dual / other)
            except Exception as e:
                raise TypeError("Cannot divide dual number %s (class Dual) by %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real / other_real, (self.dual * other_real - self.real * other_dual) / (other_real ** 2))
    
    # overloaded fns
    def __radd__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real + other, self.dual)
            except Exception as e:
                raise TypeError("Cannot add dual number %s (class Dual) to %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real + other_real, self.dual + other_dual)
    
    # fn to subtract two dual numbers
    def __rsub__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real - other, self.dual)
            except Exception as e:
                raise TypeError("Cannot subtract dual number %s (class Dual) from %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real - other_real, self.dual - other_dual)
    
    def __rmul__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real * other, self.dual * other)
            except Exception as e:
                raise TypeError("Cannot multiply dual number %s (class Dual) with %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real * other_real, self.dual * other_real + self.real * other_dual)
    
    # fn to divide two dual numbers
    # python uses truediv for division operator
    def __rtruediv__(self, other):
        try:
            other_real = other.real
            other_dual = other.dual
        except:
            try:
                return Dual(self.real / other, self.dual / other)
            except Exception as e:
                raise TypeError("Cannot divide dual number %s (class Dual) by %s (%s): " % (self, other, type(other)) + str(e))
        return Dual(self.real / other_real, (self.dual * other_real - self.real * other_dual) / (other_real ** 2))
    
    def __pow__(self, exponent):
        """
        Computes the power of the current dual number to the given `exponent`.
        
        `exponent` must be a scalar.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the current one elevated to the
            power of `exponent`.

        """
        
        return self.power(exponent)
        
    def apply(self, function, derivative):
        """
        Applies the given function to the current Dual number and returns the
        results, without modifying the current object.
        
        Both `function` and `derivative` must take a 1D numpy array or scalar
        as input. `derivative` must correspond to the exact derivative of
        `function`.

        Returns
        -------
        Dual object
            The dual number that corresponds to f(self) where f is the function.

        """
        exp_real = np.exp(self.real)
        return Dual(function(self.real), self.dual * derivative(self.real))
    
    def power(self, exponent):
        """
        Computes the power of the current dual number to the given `exponent`.
        
        `exponent` must be a scalar.
        
        This method is an alternative way of computing the power of a dual
        number; another way is by using the usual ** operator.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the current one elevated to the
            power of `exponent`.

        """
        
        return self.apply(lambda x: x ** exponent, lambda x: exponent * x ** (exponent - 1))
    
    def exp(self):
        """
        Computes the exponential of the current dual number.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the exponential of the current
            one.

        """
        
        # Note that, unlike most other numeric functions, this function does
        # not internally use the apply() method. This is to gain speed: since
        # the derivative of exp() is itself, we can compute the exponential of
        # the real part once and for all.
        
        exp_real = np.exp(self.real)
        return Dual(exp_real, self.dual * exp_real)
    
    def log(self):
        """
        Computes the natural logarithm of the current dual number.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the natural logarithm of the
            current one.

        """
        
        return self.apply(np.log, lambda x: 1.0 / x)
    
    def cos(self):
        """
        Computes the cosine of the current dual number.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the cosine of the current one.

        """
        
        return self.apply(np.cos, lambda x: -np.sin(x))
    
    def sin(self):
        """
        Computes the sine of the current dual number.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the sine of the current one.

        """
        
        return self.apply(np.sin, np.cos)
    
    def tan(self):
        """
        Computes the tangent of the current dual number.
        
        Returns
        -------
        Dual object
            The dual number that corresponds to the tangent of the current one.

        """
        
        return self.apply(np.tan, lambda x: 1 + np.square(np.tan(x)))

if __name__ == "__main__":
    z = Dual(1.0, 1.0)
    print("2 + %s =" % z, 2 + z)
    print("%s + 2 =" % z, z + 2)
    print((z - 2 * z))
    print((z * z))
    print(z/3)
    print((z * z) / 2)
    print("z / z =", z / z)
    print(z.tan())