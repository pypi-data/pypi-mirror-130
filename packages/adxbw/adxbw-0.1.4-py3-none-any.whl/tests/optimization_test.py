from adxbw.optimization import *
import pytest

def test_newton():
    x4 = AD(np.array([1.1, -1.1, 1.1]), 1)
    funct3 = " - x_k**2 - 2*x_k"

    temp_root = newton(funct3, x4)
    assert np.allclose(np.array([-x ** 2 - 2 * x for x in temp_root]), 0)

def test_newton_multi():
    x1 = AD(-1, np.array([1, 0]))
    x2 = AD(2, np.array([0, 1]))
    temp_list = {"x1": x1, "x2": x2}

    funct = "x1.sin() - x2.cos()"
    temp_root = newton_multi(funct, x_k=temp_list, lr=0.05)
    assert np.isclose((np.sin(temp_root[0]) - np.cos(temp_root[1])), 0)


#if __name__ == "__main__":
#    test_newton()
#    test_newton_multi()
