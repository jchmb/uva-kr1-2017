from sudoku3d_alt_generator import Sudoku3DAlternativeGenerator

size = 4
k = size**3 - 1
gen = Sudoku3DAlternativeGenerator(size, k)

sudoku = gen.generate()

print('Sudoku generated')
print(sudoku)
