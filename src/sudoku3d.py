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

	'''
	Check if the given cell (x, y, z) is filled.
	@param int x
	@param int y
	@param int z
	@return bool
	'''
	def isPresent(self, x, y, z):
		return (x, y, z) in self.cells

	'''
	Get the contents of a cell (x, y, z).
	@param int x
	@param int y
	@param int z
	@return int the value (digit) of the cell
	'''
	def get(self, x, y, z):
		return self.cells[(x, y, z)]

	'''
	Fill the given cell (x, y, z) with the given value (digit) d.
	@param int x
	@param int y
	@param int z
	@param int d
	'''
	def fill(self, x, y, z, d):
		self.cells[(x, y, z)] = d

	'''
	Check if the given cell (x, y, z) can contain the given value (digit) d
	without violating the Sudoku3D rules.
	@param int x
	@param int y
	@param int z
	@param int d
	@return bool
	'''
	def isValid(self, x, y, z, d):
		return self.isValidForDim(0, x, y, z, d) and \
			self.isValidForDim(1, x, y, z, d) and \
			self.isValidForDim(2, x, y, z, d)

	'''
	Check for the given dimension dim, if the given cell (x, y, z) can
	contain the given value (digit) d without violating the Sudoku3D rules.
	@param int x
	@param int y
	@param int z
	@param int d
	@return bool
	'''
	def isValidForDim(self, dim, x, y, z, d):
		for i in range(self.dim):
			position = [x, y, z]
			position[dim] = i
			position = tuple(position)
			if position in self.cells and self.cells[position] == d:
				return False
		return True

	'''
	The total number of filled cells.
	@return int
	'''
	def size(self):
		return len(self.cells)

	'''
	Save this Sudoku3D to the given file.
	@param string filename
	'''
	def save(self, filename):
		with open(filename, 'w+') as f:
			for position, d in self.cells.items():
				out = map(str, position + (d,))
				f.write(" ".join(out))
				f.write('\n')

	'''
	Load the Sudoku3D from a given file.
	@param string filename
	@return Sudoku3D
	'''
	@staticmethod
	def load(filename):
		sudoku = Sudoku3D()
		with open(filename, 'r') as f:
			for line in f:
				parts = line.split()
				x = int(parts[0])
				y = int(parts[1])
				z = int(parts[2])
				d = int(parts[3])
				sudoku.fill(x, y, z, d)
		return sudoku
