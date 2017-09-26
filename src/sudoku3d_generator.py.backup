import random
from sudoku3d import Sudoku3D

'''
Generator for Sudoku3D objects of size N*N*N.
'''


class Sudoku3DGenerator:
    '''
    Constructor.
    @param int k the number of cells to fill randomly
    @param int dim the dimensionality N of the Sudoku3D
    '''
    def __init__(self, k, size=9):
        self.size = size
        self.k = k
        self.maxSize = size**3

    '''
    Fill a single cell with a random digit, with the constraint that it must
    satisfy the Sudoku3D rules. Will try again if it fails, unless there are
    no empty cells left.
    '''
    def fillCell(self):
        if self.maxSize == self.sudoku.numberFilledCells():
            raise Exception('Too many cells to fill')

        (x, y, z) = self.sudoku.randomUnfilledPosition()
        validValues = self.sudoku.validValuesForPosition(x, y, z)

        if len(validValues) == 0:
            return False

        d = random.choice(validValues)
        self.sudoku.fill(x, y, z, d)
        return True

    '''
    Generate the Sudoku3D.
    @return Sudoku3D
    '''
    def generate(self, maxTries=10000000):

        tries = 1
        while tries <= maxTries:
            self.sudoku = Sudoku3D(size=self.size)
            foundSudoku = True

            for i in range(self.k):
                res = self.fillCell()
                if not res:
                    foundSudoku = False
                    tries += 1
                    break

            if foundSudoku:
                return self.sudoku, tries
        return None, None
