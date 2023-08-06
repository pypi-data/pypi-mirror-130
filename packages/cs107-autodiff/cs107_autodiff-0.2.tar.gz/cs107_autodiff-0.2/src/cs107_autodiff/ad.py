from collections import defaultdict
import math
import numpy as np
from .math_defs import Dual

class AD:
#Credit for algorithm for reverse mode: https://sidsite.com/posts/autodiff/
    def __init__(self, n_variables):
        """Creates the AD class

        Args:
            n_variables (int): number of variable for use
        """
        self.n_variables = n_variables
        self.curr_n_variable = 0
        self.int_to_dual_mapping = {}
        for i in range(0,n_variables):
            self.int_to_dual_mapping[i] = None

    def create_variable(self,val):
        """Creates a variable for the AD class

        Args:
            val (float): value for variable

        Returns:
            Dual representing the variable.
        """
        if self.curr_n_variable >= self.n_variables:
            raise ValueError #fix this: more info can be added
        vector = np.zeros(self.n_variables)
        vector[self.curr_n_variable] = 1
        variable = Dual(val, vector)
        self.int_to_dual_mapping[self.curr_n_variable]=variable
        self.curr_n_variable = self.curr_n_variable+1
        return variable

    def reverse_mode_compute_gradients(self, variable, path, gradients):
        """Computes gradients using reverse mode

        Args:
            variable (Dual): variable to calculate gradient for
            path:
            gradients (dict): dictionary of gradient values
        """
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
        """Computes and retrieves gradients using reverse mode

        Args:
            variable (Dual): variable to calculate gradient for

        Returns: dictionary of gradient values
        """
        gradients = defaultdict(lambda: 0)
        self.reverse_mode_compute_gradients(variable, 1, gradients)
        return gradients


    def forward_mode_gradients(self,variable: Dual):
        """Retrieves gradients using forward mode.

        Args:
            variable (Dual): variable to calculate gradient for

        Returns: dictionary of gradient values
        """
        gradients = defaultdict(lambda: 0)
        for i in range(0,self.n_variables):
            gradients[self.int_to_dual_mapping[i]]=variable.vector[i]
        return gradients

    def exp(self,val):
        """Unary operator for exp function

        Args:
            val (float/int/Dual): Dual to raise e to.

        Returns:
            Dual of the result of the exp operation
        """
        #check the type of other and create a Dual class object with its value
       #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for exp: \'{}\''.format(
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
        """Unary operator for natural log function

        Args:
            val (float/int/Dual): Dual to take natural log of

        Returns:
            Dual of the result of the natural log function
        """
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
        """Binary operator for log function using a base

        Args:
            val (float/int/Dual): value to take log of
            base (float/int/Dual): base with which to the the log

        Returns:
            Dual of the result of the log operation
        """
        #check the type of other and create a Dual class object with its value
        if isinstance(val, float) or isinstance(val, int):
            val = Dual(val, vector=np.zeros(self.n_variables))
        #raise type error when the type is wrong
        if not isinstance(val, Dual):
            raise TypeError(
                'unsupported operand type for log: \'{}\''.format(
                val.__class__.__name__))
        #check the type of other and create a Dual class object with its value
        if isinstance(base, float) or isinstance(base, int):
            base = Dual(base, np.zeros(self.n_variables))
        #raise type error when the type of other is wrong
        if not isinstance(base, Dual):
            raise TypeError(
            'unsupported operand type(s) for log: \'{}\' and \'{}\''.format(
            self.__class__.__name__, base.__class__.__name__))


        real = np.log(val.real)/np.log(base.real)
        vec = (1/(np.log(base.real)*val.real))*val.vector+(-np.log(val.real))/(base.real*(np.log(base.real))**2) *base.vector
        dual = ((val,1/(np.log(base.real)*val.real)),(base,(-np.log(val.real))/(base.real*(np.log(base.real))**2)))

        #return a new dual class object after pow
        return Dual(
            real,
            vec,
            dual
        )

    def sqrt(self,val):
        """Unary operator for square root function

        Args:
            val (float/int/Dual):value to take sqrt of.

        Returns:
            Dual of the result of the sqrt operation
        """
        #check the type of other and create a Dual class object with its value
        return val**0.5

    def sin(self,val):
        """Unary operator for sin function

        Args:
            val (float/int/Dual): Value to take sin of

        Returns:
            Dual of the result of the sin operation
        """
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
        """Unary operator for cos function

        Args:
            val (float/int/Dual): Value to take cos of

        Returns:
            Dual of the result of the cos operation
        """
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
        """Unary operator for tan function

        Args:
            val (float/int/Dual): Value to take tan of

        Returns:
            Dual of the result of the tan operation
        """
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
        """Unary operator for arcsin function

        Args:
            val (float/int/Dual): Value to take arcsin of

        Returns:
            Dual of the result of the arcsin operation
        """
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
        """Unary operator for arccos function

        Args:
            val (float/int/Dual): Value to take arccos of

        Returns:
            Dual of the result of the arccos operation
        """
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
        """Unary operator for arctan function

        Args:
            val (float/int/Dual): Value to take arctan of

        Returns:
            Dual of the result of the arctan operation
        """
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
        """Unary operator for sinh function

        Args:
            val (float/int/Dual): Value to take sinh of

        Returns:
            Dual of the result of the sinh operation
        """
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
        """Unary operator for cosh function

        Args:
            val (float/int/Dual): Value to take cosh of

        Returns:
            Dual of the result of the cosh operation
        """
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
        """Unary operator for tanh function

        Args:
            val (float/int/Dual): Value to take tanh of

        Returns:
            Dual of the result of the tanh operation
        """
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
        """Computes the trace of a function with optional seed values

        Args:
            f (Dual): function to take the trace of,
            mode (str): string indicating forward or reverse mode for trace computation
            seed ([[]]): matrix of seed values for f

        Returns:
            Trace of the function with respect to its seed values
        """
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
        """Gets the gradient of a function given a specific variable

        Args:
            target (Dual): target to compute the gradients of
            var (Dual): Specific variable to retrieve gradients of
            mode (str): string indicating the use of reverse or foward mode for calculation
        """
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
