import random
from sudoku3d import Sudoku3D


class Sudoku3DAlternativeGenerator:
    def __init__(self, N, M):
        self.N = N
        self.M = M

    def shift(self, base):
        # Copy the original list (I know, the notation is weird).
        perm = base[:]
        # Pop and append the first element to the list.
        perm.append(perm.pop(0))
        return perm

    def getBlock(self, blocks, number):
        print(blocks)
        for block in blocks:
            if block[0] == number:
                return block
        return None

    def deleteCells(self, sudoku):
        cells = list(sudoku.getCellIterator())
        for i in range(self.N**3 - self.M):
            cell = random.choice(cells)
            tdd = set(range(1, self.N + 1))
            sudoku.cells[sudoku.getCellIndex(*cell)] = tdd
            cells.remove(cell)

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
                    if not sudoku.fill(x, y, z, block[z]):
                        print(x, y, z, block)
        self.deleteCells(sudoku)
        return sudoku
