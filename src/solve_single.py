from sudoku3d import Sudoku3D
from sudoku3d_dimecs_converter import SudokuDimecsConverter
from sudoku3d_dimecs_solver import DimecsSolver

sudokus_path = '../test_sudokus/'
dimecs_path = '../test_sudokus_dimecs/'
filename = 'try5_5_5_1given'

# Load/Genereate sudoku
sudoku = Sudoku3D(5)
sudoku.fill(5, 5, 5, 5)

print(sudoku)

# Convert to dimecs and save file
converter = SudokuDimecsConverter(sudoku)
dim = converter.convert()
dim.save(dimecs_path + filename)

solver = DimecsSolver(dimecs_path)
output = solver.solve_single(filename)

if output.parsed_data['sat']:
    converter.remap_solution(dimecs_path + '/out/' + filename)
    print(sudoku)
    print(output)
else:
    print('No solution')
