import math
from collections import defaultdict
import numpy as np
from .math_defs import Dual

class AD:
    def __init__(self, n_variables):
        self.n_variables = n_variables
        self.curr_n_variable = 0
        self.int_to_dual_mapping = {}
        for i in range(0,n_variables):
            self.int_to_dual_mapping[i] = None

    def create_variable(self,val):
        if self.curr_n_variable >= self.n_variables:
            raise ValueError #fix this: more info can be added
        vector = np.zeros(self.n_variables)
        vector[self.curr_n_variable] = 1
        variable = Dual(val, vector)
        self.int_to_dual_mapping[self.curr_n_variable]=variable
        self.curr_n_variable = self.curr_n_variable+1
        return variable

    def reverse_mode_compute_gradients(self, variable, path, gradients):
        if variable.dual is None:
            pass
        else:
            for child, partial in variable.dual:
                if partial != -math.inf:
                    # "Multiply the edges of a path":
                    path_to_child = path * partial
                    # "Add together the different paths":
                    gradients[child] += path_to_child
                    # recurse through graph:
                    self.reverse_mode_compute_gradients(child, path_to_child, gradients)

    def reverse_mode_gradients(self,variable: Dual):
        gradients = defaultdict(lambda: 0)
        self.reverse_mode_compute_gradients(variable, 1, gradients)
        return gradients


    def forward_mode_gradients(self,variable: Dual):
        gradients = defaultdict(lambda: 0)
        for i in range(0,self.n_variables):
            gradients[self.int_to_dual_mapping[i]]=variable.vector[i]
        return gradients

    def exp(self,val):
        #check the type of other and create a Dual class object with its value
       #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        real= np.exp(val.real)
        vec = np.exp(val.real)*val.vector #check this
        dual= ((val, np.exp(val.real)),(val,-math.inf))
        #return a new dual class object after division
        return Dual(
            real,
            vec,
            dual
        )

    def ln(self,val):
        #check the type of other and create a Dual class object with its value
       #check the type of other and create a Dual class object with its value
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin
        real= np.log(val.real)
        vec = (1/val.real)*val.vector #check this
        dual= ((val, 1/val.real),(val,-math.inf))
        #return a new dual class object after division
        return Dual(
            real,
            vec,
            dual
        )

    def log(self,val, base): #fix this: do we need separate vector for val and base
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))

        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(base, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                base.__class__.__name__))

        #check the type of other and create a Dual class object with its value
        if isinstance(base, float) or isinstance(base, int):
            base = Dual(base, np.zeros(len(self.vector)))
        #raise type error when the type of other is wrong
        if not isinstance(base, Dual):
            raise TypeError(
            'unsupported operand type(s) for pow: \'{}\' and \'{}\''.format(
            self.__class__.__name__, base.__class__.__name__))


        real = np.log(val.real)/np.log(base.real)
        vec = (1/(np.log(base)*val.real))*val.vector
        dual = ((val,1/(np.log(base.real)*val.real)),(base,(-np.log(val.real))/(base.real*(np.log(base.real))**2)))

        #return a new dual class object after pow
        return Dual(
            real,
            vec,
            dual
        )

    def sqrt(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))

        real = np.sqrt(val.real)
        vec = (1/2)*np.sqrt(val.real)*val.vector
        dual = ((val, (1/2)*np.sqrt(val.real)),(val,-math.inf))

        #return a new dual class object after pow
        return Dual(
            real,
            vec,
            dual
        )

    def sin(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin

        real= np.sin(val.real)
        vec = np.cos(val.real)*val.vector
        dual= ((val,np.cos(val.real)),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def cos(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))

        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for cos: \'{}\''.format(
                val.__class__.__name__))

        real= np.cos(val.real)
        vec = -1*np.sin(val.real)*val.vector
        dual= ((val, -1*np.sin(val.real)),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def tan(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))

        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for tan: \'{}\''.format(
                val.__class__.__name__))

        if np.cos(val.real) == 0:
            raise ValueError(
                'Invalid input value for tan: \'{}\''.format(
                val.real
            ))

        real = np.tan(val.real)
        vec = (1/np.cos(val.real)**2)*val.vector
        dual= ((val, 1/np.cos(val.real)**2),(val,-math.inf))
        #return dual class object for tan
        return Dual(
            real,
            vec,
            dual
        )

    def arcsin(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin
        if abs(val.real) >= 1:
            raise ValueError(
                'Invalid input value for arcsin: \'{}\''.format(
                val.real
            ))
        real= np.arcsin(val.real)
        vec = 1/np.sqrt(1-val.real**2)*val.vector
        dual= ((val,1/np.sqrt(1-val.real**2)),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def arccos(self,val):
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin
        if abs(val.real) >= 1:
            raise ValueError(
                'Invalid input value for tan: \'{}\''.format(
                val.real
            ))
        real= np.arccos(val.real)
        vec = -1/np.sqrt(1-val.real**2)*val.vector
        dual= ((val,-1/np.sqrt(1-val.real**2)),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def arctan(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin

        real= np.arctan(val.real)
        vec = 1/np.sqrt(1+val.real**2)*val.vector
        dual= ((val,1/np.sqrt(1+val.real**2)),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def sinh(self,val):
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for sin: \'{}\''.format(
                val.__class__.__name__))
        #return dual class object for sin

        real= (np.exp(val.real) - np.exp(-1*val.real))/2
        vec = ((np.exp(val.real) + np.exp(-1*val.real))/2)*val.vector
        dual= ((val, (np.exp(val.real) + np.exp(-1*val.real))/2),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def cosh(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for cos: \'{}\''.format(
                val.__class__.__name__))

        real= (np.exp(val.real) + np.exp(-1*val.real))/2
        vec = ((np.exp(val.real) - np.exp(-1*val.real))/2)*val.vector
        dual= ((val, (np.exp(val.real) - np.exp(-1*val.real))/2),(val,-math.inf))
        return Dual(
            real,
            vec,
            dual
        )

    def tanh(self,val):
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for tan: \'{}\''.format(
                val.__class__.__name__))

        if math.cosh(val.real) == 0:
            raise ValueError('Invalid input value for tanh: \'{}\''.format(
                val.real))
        real= math.sinh(val.real)/math.cosh(val.real)
        x= val.real
        vec = ((math.cosh(x)*math.cosh(x) - math.sinh(x)*math.sinh(x) )/math.cosh(x)**2)*val.vector
        dual= ((val, (math.cosh(x)*math.cosh(x) - math.sinh(x)*math.sinh(x) )/math.cosh(x)**2),(val,-math.inf))
        #return dual class object for tan
        return Dual(
            real,
            vec,
            dual
        )

    def trace(self,f,mode = 'forward', seed  = None):
        vars = self.int_to_dual_mapping.values()
        d = f(*vars)
        result = []
        base_seed = []
        for var in vars:
            base_seed.append(var.vector)
        base_seed = np.array(base_seed)
        if seed is None:
            seed = base_seed
        else:
            seed = np.array(seed)
            if seed.shape != base_seed.shape:
                raise ValueError('Incorrect shape for seed vector! Expecting a n*n matrix')

        for i in d:
            if mode == 'forward':
                result.append(i.vector)
            elif mode == 'reverse':
                temp = []
                for var in vars:
                    partial = self.get_gradient(i,var,mode=mode)
                    temp.append(partial)
                result.append(temp)
            else:
                raise ValueError('Incorrect Input for mode')
        return np.array(result)@seed

    def get_gradient(self,target,var,mode = 'forward'):
        if mode == 'forward':
            gradients = self.forward_mode_gradients(target)
        elif mode == 'reverse':
            gradients = self.reverse_mode_gradients(target)
        else:
            raise ValueError('Incorrect Input for mode')
        if target == var:
            return gradients.get(var,1)
        else:
            return gradients.get(var,0)
