/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=pygone154 \
        cmd=/home/vagrant/code/pygone/bin/pygone154 \
        proto=uci \
    -each \
        tc=0/60+2 \
        timemargin=1500 \
        -concurrency 6 \
        -resign movecount=4 score=3000 \
        -openings file=book3.pgn \
        -repeat \
        -pgnout games.pgn \
        -recover \
        -wait 1000 \
        -games 2 -rounds 100 > debug.log
