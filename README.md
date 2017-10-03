## Overview

sudoku3d_generator: Generate a new sudoku, save it in sudokus (or test_sudokus)
sudoku3d_dimecs_converter: Read a sudoku from a file (in sudokus or test_sudoku), convert to dimecs and save in (test_)sudokus_dimecs
sudoku3d_dimecs_solver: Execute Minisat for file(s), parse results and save in experimental_results

## Installation

First, make sure that *cmake* and *zlib* are installed. Then, run the following command in bash:

```bash
./install
```

## How to use

To run the experiments:

```bash
./run_experiments [-h] [--k K] [--t T] nmin nmax mperc [mperc ...]

Run some experiments on some N*N*N 3D sudokus

positional arguments:
  nmin        Minimum value for N
  nmax        Maximum value for N
  mperc       Set of percentages of filled cells

optional arguments:
  -h, --help  show this help message and exit
  --k K       Number of repetitions for each parameter setting
  --t T       Number of seconds before minisat timeouts
```

To draw a plot of a given variable from a result CSV file:

```bash
./plot [-h] [--ylim-min YLIM_MIN] [--ylim-max YLIM_MAX] filename variable

Draw a plot of a given statistic

positional arguments:
  filename             Filename of the data source
  variable             Variable to put on the y axis

optional arguments:
  -h, --help           show this help message and exit
  --ylim-min YLIM_MIN  Lower bound for the y axis
  --ylim-max YLIM_MAX  Upper bound for the y axis
```

To export the plots as images for every variable from a result CSV file:

```bash
./export_plots filename
```
