/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
        depth=3 \
    -engine \
        name=sunfish \
        cmd=./sunfish/sunfish \
        depth=3 \
    -each \
        proto=uci \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 50 > debug.log
