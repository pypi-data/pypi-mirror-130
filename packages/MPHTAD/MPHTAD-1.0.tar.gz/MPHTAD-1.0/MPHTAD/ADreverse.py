"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""
import numpy as np
import math


class RVariable:
    """
        A class used to represent the various intermediate variables in the computation of reverse mode auto-differentiation

        Attributes
        ----------
        value : float
            functional value of this intermediate variable

        partial_deriv : list or tuple
            If the variable has been applied some operation on, then it comes from either one or two Rvariables object,
            the partial_deriv contains tuple(s) of the one or two subvariables and the corresponding partial derivative
            If the variable is the input, then the partial_deriv is "empty" (empty tuple)

        name: str
            name of the variable or function, the default value is None

        variables: list
            If the variable has been applied some operation on, then variables contains all input variable of this expression
            If the variable is the input, then variables is itself

        accepted_data_types: list
            data type other than RVariable that can work with RVariable

    """

    def __init__(self, value, partial_deriv=(), name=None, variables=None):
        self.name = name
        self.value = value
        self.partial_deriv = partial_deriv  # partial derivative wrt each child
        self.setvariables(variables)
        self.accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]

    def set_name(self, name):
        self.name = name

    def setvariables(self, variables):
        if variables is not None:
            self.variables = []
            for var in variables:
                if var not in self.variables:
                    self.variables.append(var)
        else:
            self.variables = [self]

    # Overload dunder methods to define elementary operations
    def __add__(self, other):
        """Dunder method overload to handle the addition of RVariable object instances with one another and with other accepted data types
        If other is RVariable, then the returned RVariable with partial derivative wrt both self and other and variables contained in both self and other.
        If other is other accepted data type, then the returned RVariable have partial derivative wrt only self and variables contained in self"""
        if type(other) == RVariable:
            # Check if the other argument passed in is of the RVariable class
            value = self.value + other.value
            # partial derivative wrt self is 1, partial derivative wrt other is 1
            partial_deriv = [(self, 1), (other, 1)]
            variables = self.variables + other.variables
        elif type(other) in self.accepted_data_types:
            # Check if the other variable passed in is an accepted data type, in which can be used in our function
            value = self.value + other
            partial_deriv = [(self, 1)]
            variables = self.variables
        else:
            # Otherwise if the data type is not recognized, then return an error to the user indicating as much
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff RVariable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __radd__(self, other):
        """
        Dunder method overload to handle the addition of RVariable object instances with one another and with other accepted data types.
        The addition of scalars is communitive, which allows for the the add dunder method to be used to implement the reverse
        order addition elementary operation as well e.g. 5 + x can be implemented via x + 5
        """
        return self.__add__(other)

    def __mul__(self, other):
        """Dunder method overload to handle the multiplication of RVariable object instances with one another and with
        e.g. x1 * 5 """
        if type(other) == RVariable:
            # Check if the other argument passed in is of the RVariable class
            value = self.value * other.value
            # the partial derivative wrt self is other.value, the partial derivative wrt other is self.value
            partial_deriv = [(self, other.value), (other, self.value)]
            variables = self.variables + other.variables

            # Check if the other variable passed in is an accepted data type, in which can be used in our function
        elif type(other) in self.accepted_data_types:
            value = self.value * other
            # the local derivative wrt self is other.value, the local derivative wrt other is self.value
            partial_deriv = [(self, other)]
            variables = self.variables
        else:
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff variable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __rmul__(self, other):
        """Dunder method overload to handle the multiplication of RVariable object instances with one another and with other accepted data types
           Since multiplication of scalars is communitive, we can call the multiplication dunder method to implement the reverse order
           multiplication elementary operation as well e.g. 5*x or x2*x1
        """
        return self * (other)

    def __neg__(self):
        """Overload the unary dunder method for negation e.g. (-x)"""
        return self * (-1)

    def __pos__(self):
        """Overload the unary dunder method for the positive indicator e.g. (+x)"""
        return RVariable(self.value, partial_deriv=[(self, 1)], variables=[self])

    def __sub__(self, other):
        """Overload the dunder method for subtraction e.g. x-5"""
        if type(other) == RVariable or type(other) in self.accepted_data_types:
            # Use the dunder method for negation and addition as defined above to handle subtraction
            return self + (-other)
        else:
            # If data type not understood, raise an error to the user and display the non-conforming part
            raise TypeError("Data type not understood: " + str(other))

    def __rsub__(self, other):
        """Overload the dunder method for reverse order subtraction e.g. (5-x), use the negation and addition dunder methods from above to implement"""
        return -self + other

    def __truediv__(self, other):
        """Overload the dunder method for division denoted by / e.g. x/5"""
        if type(other) == RVariable:
            # Check if the other argument passed in is of the RVariable class
            value = self.value / other.value
            # the partial derivative wrt self is other.value, the partial derivative wrt other is self.value
            partial_deriv = [(self, 1 / other.value), (other, -self.value / (other.value ** 2))]
            variables = self.variables + other.variables

        # Check if the other variable passed in is an accepted data type
        elif type(other) in self.accepted_data_types:
            value = self.value / other
            # the local derivative wrt self is other.value, the local derivative wrt other is self.value
            partial_deriv = [(self, 1 / other)]
            variables = self.variables
        else:
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff RVariable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __rtruediv__(self, other):
        """Overload the dunder method for reverse order division denoted by / e.g. 5/x"""
        # Other cannot be a RVariable type since in that case it would have already been handled by the __trudiv__ method

        # Check if the other variable passed in is an accepted data type
        if type(other) in self.accepted_data_types:
            value = other / self.value
            # the partial derivative wrt self is -other/(self.value**2)
            partial_deriv = [(self, -other / (self.value ** 2))]
            variables = self.variables
        else:
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff RVariable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __pow__(self, other):
        """Overload the dunder method for exponentiation with an intermediate variable as the base e.g. x**5"""
        if type(other) == RVariable:
            # Check if the other argument passed in is of the RVariable class
            value = self.value ** other.value
            partial_deriv = [(self, other.value * self.value ** (other.value - 1)),
                             (other, self.value ** other.value * math.log(self.value))]
            variables = self.variables + other.variables
        # Check if the other variable passed in is an accepted data type
        elif type(other) in self.accepted_data_types:
            value = self.value ** other
            partial_deriv = [(self, other * self.value ** (other - 1))]
            variables = self.variables
        else:
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff RVariable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __rpow__(self, other):
        """Overload the dunder method for reverse order exponentiation where an intermediate variable are the exponents e.g. 5**x"""
        # Other cannot be a RVariable type since in that case it would have already been handled by the __pow__ method

        # Check if the other variable passed in is an accepted data type
        if type(other) in self.accepted_data_types:
            value = other ** self.value
            partial_deriv = [(self, other ** self.value * math.log(other))]
            variables = self.variables
        else:
            raise TypeError("Data type not understood: " + str(other))

        # Return a new instance of the Auto Diff RVariable class that combines the 2 inputs
        return RVariable(value, partial_deriv, variables=variables)

    def __abs__(self):
        """Overload the dunder method for handling absolute value evaluation e.g. |x|"""
        if self.value > 0:
            # If the value at which we evaluate the function is positive, computation can be done
            value = self.value
            partial_deriv = [(self, 1)]
            return RVariable(value, partial_deriv, variables=self.variables)
        elif self.value < 0:
            # If the value at which we evaluate the function is negative, computation can be done
            value = -self.value
            partial_deriv = [(self, -1)]
            return RVariable(value, partial_deriv, variables=self.variables)
        else:
            # Otherwise, if the value at which we evaluate the function is 0, raise an error since the absolute value function is non-differentiable
            raise ValueError("The absolute value function non-differentiable at an input value of 0")


    def __lt__(self, other):
        """Overload the dunder method for the less than comparison < """
        if type(other) == RVariable:
            # If both of the RVariable type, compare both the value attributes for assessing equality
            return self.value < other.value

        elif type(other) in self.accepted_data_types:
            # If other is an accepted data type, compare the value of this object to that
            return self.value < other

        else:
            raise TypeError("Data type not understood: " + str(other))

    def __le__(self, other):
        """Overload the dunder method for the less than or equal comparison <= """
        if type(other) == RVariable:
            # If both of the RVariable type, compare both the value attributes for assessing equality
            return self.value <= other.value

        elif type(other) in self.accepted_data_types:
            # If other is an accepted data type, compare the value of this object to that
            return self.value <= other

        else:
            raise TypeError("Data type not understood: " + str(other))

    def __gt__(self, other):
        """Overload the dunder method for the greater than comparison > """
        if type(other) == RVariable:
            # If both of the RVariable type, compare both the value attributes for assessing equality
            return self.value > other.value

        elif type(other) in self.accepted_data_types:
            # If other is an accepted data type, compare the value of this object to that
            return self.value > other

        else:
            raise TypeError("Data type not understood: " + str(other))

    def __ge__(self, other):
        """Overload the dunder method for the greater than or equal comparison >= """
        if type(other) == RVariable:
            # If both of the RVariable type, compare both the value attributes for assessing equality
            return self.value >= other.value

        elif type(other) in self.accepted_data_types:
            # If other is an accepted data type, compare the value of this object to that
            return self.value >= other

        else:
            raise TypeError("Data type not understood: " + str(other))

    def __bool__(self):
        """Overload the dunder method for the bool method e.g. if x: to check if non-empty"""
        if self.value != None and self.partial_deriv != None:
            return True
        else:
            return False

    def __repr__(self):
        """String representation of the RVariable class for development"""
        if self.name is not None:
            return "Value: " + str(self.value) + " Partial Derivatives: " + str(self.partial_deriv) \
                   + " Name: " + self.name
        else:
            return "Value: " + str(self.value) + " Partial Derivatives: " + str(self.partial_deriv)

    def __str__(self):
        """String representation of the RVariable class"""
        partial_dev = []
        for var in self.partial_deriv:
            partial_dev.append(round(var[1], 5))
        return "Value: " + str(round(self.value, 4)) + "  Derivative: " + str(partial_dev)

    def get_gradients_dict(self):
        """ Compute the partial derivatives of the function with respect to its variables."""
        gradients = {}

        def compute_gradients(variable, path_value):
            for child_variable, partial_gradient in variable.partial_deriv:
                # chain rule
                value_of_path_to_child = path_value * partial_gradient

                if child_variable in gradients:
                    gradients[child_variable] += value_of_path_to_child
                else:
                    gradients[child_variable] = value_of_path_to_child
                # recurse through graph:
                compute_gradients(child_variable, value_of_path_to_child)

        compute_gradients(self, path_value=1)
        if gradients == {}:
            return {self: 1}
        return gradients

    def get_gradients(self):
        """ Compute the gradient of the function"""
        gradients_dict = self.get_gradients_dict()
        grad_name, grad = [], []
        for var in self.variables:
            if var.partial_deriv == ():
                grad_name.append(var.name)
                grad.append(gradients_dict[var])
        return grad_name, grad


class Rvector:
    """
           A class used to represent the vector function in reverse mode

           Attributes
           ----------
           equations : list
               list of function components in the vector valued function

           variables : list
               variables that can be taken partial derivatives
       """

    def __init__(self, equations, variables=None, equation_names=None):
        """
           Constructs all the necessary attributes of an intermediate variable instance for forward mode auto-differentiation

           Parameters
           ----------
           equations : list
                list of function components in the vector valued function

           variables : list
               If the user give the order of variables when initializing the Rvector object, the column of the jacobian
               matrix/gradient will follow this order. For each variable, if it doesn't have name, it will be given name
               as xi with the order it is evaluated in the expression.
               If not, the order of variables will be the same as they are evaluated in the expression

           equation_names: list
               If the user give the order of equations when initializing the Rvector object, the row of the jacobian
               matrix/gradient will follow this order. For each equation, if it doesn't have name, it will be given name
               as fi with the order it is evaluated in the expression.
               If not, the order of equations will be the same as they are evaluated in the expression

        """
        if type(equations) == RVariable:
            self.equations = [equations]
        elif type(equations) == list:
            self.equations = equations
        else:
            raise TypeError("equation_names should either be list or Rvariable")

        if type(variables) == RVariable or type(variables) == list or variables is None:
            self.variables = self.set_variables(variables)
        else:
            raise TypeError("variables should either be list or Rvariable")

        if type(equation_names) == str:
            equation_names = [equation_names]
            self.set_equation_names(equation_names)
        elif type(equation_names) == list or equation_names is None:
            self.set_equation_names(equation_names)
        else:
            raise TypeError("equation_names should either be list or string")

    def set_equation_names(self, equation_names):
        """If the equation_names is not None, each equation will be named with the name in equation_names.
           If not, equation(s) will be names from f1 to fn with n as the number of equations"""
        self.equation_names = []
        if equation_names is not None:
            if len(equation_names) != len(self.equations):
                raise ValueError("equation_names should have equal length with equations")
            for i, name in enumerate(equation_names):
                self.equations[i].set_name(name)
        else:
            for i, eq in enumerate(self.equations):
                eq.set_name(f"f{i}")

    def set_variables(self, variables):
        """Set equation variables and the column of the Jacobian matrix / gradient will follow this order."""
        i = 1
        if variables is not None:
            for var in variables:
                if var.name is None:
                    var.set_name(f"x{i}")
                    i += 1
        else:
            variables = []
            if type(self.equations) == RVariable:
                for var in self.equations.variables:
                    if var.name is None:
                        var.set_name(f"x{i}")
                        i += 1
                    variables.append(var)
            else:
                for eq in self.equations:
                    for var in eq.variables:
                        if var not in variables:
                            if var.name is None:
                                var.set_name(f"x{i}")
                                i += 1
                            variables.append(var)
        return variables

    def get_jacobian(self):
        """if the function is vector valued, then return the jacobian;
           note: if the function is scalar valued, then the returned value is in two dimension"""
        jacobian = []
        for eq in self.equations:
            grad_dict = eq.get_gradients_dict()
            grad = []
            for var in self.variables:
                if var not in grad_dict:
                    grad.append(0)
                else:
                    grad.append(grad_dict[var])
            jacobian.append(grad)
        return np.array(jacobian)

    def get_gradient(self):
        """if the function is scalar valued, then return the gradient
            otherwise, raise keyvalue error"""
        if len(self.equations) != 1:
            raise ValueError("The input function is vector valued, expect scalar function")
        grad = []
        grad_dict = self.equations[0].get_gradients_dict()
        for var in self.variables:
            grad.append(grad_dict[var])
        return np.array(grad)

    def get_variable_names(self):
        """Return the name of variables. The columns in Jacobian matrix will also follow this order.
        """
        var_names = []
        for var in self.variables:
            var_names.append(var.name)
        return var_names

    def get_equation_names(self):
        """Return the name of function component. The rows in Jacobian matrix will also follow this order
        """
        names = []
        for eq in self.equations:
            names.append(eq.name)
        return names

    def get_partial_derivative(self, variable):
        """Return the partial derivative of a input variable. The returned value should be a numpy array.
        If the input value is not valid or not in our function, if will raise TypeError or KeyError.
        """
        jacobian = self.get_jacobian()
        if type(variable) == RVariable:
            if variable not in self.variables:
                raise KeyError("The input variable is not a variable in the function")
            else:
                for i in range(len(self.variables)):
                    if variable == self.variables[i]:
                        return jacobian[:,i].reshape(-1,1)
        elif type(variable) == str:
            variables_name = self.get_variable_names()
            if variable not in variables_name:
                raise KeyError("The input variable is not a variable in the function")
            else:
                for i in range(len(variables_name)):
                    if variable == variables_name[i]:
                        return jacobian[:,i].reshape(-1,1)
        else:
            raise TypeError("The input variable should be Rvariable object or str")

