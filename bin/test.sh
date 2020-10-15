/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone13 \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
        depth=5 \
    -engine \
        name=umax48 \
        cmd=/home/vagrant/code/pygone/bin/umax/umax48 \
        proto=xboard \
        depth=5 \
    -each \
        tc=0/1000+4 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -resign movecount=6 score=800 \
        -concurrency 4 \
        -games 2 -rounds 100 > debug.log
