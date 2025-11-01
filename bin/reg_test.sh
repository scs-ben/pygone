./cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/ben/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=pygone156 \
        cmd=/home/ben/pygone/bin/pygone156 \
        proto=uci \
    -each \
        tc=0/1+1 \
        timemargin=1500 \
        -concurrency 4 \
        -resign movecount=4 score=3000 \
        -openings file=book2.pgn \
        -repeat \
        -pgnout games.pgn \
        -recover \
        -wait 1000 \
        -games 2 -rounds 100 > debug.log
