import subprocess


class DimecsSolver:

    def __init__(self, directory='../sudokus'):
        self.dir = directory

    def solve_single(self, filename):
        p = subprocess.Popen(['minisat %s/%s %s/%s_out' % (self.dir, filename,
                             self.dir, filename)], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.communicate()
        output = output[0].decode('ascii')
        return DimecsSolverOutputParser(output)

    def solve_multiple(self, filenames):
        for filename in filenames:
            self.solve_single(filename)

    def solve_all_in_dir(self):
        return True


class DimecsSolverOutputParser:

    def __init__(self, output):
        self.raw_output = output


def TestDimecsSolver():
    solvers = DimecsSolver('../test_sudokus_dimecs')
    solvers.solve_single('test1')

# TestDimecsSolver()
