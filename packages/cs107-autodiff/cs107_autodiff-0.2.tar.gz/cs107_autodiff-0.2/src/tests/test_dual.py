"""
This test suite (a module) runs test for dual.py
"""

import pytest
import numpy as np
# project code
from  .. import cs107_autodiff
from cs107_autodiff.math_defs import Dual as ad



class TestFunctions:
    def test_eq(self):
        assert(ad(8) == ad(8))
        assert(ad(8) != ad(7))
        assert(ad(8) != 8)
        assert(8 != (ad(8)))

    def test_radd(self):
        a = 3.0
        x = ad(2.0)
        assert (a+x).real == 5
        assert (a+x).dual == ((x, 1), (ad(3.0), 1))
        assert np.array_equal((a+x).vector, np.array([])) == True

    def test_radd2(self):
        a = 3
        x = ad(2.0)
        assert (a+x).real == 5
        assert (a+x).dual == ((x, 1), (ad(3.0), 1))
        assert np.array_equal((a+x).vector, np.array([])) == True

    def test_radd_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            a+x

    def test_add1(self):
        x1 = ad(3.0)
        assert (x1+x1).real == 6
        assert (x1+x1).dual == ((x1, 1), (x1, 1))
        assert np.array_equal((x1+x1).vector, np.array([])) == True

    def test_add2(self):
        a = 3.0
        x = ad(2.0)
        assert (x+a).real == 5
        assert (x+a).dual == ((x, 1), (ad(3.0), 1))
        assert np.array_equal((x+a).vector, np.array([])) == True

    def test_add3(self):
        a = 3
        x = ad(2.0)
        assert (x+a).real == 5
        assert (x+a).dual == ((x, 1), (ad(3), 1))
        assert np.array_equal((x+a).vector, np.array([])) == True


    def test_add_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            x+a

    def test_rmul(self):
        a = 3.0
        x = ad(2.0)
        assert (a*x).real == 6
        assert (a*x).dual == ((x, 3.0), (ad(a), 2.0))
        assert np.array_equal((a*x).vector, np.array([])) == True

    def test_rmul2(self):
        a = 3
        x = ad(2.0)
        assert (a*x).real == 6
        assert (a*x).dual == ((x, 3.0), (ad(a), 2.0))
        assert np.array_equal((a*x).vector, np.array([])) == True

    def test_rmul_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            a*x

    def test_mul1(self):
        x1 = ad(3.0)
        assert (x1*x1).real == 9
        assert (x1*x1).dual == ((x1, 3.0), (x1, 3.0))
        assert np.array_equal((x1*x1).vector, np.array([])) == True

    def test_mul2(self):
        a = 3.0
        x = ad(2.0)
        assert (x*a).real == 6
        assert (x*a).dual == ((x, 3.0), (ad(a), 2.0))
        assert np.array_equal((x*a).vector, np.array([])) == True
    #
    def test_mul3(self):
        x = ad(2.0)
        assert (3*x*2*x).real == 24

    def test_mul4(self):
        x = ad(2.0)
        assert (x*x*x*x*x).real == 32

    def test_mul_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            x*a

    def test_rsub(self):
        a = 3.0
        x = ad(2.0)
        assert (a-x).real == 1
        assert (a-x).dual == ((x, -1), (ad(3.0), 1))
        assert np.array_equal((a-x).vector, np.array([])) == True

    def test_rsub2(self):
        a = 3
        x = ad(2.0)
        assert (a-x).real == 1
        assert (a-x).dual == ((x, -1), (ad(3.0), 1))
        assert np.array_equal((a-x).vector, np.array([])) == True

    def test_rsub3(self):
        a = 3
        x = ad(5.0)
        assert (a-x).real == -2
        assert (a-x).dual == ((x, -1), (ad(3.0), 1))
        assert np.array_equal((a-x).vector, np.array([])) == True


    def test_rsub_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            a-x

    def test_sub1(self):
        x1 = ad(3.0)
        assert (x1-x1).real == 0
        assert (x1-x1).dual == ((x1, 1), (x1, -1))
        assert np.array_equal((x1-x1).vector, np.array([])) == True

    def test_sub2(self):
        x1 = ad(3.0)
        assert (3*x1-2*x1).real == 3

    def test_sub3(self):
        x1 = ad(3.0)
        assert (3*x1-6*x1).real == -9

    def test_sub4(self):
        x = ad(3.0)
        assert (3*x-6*x+2*x).real == -3

    def test_sub5(self):
        x = ad(3.0)
        assert (3*x-6*x+2).real == -7

    def test_sub_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            x-a

    def test_rdiv(self):
        a = 3.0
        x = ad(2.0)
        assert (a/x).real == 1.5
        assert (a/x).dual == ((x, -.75), (ad(3), .5))
        assert np.array_equal((a/x).vector, np.array([])) == True

    def test_rdiv2(self):
        a = 3
        x = ad(2.0)
        assert (a/x).real == 1.5
        assert (a/x).dual == ((x, -.75), (ad(3), .5))
        assert np.array_equal((a/x).vector, np.array([])) == True

    def test_rdiv_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            a/x

    def test_div1(self):
        x1 = ad(3.0)
        assert (x1/x1).real == 1
        assert (x1/x1).dual == ((x1, 1/3), (x1, -1/3))
        assert np.array_equal((x1/x1).vector, np.array([])) == True

    def test_div2(self):
        x1 = ad(3.0)
        assert ((3*x1)/(2*x1)).real == 1.5

    def test_div3(self):
        a = 2
        x = ad(3.0)
        assert (x/a).real == 1.5
        assert (x/a).dual == ((x, .5), (ad(2), -.75))
        assert np.array_equal((x/a).vector, np.array([])) == True

    def test_div4(self):
        a = 2
        x = ad(3.0)
        assert (x/a+3*x-2).real == 8.5

    def test_div_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            x/a


    # def test_fdiv(self):
    #     x1 = ad(3.0)
    #     assert (x1//x1).real == 1
    #     assert (x1//x1).dual == 0

    # def test_fdiv2(self):
    #     x1 = ad(3.0)
    #     assert ((3*x1)//(2*x1)).real == 1
    #     assert ((3*x1)//(2*x1)).dual == 0
    #
    # def test_fdiv3(self):
    #     a = 2
    #     x = ad(3.0)
    #     assert (x//a).real == 1
    #     assert (x//a).dual == 0
    #
    # def test_fdiv_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         x = ad(2.0)
    #         x//a
    #
    # def test_rfdiv(self):
    #     a = 2
    #     x = ad(3.0)
    #     assert (x//a+3*x-2).real == 8
    #     assert (x//a+3*x-2).dual == 3
    #
    # def test_rfdiv_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         x = ad(2.0)
    #         a//x
    #
    def test_rpow(self):
        a = 3.0
        x = ad(2.0)
        assert (a**x).real == 9
        assert (a**x).dual[1] == (ad(3), 12)
        assert (a**x).dual[0] == (x, 2**3*np.log(2))


    def test_rpow_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            a**x

    def test_pow1(self):
        x1 = ad(3.0)
        assert (x1**x1).real == 27
        assert (x1**x1).dual[0] == (x1, 27.0)
        assert (x1**x1).dual[1] == (x1, 3**3*np.log(3))
        assert np.array_equal((x1**x1).vector, np.array([])) == True

    def test_pow2(self):
        x1 = ad(3.0)
        assert ((x1**2)/(x1**4)).real == 1/9

    def test_pow3(self):
        a = 2
        x = ad(3.0)
        assert (x**a).real == 9
        # assert (x**a).dual == 6
        assert (x**a).dual[0] == (x, 6.0)
        assert (x**a).dual[1] == (ad(2), 3**2*np.log(3))


    def test_pow4(self):
        a = 2
        x = ad(3.0)
        assert (x**a+3*x-2).real == 16

    def test_pow_error(self):
        with pytest.raises(Exception) as e_info:
            a = [3.0]
            x = ad(2.0)
            x**a

    def test_neg(self):
        x = ad(3.0)
        assert (-x).real == -3
        assert (-x).dual[0] == (x, -1)
        assert (-x).dual[1] == (ad(-1), 3)

    def test_neg2(self):
        x = ad(3.0)
        assert (-x*3).real == -9

    def test_neg3(self):
        x = ad(3.0)
        assert (-x/3).real == -1

    def test_pos(self):
        x = ad(3.0)
        assert (+x).real == 3
        assert (+x).dual[0] == (x, 1)
        assert (+x).dual[1] == (ad(1), 3)

    def test_pos2(self):
        x = ad(3.0)
        assert (+x*3).real == 9

    def test_pos3(self):
        x = ad(3.0)
        assert (+x/3).real == 1

    def test_pow_goes_to_0(self):
        x = ad(0)
        assert (x**1).real == 0
        # assert (x**a).dual == 6
        assert (x**1).dual[0] == (x, 0)
        assert (x**1).dual[1] == (ad(1), 0)

    def test_rpow_goes_to_0(self):
        x = ad(1)
        assert (0**x).real == 0
        assert (0**x).dual[0] == (x, 0)
        assert (0**x).dual[1] == (ad(0), 0)


    # def test_sin2(self):
    #     x = ad(3.0)
    #     assert (ad.sin(x)*3).real == 3*np.sin(3)
    #     assert (ad.sin(x)*3).dual == 3*np.cos(3)
    #
    # def test_sin3(self):
    #     x = ad(3.0)
    #     assert (ad.sin(x)/(3*x)).real == np.sin(3)/9
    #     assert np.round((ad.sin(x)/(3*x)).dual,12) == np.round(-(np.sin(3)-3*np.cos(3))/27,12)
    #
    # def test_sin4(self):
    #     a = 3.0
    #     assert (ad.sin(a)).real == np.sin(3)
    #     assert (ad.sin(a)).dual == 0
    #
    # def test_sin_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         ad.sin(a)
    #
    # def test_cos(self):
    #     x = ad(3.0)
    #     assert (ad.cos(x)).real == np.cos(3)
    #     assert (ad.cos(x)).dual == -np.sin(3)
    #
    # def test_cos2(self):
    #     x = ad(3.0)
    #     assert (ad.cos(x)*3).real == 3*np.cos(3)
    #     assert (ad.cos(x)*3).dual == -3*np.sin(3)
    #
    # def test_cos3(self):
    #     x = ad(3.0)
    #     assert (ad.cos(x)/(3*x)).real == np.cos(3)/9
    #     assert np.round((ad.cos(x)/(3*x)).dual,12) == np.round(-(3*np.sin(3)+np.cos(3))/27,12)
    #
    # def test_cos4(self):
    #     a = 3.0
    #     assert (ad.cos(a)).real == np.cos(3)
    #     assert (ad.cos(a)).dual == 0
    #
    # def test_cos_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         ad.cos(a)
    #
    # def test_exp(self):
    #     x = ad(3.0)
    #     assert (ad.exp(x)).real == np.exp(3)
    #     assert (ad.exp(x)).dual == np.exp(3)
    #
    # def test_exp2(self):
    #     x = ad(3.0)
    #     assert (ad.exp(x)*3).real == 3*np.exp(3)
    #     assert (ad.exp(x)*3).dual == 3*np.exp(3)
    #
    # def test_exp3(self):
    #     x = ad(3.0)
    #     assert (ad.exp(x)/(3*x)).real == np.exp(3)/9
    #     assert np.round((ad.exp(x)/(3*x)).dual,12) == np.round((2)*np.exp(3)/27,12)
    #
    # def test_exp4(self):
    #     a = 3.0
    #     assert (ad.exp(a)).real == np.exp(3)
    #     assert (ad.exp(a)).dual == 0
    #
    # def test_exp_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         ad.exp(a)
    #
    # def test_tan(self):
    #     x = ad(3.0)
    #     assert (ad.tan(x)).real == np.tan(3)
    #     assert (ad.tan(x)).dual == (1/np.cos(3))**2
    #
    # def test_tan2(self):
    #     x = ad(3.0)
    #     assert (ad.tan(x)*3).real == 3*np.tan(3)
    #     assert (ad.tan(x)*3).dual == 3*(1/np.cos(3))**2
    #
    # def test_tan3(self):
    #     x = ad(3.0)
    #     assert (ad.tan(x)/(3*x)).real == np.tan(3)/9
    #     assert np.round((ad.tan(x)/(3*x)).dual,12) == np.round(-((np.tan(3)-3*(1/np.cos(3))**2)/27),12)
    #
    # def test_tan4(self):
    #     a = 3.0
    #     assert (ad.tan(a)).real == np.tan(3)
    #     assert (ad.tan(a)).dual == 0
    #
    # def test_tan_error(self):
    #     with pytest.raises(Exception) as e_info:
    #         a = [3.0]
    #         ad.tan(a)




if __name__ == '__main__':
		pytest.main()
