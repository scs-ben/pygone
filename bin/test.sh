/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone11 \
        cmd=pygone \
        proto=uci \
    -engine \
        name=nanochess \
        cmd=nanochess/nanochess \
        proto=xboard \
    -each \
        tc=0/300+2 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 200 > debug.log
