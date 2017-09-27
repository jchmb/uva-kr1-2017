import random


'''
Sudoku3D class. Encapsulates a 3D sudoku of size N*N*N.
'''


class Sudoku3D:
    '''
    Constructor.
    @param int size the size of the sudoku
    '''
    def __init__(self, size=9):
        self.size = size
        self.cells = {}
        self.unfilledCells = size**3
        self.filledCells = 0

    def all_positions(self):
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                for z in range(1, self.size + 1):
                    yield (x, y, z)

    def getCellIterator(self):
        return ((x, y, z) for x in range(1, self.size + 1)
                for y in range(1, self.size + 1)
                for z in range(1, self.size + 1))

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
    def fill(self, x, y, z, d, checkValid=False):
        x = int(x)
        y = int(y)
        z = int(z)
        if checkValid and not self.isValid(x, y, z, d):
            raise Exception('Invalid  %d in cell (%d, %d, %d)' % (d, x, y, z))

        if not self.isPresent(x, y, z):
            self.filledCells += 1
            self.unfilledCells -= 1
            self.cells[(x, y, z)] = int(d)

    '''
    Unfill the given cell (x, y, z) with the given value (digit) d.
    @param int x
    @param int y
    @param int z
    @param int d
    '''
    def unfill(self, x, y, z):
        if self.isPresent(x, y, z):
            self.filledCells -= 1
            self.unfilledCells += 1
            self.cells.pop((x, y, z), None)

    def ratioFilled(self):
        return self.filledCells / (self.filledCells + self.unfilledCells)

    def numberFilledCells(self):
        return self.filledCells

    def numberUnfilledCells(self):
        return self.unfilledCells

    def filledPositions(self):
        return self.cells.keys()

    def unfilledPositions(self):
        unfilledPositions = []
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                for z in range(1, self.size + 1):
                    if not self.isPresent(x, y, z):
                        unfilledPositions.append((x, y, z))

        return unfilledPositions

    def randomUnfilledPosition(self):
        if self.ratioFilled() > 0.5:
            (x, y, z) = random.choice(self.unfilledPositions())
            return (x, y, z)
        else:
            while True:
                x = random.randint(1, self.size)
                y = random.randint(1, self.size)
                z = random.randint(1, self.size)
                if not self.isPresent(x, y, z):
                    return (x, y, z)

    def validValuesForPosition(self, x, y, z):
        validValues = []
        for d in range(1, self.size + 1):
            if self.isValid(x, y, z, d):
                validValues.append(d)

        return validValues

    def __str__(self):
        returnStr = 'Sudoku of size %d\n' % (self.size)
        returnStr += '%d cells of which %d filled (%d unfilled)\n\n' % \
            (self.size**3, self.filledCells, self.unfilledCells)
        for x in range(1, self.size + 1):
            returnStr += 'x=' + str(x) + '\n'
            for y in range(1, self.size + 1):
                for z in range(1, self.size + 1):
                    if self.isPresent(x, y, z):
                        returnStr += str(self.cells[(x, y, z)])
                    else:
                        returnStr += '-'
                returnStr += '\n'
            returnStr += '\n'

        return returnStr

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
        return self.isValidForDim(1, x, y, z, d) and \
            self.isValidForDim(2, x, y, z, d) and \
            self.isValidForDim(3, x, y, z, d)

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
        dim -= 1
        for i in range(1, self.size + 1):
            position = [x, y, z]
            position[dim] = i
            position = tuple(position)
            if position in self.cells and self.cells[position] == d:
                return False
        return True

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
    def load(filename, size):
        sudoku = Sudoku3D(size)
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                x = int(parts[0])
                y = int(parts[1])
                z = int(parts[2])
                d = int(parts[3])
                sudoku.fill(x, y, z, d)
        return sudoku
