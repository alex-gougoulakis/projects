import random 
import copy
from submatrix import submatrix

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    # dictionary of the 3x3 submatrix each index in a 9x9 sudoku belongs to
    SUBMATRIX = submatrix
    
    # check if the initial state of the sudoku is valid
    if not is_valid(sudoku, SUBMATRIX):
        array = np.full((9,9), -1)
        return array
    
    # find indices in the initial state of the sudoku which are 0 (values we must fill in)
    indices = np.argwhere(sudoku == 0) 
    # convert the numpy arrays to lists
    indices = indices.tolist()
        
    # create a list of possible values mirroring the sudoku's initial state
    possible_values = sudoku.tolist() 
    
    # replace every index in possible_values that contains a 0 with the list of all possible values (0-9)
    for i in range(len(indices)):
        x = indices[i][0]
        y = indices[i][1]
        possible_values[x][y] = [1, 2, 3, 4, 5, 6, 7, 8, 9] 
        
    # stores how many possible values there are at each index with an undetermined value
    indices_dict = {}
    
    # add all indices that have undetermined values to the dictionary
    for i in range(len(indices)):
        x = indices[i][0]
        y = indices[i][1]
        # initially, all undetermined indices have 9 possible values (1-9)
        indices_dict[(x, y)] = 9 
        
    
    # apply constraints to initial state
    for i in range(9):
        for j in range(9):
            # only apply constraints for a specific index if it has an undetermined value
            if not(type(possible_values[i][j]))==list: 
                apply_constraints(i, j, possible_values, SUBMATRIX, indices_dict)
        
    
    # if applying constraints alone has not solved the sudoku
    if len(indices_dict.keys())!=0:
        possible_values = dfs(possible_values, SUBMATRIX, indices_dict, root=True)
    
    # convert possible_values back into a numpy array
    arr = np.array(possible_values)
    
    # check if the final state is valid
    if not is_valid(possible_values, SUBMATRIX):
        array = np.full((9,9), -1)
        return array
    else: 
        return arr

        
def is_valid(sudoku, SUBMATRIX):
    """
    Checks if a given sudoku state is valid (has no duplicates in the same row,
    column or 3x3 sub-matrix). It runs checks for every element in the sudoku.
    
    Parameters:
        sudoku: the sudoku state (9x9 numpy array/list)
        SUBMATRIX: a dictionary containing the 3x3 submatrices each index in a 9x9
                   sudoku belongs to
    
    Returns: bool
    """

    for i in range(9):
        for j in range(9):
            
            value = sudoku[i][j]
            # if the value is 0, we can ignore it since it is an empty space, not a number
            if value == 0: continue
                  
            # DUPLICATES IN ROWS AND COLUMNS
            for k in range(9):
                
                # if there is a duplicate in the same row
                if sudoku[i][k]==value:
                    # if the duplicate isn't in the same position as the value
                    if k!=j: return False
                        
                # if there is a duplicate in the same column
                if sudoku[k][j]==value:
                    if k!=i: return False
            
            # DUPLICATES IN 3X3 SUBMATRICES
            for m in range(SUBMATRIX[(i, j)][0][0], SUBMATRIX[(i, j)][0][1]+1):
                for n in range(SUBMATRIX[(i, j)][1][0], SUBMATRIX[(i, j)][1][1]+1):
                    
                    # if there is a duplicate in the same 3x3 sub-matrix
                    if sudoku[m][n]==value:
                        # if the duplicate isn't in the same position as the value
                        if m!=i and n!=j: return False

    return True


def is_valid_single(i, j, sudoku, SUBMATRIX):
    """
    Checks if a given sudoku state is valid (has no duplicates in the same row,
    column or 3x3 sub-matrix). It runs checks for a specific element located at
    index [i][j]
    
    Parameters:
        sudoku: the sudoku state (9x9 numpy array/list)
        SUBMATRIX: a dictionary containing the 3x3 submatrices each index in a 9x9
                   sudoku belongs to
    
    Returns: bool
    """
    
    value = sudoku[i][j]
                  
    # DUPLICATES IN ROWS AND COLUMNS
    for k in range(9):
                
        # if there is a duplicate in the same row
        if sudoku[i][k]==value:
            # if the duplicate isn't in the same position as the value
            if k!=j: return False
                        
        # if there is a duplicate in the same column
        if sudoku[k][j]==value:
            if k!=i: return False
            
    # DUPLICATES IN 3X3 SUBMATRICES
    for m in range(SUBMATRIX[(i, j)][0][0], SUBMATRIX[(i, j)][0][1]+1):
        for n in range(SUBMATRIX[(i, j)][1][0], SUBMATRIX[(i, j)][1][1]+1):
                    
            # if there is a duplicate in the same 3x3 sub-matrix
            if sudoku[m][n]==value:
                # if the duplicate isn't in the same position as the value
                if m!=i and n!=j: return False
                        
    return True


def is_goal_state(sudoku, SUBMATRIX):
    """
    Checks if a given sudoku state is the goal state.
    
    Parameters:
        sudoku: the sudoku state (9x9 numpy array/list)
        SUBMATRIX: a dictionary containing the 3x3 submatrices each index in a 9x9
                   sudoku belongs to
        
    Returns: bool
    """
    
    # first check if the sudoku is valid
    if not is_valid(sudoku, SUBMATRIX): return False
    
    # if it is valid, check if any of its values are undetermined
    else:
        for i in range(9):
            for j in range(9):
                if type(sudoku[i][j]) == list: return False
        return True
    

def least_possible_values(indices_dict):
    """
    Heuristic that determines the index at which there are the least possible branches.
    
    Parameters:
         indices_dict: keys: tuples containing pairs of i,j indices whose values are
                        undetermined
                       values: number of possible values index the index i,j can take
                       
    Returns: tuple (i, j) if a minimum is found, -1 otherwise
    """
    
    # initialize the minimum value at something absurdly high
    min_amount = 9999
    min_key = None
    
    for key in indices_dict.keys():
        # if the number of values a specific index can take is 1 (abnormal), 
        # disregard this element, since its value is already determined
        if indices_dict[key] < min_amount and indices_dict[key]!=1:
            min_amount = indices_dict[key]
            min_key = key

    # if no minimum is found, return -1
    if min_key is None: return -1
    else: return min_key
        
    
def apply_constraints(i, j, possible_values, SUBMATRIX, indices_dict):
    """
    Used to update possible values for rows, columns, and 3x3 submatrices
    when a new value is added to the sudoku.
    
    Parameters:
        i, j: the indexes of the value we are adding in the sudoku
        possible_values: a list that mirrors the sudoku--at indexes where
                         values have been determined, it contains the values.
                         at indexes with undetermined values, it contains a
                         list of possible values.
        SUBMATRIX: a dictionary containing the 3x3 submatrices each index in
                   a 9x9 sudoku belongs to
        indices_dict: keys: tuples containing pairs of i,j indices whose values are
                            undetermined
                      values: number of possible values index the index i,j can take

    Returns: None
    """
    
    # the value for which we will apply constraints
    value = possible_values[i][j]
    
    # DUPLICATES IN ROWS #
    for k in range(9):
        
        if possible_values is None:
            return None
        
        # if index i,k contains a list and the value is in the list
        if type(possible_values[i][k])==list and (value in possible_values[i][k]):
            
            # remove the value from possibilities- rows
            possible_values[i][k].remove(value)
            
            # decrement the number of possible values at index i,k
            indices_dict[(i,k)] -= 1

            # turn lists of length 1 into numbers
            if len(possible_values[i][k])==1: 
                possible_values[i][k] = possible_values[i][k][0]

                # remove key with index i,k from the dictionary
                indices_dict.pop((i, k))

                # recurse when a value is determined
                apply_constraints(i, k, possible_values, SUBMATRIX, indices_dict) 

    
    # DUPLICATES IN COLUMNS #
 
    for l in range(9):
        
        # if index l,j contains a list and the value is in the list    
        if type(possible_values[l][j])==list and (value in possible_values[l][j]):
            
            # remove already used value from possibilities- columns
            possible_values[l][j].remove(value)
            # decrement the number of possible values at index l,j
            indices_dict[(l,j)] -= 1
                
            # turn lists of length 1 into numbers
            if len(possible_values[l][j])==1:
                possible_values[l][j] = possible_values[l][j][0]

                # remove key with index i,k from the dictionary
                indices_dict.pop((l, j))
                
                # recurse when a value is determined
                apply_constraints(l, j, possible_values, SUBMATRIX, indices_dict)
    
    
    # DUPLICATES IN 3X3 SUBMATRICES #               

    for m in range(SUBMATRIX[(i, j)][0][0], SUBMATRIX[(i, j)][0][1]+1):
        for n in range(SUBMATRIX[(i, j)][1][0], SUBMATRIX[(i, j)][1][1]+1):
            
            # if index l,j contains a list and the value is in the list    
            if type(possible_values[m][n])==list  and (value in possible_values[m][n]):
                
                # remove already used value from possibilities- submatrices
                possible_values[m][n].remove(value) 
                 # decrement the number of possible values at index m,n
                indices_dict[(m,n)] -= 1
                
                # turn lists of length 1 into numbers
                if len(possible_values[m][n])==1:
                    possible_values[m][n] = possible_values[m][n][0]

                    # remove key with index m,n from the dictionary
                    indices_dict.pop((m, n))
                    
                    # recurse when a value is determined
                    apply_constraints(m, n, possible_values, SUBMATRIX, indices_dict)
                    
                    
def make_indices_dict(possible_values):
    """
    Creates an indices dict for a specific sudoku state. An indices dict contains:
        keys: tuples containing pairs of i,j indices whose values are undetermined
        values: number of possible values index the index i,j can take
                      
    Parameters:
        possible_values: the sudoku state (9x9 numpy array/list)
        
    Returns: dict
    """
    
    indices_dict = {}
    
    for i in range(9):
        for j in range(9):
            # get all the indices which contain lists = have undetermined values
            if type(possible_values[i][j])==list:
                indices_dict[(i, j)]= len(possible_values[i][j])
                
    if not indices_dict: return None
    else: return indices_dict
    
    
def dfs(possible_values, SUBMATRIX, indices_dict, root=True):
    """
    Runs a DFS on a sudoku state. 
    
    Parameters:
        possible_values: the sudoku state (9x9 numpy array/list)
        SUBMATRIX: a dictionary containing the 3x3 submatrices each index in
                   a 9x9 sudoku belongs to
        indices_dict: keys: tuples containing pairs of i,j indices whose values are
                            undetermined
                      values: number of possible values index the index i,j can take
        root: (optional--defaults to True) bool used to determine whether the function
              currently running is a recursive call
              
    Returns: a goal state (solved sudoku) if a solution exists, a 9x9 numpy array filled
             with -1s otherwise    
    """
    
    # get the index [i][j] of the sudoku state that has the least possible values
    min_key = least_possible_values(indices_dict)
    # get the list of possible values at that index
    values_list = possible_values[min_key[0]][min_key[1]]
    
    # iterate through the possible values
    for value in values_list:
        
        # create a deep copy of the current sudoku state
        new_possible_values = copy.deepcopy(possible_values)
        # set one of the values
        new_possible_values[min_key[0]][min_key[1]] = value
        
        # if the state is invalid when the value is set, continue
        if not is_valid_single(min_key[0], min_key[1], new_possible_values, SUBMATRIX): continue
            
        # make a new indices dict for the current state
        indices_dict = make_indices_dict(new_possible_values)
        
        # apply constraints to the rest of the state
        apply_constraints(min_key[0], min_key[1], new_possible_values, SUBMATRIX, indices_dict)

        # if the current state is the goal state, return it
        if is_goal_state(new_possible_values, SUBMATRIX): 
            return new_possible_values
        
        else:
            # make a new indices dict for the state after constraint propagation
            new_indices_dict = make_indices_dict(new_possible_values)
            
            # if the dict is not empty
            if new_indices_dict is not None: 
                
                # call dfs on the state
                rec = dfs(new_possible_values, SUBMATRIX, new_indices_dict, root=False)
                #if recursion finds the goal state, return it
                if is_goal_state(rec, SUBMATRIX): return rec
                else: continue
    
    # if we don't find a solution at the root, return the 9x9 full of -1s
    if root: return np.full((9,9), -1)
    # if we don't find a solution in one of the intermediate stages, return the unedited state
    else: return possible_values
        