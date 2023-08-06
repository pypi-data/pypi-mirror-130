import numpy as np
from typing import Union, List

# TENSOR SCRIPT ========================================
class Tensor():
    def __init__(self, x=None, grad=None, seed=None):
        '''
        Construct a Tensor object to perform forward mode automatic differentation.
        
        Parameters
        ----------
        x : np.ndarray, list, int, float or np.float_, optional, default is None
            values of the variable at which to compute the derivative
        grad : np.ndarray, list, int, float or np.float_, optional, default is None
               gradient with respect to the variable
        seed : np.ndarray, list, int, float or np.float_, optional, default is None
               seed vector is used to perform directional derivative
        Returns
        -------
        A Tensor object with the corresponding value, gradient, and seed
        
        Examples
        --------
        >>> x = Tensor([[1.], [2.], [3.]])
        >>> z = x + 4
        >>> print(x)
        spladtool.Tensor([[1.], [2.], [3.]])
        
        >>> print(z)
        spladtool.Tensor([[5.], [6.], [7.]])
        
        >>> print(z.grad)
        [[1.], [1.], [1.]]    
        
        '''

        super().__init__()
        if x is None:
            self.data = None
        else:
            assert type(x) in [np.ndarray, list, int, float, np.float_]
            if type(x) != np.ndarray:
                x = np.array(x)
        self.data = x
        self._shape = x.shape
        if grad is None:
            grad = np.ones_like(self.data)
        self.grad = grad
        if seed is not None:
            self.grad = np.dot(grad, seed)

    
    def __repr__(self):
        '''
        Dunder method for returning the representation of the Tensor object
        '''
        return str(self)

    def __str__(self):
        '''
        Dunder method for returning a readable string representation of the Tensor object
        '''
        return 'spladtool.Tensor(\n%s\n)' % str(self.data)

    def __add__(self, y):
        '''
        Dunder method for adding another variable to the Tensor object
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        Add a scalar
        >>> x = Tensor([[1.], [2.], [3.]])
        >>> y = 1
        >>> z = x + y
        >>> print(z)
        spladtool.Tensor([[2.], [3.], [4.]])
        
        Add another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [1.0], [1.0]])
        >>> z = x + y
        >>> print(z)
        spladtool.Tensor([[2.], [3.], [4.]])
        '''
        return sumup(self, y)

    def __radd__(self, y):
        '''
        Dunder method for adding another variable to the Tensor object from left
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = 4
        >>> z = y + x
        >>> print(z)
        spladtool.Tensor([[5.], [6.], [7.]])
        '''
        return self.__add__(y)

    def __mul__(self, y):
        '''
        Dunder method for mutiplying the Tensor object by another variable
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        Mutiply by a scalar
        >>> x = Tensor([[1.], [2.], [3.]])
        >>> y = 3
        >>> z = x * y
        >>> print(z)
        spladtool.Tensor([[3.], [6.], [9.]])
        
        Multiply by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [2.0], [3.0]])
        >>> z = x * y
        >>> print(z)
        spladtool.Tensor([[1.], [4.], [9.]])
        '''
        return prod(self, y)

    def __rmul__(self, y):
        '''
        Dunder method for mutiplying the Tensor object by another variable from left
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = 4
        >>> z = y * x
        >>> print(z)
        spladtool.Tensor([[4.], [8.], [12.]])
        '''
        return self.__mul__(y)

    def __truediv__(self, y):
        '''
        Dunder method for dividing the Tensor object by another variable
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        Divide by a scalar
        >>> x = Tensor([[2.], [4.], [6.]])
        >>> y = 2
        >>> z = x / y
        >>> print(z)
        spladtool.Tensor([[1.], [2.], [3.]])
        
        Divide by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [2.0], [3.0]])
        >>> z = x / y
        >>> print(z)
        spladtool.Tensor([[1.], [1.], [1.]])
        '''
        return div(self, y)

    def __rtruediv__(self, y):
        '''
        Dunder method for dividing the Tensor object by another variable from left
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [4.0]])
        >>> y = 4
        >>> z = y / x
        >>> print(z)
        spladtool.Tensor([[4.], [2.], [1.]])
        '''
        return div(y, self)

    def __pow__(self, y):
        '''
        Dunder method for rasing the Tensor object to the power of y
                
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [4.0]])
        >>> y = 2
        >>> z = x ** y
        >>> print(z)
        spladtool.Tensor([[1.], [4.], [16.]])
        '''
        return power(self, y)

    def __rpow__(self, *args):
        raise NotImplementedError

    def __neg__(self):
        '''
        Dunder method for negating the Tensor object
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [4.0]])
        >>> z = -x
        >>> print(z)
        spladtool.Tensor([[-1.], [-2.], [-4.]])
        '''
        return neg(self)

    def __sub__(self, y):
        '''
        Dunder method for subtracting another variable from the Tensor object
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        Subtract by a scalar
        >>> x = Tensor([[1.], [2.], [3.]])
        >>> y = 1
        >>> z = x - y
        >>> print(z)
        spladtool.Tensor([[0.], [1.], [2.]])
        
        Subtract by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [1.0], [1.0]])
        >>> z = x - y
        >>> print(z)
        spladtool.Tensor([[0.], [1.], [2.]])
        '''
        return minus(self, y)

    def __rsub__(self, y):
        '''
        Dunder method for subtracting another variable from the Tensor object from left
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = 4
        >>> z = y - x
        >>> print(z)
        spladtool.Tensor([[3.], [2.], [1.]])
        '''
        return minus(y, self)

    def __eq__(self, y):
        '''
        Dunder method for performing "equality" comparison
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[1., 2.], [3., 4.]])
        >>> y = [[1, 2], [3, 4]]
        >>> print(x == y)
        spladtool.Tensor([[True, True], [True, True]])
        '''
        return equal(self, y)

    def __lt__(self, y):
        '''
        Dunder method for performing "less than" comparison
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[1., 2.], [3., 4.]])
        >>> y = np.array([[3, 4], [1, 2]])
        >>> print(x < y)
        spladtool.Tensor([[True, True], [False, False]])
        '''
        return less(self, y)

    def __gt__(self, y):
        '''
        Dunder method for performing "greater than" comparison
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[1., 2.], [3., 4.]])
        >>> y = np.array([[3, 4], [1, 2]])
        >>> print(x > y)
        spladtool.Tensor([[False, False], [True, True]])
        '''
        return greater(self, y)

    def __ne__(self, y):
        '''
        Dunder method for performing "not equal" comparison
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[3., 2.], [3., 4.]])
        >>> y = np.array([[3, 4], [1, 2]])
        >>> print(x != y)
        spladtool.Tensor([[False, True], [True, True]])
        '''
        return not_equal(self, y)

    def __le__(self, y):
        '''
        Dunder method for performing "less or equal than" comparison
        
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[3., 2.], [3., 4.]])
        >>> y = np.array([[3, 4], [1, 2]])
        >>> print(x <= y)
        spladtool.Tensor([[True, True], [False, False])
        '''
        return less_equal(self, y)

    def __ge__(self, y):
        '''
        Dunder method for performing "greater or equal than" comparison
         
        Parameters
        ----------
        y : int, float, np.ndarray, list or Tensor
        
        Examples
        --------
        >>> x = tensor([[3., 2.], [3., 4.]])
        >>> y = np.array([[3, 4], [1, 2]])
        >>> print(x >= y)
        spladtool.Tensor([[True, False], [True, True])
        '''
        return greater_equal(self, y)

    @property
    def shape(self):
        '''
        Return the shape of the Tensor object as a property object
        '''
        return self._shape
# TENSOR SCRIPT ========================================

# FUNCTIONAL SCRIPT ========================================
def power(x, p):
    return Power()(x, p)

def sumup(x: Tensor, y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor: 
    if type(y) == Tensor:
        return TensorSum()(x, y)
    else:
        return NumSum()(x, y)

def prod(x: Tensor, y: Union[int, float, Tensor, np.ndarray, list]) -> Tensor:
    if type(y) == Tensor:
        return TensorProd()(x, y)
    else:
        return NumProd()(x, y)

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

def exp(x: Tensor):
    '''
    Compute the exponential of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = exp(x)
    >>> print(z)
    spladtool([[ 2.71828183, 7.3890561 ], [20.08553692, 54.59815003]])
    '''
    return Exp()(x)

def exp_base(x: Tensor, base: float):
    '''
    Compute the exponential of a Tensor object with an arbitrary base value
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> base = 10
    >>> z = exp_base(x, base)
    >>> print(z)
    spladtool.Tensor([[10., 100.], [1000. 10000.]])
    '''
    return Exp_Base()(x, base)

def log(x: Tensor):
    '''
    Compute the logarithm of a Tensor object with
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = log(x)
    >>> print(z)
    spladtool.Tensor([[0., 0.69314718], [1.09861229, 1.38629436]])    
    '''
    return Log()(x)

def log_base(x: Tensor, base: float):
    '''
    Compute the logarithm of a Tensor object with an arbitrary base value
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = log_base(x, 10)
    >>> print(z)
    spladtool.Tensor([[0., 0.30103], [0.47712125, 0.60205999]])
    '''
    return Log_Base()(x, base)

def sin(x: Tensor):
    '''
    Compute the sine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = sin(x)
    >>> print(z)
    spladtool.Tensor([[ 0.84147098, 0.90929743], [ 0.14112001, -0.7568025 ]])
    '''
    return Sin()(x)

def cos(x: Tensor):
    '''
    Compute the cosine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = cos(x)
    >>> print(z)
    spladtool.Tensor([[0.54030231, -0.41614684], [-0.9899925, -0.65364362]])
    '''
    return Cos()(x)

def tan(x: Tensor):
    '''
    Compute the tangent of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = tan(x)
    >>> print(z)
    spladtool.Tensor([[1.55740772, -2.18503986], [-0.14254654, 1.15782128]])
    '''
    return Tan()(x)

def arcsin(x: Tensor):
    '''
    Compute the arcsine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[0.1, 0.2], [0.3, 0.4]])
    >>> z = arcsin(x)
    >>> print(z)
    spladtool.Tensor([[1.47062891, 1.36943841], [1.26610367, 1.15927948]])
    '''
    return ArcSin()(x)

def arccos(x: Tensor):
    '''
    Compute the arccosine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[0.1, 0.2], [0.3, 0.4]])
    >>> z = arccos(x)
    >>> print(z)
    spladtool.Tensor([[0.09966865, 0.19739556], [0.29145679, 0.38050638]])
    '''
    return ArcCos()(x)

def arctan(x: Tensor):
    '''
    Compute the arctangent of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[0.1, 0.2], [0.3, 0.4]])
    >>> z = arctan(x)
    >>> print(z)
    spladtool.Tensor([[0.10016742, 0.20135792], [0.30469265 0.41151685]])
    '''
    return ArcTan()(x)

def sinh(x: Tensor):
    '''
    Compute the hyperbolic sine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = sinh(x)
    >>> print(z)
    spladtool.Tensor([[1.17520119, 3.62686041], [10.01787493, 27.2899172 ]])
    '''
    return Sinh()(x)

def cosh(x: Tensor):
    '''
    Compute the hyperbolic cosine of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = cosh(x)
    >>> print(z)
    spladtool.Tensor([[ 1.54308063, 3.76219569], [10.067662, 27.30823284]])
    '''
    return Cosh()(x)

def tanh(x: Tensor):
    '''
    Compute the hyperbolic tangent of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = tanh(x)
    >>> print(z)
    spladtool.Tensor([[0.76159416, 0.96402758], [0.99505475, 0.9993293 ]])
    '''
    return Tanh()(x)

def logistic(x: Tensor):
    '''
    Apply logistic function to a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[-1., 2.], [-3., 4.]])
    >>> z = logistic(x)
    >>> print(z)
    spladtool.Tensor([[0.73105858, 0.88079708], [0.95257413, 0.98201379]])
    '''
    return Logistic()(x)

def sqrt(x: Tensor):
    '''
    Compute the square root of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[4., 4.], [16., 16.]])
    >>> z = sqrt(x)
    >>> print(z)
    spladtool.Tensor([[12., 2.], [4., 4.]])
    '''
    return SquareRoot()(x)

def abs(x: Tensor):
    '''
    Compute the absolute value of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[-1., 2.], [-3., 4.]])
    >>> z = abs(x)
    >>> print(z)
    spladtool.Tensor([[1., 2.], [3., 4.]])
    '''
    return Abs()(x)

def equal(x: Tensor, y):
    return Equal()(x, y)

def less(x: Tensor, y):
    return Less()(x, y)

def not_equal(x: Tensor, y):
    return NotEqual()(x, y)

def greater(x: Tensor, y):
    return Greater()(x, y)

def less_equal(x: Tensor, y):
    return LessEqual()(x, y)

def greater_equal(x: Tensor, y):
    return GreaterEqual()(x, y)

def tensor(x, seed=None):
    return Tensor(x, seed)
# FUNCTIONAL SCRIPT ====================================


# LAYER SCRIPT ====================================
class Layer():
    '''
    Base class for all following functional classes to inherit from
    
    Note: when a functional class is called by a function, it will return its automatically call method with the corresponding arguments 
    '''
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer'

    def forward(self, *args):
        raise NotImplementedError

    def __call__(self, *args):
        return self.forward(*args)

    def __str__(self):
        return self.desc

    def __repr__(self):
        return self.desc

class Power(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Power'

    def forward(self, x: Tensor, p: float) -> Tensor:
        '''
        Perform the operation of rasing the Tensor object to the power of p
    
        Parameters
        ----------
        x : Tensor
        p : float
    
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after power operation
    
        '''
        y_data = np.power(x.data.copy(), p)
        y_grad = p * np.power(x.data.copy(), p - 1) * x.grad
        y = Tensor(y_data, grad=y_grad)
        return y

class TensorSum(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.TensorSum'

    def forward(self, x: Tensor, y: Tensor) -> Tensor:
        '''
        Perform the operation of adding two Tensor objects
        Parameters
        ----------
        x : Tensor
        y : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after addition
        
        '''
        assert x.shape == y.shape
        s_data = x.data + y.data
        s_grad = x.grad + y.grad
        s = Tensor(s_data, s_grad)
        return s

class TensorProd(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.TensorProd'

    def forward(self, x: Tensor, y: Tensor) -> Tensor:
        '''
        Perform the operation of multiplicating two Tensor objects
        
        Parameters
        ----------
        x : Tensor
        y : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after multiplication
        
        '''
        assert x.shape == y.shape
        p_data = x.data * y.data
        p_grad = x.grad * y.data + x.data * y.grad
        p = Tensor(p_data, p_grad)
        return p

class TensorInv(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.TensorInv'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Perform the operation of taking the inverse of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking its inverse
        '''
        i_data = 1. / x.data
        i_grad = -1. / (x.data ** 2) * x.grad
        i = Tensor(i_data, i_grad)
        return i

class NumProd(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.NumProd'

    def forward(self, x: Tensor, y: Union[int, float, list, np.ndarray]) -> Tensor:
        '''
        Perform the operation of multiplying a Tensor object by number(s)
        Parameters
        ----------
        x : Tensor
        y : int, float, list, or np.ndarray
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after mutiplication with number(s)
        '''
        if type(y) == list:
            y = np.array(y)
        s_data = x.data * y
        s_grad = x.grad * y
        s = Tensor(s_data, s_grad)
        return s

class NumSum(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.NumSum'

    def forward(self, x: Tensor, y: Union[int, float, List[float], List[int], np.ndarray]) -> Tensor:
        '''
        Perform the operation of adding number(s) to a Tensor object 
        Parameters
        ----------
        x : Tensor
        y : int, float, list, or np.ndarray
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after adding number(s) to it
        '''
        if type(y) == list:
            y = np.array(y)
        s_data = x.data + y
        s_grad = x.grad
        s = Tensor(s_data, s_grad)
        return s

class Exp(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Exp'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Perform the operation of computing the exponential of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after computing the exponential
        '''
        s_data = np.exp(x.data)
        s_grad = np.exp(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Exp_Base(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.ExpBase'

    def forward(self, x: Tensor, base: float) -> Tensor:
        '''
        Perform the operation of computing the exponential with an arbitrary base of a Tensor object
        Parameters
        ----------
        x : Tensor
        base : float
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the exponential with an arbitrary base value
        '''
        s_data = base ** x.data
        s_grad = x.data * np.power(base, x.data - 1) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Sin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Sin'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Compute the sine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the sine
        '''
        s_data = np.sin(x.data)
        s_grad = np.cos(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Cos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Cos'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Compute the cosine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the cosine
        '''
        s_data = np.cos(x.data)
        s_grad = -np.sin(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Tan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Tan'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Compute the tangent of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the tangent
        '''
        s_data = np.tan(x.data)
        s_grad = 1 / (np.cos(x.data) * np.cos(x.data)) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Abs(Layer):
    def __init__(self):
        super().__init__()
        self.desc = "spladtool.Layer.Abs"

    def forward(self, x: Tensor) -> Tensor:
        '''
        Compute the absolute value of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the absolute value
        '''
        s_data = np.abs(x.data)
        s_grad = x.data / np.abs(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Log(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.LogBase'

    def forward(self, x: Tensor) -> Tensor:
        '''
        Compute the natural logarithm of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the natural log
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a non-positive value
        '''
        if (x.data <= 0).any():
            raise ValueError('Cannot take the log of something less than or equal to 0.')
        s_data = np.log(x.data)
        s_grad = 1. / x.data * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Log_Base(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.LogBase'

    def forward(self, x: Tensor, base: float) -> Tensor:
        '''
        Compute the logarithm with an arbitrary base value of a Tensor object
        Parameters
        ----------
        x : Tensor
        base : float
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the log with an arbitrary base
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a non-positive value
        '''
        if (x.data <= 0).any():
            raise ValueError('Cannot take the log of something less than or equal to 0.')
        s_data = np.log(x.data) / np.log(base)
        s_grad = (1. / (x.data * np.log(base))) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class ArcSin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.ArcSin'

    def forward(self, x: Tensor):
        '''
        Compute the arcsine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the arcsine
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a value out of range [-1, 1]
        '''
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcSin on something outside the range of [-1,1].')
        s_data = np.arcsin(x.data)
        s_grad = (1. / np.sqrt(1 - x.data ** 2)) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class ArcCos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.ArcCos'

    def forward(self, x: Tensor):
        '''
        Compute the arccosine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the arccosine
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a value out of range [-1, 1]
        '''
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcCos on something outside the range of [-1,1].')
        s_data = np.arccos(x.data)
        s_grad = (-1. / np.sqrt(1 - x.data ** 2)) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class ArcTan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.ArcTan'

    def forward(self, x: Tensor):
        '''
        Compute the arctangent of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the arctangent
        '''
        s_data = np.arctan(x.data)
        s_grad = (1. / (1 + x.data ** 2)) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Sinh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Sinh'

    def forward(self, x: Tensor):
        '''
        Compute the hyperbolic sine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the hyperbolic sine
        '''
        s_data = np.sinh(x.data)
        s_grad = np.cosh(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Cosh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Cosh'

    def forward(self, x: Tensor):
        '''
        Compute the hyperbolic cosine of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the hyperbolic cosine
        '''
        s_data = np.cosh(x.data)
        s_grad = np.sinh(x.data) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Tanh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Tanh'

    def forward(self, x: Tensor):
        '''
        Compute the hyperbolic tangent of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the hyperbolic tangent
        '''
        s_data = np.tanh(x.data)
        s_grad = (1. / np.cosh(x.data) ** 2) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Logistic(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.Logistic'

    def forward(self, x: Tensor):
        '''
        Apply the logistic function to a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after the logistic function
        '''
        s_data = np.exp(x.data) / (np.exp(x.data) + 1)
        s_grad = (np.exp(x.data) / (np.exp(x.data) + 1) ** 2) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class SquareRoot(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool.Layer.SquareRoot'

    def forward(self, x: Tensor):
        '''
        Compute the square root of a Tensor object
        Parameters
        ----------
        x : Tensor
        Returns
        -------
        A new Tensor object with updated values and corresponding gradients after taking the square root
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a negative value
        '''
        if (x.data < 0).any():
            raise ValueError('Cannot take the square root of something less than 0.')
        s_data = np.sqrt(x.data)
        s_grad = (1. / (2 * np.sqrt(x.data))) * x.grad
        s = Tensor(s_data, s_grad)
        return s

class Comparator(Layer):
    def __init__(self, cmp):
        '''
        Initiate a generic comparator object used for the specific comparison operator cmp
        Parameters
        ----------
        cmp : np.equal, np.not_equal, np.less, np.greater, np.less_equal, or np.greater_equal
        
        '''
        super().__init__()
        self.cmp = cmp
        self.desc = 'spladtool.Layer.Comparator'

    def forward(self, x: Tensor, y: Union[float, int, np.ndarray, list, Tensor]) -> Tensor:
        '''
        Compare every element in the data of two variable correspondingly using the comparison operator self.cmp
        Parameters
        ----------
        x : Tensor
        y : float, int, np.ndarray, list, or Tensor
        Returns
        -------
        A new Tensor object with the same shape as the input and contains boolean values produced by element-wise comparisons
            
        Raises
        ------
        TypeError: if the shapes of two parameters do not match, then they cannot be compare, so raise a TypeError
        '''
        if type(y) == int or type(y) == float:
            s_data = (self.cmp(x.data, y))
            s_grad = np.nan
            return Tensor(s_data, s_grad)
        elif type(y) == list:
            y = np.array(y)
        if (y.shape != x.shape):
            raise TypeError(f'param1{type(x)} and param2{type(y)} does not have the same shape')
        else:
            if type(y) == np.ndarray:
                s_data = (self.cmp(x.data, y))
            else:
                s_data = (self.cmp(x.data, y.data))
            s_grad = np.nan
            return Tensor(s_data, s_grad)

class Equal(Comparator):
    def __init__(self):
        super().__init__(np.equal)
        self.desc = 'spladtool.Layer.Equal'

class NotEqual(Comparator):
    def __init__(self):
        super().__init__(np.not_equal)
        self.desc = 'spladtool.Layer.NotEqual'

class Less(Comparator):
    def __init__(self):
        super().__init__(np.less)
        self.desc = 'spladtool.Layer.Less'

class Greater(Comparator):
    def __init__(self):
        super().__init__(np.greater)
        self.desc = 'spladtool.Layer.Greater'

class LessEqual(Comparator):
    def __init__(self):
        super().__init__(np.less_equal)
        self.desc = 'spladtool.Layer.LessEqual'

class GreaterEqual(Comparator):
    def __init__(self):
        super().__init__(np.greater_equal)
        self.desc = 'spladtool.Layer.GreaterEqual'