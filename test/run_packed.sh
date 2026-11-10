#!/usr/bin/env bash
set -euo pipefail

artifact=$1
exec python3 <(tail -n +3 "$artifact" | xz -dc)
