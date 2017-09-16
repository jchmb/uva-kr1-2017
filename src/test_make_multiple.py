import time
from sudoku3d_generator import Sudoku3DGenerator

print('%s\t%s\t%s\t%s\t%s' % ('size', 'k', 'ratio', 'tries', 'exectime'))

max_tries = 4000
for size in range(3, 10):
    for percentage in [.2, .3, .4, .5, .6, .7, .8, .9]:
        cells = size ** 3
        k = round(cells * percentage)
        ratio = k / cells

        start_time = time.time()
        gen = Sudoku3DGenerator(k, size)

        sudoku, tries = gen.generate(max_tries)

        if sudoku is None:
            tries = str(max_tries) + '+'

        exectime = time.time() - start_time

        print('%d\t%d\t%.2f\t%s\t%f' % (size, k, ratio, str(tries), exectime))
