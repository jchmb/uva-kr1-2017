from sudoku3d_generator import Sudoku3DGenerator
from sudoku3d import Sudoku3D


size = 3
k = size**3 - 1
gen = Sudoku3DGenerator(size, k)

sudoku = gen.generate()
tries = 0 # TODO: what do with this?

fileName = '/tmp/sudoku3d_test_%d_%d.txt' % (k, size)
sudoku.save(fileName)
#sudoku = Sudoku3D.load(fileName, size) TODo

print('Sudoku generated, took %d tries' % tries)
print(sudoku)
