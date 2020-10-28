/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=sunfish \
        cmd=/home/vagrant/code/pygone/bin/sunfish/sunfish \
        proto=xboard \
    -each \
        tc=0/20+2 \
        restart=off \
        -openings file=book.pgn order=random \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 100 > debug.log
