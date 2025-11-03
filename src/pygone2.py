#!/usr/bin/env pypy3
import sys, time

from board2 import Board
from search2 import Search
from perft2 import Perft

board = Board()
search = Search(board)

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
    elif line.startswith("uci"):
        print("pygone2.0\nuciok", flush=True)
    elif line.startswith("ucinewgame"):
            board = Board()
            search.set_board(board)
    elif line.startswith("isready"):
        print("readyok", flush=True)
    elif line.startswith("position startpos "):
        board = Board()
        
        moves = line.split()
        for move in moves[3:]:
            board.uci_move(move)
            
        search.set_board(board)
    elif line.startswith("go "):
        search.set_board(board)
        
        depth = 4 # int(line[len("go depth ")])
        for s_depth, move, score in search.iterative_search():
            if s_depth >= depth:
                break
            
        print(f"bestmove {board.move_to_uci(move)}", flush=True)
    elif line.startswith("go perft "):
        perft = Perft(board)       
        depth = int(line[len("go perft ")])
        perft.run(depth)
    elif line.startswith('print'):
        board.print_board()
    elif line.startswith('fen'):
        print(board.get_fen(), flush=True)
    # else:
    #     print(f"Unknown command: {line}", flush=True)