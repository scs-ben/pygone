/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
        depth=4 \
    -engine \
        name=weiss \
        cmd=weiss/src/weiss \
        option.Hash=16 \
        option.Threads=1 \
        depth=1 \
    -each \
        proto=uci \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 2700 > debug.log