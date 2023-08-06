import numpy as np

class ReverseMode():
    def __init__(self, value):
        """
        Initializes ReverseMode object with a value that was passed in
        Inputs: Scalar or list or numpy array
        Returns: A ReverseMode object initialized with the value that is passed in

        Example:
        >>> x = ReverseMode([2, 3])
        >>> x.val
        array([2, 3])
        """
        if isinstance(value, (int, float)):
            self.value = np.array([value])
        elif isinstance(value, list):
            self.value = np.array(value)
        elif isinstance(value, np.ndarray):
            self.value = value
        else:
            raise TypeError("Enter a valid type (float, int, list or np.ndarray).")
        self.child = []
        self.gradient_coef = None

    def reset_gradient(self):
        """
        Sets the gradient of all its children to None
        Inputs: None
        Returns: None

        Example:
        >>> w = ReverseMode([1,2])
        >>> x = ReverseMode([3,4])
        >>> y = ReverseMode([5,6])
        >>> z = (3*x-w**2.5)/(x+y**w)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.25      , 0.07103553])
        >>> x.reset_gradient()
        >>> grads = []
        >>> for _, child in x.child:
        ...     grads.append(child.gradient_coef)
        ...     for _, child2 in child.child:
        ...         grads.append(child2.gradient_coef)
        ...
        >>> print(grads)
        [None, None, None, None]
        """
        self.gradient_coef = None
        for _, child in self.child:
            child.reset_gradient()

    def get_gradient(self):
        """
        Calculates the gradient with respect to the ReverseMode instance
        Inputs: None
        Returns: The gradient value (float)

        Example:
        >>> w = ReverseMode([1,2])
        >>> x = ReverseMode([3,4])
        >>> y = ReverseMode([5,6])
        >>> z = (3*x-w**2.5)/(x+y**w)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.25      , 0.07103553])
        """
        if self.gradient_coef is None:
            self.gradient_coef = sum(
                weight * child.get_gradient() for weight, child in self.child
            )
        return self.gradient_coef

    def __add__(self, other):
        """
        Overloads the addition operation
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the addition operation
        perform

        Example:
        >>> x = ReverseMode([1,2])
        >>> y = ReverseMode([3,4])
        >>> z = x + y
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1., 1.])
        >>>
        >>> x = ReverseMode([5,6])
        >>> z = x + 3
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1., 1.])

        """
        if isinstance(other, int) or isinstance(other, float):
            other = ReverseMode([other]*len(self.value))
        z = ReverseMode(self.value + other.value)
        one_array = np.ones(self.value.shape)
        self.child.append((one_array, z)) # weight = dz/dself = 1
        other.child.append((one_array, z)) # weight = dz/dother = 1
        return z

    def __radd__(self, other):
        """
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the addition operation
        performed between the argument that was passed in and the ReverseMode object

        Example:
        >>> x = ReverseMode([1.5,6.3])
        >>> z = 1 + x
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1., 1.])
        """
        return self + other

    def __sub__(self, other):
        """
        Overloads the subtraction operation
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the subtraction operation
        performed between the ReverseMode object and the argument that was passed in

        Example:
        >>> x = ReverseMode([1,2])
        >>> y = ReverseMode([3,4])
        >>> z = x - y
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1., 1.])
        >>>
        >>> x = ReverseMode([10,20])
        >>> z = x - 3
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1., 1.])
        """
        if isinstance(other, int) or isinstance(other, float):
            other = ReverseMode([other]*len(self.value))
        z = ReverseMode(self.value - other.value)
        self.child.append((np.ones(self.value.shape), z)) # weight = dz/dself = 1
        other.child.append((-np.ones(self.value.shape), z)) # weight = dz/dother = -1
        return z

    def __rsub__(self, other):
        """
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the subtraction operation
        performed between the ReverseMode object and the argument that was passed in

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = 2 - x
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-1., -1.])
        """
        if isinstance(other, int) or isinstance(other, float):
            other = ReverseMode([other]*len(self.value))
        z = ReverseMode( -self.value + other.value)
        self.child.append((-np.ones(self.value.shape), z)) 
        other.child.append((np.ones(self.value.shape), z)) 
        return z

    def __mul__(self, other):
        """
        Overloads the multiplication operation
        Inputs: Scalar or ReverseMode Instance
        Returns: A new AutoDiff object which is the result of the multiplication operation
        performed between the AutoDiff object and the argument that was passed in

        Example:
        >>> x = ReverseMode([-1,-2])
        >>> y = ReverseMode([10,20])
        >>> z = x * y
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([10, 20])
        >>>
        >>> x = ReverseMode([-1,-2])
        >>> z = x * 3
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([3, 3])
        """
        if isinstance(other, int) or isinstance(other, float):
            other = ReverseMode([other]*len(self.value))
        z = ReverseMode(self.value * other.value)
        self.child.append((other.value, z)) # weight = dz/dself = other.value
        other.child.append((self.value, z)) # weight = dz/dother = self.value
        return z

    def __rmul__(self, other):
        """
        Inputs: Scalar or AutoDiff Instance
        Returns: A new AutoDiff object which is the result of the multiplication operation
        performed between the AutoDiff object and the argument that was passed in

        Example:
        >>> x = ReverseMode([-1,-2])
        >>> z = 2 * x
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-2, -2])
        """
        return self * other

    def __truediv__(self, other):
        """
        Overloads the division operation
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the ReverseMode
        object divided by the argument that was passed in

        Example:
        >>> x = ReverseMode([-1,-2])
        >>> y = ReverseMode([10,20])
        >>> z = x / y
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1. , 0.5])
        >>>
        >>> x = ReverseMode([-1,-2])
        >>> z = x / 3
        >>> z.gradient_coef = 2
        >>> x.get_gradient()
        array([0.66666667, 0.66666667])
        """
        return self * (other ** (-1))

    def __rtruediv__(self, other):
        """
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the argument that
        was passed in divided by the ReverseMode object

        Example:
        >>> x = ReverseMode([10,5])
        >>> z = 2 / x
        >>> z.gradient_coef = 2
        >>> x.get_gradient()
        array([-0.04, -0.16])
        """
        return other*(self**(-1))

    def __pow__(self, other):
        """
        Overloads the power operation
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the ReverseMode object being
        raised to the power of the argument that was passed in

        Example:
        >>> x = ReverseMode([-2,-3])
        >>> y = ReverseMode([1,2])
        >>> z = x ** y
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([ 1., -6.])
        >>>
        >>> x = ReverseMode([-2,-3])
        >>> z = x ** 3
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([ 12., 27.])
        """

        if isinstance(other, ReverseMode):
            if len(other.value) == 1:
                other_val = other.value*np.ones(self.value.shape)
            elif len(other.value) != len(self.value):
                raise ValueError("You must have two vectors of the same length to use power on both.")
            else:
                other_val = other.value[:]
            val = np.array([float(v) ** o for v, o in zip(self.value, other_val)])
            z = ReverseMode(val)
            temp_der = np.array([float(v) ** (o - 1) for v, o in zip(self.value, other_val)])
            self.child.append((other_val * temp_der, z)) # weight = dz/dself
            other.child.append((val*np.log(self.value), z))
            return z
        elif isinstance(other, (float, int)):
            val = np.array([float(v) ** other for v in self.value])
            z = ReverseMode(val)
            temp_der = np.array([float(v) ** (other - 1) for v in self.value])
            self.child.append((other * temp_der, z))
            return z
        else:
            raise TypeError("Please us power with another ReverseMode object, int or float.")

    def __rpow__(self, other):
        """
        Inputs: Scalar or ReverseMode Instance
        Returns: A new ReverseMode object which is the result of the argument that was
        passed in being raised to the power of the ReverseMode object

        Example:
        >>> x = ReverseMode([-2,-3])
        >>> z = -2 ** x
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-0.1732868, -0.0866434])
        """

        if isinstance(other, ReverseMode):
            if len(other.value) == 1:
                other_val = other.value*np.ones(self.value.shape)
            elif len(other.value) != len(self.value):
                raise ValueError("You must have two vectors of the same length to use power on both.")
            else:
                other_val = other.value[:]
            val = np.array([float(o) ** v for v, o in zip(self.value, other_val)])
            z = ReverseMode(val)
            temp_der = np.array([(v*(float(o) ** (v-1))) for v, o in zip(self.value, other_val)])
            other.child.append((temp_der, z))
            self.child.append((val*np.log(other.value), z))
            return z
        elif isinstance(other, (float, int)):
            val = np.array([float(other) ** v for v in self.value])
            z = ReverseMode(val)
            self.child.append((val*np.log(other), z))
            return z
        else:
            raise TypeError("Please us power with another ReverseMode object, int or float.")


    def __neg__(self):
        """
        Inputs: None
        Returns: A new ReverseMode object which has the signs of
        the value and derivative ReverseModed

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = -x
        >>> z.gradient_coef = -3
        >>> x.get_gradient()
        array([3, 3])
        """
        return self.__mul__(-1)

    def __pos__(self):
        """
        Inputs: None
        Returns: The ReverseMode instance itself

        Example:
        >>> x = ReverseMode([1,2])
        >>> z = +x
        >>> z.gradient_coef = -3
        >>> x.get_gradient()
        -3
        """
        return self

    def sin(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the sine computation done on the value and derivative

        Example:
        >>> x = ReverseMode([3,5])
        >>> z = ReverseMode.sin(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-0.9899925 ,  0.28366219])
        """
        z = ReverseMode(np.sin(self.value))
        self.child.append((np.cos(self.value), z)) # z = sin(x) => dz/dx = cos(x)
        return z

    def cos(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the cosine computation
        done on the value and derivative

        Example:
        >>> x = ReverseMode([3,5])
        >>> z = ReverseMode.cos(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-0.14112001,  0.95892427])
        """
        z = ReverseMode(np.cos(self.value))
        self.child.append((-np.sin(self.value), z))
        return z

    def tan(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the tangent computation
        done on the value and derivative

        Example:
        >>> x = ReverseMode([1,2])
        >>> z = ReverseMode.tan(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([3.42551882, 5.7743992 , 1.02031952])
        """
        z = ReverseMode(np.tan(self.value))
        self.child.append((1 / (np.cos(self.value) ** 2), z))
        return z

    def sinh(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the hyperbolic sine
        computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-1,-2])
        >>> z = ReverseMode.sinh(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1.54308063, 3.76219569])
        """
        z = ReverseMode(np.sinh(self.value))
        self.child.append((np.cosh(self.value), z))
        return z

    def cosh(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the hyperbolic cosine
        computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-1,2])
        >>> z = ReverseMode.cosh(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-1.17520119,  3.62686041])
        """
        z = ReverseMode(np.cosh(self.value))
        self.child.append((np.sinh(self.value), z))
        return z

    def tanh(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the hyperbolic
        tangent computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-1,2])
        >>> z = ReverseMode.tanh(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.41997434, 0.07065082])
        """
        z = ReverseMode(np.tanh(self.value))
        self.child.append((1 / (np.cosh(self.value) ** 2), z))
        return z

    def exp(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the natural exponential
        computation done on the value  and derivative

        Example:
        >>> x = ReverseMode([2,3])
        >>> z = ReverseMode.exp(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([ 7.3890561 , 20.08553692])

        """
        z = ReverseMode(np.exp(self.value))
        self.child.append((np.exp(self.value), z))
        return z

    def exp_base(self, base):
        """
        Inputs: scalar
        Returns: A new ReverseMode object with the exponential (using a specified base)
        computation done on the value and derivative

        Example:
        >>> x = ReverseMode([1,2])
        >>> z = ReverseMode.exp_base(x, 2)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1.38629436, 2.77258872])
        """
        if isinstance(base, (int, float)):
            return self.__rpow__(base)
        else:
            raise TypeError("Please enter an int or float for base.")


    def arcsin(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the inverse
        sine computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-0.1,-0.2])
        >>> z = ReverseMode.arcsin(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([1.00503782, 1.02062073])
        """
        z = ReverseMode(np.arcsin(self.value))
        self.child.append((1 / (1 - (self.value**2))**0.5, z))
        return z

    def arccos(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the inverse
        cosine computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-0.1,-0.2])
        >>> z = ReverseMode.arccos(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([-1.00503782, -1.02062073])
        """
        z = ReverseMode(np.arccos(self.value))
        self.child.append((-1 / (1 - (self.value**2))**0.5, z))
        return z

    def arctan(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the inverse
        cosine computation done on the value and derivative

        Example:
        >>> x = ReverseMode([-0.1,-0.2])
        >>> z = ReverseMode.arctan(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.99009901, 0.96153846])
        """
        z = ReverseMode(np.arctan(self.value))
        self.child.append((1 / (1 + (self.value**2)), z))
        return z

    def logistic(self):
        """
        Inputs: None
        Returns: A new ReverseMode object calculated with logistic function

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = ReverseMode.logistic(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([4.53958077e-05, 2.06115361e-09])
        """
        z = ReverseMode(1/(1+np.exp(-self.value)))
        self.child.append((np.exp(-self.value)/((1+np.exp(-self.value))**2), z)) 
        return z


    def sqrt(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the square root
        computation done on the value and derivative

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = ReverseMode.sqrt(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.15811388, 0.1118034 ])
        """
        z = ReverseMode(self.value ** (1 / 2))
        self.child.append(((1 / 2) * (self.value ** (- 1 / 2)), z))
        return z

    def ln(self):
        """
        Inputs: None
        Returns: A new ReverseMode object with the natural log
        computation done on the value and derivative

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = ReverseMode.ln(x)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.1 , 0.05])
        """
        if (np.all(self.value > 0)) :
            z = ReverseMode(np.log(self.value))
            self.child.append(( 1 / self.value , z))
            return z
        else:
            raise ValueError("ReverseMode.ln only takes in positive numbers as arguments.")


    def log(self, base):
        """
        Inputs: scalar
        Returns: A new ReverseMode object with the log (using a specified
        base) computation done on the value and derivative

        Example:
        >>> x = ReverseMode([10,20])
        >>> z = ReverseMode.log(x, 2)
        >>> z.gradient_coef = 1
        >>> x.get_gradient()
        array([0.1442695 , 0.07213475])
        """
        if (np.all(self.value > 0) and base > 0):
            z = ReverseMode(np.log(self.value) / np.log(base))
            self.child.append((1 / (self.value * np.log(base)), z))
            return z
        else:
            raise ValueError("ReverseMode.log only takes in positive numbers as arguments.")

    def __eq__(self, other):
        """
        Overloads the equal comparision operator (==)
        Inputs: ReverseMode Instance
        Returns: True if self and other ReverseMode instance have the
        same value; False if not

        Example:
        >>> v = ReverseMode([1,2])
        >>> w = ReverseMode([3,4])
        >>> x = ReverseMode([5,4])
        >>> y = ReverseMode([5,4s])
        >>> v == w
        array([False, False])
        >>> w == x
        array([False,  True])
        >>> x == y
        array([ True,  True])
        """
        if isinstance(other, (int, float)):
            return np.equal(self.value, other)
        elif isinstance(other, ReverseMode):
            return np.equal(self.value, other.value)
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")

    def __ne__(self, other):
        """
        Overloads the not equal comparision operator (!=)
        Inputs: ReverseMode Instance
        Returns: False if self and other ReverseMode instance have the
        same value; True if not

        Example:
        >>> v = ReverseMode([3,4])
        >>> w = ReverseMode([4,6])
        >>> x = ReverseMode([5,6])
        >>> y = ReverseMode([5,6])
        >>> v != w
        array([ True,  True])
        >>> w != x
        array([ True, False])
        >>> x != y
        array([False, False])
        """
        if isinstance(other, (int, float)):
            return not np.equal(self.value, other)
        elif isinstance(other, ReverseMode):
            return self.value != other.value
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")


    def __lt__(self, other):
        """
        Compares the value of the ReverseMode instance with the input
        Inputs: Scalar or ReverseMode Instance
        Returns: True if self.value is less than other.value or
        if self.value is less than other; False if not

        Example:
        >>> v = ReverseMode([3,4])
        >>> w = ReverseMode([4,6])
        >>> x = ReverseMode([5,6])
        >>> y = ReverseMode([5,6])
        >>> v < w
        array([ True,  True])
        >>> w < x
        array([ True, False])
        >>> x < y
        array([False, False])
        """
        if isinstance(other, (int, float)):
            return np.less(self.value, other)
        elif isinstance(other, ReverseMode):
            return np.less(self.value, other.value)
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")

    def __le__(self, other):
        """
        Compares the value of the ReverseMode instance with the input
        Inputs: Scalar or ReverseMode Instance
        Returns: True if self.value is less than or equal to other.value or
        if self.value is less than or equal to other; False if not

        Example:
        >>> v = ReverseMode([3,4])
        >>> w = ReverseMode([4,6])
        >>> x = ReverseMode([5,6])
        >>> y = ReverseMode([5,6])
        >>> w <= v
        array([False, False])
        >>> x <= w
        array([False,  True])
        >>> y <= x
        array([ True,  True])
        """
        if isinstance(other, (int, float)):
            return np.less_equal(self.value, other)
        elif isinstance(other, ReverseMode):
            return np.less_equal(self.value, other.value)
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")

    def __gt__(self, other):
        """
        Compares the value of the ReverseMode instance with the input
        Inputs: Scalar or ReverseMode Instance
        Returns: True if self.value is greater than other.value or
        if self.value is greater than other; False if not

        Example:
        >>> v = ReverseMode([3,4])
        >>> w = ReverseMode([4,6])
        >>> x = ReverseMode([5,6])
        >>> y = ReverseMode([5,6])
        >>> w > v
        array([ True,  True])
        >>> x > w
        array([ True, False])
        >>> y > x
        array([False, False])
        """
        if isinstance(other, (int, float)):
            return np.greater(self.value, other)
        elif isinstance(other, ReverseMode):
            return np.greater(self.value, other.value)
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")

    def __ge__(self, other):
        """
        Compares the value of the ReverseMode instance with the input
        Inputs: Scalar or ReverseMode Instance
        Returns: True if self.value is greater than or equal to other.value or
        if self.value is greater than or equal to other; False if not

        Example:
        >>> v = ReverseMode([3,4])
        >>> w = ReverseMode([4,6])
        >>> x = ReverseMode([5,6])
        >>> y = ReverseMode([5,6])
        >>> v >= w
        array([False, False])
        >>> w >= x
        array([False,  True])
        >>> x >= y
        array([ True,  True])
        """
        if isinstance(other, (int, float)):
            return np.greater_equal(self.value, other)
        elif isinstance(other, ReverseMode):
            return np.greater_equal(self.value, other.value)
        else:
            raise TypeError("Please only compare ReverseMode object with another ReverseMode object or int or float.")
