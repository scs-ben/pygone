./cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/ben/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=pygone2b \
        cmd=/home/ben/pygone/bin/pygone2b \
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
        -concurrency 2 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
