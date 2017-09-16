from sudoku3d_generator import Sudoku3DGenerator
from sudoku3d import Sudoku3D


k = 20
size = 4
gen = Sudoku3DGenerator(k, size)

sudoku, tries = gen.generate()

fileName = '/tmp/sudoku3d_test_%d_%d.txt' % (k, size)
sudoku.save(fileName)
sudoku = Sudoku3D.load(fileName, size)

print('Sudoku generated, took %d tries' % tries)
print(sudoku)
