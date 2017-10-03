import random
from sudoku3d import Sudoku3D

'''
@class Sudoku3DAlternativeGenerator
Alternative generator for Sudoku3D objects of size N*N*N where M cells are filled.
'''
class Sudoku3DAlternativeGenerator:
	def __init__(self, N, M):
		self.N = N
		self.M = M

    '''
    Shift the sequence one to the right. The last element will appear at the start.
    @param list<int> base
    @return list<int>
    '''
	def shift(self, base):
		# Copy the original list (I know, the notation is weird).
		perm = base[:]
		# Pop and append the first element to the list.
		perm.append(perm.pop(0))
		return perm

    '''
    Get the block given a list of blocks and a block number.
    @param list<list<int>> blocks
    @param int number
    @return list<int>|None
    '''
	def getBlock(self, blocks, number):
		for block in blocks:
			if block[0] == number:
				return block
		return None

    '''
    Delete N**3 - M cells for the given Sudoku3D.
    @param Sudoku3D sudoku
    '''
	def deleteCells(self, sudoku):
		cells = list(sudoku.getCellIterator())
		for i in range(self.N**3 - self.M):
			cell = random.choice(cells)
			del sudoku.cells[cell]
			cells.remove(cell)

    '''
    Generate the Sudoku3D.
    @return Sudoku3D
    '''
	def generate(self):
		sudoku = Sudoku3D(self.N)
		base = list(range(1, self.N + 1))
		random.shuffle(base)
		rows = []
		perm = base
		for i in range(self.N):
			rows.append(perm)
			perm = self.shift(perm)
		random.shuffle(rows)
		baseBlock = list(range(1, self.N + 1))
		random.shuffle(baseBlock)
		blocks = []
		block = baseBlock
		for i in range(self.N):
			blocks.append(block)
			block = self.shift(block)
		for x in range(self.N):
			for y in range(self.N):
				block = self.getBlock(blocks, rows[x][y])
				for z in range(self.N):
					sudoku.fill(x + 1, y + 1, z + 1, block[z])
		self.deleteCells(sudoku)
		return sudoku
