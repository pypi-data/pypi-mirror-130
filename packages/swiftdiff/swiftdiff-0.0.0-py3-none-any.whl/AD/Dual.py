import numpy as np

class Dual():
    
    """
    Here we are creating a Dual Class to fuel Automatic Differentation (forward).

    ATTRIBUTES:
    value (int or float) - value of the user-inputted variable
    derivative (int or float) - derivative, gradient, or Jacobian of the user-inputted variable

    OPTIONAL ATTRIBUTES: (for functions with multiple input variables):
    index (int) - index of the variable within the list of input variables for the function
    total (int) - total number of input variables for the function
  
    """

    def __init__(self, value, derivative, **kwargs):
        
        """
        Initiates an instance of the Dual class.
        
        INPUTS:
        value (int or float) - value of the user-inputted variable
        derivative (int or float) - derivative, gradient, or Jacobian of the user-inputted variable

        OPTIONAL INPUTS: (for functions with multiple input variables):
        index (int) - index of the variable within the list of input variables for the function
        total (int) - total number of input variables for the function
        """
        
        self.value = value
        if kwargs:
            self.total = kwargs["total"]
            self.index = kwargs["index"]
            self.derivative = np.zeros(self.total)
            self.derivative[self.index] = derivative
        else:
            self.derivative = derivative
      

    def __repr__(self): 
        
        """
        Prints information about the Dual class instance.
         
        EXAMPLES:
        
        For single input functions:
        >>> Dual(5, 2) 
        Dual('value': 5, 'derivative': 2)

        For multivariable functions:
        >>> x = Dual(5, 2, index = 0, total = 2)
        >>> x
        Dual('value': 5, 'derivative': 3, 'index': 0, 'total': 2)
          >>> y = Dual(10, 1, index = 1, total = 2)
          >>> y
        Dual('value': 10, 'derivative': 1, 'index': 1, 'total': 2)
        >>> z = x + y
        >>> z
        Dual('value': 5, 'derivative': [2, 1])
        """
        
        return "{class_name}({attributes})".format(class_name = type(self).__name__, attributes = self.__dict__)


    def __add__(self,other):
        
        """
        Adds self and a Dual object, float, or int.
         
        INPUTS:
        self (Dual object) - to add
        other (Dual object, float, or int) - to add
        
        OUTPUT: Dual object that is the sum of self and other
        
        EXAMPLES:
        
        Dual + Dual:
        >>> Dual(5, 2) + Dual(3, 1)
        Dual('value': 8, 'derivative': 3)

        Dual + float:
          >>> Dual(5, 2) + 3.0
        Dual('value': 8.0, 'derivative': 2)
      
        Dual + int:
        >>> Dual(5, 2) + 3
        Dual('value': 8, 'derivative': 2)
      
         For multivariate functions:
        >>> Dual(5, 2, index = 0, total = 2) + Dual(10, 1, index = 1, total = 2)
        Dual('value': 15, 'derivative': [2, 1])
        """
        
        try:
            value = self.value + other.value
            derivative = self.derivative + other.derivative
        except AttributeError:
            value = self.value + other
            derivative = self.derivative
        return Dual(value, derivative)

    def __radd__(self,other):
        
        """
        Adds a Dual object, float, or int and self.
         
        INPUTS:
        self (Dual object) - to add
        other (Dual object, float, or int) - to add
        
        OUTPUT: Dual object that is the sum of self and other
        
        EXAMPLES:
        
        Dual + Dual:
        >>> Dual(5, 2) + Dual(3, 1)
        Dual('value': 8, 'derivative': 3)

        float + Dual:
          >>> 3.0 + Dual(5, 2)
        Dual('value': 8.0, 'derivative': 2)
      
        int + Dual:
        >>> 3 + Dual(5, 2)
        Dual('value': 8, 'derivative': 2)
      
            For multivariate functions:
        >>> Dual(5, 2, index = 0, total = 2) + Dual(10, 1, index = 1, total = 2)
        Dual('value': 15, 'derivative': [2, 1])
        """
        
        return self.__add__(other)

    def __sub__(self,other):
        
        """
        Subtracts a Dual object, float, or int from self.
         
        INPUTS:
        self (Dual object) - to subtract from
        other (Dual object, float, or int) - to subtract
        
        OUTPUT: Dual object that is the subtraction of other from self
        
        EXAMPLES:
        
        Dual - Dual:
        >>> Dual(5, 2) - Dual(3, 1)
        Dual('value': 2, 'derivative': -1)

        Dual - float:
          >>> Dual(5, 2) - 3.0
        Dual('value': 2.0, 'derivative': 2)
      
            Dual - int:
          >>> Dual(5, 2) - 3
        Dual('value': 2, 'derivative': 2)
      
            For multivariate functions:
        >>> Dual(5, 2, index = 0, total = 2) - Dual(10, 1, index = 1, total = 2)
        Dual('value': -5, 'derivative': [2, 1])
        """
        
        try:
            value = self.value - other.value
            derivative = self.derivative - other.derivative
        except AttributeError:
            value = self.value - other
            derivative = self.derivative
        return Dual(value, derivative)
        # try:
        #     value = self.value - other.value
        #     derivative = self.derivative - other.derivative
        # except AttributeError:
        #     value = self.value - other
        #     derivative = self.derivative
        # return Dual(value, derivative)

    def __rsub__(self,other):
        
        """
        Subtracts self from a Dual object, float, or int.
         
        INPUTS:
        self (Dual object) - to subtract
        other (Dual object, float, or int) - to subtract from
        
        OUTPUT: Dual object that is the subtraction of self from other
        
        EXAMPLES:
        
        Dual - Dual:
        >>> Dual(5, 2) - Dual(3, 1)
        Dual('value': 2, 'derivative': -1)

        float - Dual:
          >>> 3.0 - Dual(5, 2)
        Dual('value': -2.0, 'derivative': 2)
      
        int - Dual:
        >>> 3 - Dual(5, 2)
        Dual('value': -2, 'derivative': 2)
      
        For multivariate functions:
        >>> Dual(5, 2, index = 0, total = 2) - Dual(10, 1, index = 1, total = 2)
        Dual('value': -5, 'derivative': [2, 1])
        """
        
        return -(self.__sub__(other))

    def __neg__(self):
        
        """
        Returns the negative of the self.
         
        INPUTS:
        self (Dual object) - to make negative
        
        OUTPUT: Dual object that is the negative of the self
        
        EXAMPLES:
        
        >>> Dual(5, 2)
        Dual('value'-5: , 'derivative': -2)

        >>> Dual([1, 2, 3], [2, 4, 6])
        Dual('value':[-1, -2, -3] , 'derivative': [-2, -4, -6])
        """
        
        value = -self.value
        derivative = -self.derivative
        return Dual(value,derivative)  

    def __mul__(self,other):
        
        """
        Multiplies self and a Dual object, float, or int.
         
        INPUTS:
        self (Dual object) - to multiply 
        other (Dual object, float, or int) - to multiply
        
        OUTPUT: Dual object that is the multiplication of self and other
        
        EXAMPLES:
        
        Dual * Dual:
        >>> Dual(5, 2) * Dual(3, 1)
        Dual('value': 15, 'derivative': 2)

        float * Dual:
        >>> 3.0 * Dual(5, 2)
        Dual('value': 15.0, 'derivative': 6.0)
      
        int * Dual:
        >>> 3 * Dual(5, 2)
        Dual('value': 15, 'derivative': 6)
        """

        try:
            value = self.value * other.value
            derivative = self.derivative * other.value + self.value * other.derivative
        except AttributeError:
            value = self.value * other
            derivative = self.derivative * other
        return Dual(value,derivative)

    def __rmul__(self,other):

        """
        Multiplies a Dual object, float, or int and self.
         
        INPUTS:
        self (Dual object) - to multiply 
        other (Dual object, float, or int) - to multiply
        
        OUTPUT: Dual object that is the multiplication of self and other
        
        EXAMPLES:
        
        Dual * Dual:
        >>> Dual(5, 2) * Dual(3, 1)
        Dual('value': 15, 'derivative': 2)

        Dual * float:
        >>> Dual(5, 2) * 3.0
        Dual('value': 15.0, 'derivative': 6.0)
      
        Dual * int:
        >>> Dual(5, 2) * 3
        Dual('value': 15, 'derivative': 6)
        """

        return self.__mul__(other)

    def __truediv__(self,other):

        """
        Divides self by a Dual object, float, or int.
         
        INPUTS:
        self (Dual object) - to divide
        other (Dual object, float, or int) - to divide by
        
        OUTPUT: Dual object that is the division of self by other
        
        EXAMPLES:
        
        Dual / Dual:
        >>> Dual(1, 2, index = 0, total = 2) / Dual(2, 2, index = 1, total = 2)
        Dual('value': 0.5, 'derivative': [0.5, -0.5])

        Dual / float:
        >>> Dual(1, 1) / 2.0
        Dual('value': 0.5, 'derivative': -0.5)
      
        Dual / int:
        >>> Dual(1, 1) / 2
        Dual('value': 0.5, 'derivative': -0.5)
        """

        try:
            value=self.value/other.value
            derivative=(self.derivative*other.value-self.value*other.derivative)/(other.value)**2
        except AttributeError:
            value=self.value/other
            derivative=self.derivative/other
        return Dual(value, derivative)

    def __rtruediv__(self,other):
        
        """
        Divides a Dual object, float, or int by self
         
        INPUTS:
        self (Dual object) - to divide by
        other (Dual object, float, or int) - to divide
        
        OUTPUT: Dual object that is the division of self by other
        
        EXAMPLES:
        
        Dual / Dual:
        >>> Dual(1, 2, index = 0, total = 2) / Dual(2, 2, index = 1, total = 2)
        Dual('value': 0.5, 'derivative': [0.5, -0.5])

        float / Dual:
        >>> 2.0 / Dual(1, 1)
        Dual('value': 2.0, 'derivative': -2.0)
      
        int / Dual:
        >>> 2 / Dual(1, 1)
        Dual('value': 2, 'derivative': -2)
        """

        if self.value==0: raise ZeroDivisionError
        value=other/self.value
        derivative=-other * self.derivative / self.value ** 2
        return Dual(value,derivative)

    def __pow__(self,other):

        """
        Raises a Dual object to the power of a Dual object, float, or int 
         
        INPUTS:
        self (Dual object) - base
        other (Dual object, float, or int) - power to raise to
        
        OUTPUT: Dual object that is the self raised to the power of the other
        
        EXAMPLES:
        
        Dual ** Dual:
        >>> Dual(2, 2,index = 0,total = 2) ** Dual(3, 3,index = 1,total = 2)
        Dual('value': 8, 'derivative': [24, 8*np.log(2)*3])

        Dual ** float:
        >>> Dual(2, 2) ** 2.0
        Dual('value': 4.0, 'derivative': 8.0)
      
        Dual ** int:
        >>> Dual(2, 2) ** 2
        Dual('value': 4, 'derivative': 8)
        """

        value_base = self.value
        derivative_base = self.derivative
        if value_base < 0 and 0<other<1: raise ValueError('Cannot take power of non-positive values')
        if value_base == 0 and other < 1: raise ZeroDivisionError

        try:
            value=value_base**other.value
            derivative=value*(other.derivative*np.log(value_base)+other.value*derivative_base/value_base)
            return Dual(value,derivative)
            
        except AttributeError:
            value = value_base**other
            derivative = other * derivative_base * value_base**(other - 1)
            return Dual(value,derivative)    

    def __rpow__(self,other):

        """
        Raises a Dual object, float, or int to the power of a Dual object
         
        INPUTS:
        self (Dual object) - base
        other (Dual object, float, or int) - power to raise to
        
        OUTPUT: Dual object that is the self raised to the power of the other
        
        EXAMPLES:
        
        Dual ** Dual:
        >>> Dual(2, 2,index = 0,total = 2) ** Dual(3, 3,index = 1,total = 2)
        Dual('value': 8, 'derivative': [24, 8*np.log(2)*3])

        float ** Dual:
        >>> 2.0 ** Dual(2, 2)
        Dual('value': 4.0, 'derivative': np.log(2)*4*2)
      
        int ** Dual:
        >>> 2 ** Dual(2, 2)
        Dual('value': 4, 'derivative': np.log(2)*4*2)
        """

        value=other**self.value
        derivative = np.log(other) * other ** self.value * self.derivative
        return Dual(value,derivative)


    def __lt__(self,other):

        """
        Decides if self is less than a Dual object, float, or int
        When compared to float or int, return False all the time

        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is less than other
        
        EXAMPLES:
        
        Dual < Dual:
        >>> Dual(1,1) < Dual(2,2)
        True
        >>> Dual(2,2) < Dual(1,1)
        False

        Dual < float:
        >>> Dual(1,1) < 2.0
        False
        >>> Dual(1,1) < 0.0
        False
      
        Dual < int:
        >>> Dual(1,1) < 2
        False
        >>> Dual(1,1) < 0
        False
        """

        try:
            if (self.value < other.value) and (self.derivative < other.derivative):
                return True
            else:
                return False
        except AttributeError:
                return False

    def __le__(self, other):

        """
        Decides if self is less than or equal to a Dual object, float, or int
        When compared to float or int, return False all the time   

        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is less than or equal to other
        
        EXAMPLES:
        
        Dual < Dual:
        >>> Dual(1,1) <= Dual(2,2)
        True
        >>> Dual(1,1) <= Dual(1,1)
        True
        >>> Dual(2,2) <= Dual(1,1)
        False

        Dual < float:
        >>> Dual(1,1) <= 2.0
        False
        >>> Dual(1,1) <= 1.0
        False
        >>> Dual(1,1) <= 0.0
        False
      
        Dual < int:
        >>> Dual(1,1) <= 2
        False
        >>> Dual(1,1) <= 1
        False
        >>> Dual(1,1) <= 0
        False
        """

        try:
            if (self.value <= other.value) and (self.derivative <= other.derivative):
                return True
            else:
                return False
        except AttributeError:
                return False

    def __gt__(self,other):

        """
        Decides if self is greater than a Dual object, float, or int
        When compares to float or int, return False all the time    

        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is greater than other
        
        EXAMPLES:
        
        Dual > Dual:
        >>> Dual(1,1) > Dual(2,2)
        False
        >>> Dual(2,2) > Dual(1,1)
        True

        Dual > float:
        >>> Dual(1,1) > 2.0
        False
        >>> Dual(1,1) > 0.0
        False
      
        Dual > int:
        >>> Dual(1,1) > 2
        False
        >>> Dual(1,1) > 0
        False
        """

        try:
            if (self.value > other.value) and (self.derivative > other.derivative):
                return True
            else:
                return False
        except AttributeError:
                return False

    def __ge__(self, other):

        """
        Decides if self is greater than or equal to a Dual object, float, or int
        When compares to float or int, return False all the time

        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is greater or equal to than other
        
        EXAMPLES:
        
        Dual >= Dual:
        >>> Dual(1,1) >= Dual(2,2)
        False
        >>> Dual(1,1) >= Dual(1,1)
        True
        >>> Dual(2,2) >= Dual(1,1)
        True

        Dual >= float:
        >>> Dual(1,1) >= 2.0
        False
        >>> Dual(1,1) >= 1.0
        False
        >>> Dual(1,1) >= 0.0
        False
      
        Dual >= int:
        >>> Dual(1,1) >= 2
        False
        >>> Dual(1,1) >= 1
        False
        >>> Dual(1,1) >= 0
        False
        """

        try:
            if (self.value >= other.value) and (self.derivative >= other.derivative):
                return True
            else:
                return False
        except AttributeError:
                return False

    def __eq__(self, other):

        """
        Decides if self is equal to a Dual object, float, or int
        When compares to float or int, return False all the time 

        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is equal to other
        
        EXAMPLES:
        
        Dual = Dual:
        >>> Dual(1,1) = Dual(2,2)
        False
        >>> Dual(1,1) = Dual(1,1)
        True
        >>> Dual(2,2) = Dual(1,1)
        False

        Dual = float:
        >>> Dual(1,1) = 2.0
        False
        >>> Dual(1,1) = 1.0
        False
        >>> Dual(1,1) = 0.0
        False
      
        Dual = int:
        >>> Dual(1,1) = 2
        False
        >>> Dual(1,1) = 1
        False
        >>> Dual(1,1) = 0
        False
        """
        
        try:
            if (self.value == other.value) and (self.derivative == other.derivative):
                return True
            else:
                return False
        except AttributeError:
                return False

    def __ne__(self,other):

        """
        Decides if self is not equal to a Dual object, float, or int
              
        INPUTS:
        self (Dual object)
        other (Dual object, float, or int)
        
        OUTPUT: Boolean indicating whether self is not equal to other
        
        EXAMPLES:
        
        Dual != Dual:
        >>> Dual(1,1) != Dual(2,2)
        True
        >>> Dual(1,1) != Dual(1,1)
        False
        >>> Dual(2,2) != Dual(1,1)
        True

        Dual != float:
        >>> Dual(1,1) != 2.0
        True
        >>> Dual(1,1) != 1.0
        True
        >>> Dual(1,1) != 0.0
        True
      
        Dual != int:
        >>> Dual(1,1) != 2
        True
        >>> Dual(1,1) != 1
        True
        >>> Dual(1,1) != 0
        True
        """

        try:
            if (self.value == other.value) and (self.derivative == other.derivative):
                return False
            else:
                return True
        except AttributeError:
                return True