# Documentation for SAT solver for the "Nonogram" problem (problem #21)

## Problem description 

Nonograms are a popular picture puzzles. Nonogram is a $m \times n$ grid of cells (not necessarily $m=n$), cells must be colored black or left empty (not colored) according to the numbers on edges of the grid. Each row and column of a grid has a number. The coloring of the row/edge must follow the constraint given by its respective numbers and do not break the constraints of the neighbouring rows and columns - with that said, it is meant that every row and every column matches its clues exactly. Constraints usually shows the required sequence of the colored consecutive cells. Example: (3,1) clause for a row means that we have block of 3 colored cells, empty gap of unspecified amount of uncolored cells, 1 colored cell. 
As a result the user gets valid coloring of the cells, which results in the picture. 
More information about the nonograms are available online [online](https://en.wikipedia.org/wiki/Nonogram).

The problem is described by giving the solver the .txt file with the input (grid with the rows and columns constraints) and getting the result after processing, showing if this is valid colorable nonogram or not. 

An example of a valid input format is a 
```
4 4
1 1 
1 1 
2
3
2
2
1 1
3
```

First line: number of rows $m$ and number of columns $n$. Next $m$ lines are the constraints for all $m$ rows. One line per each row, separated by a whitespace. Next $n$ lines are the column constraints, similarly one per each column. By convention, there can be empty row or empty column in the nonogram - no cells are colored, this will be denoted as 0. 
Note: if sum of $m$ rows does not equal sum of $n$ columns - trivially not a valid nonogram (i.e.unsolvable). 

## Encoding 
The problem is encoded using two sets of variables - cells variables and pattern variables. For $m \times n$ grid, there are $mn$ cells, each of the form $(row, column)$. Each cell is mapped to its variable number. According to the DIMACS CNF format, the first variable will have number 1. The last cell variable number is $m*n + 1$. Second set of variables - pattern variables. 

## User documentation 

Usage: 
```
python3 nonogram.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}] [--show-model]
```
Basic usage (default):
```
python3 nonogram.py [-i INPUT] [-v {0,1}]
```

Command-line options: 
* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula). Default: "formula.cnf".
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used. 0 hides the solver statistics and program output, 1 includes it.
*  `--show-model`: Also prints the raw model (lines starting with 'v') returned by SAT solver to the stdout. Be default hidden due to the big size for big instances and not suitable for human - readable solution.

Example of the call to additionally print the model for an instance of the input:
```
python3 nonogram.py -i instances/input-10by10.in --show-model
```

## Example instances 

* `input-3by3.in`: A 3x3 instance, the fastest and the easiest, human-solvable
* `input-3by3unsat.in`: A 3x3 instance, unsolvable
* `input-5by5.in`: A 5x5 instance
* `input-5by5unsat.in`: A 5x5 instance, unsolvable
* `input-10by10.in`: A 10x10 instance
* `input-10by10unsat.in`: A 10x10 instance, unsolvable
* `input-25by25.in`: A 25x25 instance middle
* `input-26by26hard.in`: A 26x26 instance, the hardest example, takes approximately 61s of real time and 207s of cpu time to solve on this machine
