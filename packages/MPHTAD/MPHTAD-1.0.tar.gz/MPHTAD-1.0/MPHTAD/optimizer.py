# -*- coding: utf-8 -*-
"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""

from vector_autodiff import VectorAutoDiff
from ADforward import Variable
import inspect
import numpy as np

def gradient_optimizer(input_function, initial_vector=[], learning_rate = 0.05, max_iter=25, proximity=0.0001, minimize=True, verbose=False):
        
    """
    A function used to find the argmin/max and min/max of a multivariable function using the technique of gradient decent/ascent
    This function inherits the Variable and VectorAutoDiff classes and uses them to iterively to calculate the gradient of a fucntion
    and move in the direction of that gradient in order to find the miniumum or maximum of the multivariable function.
    
    Parameters
    ----------
    input_function: lambda function
        The input_function of potentially many variables for which the optimizer will search for an optimized min/max using gradient
        descent/ascent. The input_function should be specified as a lambda function e.g. input_function = lambda x1 x2: x1**2 + x2*3
    
    initial_vector : list, tuple, nparray
        A vector specifying the initial values of the parameters of the input_function which will serve as a starting point for the 
        iterative gradient optimization algorithm to search for a function min/max.
        
    learning_rate : float
        A float indicating the learning rate. This parameter controls the stepsize of the iterative gradient descent/ascent algorithm.
        The larger the learning_rate, the faster the algorithm will converge toward the min/max, but may risk overshooting its objective.
        A smaller learning_rate will take more iterations to reach convergence but is likely to result in a closer approximation
    
    max_iter : int, optional
        The max number of iterations this function will run in search of the optimized min/max. The default is 25.
    
    proximity : float, optional
        Specifies an exit condition that will end the iterative search process if after a subsequent step, the value of the objective
        function does not change by more than this amount. In otherwords, in search of a min/max, if the next iterative set of input
        parameters does not yield a change of at least "proximity", then the algorithm will stop. The default is 0.0001.
    
    minimize : bool, optional
        A True/False boolean value indicating whether the gradient_optimizer function will search for a min/max. The default is True and 
        therefore this function will by default perform gradient descent and search for an argmin and function min.
    
    verbose : bool, optional
        Specifies if the gradient_optimizer function will print out screen updates as it iterates. The default is False.
 
    proximity : int, float
        A float or possibly an integer that determine the criteria for how close your function needs tro be to 0 in order for it to be 
        considered a root. After the function has finished the while loop is evaluates the lambda function at the current value of 
        x and if the absolut value of the function is not less than the proximity than it is not considered a root. 0.0001 is the default
        value for this.
        
    Returns
    -------
    x_curr : float
        Returns the approximate argmin/argmax of the input_function found using iterative gradient descent/ascent. I.e. vector of input
        parameters that achieves the min/max of the input_function.
    
    function_value_new : float
        Returns the approximate min/max of the function found using iterative gradient descent/ascent. I.e. the approximate min/max value
        of the input_function.
    """
    # Data validation to check that the input_function is indeed a callable function
    accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]
    if not callable(input_function):
        raise TypeError("input_function must be a callable function")
    
    #Convert any acceptable data type to a numpy array
    if type(initial_vector) in [list, tuple]:
        x_curr=np.array(initial_vector)
    elif type(initial_vector) == np.ndarray:
        x_curr=initial_vector.copy()
    else:
        raise TypeError("initial_guess data type note understood. Expected list, tuple or np.ndarray, got "+str(type(initial_vector)))
            
    # Check that the number of input variables is equal in dimension to the initial_vector specified
    variable_used = inspect.getfullargspec(input_function)[0]
    if len(variable_used) != len(initial_vector):
        raise IndexError("initial_vector vector ("+str(len(initial_vector))+") length does not match variable count ("+str(len(variable_used))+") in the input_function")
    
    if type(verbose) != bool:
        raise("verbose must be specified as a bool")
        
    if type(learning_rate) not in accepted_data_types:
        raise TypeError("learning_rate type not understood, expected a float or int, got "+str(type(learning_rate)))
    
    # Create a named collection of Variable instances using the variables used in the input_function definition
    var_collection = {var:Variable(val,1) for var, val in zip(variable_used, initial_vector)}    
    obj_function = VectorAutoDiff(variable_collection=var_collection, equation_list=[input_function])
    
    iterations=0;function_value_prev = obj_function.compute_value(0) # Compute the value of the function using the initial guesss
    abs_change = proximity + 1 # Set the initial abs_change above that of the proximity so that we can iterate
    
    while iterations <= max_iter and abs_change >= proximity:
        obj_func_gradient = obj_function.compute_gradient(0, coordinate_vector=x_curr)
        
        if verbose:
            print("\nIteration: "+str(iterations))
            print("Function Value Start: "+str(function_value_prev))
            print("obj_func_gradient: "+str(obj_func_gradient))
            print("Learning Rate: "+str(learning_rate))
            print("x_curr: "+str(x_curr))      

        if minimize == True:
            # If gradient_optimizer set to minimize, perform gradient descent
            x_curr = x_curr - learning_rate*obj_func_gradient
        else:
            # If gradient_optimizer set to maximize, perform gradient ascent
            x_curr = x_curr + learning_rate*obj_func_gradient
        
        function_value_new = obj_function.compute_value(0, coordinate_vector=x_curr) # Compute the new function value
        abs_change = abs(function_value_new - function_value_prev) # Compute the absolute value change in f(x1, x2, ...)
        function_value_prev = function_value_new # Update the prev function value with the new one computed this iteration
        iterations+=1 # Incriment up our iteration counter
        
    return x_curr, function_value_new

