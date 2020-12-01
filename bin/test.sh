/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=nanochess \
        cmd=/home/vagrant/code/pygone/bin/nanochess/nanochess \
        proto=xboard \
    -each \
        tc=0/1+2 \
        timemargin=1000 \
        restart=on \
        -openings file=book.pgn order=random \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 1 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
