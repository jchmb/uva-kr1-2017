'''
Sudoku3D class. Encapsulates a 3D sudoku of size N*N*N.
'''
class Sudoku3D:
	'''
	Constructor.
	@param int dim the dimensionality N of the Sudoku3D
	'''
	def __init__(self, dim=9):
		self.dim = dim
		self.cells = {}

	def isPresent(self, x, y, z):
		return (x, y, z) in self.cells

	def get(self, x, y, z):
		return self.cells[(x, y, z)]

	def fill(self, x, y, z, d):
		self.cells[(x, y, z)] = d

	def isValid(self, x, y, z, d):
		return self.isValidForDim(0, x, y, z, d) and \
			self.isValidForDim(1, x, y, z, d) and \
			self.isValidForDim(2, x, y, z, d)

	def isValidForDim(self, dim, x, y, z, d):
		for i in range(self.dim):
			position = [x, y, z]
			position[dim] = i
			position = tuple(position)
			if position in self.cells and self.cells[position] == d:
				return False
		return True

	def size(self):
		return len(self.cells)

	def save(self, filename):
		with open(filename, 'w+') as f:
			for position, d in self.cells.items():
				out = map(str, position + (d,))
				f.write(" ".join(out))
				f.write('\n')
