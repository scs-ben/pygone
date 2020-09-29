/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone11 \
        cmd=pygone \
        proto=uci \
    -engine \
        name=sf \
        cmd=stockfish_20090418_x64 \
        proto=uci \
        depth=1 \
    -each \
        tc=0/300+2 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 200 > debug.log
