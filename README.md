pygone

Created as a way to learn more python and to see how hard it is to build a chess engine.
This engine is created to have a Unix executable binary that is <= 4,096 bytes.

For shell scripts, may need to execute: `sed -i -e 's/\r$//' file.sh` to clean up line endings

To build: `cd src`
`make`

This will produce an executable in `bin`

In `prepare.sh` need to set `NUMBER_OF_LINES` to the length of the binary (around 24 lines). The file needs to have a blank line added at the end to work proplery.

This file needs to be further shrunk by running `bin/prepare.sh`
