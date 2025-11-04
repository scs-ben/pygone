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
            search.set_depth(depth)
        else:
            side_time = (wtime if board.white_to_move else btime) / 1000
            
            move_time = max(2.2, side_time / 28)
            
            search.set_time_limit(move_time)
            
        move, score = search.iterative_search()
            
        print(f"bestmove {board.move_to_uci(move)}", flush=True)
    elif line.startswith('print'):
        board.print_board()
    elif line.startswith('fen'):
        print(board.get_fen(), flush=True)
    # else:
    #     print(f"Unknown command: {line}", flush=True)