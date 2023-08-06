"""
This test suite (a module) runs test for ad.py
"""

import pytest
import math
import numpy as np
# project code
from ..ad import AD




class TestFunctions:
    def test_sin(self):
        ad = AD(n_variables=1)
        x = ad.create_variable(3.0)

        val = ad.sin(x)

        assert (val.real == np.sin(3))


if __name__ == '__main__':
    pytest.main()
