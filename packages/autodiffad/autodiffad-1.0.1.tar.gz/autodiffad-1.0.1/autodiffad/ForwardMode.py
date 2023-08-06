# -*- coding: utf-8 -*-

import numpy as np

class DualNumber:
    
    def __init__(self, real = 1.0, dual = np.array([1.0])):
        """
        __init__(self, real = 1.0, dual = np.array([1.0]))

        Initiate a DualNumber object.
         
        Parameters
        ----------
        self : variable object
        real : integer/float, optional
            The value of the variable.
            Defalut value is 1.0.
        dual : array, optional
            The initial derivative of the variable.
            Default value is np.array([1.0]).
         
        Examples
        --------
        >>> x = DualNumber()

        Neither input real and dual value is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        """
        self.real = float(real)
        self.dual = dual       
  

    def __add__(self, other):
        """
        __add__(self, other)

        Dunder method for adding anthor DualNumber or number.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with `other` added.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = x + 1.2
        >>> x.real
        1.2
        >>> x.dual
        array([1.])

        Neither adding a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = x + y
        >>> z.real
        5.0
        >>> z.dual
        array([1, 1])
        """
        # if other is also a dual number
        if(isinstance(other, DualNumber)):
                       
            return DualNumber(self.real+other.real, self.dual+other.dual)
            
        # if other is an int or a float
        elif(isinstance(other, (int, float))):
                   
            return DualNumber(self.real+other, self.dual)
        
        # if trying to add an unsupported thing to a dual number
        else:
            raise AttributeError('Attribute not supported, e.g. not a dual number or int / float!')
    

    def __sub__(self, other):
        """
        __sub__(self, other)

        Dunder method for substracting anthor DualNumber or number.
    
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with `other` subtracted.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = x - 1.2
        >>> x.real
        -1.2
        >>> x.dual
        array([1.])

        Neither substracting a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = x - y
        >>> z.real
        -1.0
        >>> z.dual
        array([ 1, -1])
        """
        # reuse the add method
        # Note: if other is a dual number, this will automatically call the __mul__ method of that instance
        return self.__add__(-1*other) 


    def __rsub__(self, other):
        """
        __rsub__(self, other)

        Dunder method for substacted by anthor DualNumber or number.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with substracted by `other`.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = 1 - x
        >>> x.real
        1.0
        >>> x.dual
        array([-1.])

        Neither subtracted by a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = y - x
        >>> z.real
        1.0
        >>> z.dual
        array([-1,  1])
        """
        ##reuse the add method; Note: if other is a dual number, this will automatically call the __mul__ method of that instance
        t = self.__mul__(-1)
        return t.__add__(other)


    def __neg__(self):
        """
        __neg__(self)

        Dunder method for taking the negative.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object negation.
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = - x
        >>> x.real
        -0.0
        >>> x.dual
        array([-1.])
        """
        return DualNumber(-self.real, -self.dual)

    __isub__ = __sub__   
        
   
    def __mul__(self, other):
        """
        __mul__(self, other)

        Dunder method for multiplying anthor DualNumber or number.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with `other` multiplied.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = x * 4
        >>> x.real
        0.0
        >>> x.dual
        array([4.])

        Neither multiplying a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = x + y
        >>> z.real
        6.0
        >>> z.dual
        array([3., 2.])
        """
        #if other is also a dual number
        if(isinstance(other, DualNumber)):
             return DualNumber(self.real*other.real, self.real*other.dual+self.dual*other.real)
        
        #if other is an int or a float
        elif(isinstance(other, (int, float))):   
            return DualNumber(self.real*other, self.dual*other)
        
        #if trying to add an unsupported thing to a dual number
        else:
            raise AttributeError('Attribute not supported, e.g. not a dual number or int / float!')
    
    
    # when saying like dual number += sth, then it is the same as dual number + sth (but python calls a different dunder method for the += case)
    __iadd__ = __add__
    __imul__ = __mul__
     
    #saying that reverse multiplication is the same as multiplication   
    __rmul__ = __mul__  
    #saying that reverse addition is the same as addition   
    __radd__ = __add__  


    def __floordiv__(self, *args):
        """
        Raises
        ------
        NotImplementedError
          Floor division doesn't really make sense in our use case.
          Therefore raise an exception.
        """
        raise NotImplementedError('Floor division is not supported!')


    __rfloordiv__ = __floordiv__


    def __ifloordiv__(self, *args):
        """
        Raises
        ------
        NotImplementedError
          Ifloor division doesn't really make sense in our use case.
          Therefore raise an exception.
        """
        raise NotImplementedError('Floor division is not supported!')

       
    def __truediv__(self, other):
        """
        __truediv__(self, other)

        Dunder method for dividing anthor DualNumber or number.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with `other` divided.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = x / 2
        >>> x.real
        0.0
        >>> x.dual
        array([0.25])

        Neither dividing a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = x / y
        >>> z.real
        0.6666666666666666
        >>> z.dual
        array([ 0.33333333, -0.22222222])
        """
        #calculate the division complement of the other object, then reuse multiplication
        #e.g. if other = z1 (dual number), then calculate '1/z1' and reuse the mul-dunder-method
        
        #if other is also a dual number
        if(isinstance(other, DualNumber)):
            
            t = DualNumber(1/other.real, -1*(other.dual/(other.real*other.real)))
            
            return self.__mul__(t)
        
        #if other is an int or a float
        elif(isinstance(other, (int, float))):
            ##reusing the method from above
            
            t = DualNumber(1/other, 0)
            
            return self.__mul__(t)
        
        #if trying to add an unsupported thing to a dual number
        else:
            raise AttributeError('Attribute not supported, e.g. not a dual number or int / float!')


    #re-implementing the reverse true division of dual numbers, because division is NOT commutative
    def __rtruediv__(self, other):
        """
        __add__(self, other)

        Dunder method for being divided by anthor DualNumber or number.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object divided by `other`.

        Raises
        ------
        AttributeError
          If `other` is not integer, float or DualNumber. 
  
        Examples
        --------
        >>> x = DualNumber(real = 1)
        >>> x = 1 / x
        >>> x.real
        1.0
        >>> x.dual
        array([-1.])

        Neither divided by a DualNumber is acceptable.

        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> z = y / x
        >>> z.real
        1.5
        >>> z.dual
        array([-0.75,  0.5 ])
        """
        #we are creating the divisional complement of the instance of self, then we multiply it with other      
        t = DualNumber(1/self.real, -1*(self.dual/(self.real*self.real)))
            
        return t.__mul__(other)
        
    
    #to support both the __truediv__ as well as __div__ methods, which are the same in our context
    __div__ = __truediv__
    __itruediv__ = __truediv__
    

    def __eq__(self, other):
        """
        __eq__(self, other)

        Dunder method for comparing self with other to check if they are equal.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber

        Returns
        -------
        output : bool, True/False
          If self.real=other.real and self.dual=other.dual, retrurn True else return False.

        Examples
        --------
        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> x == y
        False
        """
        return self.real==other.real and (self.dual==other.dual).all()

    def __ne__(self, other):
        """
        __add__(self, other)

        Dunder method for comparing self ith other to check if they are not equal.
         
        Parameters
        ----------
        self : variable object
        other : DualNumber/integer/float

        Returns
        -------
        output : bool, True/False
          If self.real!=other.real or self.dual=other.dual, retrurn True else return False.
  
        Examples
        --------
        >>> x = DualNumber(real = 2, dual = np.array([1,0]))
        >>> y = DualNumber(real = 3, dual = np.array([0,1]))
        >>> x != y
        True
        """
        return self.real!=other.real or (self.dual!=other.dual).any()


    def __lt__ (self, other):
        """
        __lt__(self, other)
        
        Comapring self with other to check if self is less than other.

        Raises
        ------
        NotImplementedError
          Less than doesn't really make sense in our use case.
          Therefore raise an exception.
        """
        raise NotImplementedError('Less than comparison is not appliable to Dual Numbers!')


    def __gt__ (self, other):
        """
        __gt__(self, other)
        
        Comapring self with other to check if self is greater than other.

        Raises
        ------
        NotImplementedError
          Greater than doesn't really make sense in our use case.
          Therefore raise an exception.
        """
        raise NotImplementedError('Greater than comparison is not appliable to Dual Numbers!')


    def __le__ (self, other):
        """
        __le__(self, other)
        
        Comapring two dual numbers if self is less than or euqal to other.

        Raises
        ------
        NotImplementedError
          Less than doesn't really make sense in our use case.
          Therefore raise an exception.
        """
        raise NotImplementedError('Less than or equal to comparison is not appliable to Dual Numbers!')

    def __ge__ (self, other):
        """
        __ge__(self, other)
        
        Comapring self with other to check if self is greater than other.

        Raises
        ------
        NotImplementedError
          Greater than doesn't really make sense in our use case
          Therefore raise an exception
        """
        raise NotImplementedError('Greater than or equal comparison is not appliable to Dual Numbers!')
    

    def __pow__(self, p):
        """
        __pow__(self, other)

        Dunder method for powering self to p.
         
        Parameters
        ----------
        self : variable object
        p : integer/float

        Returns
        -------
        output : DualNumber
             A DualNumber object with `p` powered.
  
        Examples
        --------
        >>> x = DualNumber(real = 2)
        >>> x = x**3.4
        >>> x.real
        10.556063286183154
        >>> x.dual
        array([17.94530759])
        """
        return DualNumber(np.power(self.real,p), p * np.power(self.real,p-1) * self.dual)


    def exp(self, base=np.exp(1)):
        """
        exp(self)

        Taing exponential for any base.
  
        Parameters
        ----------
        self : variable object
        base : real, optional 
            The base of the exponential.
            Default value of the base is e.

        Returns
        -------
        output : DualNumber
             A DualNumber object with exponential for the base. 
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = DualNumber.exp(x)
        >>> x.real
        1.0
        >>> x.dual
        array([1.])

        Neither other base is acceptable.

        >>> x = DualNumber()
        >>> x = DualNumber.exp(x, base = 2.2)
        >>> x.real
        2.2
        >>> x.dual
        array([1.73460619])
        """
        return DualNumber(np.power(base, self.real), self.dual*np.power(base, self.real)*np.log(base))
    

    def sin(self):
        """
        sin(self)

        Taking sin.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with sin.
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = np.sin(x)
        >>> x.real
        0.0
        >>> x.dual
        array([1.])
        """
        return DualNumber(np.sin(self.real),self.dual*np.cos(self.real))
    

    def cos(self):
        """
        sin(self)

        Taking cos.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with cos.
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = np.cos(x)
        >>> x.real
        1.0
        >>> x.dual
        array([-0.])
        """
        return DualNumber(np.cos(self.real),self.dual*np.sin(self.real)*(-1))
    

    def tan(self):
        """
        sin(self)

        Taking tan.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with tan.
             
        Raises
        ------
        ValueError
          If self.real == pi/2 + (pi * n), where n is an integer.  
  
        Examples
        --------
        >>> x = DualNumber(real = 0)
        >>> x = np.tan(x)
        >>> x.real
        0.0
        >>> x.dual
        array([1.])
        """
        if self.real % np.pi == (np.pi/2):
            raise ValueError('Cannot take the tangent of pi/2 + (pi * n) when n is an integer!')
        return DualNumber(np.tan(self.real), self.dual*1/(np.cos(self.real)**2))
    

    def sqrt(self):
        """
        sqrt(self)

        Taking sqrt.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with sqrt.

        Raises
        ------
        ValueError
          If self.real < 0.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = np.sqrt(x)
        >>> x.real
        1.0
        >>> x.dual
        array([0.5])
        """
        if self.real < 0:
            raise ValueError('Cannot take sqrt of a negative value!')
        return DualNumber(np.sqrt(self.real), self.dual*1/(2*np.sqrt(self.real)))
    

    def log(self, base=np.exp(1)):
        """
        log(self)

        Taking log for any base.
         
        Parameters
        ----------
        self : variable object
        base : real, optional 
            The base of the log function.
            Default value for the base is e. 

        Returns
        -------
        output : DualNumber
             A DualNumber object with taking log.

        Raises
        ------
        ValueError
          If self.real <= 0.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = DualNumber.log(x)
        >>> x.real
        0.0
        >>> x.dual
        array([1.])

        Neither other base is acceptable.

        >>> x = DualNumber()
        >>> x = DualNumber.log(x, base = 2.2)
        >>> x.real
        0.0
        >>> x.dual
        array([1.2682994])
        """
        if self.real <= 0:
            raise ValueError('Cannot take the log of a nonpositive number!')
        return DualNumber(np.log(self.real)/np.log(base), self.dual*1.0/(self.real*np.log(base)))


    def arcsin(self):
        """
        arcsin(self)

        Taking arcsin.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with arcsin.

        Raises
        ------
        ValueError
          If self.real <= -1 or self.real >= 1.
  
        Examples
        --------
        >>> x = DualNumber(real = 0.5)
        >>> x = np.arcsin(x)
        >>> x.real
        0.5235987755982989
        >>> x.dual
        array([1.15470054])
        """
        if self.real >= 1 or self.real <= -1:
            raise ValueError('Please input value -1<x<1 for arcsin!')
        return DualNumber(np.arcsin(self.real), self.dual*1/(1-self.real**2)**(1/2))
    

    def arccos(self):
        """
        arccos(self)

        Taking log10.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with arccos.

        Raises
        ------
        ValueError
          If self.real <= -1 or self.real >= 1.
  
        Examples
        --------
        >>> x = DualNumber(real = 0.5)
        >>> x = np.arccos(x)
        >>> x.real
        1.0471975511965979
        >>> x.dual
        array([-1.15470054])
        """
        if self.real >= 1 or self.real <= -1:
            raise ValueError('Please input value -1<x<1 for arccos!')
        return DualNumber(np.arccos(self.real), self.dual*-1/(1-self.real**2)**(1/2))
    

    def arctan(self):
        """
        arctan(self)

        Taking arctan.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with arctan.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = np.arctan(x)
        >>> x.real
        0.7853981633974483
        >>> x.dual
        array([0.5])
        """
        return DualNumber(np.arctan(self.real), self.dual*1/(1+self.real**2))
    

    def sinh(self):
        """
        sinh(self)

        Taking sinh.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with sinh.

        Raises
        ------
        ValueError
          If self.real <= 0.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = np.sinh(x)
        >>> x.real
        1.1752011936438014
        >>> x.dual
        array([1.54308063])
        """
        return DualNumber(np.sinh(self.real), self.dual*np.cosh(self.real))


    def cosh(self):
        """
        cosh(self)

        Taking cosh.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with cosh.

        Raises
        ------
        ValueError
          If self.real <= 0.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = np.cosh(x)
        >>> x.real
        1.5430806348152437
        >>> x.dual
        array([1.17520119])
        """
        return DualNumber(np.cosh(self.real), self.dual*np.sinh(self.real))
    

    def tanh(self):
        """
        tanh(self)

        Taking tanh.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with tanh.

        Raises
        ------
        ValueError
          If self.real <= 0.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = np.tanh(x)
        >>> x.real
        0.7615941559557649
        >>> x.dual
        array([0.41997434])
        """
        return DualNumber(np.tanh(self.real), self.dual*1/(np.cosh(self.real)**2))


    def logistic(self):
        """
        logistic(self)

        Taking logistic.
         
        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : DualNumber
             A DualNumber object with logistic.
  
        Examples
        --------
        >>> x = DualNumber()
        >>> x = DualNumber.logistic(x)
        >>> x.real
        0.7310585786300049
        >>> x.dual
        array([0.19661193])
        """
        return DualNumber(np.exp(self.real)/(1 + np.exp(self.real)), self.dual*np.exp(-self.real)/(1+np.exp(-self.real))**2)




class ForwardMode():

    def __init__(self, *args):
        """
        __init__(self, *args)

        Initiate a ForwardMode object.
         
        Parameters
        ----------
        self : variable object
        *args : list, optional
             A list of functions that users want to get derivative and value.
         
        Examples
        --------
        >>> f = ForwardMode()

        Neither a list of functions is acceptable:

        >>> x = DualNumber(real = 1)
        >>> f = ForwardMode([x**2]) 
        """

        if len(args) > 0:
            self.f = args[0]
            self.number_of_funtions = len(self.f)
    
    def set_function(self, f):
        """
        set_function(self, f):

        Set the function that users want to get derivative and value.

        Parameters
        ----------
        self : variable object
        f : list
           A list of functions that users want to get derivative and value.
         
        Examples
        --------
        >>> x = DualNumber(real = 1)
        >>> f = ForwardMode()
        >>> f.set_function([x**2, np.exp(x)])
        """
        self.f = f
        self.number_of_funtions = len(self.f)
        
    def get_derivative(self):
        """
        get_derivative(self, f):

        Get the derivative/Jacobian matrix of the function.

        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : array
            Returns the derivative/Jacobian matrix of the function.
         
        Examples
        --------
        >>> x = DualNumber(real = 1)
        >>> f = ForwardMode()
        >>> f.set_function([((x**2)+3.5*x-20)/x, x])
        >>> f.get_derivative()
        array([[21.],
            [1.]])
        """
        self.derivative = np.array([self.f[0].dual])
        for i in range(1, self.number_of_funtions):
            self.derivative = np.r_[self.derivative, np.array([self.f[i].dual])]
        return self.derivative
    
    def get_function_value(self):
        """
        get_derivative(self, f):

        Get the value of the function.

        Parameters
        ----------
        self : variable object

        Returns
        -------
        output : array
            Returns the value of the function.
         
        Examples
        --------
        >>> x = DualNumber(real = 1)
        >>> f = ForwardMode()
        >>> f.set_function([((x**2)+3.5*x-20)/x, x])
        >>> f.get_function_value()
        array([-15.5,   1. ])
        """
        return np.array([f.real for f in self.f])
        