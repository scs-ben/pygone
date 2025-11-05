#!/usr/bin/env pypy3
import sys, time

# TODO
# position startpos moves b2b4 d7d5 c1b2 c8g4 g1f3 g4f3 g2f3 e7e6 b2g7 f8g7 h1g1 e8f8 g1g7 f8g7 f1h3 g7f8 h3e6 b8c6 e6d5 d8d5 b1c3 d5e5 b4b5 c6e7 h2h3 e5f6 d1b1 a8b8 b1b4 h7h5 b4c5 b7b6 c5c7 b8c8 c7a7 f6e6 a1c1 g8f6 c1d1 h8g8 e2e4 c8d8 c3e2 f6d7 a7c7 d8c8 c7f4 f8e8 f4h4 c8c2 h4h5 c2a2 d1c1 d7f6 e2c3 f6h5 c3a2 f7f6 c1c7 h5f4 c7e7 e6e7 d2d4 e7e6 d4d5 e6e5 e1d2 e5d4 d2c2 d4f2 c2b3 f2e3 b3a4 e3g1 a2b4 g1d1
# this set up a position where the King tries to move into check

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
    
    if line.startswith("position"):
        board = Board()
        
        # Strip the "position " prefix
        cmd = line[9:]

        # Default to the starting position if nothing else is provided
        if cmd.startswith("startpos"):
            cmd = cmd[len("startpos"):]
        elif cmd.startswith("fen"):
            # Extract FEN before the "moves" keyword if present
            fen_section = cmd[len("fen "):]
            if " moves " in fen_section:
                fen, moves_section = fen_section.split(" moves ", 1)
            else:
                fen, moves_section = fen_section, ""
            board.set_fen(fen)
            cmd = moves_section
        else:
            moves_section = ""

        # Apply moves if given
        if "moves" in cmd:
            moves_section = cmd.split("moves ", 1)[1]

        if moves_section:
            moves = moves_section.split()
            for move in moves:
                board.uci_move(move)
                
        search.set_board(board)
    elif line.startswith("ucinewgame"):
            board = Board()
            search = Search(board)
    elif line.startswith("uci"):
        print("pygone2.0\nuciok", flush=True)
    elif line.startswith("isready"):
        print("readyok", flush=True)
    elif line.startswith("go "):
        tokens = line.split()
        wtime = btime = movestogo = None
        depth = None
        perft_depth = None

        i = 1
        while i < len(tokens):
            if tokens[i] == "wtime":
                wtime = int(tokens[i+1])
                i += 2
            elif tokens[i] == "btime":
                btime = int(tokens[i+1])
                i += 2
            elif tokens[i] == "movestogo":
                movestogo = int(tokens[i+1])
                i += 2
            elif tokens[i] == "depth":
                depth = int(tokens[i+1])
                i += 2
            elif tokens[i] == "perft":
                perft_depth = int(tokens[i+1])
                i += 2
            else:
                i += 1
              
        if perft_depth:
            perft = Perft(board)
            perft.run(perft_depth)
            continue
              
        search.set_board(board)
          
        if depth:
            search.set_time_limit(1e8)
            search.set_depth(depth)
        else:
            search.set_depth(50)
            side_time = (wtime if board.white_to_move else btime) / 1000
            
            move_time = max(2.2, side_time / 28)
            
            search.set_time_limit(move_time)
            
        move, score = search.iterative_search()
        
        if not move:
            search.set_depth(1)
            move, score = search.iterative_search()
            
        if move:
            print(f"bestmove {board.move_to_uci(move)}", flush=True)
    elif line.startswith('print'):
        board.print_board()
    elif line.startswith('fen'):
        print(board.get_fen(), flush=True)
    # else:
    #     print(f"Unknown command: {line}", flush=True)