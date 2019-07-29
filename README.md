# Sudoku game

Solve Sudoku like CSP (Constraint Satisfaction Problem)

Each celd inside the Sudoku is treat like a variable, that need to satisfied a number of contraints, i.e. non repeat same number in the row, col or square.
The game have 81 variables, some of them are assigned, other must be guessed.

AC3 (arcs-constraint) algorithm is used for pre-processing and some heuristics like LCV (less constraint value) in order to improve the search time.

Finally, the magic is done with the combination of Backtracking search and AC3 algorithm.

The repo include a file with 400 sudokus for testing. 
