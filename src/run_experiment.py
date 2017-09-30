import sys
import csv
import os
import re
from argparse import ArgumentParser
from sudoku3d_alt_generator import Sudoku3DAlternativeGenerator
from sudoku3d_dimecs_converter import SudokuDimecsConverter
from sudoku3d_dimecs_solver import DimecsSolver

# Parse args
argparser = ArgumentParser(description='Run some experiments on some N*N*N 3D sudokus')
argparser.add_argument('nmin', type=int, help='Minimum value for N')
argparser.add_argument('nmax', type=int, help='Maximum value for N')
argparser.add_argument('mperc', type=int, nargs='+', help='Set of percentages of filled cells')
argparser.add_argument('--k', type=int, default=1, help='Number of repetitions for each parameter setting')
parsed_args = argparser.parse_args()

def parameter_iterator(min_N, max_N, percentages_M):
    for N in range(min_N, max_N + 1):
        for percentage_M in percentages_M:
            M = int((float(percentage_M) / 100.0) * (N**3))
            yield (N, M)

# Define directories
directory = '../experimental_results'
dimecs_directory = '%s/%s' % (directory, 'dimecs')

# Create directories if missing
if not os.path.exists(dimecs_directory):
    os.makedirs(dimecs_directory)
    os.makedirs('%s/%s' % (dimecs_directory, 'out'))

num_experiments = parsed_args.k
for N, M in parameter_iterator(parsed_args.nmin, parsed_args.nmax, parsed_args.mperc):
    gen = Sudoku3DAlternativeGenerator(N, M)
    for i in range(num_experiments):
        sudoku = gen.generate()
        converter = SudokuDimecsConverter(sudoku)
        for smart in [True, False]:
            dimecs = converter.convert()
            dimecs.save('%s/sudoku_%s_%s_%s_%s' % (dimecs_directory, N, M, i, 1 if smart else 0))

# Solve and write the results to a CSV file.
field_names = ['N', 'M', 'k', 'smart', 'sat',
    'restarts', 'conflicts', 'decisions',
    'conflict_literals', 'propagations',
    'cpu_time', 'clauses', 'variables']
solver = DimecsSolver(dimecs_directory)
results = solver.solve_all_in_dir()
with open('%s/results.csv' % (directory,), 'w') as f:
    writer = csv.DictWriter(f, field_names)
    writer.writeheader()
    for res in results:
        match = re.search('sudoku_([0-9]+)_([0-9]+)_([0-9]+)_([0-9])', res.name)
        line = dict(res.parsed_data)
        line['N'] = int(match.group(1))
        line['M'] = int(match.group(2))
        line['k'] = int(match.group(3))
        line['smart'] = bool(match.group(4))
        writer.writerow(line)
