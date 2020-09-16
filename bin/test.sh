/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
        depth=4 \
    -engine \
        name=Ethereal \
        cmd=ethereal/src/Ethereal \
        option.Hash=16 \
        option.Threads=1 \
        depth=4 \
    -each \
        proto=uci \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 2700 > debug.log
