./cutechess-cli \
    -debug \
    -engine \
        name=pygone156 \
        cmd=/home/ben/pygone/bin/pygone156 \
        proto=uci \
    -engine \
        name=stockfish \
        cmd=/home/ben/pygone/bin/stockfish/stockfish \
        proto=uci \
	nodes=100 \
    -each \
        tc=0/20+2 \
        timemargin=10000 \
        restart=on \
        -openings file=book.pgn order=random \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 4 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
