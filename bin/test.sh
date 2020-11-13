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
        tc=0/1+2 \
        timemargin=1000 \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 1 \
        -resign movecount=6 score=800 \
        -games 2 -rounds 10 > debug.log
