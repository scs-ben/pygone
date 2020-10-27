/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=umax44 \
        cmd=/home/vagrant/code/pygone/bin/umax/umax44 \
        proto=xboard \
    -each \
        tc=0/50+2 \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
