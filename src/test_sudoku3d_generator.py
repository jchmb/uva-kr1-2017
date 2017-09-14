from sudoku3d_generator import Sudoku3DGenerator

gen = Sudoku3DGenerator(10)
gen.generate()
gen.sudoku.save('/tmp/sudoku3d_test.txt')
