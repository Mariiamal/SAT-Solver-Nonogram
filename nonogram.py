import subprocess
from argparse import ArgumentParser 

def parse_clue(line): 
    clue = tuple(map(int, line.split()))
    if any(i < 0 for i in clue): raise ValueError("Invalid negative number in a constraint, unsatisfiable")
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
    sum_of_rows_colored = sum(map(sum, rows))
    sum_of_cols_colored = sum(map(sum, cols))
    if sum_of_rows_colored != sum_of_cols_colored: 
        raise ValueError("Row and column clues have different totals, trivially unsatisfiable")
  
    return number_of_rows, number_of_cols, rows, cols

def encode(instance): 
