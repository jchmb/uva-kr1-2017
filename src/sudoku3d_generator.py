import random
from sudoku3d import Sudoku3D

class Sudoku3DGenerator:
	def __init__(self, N, M, tries=999):
		self.N = N
		self.M = M
		self.tries = tries

	def getRandomPosition(self):
		return random.randint(0, self.N - 1)

	def generate(self):
		sudoku = Sudoku3D(self.N)
		for i in range(self.M):
			for j in range(self.tries):
				unfilledCells = [position for position in sudoku.getCellIterator() if not sudoku.isFilled(*position)]
				position = random.choice(unfilledCells)
				d = random.choice(list(sudoku.get(*position)))
				if sudoku.fill(*position, d):
					break
		return sudoku
