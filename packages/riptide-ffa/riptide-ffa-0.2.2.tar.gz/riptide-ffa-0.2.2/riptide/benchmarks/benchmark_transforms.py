import argparse

import numpy as np
from numpy import log2
import pandas

from riptide.libcpp import *


def complexity(rows, cols):
    return rows * log2(rows) * cols


def benchmark(rows, cols, expected_runtime=1.0, expected_flops=4.0e9):
    cpx = complexity(rows, cols)
    loops = int(expected_runtime / (cpx / expected_flops))
    loops = max(loops, 3)
    tseq = benchmark_ffa2(rows, cols, loops)
    tpar = benchmark_ffa2_parallel(rows, cols, loops)
    gflops_seq = cpx / tseq / 1e9
    gflops_par = cpx / tpar / 1e9
    speedup = tseq / tpar
    result = {
        'rows': rows,
        'cols': cols,
        'kb': rows * cols * 4 / 1024.0,
        'loops': loops,
        'tseq': tseq,
        'tpar': tpar,
        'gflops_seq': gflops_seq,
        'gflops_par': gflops_par,
        'speedup': speedup
    }
    print(result)
    return result


def parse_args():
    def csv_file(arg):
        if not isinstance(arg, str) or not arg.endswith('.csv'):
            raise TypeError("")
        return arg
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', help='CSV file name in which to save the results', type=csv_file)
    return parser.parse_args()


def main():
    args = parse_args()
    pandas.set_option('display.max_rows', 1000)

    expected_flops = 4.0e9
    expected_runtime = 0.80 # seconds

    rows_min = 16
    rows_max = 8192
    cols_min = 256
    cols_max = 8192
    size_max = 8192 * 8192

    grid_rows = 2 ** np.arange(int(log2(rows_min)), int(log2(rows_max)) + 1)
    grid_cols = 2 ** np.arange(int(log2(cols_min)), int(log2(cols_max)) + 1)
    grid_cols = np.concatenate([grid_cols, grid_cols * 1.5])
    grid_cols = grid_cols[grid_cols <= cols_max]
    grid_cols = np.sort(grid_cols).astype(int)

    print(f"Rows: {grid_rows}")
    print(f"Cols: {grid_cols}")

    results = [
        benchmark(rows, cols, expected_runtime, expected_flops)
        for rows in grid_rows
        for cols in grid_cols
        if rows * cols <= size_max
    ]

    results = pandas.DataFrame(results)
    results = results.sort_values('gflops_par', ascending=False)
    print(results)

    results.to_csv(args.outfile, index=False)


if __name__ == "__main__":
    main()