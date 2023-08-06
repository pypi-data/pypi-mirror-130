# -*- coding: utf-8 -*-
"""
AC 207 Final Project - Jeffrey Mayolo, Manu Penenory, Eric Helmold, Ziye Tao
Last updated 12 11 2021
"""

from ADforward import Variable
import numpy as np
import inspect

class VectorAutoDiff:
    def __init__(self, variable_collection = None, *, coordinate_vector = None, p_vector = None, equation_list = None):
        """
        A class used to represent a vector valued equation of one more more input variables that maps inputs from R^m to outputs in R^n. There are 2 internal
        data structures that must be created for any VectorAutoDiff instance. First, the variable dictionary (var_dict) which holds the names and associated
        Variable class instance objects of each input variable. Second, the equation list (equation_list), which holds a series of lambda defined functions
        of variables contained in the var_dict
        
        Parameters
        ----------
        variable_collection : list, np.ndarray, tuple or dict, optional
            An input list, numpy vector, or tuple containing instances of the Variable class. Variables will be sequentually assigned names x1, x2, ..., xp
            If a dict is specified, the variable names encoded in the the variable dictionary (var_dict) will be named according to the key names provided
            in the variable_collection passed in. Values in the input variable_collection dict should be instances of the Variable class. Note, all variables
            used in equations must be contained in the var_dict and must therefore be specified at instanciation through the variable_collection input
        
        coordinate_vector : list, np.ndarray, tuple, optional
            An alternative way to create an instance of the VectorAutoDiff, requires a p_vector to also be specifies. Passing in a coordinate_vector will 
            specify a series of input coordinate variable values to variables that will be sequentually assigned names x1, x2, ..., xp
            
        p_vector : list, np.ndarray, tuple, optional
            An alternative way to create an instance of the VectorAutoDiff, requires a coordinate_vector to also be specifies. Passing in a p_vector will 
            specify a series of input coordinate variable p-vector elements to variables that will be sequentually assigned names x1, x2, ..., xp
            
        equation_list : list, np.ndarray, tuple, optional
            A list of lambda defined functions representing each equation's computational formulation of input variables with functions and constants
            Each equation must have keyword arguments (e.g. x1, x1) that are a subset of the variables contained in the var_dict. See the add_eq()
            for more details about adding equations after instanciation. 
        """
        if variable_collection is not None:
            if type(variable_collection) in [list, np.ndarray, tuple]:
                self.var_dict = dict() # Create a blank dict to hold the variable names and objects
                # If provided a list or numpy array or tuple, then create a series of variables x1, x2, ... , xp to represent the inputs
                for i, var in enumerate(variable_collection):
                    if type(var) != Variable:
                        raise TypeError(str(var)+": Not an instance of the Variable class, all variables in the variable collection must be")
                    else:
                        self.var_dict['x' + str(i+1)] = var
                    
            elif type(variable_collection) == dict:
                self.var_dict = variable_collection.copy() # If a dict is passed in, then assign that to be the variable dictionary
            
            else:
                raise TypeError("variable_collection type not understood. Expected list, tuple, dict, or numpy array. Got "+str(type(variable_collection)))
        
        # If no variable_collection provided, then attempt to create the variable dictionary using an inputted coordinate_vector and p_vector
        elif coordinate_vector is not None and p_vector is not None:
            
            assert len(coordinate_vector) == len(p_vector), "coordinate_vector ("+str(len(coordinate_vector))+") and p_vector ("+str(len(p_vector))+") are of differing dimensions"
            
            if type(coordinate_vector) not in [list, np.ndarray, tuple]:
                raise TypeError("p_vector type not conformable. Expected list, numpy array or tuple. Got "+str(type(coordinate_vector)))
            
            if type(p_vector) not in [list, np.ndarray, tuple]:
                raise TypeError("p_vector type not conformable. Expected list, numpy array or tuple. Got "+str(type(p_vector)))
            
            self.var_dict = dict() # Create a blank dict to hold the variable names and objects
            # Use the coordinate_vector and p_vector to create the variable dictionary
            for i, coord in enumerate(coordinate_vector):
                # Since variable names were not provided, assign them the default names of x1, x2, ... etc.
                self.var_dict['x' + str(i+1)] = Variable(value = coord, deriv = p_vector[i])
   
        else:
            raise NameError("Could not instanciate object instance from the VectorAutoDiff class. Please provide a valid variable_collection or coordinate_vector and p_vector") 
            
        # Save a copy of the equations list as an attribute of this object instance - check input type
        if equation_list is not None:
            if type(equation_list) in [list, np.ndarray, tuple]:
                # Accept a list, numpy array or tuple as the input
                if type(equation_list) in [list, np.ndarray]:
                    self.equation_list = list(equation_list.copy()) # Create a copy of the list or numpy array object
                else:
                    # If tuple, then convert to a list and store it in the equation_list attribute
                    self.equation_list = list(equation_list)
            
                # For each equation passed in, check that every variable used is contained in the variable dictionary
                for equation in equation_list:
                    variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
                    self._check_variable_usage(variables_used) # Check that all variables used are contained in the var_dict
            else:
                raise TypeError("equation_list type not understood. Expected list, numpy array or tuple. Got "+str(type(equation_list)))
        else:
            self.equation_list = [] # If blank, then leave as a blank list
        # Create an attribute to hold the accepted data types
        self.accepted_data_types = [int, float, np.int32, np.int64, np.float32, np.float64]
        
    def add_eq(self, *args):
        """
        A method for adding an equation or multiple equations to an instance of the VectorAutoDiff class. Equations should be passed in as positional arguments
        and defined using lambda function notation. 
        Example usage: 
            Assuming we have a VectorAutoDiff_instance instance of the VectorAutoDiff class and want to add an equation of 2 variables: x1 and x2:
            VectorAutoDiff_instance.add_eq(lambda: x1, x2: x1**2 + x2)
        Example usage:
            Multiple equations can be added in a similar way all at once by passing in additional lambda defined functions of the input variables
            VectorAutoDiff_instance.add_eq(lambda: x1, x2: x1**2 + x2, sin(x2)+cos(x1))
        """       
        # For each equation passed in, add it to the internal list of equations. These will preserve the computational steps of evaluation for each function 
        # for future repeated use later e.g. for computing gradients or other derivative and/or functional evaluations
        for equation in args:
            # First check that each argument passed in is a function
            assert callable(equation), "Argument passed in to the add equation method that is not a function."
            variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
            self._check_variable_usage(variables_used) # Check that all variables used for this equation are contained in the variable dictionary, otherwise raise an error
            self.equation_list.append(equation) # If all checks pass, then append this new equation to the internal equation_list
        
        
    def compute_gradient(self, eq_index:int, coordinate_vector=None, full_var_set=False, return_symbolic=False):
        """
        Computes the gradient of a specified equation from the equation list and return it to the user as a numpy array. By default, will compute the gradient
        using the coordinates input variable values encoded in the variable dictionary unless overriden by a user specified coordinate_vector. 

        Parameters
        ----------
        eq_index : int
            The index of the equation from the equation list on which to compute the gradient vector
        
        coordinate_vector : list, np.ndarray, tuple, optional
            An optional user-specified coordinate vector for the input variables. Will compute the gradient vector using this set of input variable coordinate
            values instead of the encoded values found in the variable dictionary, will not change the values of the inputs in the variable dictionary
        
        full_var_set : bool, optional
            A binary indicator that allows a user to specify if they wish for the gradient vector to be return for the entire variable set in the variable dictionary
            where variables that are not present in the equation will have partial derivatives of 0 in the vector corresponding to their entries
        
        Returns
        -------
        np.ndarray
            Returns the gradient vector of the specified equation from the equation list evaluated at the coordinates encoded in the variable dictionary or at the
            coordinates specified by the user
        """
        gradient_vector = [] # Create a blank list to hold the gradient values
        self._validate_eq_index(eq_index) # Validate user input for eq_index
        equation = self.equation_list[eq_index] # Get the equation in question
        # Find the input variables for this function - note, equation keyword argument names must be a subset of the input variables from the variable_vector
        variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
        self._check_variable_usage(variables_used) # Confirm that all variables used in this equation are a subset of the variable dictionary
        
        if return_symbolic==True:
            if full_var_set==True:
                return np.array(["∂f"+str(eq_index+1)+"/∂"+str(var) for var in self.var_dict.keys()])
            else:
                return np.array(["∂f"+str(eq_index+1)+"/∂"+str(var) for var in variables_used])
            
        if coordinate_vector is not None:
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, var_len=len(variables_used)) # Validate user input
            for i, variable in enumerate(variables_used):
                # Loop over each variable used in the function and compute the partial derivative of the function with respect to that variable
                input_variables = [Variable(value = coordinate_vector[i], deriv = 0) if j!=i 
                                   else Variable(value = coordinate_vector[i], deriv = 1) for j in range(len(variables_used))]
                gradient_vector.append(equation(*input_variables).deriv) # Evaluate using this set of variables and append to the output graduent vector
            
        else:
            for i, variable in enumerate(variables_used):
                # Loop over each variable used in the function and compute the partial derivative of the function with respect to that variable
                input_variables = [Variable(value = self.var_dict[var].value, deriv = 0) if j!=i 
                                   else Variable(value = self.var_dict[var].value, deriv = 1) for j, var in enumerate(variables_used)]
                gradient_vector.append(equation(*input_variables).deriv) # Evaluate using this set of variables and append to the output graduent vector
        
        if type(full_var_set)!=bool:
            raise TypeError("full_var_set must be a bool type, got "+str(type(full_var_set)))
            
        if full_var_set==True:
            # If full_var_set is set to true, then insert zeros where the other variables from the variable dictionary would be otherwise           
            gradient_vector = [gradient_vector[variables_used.index(var)] if var in variables_used else 0 for var in list(self.var_dict.keys())]
            
        # Convert to a numpy array as the output and return to the user
        return np.array(gradient_vector)
        
    def compute_jacobian(self, return_symbolic=False, coordinate_vector=None):
        """
        Computes the Jacobian matrix for the full set of equations contained in the equation list and for the full set of input variables encoded in the
        variable dictionary. By default, the Jacobian will be evaluated at the coordianted encoded in the variable dictionary, but the user has the option
        to also pass in a coordinate_vector to compute the Jacobian matrix at an alternative set of coordinates. 

        Parameters
        ----------
        return_symbolic : bool, optional
            If set to true, this method will return the symbolic representation of the Jacobian matrix that describes the computation being done using standard
            calculus notation for each entry of the Jacobian matrix e.g. ∂f1/∂x1 would be the top left entry.
            
        coordinate_vector : list, np.ndarray, tuple, optional
            An optional coordinate vector that users can specify to override the default coordinate location encoded in the variable matrix at which to compute
            the Jacobian matrix for the set of equations contained in the equations list. Passing in an optional coordinate vector will not change the values
            stored in the variable dictionary and must long enough to specify a new coordinate for each and every input variable belonging to the variable dictionary

        Returns
        -------
        np.ndarray
            Return the Jacobian matrix as a numpy array

        """
        if return_symbolic==True:
            # If return_symbolic is set to true, print the Jacobian matrix equations and partial derivatives being computed for each entry in the array
            return np.array([["∂f"+str(i)+"/∂"+str(var) for var in self.var_dict.keys()] for i in range(1,len(self.equation_list)+1)])
        
        if coordinate_vector is not None:
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, var_len=len(self.var_dict)) # Validate user input
            jacobian_output = []
            for eq_idx, equation in enumerate(self.equation_list):
                variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
                input_variables = [coord for var, coord in zip(list(self.var_dict.keys()),coordinate_vector) if var in variables_used]
                jacobian_output.append(self.compute_gradient(eq_idx, coordinate_vector=input_variables, full_var_set=True)) # Compute the gradient of this function for this coord input
            # Return the aggregate output as a numpy array
            return np.array(jacobian_output)
        
        # Computes the Jacobian matrix for a vector valued function of potentially multiple inputs and leverages the compute_gradient method defined above
        # Produces the Jacobian matrix, each row is the gradient of each function with respect to all variables in the variable dictionary
        jacobian_matrix = np.array([self.compute_gradient(eq_idx, full_var_set=True) for eq_idx in range(len(self.equation_list))])       
        return jacobian_matrix

    
    def _check_variable_usage(self, variables_used: list):
        """Helper function that checks that all entries of the list of variables_used passed in are located in the set of var_dict keys"""
        # Checks if a set of variables (a list of strings) are all elements of the var_dict, if not, raise an error to the user specifying which one
        all_vars = list(self.var_dict.keys())
        for var in variables_used:
            if var not in all_vars:
               raise KeyError("Equation variable "+str(var)+" not found in variable vector, please redefine usage")

    def _validate_coordinate_and_p_vector(self, *, coord_vec=None, p_vec=None, var_len):
        """Helper function to validate that the coordinate_vector and p_vector are of an acceptable data type and are both the same length as the required var_len"""
        
        if coord_vec is not None and p_vec is not None:
            # Check the that the length of the coordinate_vector and p_vector match
            if len(coord_vec) != len(p_vec):
                    raise IndexError("Length mismatch between coordinate_vector ("+str(len(coord_vec))+") and p_vector ("+str(len(p_vec))+")")
        
        if coord_vec is not None:
            # Check the that the length of the coordinate_vector and matches that which is expected by var_len
            if len(coord_vec) != var_len:
                raise IndexError("Length mismatch between coordinate_vector ("+str(len(coord_vec))+") and required input variables ("+str(var_len)+")")
        
            # Check that the data type of the coordinate_vector is one of the supported types
            if type(coord_vec) not in [list, np.ndarray, tuple]:
                raise TypeError("coordinate_vector type not understood. Expected list, tuple, or numpy array. Got " + str(type(coord_vec)))
        
        if p_vec is not None:
            # Check the that the length of the p_vector and matches that which is expected by var_len
            if len(p_vec) != var_len:
                raise IndexError("Length mismatch between p_vector ("+str(len(p_vec))+") and required input variables ("+str(var_len)+")")
        
            # Check that the data type of the p_vector is one of the supported types
            if type(p_vec) not in [list, np.ndarray, tuple]:
                raise TypeError("p_vector type not understood. Expected list, tuple, or numpy array. Got " + str(type(p_vec)))

    def _validate_eq_index(self, eq_index):
        """Helper function to validate a eq_index input"""
        if type(eq_index) not in [int, np.int32, np.int64]:
            raise TypeError("eq_index must be passed in as an int type parameter")
        
        if eq_index >= len(self.equation_list):
            raise IndexError("eq_index must be an integer the number of equations, eq_index must be <="+str(len(self.equation_list)-1))
    
    def compute_value(self, eq_index: int, coordinate_vector=None):
        """
        Returns the value of a particular equation evaluated at the current variable values encoded in the variable dictionary, user can also pass in a 
        vector of values to evaluate the function at instead, providing a coordinate_vector will not override the values stored in the variable dictionary
        """
        self._validate_eq_index(eq_index) # Validate the eq_index passed into this method before use
        
        equation = self.equation_list[eq_index] # Pull out the equation to be evaluated
        variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
        self._check_variable_usage(variables_used) # Check that these variables used are part of the variable dictionary
        
        if coordinate_vector is not None:
            # If a user has passed in their own custom coordinate_vector, then compute accordingly instead of using the encoded values in the var_dict
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, var_len=len(variables_used)) # Validate user input
            # If all data validation checks have been passed, then create an input_variables vector to pass into the equation whose value is to be evaluated
            input_variables = [Variable(coordinate_vector[i], self.var_dict[var].deriv) for i, var in enumerate(variables_used)] # Create a new variable subset
            
        else:
            # If no coordinate values passed in, then evalute this function as the values currently set in the variable dictionary
            input_variables = [self.var_dict[var] for var in variables_used] # Extract the variables for this evaluation in the order required by the function
        
        return equation(*input_variables).value # Return the value of this function evaluated at the input variables provided
    
    def compute_value_vector(self, coordinate_vector=None):
        """
        Returns an array of values corresponding to each function in the function list's primal trace functional evaluation given the current encoded variable
        values contained in the variable dictionary. Users can compute a vector of function value evaluations for a different set of coordinate variable input 
        values by passing in an optional coordinate_vector.

        Parameters
        ----------
        coordinate_vector : list, np.ndarray, tuple, optional
            A vector or list of coordinates to evaluate the system of equations at instead of the values currently encoded in the variable dictionary

        Returns
        -------
        np.ndarray
            A vector of values corresponding to each function in the function list evaluated at the current input coorindate variable values

        """
        if coordinate_vector is not None:
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, var_len=len(self.var_dict)) # Validate user input
            output_list = [] # Create a blank list to hold the summary output
            for eq_idx, equation in enumerate(self.equation_list):
                # Iterate over each equation in the equation list
                variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
                # Extract the corresponding coordinate_vector for the variables used in this particular equation for evaluation below 
                input_vector = [coordinate_vector[i] for i, var in enumerate(self.var_dict.keys()) if var in variables_used] 
                output_list.append(self.compute_value(eq_idx, input_vector)) # Use the input_vector generated from the coordinate_vector to evaluate
            return np.array(output_list)

        else:
            # Returns the vector of each function evaluated at the input variables currently encoded in the variable dictionary
            return np.array([self.compute_value(eq_idx) for eq_idx in range(len(self.equation_list))])
            
    def compute_deriv(self, eq_index, coordinate_vector=None, p_vector=None):
        """
        Returns the derivative values of a particular equation evaluated at the current variable class values and p-vector unless the user specifies otherwise
        To specify a custom coordinate_vector and p_vector for evaluation, pass in a list, tuple, or numpy.array for both arguments. Returns a scalar value.
        """
        self._validate_eq_index(eq_index) # Validate the eq_index passed into this method before use
        equation = self.equation_list[eq_index] # Pull out the equation to be evaluated
        variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
        self._check_variable_usage(variables_used) # Check that these variables used are part of the variable dictionary
        
        if coordinate_vector is not None and p_vector is not None:
            # If a user has passed in their own custom coordinate_vector and p_vector, then compute accordingly instead of using the encoded values in the var_dict
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, p_vec=p_vector, var_len=len(variables_used)) # Validate data inputs
            
            # If all data validation checks have been passed, then create an input_variables vector to pass into the equation whose derivative is to be evaluated
            input_variables = [Variable(val, deriv) for val, deriv in zip(coordinate_vector, p_vector)]
            return equation(*input_variables).deriv # Return the value of this function evaluated at the input variables provided
      
        else:
            # If no coordinate values and p-vector passed in, the evaluate this function at the values currently set in the variable dictionary
            input_variables = [self.var_dict[var] for var in variables_used] # Extract the variables for this evaluation in the order required by the function
            return equation(*input_variables).deriv # Return the value of this function evaluated at the input variables provided

    def compute_deriv_vector(self, coordinate_vector=None, p_vector=None):
        """
        Returns an array of values corresponding to each function in the function list's tangent trace derivative evaluation given the current encoded variable
        values contained in the variable dictionary. Users can compute a vector of function derivative evaluations for a different set of coordinate variable input 
        values and p-vector values by passing in an optional coordinate_vector and p_vector.

        Parameters
        ----------
        coordinate_vector : list, np.ndarray, tuple, optional
            A vector or list of coordinates to evaluate the system of equations at instead of the values currently encoded in the variable dictionary
            
        p_vector : list, np.ndarray, tuple, optional
            A vector or list of derivative values to evaluate the system of equations at instead of the values currently encoded in the variable dictionary

        Returns
        -------
        np.ndarray
            A vector of values corresponding to each function in the function list's derivative evaluated at the current input coorindate variable values and p-vector

        """
        if coordinate_vector is not None and p_vector is not None:
            self._validate_coordinate_and_p_vector(coord_vec=coordinate_vector, p_vec=p_vector, var_len=len(self.var_dict)) # Validate user input
            output_list = [] # Create a blank list to hold the summary output
            for eq_idx, equation in enumerate(self.equation_list):
                # Iterate over each equation in the equation list
                variables_used = inspect.getfullargspec(equation)[0] # Get the list of variables used in this function
                # Extract the corresponding coordinate_vector and p_vector values for the variables used in this particular equation for evaluation below 
                input_vector_coords = [coordinate_vector[i] for i, var in enumerate(self.var_dict.keys()) if var in variables_used] 
                input_vector_p_vec = [p_vector[i] for i, var in enumerate(self.var_dict.keys()) if var in variables_used] 
                output_list.append(self.compute_deriv(eq_idx, input_vector_coords, input_vector_p_vec)) # Use the input_vector generated from the coordinate_vector and p_vector to evaluate
            return np.array(output_list)

        else:
            # Returns the vector of each function evaluated at the input variables currently encoded in the variable dictionary
            return np.array([self.compute_deriv(eq_idx) for eq_idx in range(len(self.equation_list))])

    def __repr__(self):
        """Returns a more comprehensive string representation of the object with the variable dictionary and equation list printed to the screen"""
        return "Variable dictionary:\n"+str(self.var_dict)+"\n\nEquations list:\n"+self.__str__()
    
    def __len__(self):
        """Returns the length of a VectorAutoDiff object which will be defined as the length of the equation list"""
        return len(self.equation_list)
    
    def __str__(self):
        """Defines the string representation of the vector valued function VectorAutoDiff object instance. Displays each equation's formulaic expression"""
        
        def clean_equation_str(eq_srt):
            """Helper function to transform the raw string representation of the function into the inner computational component"""
            eq_srt=eq_srt.split(",\n")[0].replace(")\n","")
            return eq_srt[eq_srt.find(":")+1:].strip()

        output_list = [clean_equation_str(inspect.getsource(func)) for func in self.equation_list]
        if len(output_list)>0:
            # If there is at least 1 equation in the equation list, then retunr the vector representation with one equation listed per row
            return "[\n"+",\n".join(output_list)+"\n]"
        else:
            # Otherwise return a blank list representation
            return "[]"
       
    def get_p_vector(self, var_names=False):
        """
        Returns to the user the current p-vector across all variables as a dictionary or without variable names as a numpy array
        
        Parameters
        ----------
        var_names : bool
            A true or false value indicating whether or not the p_vector is to be return as a dictionary with names or numpy array without names
        
        Returns
        -------
            Either a dictionary or numpy array depending on the value of var_names
        """
        if type(var_names)!=bool:
            raise TypeError("var_names must be a boolean value.")
        if var_names==True:
            return {var:item.deriv for var, item in self.var_dict.items()}
        else:
            return np.array([item.deriv for item in self.var_dict.values()])


    def get_coordinate_vector(self, var_names=False):
        """
        Returns to the user the current coordinate vector across all variables as a dictionary or without variable names as a numpy array
        
        Parameters
        ----------
        var_names : bool
            A true or false value indicating whether or not the p_vector is to be return as a dictionary with names or numpy array without names
        
        Returns
        -------
            Either a dictionary or numpy array depending on the value of var_names
        """
        if type(var_names)!=bool:
            raise TypeError("var_names must be a boolean value.")
        if var_names==True:
            return {var:item.value for var, item in self.var_dict.items()}
        else:
            return np.array([item.value for item in self.var_dict.values()])
    
    def update_p_vector(self, p_vector):
        """
        Allows the user to update the p-vector for all variables contained in the variable dictionary all at once or as a subset by name using
        a dictionary of variable names and associated values to update
        
        Parameters
        ----------
        p_vector : list, np.ndarray, tuple, dict
            A list, numpy array, tuple, or dictionary in which either all p-vector values are replaced in-order or specific variables and their values are replaced
        """
        if type(p_vector) in [list, np.ndarray, tuple]:
            if len(p_vector)==len(self.var_dict):
                self.var_dict = {var: Variable(item.value, p_vector[i]) for i, (var, item) in enumerate(self.var_dict.items())}
            else:
                raise IndexError("p_vector length mismatch. Expected length: "+ str(len(self.var_dict)) + ". Got: " +str(len(p_vector)))
        
        elif type(p_vector) == dict:
            if len(p_vector)>len(self.var_dict):
                raise IndexError("p_vector length mismatch. Expected length no greater than: "+ str(len(self.var_dict)) + ". Got: " +str(len(p_vector)))
            else:
                self._check_variable_usage(p_vector.keys())
                for var, item in p_vector.items():
                    if type(item) in self.accepted_data_types:
                        self.var_dict[var].deriv = item
                    else:
                        raise TypeError("p_vector deriv type not understood. Expected float or int as Variable deriv. Got "+ str(type(item)))
        else:
            raise TypeError("p_vector type not understood. Expected list, numpy array, tuple, or or dict. Got "+ str(type(p_vector)))


    def update_coordinate_vector(self, coordinate_vector):
        """
        Allows the user to update the coordinate-vector for all variables contained in the variable dictionary all at once or as a subset by name using
        a dictionary of variable names and associated values to update
        
        Parameters
        ----------
        p_vector : list, np.ndarray, tuple, dict
            A list, numpy array, tuple, or dictionary in which either all coordinate-vector values are replaced in-order or specific variables and their values are replaced
        """
        if type(coordinate_vector) in [list, np.ndarray, tuple]:
            if len(coordinate_vector)==len(self.var_dict):
                self.var_dict = {var: Variable(coordinate_vector[i], item.deriv) for i, (var, item) in enumerate(self.var_dict.items())}
            else:
                raise IndexError("coordinate_vector length mismatched. Expected length: "+ str(len(self.var_dict)) + " Got: " +str(len(coordinate_vector)))
        
        elif type(coordinate_vector) == dict:
            if len(coordinate_vector)>len(self.var_dict):
                raise IndexError("coordinate_vector length mismatched. Expected length no greater than: "+ str(len(self.var_dict)) + " Got: " +str(len(coordinate_vector)))
            else:
                self._check_variable_usage(coordinate_vector.keys())
                for var, item in coordinate_vector.items():
                    if type(item) in self.accepted_data_types:
                        self.var_dict[var].value = item
                    else:
                        raise TypeError("p_vector deriv type not understood. Expected float or int as Variable deriv. Got "+ str(type(item)))
        else:
            raise TypeError("coordinate_vector type not understood. Expected list, tuple, dict, or numpy array. Got " + str(type(coordinate_vector)))
    
    def add_var(self,new_var_dict: dict):
        """
        A method for adding one or more new variables to the variable dictionary core data structure of a VectorAutoDiff object instance
        
        Parameters
        ----------
        new_var_dict :  dict
            A dictionary in which new variables will be added to the existing variable dictionary. If keys provided already exist, updates will be made to those varaibles
            Keys should be provided as variable name strings e.g. "x1" and corresponding values should be instance of the Variable class
        """
        for var, item in new_var_dict.items():
            if type(item) == Variable:
                # Create a new entry in the variable dictionary if one does not already exist or alternatively update the record currently stored at that variable key
                self.var_dict[var] = item
            else:
                raise TypeError("new_var_dict data value not understood. Expectd each element to be an instance of the Variable class. Got "+str(type(item)))
    
    def get_eq_variables(self, eq_index):
        """
        Returns to the user a list of variables used by a particular equation specified at eq_index from the equation_list
        
        Parameters
        ----------
        eq_index :  int
            An index in which the equations at that index from the equations list will be 
        """
        self._validate_eq_index(eq_index) # Validate the eq_index passed into this method before use
        return inspect.getfullargspec(self.equation_list[eq_index])[0]
