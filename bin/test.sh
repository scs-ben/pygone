/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
        depth=4 \
    -engine \
        name=sunfish \
        cmd=sunfish/sunfish \
        depth=4 \
    -each \
        proto=uci \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 1350 > debug.log
