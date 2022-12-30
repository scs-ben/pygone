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
        timemargin=1500 \
        -concurrency 8 \
        -resign movecount=4 score=3000 \
        -openings file=book3.pgn \
        -repeat \
        -pgnout games.pgn \
        -recover \
        -wait 1000 \
        -games 2 -rounds 200 > debug.log
