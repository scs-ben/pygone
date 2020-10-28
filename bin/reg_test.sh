/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone14 \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=pygone13 \
        cmd=/home/vagrant/code/pygone/bin/pygone13 \
        proto=uci \
    -each \
        tc=0/1+0.5 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -concurrency 1 \
        -games 2 -rounds 200 > debug.log
