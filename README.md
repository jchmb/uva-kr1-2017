
Execute MiniSat, parse output.
 ./MiniSat_v1.14_linux sudoku.cnf sudoku.cnf_out | grep ':' | sed 's/.*: //' | cut -d ' ' -f 1

