import numpy as np

from GrADim.GrADim import Gradim

class ReverseMode(Gradim):
    def __init__(self, value, derivative=None):
        self.value = value
        # The children attribute is a list of tuples. Each tuple contains the following node in the evaluation tree
        # and the constant by which it needs to be multiplied to compute the derivative
        self.children = []
        if derivative is not None:
            self.seed = derivative
        else:
            self.seed = np.ones(value.shape) if type(value) == np.ndarray else 1

    def __getitem__(self, item):
        weight = np.zeros(self.value.shape)
        weight[item] = 1
        new = ReverseMode(self.value[item], self.seed)
        self.children.append((weight, new))
        return new

    def __add__(self, other):
        if type(other) != self.__class__:
            new = ReverseMode(self.value + other, self.seed)
        else:
            new = ReverseMode(self.value + other.value, self.seed)
            other.children.append((1, new))
        self.children.append((1, new))
        return new

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        new = ReverseMode(- self.value, self.seed)
        self.children.append((-1, new))
        return new

    def __sub__(self, other):
        return self.__add__(- other)

    def __rsub__(self, other):
        return - self.__sub__(other)

    def __mul__(self, other):
        if type(other) != self.__class__:
            new = ReverseMode(self.value * other, self.seed)
            self.children.append((other, new))
        else:
            new = ReverseMode(self.value * other.value, self.seed)
            other.children.append((self.value, new))
            self.children.append((other.value, new))
        return new

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        if type(power) != self.__class__:
            new = ReverseMode(self.value ** power, self.seed)
            self.children.append((power * self.value ** (power - 1), new))
        else:
            new = ReverseMode(self.value ** power.value, self.seed)
            self.children.append((power.value * self.value ** (power.value - 1), new))
            power.children.append((np.log(self.value) * self.value ** power.value, new))
        return new

    def __rpow__(self, other, modulo=None):
        new = ReverseMode(other ** self.value, self.seed)
        self.children.append((np.log(other) * other ** self.value, new))
        return new

    def __truediv__(self, other):
        if type(other) != self.__class__:
            new = ReverseMode(self.value/other, self.seed)
            self.children.append((1/other, new))
        else:
            new = ReverseMode(self.value/other.value, self.seed)
            other.children.append((- self.value/other.value**2, new))
            self.children.append((1/other.value, new))
        return new

    def __rtruediv__(self, other):
        new = ReverseMode(other/self.value, self.seed)
        self.children.append((-other/self.value**2, new))
        return new

    def __eq__(self, other):
        if type(other) != self.__class__:
            return (self.value == other)
        return (self.value == other.value)

    def __ne__(self, other):
        if type(other) != self.__class__:
            return (self.value != other)
        return (self.value != other.value)

    def __lt__(self, other):
        if type(other) != self.__class__:
            return (self.value < other)
        return (self.value < other.value)

    def __gt__(self, other):
        if type(other) != self.__class__:
            return (self.value > other)
        return (self.value > other.value)

    def __le__(self, other):
        if type(other) != self.__class__:
            return (self.value <= other)
        return (self.value <= other.value)

    def __ge__(self, other):
        if type(other) != self.__class__:
            return (self.value >= other)
        return (self.value >= other.value)

    @property
    def derivative(self):
        leaves, derivatives = self.derivative_helper(1, [], [])
        if len(derivatives) == 1:
            return derivatives[0]
        return np.array(derivatives)

    def derivative_helper(self, const, leaves, derivatives):
        if not self.children:
            if any(self is leaf for leaf in leaves):
                derivatives[leaves.index(self)] += const * self.seed
            else:
                leaves.append(self)
                derivatives.append(const * self.seed)

        else:
            for const2, child in self.children:
                leaves, derivatives = child.derivative_helper(const * const2, leaves, derivatives)

        return leaves, derivatives

    def sqrt(self):
        return self**0.5

    def exp(self):
        new = ReverseMode(np.exp(self.value), self.seed)
        self.children.append((np.exp(self.value), new))
        return new

    def sin(self):
        new = ReverseMode(np.sin(self.value), self.seed)
        self.children.append((np.cos(self.value), new))
        return new

    def cosec(self):
        return 1/Gradim.sin(self)

    def cos(self):
        new = ReverseMode(np.cos(self.value), self.seed)
        self.children.append((-np.sin(self.value), new))
        return new

    def sec(self):
        return 1/Gradim.cos(self)

    def tan(self):
        new = ReverseMode(np.tan(self.value), self.seed)
        self.children.append((1 + np.tan(self.value)**2, new))
        return new

    def cot(self):
        return 1/Gradim.tan(self)

    def ln(self):
        return Gradim.log(self)

    def log(self, base=np.exp(1)):
        new = ReverseMode(np.log(self.value)/np.log(base), self.seed)
        self.children.append((1/(self.value * np.log(base)), new))
        return new

    def arcsin(self):
        new = ReverseMode(np.arcsin(self.value), self.seed)
        self.children.append((1/np.sqrt(1 - self.value**2), new))
        return new

    def arccos(self):
        new = ReverseMode(np.arccos(self.value), self.seed)
        self.children.append((- 1/np.sqrt(1 - self.value**2), new))
        return new

    def arctan(self):
        new = ReverseMode(np.arctan(self.value), self.seed)
        self.children.append((1/(1 + self.value**2), new))
        return new

    def sinh(self):
        return (Gradim.exp(self) - Gradim.exp(-self)) / 2

    def cosh(self):
        return (Gradim.exp(self) + Gradim.exp(-self)) / 2

    def tanh(self):
        return (Gradim.exp(self) - Gradim.exp(-self)) / (Gradim.exp(self) + Gradim.exp(-self))

    def logistic(self):
        return 1 / (1 + Gradim.exp(-self))

    @staticmethod
    def multiple_outputs(func):
        """
        Just applying func to a ReverseMode object would give an array of ReverseMode objects.
        This function transforms this array into one single ForwardMode object
        """
        def wrapper(X):
            Y = func(X)
            Y_values = np.array([y.value for y in Y])
            return ReverseMode(Y_values)
        return wrapper
