from sudoku3d import Sudoku3D
from pprint import pformat
import itertools
import re


class SymbolConverter:

    def __init__(self):
        self.map = {}
        self.map_rev = {}
        self.counter = 1

    def rev_convert(self, number_to_find):
        number_to_find = int(number_to_find)
        number_to_find_abs = abs(number_to_find)
        if number_to_find_abs in self.map_rev:
            if number_to_find < 0:
                return '-' + self.map_rev[number_to_find_abs]
            else:
                return self.map_rev[number_to_find_abs]

    def convert(self, symbol):
        if symbol in self.map:
            return self.map[symbol]
        else:
            self.map[symbol] = self.counter
            self.map_rev[self.counter] = symbol
            self.counter += 1
            return self.map[symbol]

    def conv_pos_value(self, pos, value):
        pos += (value, )
        return self.convert('p_%d_%d_%d_%d' % pos)

    def print_map(self, reverse=False):
        for key, value in self.map.items():
            if reverse:
                print(str(value) + ' -> ' + str(key))
            else:
                print(str(key) + ' -> ' + str(value))


class DimecsRepresentaion:

    def __init__(self):
        self.clauses = []
        self.comments = []

    def add_clause(self, clause, comments=None):
        self.clauses.append(clause)
        self.comments.append(comments)

    def add_clause_neg(self, clause, comments=None):
        clause = list(map(lambda x: x * -1, clause))
        self.add_clause(clause, comments)

    def add_single_var(self, var, comments=None):
        self.add_clause([var], comments)

    def add_single_var_neg(self, var, comments=None):
        self.add_clause([-var], comments)

    def num_vars(self):
        flat_list = [abs(var) for clause in self.clauses for var in clause]
        return len(set(flat_list))

    def num_clauses(self):
        return len(self.clauses)

    def get_dimecs(self, comments=True):
        dimecs = 'p cnf %d %d\n' % (self.num_vars(), self.num_clauses())

        for (clause, comment) in zip(self.clauses, self.comments):
            if comment is not None and comments:
                dimecs += 'c ' + comment + '\n'
            for var in clause:
                dimecs += str(var) + ' '
            dimecs += '0\n'

        return dimecs

    def get_dimecs_mapped(self, converter, comments=True):
        dimecs = 'p cnf %d %d\n' % (self.num_vars(), self.num_clauses())

        for (clause, comment) in zip(self.clauses, self.comments):
            if comment is not None and comments:
                dimecs += 'c ' + comment + '\n'
            for var in clause:
                dimecs += converter.rev_convert(var) + ' '
            dimecs += '0\n'

        return dimecs

    def save(self, filename):
        with open(filename, 'w+') as f:
            for line in self.get_dimecs(False):
                f.write(line)

    def __str__(self):
        return pformat(self.clauses)


class SudokuDimecsConverter:

    def __init__(self, sudoku):
        self.dim = DimecsRepresentaion()
        self.conv = SymbolConverter()
        self.su = sudoku

    def convert(self, smart=True):
        self.smart = smart
        self.add_givens()
        self.add_at_least_one()
        self.add_at_most_one()
        self.add_valid_rows()
        self.add_valid_columns()
        self.add_valid_layers()

        return self.dim

    def remap_solution(self, filename):
        with open(filename, 'r') as f:
            # dirty trick, we only want the last line of the file
            for line in f:
                pass

            variables = line.rstrip('\n').split(' ')
            variables = filter(lambda x: int(x) > 0, variables)
            symbols = map(lambda x: self.conv.rev_convert(x), variables)

            for symbol in symbols:
                match = re.match(r'p_(\d)_(\d)_(\d)_(\d)', symbol)
                (x, y, z, d) = match.groups()
                self.su.fill(x, y, z, d)

    def add_givens(self):
        for pos in self.su.filledPositions():
            value = self.su.get(*pos)
            symbol = self.conv.conv_pos_value(pos, value)
            self.dim.add_single_var(symbol, 'Given value')

            if self.smart:
                all_values = list(range(1, self.su.size+1))
                all_values.remove(value)
                for value in all_values:
                    symbol = self.conv.conv_pos_value(pos, value)
                    self.dim.add_single_var_neg(symbol)

    def add_at_least_one(self):
        if self.smart:
            positions = self.su.unfilledPositions()
        else:
            positions = self.su.all_positions()

        for pos in positions:
            clause = []
            for d in range(1, self.su.size + 1):
                clause.append(self.conv.conv_pos_value(pos, d))
            self.dim.add_clause(clause, 'at least one (%d, %d, %d)' % pos)

    def add_at_most_one(self):
        if self.smart:
            positions = self.su.unfilledPositions()
        else:
            positions = self.su.all_positions()

        for pos in positions:
            for (d, e) in different_number_combinations(self.su.size):
                clause = [-1 * self.conv.conv_pos_value(pos, d),
                          -1 * self.conv.conv_pos_value(pos, e)]
                self.dim.add_clause(clause, 'at most one (%d, %d, %d)' % pos)

    def add_valid_rows(self):
        for y in range(1, self.su.size + 1):
            for z in range(1, self.su.size + 1):
                row = [(x, y, z) for x in range(1, self.su.size + 1)]
                self.add_valid(row, 'is valid row (y,z) = (%d,%d)' % (y, z))

    def add_valid_columns(self):
        for x in range(1, self.su.size + 1):
            for z in range(1, self.su.size + 1):
                col = [(x, y, z) for y in range(1, self.su.size + 1)]
                self.add_valid(col, 'is valid col (x,z) = (%d,%d)' % (x, z))

    def add_valid_layers(self):
        for x in range(1, self.su.size + 1):
            for y in range(1, self.su.size + 1):
                lay = [(x, y, z) for z in range(1, self.su.size + 1)]
                self.add_valid(lay, 'is valid layer (x,y) = (%d,%d)' % (x, y))

    def add_valid(self, positions, comment):
        for p in itertools.permutations(positions, 2):
            # we need only half of permutations because (p1, p2) == (p2, p1)
            if p[0] < p[1]:
                for d in range(1, self.su.size + 1):
                    clause = [-1 * self.conv.conv_pos_value(p[0], d),
                              -1 * self.conv.conv_pos_value(p[1], d)]
                    self.dim.add_clause(clause, comment)


def different_number_combinations(n):
    n += 1
    for d in range(1, n):
        for e in range(d + 1, n):
            yield (d, e)


def TestSymbolConverter():
    conv = SymbolConverter()
    p1234 = conv.convert('p1234')
    p1235 = conv.convert('p1235')
    p1234_2 = conv.convert('p1234')
    p1235_2 = conv.convert('p1235')

    assert p1234 == p1234_2 == 1
    assert p1235 == p1235_2 == 2
    assert conv.rev_convert(-1) == '-p1234'


def TestSudokuDimecsConverter():
    sudoku = Sudoku3D(9)

    converter = SudokuDimecsConverter(sudoku)
    dimecs = converter.convert(smart=False)

    assert dimecs.num_clauses() == 105705
    assert dimecs.num_vars() == 6561

    dimecs.get_dimecs(False)
    dimecs.get_dimecs_mapped(converter.conv, comments=False)


def TestBigSudokuDimecsConverter():
    sudoku = Sudoku3D(17)

    converter = SudokuDimecsConverter(sudoku)
    dimecs = converter.convert(smart=False)

    dimecs.get_dimecs(comments=False)
    dimecs.save('/tmp/17')
    dimecs.get_dimecs_mapped(converter.conv, comments=False)

# TestSymbolConverter()
# TestSudokuDimecsConverter()
# TestBigSudokuDimecsConverter()
