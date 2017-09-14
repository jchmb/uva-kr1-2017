from sudoku3d_generator import Sudoku3DGenerator
from sudoku3d import Sudoku3D

gen = Sudoku3DGenerator(10)
gen.generate()
gen.sudoku.save('/tmp/sudoku3d_test.txt')
sudoku = Sudoku3D.load('/tmp/sudoku3d_test.txt')
sudoku.save('/tmp/sudoku3d_test_loaded_then_saved.txt')
