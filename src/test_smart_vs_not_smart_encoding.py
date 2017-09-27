from sudoku3d import Sudoku3D
from sudoku3d_dimecs_converter import SudokuDimecsConverter
from sudoku3d_dimecs_solver import DimecsSolver

sudokus_path = '../test_sudokus/'
dimecs_path = '../test_sudokus_dimecs/'
filename = 'try5_5_5_1given'

# Load/Genereate sudoku
sudoku = Sudoku3D(5)
sudoku2 = Sudoku3D(5)
sudoku.fill(5, 5, 4, 4)
sudoku2.fill(5, 5, 4, 4)
sudoku.fill(5, 5, 5, 5)
sudoku2.fill(5, 5, 5, 5)


print(sudoku)

# Convert to dimecs and save file
converter = SudokuDimecsConverter(sudoku)
converter2 = SudokuDimecsConverter(sudoku2)

dim = converter.convert(smart=False)
dim2 = converter2.convert(smart=True)

dim.save(dimecs_path + filename)
dim2.save(dimecs_path + filename + 'smart')

solver = DimecsSolver(dimecs_path)

output = solver.solve_single(filename)
output2 = solver.solve_single(filename + 'smart')

if output.parsed_data['sat']:
    converter.remap_solution(dimecs_path + '/out/' + filename)
    print(sudoku)
    print(output)
    print(output2)
    print(dim.num_vars())
    print(dim2.num_vars())
    print(dim.num_clauses())
    print(dim2.num_clauses())
else:
    print('No solution')
