# -*- coding: utf-8 -*-
"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""

from vector_autodiff import VectorAutoDiff
from ADforward import Variable
import inspect
import numpy as np

def newtons_method_root_finder(input_function, initial_guess=1, max_iter=25, epsilon=0.01, proximity=0.0001, verbose=False):
    """
    A function for finding a root of an equation of 1 variable using the VectorAutoDiff class object and methods. Given a f(x),
    this function employs Newton's Method to find a point x0 such that f(x0) = 0


    Parameters
    ----------
    input_function : callable function
        A lambda defined function of 1 variable e.g. lambda x1: x1**2 - 2*x1 - 4 
    
    initial_guess : int, float, optional
        The initial value at which to begin searching for a root to the equation provided as the input_function. For functions with
        multiple real valued roots, different initial_guess inputs can yield different results
    
    max_iter : int, optional
        Specifies the max number of iterations to compute in search of a root. The default is 25. The function will stop of the iteration
        count exceeds the max_iter argument
    
    epsilon : float, optional
        Specifies the minimum amount of change in the input variable required each iteration to continue to iterate. The default is 0.01.
        If the root finding algorithm's next iterative approximation of the root location is not at least epsilon different from the last,
        the function will end its search
        
    proximity : float, optional
        Specifies the proximity to 0 that f(x0) must achieve in order for the approximate x0 root to be reported by the function. The 
        default is 0.0001.
        
    verbose : bool, optional
        A parameter that can be set to True to toggle the function's print statements on which will provide screen updates each iteration
        as the algorithm progresses through Newton's Method. The default is False.

    Returns
    -------
    x0 : float
        Returns a float that is the approximate location where the input_function reaches a zero i.e. returns x0 such that f(x0) = 0.
        Root finder algorithm iterates until either the max_iter limit is reached or the estimated x0 changes by less than epsilon. If
        the resulting f(x0) is within a proximity of input parameter 'proximity' to zero, then the estimated x0 will be return to the 
        user. Otherwise, a string message will be returned indicating that no appropriate root was able to be found
    """
    
    # Perform data validation, check that the input_function is indeed a function
    if not callable(input_function):
        raise TypeError("input_function must be a callable function")
    
    # Instanciate variables to count the number of iterations and track exit conditions
    iterations=0;x_curr=initial_guess;abs_change=epsilon+1
    variable_used = inspect.getfullargspec(input_function)[0] # Extract the keyword argument(s) of the input function
    vars_used = len(variable_used) # Get the length of the function parameters list, should be of length 1 for a function of 1 variable
    # Perform data validation, check that the input_function is indeed a function of 1 input parameter
    if vars_used != 1:
        raise IndexError("Input function should be a function of 1 variable, instead got a function of "+str(vars_used))
    
    if type(verbose) != bool:
        raise("verbose must be specified as a bool")
        
        
    # Create a VectorAutoDiff class instance to compute the gradient of the function for each iteration, preserve the naming convention
    # used in the definition of input_function for user interpretability
    obj_function = VectorAutoDiff(variable_collection={variable_used[0]:Variable(initial_guess,1)})
    obj_function.add_eq(input_function) # Add this equation to the instance of the VectorAutoDiff object
    
    if verbose:
        print("Starting root finding search...") # Screen update inidicating the start of the root finding iterative process
    
    while iterations <= max_iter and abs_change >= epsilon:
        
        if verbose:
            print("\nIteration: "+str(iterations))
            print("Current "+variable_used[0]+": "+str(x_curr))
            print("Current f("+variable_used[0]+"): "+str(input_function(x_curr)))
        
        # Compute the derivative of f with respect of the input variable at the current coordinate root estimate
        x_curr_deriv = obj_function.compute_deriv(0, coordinate_vector=[x_curr], p_vector=[1])
        
        if verbose:
            print("Current df/d"+variable_used[0]+": "+str(x_curr_deriv))
        
        # Examine the magnitude of the current derivative and adjust accordingly to avoid unstable behavior
        if abs(x_curr_deriv)<0.0001 and abs(input_function(x_curr))>proximity:
            # If the current deriv is very small, then shift slightly until we find a new x that has a larger
            for i in range(25):
                x_curr = x_curr*1.01
                x_curr_deriv = obj_function.compute_deriv(0, coordinate_vector=[x_curr], p_vector=[1])
            iterations+=1 
        
        else:
            x_new = x_curr - input_function(x_curr)/x_curr_deriv
            abs_change = abs(x_new-x_curr) # Compute the absolute value of the change in x for this iteration
            x_curr = x_new # Update our current x with the new x just computed
            iterations+=1
            if x_curr in [np.inf, -np.inf]:
                return "No root found, estimate tends towards infinity, please try again with a different initial guess"

    
    if abs(input_function(x_curr))<proximity:
        return x_curr
    else:
        return "No root found, function value at approximate not near zero, please try again with a different initial guess or a higher max iteration allowance"


def newtons_method_root_finder_multi(input_function, initial_guess_domain = (0,1), max_iter=25, epsilon=0.01, proximity=0.0001, max_runs=10, root_sig_digits=4):

    """
    A function for finding potentially many roots of a single-variable input_function. Given a f(x) input_function, this function 
    employs Newton's Method to find a point x0 such that f(x0) = 0
    
    A function for finding potentially many roots of an equation of 1 variable using the VectorAutoDiff class object and methods. Given a f(x),
    input_function, this function employs Newton's Method to find a point x0 such that f(x0) = 0 iteratively many times over a user specified
    initial guess domain. 

    Parameters
    ----------
    input_function : callable function
        A lambda defined function of 1 variable e.g. lambda x1: x1**2 - 2*x1 - 4 
        
    initial_guess_domain : TYPE, optional
        The initial values at which to begin searching for a root to the equation provided as the input_function. For functions with
        multiple real valued roots, different initial_guess inputs can yield different results. Equally spaced initial guesses from 
        the initial_guess_domain, max_runs in total, are used to search for roots.
        
    max_iter : int, optional
        Specifies the max number of iterations to compute in search of a root. The default is 25. The function will stop of the iteration
        count exceeds the max_iter argument.
    
    epsilon : float, optional
        Specifies the minimum amount of change in the input variable required each iteration to continue to iterate. The default is 0.01.
        If the root finding algorithm's next iterative approximation of the root location is not at least epsilon different from the last,
        the function will end its search.
        
    proximity : float, optional
        Specifies the proximity to 0 that f(x0) must achieve in order for the approximate x0 root to be reported by the function. The 
        default is 0.0001.
        
    max_runs : int, optional
        Specifies the number of initial guesses to use and run through the newtons_method_root_finder algorithm in search of function roots. 
        The default is 10. If the number of roots expected is not found when running this function, try increasing the max_runs parameter to
        search over the initial_guess_domain more throughly.
        
    root_sig_digits : int, optional
        Specifies the number of significant digits in the equation roots found. This paramter is used when comparing the similarity of roots
        obtained by various internal runs of the newtons_method_root_finder algorithm. If a new initial guess run returns a root value that is
        too similar to one already found, the new estimated root will be discarded. A higher root_sig_digits may result in duplicate estimates
        of the same root.

    Returns
    -------
    roots_found : list
        Returns a list of root estimates found for the provided input_function using equally spaced n=max_runs initial guesses equally spaced
        along the initial_guess_domain. If the number of roots returned is less than expected, try expanding the initial_guess_domain and/or
        increasing the max_runs parameter.
    """
    # A function for finding multiple roots of an equation with potentially many root values
    roots_found = [] # Create a blank list to hold the roots found for this equation
    
    # Create a series of initial guesses evenly spaces in the interval specified by the user
    initial_guesses = np.linspace(initial_guess_domain[0],initial_guess_domain[1],num=max_iter) 
    
    # Loop through the initial_guesses and attempt to compute a new root initialized at each
    for initial_guess in initial_guesses:
        # Compute a new root for this equation using the input arguments
        new_root = newtons_method_root_finder(input_function=input_function, initial_guess=initial_guess, max_iter=max_iter, epsilon=epsilon, proximity=proximity, verbose=False)
        
        if type(new_root) != str:
            new_root=round(new_root, root_sig_digits) # Round to the designated level of precision 
            
            # If there are currently no roots found, then append this new root to the roots_found list
            if len(roots_found)==0:
                roots_found.append(new_root)
            
            # Otherwise, check to see if there is a root that is already in the roots_found list that is very similar
            else:
                # Check if there is a root already in the roots_found list that is very similar. Look for the min difference among all
                # current roots listed in teh roots_found list, if there is at least 1 that is the same, then do not add this root
                if min([abs(new_root-root) for root in roots_found]) > 0:
                    # If the new_root is sufficiently different from all others already located, then append it to the roots_found list
                    roots_found.append(new_root)
                    
    if len(roots_found)>0:    
        return roots_found
    else:
        return "No roots found! Please try again with a different initial_guess_domain and/or higher max_runs parameter"
        
    