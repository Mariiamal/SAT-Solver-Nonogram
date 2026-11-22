# Documentation for SAT solver for the "Nonogram" problem (problem #21)

## Problem description 

Nonograms are popular picture puzzles. Nonogram is a $m \times n$ grid of cells (not necessarily $m=n$), cells must be colored black or left empty (not colored) according to the numbers on edges of the grid(constraints). Each row and column of a grid has a number (or numbers). The coloring of the row/edge must follow the constraint given by its respective numbers and do not break the constraints of the neighbouring rows and columns - with that said, it is meant that every row and every column matches its clues exactly. Constraints show the required sequence of the colored consecutive cells. Example: (3,1) clause for a row means that this row must have block of 3 colored cells, empty gap of unspecified amount of uncolored cells (minimum mandatory gap is 1), 1 colored cell. 
As a result the user gets valid coloring of the cells, which results in the picture. 
More information about the nonograms are available online [online](https://en.wikipedia.org/wiki/Nonogram).

The problem is described by giving the solver the .txt file with the input (grid with the rows and columns constraints) and getting the result after processing, showing if this is valid colorable nonogram or not - solver prints SAT/UNSAT to the stdout, the statistics and the 'colored' nonogram (if SAT). 

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

First line: number of rows $m$ and number of columns $n$. Next $m$ lines are the constraints for all $m$ rows. One line per each row, separated by a whitespace. Next $n$ lines are the column constraints, similarly one per each column, divided by a whitespace. By convention, there can be empty row or empty column in the nonogram - no cells are colored, this will be denoted as 0. 

## Encoding 
The problem is encoded using two sets of variables - cells variables and pattern variables. 

For $m \times n$ grid, there are $m \times n$ cells, each of the form $(row, column)$. Each cell is mapped to its variable number. According to the DIMACS CNF format, the first variable will have number 1, such that cells variables are $1, \dots, m \times n$. Variable is True, when it is colored. In the results it is shown as # (hashtag). Variable is False, when it is not colored, denoted as . (dot). 

By DIMACS CNF, $x$ means that variable $x$ is True and $-x$ means that x is False.

Second set of variables - pattern variables, denoted as $p$. The first pattern variable has number $m \times n + 1$, all next variables are numbered one higher. For each row and column, we generate all possible valid placements that satisfy the given constraint for that line. For each such placement, set one pattern variable. 

To understand if there is a solution to the given nonogram, we use the following constraints: 
- Numbers in the input file has to be non-negative (0 is valid by the rules of the game). 
- If the sum of $m$ rows does not equal the sum of $n$ columns - not a valid nonogram, UNSAT.
- The sum of the constraints + gaps between them must be less than or equal to the length of the line, otherwise UNSAT.
- Process every row and column (further see as line):
  
  As previously noted, all possible placements of the blocks, defined by the constraint with minimum unit gap in between, are generated for each line and pattern variables are       assigned. Cells inside the block are colored (variable is True). There can be several placements for each line, but there is only one final pattern which will satisfy the          assignment. If the pattern variable $p$ is True, it implies that every cell of the line must have the value that $p$ assigns to it.
  $p \implies l_1 \wedge l_2 \wedge \dots \wedge l_k$, where $l_i$ is $x_i$ if the cell is colored and $\neg x_i$ if not, $\forall i = 1 \dots k$, where $k$ is the length of the     line.
  For each cell add the corresponding clause to the CNF formula:
  - $x$ is True in pattern $p$, then $(\neg p \vee x)$
  - $x$ is False in pattern $p$, then $(\neg p \vee \neg x)$
- There is only one proper assignment for the line:
  
  If there were 2 valid assignments, their patterns have to differ at least in one cell, so that one cell will be colored and blank at the same time, which is contradiction to the   satisfiability of the nonogram.
- There is at least one valid placement per line:

  For each line, after adding all placement clauses, include the clause with all of its pattern variables, which is equivalent to saying that there is at least one proper            placement. Example: there are 3 patterns $p_{15}$, $p_{16}$, $p_{17}$ for a line, add clause $(p_{15} \vee p_{16} \vee p_{17})$ to the CNF.

## Alternatives of the encoding



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
