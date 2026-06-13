./cutechess-cli \
    -debug \
    -engine \
        name=pygone-latest \
        cmd=/home/ben/pygone/dist/pygone \
        proto=uci \
    -engine \
        name=pygone2 \
        cmd=/home/ben/pygone/historical/pygone2-279d61 \
        proto=uci \
    -each \
        tc=0/30+2 \
        timemargin=10000 \
        restart=on \
        -openings file=balance.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 1 \
        -resign movecount=6 score=2000 \
        -games 2 -rounds 50 > debug.log
