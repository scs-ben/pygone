pygone v2

Created as a way to learn more python and to see how hard it is to build a chess engine.
This engine is created to have a Unix executable binary that is <= 4,096 bytes.

This is intended to be run on Linux. `python_minifier` is a dependency that should be installed with `pip`. The engine will perform better with `pypy3` but will run fine with `python3`.

The Makefile will strip down the functionality of pygone to bare minimums but if you just run `pypy3 pygone.py` it will have access to more bells and whistles.

Building on Windows (does not result in 4kb compatable file):
`pyinstaller --distpath=dist/pygone_windows --onefile pygone.py`

## Testing

Run correctness and fixed-depth checks from WSL:

```sh
make test
make bench
```

Windows Cute Chess can run paired matches through WSL from PowerShell:

```powershell
# Candidate versus the historical regression baseline (100 games)
.\test\reg_test.ps1 -Mode Regression -Rounds 50 -Concurrency 8

# Earlier second LMR reduction versus the otherwise-identical move-16 build
.\test\reg_test.ps1 -Mode Regression -Rounds 50 -Concurrency 4 `
    -BaselineArtifact .\test\baselines\pygone-lmr15 -Seed 2025

# Candidate versus Stockfish fixed at 1,000 nodes per move (40 games)
.\test\reg_test.ps1 -Mode Stockfish -Rounds 20 -Concurrency 8 -StockfishNodes 1000
```

Each round contains two games with colors reversed and the same opening. The
default opening order is sequential, so 100 rounds exercises every position in
the 100-opening suite once with both colors. Match
logs and PGNs are written to timestamped files under `test/`. Use `-TimeControl`
and `-MaxMoves` to trade test duration for search quality. The default
`test/balance100.pgn` suite contains 100 unique positions filtered to within
120 centipawns by Stockfish. Rebuild it with `test/build_opening_suite.py`, or
pass `-OpeningsFile` to test another PGN. Use `-OpeningOrder random` when you
deliberately want seeded random sampling instead of full-suite coverage.
