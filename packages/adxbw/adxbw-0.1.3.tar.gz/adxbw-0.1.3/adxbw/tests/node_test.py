from adxbw.node import *
import pytest


def test_add(verbose=True):
    # Test for single scalar input (plus with node and plus with constant)
    x1 = AD(2, 1)  # x = 2
    n1 = x1 + x1 + 4  # 2x + 4

    assert n1.val == 2 * 2 + 4
    assert n1.partial_ders == 2 * 1

    # Test for multiple scalar inputs
    x2 = AD(2, np.array([1, 0]))  # x = 2
    x3 = AD(3, np.array([0, 1]))  # y = 3
    n2 = 1 + x2 + x3 + 2  # x + y + 3

    assert n2.val == 2 + 3 + 3
    assert np.all(n2.partial_ders == np.array([1, 1]))

    if verbose:
        print(n1)
        print(n2)


def test_multiply(verbose=True):
    # Test for single scalar input
    x1 = AD(2, 1)  # x = 2
    n1 = x1 * x1 + 2 * x1 + 4  # x^2 + 2x + 4

    assert (n1.val == 2 * 2 + 2 * 2 + 4 and n1.partial_ders == 2 * 2 + 2)

    # Test for multiple scalar inputs
    x2 = AD(2, np.array([1, 0]))  # x = 2
    x3 = AD(3, np.array([0, 1]))  # y = 3
    n2 = 1 + x2 + 2 * x3 + 2  # x + 2y + 3

    assert (n2.val == 2 + 2 * 3 + 3 and np.all(n2.partial_ders == np.array([1, 2])))

    # Another test for multiple scalar inputs
    x4 = AD(4, np.array([1, 0]))  # x = 4
    x5 = AD(-1, np.array([0, 1]))  # y = -1
    n3 = 1 + x4 + 2 * x5 + x4 * x5  # xy + x + 2y + 1

    assert n3.val == -1
    assert np.all(n3.partial_ders == np.array([0, 6]))

    if verbose:
        print(n1)
        print(n2)
        print(n3)


def test_subtract(verbose=True):
    # Test for single scalar input
    x1 = AD(5, 1)  # x = 5
    n1 = x1 * x1 - 2 * x1 - 4  # x^2 - 2x + 4

    assert n1.val == 5 ** 2 - 2 * 5 - 4
    assert n1.partial_ders == 2 * 5 - 2

    # Test for multiple scalar inputs
    x2 = AD(2, np.array([1, 0]))  # x = 2
    x3 = AD(3, np.array([0, 1]))  # y = 3
    n2 = 1 - 2 * x3 + x2 + 2  # x - 2y + 3

    assert n2.val == 2 - 2 * 3 + 3
    assert np.all(n2.partial_ders == np.array([1, -2]))

    if verbose:
        print(n1)
        print(n2)


def test_negate(verbose=True):
    # Test for single scalar input
    x1 = AD(5, 1)  # x = 5
    n1 = (-x1) * x1 + 2 * x1 + 4  # - x^2 + 2x + 4

    assert (n1.val == - 5 ** 2 + 2 * 5 + 4 and n1.partial_ders == -2 * 5 + 2)

    # Test for multiple scalar inputs
    x2 = AD(2, np.array([1, 0]))  # x = 2
    x3 = AD(3, np.array([0, 1]))  # y = 3
    n2 = - x2 + 2 * x3 + 3  # - x + 2y + 3

    assert (n2.val == - 2 + 2 * 3 + 3 and np.all(n2.partial_ders == np.array([-1, 2])))

    if verbose:
        print(n1)
        print(n2)


def test_exp(verbose=True):
    test_n = []
    # test default exp, only x
    x1 = AD(2, 1)  # x = 1
    n1 = x1.exp()  # e^x
    test_n.append(n1)
    assert (n1.val == math.e ** 2 and n1.partial_ders == math.e ** 2)

    # test exp with base = 2, only x
    n2 = x1.exp(2)  # 2^x
    test_n.append(n2)
    assert (n2.val == 2 ** 2 and n2.partial_ders == np.log(2) * 2 ** 2)

    # edge case: test exp base = 0, only x
    n3 = x1.exp(0)  # 0^x
    test_n.append(n3)
    assert (n3.val == 0 and n3.partial_ders == 0)

    # test exp base = neg, only x
    with pytest.raises(ArithmeticError):
        n4 = x1.exp(-2)  # -2^x
        test_n.append(n4)

    # test exp x = 0
    x2 = AD(0, 1)
    n5 = x2.exp(2)  # 2^0
    test_n.append(n5)
    assert (n5.val == 1 and n5.partial_ders == np.log(2) * 2 ** (0))

    # test exp x = neg
    x3 = AD(-1, 1)
    n6 = x3.exp(2)  # 2^-1
    test_n.append(n6)
    assert (n6.val == 2 ** (-1) and n6.partial_ders == np.log(2) * 2 ** (-1))

    # test exp with chain rule, x and y
    x4 = AD(4, np.array([1, 0]))  # x = 2
    x5 = AD(3, np.array([0, 1]))  # y = 3
    n7 = (x4 + x5).exp(2)  # 2^(x+y)
    test_n.append(n7)
    assert (n7.val == 2 ** (4 + 3) and np.all(n7.partial_ders == np.array([np.log(2) * 2 ** 7, np.log(2) * 2 ** 7])))

    # test exp with vector inputs
    x6 = AD(np.array([[1, 2, 3], [3, 0, 1]]), 1)
    n8 = x6.exp(2)
    test_n.append(n8)
    assert np.all(n8.val == 2 ** (x6.val))
    assert np.all(np.isclose(n8.partial_ders, np.log(2) * (2 ** x6.val)))

    if verbose:
        for n in test_n:
            print(n)


def test_power(verbose=True):
    # regular pow, only x
    test_n = []
    x1 = AD(3, 1)  # x = 2
    n1 = x1 ** 2
    test_n.append(n1)
    assert (n1.val == 3 ** 2 and n1.partial_ders == 2 * 3)

    # pow = 0
    n2 = x1 ** 0
    test_n.append(n2)
    assert (n2.val == 1 and n2.partial_ders == 0)

    # pow = -1
    n3 = x1 ** (-1)
    test_n.append(n3)
    assert (n3.val == 3 ** (-1) and n3.partial_ders == -1 / 9)

    # x = 0
    x2 = AD(0, 1)  # x = 0
    n4 = x2 ** 2
    test_n.append(n4)
    assert (n4.val == 0 ** 2 and n4.partial_ders == 2 * 0)

    # x = -1
    x3 = AD(-1, 1)  # x = -1
    n5 = x3 ** 2
    test_n.append(n5)
    assert (n5.val == 1 and n5.partial_ders == -2)

    # x and y
    x4 = AD(4, np.array([1, 0]))  # x = 2
    x5 = AD(3, np.array([0, 1]))  # y = 3
    n6 = (x4 + x5) ** 2  # (x +y) **2
    test_n.append(n6)
    assert (n6.val == (4 + 3) ** 2 and np.all(n6.partial_ders == np.array([2 * 7, 2 * 7])))

    # test exp with vector inputs
    x6 = AD(np.array([[1, 2, 3], [-1, 0, 1]]), 1)
    n8 = x6 ** 2
    test_n.append(n8)
    assert np.all(n8.val == (x6.val) ** 2)
    assert np.all(np.isclose(n8.partial_ders, 2 * x6.val))

    if verbose:
        for node in test_n:
            print(node)


def test_sqrt(verbose=True):
    # since the original sqrt implementation is manually computed
    # here we can test sqrt() with **0.5
    test_n = []

    # regular sqrt, only x
    x1 = AD(4, 1)  # x =
    n1 = x1.sqrt()
    test_n.append(n1)
    assert n1.val == 2
    assert n1.partial_ders == 0.5 * 4 ** (-0.5)

    # x = 0
    x2 = AD(0, 1)
    with pytest.raises(ZeroDivisionError):
        n2 = x2.sqrt()

    # x = neg
    x3 = AD(-1, 1)
    with pytest.raises(ArithmeticError):
        n3 = x3.sqrt()

    # x and y
    x2 = AD(4, np.array([1, 0]))  # x = 4
    x3 = AD(3, np.array([0, 1]))  # y = 3
    n4 = (x2 + x3).sqrt()
    test_n.append(n4)
    assert n4.val == (4 + 3) ** 0.5
    assert np.all(n4.partial_ders == \
                  np.array([1 / (2 * math.sqrt(7)), 1 / (2 * math.sqrt(7))]))

    # test exp with vector inputs
    x4 = AD(np.array([[1, 2, 3]]), 1)
    n5 = x4.sqrt()
    test_n.append(n5)
    assert np.all(n5.val == x4.val ** (1 / 2))
    assert np.all(np.isclose(n5.partial_ders, (1 / 2) * x4.val ** (-1 / 2)))

    if verbose:
        print("/n===========/nTesting sqrt function...")
        for node in test_n:
            print(node)


def test_log(verbose=True):
    test_n = []
    # test default log, base = e, only x
    x1 = AD(2, 1)  # x = 2
    n1 = x1.log()  # log_e(x)
    test_n.append(n1)
    assert (n1.val == math.log(2) and n1.partial_ders == 1 / 2)

    # test exp with base = 2, only x
    n2 = x1.log(2)  # 2^x
    test_n.append(n2)
    assert (n2.val == 1 and n2.partial_ders == 1 / (2 * np.log(2)))

    # edge case: test exp base = 0, only x
    with pytest.raises(ArithmeticError):
        n3 = x1.log(0)  # 0^x

    # test exp base = neg, only x
    with pytest.raises(ArithmeticError):
        n4 = x1.log(-2)  # -2^x

    # test x = 0
    x2 = AD(0, 1)
    with pytest.raises(ZeroDivisionError):
        n5 = x2.log(2)  # log2(0)

    # test exp x = neg
    x3 = AD(-1, 1)
    with pytest.raises(ArithmeticError):
        n6 = x3.log(2)  # log2(-1)

    # test exp with chain rule, x and y
    x4 = AD(1, np.array([1, 0]))  # x = 1
    x5 = AD(7, np.array([0, 1]))  # y = 7
    n7 = (x4 + x5).log(2)  # log2(8)
    test_n.append(n7)
    assert n7.val == 3
    assert np.all(n7.partial_ders == np.array([1 / (8 * np.log(2)), 1 / (8 * np.log(2))]))

    # test exp with vector inputs
    x6 = AD(np.array([[1, 2, 3]]), 1)
    n8 = x6.log(3)
    test_n.append(n8)
    assert np.all(n8.val == np.log(x6.val) / np.log(3))
    assert np.all(np.isclose(n8.partial_ders, 1 / (x6.val * np.log(3))))

    if verbose:
        print("/n===========/nTesting log function...")
        for node in test_n:
            print(node)


def test_sin():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.sin()

    assert n1.val == math.sin(0)
    assert n1.partial_ders == math.cos(0)

    # test x = pi/2, with normal radian value
    x2 = AD(math.pi / 2, 1)
    n2 = x2.sin()

    assert n2.val == math.sin(math.pi / 2)
    assert n2.partial_ders == math.cos(math.pi / 2)

    # test x = -1, negative value
    x3 = AD(-1, 1)
    n3 = x3.sin()

    assert n3.val == math.sin(-1)
    assert n3.partial_ders == math.cos(-1)

    # test x = 1000, large value, abnormal radian value
    x4 = AD(1000, 1)
    n4 = x4.sin()

    assert n4.val == math.sin(1000)
    assert n4.partial_ders == math.cos(1000)

    # test univariate operation
    n5 = (x4 ** 2).sin()

    assert n5.val == math.sin(x4.val ** 2)
    assert n5.partial_ders == math.cos(x4.val ** 2) * (x4 ** 2).partial_ders

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(1, np.array([0, 1]))
    n6 = (x5 + x6).sin()

    assert n6.val == math.sin(x5.val + x6.val)
    assert np.all(n6.partial_ders == math.cos((x5 + x6).val) * (x5 + x6).partial_ders)


def test_cos():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.cos()

    assert (n1.val == math.cos(0) and n1.partial_ders == -math.sin(0))

    x2 = AD(math.pi / 2, 1)
    n2 = x2.cos()

    assert (n2.val == math.cos(math.pi / 2) and n2.partial_ders == -math.sin(math.pi / 2))

    # test x = -1, negative value
    x3 = AD(-1, 1)
    n3 = x3.cos()

    assert (n3.val == math.cos(-1) and n3.partial_ders == -math.sin(-1))

    # test x = 1000, large value, abnormal radian value
    x4 = AD(1000, 1)
    n4 = x4.cos()

    assert (n4.val == math.cos(1000) and n4.partial_ders == -math.sin(1000))

    # test univariate operation
    n5 = (x4 ** 2).cos()

    assert (n5.val == math.cos(x4.val ** 2) and n5.partial_ders == -math.sin(x4.val ** 2) * (x4 ** 2).partial_ders)

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(1, np.array([0, 1]))
    n6 = (x5 + x6).cos()

    assert (n6.val == math.cos(x5.val + x6.val) and np.all(
        n6.partial_ders == -math.sin((x5 + x6).val) * (x5 + x6).partial_ders))


def test_tan():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.tan()

    assert (n1.val == math.tan(0) and n1.partial_ders == (1 / math.cos(0)) ** 2)

    with pytest.raises(ArithmeticError):
        x2 = AD(math.pi / 2, 1)
        n2 = x2.tan()

    # assert (n2.val == math.tan(math.pi/2) and n2.partial_ders == (1/math.cos(math.pi/2))**2)

    # test x = -1, negative value
    x3 = AD(-1, 1)
    n3 = x3.tan()

    assert (n3.val == math.tan(-1) and n3.partial_ders == (1 / math.cos(-1)) ** 2)

    # test x = 1000, large value, abnormal radian value
    x4 = AD(1000, 1)
    n4 = x4.tan()

    assert (n4.val == math.tan(1000) and math.isclose(n4.partial_ders, (1 / math.cos(1000)) ** 2))

    # test univariate operation
    n5 = (x4 ** 2).tan()

    assert (n5.val == math.tan(x4.val ** 2) and math.isclose(n5.partial_ders, ((1 / math.cos(x4.val ** 2)) ** 2) * (
            x4 ** 2).partial_ders))

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(1, np.array([0, 1]))
    n6 = (x5 + x6).tan()

    assert n6.val == math.tan(x5.val + x6.val)
    assert np.all(n6.partial_ders == ((1 / math.cos((x5 + x6).val)) ** 2) * (x5 + x6).partial_ders)


def test_truediv():
    # test x = 2, divided by negative value
    x1 = AD(2, 1)
    n1 = x1 / 2

    assert (n1.val == x1.val / 2 and n1.partial_ders == 1 / 2)

    # test x = 2, divided by negative value
    n2 = x1 / (-2)

    assert (n2.val == x1.val / (-2) and n2.partial_ders == -1 / 2)

    # test univariate with operations
    n3 = (x1 * x1 ** 3) / 2

    assert n3.val == (x1 * x1 ** 3).val / 2
    assert n3.partial_ders == (x1 * x1 ** 3).partial_ders / 2

    # test multivarite, divide by real number
    x2 = AD(4, np.array([1, 0]))
    x3 = AD(5, np.array([0, 1]))
    n4 = (x2 ** 2 + x3) / 2

    assert n4.val == (x2 ** 2 + x3).val / 2
    assert np.all(n4.partial_ders == (x2 ** 2 + x3).partial_ders / 2)

    # test multivariate, divide by other function
    n5 = x2 / x3
    assert n5.val == x2.val / x3.val
    assert np.all(n5.partial_ders == (x2.partial_ders * x3.val - x3.partial_ders * x2.val) / (x3.val ** 2))

    # test div by 0
    with pytest.raises(ZeroDivisionError):
        n6 = x1 / 0

    # test div by 0 node
    with pytest.raises(ZeroDivisionError):
        n7 = x1 / AD(0, 1)


def test_arcsin():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.arcsin()

    assert n1.val == math.asin(0)
    assert n1.partial_ders == (1 / math.sqrt(1 - 0 ** 2))

    # test x = pi/4, with normal radian value
    x2 = AD(math.pi / 4, 1)
    n2 = x2.arcsin()

    assert (n2.val == math.asin(math.pi / 4) and n2.partial_ders == (1 / math.sqrt(1 - (math.pi / 4) ** 2)))

    # test x = 1000, outside of range, should throw error
    with pytest.raises(ArithmeticError):
        x4 = AD(1000, 1)
        n4 = x4.arcsin()

    with pytest.raises(ArithmeticError):
        x4 = AD(-1000, 1)
        n4 = x4.arcsin()

    # assert (n4.val == math.asin(1000) and n4.partial_ders == (1 / math.sqrt(1 - 1000 ** 2)))

    # test univariate operation
    n5 = (x2 ** 2).arcsin()

    assert n5.val == math.asin(x2.val ** 2)
    assert n5.partial_ders == (x2 ** 2).partial_ders / \
           math.sqrt(1 - (x2.val ** 2) ** 2)

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(0.5, np.array([0, 1]))
    n6 = (x5 + x6).arcsin()

    assert n6.val == math.asin(x5.val + x6.val)
    assert np.all(n6.partial_ders == (x5 + x6).partial_ders / math.sqrt(1 - (x5.val + x6.val) ** 2))


def test_arccos():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.arccos()

    assert n1.val == math.acos(0)
    assert n1.partial_ders == (-1 / math.sqrt(1 - 0 ** 2))

    # test x = pi/4, with normal radian value
    x2 = AD(math.pi / 4, 1)
    n2 = x2.arccos()

    assert (n2.val == math.acos(math.pi / 4) and n2.partial_ders == (-1 / math.sqrt(1 - (math.pi / 4) ** 2)))

    # test x = 1000, outside of range, should throw error
    with pytest.raises(ArithmeticError):
        x4 = AD(1000, 1)
        n4 = x4.arccos()

    with pytest.raises(ArithmeticError):
        x4 = AD(-1000, 1)
        n4 = x4.arccos()

    # test uni-variate operation
    n5 = (x2 ** 2).arccos()

    assert (n5.val == math.acos(x2.val ** 2) and n5.partial_ders == -(x2 ** 2).partial_ders / math.sqrt(
        1 - (x2.val ** 2) ** 2))

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(0.5, np.array([0, 1]))
    n6 = (x5 + x6).arccos()

    assert n6.val == math.acos(x5.val + x6.val)
    assert np.all(n6.partial_ders == -(x5 + x6).partial_ders / math.sqrt(1 - (x5.val + x6.val) ** 2))


def test_arctan():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.arctan()
    assert n1.val == math.atan(0)
    assert n1.partial_ders == (1 / (1 + 0 ** 2))

    # test x = pi/2, with normal radian value
    x2 = AD(math.pi / 2, 1)
    n2 = x2.arctan()

    assert (n2.val == math.atan(math.pi / 2) and n2.partial_ders == (1 / (1 + (math.pi / 2) ** 2)))

    # test x = -1, negative value
    x3 = AD(-1, 1)
    n3 = x3.arctan()
    assert (n3.val == math.atan(-1) and n3.partial_ders == (1 / (1 + (-1) ** 2)))

    # test x = 1000, large value
    x4 = AD(1000, 1)
    n4 = x4.arctan()
    assert (n4.val == math.atan(1000) and n4.partial_ders == (1 / (1 + 1000 ** 2)))

    # test univariate operation
    n5 = (x2 ** 2).arctan()

    assert n5.val == math.atan(x2.val ** 2)
    assert np.isclose(n5.partial_ders, (x2 ** 2).partial_ders / (1 + (x2.val ** 2) ** 2))

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(0.5, np.array([0, 1]))
    n6 = (x5 + x6).arctan()

    assert (n6.val == math.atan(x5.val + x6.val) and np.all(
        n6.partial_ders == (x5 + x6).partial_ders / (1 + (x5.val + x6.val) ** 2)))


def test_eq_ne():
    # uni-variate situation
    x1 = AD(0, 1)
    x2 = AD(0, 1)
    x3 = AD(0, 3)

    assert x1 == x2
    assert x2 != x3
    assert x1 != x3

    # multivariate situation
    x4 = AD(0, np.array([1, 0]))
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(0.5, np.array([0, 1]))

    assert (x4 == x5 and x4 != x6 and x5 != x6)

    assert (x1 != x4)


def test_logits():
    # test x = 0
    x1 = AD(0, 1)
    n1 = x1.sigmoid()
    assert n1.val == 1 / 2
    assert n1.partial_ders == 0.25

    # test x = -1, negative value
    x3 = AD(-1, 1)
    n3 = x3.sigmoid()
    assert n3.val == 1 / (1 + math.e ** (-(-1)))
    assert n3.partial_ders == (1 / (1 + math.e)) * (1 - (1 / (1 + math.e))) * x3.partial_ders

    # test x = 1000, large value
    x4 = AD(1000, 1)
    n4 = x4.sigmoid()
    assert n4.val == 1 / (1 + math.e ** (-1000))
    assert n4.partial_ders == (1 / (1 + math.e ** (-1000))) * (1 - (1 / (1 + math.e ** (-1000)))) * x4.partial_ders

    # test uni-variate operation
    x2 = AD(2, 1)
    n5 = (x2 ** 2).sigmoid()

    assert n5.val == 1 / (1 + math.e ** (-(x2 ** 2).val))
    assert n5.partial_ders == (1 / (1 + math.e ** (-(x2 ** 2).val))) * (1 - (1 / (1 + math.e ** (-(x2 ** 2).val)))) * \
           (x2 ** 2).partial_ders

    # test multivariate situation
    x5 = AD(0, np.array([1, 0]))
    x6 = AD(0.5, np.array([0, 1]))
    n6 = (x5 + x6).sigmoid()

    assert n6.val == 1 / (1 + math.e ** (-(x5 + x6).val))
    assert np.all(n6.partial_ders == (1 / (1 + math.e ** (-(x5 + x6).val))) * \
                  (1 - (1 / (1 + math.e ** (-(x5 + x6).val)))) * (x5 + x6).partial_ders)


def test_sinh():
    # test x = 1
    x1 = AD(1, 1)
    n1 = x1.sinh()

    assert n1.val == np.sinh(1)
    assert n1.partial_ders == np.cosh(1)

    # test x = pi/4, with normal radian value
    x2 = AD(math.pi / 4, 1)
    n2 = x2.sinh()

    assert n2.val == np.sinh(math.pi / 4)
    assert np.isclose(n2.partial_ders, np.cosh(math.pi / 4))

    # test exp with vector inputs
    x3 = AD(np.array([[math.pi / 4, math.pi / 2, math.pi / 6],
                      [math.pi / 3, math.pi / 9, math.pi / 10]]), 1)
    n3 = x3.sinh()
    assert np.all(n3.val == np.sinh(x3.val))
    assert np.all(np.isclose(n3.partial_ders, np.cosh(x3.val)))


def test_cosh():
    # test x = 1
    x1 = AD(1, 1)
    n1 = x1.cosh()

    assert n1.val == np.cosh(1)
    assert n1.partial_ders == np.sinh(1)

    # test x = pi/4, with normal radian value
    x2 = AD(math.pi / 4, 1)
    n2 = x2.cosh()

    assert (n2.val == np.cosh(math.pi / 4) and n2.partial_ders == np.sinh(math.pi / 4))

    # test exp with vector inputs
    x3 = AD(np.array([[math.pi / 4, math.pi / 2, math.pi / 6],
                      [math.pi / 3, math.pi / 9, math.pi / 10]]), 1)
    n3 = x3.cosh()
    assert np.all(n3.val == np.cosh(x3.val))
    assert np.all(np.isclose(n3.partial_ders, np.sinh(x3.val)))


def test_tanh():
    # test x = 1
    x1 = AD(1, 1)
    n1 = x1.tanh()

    assert n1.val == np.tanh(1)
    assert np.isclose(n1.partial_ders, 1 - np.tanh(1) ** 2)

    # test x = pi/4, with normal radian value
    x2 = AD(math.pi / 4, 1)
    n2 = x2.tanh()

    assert n2.val == np.tanh(math.pi / 4)
    assert np.isclose(n2.partial_ders, 1 - np.tanh(math.pi / 4) ** 2)

    # test exp with vector inputs
    x3 = AD(np.array([[math.pi / 4, math.pi / 2, math.pi / 6],
                      [math.pi / 3, math.pi / 9, math.pi / 10]]), 1)
    n3 = x3.tanh()
    assert np.all(n3.val == np.tanh(x3.val))
    assert np.all(np.isclose(n3.partial_ders, 1 - np.tanh(x3.val) ** 2))

# if __name__ == "__main__":
#     test_add()
#     test_multiply()
#     test_subtract()
#     test_negate()
#
#     test_exp()
#     test_power()
#     test_sqrt()
#     test_log()
#
#     test_sin()
#     test_cos()
#     test_tan()
#     test_truediv()
#
#     test_arcsin()
#     test_arccos()
#     test_arctan()
#
#     test_eq_ne()
#     test_logits()
#
#     test_sinh()
#     test_cosh()
#     test_tanh()
