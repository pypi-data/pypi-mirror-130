# -*- coding: utf-8 -*-
"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""

import numpy as np        

class Variable:
    """
    A class used to represent the various intermediate variables in the computation of forward mode auto-differentiation
    
    Attributes
    ----------
    value : float
        functional value of this intermediate variable, used in the primal trace evaluation
    
    deriv : float
        derivative value of this intermediate variable, used in the tangent trace evaluation
        
    """
    def __init__(self, value, deriv=1):
        """
        Constructs all the necessary attributes of an intermediate variable instance for forward mode auto-differentiation
        
        Parameters
        ----------
        value : float
            Functional value of this intermediate variable, used in the primal trace evaluation
            for assignment intermediate variables, value will be equal to the value of the coordinate passed in 
        
        deriv : float
            derivative value of this intermediate variable with respect to the input variable, used in the tangent trace evaluation
            by default, this is set to a value of 1 which will be the case when instanciating an intermediate variable and seeking
            to compute the derivative of a function with respect to a 1 unit change in the input x variable
                   
        """
        self.value = value
        self.deriv = deriv
        self.accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]
    
    # Overload dunder methods to define elementary operations
    def __add__(self, other):
        """Dunder method overload to handle the addition of Variable object instances with one another and with floats or ints"""
        if type(other)==Variable:
            # Check if the other argument passed in is of the Variable class
            output=Variable(self.value + other.value, self.deriv + other.deriv)
        elif type(other) in self.accepted_data_types:
            # Check if the other variable passed in is a float or an int, in which can be used in our function
            output=Variable(self.value + other, self.deriv)
        else:
            # Otherwise if the data type is not recognized, then return an error to the user indicating as much
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))
    
        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
        
    def __radd__(self, other):
        """
        Dunder method overload to handle the addition of Variable object instances with one another and with floats or ints.
        The addition of scalars is communitive, which allows for the the add dunder method to be used to implement the reverse 
        order addition elementary operation as well e.g. 5 + x can be implemented via x + 5
        """
        return self.__add__(other)
    
    
    def __mul__(self, other):
        """Dunder method overload to handle the multiplication of Variable object instances with one another and with floats or ints e.g. x1 * 5"""
        if type(other)==Variable:
            # Check if the other argument passed in is of the Variable class
            output=Variable(self.value * other.value, self.deriv*other.value + self.value * other.deriv)
        
        # Check if the other variable passed in is a float or an int, in which can be used in our function
        elif type(other) in self.accepted_data_types:
            output=Variable(self.value*other, self.deriv*other)
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))
        
        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
    
    def __rmul__(self, other):
        """Dunder method overload to handle the multiplication of Variable object instances with one another and with floats or ints
           Since multiplication of scalars is communitive, we can call the multiplication dunder method to implement the reverse order 
           multiplication elementary operation as well e.g. 5*x or x2*x1
        """
        return self*(other)
    
    def __neg__(self):
        """Overload the unary dunder method for negation e.g. (-x)"""
        return self * (-1)
    
    def __pos__(self):
        """Overload the unary dunder method for the positive indicator e.g. (+x)"""
        return self
    
    def __sub__(self, other):
        """Overload the dunder method for subtraction e.g. x-5"""
        if type(other) == Variable or type(other) in self.accepted_data_types:
            # Use the dunder method for negation and addition as defined above to handle subtraction
            return self + (-other)
        
        else:
            # If data type not understood, raise an error to the user and display the non-conforming part
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))
    
    def __rsub__(self, other):
        """Overload the dunder method for reverse order subtraction e.g. (5-x), use the negation and addition dunder methods from above to implement"""
        return -self + other
    
    def __truediv__(self, other):
        """Overload the dunder method for division denoted by / e.g. x/5"""
        if type(other)==Variable:
            # Check if the other argument passed in is of the Variable class
            output=Variable(self.value / other.value, (self.deriv * other.value - self.value * other.deriv)/(other.value**2))

        # Check if the other variable passed in is a float or an int
        elif type(other) in self.accepted_data_types:
            output=Variable(self.value/other, self.deriv/other)
            
        else:
            raise TypeError("Data type not understood: "+str(other))

        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
    
    def __rtruediv__(self, other):
        """Overload the dunder method for reverse order division denoted by / e.g. 5/x"""
        # Other cannot be a Variable type since in that case it would have already been handled by the __trudiv__ method            
        
        # Check if the other variable passed in is a float or an int
        if type(other) in self.accepted_data_types:
            output=Variable(other/self.value, ((-1)*other/(self.value)**2)*self.deriv)
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
        
    def __pow__(self, other):
        """Overload the dunder method for exponentiation with an intermediate variable as the base e.g. x**5"""
        if type(other)==Variable:
            # Check if the other argument passed in is of the Variable class
            output=Variable(self.value**other.value, (self.value**other.value)*(other.deriv * np.log(self.value) + (other.value * self.deriv)/self.value))
            
        # Check if the other variable passed in is a float or an int
        elif type(other) in self.accepted_data_types:
            output=Variable(self.value**other, (other*self.value**(other-1))*self.deriv)
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
    
    def __rpow__(self, other):
        """Overload the dunder method for reverse order exponentiation where an intermediate variable are the exponents e.g. 5**x"""
        # Other cannot be a Variable type since in that case it would have already been handled by the __pow__ method            
                    
        # Check if the other variable passed in is a float or an int
        if type(other) in self.accepted_data_types:
            output=Variable(other**self.value, self.deriv * other**self.value * np.log(other))
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))
    
        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return output
            
    def __abs__(self):
        """Overload the dunder method for handling absolute value evaluation e.g. |x|"""
        if self.value>0:
            # If the value at which we evaluate the function is positive, computation can be done
            return Variable(self.value, self.deriv)
        elif self.value<0:
            # If the value at which we evaluate the function is negative, computation can be done
            return Variable(-self.value, -self.deriv)
        else:
            # Otherwise, if the value at which we evaluate the function is 0, raise an error since the absolute value function is non-differentiable
            raise ValueError("The absolute value function non-differentiable at an input value of 0")

    def __eq__(self,other):
        """Overload the dunder method for the equals comparison == """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value == other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value == other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

    def __ne__(self, other):
        """Overload the dunder method for the not equal comparison != """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value != other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value != other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

    def __lt__(self, other):
        """Overload the dunder method for the less than comparison < """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value < other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value < other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))
        
    def __le__(self, other):
        """Overload the dunder method for the less than or equal comparison <= """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value <= other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value <= other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

    def __gt__(self, other):
        """Overload the dunder method for the greater than comparison > """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value > other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value > other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

    def __ge__(self, other):
        """Overload the dunder method for the greater than or equal comparison >= """
        if type(other) == Variable:
            # If both of the variable type, compare both the value attributes for assessing equality
            return self.value >= other.value
        
        elif type(other) in self.accepted_data_types:
            # If other is an int or float, compare the value of this object to that
            return self.value >= other
        
        else:
            raise TypeError("Data type not understood: "+str(other)+": "+str(type(other)))

    def __bool__(self):
        """Overload the dunder method for the bool method e.g. if x: to check if non-empty"""
        if self.value != None and self.deriv != None:
            return True
        else:
            return False

    def __repr__(self):
        """String representation of the Variable class for development"""
        return "Value: "+str(self.value)+"  Derivative: "+str(self.deriv)

    def __str__(self):
        """String representation of the Variable class"""
        return "Value: "+str(round(self.value,4))+"  Derivative: "+str(round(self.deriv,4))

 

