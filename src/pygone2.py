#!/usr/bin/env pypy3
import sys, time

from board2 import Board
from search2 import Search
from perft2 import Perft

board = Board()
board.set_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")

for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    if line.lower() in ["quit", "exit"]:
        break
    if line.startswith("position fen "):
        fen = line[len("position fen "):]
        board.set_fen(fen)
        board.print_board()
    elif line.startswith("position startpos "):
        moves = line[len("position startpos ")]
    elif line.startswith("go depth "):
        search = Search(board)
        
        depth = int(line[len("go depth ")])
        for s_depth, move, score in search.iterative_search():
            if s_depth >= depth:
                break
            
        print(f"bestmove {board.move_to_uci(move)}")
    elif line.startswith("go perft "):
        perft = Perft(board)       
        depth = int(line[len("go perft ")])
        perft.run(depth)
    else:
        print(f"Unknown command: {line}", flush=True)