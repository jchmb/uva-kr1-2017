import random
from sudoku3d import Sudoku3D

'''
Generator for Sudoku3D objects of size N*N*N.
'''
class Sudoku3DGenerator:
	'''
	Constructor.
	@param int k the number of cells to fill randomly
	@param int dim the dimensionality N of the Sudoku3D
	'''
	def __init__(self, k, dim=9):
		self.sudoku = Sudoku3D(dim)
		self.k = k
		self.maxSize = dim**3

	'''
	Generate a random digit between 1 and N (inclusive).
	@return int
	'''
	def randomDigit(self):
		return random.randint(1, self.sudoku.dim)

	'''
	Fill a single cell with a random digit, with the constraint that it must
	satisfy the Sudoku3D rules. Will try again if it fails, unless there are
	no empty cells left.
	'''
	def fillCell(self):
		if self.maxSize == self.sudoku.size():
			pass
		x = self.randomDigit()
		y = self.randomDigit()
		z = self.randomDigit()
		d = self.randomDigit()
		if self.sudoku.isPresent(x, y, z) or not self.sudoku.isValid(x, y, z, d):
			self.fillCell()
		else:
			self.sudoku.fill(x, y, z, d)

	'''
	Generate the Sudoku3D.
	@return Sudoku3D
	'''
	def generate(self):
		for i in range(self.k):
			self.fillCell()
		return self.sudoku
