import random
from sudoku3d import Sudoku3D

class Sudoku3DGenerator:
	def __init__(self, N, M, tries=50, restarts=1000000):
		self.N = N
		self.M = M
		self.tries = tries
		self.restarts = 50

	def getRandomPosition(self):
		return random.randint(0, self.N - 1)

	def generate(self):
		for i in range(self.restarts):
			sudoku = self.generateStep()
			if self.N**3 - len(sudoku.getUnfilledCells()) >= self.M:
				return sudoku
		return None

	def generateStep(self):
		sudoku = Sudoku3D(self.N)
		for i in range(self.M):
			for j in range(self.tries):
				unfilledCells = sudoku.getUnfilledCells()
				if len(unfilledCells) == 0:
					return sudoku
				position = random.choice(unfilledCells)
				d = random.choice(list(sudoku.get(*position)))
				if sudoku.fill(*position, d):
					break
		return sudoku
