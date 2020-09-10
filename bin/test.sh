/home/vagrant/code/gogone/bin/cutechess-cli \
    -wait 2000 \
    -debug \
    -engine \
        name=pygone \
        cmd=pygone \
    -engine \
        name=sf12 \
        cmd=stockfish_20090418_x64 \
        option.Hash=16 \
        option.Contempt=0 \
        option.Threads=1 \
    -each \
        proto=uci \
        tc=inf \
        depth=1 \
        restart=off \
        -openings file=book.pgn \
        -draw movenumber=50 movecount=10 score=0 \
        -resign movecount=10 score=750 \
        -repeat \
        -pgnout games.pgn \
        min -games 2 -rounds 100 > debug.log
