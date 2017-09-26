from sudoku3d_alt_generator import Sudoku3DAlternativeGenerator
from sudoku3d import Sudoku3D


size = 9
k = size**3 - 1
# k = int(size**3 / 2)
gen = Sudoku3DAlternativeGenerator(size, k)#, 50, 1000)

sudoku = gen.generate()
tries = 0 # TODO: what do with this?

fileName = '/tmp/sudoku3d_test_%d_%d.txt' % (k, size)
sudoku.save(fileName)
#sudoku = Sudoku3D.load(fileName, size) TODo

print('Sudoku generated, took %d tries' % tries)
print(sudoku)
