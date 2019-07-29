"""
Created on Wed Mar 15 15:30:30 2017

@author: evimar.principal@gmail.com

AI Solves Sudoku games like Constraint Satisfaction Problem
Using AI algorithms of AC3 and backtracking
"""
from itertools import product
from collections import deque
import copy

LETTERS = 'ABCDEFGHI'
NUMBERS = '123456789'
DOMAIN = {i for i in NUMBERS}


def neighbors(variable):
    """ List all celds in the influence areas (row, col and square)
    :param variable a tuple: a valid celd to fill
    :return houses a set of celds that affect the variable
    """
    row, col = variable
    houses = set()

    # same row
    for i in product(row, NUMBERS.replace(col, '')):
        houses.add(i[0]+i[1])

    # same column
    for i in product(LETTERS.replace(row, ''), col):
        houses.add(i[0]+i[1])
        
    # same square
    r1 = (LETTERS.index(row)//3) * 3
    c1 = (NUMBERS.index(col)//3) * 3
    
    for i in product(LETTERS[r1:r1+3].replace(row, ''),
                     NUMBERS[c1:c1+3].replace(col, '')):
        houses.add(i[0]+i[1])
        
    return houses


def arcs(variable):
    """ Return a set of tuple (variable, influence)
    where influence is a celd in the same area (row, col or square)
    that the variable celd
    """
    neighborhood = neighbors(variable)
    
    constraint = set()

    for i in neighborhood:
        constraint.add((variable, i))
        
    return constraint


def revise(xi, xj, d):
    revised = False
    di = copy.deepcopy(d[xi])
    dj = d[xj]
    for x in di:
        if len(dj - {x}) == 0:
            d[xi] -= {x}
            revised = True
            
    return revised


def ac3(unassigned, doms):
    """
    Modifies the domains of each non-assigned variable
    Return
    False - If some variable domain is empty, because this path is no viable.
    True - If each non-assigned variable has at least one value in its domain.
    """
    # Init the Queue with the rules
    queue = deque()

    for variable in unassigned:
        cons = arcs(variable)
        for c in cons:
            queue.append(c)
            
    while queue:
        xi, xj = queue.popleft()
        if revise(xi, xj, doms):
            if not len(doms[xi]):
                return False
            neighborhood = neighbors(xi) - {xj}
            for xk in neighborhood:
                queue.append((xk, xi))

    return True


def lcv(variables, domain_dict):
    """
    Less constraint variable
    Choose the variable with less remain values to assign
    :param: variables is a set of variables names
    :param domain_dict is a dict maps variables -> domain
    :return
    the name of variable with less constraints
    """
    lcv = ''
    min_domain = 100
    for variable in variables:
        len_domain = len(domain_dict[variable])
        if len_domain < min_domain:
            min_domain = len_domain
            lcv = variable
        
    return lcv


def domain(variable, sudoku):
    """
    Calculate the values that this variable can take
    between 1 and 9 according to the constraint of sudoku
    Arg variable is a text a letter and number like A1 or I9
    rows are letters between A and I and 
    columns are numbers between 1 and 9
    sudoku is a dictionary with the actual assigment
    
    return a set of string values 
    """
    
    if sudoku[variable] != '0':
        return {sudoku[variable]}
        
    exclude = {sudoku[tile] for tile in neighbors(variable)}

    return DOMAIN - exclude


def backtrack(unassigned, domain_dict, sudoku):
    missing = len(unassigned)

    if missing:
        # solution found!
        r = ""
        for i in product(LETTERS, NUMBERS):
            variable = i[0]+i[1]
            r += sudoku[variable]
            
        print(sudoku)
        print(domain_dict)
        return r     
        
    # Choose the variable with shortest domain
    var = lcv(unassigned, domain_dict)
    print("Choose variable ", var, domain_dict[var])
    var_domain = list(domain_dict[var])
    
    # Let's try to find a suitable value for this variable
    unassigned = unassigned - {var}  

    # Try one by one all possible values in the variable domain,
    # and test which are consistent
    for valor in var_domain:
        # Try assign a possible value
        sudoku[var] = valor
        domain_dict[var] = {valor}
        
        # Copy the domain dictionary
        # before to make inferences (guesses)
        # work with the copy and let intact the original,
        # in case we need back to this point.
        dict_domain_copy = copy.deepcopy(domain_dict)
        
        # If it is consistent
        if ac3(unassigned, dict_domain_copy):
            # making inferences
            unassigned_copy = unassigned.copy()
            for variable in unassigned_copy:
                if len(dict_domain_copy[variable])==1:
                    sudoku[variable] = dict_domain_copy[variable].pop()
                    unassigned.remove(variable)

            # and calculate the next variable
            result = backtrack(unassigned, dict_domain_copy, sudoku)
            
            if result != 'failure':
                return result

            # we must try the next value
            unassigned = unassigned_copy

    return 'failure'
    
    
def backtracking_search(unassigned, domain_dict, sudoku):
    return backtrack(unassigned, domain_dict, sudoku)

    
def solve_sudoku(sudoku_digits):
    """ Solve sudoku game
    :param sudoku_digits string - represent a sudoku game,
        each char represent a celd of the sudoku, in total 81 celds
        the empty celds will be represent with 0 digit
        The string have exactly 81 digits between 0 and 9
        """
    param1 = [i for i in sudoku_digits]

    sudoku = dict()
    domain_dict = dict()
    unassigned = set()

    posi = 0

    # Create the dict with initial digits according to arg
    # Build the initial sudoku
    for i in product(LETTERS, NUMBERS):
        value = param1[posi]
        variable = i[0]+i[1]
        sudoku[variable] = value  # Assign the initial param value to the dict
        # If the digit is zero, this celd needs to be filled
        if value == '0':
            unassigned.add(variable)
        posi += 1
    
    for variable in sudoku:
        domain_dict[variable] = domain(variable, sudoku)
    
    solution = backtracking_search(unassigned, domain_dict, sudoku)

    return solution


if __name__ == '__main__':
    # read 400 sudokus file
    with open("sudokus_start.t  xt", "r") as f:
        sudokus = [l.replace("\n", "") for l in f.readlines()]

    solutions = list()
    # solve 400 sudokus
    for sudoku in sudokus:
        solutions.append(solve_sudoku(sudoku))

