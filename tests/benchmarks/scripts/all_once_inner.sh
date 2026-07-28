#!/bin/bash

set -eux

base=/srv

commit="$1"

source $base/venv/bin/activate

cd $base/mypyc-benchmarks

for benchmark in $(python runbench.py --list --raw); do
    python -m reporting.collect "$benchmark" $base/mypy $base/mypyc-benchmark-results "$commit~1" "$commit"
done

echo "<< success >>"
echo
echo "NOTE: The results must be committed manually."
