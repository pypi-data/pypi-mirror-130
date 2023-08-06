# elementary functions

# import dependencies

import numpy as np
from Dual import Dual

def exp(var):

    """
    Calculates e to the power of the input

    INPUTS:
    var (Dual object, float, or int) - to raise e to the power of
    
    OUTPUT: Dual object that is e to the power of var
        
    EXAMPLES:
    
    >>> exp(Dual(1, 1)).value
    np.e
    >>> exp(Dual(1, 1)).derivative
    np.e
    >>> exp(Dual(2, 2)).value
    np.exp(2)
    >>> exp(Dual(2, 2)).derivative
    2*np.exp(2)
    >>> exp(3)
    np.exp(3)
    """

    try:
        value = np.exp(var.value)
        derivative = np.exp(var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.exp(var) 

## Trig functions 
def sin(var):

    """
    Calculates the sine of the input

    INPUTS:
    var (Dual object, float, or int) - to take the sine of
    
    OUTPUT: Dual object that is the sine of var
        
    EXAMPLES:
    
    >>> sin(Dual(0.5, 1)).value
    np.sin(0.5)
    >>> sin(Dual(np.pi, 1)).derivative
    np.cos(0.5)
    >>> sin(0.5)
    np.sin(0.5)
    """

    try:
        value = np.sin(var.value)
        derivative = np.cos(var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.sin(var)

def cos(var):

    """
    Calculates the cosine of the input

    INPUTS:
    var (Dual object, float, or int) - to take the cosine of
    
    OUTPUT: Dual object that is the cosine of var
        
    EXAMPLES:
    
    >>> cos(Dual(0.5, 1)).value
    np.cos(0.5)
    >>> cosin(Dual(np.pi, 1)).derivative
    -np.sin(0.5)
    >>> cos(0.5)
    np.cos(0.5)
    """

    try:
        value = np.cos(var.value)
        derivative = -1 * np.sin(var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.cos(var)

def tan(var):

    """
    Calculates the tangent of the input

    INPUTS:
    var (Dual object, float, or int) - to take the tangent of
    
    OUTPUT: Dual object that is the tangent of var
        
    EXAMPLES:
    
    >>> tan(Dual(0.5, 1)).value
    np.tan(0.5)
    >>> tan(Dual(np.pi, 1)).derivative
    (1 / np.cos(0.5) ** 2)
    >>> tan(0.5)
    np.tan(0.5)
    """

    try:
        derivative = (1 / np.cos(var.value) ** 2) * var.derivative
        value = np.tan(var.value)
        return Dual(value, derivative)
    except AttributeError:
        return np.tan(var)

## Hyperbolic functions 

def sinh(var):

    """
    Calculates the hyperbolic sine of the input

    INPUTS:
    var (Dual object, float, or int) - to take the hypberolic sine of
    
    OUTPUT: Dual object that is the hyperbolic sine of var
        
    EXAMPLES:
    
    >>> sinh(Dual(1,1)).value
    np.sinh(0.5)
    >>> sinh(Dual(1,1)).derivative
    np.cosh(1)
    >>> sinh(1)
    np.sinh(1)
    """

    try:
        value = np.sinh(var.value)
        derivative = np.cosh(var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.sinh(var)


def cosh(var):

    """
    Calculates the hyperbolic cosine of the input

    INPUTS:
    var (Dual object, float, or int) - to take the hyperbolic cosine of
    
    OUTPUT: Dual object that is the hyperbolic cosine of var
        
    EXAMPLES:
    
    >>> cosh(Dual(1,1)).value
    np.cosh(0.5)
    >>> cosh(Dual(1,1)).derivative
    np.sinh(1)
    >>> cosh(1)
    np.cosh(1)
    """

    try:
        value = np.cosh(var.value)
        derivative = np.sinh(var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.cosh(var)


def tanh(var):

    """
    Calculates the hyperbolic tangent of the input

    INPUTS:
    var (Dual object, float, or int) - to take the hypberbolic tangent of
    
    OUTPUT: Dual object that is the hyperbolic cosine of var
        
    EXAMPLES:
    
    >>> tanh(Dual(0.5,1)).value
    np.tanh(0.5)
    >>> tanh(Dual(0.5,1)).derivative
    (1 / (np.cosh(0.5)**2))
    >>> tanh(1)
    np.tanh(1)
    """

    try:
        value = np.tanh(var.value)
        derivative = (1 /np.cosh(var.value)**2) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.tanh(var)

## Logarithms

def ln(var):

    """
    Calculates the log of the input

    INPUTS:
    var (Dual object, float, or int) - to take the log of
    
    OUTPUT: Dual object that is the log of var
        
    EXAMPLES:
    
    >>> ln(Dual(1,1)).value
    0
    >>> ln(Dual(1,1)).derivative
    1
    >>> ln(3)
    np.ln(3)
    """

    try:
        value = np.log(var.value)
        derivative = (1 / var.value) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return np.log(var)


def log_base(var, base):

    """
    Calculates the log of the input in a specified base

    INPUTS:
    var (Dual object, float, or int) - to take the log of
    base (Daul object, float, or int) - base to take the log in
    
    OUTPUT: Dual object that is the log of var in a specified base
        
    EXAMPLES:
    
    >>> log_base(Dual(3,1), 3).value
    1
    >>> log_base(Dual(3,1), 3).derivative
    1/3/np.log(3)
    >>> log_base(2, 2)
    np.log_base(1)
    """

    return ln(var) / np.log(base)

## Logistic function

def logistic(var, L=1, k=1, x0=0):

    """
    Calculates the logistic function including the input
    
    INPUTS:
    var (Node object, float, or int) - to take the log of
    optional:
    L(float, or int) - curve's maximum value
    k (float, or int) - logistic growth rate or steepness of the curve
    x0 (float, or int) - the x value of the sigmoid midpoint
    
    OUTPUT: Dual object that is the logistic function of var in a specified base
        
    EXAMPLES:
    
    >>> logistic(Dual(1,1)).value
    1/(1+np.exp(-1))
    >>> logistic(Dual(3,1), 3).derivative
    1/(1+np.exp(-1))*(1-1/(1+np.exp(-1)))
    >>> logistic(1)
    1/(1+np.exp(-1))
    """

    try:
        value = L / (1 + np.exp(-k * (var.value - x0)))
        derivative = k * value * (1 - value/L) * var.derivative
        return Dual(value, derivative)
    except AttributeError:
        return L / (1 + np.exp(-k * (var - x0)))


## Square root

def sqrt(var):

    """
    Calculates the square root of the input

    INPUTS:
    var (Dual object, float, or int) - to take the square root of

    OUTPUT: Dual object that is the square root of var
        
    EXAMPLES:
    
    >>> sqrt(Dual(9,1)).value
    3
    >>> sqrt(Dual(9,1)).derivative
    1 / 2 * (9 ** -0.5)
    >>> sqrt(9)
    3
    """

    try:
        value = np.sqrt(var.value)
        derivative = 1 / 2 * var.derivative * (var.value ** -0.5)
        return Dual(value, derivative)
    except AttributeError:
        return np.sqrt(var)
