import subprocess
from argparse import ArgumentParser 

def parse_clue(line): 
    clue = tuple(map(int, line.split()))
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
  
    return number_of_rows, number_of_cols, rows, cols

# Get variable number for DIMACS CNF format, they always start with 1
def get_variable_number(cell_tuple, number_of_cols):
    return cell_tuple[0] * number_of_cols + cell_tuple[1] + 1

def get_cell_row_and_col(variable_number, number_of_cols): 
    number = variable_number - 1
    row = number // number_of_cols
    column = number % number_of_cols 
    return (row, column)

def generate_valid_placements(length, clue): 
    # For each cell: colored 1, not colored 0
    # If block is colored - all cells (i,j) = 1
    valid_placements = []
    blocks_starts = []

    
    # Check all possible starts of the block and recursively call the function for the subsequent blocks. 
    # If the end of the line is reached - each cell of the block has value 1.
    # Save the pattern to the valid placement list 
    def recursive_placement_helper(block_idx, earliest_start): 
        # Base case: all blocks are placed, add valid pattern to the list
        if block_idx == len(clue): 
            pattern = length * [0]
            for i in range(len(clue)): 
                pattern[blocks_starts[i] : blocks_starts[i] + clue[i]] = clue[i] * [1]
            valid_placements.append(pattern)
            return

        remaining_blocks = clue[block_idx:]
        # Minimum space remaining blocks take when they are packed with 1 gap in between
        needed_place = sum(remaining_blocks) + len(remaining_blocks) - 1 
        latest_start = length - needed_place 

        # Try all valid positions for the block: for each i, add it as a start, recursive call, undo i
        for i in range(earliest_start, latest_start + 1): 
            blocks_starts.append(i)
            recursive_placement_helper(block_idx + 1, i + clue[block_idx] + 1)
            blocks_starts.pop() 

    recursive_placement_helper(0, 0)
    return valid_placements

# Variables counter gives the starting point for the pattern variables numbers
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
            if pattern[i] == 1: clauses.append([-p, cells_variable_numbers[i]])
            elif pattern[i] == 0: clauses.append([-p, -cells_variable_numbers[i]])

    clauses.append(patterns_variable_numbers)

    return clauses, variables_counter

def encode(instance): 
    number_of_rows, number_of_cols, rows, cols = instance
    cnf = []
    # Start from rows*cols+1 - that are the cells variables numbers which are already reserved
    variables_counter = number_of_rows * number_of_cols + 1

    for i in range(number_of_rows):
        cells = [get_variable_number((i, j), number_of_cols) for j in range(number_of_cols)]
        row_clauses, variables_counter = encode_line(cells, rows[i], variables_counter)
        cnf.extend(row_clauses)

    for j in range(number_of_cols):
        cells = [get_variable_number((i, j), number_of_cols) for i in range(number_of_rows)]
        column_clauses, variables_counter = encode_line(cells, cols[j], variables_counter)
        cnf.extend(column_clauses)

    return cnf, variables_counter - 1

def call_solver(cnf, variables_number, output_filename, solver_name, verbosity): 
    # Print CNF into formula.cnf in DIMACS format
    with open(output_filename, "w") as file: 
        file.write("p cnf " + str(variables_number) + " " + str(len(cnf)) + '\n')
        for clause in cnf: 
            file.write(' '.join(str(lit) for lit in clause + ["0"]) + '\n')

    # Call the solver and return result 
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_filename], stdout=subprocess.PIPE)

# Convention: 10=SAT, 20=UNSAT, 0=UNKNOWN, 1(or other non-zero)=Error
def print_result(result, number_of_rows, number_of_cols): 

    # Print the whole output of the SAT solver to the stdout
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if result.returncode == 20: 
        print("UNSAT")
        return
    elif result.returncode == 0: 
        print("UNKNOWN")
        return
    elif result.returncode != 10:
        print("Error")
        return

    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):    # There might be more lines of the model, each starting with 'v'
            variables = line.split()
            variables.remove("v")
            model.extend(int(v) for v in variables)      
    model.remove(0) # 0 is the end of the model, ignore it

    print()
    print("##################################################################")
    print("###########[ Human readable result of the Nonogram ]##############")
    print("##################################################################")
    print()

    # Decode the meaning of the assignment
    for i in range(number_of_rows): 
        for j in range(number_of_cols): 
            v = get_variable_number((i,j), number_of_cols)
            if model[v-1] > 0: 
                print("#", end="")
            else: 
                print('.', end="")
        print()

if __name__ == "__main__": 
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # Get the input instance
    instance = load_instance(args.input)
    number_of_rows, number_of_cols, rows, cols = instance

    # Encode the problem to create CNF formula
    cnf, variables_number = encode(instance)

    # Call the SAT solver and get the result
    result = call_solver(cnf, variables_number, args.output, args.solver, args.verb)

    # Interpret the result and print it in a human-readable format
    print_result(result, number_of_rows, number_of_cols)
  