#!/usr/bin/env bash
set -euo pipefail

test_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_dir=$(cd -- "$test_dir/.." && pwd)

cutechess=${CUTECHESS:-"$test_dir/cutechess-cli"}
candidate=${1:-"$repo_dir/dist/pygone"}
baseline=${2:-"$repo_dir/historical/pygone2-fb1ccc"}
rounds=${ROUNDS:-50}
concurrency=${CONCURRENCY:-2}
time_control=${TC:-0/10+0.1}
restart=${RESTART:-on}
max_moves=${MAX_MOVES:-100}
seed=${SEED:-2025}
openings=${OPENINGS:-"$test_dir/balance100.pgn"}
opening_order=${OPENING_ORDER:-sequential}
output_prefix=${OUT_PREFIX:-"$test_dir/regression"}
baseline_nodes=${BASELINE_NODES:-}

for executable in "$cutechess" "$candidate" "$baseline"; do
    if [[ ! -x "$executable" ]]; then
        echo "Not executable: $executable" >&2
        exit 2
    fi
done
if [[ ! -f $openings ]]; then
    echo "Opening suite not found: $openings" >&2
    exit 2
fi

candidate_engine=(-engine name=candidate cmd="$candidate" proto=uci)
baseline_engine=(-engine name=baseline cmd="$baseline" proto=uci)
if [[ -n $baseline_nodes ]]; then
    baseline_engine+=(nodes="$baseline_nodes")
fi

args=(
    "${candidate_engine[@]}"
    "${baseline_engine[@]}"
    -each tc="$time_control" timemargin=10000 restart="$restart"
    -openings file="$openings" order="$opening_order"
    -srand "$seed"
    -repeat
    -pgnout "$output_prefix.pgn" min
    -recover
    -concurrency "$concurrency"
    -maxmoves "$max_moves"
    -resign movecount=6 score=2000
    -games 2
    -rounds "$rounds"
)

if [[ ${DEBUG:-0} == 1 ]]; then
    args=(-debug "${args[@]}")
fi

echo "candidate=$candidate"
echo "baseline=$baseline"
echo "openings=$openings order=$opening_order"
echo "rounds=$rounds concurrency=$concurrency tc=$time_control restart=$restart maxmoves=$max_moves seed=$seed"
if [[ -n $baseline_nodes ]]; then
    echo "baseline_nodes=$baseline_nodes"
fi

"$cutechess" "${args[@]}" 2>&1 | tee "$output_prefix.log"
