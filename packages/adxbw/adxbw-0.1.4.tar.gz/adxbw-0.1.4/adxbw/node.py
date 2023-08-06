import numpy as np
import math

class AD:

    def __init__(self, x, ders=1, digits=-1):
        """
        Constructor
        :param x: value, only allow single scalar, multiple scalar, or single vector
        :param ders: partial derivatives; for multiple scalar, length of this numpy array need to be 
            corresponded to the number of variables
        :param digits: number of digits of values to display
        """
        if type(x) is np.ndarray:
            x = x.astype("float")
        elif type(x) is int:
            x = float(x)
        elif type(x) is not float:
            raise (TypeError("Invalid value type: only allow float/int/numpy ndarray"))

        if type(ders) is int:
            ders = float(ders)
        elif type(ders) is np.ndarray:
            ders = ders.astype("float")
        elif type(ders) is not float:
            raise (TypeError("Invalid derivatives type: only allow float/int/numpy ndarray"))

        self._val = x
        self._partial_ders = ders
        self.digits = digits

    @property
    def val(self):
        """
        Getter of current value
        :return: None
        """
        return (self._val)

    @val.setter
    def val(self, x):
        """
        Setter of current value
        :param value:
        :return: None
        """

        if type(x) is np.ndarray:
            x = x.astype("float")
        elif type(x) is int:
            x = float(x)

        self._val = x

    @property
    def partial_ders(self):
        """
        Getter of partial derivatives
        :return: None
        """
        return (self._partial_ders)

    @partial_ders.setter
    def partial_ders(self, ders):
        """
        Setter of partial derivatives
        :param ders:
        :return: None
        """
        if type(ders) is int:
            ders = float(ders)
        elif type(ders) is np.ndarray:
            ders = ders.astype("float")

        self._partial_ders = ders

    # Jiaye Chen
    def __add__(self, other):
        """
        Addition operator 
        :param other: An AD object or a real number 
        :return: An AD object
        """
        temp_autodiff = AD(1)
        try:  # Node + Node
            temp_autodiff.val = self.val + other.val
            temp_autodiff.partial_ders = self.partial_ders + other.partial_ders

            # temp_autodiff.ADlist = self.ADlist + other.ADlist
            return temp_autodiff

        except AttributeError:  # Node + value (int/float)
            temp_autodiff.val = self.val + other
            temp_autodiff.partial_ders = self.partial_ders

            return temp_autodiff

    def __radd__(self, other):
        """
        Right addition operator
        :param other: An AD object or a real number 
        :return: An AD object
        """
        return self + other

    def __mul__(self, other):
        """
        Multiplication operator
        :param other: An AD object or a real number 
        :return: An AD object
        """
        temp_autodiff = AD(1)
        try:

            temp_autodiff.val = self.val * other.val
            if type(self.val) is np.ndarray and type(other.val) is np.ndarray:
                print("Warning: using '*' Multiplication for matrices. For dot product, please use dot() function!")

            temp_autodiff.partial_ders = self.partial_ders * other.val + other.partial_ders * self.val

            return temp_autodiff

        except AttributeError:

            temp_autodiff.val = self.val * other
            temp_autodiff.partial_ders = self.partial_ders * other

            return temp_autodiff

    def __rmul__(self, other):
        """
        Right Multiplication operator
        :param other: An AD object or a real number 
        :return: An AD object
        """
        return self * other

    def __sub__(self, other):
        """
        Subtraction operator
        :param other: An AD object or a real number 
        :return: An AD object
        """
        temp_autodiff = AD(1)
        try:
            temp_autodiff.val = self.val - other.val
            temp_autodiff.partial_ders = self.partial_ders - other.partial_ders

            return temp_autodiff

        except AttributeError:
            temp_autodiff.val = self.val - other
            temp_autodiff.partial_ders = self.partial_ders

            return temp_autodiff

    def __rsub__(self, other):
        """
        Right subtraction operator
        :param other: An AD object or a real number
        :return: An AD object
        """
        return (-self) + other

    def __neg__(self):
        """
        Negation operator
        :return: An AD object
        """
        return self * (-1)

    def arcsin(self):
        """
        Arcsin operator
        :return: An AD object
        """
        temp_autodiff = AD(1)

        if self.val > 1 or self.val < -1:
            raise (ArithmeticError("Input out of range. Input value should be in the range of [-1,1]!"))

        temp_autodiff.val = np.arcsin(self.val)
        temp_autodiff.partial_ders = (1 / np.sqrt(1 - self.val ** 2)) * self.partial_ders

        return temp_autodiff

    def arccos(self):
        """
        Arccos operator
        :return: An AD object
        """
        temp_autodiff = AD(1)

        if self.val > 1 or self.val < -1:
            raise (ArithmeticError("Input out of range. Input value should be in the range of [-1,1]!"))

        temp_autodiff.val = np.arccos(self.val)
        temp_autodiff.partial_ders = -(1 / np.sqrt(1 - self.val ** 2)) * self.partial_ders

        return temp_autodiff

    def arctan(self):
        """
        Arctan operator
        :return: An AD object
        """
        temp_autodiff = AD(1)

        temp_autodiff.val = np.arctan(self.val)
        temp_autodiff.partial_ders = (1 / (1 + self.val ** 2)) * self.partial_ders

        return temp_autodiff

    # Lanting Li

    def log(self, base=math.e):
        """
        Returns a new AD object which represents log(x,base)
        :param base: log base
        :return: an AD object
        """
        assert type(base) is float or type(base) is int, "Illegal base"

        temp_autodiff = AD(1)
        if base == 0:
            raise (ZeroDivisionError("Cannot calculate derivative(s): base is zero"))
        elif base < 0:
            raise (ArithmeticError("Math domain error: base is less than 0"))
        elif np.any(self.val == 0):
            raise (ZeroDivisionError("Cannot calculate derivatives: value is zero"))
        elif np.any(self.val < 0):
            raise (ArithmeticError("Math domain error: value is less than zero"))
        else:
            if type(self.val) is float or type(self.val) is int:
                temp_autodiff.val = math.log(self.val, base)  # loga(x)
                temp_autodiff.partial_ders = (1 / (self.val * np.log(base))) * self.partial_ders  # 1 / (x * ln(a)) * x'
            elif type(self.val) is np.ndarray:
                temp_autodiff.val = np.log(self.val) / np.log(base)
                temp_autodiff.partial_ders = (1 / (self.val * np.log(base))) * self.partial_ders
            else:
                raise (TypeError("Type of value of input AD object can only be int, float, or numpy ndarray."))

            return temp_autodiff

    def sqrt(self):
        """
        Returns a new AD object which represent the squared root of original AD object
        :return: an AD object
        """
        temp_autodiff = AD(1)
        if np.any(self.val == 0):
            # temp_autodiff.val = 0
            # temp_autodiff.partial_ders = 0
            raise (ZeroDivisionError("Cannot calculate derivatives: Value is zero"))
        elif np.any(self.val < 0):
            raise (ArithmeticError("Math domain error: value is less than 0"))
        else:
            temp_autodiff.val = np.sqrt(self.val)
            temp_autodiff.partial_ders = (1 / (2 * np.sqrt(self.val))) * self.partial_ders

            return temp_autodiff

    def exp(self, base=math.e):  # a^x (a default to be e if not specified)
        """
        Return a new AD object which represents base^x
        :param base: exponential base, should be either float or int
        :return: an AD object.
        """

        assert type(base) is float or type(base) is int, "Illegal base"

        temp_autodiff = AD(1)

        if base == 0:
            temp_autodiff.val = 0
            temp_autodiff.partial_ders = 0
        elif base < 0:
            raise (ArithmeticError("Cannot calculate derivatives: base is less than 0"))
        else:
            temp_autodiff.val = base ** self.val  # a^x
            temp_autodiff.partial_ders = np.log(base) * (base ** self.val) * self.partial_ders  # ln(a) * a^x * x'

        return temp_autodiff

    def __pow__(self, other):
        """
        Return a new AD object which represents self**a where a should be a real number
        :param other: Real number, power
        :return: an AD represents x**a
        """

        assert type(other) is float or type(other) is int, "Illegal power"

        temp_autodiff = AD(1)

        temp_autodiff.val = self.val ** other  # x^a
        temp_autodiff.partial_ders = other * (self.val ** (other - 1)) * self.partial_ders  # a * x^(a-1) * x'

        return temp_autodiff

    def __eq__(self, other):
        """
        To evaluate if the two AD objects are equal.
        :param other: Another AD object to evaluate if both value and partial derivatives
            are equal to of self AD object.
        :return: True or False
        """

        if type(self.val) is np.ndarray and type(other.val) is np.ndarray:
            val_eq = np.all(np.isclose(self.val, other.val))
        elif (type(self.val) is int or type(self.val) is float) and \
                (type(other.val) is int or type(other.val) is float):
            val_eq = np.isclose(self.val, other.val)
        else:
            return False

        if type(self.partial_ders) is np.ndarray and type(other.partial_ders) is np.ndarray:
            der_eq = np.all(np.isclose(self.partial_ders, other.partial_ders))
        elif (type(self.partial_ders) is int or type(self.partial_ders) is float) and \
                (type(other.partial_ders) is int or type(other.partial_ders) is float):
            der_eq = np.isclose(self.partial_ders, other.partial_ders)
        else:
            return False
        return (val_eq and der_eq)

    def __ne__(self, other):
        """
        To evaluate if the two AD objects are non-equal.
        :param other: Another AD object to evaluate if either value or partial derivatives
            is not equal to of self AD object.
        :return: True or False
        """
        return (self == other) == False

    def sigmoid(self):
        """
        Logistic function.
        :return: an AD function represents 1/(1+exp(-x))
        """

        temp_autodiff = AD(1)

        temp_autodiff.val = 1 / (1 + math.e ** (-self.val))
        temp_autodiff.partial_ders = temp_autodiff.val * (1 - temp_autodiff.val) * self.partial_ders

        return temp_autodiff

    # Jenny Dong

    def __truediv__(self, other):
        """
        Division operator
        :param other: another node object or scalar value
        :return: An AD object
        """
        temp_autodiff = AD(1)

        try:
            if other.val == 0:
                raise (ZeroDivisionError("Cannot divide by zero"))
            temp_autodiff.val = self.val / other.val
            # use division rule
            temp_autodiff.partial_ders = (
                                                 self.partial_ders * other.val - other.partial_ders * self.val) / other.val ** 2

            return temp_autodiff

        except AttributeError:
            # when the other value is a float
            if other == 0:
                raise (ZeroDivisionError("Cannot divide by zero"))
            temp_autodiff.val = self.val / other
            temp_autodiff.partial_ders = self.partial_ders / other

            return temp_autodiff

    def sin(self):
        """
        sin(x)
        :return: An AD object
        """
        temp_autodiff = AD(1)

        temp_autodiff.val = np.sin(self.val)
        temp_autodiff.partial_ders = np.cos(self.val) * self.partial_ders

        return temp_autodiff

    def cos(self):
        """
        cos(x)
        :return: An AD object
        """
        temp_autodiff = AD(1)

        temp_autodiff.val = np.cos(self.val)
        temp_autodiff.partial_ders = 0 - np.sin(self.val) * self.partial_ders
        return temp_autodiff

    def tan(self):
        """
        tan(x)
        :return: An AD object
        """
        # raise error for tan(pi/2)
        if self.val % (math.pi / 2) == 0 and self.val != 0:
            raise (ArithmeticError("Tan(pi/2) should be undefined"))
        temp_autodiff = AD(0)

        temp_autodiff.val = np.tan(self.val)
        temp_autodiff.partial_ders = ((1 / np.cos(self.val)) ** 2) * self.partial_ders  # x' * 1/cos(x)^2
        return temp_autodiff

    def sinh(self):
        """
        sinh(x), range: (-inf, inf)
        :return: An AD object
        """
        temp_autodiff = AD(0)
        temp_autodiff.val = np.sinh(self.val)
        temp_autodiff.partial_ders = np.cosh(self.val) * self.partial_ders
        return temp_autodiff

    def cosh(self):
        """
        cosh(x), range: (-inf, inf)
        :return: An AD object
        """
        temp_autodiff = AD(0)
        temp_autodiff.val = np.cosh(self.val)
        temp_autodiff.partial_ders = np.sinh(self.val) * self.partial_ders
        return temp_autodiff

    def tanh(self):
        """
        tanh(x), range: (-inf, inf)
        :return: An AD object
        """

        temp_autodiff = AD(0)
        temp_autodiff.val = np.tanh(self.val)
        temp_autodiff.partial_ders = self.partial_ders / (np.cosh(self.val) ** 2)
        return temp_autodiff

    def __str__(self):
        """
        Return string representation
        :return: str
        """
        if self.digits < 0:
            return f"The value and derivative of current function are {self.val} and {self.partial_ders}"
        else:
            return f"The value and derivative of current function are {round(self.val, self.digits)} and {np.round(self.partial_ders, self.digits)}"
