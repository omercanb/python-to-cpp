# benchmarks

These are a collection of benchmarks that were mostly adapted from the mypyc benchmarks at [https://github.com/mypyc/mypyc-benchmarks](https://github.com/mypyc/mypyc-benchmarks). Both the benchmarks and the scripts that are used to benchmark are taken from there. The benchmarks are used to measure performance between python programs, their translations using python-to-cpp, and a handwritten C++ program. These results are tracked to see how close we can come to native C++ performance. 

*Some benchmarks are microbenchmarks that are only useful for finding
big performance differences related to specific operations or language
features. They don't reflect real-world performance.*

## Benchmark results

The benchmarks are collected into `benchmarks.csv`.

The benchmark results are collected along with the commit hash to see what commit has made a difference in performance.

Currently there is no ready way to tabulate or graph the benchmark results.


## Running benchmarks

Run the benchmarks from the root dir using `python -m tests.benchmarks.run_bench <benchmark name>`  

To list all the different benchmarks run `python -m tests.benchmarks.run_bench --list`

For each benchmark, the translated versions will be created automatically. But you should also provide a handwritten C++ version to compare against. This file should be named `hw_benchfile.cpp` where `benchfile` is the name of the corresponding Python benchmark module.

## Documentation

Documentation for specific benchmarks is provided in [./doc/benchmarks.rst](./doc/benchmarks.rst)
