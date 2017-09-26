import random
from sudoku3d import Sudoku3D

class Sudoku3DAlternativeGenerator:
	def __init__(self, N, M):
		self.N = N
		self.M = M

	def generate(self):
		sudoku = Sudoku3D(self.N)
		base1 = list(range(self.N))
		random.shuffle(base)
