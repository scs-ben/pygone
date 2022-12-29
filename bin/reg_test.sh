/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone153 \
        cmd=/home/vagrant/code/pygone/bin/pygone153 \
        proto=uci \
    -engine \
        name=pygone154 \
        cmd=/home/vagrant/code/pygone/bin/pygone154 \
        proto=uci \
    -each \
        tc=0/1+1 \
        timemargin=1000 \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -games 2 -rounds 200 > debug.log
