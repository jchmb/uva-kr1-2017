from sudoku3d_generator import Sudoku3DGenerator
from sudoku3d_dimecs_converter import SudokuDimecsConverter
from sudoku3d_dimecs_solver import DimecsSolver

size = 16
missing = 400
k = size**3 - missing

sudokus_path = '../test_sudokus/'
dimecs_path = '../test_sudokus_dimecs/'
filename = 'sudoku_%d-missing-%d' % (size, missing)

gen = Sudoku3DGenerator(size, k)
sudoku = gen.generate()

converter = SudokuDimecsConverter(sudoku)
dim = converter.convert(smart=True)
dim.save(dimecs_path + filename)
solver = DimecsSolver(dimecs_path)
output = solver.solve_single(filename)

print('Sudoku generated')
print(sudoku)

if output.parsed_data['sat']:
    converter.remap_solution(dimecs_path + '/out/' + filename)
    print(sudoku)
    print(output)
else:
    print('No solution')
