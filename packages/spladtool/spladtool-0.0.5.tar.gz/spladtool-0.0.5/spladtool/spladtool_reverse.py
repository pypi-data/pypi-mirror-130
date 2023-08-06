import numpy as np
from typing import Union, List


# TENSOR SCRIPT ========================================
class Tensor():
    '''
    A class for lazily-computed variables with auto-differentiation
    '''

    def __init__(self, x=None):
        '''
        Construct a Tensor object to perform reverse mode automatic differentation.
        
        Parameters
        ----------
        x : np.ndarray, list, int, float or np.float_, optional, default is None
            values of the variable at which to compute the derivative
       
        Returns
        -------
        A Tensor object with the corresponding value, gradient, and dependency(used to track the dependent tensor objects)
        
        Examples
        --------
        >>> x = Tensor([[1.], [2.], [3.]])
        >>> z = x + 4
        >>> print(z)
        spladtool_reverse.Tensor([[5.], [6.], [7.]])   
        
        >>> print(z.dependency)
        [spladtool_reverse.Tensor([[1.], [2.], [3.]])]
        '''
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
        '''
        Method that calls the layer.backward method with arguments being corresponding dependencies
        Parameters
        ----------
        g : np.ndarray, list, int, or float, optional, default is None
        '''
        if g is None:
            g = np.ones_like(self.data)
        assert g.shape == self.data.shape
        self._grad += g
        if self.dependency is not None:
            self.layer.backward(*self.dependency, g)

    def __repr__(self):
        '''
        Dunder method for returning the representation of the Tensor object
        '''
        return str(self)

    def __str__(self):
        '''
        Dunder method for returning a readable string representation of the Tensor object
        '''
        return 'spladtool_reverse.Tensor(%s)' % str(self.data)

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
        spladtool_reverse.Tensor([[2.], [3.], [4.]])
        
        Add another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [1.0], [1.0]])
        >>> z = x + y
        >>> print(z)
        spladtool_reverse.Tensor([[2.], [3.], [4.]])
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
        spladtool_reverse.Tensor([[5.], [6.], [7.]])
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
        spladtool_reverse.Tensor([[3.], [6.], [9.]])
        
        Multiply by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [2.0], [3.0]])
        >>> z = x * y
        >>> print(z)
        spladtool_reverse.Tensor([[1.], [4.], [9.]])
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
        spladtool_reverse.Tensor([[4.], [8.], [12.]])
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
        spladtool_reverse.Tensor([[1.], [2.], [3.]])
        
        Divide by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [2.0], [3.0]])
        >>> z = x / y
        >>> print(z)
        spladtool_reverse.Tensor([[1.], [1.], [1.]])
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
        spladtool_reverse.Tensor([[4.], [2.], [1.]])
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
        spladtool_revrese.Tensor([[1.], [4.], [16.]])
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
        spladtool_reverse.Tensor([[-1.], [-2.], [-4.]])
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
        spladtool_reverse.Tensor([[0.], [1.], [2.]])
        
        Subtract by another Tensor object
        >>> x = Tensor([[1.0], [2.0], [3.0]])
        >>> y = Tensor([[1.0], [1.0], [1.0]])
        >>> z = x - y
        >>> print(z)
        spladtool_reverse.Tensor([[0.], [1.], [2.]])
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
        spladtool_reverse.Tensor([[3.], [2.], [1.]])
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
        spladtool_reverse.Tensor([[True, True], [True, True]])
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
        spladtool_reverse.Tensor([[True, True], [False, False]])
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
        spladtool_reverse.Tensor([[False, False], [True, True]])
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
        spladtool_reverse.Tensor([[False, True], [True, True]])
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
        spladtool_reverse.Tensor([[True, True], [False, False])
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
        spladtool_reverse.Tensor([[True, False], [True, True])
        '''
        return greater_equal(self, y)

    def mean(self):
        '''
        Dunder method for calculating the mean of the Tensor object
         
        Parameters
        ----------
        Examples
        --------
        >>> x = tensor([[1., 2.], [3., 4.]])
        >>> y = mean(x)
        >>> print(y)
        spladtool_reverse.Tensor(2.5)
        '''
        return mean(self)

    def sum(self):
        '''
        Dunder method for calculating the mean of the Tensor object
         
        Parameters
        ----------
        Examples
        --------
        >>> x = tensor([[1., 2.], [3., 4.]])
        >>> y = sum(x)
        >>> print(y)
        spladtool_reverse.Tensor(10.0)
        '''
        return sum(self)

    def repeat(self, times):
        '''
        Dunder method for repeating a Tensor with single value for arbitrary times
         
        Parameters
        ----------
        times: int
            
        Examples
        --------
        >>> x = tensor(2)
        >>> print(repeat(x, 4))
        spladtool_reverse.Tensor([2. 2. 2. 2.])
        '''
        return repeat(self, times)

    @property
    def shape(self):
        '''
        Return the shape of the Tensor object as a property object
        '''
        return self._shape

    @property
    def grad(self):
        '''
        Return the gradient of the Tensor object as a property object
        '''
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
    spladtool_reverse.Tensor([[ 2.71828183, 7.3890561 ], [20.08553692, 54.59815003]])
    '''
    return Exp()(x)

def log(x: Tensor) -> Tensor:
    '''
    Compute the logarithm of a Tensor object
    
    Parameters
    ----------
    x : Tensor
    
    Examples
    -------
    >>> x = tensor([[1., 2.], [3., 4.]])
    >>> z = log(x)
    >>> print(z)
    spladtool_reverse.Tensor([[0., 0.69314718], [1.09861229, 1.38629436]])    
    '''
    return Log()(x)

def sqrt(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[12., 2.], [4., 4.]])
    '''
    return SquareRoot()(x)

def sin(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[ 0.84147098, 0.90929743], [ 0.14112001, -0.7568025 ]])
    '''
    return Sin()(x)

def cos(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[0.54030231, -0.41614684], [-0.9899925, -0.65364362]])
    '''
    return Cos()(x)

def tan(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[1.55740772, -2.18503986], [-0.14254654, 1.15782128]])
    '''
    return Tan()(x)

def arcsin(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[1.47062891, 1.36943841], [1.26610367, 1.15927948]])
    '''
    return ArcSin()(x)

def arccos(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[0.09966865, 0.19739556], [0.29145679, 0.38050638]])
    '''
    return ArcCos()(x)

def arctan(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[0.10016742, 0.20135792], [0.30469265 0.41151685]])
    '''
    return ArcTan()(x)

def sinh(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[1.17520119, 3.62686041], [10.01787493, 27.2899172 ]])
    '''
    return Sinh()(x)

def cosh(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[ 1.54308063, 3.76219569], [10.067662, 27.30823284]])
    '''
    return Cosh()(x)

def tanh(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[0.76159416, 0.96402758], [0.99505475, 0.9993293 ]])
    '''
    return Tanh()(x)

def logistic(x: Tensor) -> Tensor:
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
    spladtool_reverse.Tensor([[0.73105858, 0.88079708], [0.95257413, 0.98201379]])
    '''
    return 1 / (1 + exp(-x))

def sum(x: Tensor) -> Tensor:
    return Sum()(x)

def mean(x: Tensor) -> Tensor:
    return sum(x) / np.prod(x.data.shape)

def log_prob(x: Tensor) -> Tensor:
    return log(logistic(x))

def repeat(x: Tensor, times: int) -> Tensor:
    return Repeat()(x, times)

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


# FUNCTIONAL SCRIPT ====================================


# LAYER SCRIPT ====================================
class Layer():
    '''
    Base class for all following functional classes to inherit from
    
    Note: when a functional class is called by a function, it will automatically call its forward method with the corresponding arguments 
    '''
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
        '''
        Perform the operation of rasing the Tensor object to the power of p
    
        Parameters
        ----------
        x : Tensor
        p : float
    
        Returns
        -------
        A new Tensor object with updated values and dependency after power operation
    
        '''
        y = Tensor(np.power(x.data.copy(), self.p))
        y.dependency = [x]
        y.layer = self
        return y

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the power
        '''
        grad = self.p * np.power(x.data.copy(), self.p - 1) * g
        x.backward(grad)


class TensorSum(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorSum'

    def forward(self, x, y):
        '''
        Perform the operation of adding two Tensor objects
        Parameters
        ----------
        x : Tensor
        y : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and dependency after addition
        
        '''
        assert x.shape == y.shape
        s_data = x.data + y.data
        s = Tensor(s_data)
        s.dependency = [x, y]
        s.layer = self
        return s

    def backward(self, x, y, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after addition
        '''
        x_grad = g.copy()
        y_grad = g.copy()
        x.backward(x_grad)
        y.backward(y_grad)


class TensorProd(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorProd'

    def forward(self, x, y):
        '''
        Perform the operation of multiplicating two Tensor objects
        
        Parameters
        ----------
        x : Tensor
        y : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after multiplication
        
        '''
        assert x.shape == y.shape
        p_data = x.data * y.data
        p = Tensor(p_data)
        p.dependency = [x, y]
        p.layer = self
        return p

    def backward(self, x, y, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after multiplication
        '''
        x_grad = y.data * g
        y_grad = x.data * g
        x.backward(x_grad)
        y.backward(y_grad)


class TensorInv(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.TensorInv'

    def forward(self, x):
        '''
        Perform the operation of taking the inverse of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking its inverse
        '''
        i_data = 1. / x.data
        i = Tensor(i_data)
        i.dependency = [x]
        i.layer = self
        return i

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the inverse
        '''
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
        '''
        Perform the operation of multiplying a Tensor object by number(s)
        Parameters
        ----------
        x : Tensor
        y : int, float, list, or np.ndarray
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after mutiplication with number(s)
        '''
        s_data = x.data * self.num
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after multiplying by number(s)
        '''
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
        '''
        Perform the operation of adding number(s) to a Tensor object 
        
        Parameters
        ----------
        x : Tensor
        y : int, float, list, or np.ndarray
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after adding number(s) to it
        '''
        s_data = x.data + self.num
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after adding to number(s)
        '''
        x.backward(g)


class Exp(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Exp'

    def forward(self, x):
        '''
        Perform the operation of computing the exponential of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after computing the exponential
        '''
        s_data = np.exp(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the exponential
        '''
        grad = g * np.exp(x.data)
        x.backward(grad)


class Log(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Log'

    def forward(self, x):
        '''
        Compute the natural logarithm of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the natural log
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a non-positive value
        '''
        if (x.data <= 0).any():
            raise ValueError('Cannot take the log of something less than or equal to 0.')
        s_data = np.log(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the logarithm
        '''
        grad = g * (1. / x.data)
        x.backward(grad)


class SquareRoot(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.SquareRoot'

    def forward(self, x):
        '''
        Compute the square root of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the square root
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a negative value
        '''
        if (x.data < 0).any():
            raise ValueError('Cannot take the square root of something less than 0.')
        s_data = np.sqrt(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the square root
        '''
        grad = g * (1 / (2*np.sqrt(x.data)))
        x.backward(grad)

class Sin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Sin'

    def forward(self, x):
        '''
        Compute the sine of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the sine
        '''
        s_data = np.sin(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the sine
        '''
        grad = g * np.cos(x.data)
        x.backward(grad)

class Cos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cos'

    def forward(self, x):
        '''
        Compute the cosine of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the cosine
        '''
        s_data = np.cos(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the cosine
        '''
        grad = g * -np.sin(x.data)
        x.backward(grad)

class Tan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Tan'

    def forward(self, x):
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
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the tangent
        '''
        grad = g * (1. / np.cos(x.data)) ** 2
        x.backward(grad)


class ArcSin(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcSin'

    def forward(self, x):
        '''
        Compute the arcsine of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the arcsine
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a value out of range [-1, 1]
        '''
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcSin on something outside the range of [-1,1].')
        s_data = np.arcsin(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the arcsine
        '''
        grad = g * (1. / np.sqrt(1 - x.data**2))
        x.backward(grad)

class ArcCos(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcCos'

    def forward(self, x):
        '''
        Compute the arccosine of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the arccosine
        
        Raises
        ------
        ValueError : raise a ValueError if any element of x has a value out of range [-1, 1]
        '''
        if (x.data < -1).any() or (x.data > 1).any():
            raise ValueError('Cannot perform ArcCos on something outside the range of [-1,1].')
        s_data = np.arccos(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the arccosine
        '''
        grad = g * (-1. / np.sqrt(1 - x.data**2))
        x.backward(grad)

class ArcTan(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.ArcTan'

    def forward(self, x):
        '''
        Compute the arctangent of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding denpendency after taking the arctangent
        '''
        s_data = np.arctan(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the arctangent
        '''
        grad = g * (1 / (1 + x.data**2))
        x.backward(grad)

class Sinh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Sinh'

    def forward(self, x):
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
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the hyperbolic sine
        '''
        grad = g * np.cosh(x.data)
        x.backward(grad)

class Cosh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cosh'

    def forward(self, x):
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
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the hyperbolic cosine
        '''
        grad = g * np.sinh(x.data)
        x.backward(grad)


class Tanh(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Cosh'

    def forward(self, x):
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
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the hyperbolic tangent
        '''
        grad = g * (1 - (np.tanh(x.data)**2))
        x.backward(grad)
        

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
        self.desc = 'spladtool_reverse.Layer.Comparator'
    
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
        '''
        backward function keeps track of the calculated gradient of the Tensor object after doing comparisons, which are all set to be np.nan
        '''
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
        '''
        Compute the sum of all elements of a Tensor object
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after taking the sum
        '''
        s_data = np.sum(x.data)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after taking the sum of all elements
        '''
        grad = g * np.ones_like(x.data)
        x.backward(grad)


class Repeat(Layer):
    def __init__(self):
        super().__init__()
        self.desc = 'spladtool_reverse.Layer.Repeat'

    def forward(self, x: Tensor, times: int):
        '''
        Repeat a Tensor object for arbitrary times
        
        Parameters
        ----------
        x : Tensor
        
        Returns
        -------
        A new Tensor object with updated values and corresponding dependency after repeating for arbitrary times
        '''
        assert len(x.shape) == 0
        s_data = np.repeat(x.data, times)
        s = Tensor(s_data)
        s.dependency = [x]
        s.layer = self
        return s

    def backward(self, x, g):
        '''
        backward function keeps track of the calculated gradient of the Tensor object after repeating for an arbitrary times
        '''
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
    
x = tensor([[1., 2.], [3., 4.]])
print(exp(x))
print(log(x))