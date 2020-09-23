/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
    -engine \
        name=sunfish \
        cmd=./sunfish/sunfish \
    -each \
        proto=uci \
        tc=0/300+2 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 50 > debug.log
