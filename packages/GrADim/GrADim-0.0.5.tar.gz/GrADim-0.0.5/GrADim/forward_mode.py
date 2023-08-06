import numpy as np

from GrADim.GrADim import Gradim

class ForwardMode(Gradim):
    
    #Initialize the value and derivative, if the derivative is not provided set it to 1. (Essentailly dual number Value + e derivative)
    def __init__(self, value, derivative=None):
        self.value = value
        if derivative is not None:
            self.derivative = derivative
        else:
            self.derivative = np.ones(value.shape) if type(value) == np.ndarray else 1

    def __getitem__(self, item):
        new_derivative = np.zeros(self.derivative.shape)
        new_derivative[item] = self.derivative[item]
        return ForwardMode(self.value[item], new_derivative)

    def __add__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(self.value + other, self.derivative)
        return ForwardMode(self.value + other.value, self.derivative + other.derivative)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return ForwardMode(-self.value, -self.derivative)

    def __sub__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(self.value - other, self.derivative)
        return ForwardMode(self.value - other.value, self.derivative - other.derivative)

    def __rsub__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(other - self.value, - self.derivative)
        #return ForwardMode(other.value - self.value, other.derivative - self.derivative)

    def __mul__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(other * self.value, other * self.derivative)
        return ForwardMode(self.value * other.value, self.derivative * other.value + self.value * other.derivative)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        if type(power) != self.__class__:
            return ForwardMode(self.value ** power, power * self.derivative * self.value ** (power-1))
        return ForwardMode(self.value ** power.value, self.value**power.value * (power.derivative * np.log(self.value) + power.value/self.value*self.derivative) )
    
    def __rpow__(self, other, modulo=None):
        if type(other) != self.__class__:
            return ForwardMode(other ** self.value, (other ** self.value) * np.log(other)*self.derivative)
        #return other.__pow__(self)

    def __truediv__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(self.value / other, self.derivative / other)
        return ForwardMode(self.value / other.value, (self.derivative * other.value - self.value * other.derivative) / other.value ** 2)

    def __rtruediv__(self, other):
        if type(other) != self.__class__:
            return ForwardMode(other / self.value, - other * self.derivative / self.value**2)
        #return ForwardMode(other.value / self.value, (self.value * other.derivative - self.derivative * other.value) / self.value ** 2)
    
    def sqrt(self):
        return self**0.5
        
    def exp(self):
        return ForwardMode(np.exp(self.value), self.derivative * np.exp(self.value))

    def sin(self):
        return ForwardMode(np.sin(self.value), self.derivative * np.cos(self.value))
    
    def cosec(self):
        return 1 / Gradim.sin(self)

    def cos(self):
        return ForwardMode(np.cos(self.value), - self.derivative * np.sin(self.value))
    
    def sec(self):
        return 1 / Gradim.cos(self)

    def tan(self):
        return ForwardMode(np.tan(self.value), self.derivative * (1 + np.tan(self.value)**2))
    
    def cot(self):
        return 1 / Gradim.tan(self)
    
    def log(self, base = np.exp(1)):
        if type(base) != self.__class__:
            return ForwardMode(np.log(self.value)/np.log(base), self.derivative * (1/self.value)/np.log(base))
        return ForwardMode(np.log(self.value)/np.log(base.value), self.derivative * (1/self.value)/np.log(base.value) - base.derivative*(1/base.value)/np.log(base.value)**2)
    
    def ln(self):
        return Gradim.log(self)

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
    
    def sinh(self):
        return (Gradim.exp(self) - Gradim.exp(-self))/2
    
    def cosh(self):
        return (Gradim.exp(self) + Gradim.exp(-self))/2
    
    def tanh(self):
        return (Gradim.exp(self) - Gradim.exp(-self))/(Gradim.exp(self) + Gradim.exp(-self))
    
    def logistic(self):
        return 1/(1+Gradim.exp(-self))
        
    @staticmethod
    def multiple_outputs(func):
        """
        Just applying func to a ForwardMode object would give an array of ForwardMode objects.
        This function transforms this array into one single ForwardMode object
        """
        def wrapper(*args, **kwargs):
            Y = func(*args, **kwargs)
            Y_values = np.array([y.value for y in Y])
            Y_derivatives = np.array([y.derivative for y in Y])
            return ForwardMode(Y_values, Y_derivatives)
        return wrapper

    def arcsin(self):
        return ForwardMode(np.arcsin(self.value), self.derivative * (1/np.sqrt(1 - self.value**2)))
    
    def arccos(self):
        return ForwardMode(np.arccos(self.value), - self.derivative * (1/np.sqrt(1 - self.value**2)))

    def arctan(self):
        return ForwardMode(np.arctan(self.value), self.derivative * (1/(1 + self.value**2)))
    '''
    @staticmethod
    def Newton_Raphson(fun,x0,eps,epochs):
        xn = x0
        for i in range(epochs):
            X = ForwardMode(xn)
            y = fun(X)
            e = np.float(y.value) / np.float(y.derivative)
            xn = xn - e
            if abs(e) < eps:
                print("The root found is: ", xn)
                return xn
                
        print("Max epochs reached, the closest root value is: ", xn)
        return xn


if __name__ == "__main__":
    X = ForwardMode(2)
    # def f(x):
    #     return x**2 - 2
    #
    #
    # def g(x):
    #     return ForwardMode.exp(ForwardMode.sin(x))**0.2 + 2 * ForwardMode.sin(x) * ForwardMode.cos(x)
    #
    # Y = f(X)
    # print(Y.value)
    # print(Y.derivative)
    #
    # Y2 = g(X)
    # print(Y2.value)
    # print(Y2.derivative)
    #
    #
    # def f1(x):
    #     return x**2 - 2*x + 1
    #
    # def f2(x):
    #     return x
    #
    
    def f3(x):
        return ForwardMode.exp(ForwardMode.sin(x))**0.2 + 2 * ForwardMode.sin(x) * ForwardMode.cos(x)
    
    ForwardMode.Newton_Raphson(f1,1.4,0.01,100)
    ForwardMode.Newton_Raphson(f2,1.4,0.01,100)
    ForwardMode.Newton_Raphson(f3,1.4,0.01,100)
    
    multiple_X = ForwardMode(np.array([1, 2, 3]))

    def function_multiple_inputs(x):
        return Gradim.cos(x[0]) + Gradim.exp(x[2])*x[1]

    @ForwardMode.multiple_outputs
    def function_multiple_outputs(x):
        return 3*x, Gradim.sin(x), Gradim.sqrt(x)

    @ForwardMode.multiple_outputs
    def function_multiple_inputs_and_outputs(x):
        return x[0] + 2*x[1] * x[2], x[0] - x[2]

    Y1 = function_multiple_inputs(multiple_X)
    Y2 = function_multiple_outputs(X)
    Y3 = function_multiple_inputs_and_outputs(multiple_X)
    print(Y1.value)
    print(Y1.derivative)
    print(Y2.value)
    print(Y2.derivative)
    print(Y3.value)
    print(Y3.derivative)
    '''
