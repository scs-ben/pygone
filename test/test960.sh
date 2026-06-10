./cutechess-cli \
    -debug \
    -variant fischerandom \
    -engine \
        name=pygone \
        cmd=/home/ben/pygone/dist/pygone-960 \
        proto=uci \
    -engine \
        name=stockfish1000 \
        cmd=/home/ben/pygone/bin/stockfish/stockfish \
        proto=uci \
        nodes=1000 \
    -each \
        tc=0/30+2 \
        timemargin=10000 \
        restart=on \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 2 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 1 > debug.log
