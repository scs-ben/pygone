./cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/ben/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=stockfish100 \
        cmd=/home/ben/pygone/bin/stockfish/stockfish \
        proto=uci \
	nodes=100 \
    -each \
        tc=0/60+2 \
        timemargin=10000 \
        restart=on \
        -openings file=balance.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 3 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log