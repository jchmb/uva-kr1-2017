import sys

class Sudoku3D:
	def __init__(self, N):
		self.N = N
		self.cells = [set(range(1, N+1)) for i in range(N**3)]

	def getCellIterator(self):
		return ((x, y, z) for x in range(self.N) for y in range(self.N) for z in range(self.N))

	def getCellIndex(self, x, y, z):
		return x + y * self.N + z * (self.N**2)

	def get(self, x, y, z):
		return self.cells[self.getCellIndex(x, y, z)]

	def getLineIterator(self, dim, x, y, z, excludeOrigin=False):
		origin = (x, y, z)
		for i in range(self.N):
			pos = [x, y, z]
			pos[dim] = i
			pos = tuple(pos)
			if not excludeOrigin or pos != origin:
				yield pos

	def atLeastOnce(self, dim, x, y, z, withoutD):
		for d in range(self.N):
			count = 0
			for pos in self.getLineIterator(dim, x, y, z):
				cell = self.get(*pos) - set([withoutD])
				if d in cell:
					count += 1
			if count < 1:
				return False
		return True

	def atMostOnce(self, dim, x, y, z, withoutD):
		for d in range(self.N):
			count = 0
			for pos in self.getLineIterator(dim, x, y, z):
				cell = self.get(*pos) - set([withoutD])
				if d in cell:
					count += 1
					if count > 1:
						return False
		return True

	def validForDim(self, dim, x, y, z, d):
		origin = (x, y, z)
		for i in range(self.N):
			pos = [x, y, z]
			pos[dim] = i
			pos = tuple(pos)

			# If filling in d at (x, y, z) causes pos to be invalid,
			# then it is not a valid action.
			updatedCell = self.get(*pos) - set([d])
			if pos != origin:
				if updatedCell == set():# or not self.atLeastOnce(dim, *pos, d):
					return False
		return True

	def validForCell(self, x, y, z, d):
		index = self.getCellIndex(x, y, z)
		return d in self.cells[index] and \
			self.validForDim(0, x, y, z, d) and \
			self.validForDim(1, x, y, z, d) and \
			self.validForDim(2, x, y, z, d)

	def prunePossibilities(self, dim, x, y, z, d):
		origin = (x, y, z)
		for i in range(self.N):
			pos = [x, y, z]
			pos[dim] = i
			pos = tuple(pos)
			if pos != origin:
				self.cells[self.getCellIndex(*pos)] -= set([d])

	def getUnfilledCells(self):
		return [position for position in self.getCellIterator() if not self.isFilled(*position)]

	def isFilled(self, x, y, z):
		return len(self.get(x, y, z)) == 1

	def fill(self, x, y, z, d):
		if self.isFilled(x, y, z) or not self.validForCell(x, y, z, d):
			return False
		self.cells[self.getCellIndex(x, y, z)] &= set([d])
		self.prunePossibilities(0, x, y, z, d)
		self.prunePossibilities(1, x, y, z, d)
		self.prunePossibilities(2, x, y, z, d)
		return True

	def __str__(self):
		unfilledCellsCount = len(self.getUnfilledCells())
		filledCellsCount = self.N**3 - unfilledCellsCount
		returnStr = 'Sudoku of size %d\n' % (self.N)
		returnStr += '%d cells of which %d filled (%d unfilled)\n\n' % \
			(self.N**3, filledCellsCount, unfilledCellsCount)
		for x in range(self.N):
			returnStr += 'x=' + str(x) + '\n'
			for y in range(self.N):
				for z in range(self.N):
					if self.isFilled(x, y, z):
						(d,) = self.get(x, y, z)
						returnStr += str(d)
					else:
						returnStr += '-'
				returnStr += '\n'
			returnStr += '\n'

		return returnStr

	'''
	Save this Sudoku3D to the given file.
	@param string filename
	'''
	def save(self, filename):
		with open(filename, 'w+') as f:
			for position in self.getCellIterator():
				possibilities = self.get(*position)
				(d,) = possibilities if len(possibilities) == 1 else (0,)
				out = map(str, position + (d,))
				f.write(" ".join(out))
				f.write('\n')
