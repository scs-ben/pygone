/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone14 \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    -engine \
        name=pygone14baseline \
        cmd=/home/vagrant/code/pygone/bin/pygone14 \
        proto=uci \
    -each \
        tc=0/1+0.5 \
        timemargin=1000 \
        -openings file=book.pgn order=random \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -wait 1000 \
        -concurrency 16 \
        -sprt elo0=30 elo1=30 alpha=50 beta=50 \
        -games 2 -rounds 200 > debug.log
