/home/vagrant/code/pygone/bin/cutechess-cli \
    -debug \
    -engine \
        name=pygone13 \
        cmd=pygone \
        proto=uci \
    	depth=2 \
    -engine \
        name=sunfish \
        cmd=sunfish/sunfish \
        proto=uci \
	    depth=2 \
    -each \
        tc=inf \
        restart=off \
        -openings file=book.pgn \
        -repeat \
        -pgnout games.pgn min \
        -games 2 -rounds 200 > debug.log
