/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone13 \
        cmd=/home/vagrant/code/pygone/bin/pygone \
        proto=uci \
    	depth=3 \
    -engine \
        name=pygone12 \
        cmd=/home/vagrant/code/pygone/bin/pygone12 \
        proto=uci \
	    depth=3 \
    -each \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -recover \
        -concurrency 2 \
        -games 2 -rounds 200 > debug.log
