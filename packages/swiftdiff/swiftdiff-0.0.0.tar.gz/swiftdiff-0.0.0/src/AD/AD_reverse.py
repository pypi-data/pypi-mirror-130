
# base class for autodiff
import numpy as np
from Node import *
from elementary import *


class AutoDiff():
    def __init__(self, f):
        self.f = f if isinstance(f, list) else [f]

# child class inherits from autodiff
class Reverse(AutoDiff):
    def __init__(self,f,variables):
        super().__init__(f)  
        self.variables=variables 
    
    def get_value(self):
        l=[]
        var_list=[]
        for var in self.variables:
            var_list.append(Node(var.value))
        for function in self.f:
            l.append([function(*(var_list)).value])    
        return l
    
    
    def get_jacobian(self):
        l=np.empty((len(self.f),len(self.variables)))
        j_dic={}
        for i in range(len(self.f)):
            j_dic[i]=[]
            for j in range(len(self.variables)):
                node=Node(self.variables[j].value)
                j_dic[i].append(node)

            self.f[i](*(j_dic[i])).derivative= 1

        for i in range(len(self.f)):
            for k in range(len(j_dic[i])):
                node=j_dic[i][k]
                
                l[i,k]=node.der() 
   
        return l
