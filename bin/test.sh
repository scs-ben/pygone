/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone12 \
        cmd=pygone \
        proto=uci \
        depth=3 \
    -engine \
        name=sf12 \
        cmd=stockfish_20090418_x64 \
        proto=uci \
        depth=1 \
    -each \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 100 > debug.log
