import random
from sudoku3d import Sudoku3D

class Sudoku3DGenerator:
	def __init__(self, k, dim=9):
		self.sudoku = Sudoku3D(dim)
		self.k = k
		self.maxSize = dim**3

	def randomDigit(self):
		return random.randint(1, self.sudoku.dim)

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

	def generate(self):
		for i in range(self.k):
			self.fillCell()
