import numpy as np
from typing import Union, List


# TENSOR SCRIPT ========================================
class Tensor():
    '''
    A class for lazily-computed variables with auto-differentiation
    '''

    def __init__(self, x=None):
        super().__init__()
        if x is None:
            self.data = None
        else:
            assert type(x) in [np.ndarray, list, int, float, np.float64]
            if type(x) != np.ndarray:
                x = np.array(x).astype(float)
        self.data = x
        self._grad = np.zeros_like(self.data)
        self.dependency = None
        self.layer = None
        self._shape = x.shape

    def backward(self, g=None):
        if g is None:
            g = np.ones_like(self.data)
        assert g.shape == self.data.shape
        self._grad += g
        if self.dependency is not None:
            self.layer.backward(*self.dependency, g)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'spladtool_reverse.Tensor(%s)' % str(self.data)

    def __add__(self, y):
        return sumup(self, y)

    def __radd__(self, y):
        return self.__add__(y)

    def __mul__(self, y):
        return prod(self, y)

    def __rmul__(self, y):
        return self.__mul__(y)

    def __truediv__(self, y):
        return div(self, y)

    def __rtruediv__(self, y):
        return div(y, self)

    def __pow__(self, y):
        return power(self, y)

    def __rpow__(self, *args):
        raise NotImplementedError

    def __neg__(self):
        return neg(self)

    def __sub__(self, y):
        return minus(self, y)

    def __rsub__(self, y):
        return minus(y, self)
    
    def __eq__(self, y):
        return equal(self, y)

    def __lt__(self, y):
        return less(self, y)

    def __gt__(self, y):
        return greater(self, y)

    def __ne__(self, y):
        return not_equal(self, y)

    def __le__(self, y):
        return less_equal(self, y)
    
    def __ge__(self, y):
        return greater_equal(self, y)

    def mean(self):
        return mean(self)

    def sum(self):
        return sum(self)

    def repeat(self, times):
        return repeat(self, times)

    @property
    def shape(self):
        return self._shape

    @property
    def grad(self):
        return self._grad

# TENSOR SCRIPT ========================================


# FUNCTIONAL SCRIPT ====================================
def power(x, p):
    return Power(p)(x)


def sumup(x: Tensor, y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor:
    if type(y) == Tensor:
        return TensorSum()(x, y)
    else:
        return NumSum(y)(x)


def prod(x: Tensor, y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor:
    if type(y) == Tensor:
        return TensorProd()(x, y)
    else:
        return NumProd(y)(x)


def inv(x: Tensor) -> Tensor:
    return TensorInv()(x)


def div(x: Union[Tensor, int, float, Tensor, np.ndarray, list],
        y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor:
    if type(y) == Tensor:
        if type(x) == Tensor:
            return prod(x, inv(y))
        else:
            return x * inv(y)
    else:
        assert type(x) == Tensor
        return prod(x, 1. / y)


def neg(x: Tensor) -> Tensor:
    return prod(x, -1)


def minus(x: Union[Tensor, int, float, Tensor, np.ndarray, list],
          y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor:
    if type(y) == Tensor:
        if type(x) == Tensor:
            return sumup(x, -y)
        else:
            return sumup(-y, x)
    else:
        assert type(x) == Tensor
        return sumup(x, -y)

def exp(x: Tensor) -> Tensor:
    return Exp()(x)

def log(x: Tensor) -> Tensor:
    return Log()(x)

def sqrt(x: Tensor) -> Tensor:
    return SquareRoot()(x)

def sin(x: Tensor) -> Tensor:
    return Sin()(x)

def cos(x: Tensor) -> Tensor:
    return Cos()(x)

def tan(x: Tensor) -> Tensor:
    return Tan()(x)

def arcsin(x: Tensor) -> Tensor:
    return ArcSin()(x)

def arccos(x: Tensor) -> Tensor:
    return ArcCos()(x)

def arctan(x: Tensor) -> Tensor:
    return ArcTan()(x)

def sinh(x: Tensor) -> Tensor:
    return Sinh()(x)

def cosh(x: Tensor) -> Tensor:
    return Cosh()(x)

def tanh(x: Tensor) -> Tensor:
    return Tanh()(x)

def equal(x: Tensor, y) -> Tensor:
    return Equal()(x, y)

def less(x: Tensor, y) -> Tensor:
    return Less()(x,y)

def not_equal(x:Tensor, y) -> Tensor:
    return NotEqual()(x,y)
    
def greater(x: Tensor, y) -> Tensor:
    return Greater()(x,y)

def less_equal(x: Tensor, y) -> Tensor:
    return LessEqual()(x,y)

def greater_equal(x: Tensor, y) -> Tensor:
    return GreaterEqual()(x,y)

def sum(x: Tensor) -> Tensor:
    return Sum()(x)

def mean(x: Tensor) -> Tensor:
    return sum(x) / np.prod(x.data.shape)

def logistic(x: Tensor) -> Tensor:
    return 1 / (1 + exp(-x))

def log_prob(x: Tensor) -> Tensor:
    return log(logistic(x))

def repeat(x: Tensor, times: int) -> Tensor:
    return Repeat()(x, times)

# FUNCTIONAL SCRIPT ====================================


# LAYER SCRIPT ====================================
class Layer():
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer'

    def forward(self, *args):
        raise NotImplementedError

    def backward(self, *args):
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.desc

    def __str__(self) -> str:
        return self.desc

    def __call__(self, *args):
        return self.forward(*args)


class Power(Layer):
    def __init__(self, p):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Power'
        self.p = p

    def forward(self, x):
        y = Tensor(np.power(x.data.copy(), self.p))
        y.dependency = [x]
        y.layer = self
        return y

    def backward(self, x, g):
        grad = self.p * np.power(x.data.copy(), self.p - 1) * g
        x.backward(grad)


class TensorSum(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorSum'

    def forward(self, x, y):
        assert x.shape == y.shape
        s_data = x.data + y.data
        s = Tensor(s_data)
        s.dependency = [x, y]
        s.layer = self
        return s

    def backward(self, x, y, g):
        x_grad = g.copy()
        y_grad = g.copy()
        x.backward(x_grad)
        y.backward(y_grad)


class TensorProd(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorProd'

    def forward(self, x, y):
        assert x.shape == y.shape
        p_data = x.data * y.data
        p = Tensor(p_data)
        p.dependency = [x, y]
        p.layer = self
        return p

    def backward(self, x, y, g):
        x_grad = y.data * g
        y_grad = x.data * g
        x.backward(x_grad)
        y.backward(y_grad)


class TensorInv(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorInv'

    def forward(self, x):
        i_data = 1. / x.data
        i = Tensor(i_data)
        i.dependency = [x]
        i.layer = self
        return i

    def backward(self, x, g):
        grad = -1. / (x.data ** 2) * g
        x.backward(grad)


class NumProd(Layer):
    def __init__(self, num):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.NumProd'
        if type(num) == list:
            self.num = np.array(num)
        else:
            self.num = num

    def forward(self, x):
        s_data = x.data * self.num
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = self.num * g
        x.backward(grad)


class NumSum(Layer):
    def __init__(self, num):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.NumSum'
        if type(num) == list:
            self.num = np.array(num)
        else:
            self.num = num

    def forward(self, x):
        s_data = x.data + self.num
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        x.backward(g)


class Exp(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Exp'

    def forward(self, x):
        s_data = np.exp(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * np.exp(x.data)
        x.backward(grad)


class Log(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Log'

    def forward(self, x):
        if (x.data <= 0).any():
            raise ValueError('Cannot take the log of something less than or equal to 0.')
        s_data = np.log(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1. / x.data)
        x.backward(grad)


class SquareRoot(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.SquareRoot'

    def forward(self, x):
        if (x.data <= 0).any():
            raise ValueError('Cannot take the square root of something less than 0.')
        s_data = np.sqrt(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1 / (2*np.sqrt(x.data)))
        x.backward(grad)

class Sin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Sin'

    def forward(self, x):
        s_data = np.sin(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * np.cos(x.data)
        x.backward(grad)

class Cos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cos'

    def forward(self, x):
        s_data = np.cos(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * -np.sin(x.data)
        x.backward(grad)

class Tan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Tan'

    def forward(self, x):
        s_data = np.tan(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1. / np.cos(x.data)) ** 2
        x.backward(grad)


# need to raise error?? derivative is undefined outside of [-1,1]
# both ArcSin and ArcCos work with 1 input, but not with 2 inputs (e.g. z = arcsin(x*y)
class ArcSin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcSin'

    def forward(self, x):
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcSin on something outside the range of [-1,1].')
        s_data = np.arcsin(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1. / np.sqrt(1 - x.data**2))
        x.backward(grad)

class ArcCos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcCos'

    def forward(self, x):
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcCos on something outside the range of [-1,1].')
        s_data = np.arccos(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (-1. / np.sqrt(1 - x.data**2))
        x.backward(grad)

class ArcTan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcTan'

    def forward(self, x):
        s_data = np.arctan(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1 / (1 + x.data**2))
        x.backward(grad)

class Sinh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Sinh'

    def forward(self, x):
        s_data = np.sinh(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * np.cosh(x.data)
        x.backward(grad)

class Cosh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cosh'

    def forward(self, x):
        s_data = np.cosh(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * np.sinh(x.data)
        x.backward(grad)


class Tanh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cosh'

    def forward(self, x):
        s_data = np.tanh(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * (1 - (np.tanh(x.data)**2))
        x.backward(grad)
        

class Comparator(Layer):
    def __init__(self, cmp):
        super().__init__()
        self.cmp = cmp
        self.desc = 'spladtool_reverse.Layer.Comparator'
    
    def forward(self, x: Tensor, y: Union[float, int, np.ndarray, list, Tensor]) -> Tensor:
        if type(y) == int or type(y) == float:
            s_data = (self.cmp(x.data, y))
            return Tensor(s_data)
        elif type(y) == list:
            y = np.array(y)
        if (y.shape != x.shape):
            raise TypeError(f'param1{type(x)} and param2{type(y)} does not have the same shape')
        else:
            if type(y) == np.ndarray:
                s_data = (self.cmp(x.data, y))
            else:
                s_data = (self.cmp(x.data, y.data))
            return Tensor(s_data)

    def backward(self, x, y, g):
        x.backward(np.nan)
        y.backward(np.nan)


class Equal(Comparator):
    def __init__(self):
        super().__init__(np.equal)
        self.desc = 'spladtool_reverse.Layer.Equal'


class NotEqual(Comparator):
    def __init__(self):
        super().__init__(np.not_equal)
        self.desc = 'spladtool_reverse.Layer.NotEqual'
    

class Less(Comparator):
    def __init__(self):
        super().__init__(np.less)
        self.desc = 'spladtool_reverse.Layer.Less'


class Greater(Comparator):
    def __init__(self):
        super().__init__(np.greater)
        self.desc = 'spladtool_reverse.Layer.Greater'


class LessEqual(Comparator):
    def __init__(self):
        super().__init__(np.less_equal)
        self.desc = 'spladtool_reverse.Layer.LessEqual'


class GreaterEqual(Comparator):
    def __init__(self):
        super().__init__(np.greater_equal)
        self.desc = 'spladtool_reverse.Layer.GreaterEqual'

def tensor(x):
    return Tensor(x)


class Sum(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Sum'

    def forward(self, x):
        s_data = np.sum(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        grad = g * np.ones_like(x.data)
        x.backward(grad)


class Repeat(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Repeat'

    def forward(self, x: Tensor, times: int):
        assert len(x.shape) == 0
        s_data = np.repeat(x.data, times)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        x_grad = g.sum()
        x.backward(x_grad)

# LAYER SCRIPT ====================================



# EXAMPLE LAYERS==================================

class Module(Layer):
    '''
    Module inherits from a layer and does not requires a backward function
    However you can override it if you want.
    The Module class provides an interface to create your own models with trainable parameters
    You can register it in the init function and pass them to the optimizers by parameters() method
    '''
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Module'
        self.params = {}

    def register_param(self, **kwargs):
        for k, v in kwargs.items():
            self.params[k] = v
    
    def parameters(self):
        return self.params
    

class MSELoss(Module):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.MSE'

    def forward(self, y_true, y_pred):
        diff = y_true - y_pred
        diff_squared = diff ** 2
        mse = diff_squared.mean()  
        return mse
        

class BCELoss(Module):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.CE'

    def forward(self, y_true, y_pred):
        log_positive_prob = log_prob(y_pred)
        log_negative_prob = log_prob(1 - y_pred)
        nll = y_true * log_positive_prob + (1 - y_true) * log_negative_prob
        nll = -nll.mean()
        return nll