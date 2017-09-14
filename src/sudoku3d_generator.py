import random
from sudoku3d import Sudoku3D

class Sudoku3DGenerator:
	def __init__(self, k, dim=9):
		self.sudoku = Sudoku3D(dim)
		self.k = k
		self.maxSize = dim**3

	def fillCell(self):
		if self.maxSize == self.sudoku.size():
			pass
		x = random.choice(self.sudoku.dim)
		y = random.choice(self.sudoku.dim)
		z = random.choice(self.sudoku.dim)
		d = random.choice(self.sudoku.dim)
		if self.sudoku.isPresent(x, y, z) or not self.sudoku.isValid(x, y, z, d):
			self.fillCell()

	def generate(self):
		for i in range(self.k):
			self.fillCell()
