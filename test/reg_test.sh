./cutechess-cli \
    -debug \
    -engine \
        name=pygone-latest \
        cmd=/home/ben/pygone/dist/pygone \
        proto=uci \
    -engine \
        name=pygone2 \
        cmd=/home/ben/pygone/historical/pygone2-11b142 \
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
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
