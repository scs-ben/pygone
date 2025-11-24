pygone v2

Created as a way to learn more python and to see how hard it is to build a chess engine.
This engine is created to have a Unix executable binary that is <= 4,096 bytes.

This is intended to be run on Linux. `python_minifier` is a dependency that should be installed with `pip`. The engine will perform better with `pypy3` but will run fine with `python3`.

The Makefile will strip down the functionality of pygone to bare minimums but if you just run `pypy3 pygone.py` it will have access to more bells and whistles.