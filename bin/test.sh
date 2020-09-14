/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
        depth=2 \
    -engine \
        name=sf12 \
        cmd=stockfish_20090418_x64 \
        option.Hash=16 \
        option.Contempt=0 \
        option.Threads=1 \
        depth=1 \
    -each \
        proto=uci \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 100 > debug.log