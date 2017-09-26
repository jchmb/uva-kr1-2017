import subprocess
import pprint
import re
from os import listdir
from os.path import isfile, join


class DimecsSolver:

    def __init__(self, directory='../sudokus'):
        self.dir = directory

    def solve_single(self, filename):
        p = subprocess.Popen(['minisat %s/%s %s/out/%st' % (self.dir, filename,
                             self.dir, filename)], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.communicate()
        output = output[0].decode('ascii')
        return DimecsSolverOutputParser(output)

    def solve_multiple(self, filenames):
        res = []
        for filename in filenames:
            res.append(self.solve_single(filename))

        return res

    def solve_all_in_dir(self):
        files = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]
        return self.solve_multiple(files)


class DimecsSolverOutputParser:

    def __init__(self, output):
        self.reset(output)

    def reset(self, output, parse=True):
        self.raw_output = output
        self.parsed_data = {}

        if(parse):
            self.parse()

    def parse(self):
        self.parsed_data['sat'] = 'UNSATISFIABLE' not in self.raw_output

        find = [('restarts', 'restarts'),
                ('conflicts', 'conflicts'),
                ('decisions', 'decisions'),
                ('conflict literals', 'conflict_literals'),
                ('propagations', 'propagations')]

        for f in find:
            reg, key = f
            res = re.search(reg + r'\s*: (\d*)', self.raw_output)
            self.parsed_data[key] = res.group(1)

        res = re.search(r'CPU time\s*: (.*) s', self.raw_output)
        self.parsed_data['cpu_time'] = res.group(1)

        res = re.search(r'Number of clauses:\s*(\d*)', self.raw_output)
        self.parsed_data['clauses'] = res.group(1)

        res = re.search(r'Number of variables:\s*(\d*)', self.raw_output)
        self.parsed_data['variables'] = res.group(1)

    def __str__(self):
        res = pprint.pformat(self.parsed_data)
        return res


def TestDimecsSolver():
    solvers = DimecsSolver('../test_sudokus_dimecs')

    # res1 = [solvers.solve_single('test')]
    # res1 = solvers.solve_multiple(['simple', 'simple_un'])
    res1 = solvers.solve_all_in_dir()

    for a in res1:
        print(a)

TestDimecsSolver()
