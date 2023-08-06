import numpy as np

from Node import Node

def exp(var):
    """
    Calculates e to the power of the input

    INPUTS:
    var ( Node object, float, or int) - to raise e to the power of
    
    OUTPUT: Node object that is e to the power of var
        
    EXAMPLES:
    
    >>>x=Node(2)
    >>>y=exp(x)
    >>>y.derivative=1
    >>> y.value
    np.exp(2)
    >>> x.der()
    np.exp(2)
    >>> exp(3)
    np.exp(3)
    """
    try:        
        value = np.exp(var.value)       
        derivative = np.exp(var.value)       
        node = Node(value)       
        var.children.append((node,derivative))        
        return node    
    except AttributeError:     
        return np.exp(var)
           
def sin(var):
    """
    Calculates the sine of the input

    INPUTS:
    var (Node object, float, or int) - to take the sine of
    
    OUTPUT: Node object that is the sine of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=sin(x)
    >>>y.derivative=1
    >>> sin(y).value
    np.sin(0.5)
    >>> x.der()
    np.cos(0.5)
    >>> sin(0.5)
    np.sin(0.5)
    """
    try:     
        value = np.sin(var.value)    
        derivative = np.cos(var.value)   
        node = Node(value)       
        var.children.append((node,derivative))       
        return node   
    except AttributeError:       
        return np.sin(var)

def cos(var): 
    """
    Calculates the cosine of the input

    INPUTS:
    var (Node object, float, or int) - to take the cosine of
    
    OUTPUT: Node object that is the cosine of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=cos(x)
    >>>y.derivative=1   
    >>> cosin(y).value
    np.cos(0.5)
    >>> x.der()
    -np.sin(0.5)
    >>> cosin(0.5)
    np.cosin(0.5)
    """
    try:       
        value = np.cos(var.value)       
        derivative = -1*np.sin(var.value)     
        node = Node(value)     
        var.children.append((node,derivative))     
        return node   
    except AttributeError:       
        return np.cos(var)

def tan(var): 
    """
    Calculates the tangent of the input

    INPUTS:
    var (Node object, float, or int) - to take the tangent of
    
    OUTPUT: Node object that is the tangent of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=tan(x)
    >>>y.derivative=1       
    >>> y.value
    np.tan(0.5)
    >>> x.der()
    (1 / np.cos(0.5) ** 2)
    >>> tan(0.5)
    np.tangent(0.5)
    """   
    try:        
        value = np.tan(var.value)     
        derivative = (1 / np.cos(var.value) ** 2)        
        node = Node(value)
        var.children.append((node,derivative))  
        return node    
    except AttributeError:        
        return np.tan(var)

def sinh(var):   
    
    """
    Calculates the hyperbolic sine of the input

    INPUTS:
    var (Node object, float, or int) - to take the hypberolic sine of
    
    OUTPUT: Node object that is the hyperbolic sine of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=sinh(x)
    >>>y.derivative=1 
    >>> y.value
    np.sinh(0.5)
    >>> x.der()
    np.cosh(1)
    >>> sinh(1)
    np.sinh(1)
    """   
    try:        
        value = np.sinh(var.value)        
        derivative = np.cosh(var.value)        
        node = Node(value)       
        var.children.append((node,derivative))       
        return node
    except AttributeError:        
        return np.sinh(var)
        
def cosh(var):
    """
    Calculates the hyperbolic cosine of the input

    INPUTS:
    var (Node object, float, or int) - to take the hyperbolic cosine of
    
    OUTPUT: Node object that is the hyperbolic cosine of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=cosh(x)
    >>>y.derivative=1 
    >>> y.value
    np.cosh(0.5)
    >>> x.der()
    np.sinh(1)
    >>> cosh(1)
    np.cosh(1)
    """
    try:
        value = np.cosh(var.value)        
        derivative = np.sinh(var.value)        
        node = Node(value)       
        var.children.append((node,derivative))        
        return node   
    except AttributeError:        
        return np.cosh(var)
        
def tanh(var):
    """
    Calculates the hyperbolic tangent of the input

    INPUTS:
    var (Node object, float, or int) - to take the hypberbolic tangent of
    
    OUTPUT: Node object that is the hyperbolic cosine of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=tanh(x)
    >>>y.derivative=1 
    >>> y.value
    np.tanh(0.5)
    >>> x.der()
    (1 / (np.cosh(0.5)**2))
    >>> tanh(1)
    np.tanh(1)
    """
    try:
        value = np.tanh(var.value)  
        derivative = 1 / (np.cosh(var.value)**2)        
        node = Node(value)        
        var.children.append((node,derivative))        
        return node    
    except AttributeError:        
        return np.tanh(var)
        
def ln(var):
    """
    Calculates the log of the input

    INPUTS:
    var (Node object, float, or int) - to take the log of
    
    OUTPUT: Node object that is the log of var
        
    EXAMPLES:
    >>>x=Node(0.5)
    >>>y=ln(x)
    >>>y.derivative=1    
    >>> y.value
    0
    >>> x.der()
    1
    >>> ln(3)
    np.ln(3)
    """

    try:        
        if var.value < 0:    
            raise ValueError('Log undefined for negative numbers') 
        else:           
            node = Node(np.log(var.value)) 
            derivative= 1/(var.value)       
            var.children.append((node,derivative))            
        return node   
    except AttributeError:        
        if var < 0:          
            raise ValueError('Log undefined for negative numbers')        
        else:             
            return np.log(var)
    
def log_base(var,base):
    """
    Calculates the log of the input in a specified base

    INPUTS:
    var (Node object, float, or int) - to take the log of
    base (Node object, float, or int) - base to take the log in
    
    OUTPUT: Dual object that is the log of var in a specified base
        
    EXAMPLES:
    >>>x=Node(3)
    >>>y=log_base(3,3)
    >>>y.derivative=1   
    >>> y.value
    1
    >>> x.der()
    1/3/np.log(3)
    >>> log_base(2, 2)
    np.log_base(1)
    """
    try:        
        if var.value < 0:    
            raise ValueError('Log undefined for negative numbers') 
        else:            
            node = Node(np.log(var.value)/np.log(base))  
            derivative= 1/(var.value*np.log(base))        
            var.children.append((node,derivative))            
        return node   
    except AttributeError:        
        if var < 0:          
            raise ValueError('Log undefined for negative numbers')        
        else:             
            return np.log(var)/np.log(base)
        
def logistic(var, L=1, k=1, x0=0):

    """
    Calculates the log of the input in a specified base

    INPUTS:
    var (Node object, float, or int) - to take the log of
    optional:
    L(float, or int) - curve's maximum value
    k (float, or int) - logistic growth rate or steepness of the curve
    x0 (float, or int) - the x value of the sigmoid midpoint
    
    OUTPUT: Node object that is the logistic function of var in a specified base
        
    EXAMPLES:
    >>>x=Node(1)
    >>>y=logistic(x)
    >>>y.derivative=1     
    >>> y.value
    1/(1+np.exp(-1))
    >>> x.der
    1/(1+np.exp(-1))*(1-1/(1+np.exp(-1)))
    >>> logistic(1)
    1/(1+np.exp(-1))
    """

    try:
        value=L / (1 + np.exp(-k * (var.value - x0)))
        node = Node(value) 
        derivative = k * value * (1 - value/L) 
        var.children.append((node,derivative))
        return node
    except AttributeError:
        return L / (1 + np.exp(-k * (var - x0)))      
    
def sqrt(var):
    """
    Calculates the square root of the input

    INPUTS:
    var (Node object, float, or int) - to take the square root of

    OUTPUT: Node object that is the square root of var
        
    EXAMPLES:
    >>>x=Node(9)
    >>>y=sqrt(x)
    >>>y.derivative=1     
    >>> y.value
    3
    >>> x.der()
    1 / 2 * (9 ** -0.5)
    >>> sqrt(9)
    3
    """
    try:     
       if var.value < 0:          
             raise ValueError('Sqrt undefined for negative numbers')    
       else:          
              node = Node(np.sqrt(var.value))   
              derivative=1/(2*np.sqrt(var.value))
              var.children.append((node,derivative))        
              return node    
    except AttributeError:        
        if var < 0:            
            raise ValueError('Sqrt undefined for negative numbers')      
        else:            
             return np.sqrt(var)
