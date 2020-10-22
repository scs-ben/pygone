/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone13 \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
        depth=5 \
    -engine \
        name=sunfish \
        cmd=/home/vagrant/code/pygone/bin/sunfish/sunfish \
        proto=uci \
	    depth=5 \
    -each \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -concurrency 6 \
        -games 2 -rounds 200 > debug.log
