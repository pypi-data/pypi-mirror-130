"""
This test suite (a module) runs test for ad.py
"""

import pytest
import numpy as np
import math
# project code
from  .. import cs107_autodiff
from cs107_autodiff.ad import AD



class TestFunctions:

    def test_add(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = a+b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 7
        assert fg[a] == 1
        assert rg[a] == 1


    def test_add_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            c = ad.create_variable(2)
            a+c

    def test_radd(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = a+b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 7
        assert fg[a] == 1
        assert rg[a] == 1

    def test_radd_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            c+a

    def test_mul(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = a*b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 12
        assert fg[a] == 3
        assert rg[a] == 3

    def test_mul_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            a*c

    def test_rmul(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = c*b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 21
        assert fg[a] == 0
        assert rg[b] == 7

    def test_rmul_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            c*a

    def test_rsub(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = c-b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 4
        assert fg[a] == 0
        assert rg[b] == -1

    def test_rsub_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            c-a

    def test_sub(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = b-c
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == -4
        assert fg[a] == 0
        assert rg[b] == 1

    def test_sub_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            a-c

    def test_div(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = a/b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 4/3
        assert rg[a] == 1/3
        assert fg[a] == 1/3

    def test_div_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            c/a

    def test_rdiv(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = c/b
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 7/3
        assert fg[a] == 0
        assert np.round(rg[b],10) == np.round(-7/9,10)


    def test_rdiv_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.create_variable(2)
            a/c

    def test_neg(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = -a
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == -4
        assert fg[a] == -1
        assert rg[b] == 0


    def test_pos(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        b = ad.create_variable(3)
        c = 7
        d = +a
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == 4
        assert fg[a] == 1
        assert rg[b] == 0

    def test_sin(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.sin(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.sin(4)
        assert fg[a] == np.cos(4)
        assert rg[a] == np.cos(4)


    def test_sin2(self):
        ad = AD(n_variables = 3)
        a = ad.sin(2)
        assert a.real == np.sin(2)


    def test_sin_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.sin(a)


    def test_cos(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.cos(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.cos(4)
        assert fg[a] == -np.sin(4)
        assert rg[a] == -np.sin(4)

    def test_cos2(self):
        ad = AD(n_variables = 3)
        a = ad.cos(2)
        assert a.real == np.cos(2)


    def test_cos_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.cos(a)

    def test_tan(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.tan(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.tan(4)
        assert fg[a] == 1/np.cos(4)**2
        assert rg[a] == 1/np.cos(4)**2

    def test_tan2(self):
        ad = AD(n_variables = 3)
        a = ad.tan(2)
        assert a.real == np.tan(2)

    def test_tan_error(self):
        with pytest.raises(TypeError) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.tan(a)

    def test_arcsin(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(0.5)
        d = ad.arcsin(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.arcsin(0.5)
        assert fg[a] == 1/np.sqrt(1-0.5**2)
        assert rg[a] ==1/np.sqrt(1-0.5**2)

    def test_arcsin2(self):
        ad = AD(n_variables = 3)
        a = ad.arcsin(0.5)
        assert a.real == np.arcsin(0.5)

    def test_arcsin_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.arcsin(a)

    def test_arcsin_error3(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = 3
            c = ad.arcsin(a)

    def test_arccos(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(0.5)
        d = ad.arccos(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.arccos(0.5)
        assert fg[a] == -1/np.sqrt(1-0.5**2)
        assert rg[a] == -1/np.sqrt(1-0.5**2)

    def test_arccos2(self):
        ad = AD(n_variables = 3)
        a = ad.arccos(0.5)
        assert a.real == np.arccos(0.5)

    def test_arccos_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.arccos(a)

    def test_arccos_error2(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = 3
            c = ad.arccos(a)

    def test_arctan(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(0.5)
        d = ad.arctan(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.arctan(0.5)
        assert fg[a] == 1/np.sqrt(1+0.5**2)
        assert rg[a] == 1/np.sqrt(1+0.5**2)

    def test_artan2(self):
        ad = AD(n_variables = 3)
        a = ad.arctan(0.5)
        assert a.real == np.arctan(0.5)


    def test_arctan_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.arctan(a)

    def test_sinh(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.sinh(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert np.round(d.real,10) == np.round(np.sinh(4),10)
        assert fg[a] == (np.exp(4) + np.exp(-1*4))/2
        assert rg[a] == (np.exp(4) + np.exp(-1*4))/2


    def test_sinh2(self):
        ad = AD(n_variables = 3)
        a = ad.sinh(2)
        assert np.round(a.real,10) == np.round(np.sinh(2),10)
        assert a.vector.all() == np.array([0,0,0]).all()


    def test_sinh_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.sinh(a)

    def test_cosh(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.cosh(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        assert d.real == np.cosh(4)
        assert fg[a] == ((np.exp(4) - np.exp(-1*4))/2)
        assert rg[a] == ((np.exp(4) - np.exp(-1*4))/2)


    def test_cosh2(self):
        ad = AD(n_variables = 3)
        a = ad.cosh(2)
        assert a.real == np.cosh(2)
        assert a.vector.all() == np.array([0,0,0]).all()

    def test_cosh_error(self):
        with pytest.raises(Exception) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.cosh(a)

    def test_tanh(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(4)
        d = ad.tanh(a)
        fg = ad.forward_mode_gradients(d)
        rg = ad.reverse_mode_gradients(d)
        x= 4
        assert d.real == np.tanh(4)
        assert fg[a] == (np.cosh(x)*np.cosh(x) - np.sinh(x)*np.sinh(x) )/np.cosh(x)**2
        assert rg[a] == (np.cosh(x)*np.cosh(x) - np.sinh(x)*np.sinh(x) )/np.cosh(x)**2

    def test_tanh2(self):
        ad = AD(n_variables = 3)
        a = ad.tanh(2)
        assert a.real == np.tanh(2)
        assert a.vector.all() == np.array([0,0,0]).all()

    def test_tanh_error(self):
        with pytest.raises(TypeError) as e_info:
            ad = AD(n_variables = 3)
            a = [3.0]
            c = ad.tanh(a)

    def test_create_variable_error(self):
        ad = AD(n_variables = 2)
        a = ad.create_variable(2)
        b = ad.create_variable(4)
        with pytest.raises(ValueError):
            c = ad.create_variable(10)

    def test_exp(self):
        ad = AD(n_variables = 3)
        a = ad.exp(3)
        b = ad.create_variable(2)
        fg = ad.forward_mode_gradients(a)
        rg = ad.reverse_mode_gradients(a)
        x = 3
        assert a.real == np.exp(x)
    #
    def test_exp2(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(3)
        b = ad.exp(a)
        fg = ad.forward_mode_gradients(b)
        rg = ad.reverse_mode_gradients(b)

        # print(a.real)
        assert b.real == np.exp(3)
        assert fg[a] == np.exp(3)
        assert rg[a] == np.exp(3)


    def test_exp_error(self):
        with pytest.raises(TypeError):
            ad = AD(n_variables = 3)
            a = [3.0]
            b = ad.exp(a)

    def test_ln(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(3)
        b = ad.ln(a)
        fg = ad.forward_mode_gradients(b)
        rg = ad.reverse_mode_gradients(b)

        assert b.real == np.log(3)
        assert fg[a] == 1/3
        assert rg[a] == 1/3

    def test_ln2(self):
        ad = AD(n_variables = 3)
        b = ad.ln(3)
        fg = ad.forward_mode_gradients(b)
        rg = ad.reverse_mode_gradients(b)

        assert b.real == np.log(3)

    def test_ln_error(self):
        with pytest.raises(TypeError):
            ad = AD(n_variables = 3)
            a = [3.0]
            b = ad.ln(a)

    def test_log(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(100)
        b = ad.create_variable(10.0)
        c = ad.log(a, b)
        fg = ad.forward_mode_gradients(c)
        rg = ad.reverse_mode_gradients(c)

        assert c.real == 2
        assert fg[a] == 1/(np.log(10)*100)
        assert rg[a] == 1/(np.log(10)*100)
        assert fg[b] == rg[b]

    def test_log2(self):
        ad = AD(n_variables = 3)
        c = ad.log(100.0, 10.0)

        assert c.real == 2

    def test_log_error(self):
        with pytest.raises(TypeError):
            ad = AD(n_variables = 3)
            a = [3.0]
            b = ad.log(a, 10)

    def test_log_error2(self):
        with pytest.raises(TypeError):
            ad = AD(n_variables = 3)
            a = [3.0]
            b = ad.log(10, a)

    def test_sqrt(self):
        ad = AD(n_variables = 3)
        b = ad.sqrt(9)

        assert b.real == 3

    def test_sqrt2(self):
        ad = AD(n_variables = 3)
        a = ad.create_variable(9)
        b = ad.sqrt(a)

        fg = ad.forward_mode_gradients(b)
        rg = ad.reverse_mode_gradients(b)

        assert b.real == 3
        assert fg[a] == .5 / np.sqrt(9)

    def test_sqrt_error(self):
        with pytest.raises(TypeError):
            ad = AD(n_variables = 3)
            a = [3.0]
            b = ad.sqrt(a)

    def test_get_gradient(self):
        ad = AD(n_variables=3)
        x = ad.create_variable(1)
        y = ad.create_variable(1)

        z = (x**2) + (y**2)

        fg = ad.get_gradient(z, x, mode='forward')
        rg = ad.get_gradient(z, x, mode='reverse')

        assert fg == 2
        assert rg == 2

        fg = ad.get_gradient(z, y, mode='forward')
        rg = ad.get_gradient(z, y, mode='reverse')
        assert fg == 2
        assert rg == 2

        fg = ad.get_gradient(z, z, mode='forward')
        rg = ad.get_gradient(z, z, mode='reverse')
        assert fg == 1
        assert rg == 1

        fg = ad.get_gradient(x, x, mode='forward')
        rg = ad.get_gradient(x, x, mode='reverse')
        assert fg == 1
        assert rg == 1

    def test_get_gradient2(self):
        ad = AD(n_variables=3)
        w  = ad.create_variable(1)
        x = ad.create_variable(1)
        y = ad.create_variable(1)

        z = ad.exp(x+y)

        fg = ad.get_gradient(z, x, mode='forward')
        rg = ad.get_gradient(z, x, mode='reverse')

        assert fg == np.exp(2)
        assert rg == np.exp(2)

        fg = ad.get_gradient(z, y, mode='forward')
        rg = ad.get_gradient(z, y, mode='reverse')
        assert fg == np.exp(2)
        assert rg == np.exp(2)

        fg = ad.get_gradient(z, z, mode='forward')
        rg = ad.get_gradient(z, z, mode='reverse')
        assert fg == 1
        assert rg == 1

        fg = ad.get_gradient(z, w, mode='forward')
        rg = ad.get_gradient(z, w, mode='reverse')
        assert fg == 0
        assert rg == 0

    def test_trace(self):
        ad = AD(n_variables = 2)
        x = ad.create_variable(1)
        y = ad.create_variable(1)

        def f(x,y):
            return [x**2 + y**2, ad.exp(x+y)]
        assert np.array_equal(
            ad.trace(f,mode = 'reverse',seed=[[1,1],[-2,1]]),
            [[-2, 4], [-np.exp(2), 2*np.exp(2)]]
        ) == True

    def test_trace2(self):
        ad = AD(n_variables = 2)
        x = ad.create_variable(1)
        y = ad.create_variable(1)

        def f(x,y):
            return [x**2 + y**2, ad.exp(x+y)]
        assert np.array_equal(
            ad.trace(f,mode = 'reverse',seed=[[1,0],[0,1]]),
            [[2, 2], [np.exp(2), np.exp(2)]]
        ) == True

if __name__ == '__main__':
		pytest.main()
