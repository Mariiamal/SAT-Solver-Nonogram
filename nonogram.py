import subprocess
from argparse import ArgumentParser 

def parse_clue(line): 
    clue = tuple(map(int, line.split()))
   # if any(i < 0 for i in clue): raise ValueError("Invalid negative number in a constraint, unsatisfiable")
    return () if clue == (0,) else clue


def load_instance(input_file_name): 
    rows = []
    cols = []
    with open(input_file_name, "r") as file: 
        dims = next(file).split()
        number_of_rows = int(dims[0]) 
        number_of_cols = int(dims[1])
        for _ in range(number_of_rows): 
            rows.append(parse_clue(next(file)))
        for _ in range(number_of_cols): 
            cols.append(parse_clue(next(file)))
    # sum_of_rows_colored = sum(map(sum, rows))
    # sum_of_cols_colored = sum(map(sum, cols))
    # if sum_of_rows_colored != sum_of_cols_colored: 
    #     raise ValueError("Row and column clues have different totals, trivially unsatisfiable")
  
    return number_of_rows, number_of_cols, rows, cols

# get variable number for dimacs variable, they always start with 1
def get_variable_number(cell_tuple, number_of_cols):
    return cell_tuple[0] * number_of_cols + cell_tuple[1] + 1

def get_cell_row_and_col(variable_number, number_of_cols): 
    number = variable_number - 1
    row = number // number_of_cols
    column = number % number_of_cols 
    return (row, column)

def generate_valid_placements(length, clue): 
    # for each cell: colored 1, not colored 0 -- block get 1 
    valid_placements = []
    blocks_starts = []

    # each time we handle one block (check all possible starts of this block) 
    # and recursively call this function to handle the next block. if we reached the end of the line - we fill cells of the blocks with 1s 
    # and save to the valid placement list 
    def recursive_placement_helper(block_idx, earliest_start): 
        ## base case: all blocks are placed, add valid pattern
        if block_idx == len(clue): 
            pattern = length * [0]
            for i in range(len(clue)): 
                pattern[blocks_starts[i] : blocks_starts[i] + clue[i]] = clue[i] * [1]
            valid_placements.append(pattern)
            return

        remaining_blocks = clue[block_idx:]
        # minimum space remaining blocks take when they are packed with 1 gap in between
        needed_place = sum(remaining_blocks) + len(remaining_blocks) - 1 
        latest_start = length - needed_place 

        # trying all valid pos for the block: for each i, add it as a start, recursive call, undo i
        for i in range(earliest_start, latest_start + 1): 
            blocks_starts.append(i)
            recursive_placement_helper(block_idx + 1, i + clue[block_idx] + 1)
            blocks_starts.pop() 

    recursive_placement_helper(0, 0)
    return valid_placements

# x1 is cell colored black and ~x1 is cell colored white 
# in the variables it is p1 and -p1 

# variables counter gives us the starting point for the pattern variables numbers
# cells_variable_numbers - list 
def encode_line(cells_variable_numbers, clue, variables_counter): 
    clauses = []
    patterns_variable_numbers = []

    placements = generate_valid_placements(len(cells_variable_numbers), clue)

    for pattern in placements: 
        p = variables_counter
        variables_counter += 1 
        patterns_variable_numbers.append(p)

        for i in range(len(cells_variable_numbers)): 
            if (pattern[i] == 1): clauses.append([-p, cells_variable_numbers[i]])
            elif (pattern[i] == 0): clauses.append([-p, -cells_variable_numbers[i]])

    clauses.append(patterns_variable_numbers)

    return clauses, variables_counter

def encode(instance): 
    number_of_rows, number_of_cols, rows, cols = instance
    clauses = []
    # start from rows*cols+1 because thats the cells variables which are already taken
    variables_counter = number_of_rows * number_of_cols + 1

    for i in range(number_of_rows):
        cells = [get_variable_number((i, j), number_of_cols) for j in range(number_of_cols)]
        row_clauses, variables_counter = encode_line(cells, rows[i], variables_counter)
        clauses.extend(row_clauses)

    for j in range(number_of_cols):
        cells = [get_variable_number((i, j), number_of_cols) for i in range(number_of_rows)]
        column_clauses, variables_counter = encode_line(cells, cols[i], variables_counter)
        clauses.extend(column_clauses)

    return clauses, variables_counter - 1