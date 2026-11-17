# Documentation for SAT solver for the "Nonogram" problem (problem #21)

## Problem description 

Nonograms are a popular picture puzzles. Nonogram is a $m \times n$ grid of cells (not necessarily $m=n$), cells must be colored black or left empty (not colored) according to the numbers on edges of the grid. Each row and column of a grid has a number. The coloring of the row/edge must follow the constraint given by its respective numbers and do not break the constraints of the neighbouring rows and columns - with that said, it is meant that every row and every column matches its clues exactly. Constraints usually shows the required sequence of the colored consecutive cells. Example: (3,1) clause for a row means that we have block of 3 colored cells, empty gap of unspecified amount of uncolored cells, 1 colored cell. 
As a result the user gets valid coloring of the cells, which results in the picture. 
More information about the nonograms are available online [online](https://en.wikipedia.org/wiki/Nonogram).

The problem is described by giving the solver the .txt file with the input (grid with the rows and columns constraints) and getting the result after processing, showing if this is valid colorable nonogram or not. 

An example of a valid input format is a 


## Encoding 



## User documentation 



## Example instances 


## Experiments 
