# Sudoku game

Solve Sudoku like CSP (Constraint Satisfaction Problem)

Each cell inside the Sudoku is treated as a variable, that needs to satisfy a number of constraints, i.e. no-repeat same number in the row, column or square. The game has 81 variables, some of them are assigned, others must be guessed.

[AC3 (arcs-constraint) algorithm](https://en.wikipedia.org/wiki/AC-3_algorithm) is used for pre-processing and some heuristics like [LCV (Least-constraining-value)](https://cs.stackexchange.com/questions/47870/what-is-least-constraining-value) in order to improve the search time.

Finally, the magic is done with the combination of [Backtracking search](https://en.wikipedia.org/wiki/Backtracking) and AC3 algorithm.

The repo includes a file with 400 sudokus for testing. [sudokus_start](https://github.com/evimarp/sudoku/blob/master/sudokus_start.txt)
