"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""
import numpy as np
import math
from ADreverse import RVariable

accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]

# Power and logarithmic functions

def log(x, base=math.e):
    """ If x is a Variable object instance, it will return a RVariable object.
        With one argument, return RVariable object with value as the natural logarithm of  value of x (to base e)
        and corresponding (partial) derivative with respect to x itself
        With two arguments, return RVariable object with value as logarithm of value of x to the given base,
        calculated as log(x)/log(base)  and corresponding (partial) derivative with respect to x itself
        If x is int or float, then this method is same as math.log(x,base)
    """
    if type(x) == RVariable:
        value = math.log(x.value, base)
        partial_deriv = [(x, 1 / math.log(base) * (1 / x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.log(x, base)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))

def ln(x):
    """ same as log(x,e)
    """
    return log(x, math.e)

def log2(x):
    """
    If x is a Variable object instance, it will return a RVariable object.
    Return RVariable object with value base-2 logarithm of x and corresponding (partial) derivative with respect to x itself
    If x is int or float, then this method is same as math.log2(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.log2(x.value)
        partial_deriv = [(x, 1 / math.log(2) * (1 / x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.log2(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def log10(x):
    """
    If x is a RVariable object instance, it will return a Variable object with value base-10 logarithm of x
    corresponding (partial) derivative with respect to x itself.
    If x is int or float, then this method is same as math.log10(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.log10(x.value)
        partial_deriv = [(x, 1 / math.log(10) * (1 / x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.log10(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def log1p(x):
    """
    If x is a RVariable object instance, it will return a Variable object with value as natural logarithm of 1+x (base e)
    and corresponding (partial) derivative with respect to x itself
    The result is calculated in a way which is accurate for x near zero.
    If x is int or float, then this method is same as math.log1p(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.log1p(x.value)
        partial_deriv = [(x, (1 / (x.value + 1)))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.log1p(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def exp(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as e raised to the power x and corresponding (partial) derivative with respect to x itself,
    where e = 2.71828... is the base of natural logarithms.
    If x is int or float, then this method is same as math.exp(x)
    This is usually more accurate than math.e ** x or pow(math.e, x).
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.exp(x.value)
        partial_deriv = [(x, math.exp(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.exp(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def exp2(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as 2 raised to the power x and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as 2**x
    x should be RVariable object instance or int or float.
    """
    return 2 ** x


def expm1(x):
    """
    For small floats x, the subtraction in exp(x) - 1 can result in a significant loss of precision;
    the expm1() function provides a way to compute this quantity to full precision
    If x is a Variable object instance, it will return a Variable object with value as exp(x) - 1 under natural base and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.expm1(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.expm1(x.value)
        partial_deriv = [(x, math.exp(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.expm1(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


# Trigonometric functions


def sin(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as sine of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.sin(x)
    x should be RVariable object instance or int or float.
    """

    if type(x) == RVariable:
        value = math.sin(x.value)
        partial_deriv = [(x, math.cos(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.sin(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def cos(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as cosine of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.cos(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.cos(x.value)
        partial_deriv = [(x, -math.sin(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.cos(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def tan(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as tangent of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.tan(x)
    x should be RVariable object instance or int or float
    """
    if type(x) == RVariable:
        value = math.tan(x.value)
        partial_deriv = [(x, 1/math.cos(x.value)**2)]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.tan(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def cot(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as cotangent of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.cot(x)
    x should be RVariable object instance or int or float
    """
    if type(x) == RVariable:
        value = 1/math.tan(x.value)
        partial_deriv = [(x, -(1 / (math.sin(x.value)) ** 2))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = 1/math.tan(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def sec(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as secant of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.sec(x)
    x should be RVariable object instance or int or float
    """

    if type(x) == RVariable:
        value = 1 / math.cos(x.value)
        partial_deriv = [(x, (1 / math.cos(x.value) * math.tan(x.value)))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = 1/math.cos(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def csc(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as cosecant of x value in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.csc(x)
    x should be RVariable object instance or int or float
    """
    if type(x) == RVariable:
        value = 1 / math.sin(x.value)
        partial_deriv = [(x, -(1 / math.sin(x.value) / math.tan(x.value)))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = 1/math.sin(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def atan(x):
    """
    If x is a RVariable object instance, it will return a RVariable object  with value as arc tangent of x value, in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.atan(x)
    The result value is between -pi/2 and pi/2.
    x should be Variable object instance or int or float
    """
    if type(x) == RVariable:
        value = math.atan(x.value)
        partial_deriv = [(x, (1 / (1 + x.value ** 2)))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.atan(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def acos(x):
    """
    If x is a RVariable object instance, it will return a RVariable object  with value as arc cosine of x, in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.acos(x)
    The result value is between 0 and pi.
    x should be Variable object instance or int or float
    """
    if type(x) == RVariable:
        value = math.acos(x.value)
        partial_deriv = [(x, -(1 / math.sqrt(1 - x.value ** 2)))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.acos(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def asin(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as arc sine of x value, in radians and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.asin(x)
    The result value is between -pi/2 and pi/2.
    x should be RVariable object instance or int or float
    """
    if type(x) == RVariable:
        value = math.asin(x.value)
        partial_deriv = [(x, 1 / math.sqrt(1 - x.value ** 2))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.asin(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


# Hyperbolic functions

def acosh(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the inverse hyperbolic cosine of x value and corresponding (partial) derivative with respect to x itself,
    x should be RVariable object instance or int or float
    If x is int or float, then this method is same as math.acosh(x)
    Inverse hyperbolic cosine domain is the closed interval [1, infinity)
    arcosh(x) = ln(x+sqrt(x^2-1))
    """
    if type(x) == RVariable:
        if x.value == 1:
            raise ValueError("The inverse hyperbolic cosine non-differentiable at an input value of 1")
        elif x.value < 1:
            raise ValueError("The inverse hyperbolic cosine not defined at an input value smaller than 1")
        else:
            value = math.acosh(x.value)
            partial_deriv = [(x, 1 / math.sqrt(x.value ** 2 - 1))]
            variables = x.variables
            return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        if x < 1:
            raise ValueError("The inverse hyperbolic cosine not defined at an input value smaller than 1")
        else:
            value = math.acosh(x)
            return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def asinh(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the inverse hyperbolic sine of x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.asinh(x)
    x should be RVariable object instance or int or float.
    Inverse hyperbolic sine domain is the closed interval (-infinity, infinity)
    arsinh(x) = ln(x+sqrt(x^2+1))
    """
    if type(x) == RVariable:
        value = math.asinh(x.value)
        partial_deriv = [(x, 1 / math.sqrt(x.value ** 2 + 1))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.asinh(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def atanh(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the inverse hyperbolic tangent of x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.atanh(x)
    x should be Variable object instance or int or float.
    Inverse hyperbolic tan, domain is the closed interval [-1,1]
    artanh(x) = ln((1+x)/(1-x))/2
    """

    if type(x) == RVariable:
        value = math.atanh(x.value)
        partial_deriv = [(x, 1 / (1 - x.value ** 2))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.atanh(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def cosh(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the hyperbolic cosine of x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.cosh(x)
    x should be RVariable object instance or int or float.
    """

    if type(x) == RVariable:
        value = math.cosh(x.value)
        partial_deriv = [(x, math.sinh(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.cosh(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def sinh(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the hyperbolic sine of x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.sinh(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.sinh(x.value)
        partial_deriv = [(x, math.cosh(x.value))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.sinh(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def tanh(x):
    """
    If x is a RVariable object instance, it will return a R Variable object with value as the hyperbolic tangent of x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.tanh(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.tanh(x.value)
        partial_deriv = [(x, (1 / math.cosh(x.value) ** 2))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.tanh(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))


def sqrt(x):
    """
    If x is a RVariable object instance, it will return a Variable object with value as the square root x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as math.sqrt(x)
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = math.sqrt(x.value)
        partial_deriv = [(x, (1 / math.sqrt(x.value)) / 2)]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        value = math.sqrt(x)
        return value
    else:
        raise TypeError("Data type not understood: " + str(x))

def logistic(x):
    """
    If x is a RVariable object instance, it will return a RVariable object with value as the logistic x value and corresponding (partial) derivative with respect to x itself,
    If x is int or float, then this method is same as 1/(1+math.exp(-x))
    x should be RVariable object instance or int or float.
    """
    if type(x) == RVariable:
        value = 1/(1+math.exp(-x.value))
        partial_deriv = [(x, 1/(1+math.exp(-x.value))*(1-1/(1+math.exp(-x.value))))]
        variables = x.variables
        return RVariable(value, partial_deriv=partial_deriv, variables=variables)
    elif type(x) in accepted_data_types:
        return 1/(1+math.exp(-x))
    else:
        raise TypeError("Data type not understood: "+str(x))

def logit(x):
    """
    If x is a Variable object instance, it will return a RVariable object with value as the logit x value and corresponding derivative calculated from chain rule.
    If x is int or float, then this method is same as ln(x/(1-x))
    x should be RVariable object instance or int or float.
    """
    return ln(x/(1-x))
