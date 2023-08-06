#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math

class Dual:
    def __init__(self, real: float, vector = np.array([]), dual=None):
        self.real = real
        self.dual = dual
        self.vector = vector

    def __eq__(self, other):
        if isinstance(other, Dual):
            return (
                self.real == other.real and
                self.dual == other.dual and
                np.array_equal(self.vector, other.vector)
            )

        return False


    def __add__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))
        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for +: \'{}\' and \'{}\''.format(
            self.__class__.__name__, other.__class__.__name__))
        real = self.real + other.real
        vec = self.vector + other.vector
        dual = (
        (self, 1),  # the local derivative with respect to a is 1
        (other, 1)   # the local derivative with respect to b is 1
        )
        # return a new dual class object after addition
        return Dual(
            real,
            vec,
            dual,
        )

    def __mul__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))
        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for *: \'{}\' and \'{}\''.format(
            self.__class__.__name__, other.__class__.__name__))
        real = self.real * other.real
        vec = self.real*other.vector + self.vector*other.real
        dual = (
            (self, other.real),  # the local derivative with respect to a is 1
            (other, self.real)   # the local derivative with respect to b is 1
            )
        #return a new dual class object after multiplication
        return Dual(
            real,
            vec,
            dual
        )

    def __rmul__(self, other):
        # We can do this because multiplication is commutative for scalar
        return self * other

    def __radd__(self, other):
        # We can do this because addition is commutative for scalar
        return self + other

    def __sub__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other,np.zeros(len(self.vector)))

        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for -: \'{}\' and \'{}\''.format(
            self.__class__.__name__, other.__class__.__name__))
        real= self.real-other.real
        vec = self.vector-other.vector
        dual= ((self,1),(other,-1))
        #return a new dual class object after subtraction
        return Dual(
            real,
            vec,
            dual
        )

    def __rsub__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other,np.zeros(len(self.vector)))

        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for -: \'{}\' and \'{}\''.format(
            other.__class__.__name__, self.__class__.__name__))


        real= other.real-self.real
        vec = other.vector-self.vector
        dual= ((self,-1),(other,1))
        #return a new dual class object after subtraction
        return Dual(
            real,
            vec,
            dual
        )


    def __truediv__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))

        #raise type error when the type of other is wrong
        if not isinstance(other, Dual) or other.real == 0:
            raise TypeError(
            'unsupported operand type(s) for /: \'{}\' and \'{}\''.format(
            self.__class__.__name__, other.__class__.__name__))

        real= self.real/other.real
        vec = (1/other.real*self.vector-other.vector*self.real/other.real**2)
        dual= ((self, 1/other.real),(other, -1*self.real*other.real**(-2)))
        #return a new dual class object after division
        return Dual(
            real,
            vec,
            dual
        )

    def __rtruediv__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))

        #raise type error when the type of other is wrong
        if not isinstance(other, Dual) or self.real == 0:
            raise TypeError(
            'unsupported operand type(s) for /: \'{}\' and \'{}\''.format(
            other.__class__.__name__, self.__class__.__name__))

        real= other.real/self.real
        vec = (self.real*other.vector-self.vector*other.real)/self.real**2
        dual= ((self, -1*other.real*self.real**(-2)),(other, 1/self.real))
        #return a new dual class object after division
        return Dual(
            real,
            vec,
            dual
        )


    def __neg__(self):
        #return negative
        return -1.0 * self

    def __pos__(self):
        #return positive
        return 1.0 * self



    def __pow__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))
        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for pow: \'{}\' and \'{}\''.format(
            self.__class__.__name__, other.__class__.__name__))

        if self.real**other.real == 0:
            real= 0
            vec = 0*self.vector
            dual= ((self, 0),(other, 0))
        else:
            real = self.real**other.real
            vec = (self.real**other.real) * ((other.real/self.real*self.vector) + (other.vector* math.log(self.real)))
            dual = ((self, other.real*self.real**(other.real-1)),(other, self.real**other.real*np.log(self.real)))

        #return a new dual class object after pow
        return Dual(
            real,
            vec,
            dual
        )

    def __rpow__(self, other):
        #check the type of other and create a Dual class object with its value
        if isinstance(other, float) or isinstance(other, int):
            other = Dual(other, np.zeros(len(self.vector)))
        #raise type error when the type of other is wrong
        if not isinstance(other, Dual):
            raise TypeError(
            'unsupported operand type(s) for pow: \'{}\' and \'{}\''.format(
            other.__class__.__name__, self.__class__.__name__))

        if self.real**other.real == 0:
            real= 0
            vec = 0*other.vector
            dual= ((self, 0),(other, 0))
        else:
            real = other.real**self.real
            vec = (other.real**self.real) * ((self.real/other.real*other.vector) + (self.vector* math.log(other.real)))
            dual = ((self, self.real**other.real*np.log(self.real)), (other, other.real*self.real**(other.real-1)))

        return Dual(
            real,
            vec,
            dual
        )
