import subprocess
import pprint
import re
from os import listdir
from os.path import isfile, join
from sudoku3d_dimecs_converter import SudokuDimecsConverter

class DimecsSolver:

    def __init__(self, directory='../sudokus'):
        self.dir = directory
        self.minisat_binary = '../externals/minisat/minisat_core'

    def solve_single(self, filename):
        p = subprocess.Popen(['%s %s/%s %s/out/%s' % (self.minisat_binary, self.dir, filename,
                             self.dir, filename)], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.communicate()
        output = output[0].decode('ascii')
        return DimecsSolverOutputParser(filename, output)

    def solve_multiple(self, filenames):
        res = []
        for filename in filenames:
            res.append(self.solve_single(filename))

        return res

    def solve_all_in_dir(self):
        files = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]
        return self.solve_multiple(files)

    def apply_solution(self, sudoku, filename):
        return


class DimecsSolverOutputParser:

    def __init__(self, name, output):
        self.reset(name, output)

    def reset(self, name, output, parse=True):
        self.raw_output = output
        self.name = name
        self.parsed_data = {}

        if(parse):
            self.parse()

    def parse(self):
        #print(self.raw_output)
        self.parsed_data['sat'] = 'UNSATISFIABLE' not in self.raw_output

        find = [('restarts', 'restarts'),
                ('conflicts', 'conflicts'),
                ('decisions', 'decisions'),
                ('conflict literals', 'conflict_literals'),
                ('propagations', 'propagations')]

        for f in find:
            reg, key = f
            res = re.search(reg + r'\s*: (\d*)', self.raw_output)
            self.parsed_data[key] = int(res.group(1))

        res = re.search(r'CPU time\s*: (.*) s', self.raw_output)
        self.parsed_data['cpu_time'] = float(res.group(1))

        res = re.search(r'Number of clauses:\s*(\d*)', self.raw_output)
        self.parsed_data['clauses'] = int(res.group(1))

        res = re.search(r'Number of variables:\s*(\d*)', self.raw_output)
        self.parsed_data['variables'] = int(res.group(1))

    def __str__(self):
        res = self.name
        res += pprint.pformat(self.parsed_data)
        return res


def TestDimecsSolver():
    solvers = DimecsSolver('../test_sudokus_dimecs')

    test = solvers.solve_single('test')
    testUnsat = solvers.solve_single('simple_un')
    testSat = solvers.solve_single('simple')

    assert testSat.parsed_data['sat'] is True
    assert testUnsat.parsed_data['sat'] is False
    assert test.parsed_data['sat'] is True
    assert test.parsed_data['clauses'] == 44061
    assert test.parsed_data['propagations'] == 1310689
    assert test.parsed_data['restarts'] == 15


# TestDimecsSolver()
