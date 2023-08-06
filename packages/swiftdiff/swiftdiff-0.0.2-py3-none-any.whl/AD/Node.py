import numpy as np
class Node:
    """
    Here we are creating a Node Class to fuel Automatic Differentation (reverse).

    ATTRIBUTES:
    value (int or float) - value of the user-inputted variable
    """
    def __init__(self, value):
        """
        Initiates an instance of the Node class.
        
        INPUTS:
        value (int or float) - value of the user-inputted variable
        """
        self.value = value
        self.derivative = None
        self.children = [] 
        
    def __repr__(self): 
        
        """
        Prints information about the Node class instance.
         
        EXAMPLES:
        
        >>> Node(1)
        Node({'value': 1, 'derivative': None, 'children': []})
        """
        
        return "{class_name}({attributes})".format(class_name = type(self).__name__, attributes = self.__dict__)

    def der(self):
        """
        Calculates the derivatives
        
        None will convert to 0

        EXAMPLES:
        
        >>> Node(1).der()
        0
        """

        if self.derivative is None:         
            total=0
            for node,d in self.children:
                    total=total+d*node.der()
            self.derivative = total
        return self.derivative

    def __add__(self, other):
        """
        Adds self and a Node object, float, or int.
         
        INPUTS:
        self (Node object) - to add
        other (Node object, float, or int) - to add
        
        OUTPUT: Node object that is the sum of self and other
        
        EXAMPLES:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>> y=x1+x1+x2
        >>> y.derivative=1
        >>>y.value
        >>>3
        >>>x1.der()
        >>>2
        >>>x2.der()
        >>>1

        """
        node = Node(0)
        try:
            node.value = self.value+other.value
        except AttributeError:
            other=Node(other)
            node.value = self.value+other.value
        self.children.append((node,1))
        other.children.append((node,1))        
        return node

    def __radd__(self, other):
        """
        Adds a Node object, float, or int and self.
         
        INPUTS:
        self (Node object) - to add
        other (Node object, float, or int) - to add
        
        OUTPUT: Node object that is the sum of self and other
        
        EXAMPLES:
        Node + Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x2+x1
        >>>y.derivative=1
        >>>y.value
        >>>3
        >>>x1.der()
        >>>1
        >>>x2.der()
        >>>1    

        int + Node:
        >>> y=3 + x1
        >>>y.derivative=1
        >>>y.value
        >>>4
        >>>x1.der()=1
 
        """
        other = Node(other)
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtracts a Node object, float, or int from self.
         
        INPUTS:
        self (Node object) - to subtract from
        other (Node object, float, or int) - to subtract
        
        OUTPUT: Node object that is the subtraction of other from self
        
        EXAMPLES:

        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x1-x1-x2
        >>>y.derivative=1
        >>>y.value
        >>>-2
        >>>x1.der()
        >>>0
        >>>x2.der()
        >>>-1
        """
        node = Node(0)
        try:
            node.value = self.value-other.value
        except AttributeError:
            other=Node(other)
            node.value = self.value-other.value
        self.children.append((node,1))
        other.children.append((node,-1))        
        return node

    def __rsub__(self, other):

        """
        Subtracts self from a Node object, float, or int.
         
        INPUTS:
        self (Node object) - to subtract
        other (Node object, float, or int) - to subtract from
        
        OUTPUT: Node object that is the subtraction of self from other
        
        EXAMPLES:
        
        Node - Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x2-x1
        >>>y.derivative=1
        >>>y.value
        >>>`
        >>>x1.der()
        >>>-1
        >>>x2.der()
        >>>1  

      
        int - Node:
        >>> y=3 - x1
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()=-1
        """
        
        try:
            node = Node(other.value - self.value)
        except AttributeError:
            other=Node(other)
            node = Node(other.value - self.value)
        self.children.append((node,-1)) 
        other.children.append((node,1))   
        return node

    def __neg__(self):
        """
        Returns the negative of the self.
         
        INPUTS:
        self (Node object) - to make negative
        
        OUTPUT: Node object that is the negative of the self
        
        EXAMPLES:
        
        >>>x1=Node(1)
        >>>y=-x1
        >>>y.derivative=1
        >>>y.value
        >>>-1
        >>>x.der()
        >>>-1
        """
        node=Node(-self.value)
        self.children.append((node,-1)) 
        return node

    def __mul__(self, other):
        """
        Multiplies self and a Node object, float, or int.
         
        INPUTS:
        self (Node object) - to multiply 
        other (Node object, float, or int) - to multiply
        
        OUTPUT: Node object that is the multiplication of self and other
        
        EXAMPLES:
        
        Node * Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x1*x2
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()=2
        >>>x2.der()=1  

      
        int * Node:
        >>>x1=Node(1)
        >>>y=x1*2
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()
        >>>2

        """
        node=Node(0)
        try:
            node.value=self.value * other.value
        except AttributeError:
            other=Node(other)
            node.value=self.value*other.value
        self.children.append((node,other.value))
        other.children.append((node,self.value))
        return node

    def __rmul__(self, other):
        """
        Multiplies a Node object, float, or int and self.
         
        INPUTS:
        self (Node object) - to multiply 
        other (Node object, float, or int) - to multiply
        
        OUTPUT: Node object that is the multiplication of self and other
        
        EXAMPLES:
        
        Node * Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x2*x1
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()
        >>>1
        >>>x2.der()
        >>>2 
 
        Node * int:
        >>>x1=Node(1)
        >>>y=2*x1
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()
        >>>2
        """
        other = Node(other)
        return self.__mul__(other)


    def __truediv__(self, other):
        """
        Divides self by a Node object, float, or int.
         
        INPUTS:
        self (Node object) - to divide
        other (Node object, float, or int) - to divide by
        
        OUTPUT: Node object that is the division of self by other
        
        EXAMPLES:
        
        Node / Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x1/x2
        >>>y.derivative=1
        >>>y.value
        >>>0.5
        >>>x1.der()
        >>>0.5
        >>>x2.der()
        >>>-0.25  

        Node / int:
        >>>x1=Node(1)
        >>>y=x1/2
        >>>y.derivative=1
        >>>y.value
        >>>0.5
        >>>x1.der()
        >>>0.5
        """

        return self * (other ** (-1))
    
    def __rtruediv__(self, other):
        """
        Divides a Node object, float, or int by self
         
        INPUTS:
        self (Node object) - to divide by
        other (Node object, float, or int) - to divide
        
        OUTPUT: Node object that is the division of self by other
        
        EXAMPLES:
        
        Node / Node:
        >>>x1=Node(1)
        >>>x2=Node(2) 
        >>>y=x2/x1
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()
        >>>1
        >>>x2.der()
        >>>-2 

        Node / int:
        >>>x1=Node(1)
        >>>y=2/x1
        >>>y.derivative=1
        >>>y.value
        >>>2
        >>>x1.der()
        >>>-2
        """

        return other * (self ** (-1))


    def __pow__(self, other):
        """
        Raises a Node object to the power of a Node object, float, or int 
         
        INPUTS:
        self (Node object) - base
        other (Node object, float, or int) - power to raise to
        
        OUTPUT: Node object that is the self raised to the power of the other
        
        EXAMPLES:
        
        Node ** Node:
        >>>x1=Node(2)
        >>>x2=Node(3) 
        >>>y=x1**x2
        >>>y.derivative=1
        >>>y.value
        >>>8
        >>>x1.der()
        >>>12
        >>>x2.der()
        >>>8*np.log(2)
 
        Node ** int:
        >>>x1=Node(2)
        >>>y=x1**2
        >>>y.derivative=1
        >>>y.value
        >>>4
        >>>x1.der()
        >>>4
        """

        node=Node(0)
        try:
            node.value=self.value**other.value
        except AttributeError:
            other=Node(other)
            node.value=self.value**other.value

        self.children.append((node,other.value*self.value**(other.value-1)))
        other.children.append((node,(self.value**other.value)*np.log(self.value)))
        return node


    def __rpow__(self, other):
        """
        Raises a Node object to the power of a Node object, float, or int 
         
        INPUTS:
        self (Node object) - base
        other (Node object, float, or int) - power to raise to
        
        OUTPUT: Node object that is the self raised to the power of the other
        
        EXAMPLES:
        
        Node ** Node:
        >>>x1=Node(2)
        >>>x2=Node(3) 
        >>>y=x2**x1
        >>>y.derivative=1
        >>>y.value
        >>>9
        >>>x1.der()
        >>>9*np.log(3)
        >>>x2.der()
        >>>6
 
        Node ** int:
        >>>x1=Node(2)
        >>>y=2**x1
        >>>y.derivative=1
        >>>y.value
        >>>4
        >>>x1.der()
        >>>4*np.log(2)
        """
        if not isinstance(other,Node):
            other = Node(other)
        return other.__pow__(self)

    def __lt__(self,other):
        """
        Decides if self is less than a Node object, float, or int
        When compares to float or int, return False all the time

        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is less than other
        
        EXAMPLES:
        
        Node < Node:
        >>> Node(1,1) < Node(2,2)
        True
        >>> Node(2,2) < Node(1,1)
        False

        Node < float:
        >>> Node(1,1) < 2.0
        False
        >>> Node(1,1) < 0.0
        False
      
        Node < int:
        >>> Node(1,1) < 2
        False
        >>> Node(1,1) < 0
        False
        """
        try:
            checkself=self.der()
            checkother=other.der()
            if (checkself and not checkother) or (not checkself and checkother):
                return False
            else:
                if self.value < other.value:
                    if checkself :
                      return (checkself<checkother)
      
                    else: 
                        return True
                else:

                    return False
            
        except AttributeError:
            return False

    def __le__(self, other):
        """
        Decides if self is less than or equal to a Node object, float, or int
        When compares to float or int, return False all the time   

        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is less than or equal to other
        
        EXAMPLES:
        
        Node < Node:
        >>> Node(1,1) <= Node(2,2)
        True
        >>> Node(1,1) <= Node(1,1)
        True
        >>> Node(2,2) <= Node(1,1)
        False

        Node < float:
        >>> Node(1,1) <= 2.0
        False
        >>> Node(1,1) <= 1.0
        False
        >>> Node(1,1) <= 0.0
        False
      
        Node < int:
        >>> Node(1,1) <= 2
        False
        >>> Node(1,1) <= 1
        False
        >>> Node(1,1) <= 0
        False
        """
        try:
            checkself=self.der()
            checkother=other.der()
            if (checkself and not checkother) or (not checkself and checkother):
                return False
            else:
                if self.value <= other.value:
                    if checkself:
                      return (checkself <=checkother)
                    else: return True
                else:
                    return False
        except AttributeError:
            return False

    def __gt__(self,other):
        """
        Decides if self is greater than a Node object, float, or int
        When compares to float or int, return False all the time    

        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is greater than other
        
        EXAMPLES:
        
        Node > Node:
        >>> Node(1,1) > Node(2,2)
        False
        >>> Node(2,2) > Node(1,1)
        True

        Node > float:
        >>> Node(1,1) > 2.0
        False
        >>> Node(1,1) > 0.0
        False
      
        Node > int:
        >>> Node(1,1) > 2
        False
        >>> Node(1,1) > 0
        False
        """
        try:
            checkself=self.der()
            checkother=other.der()
            print(checkself)
            if (checkself and not checkother) or (not checkself and checkother):
                print('jin')
                return False
            else:
                if self.value > other.value:
                    if checkself:
                      return( checkself > checkother)
                         
                    else: return True
                else:
                    return False
        except AttributeError:
            return False

    def __ge__(self, other):


        """
        Decides if self is greater than or equal to a Node object, float, or int
        When compares to float or int, return False all the time

        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is greater or equal to than other
        
        EXAMPLES:
        
        Node >= Node:
        >>> Node(1,1) >= Node(2,2)
        False
        >>> Node(1,1) >= Node(1,1)
        True
        >>> Node(2,2) >= Node(1,1)
        True

        Node >= float:
        >>> Node(1,1) >= 2.0
        False
        >>> Node(1,1) >= 1.0
        False
        >>> Node(1,1) >= 0.0
        False
      
        Node >= int:
        >>> Node(1,1) >= 2
        False
        >>> Node(1,1) >= 1
        False
        >>> Node(1,1) >= 0
        False
        """
        try:
            checkself=self.der()
            checkother=other.der()
            if (checkself and not checkother) or (not checkself and checkother):
                return False
            else:
                if self.value >= other.value:
                    if checkself:
                      return( checkself >= checkother)
                         
                    else: return True
                else:
                    return False
        except AttributeError:
            return False

    def __eq__(self, other):
        """
        Decides if self is equal to a Node object, float, or int
        When compares to float or int, return False all the time 

        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is equal to other
        
        EXAMPLES:
        
        Node = Node:
        >>> Node(1,1) = Node(2,2)
        False
        >>> Node(1,1) = Node(1,1)
        True
        >>> Node(2,2) = Node(1,1)
        False

        Node = float:
        >>> Node(1,1) = 2.0
        False
        >>> Node(1,1) = 1.0
        False
        >>> Node(1,1) = 0.0
        False
      
        Node = int:
        >>> Node(1,1) = 2
        False
        >>> Node(1,1) = 1
        False
        >>> Node(1,1) = 0
        False
        """
        try:
            checkself=self.der()
            checkother=other.der()
            if (checkself and not checkother) or (not checkself and checkother):
                return False
            else:
                if self.value == other.value:
                    if checkself:
                      return( checkself==checkother)
                        
                    else: return True
                else:
                    return False
        except AttributeError:
            return False
        
    def __ne__(self, other):
        """
        Decides if self is not equal to a Node object, float, or int
              
        INPUTS:
        self (Node object)
        other (Node object, float, or int)
        
        OUTPUT: Boolean indicating whether self is not equal to other
        
        EXAMPLES:
        
        Node != Node:
        >>> Node(1,1) != Node(2,2)
        True
        >>> Node(1,1) != Node(1,1)
        False
        >>> Node(2,2) != Node(1,1)
        True

        Node != float:
        >>> Node(1,1) != 2.0
        True
        >>> Node(1,1) != 1.0
        True
        >>> Node(1,1) != 0.0
        True
      
        Node != int:
        >>> Node(1,1) != 2
        True
        >>> Node(1,1) != 1
        True
        >>> Node(1,1) != 0
        True
        """
        return not self.__eq__(other)

 
    
