"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""
import numpy as np
import math
from ADforward import Variable

accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]

# Using chain rule to create variable class for all math and numpy operations

def log(x, base=math.e):
    """ If x is a Variable object instance, it will return a Variable object.
        With one argument, return Variable object with value as the natural logarithm of  value of x (to base e)
        and corresponding derivative calculated from chain rule.
        With two arguments, return Variable object with value as logarithm of value of x to the given base,
        calculated as log(x)/log(base)  and corresponding derivative calculated from chain rule.
        If x is other accepted data type, then this method is same as math.log(x,base)
    """
    if type(x) == Variable:
        return Variable(math.log(x.value, base), 1/math.log(base)*(1/x.value)*x.deriv)
    elif type(x) in accepted_data_types:
        return math.log(x, base)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def ln(x):
    """ same as log(x,e)
    """
    return log(x, math.e)


def log2(x):
    """
    If x is a Variable object instance, it will return a Variable object.
    Return Variable object with value base-2 logarithm of x and corresponding derivative calculated from chain rule.
    If x is iother accepted data type, then this method is same as math.log2(x)
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(math.log2(x.value), 1 / math.log(2) * (1 / x.value) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.log2(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def log10(x):
    """
    If x is a Variable object instance, it will return a Variable object with value base-10 logarithm of x and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.log10(x)
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(math.log10(x.value), 1 / math.log(10) * (1 / x.value) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.log10(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def log1p(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as natural logarithm of 1+x (base e) and corresponding derivative calculated from chain rule.
    The result is calculated in a way which is accurate for x near zero.
    If x is other accepted data type, then this method is same as math.log1p(x)
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(math.log1p(x.value), (1 / (x.value + 1)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.log1p(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def exp(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as e raised to the power x and corresponding derivative calculated from chain rule,
    where e = 2.71828... is the base of natural logarithms.
    If x is other accepted data type, then this method is same as math.exp(x)
    This is usually more accurate than math.e ** x or pow(math.e, x).
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(math.exp(x.value), (math.exp(x.value)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.exp(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def exp2(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as 2 raised to the power x and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as 2**x
    x should be Variable object instance or other accepted data type.
    """
    return 2 ** x

def expm1(x):
    """
    For small floats x, the subtraction in exp(x) - 1 can result in a significant loss of precision;
    the expm1() function provides a way to compute this quantity to full precision
    If x is a Variable object instance, it will return a Variable object with value as exp(x) - 1 under natural base and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.expm1(x)
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(math.expm1(x.value), math.exp(x.value) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.expm1(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


# Trigonometric functions


def sin(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as sine of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.sin(x)
    x should be Variable object instance or other accepted data type.
    """

    if type(x) == Variable:
        return Variable(np.sin(x.value), np.cos(x.value)*x.deriv)
    elif type(x) in accepted_data_types:
        return math.sin(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def cos(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as cosine of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.cos(x)
    x should be Variable object instance or other accepted data type.
    """
    if type(x) == Variable:
        return Variable(np.cos(x.value), -np.sin(x.value) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.cos(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def tan(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as tangent of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.tan(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.tan(x.value), (1/(math.cos(x.value))**2) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.tan(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def cot(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as cotangent of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.cot(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(1/math.tan(x.value), -(1/(math.sin(x.value))**2) * x.deriv)
    elif type(x) in accepted_data_types:
        return 1/math.tan(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def sec(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as secant of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.sec(x)
    x should be Variable object instance or other accepted data type
    """

    if type(x) == Variable:
        return Variable(1/math.cos(x.value), (1/math.cos(x.value)*math.tan(x.value)) * x.deriv)
    elif type(x) in accepted_data_types:
        return 1/math.cos(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def csc(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as cosecant of x value in radians and corresponding derivative calculated from chain rule
    If x is other accepted data type, then this method is same as math.csc(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(1/math.sin(x.value), -(1/math.sin(x.value)/math.tan(x.value)) * x.deriv)
    elif type(x) in accepted_data_types:
        return 1/math.sin(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def atan(x):
    """
    If x is a Variable object instance, it will return a Variable object  with value as arc tangent of x value, in radians and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.atan(x)
    The result value is between -pi/2 and pi/2.
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.atan(x.value), (1/(1+x.value**2)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.atan(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def acos(x):
    """
    If x is a Variable object instance, it will return a Variable object  with value as arc cosine of x, in radians and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.acos(x)
    The result value is between 0 and pi.
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.acos(x.value), -(1/math.sqrt(1-x.value**2)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.acos(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def asin(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as arc sine of x value, in radians and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.asin(x)
    The result value is between -pi/2 and pi/2.
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.asin(x.value), (1/math.sqrt(1-x.value**2)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.asin(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

# Hyperbolic functions

def acosh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the inverse hyperbolic cosine of x value and corresponding derivative calculated from chain rule.
    x should be Variable object instance or other accepted data type
    If x is other accepted data type, then this method is same as math.acosh(x)
    Inverse hyperbolic cosine domain is the closed interval [1, infinity)
    arcosh(x) = ln(x+sqrt(x^2-1))
    """
    if type(x) == Variable:
        if x.value == 1:
            raise ValueError("The inverse hyperbolic cosine non-differentiable at an input value of 1")
        elif x.value < 1:
            raise ValueError("The inverse hyperbolic cosine not defined at an input value smaller than 1")
        else:
            return Variable(math.acosh(x.value), (1/math.sqrt(x.value**2 - 1)) * x.deriv)
    elif type(x) in accepted_data_types:
        if x < 1:
            raise ValueError("The inverse hyperbolic cosine not defined at an input value smaller than 1")
        else:
            return math.acosh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def asinh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the inverse hyperbolic sine of x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.asinh(x)
    x should be Variable object instance or other accepted data type.
    Inverse hyperbolic sine domain is the closed interval (-infinity, infinity)
    arsinh(x) = ln(x+sqrt(x^2+1))
    """
    if type(x) == Variable:
        return Variable(math.asinh(x.value), (1 / math.sqrt(x.value ** 2 + 1)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.asinh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def atanh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the inverse hyperbolic tangent of x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.atanh(x)
    x should be Variable object instance or other accepted data type
    Inverse hyperbolic tan, domain is the closed interval [-1,1]
    artanh(x) = ln((1+x)/(1-x))/2
    """

    if type(x) == Variable:
        return Variable(math.atanh(x.value), (1 / (1-x.value ** 2)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.atanh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def cosh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the hyperbolic cosine of x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.cosh(x)
    x should be Variable object instance or other accepted data type
    """

    if type(x) == Variable:
        return Variable(math.cosh(x.value), (math.sinh(x.value)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.cosh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def sinh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the hyperbolic sine of x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.sinh(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.sinh(x.value), (math.cosh(x.value)) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.sinh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def tanh(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the hyperbolic tangent of x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.tanh(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.tanh(x.value), (1/math.cosh(x.value)**2) * x.deriv)
    elif type(x) in accepted_data_types:
        return math.tanh(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))


def sqrt(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the square root x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as math.sqrt(x)
    x should be Variable object instance or other accepted data type
    """
    if type(x) == Variable:
        return Variable(math.sqrt(x.value), (1/math.sqrt(x.value))/2 * x.deriv)
    elif type(x) in accepted_data_types:
        return math.sqrt(x)
    else:
        raise TypeError("Data type not understood: "+str(x)+": "+str(type(x)))

def logistic(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the logistic x value and corresponding derivative calculated from chain rule.
    If x is other accepted data type, then this method is same as 1/(1+math.exp(-x))
    x should be RVariable object instance or other accepted data type.
    """
    if type(x) == Variable:
        value = 1/(1+math.exp(-x.value))
        return Variable(value, 1/(1+math.exp(-x.value))*(1-1/(1+math.exp(-x.value)))*x.deriv)
    elif type(x) in accepted_data_types:
        return 1/(1+math.exp(-x))
    else:
        raise TypeError("Data type not understood: "+str(x))

def logit(x):
    """
    If x is a Variable object instance, it will return a Variable object with value as the logit x value and corresponding derivative calculated from chain rule.
    If x is accepted data type, then this method is same as ln(x/(1-x))
    x should be Variable object instance or other accepted data typ.
    """
    return ln(x/(1-x))

