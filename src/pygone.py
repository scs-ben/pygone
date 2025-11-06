#!/usr/bin/env pypy3
import sys
from board import Board
from search import Search
# from perft import Perft

board = Board()
search = Search(board)

for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    if line.lower() in ("stop", "quit"):
        break
    
    if line.startswith("position"):
        board = Board()
        
        # Strip the "position " prefix
        cmd = line[9:]

        # Default to the starting position if nothing else is provided
        if cmd.startswith("startpos"):
            cmd = cmd[len("startpos"):]
        elif cmd.startswith("fen"):
            search = Search(board)
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
            input_moves = moves_section.split()
            for s_move in input_moves:
                board.uci_move(s_move)
                
        search.set_board(board)
    elif line.lower() == "ucinewgame":
            board = Board()
            search = Search(board)
    elif line.lower() == "uci":
        print("pygone2.0\nuciok", flush=True)
    elif line.startswith("isready"):
        print("readyok", flush=True)
    elif line.startswith("go "):
        tokens = line.split()
        w_time = b_time = None
        movestogo = None
        s_depth = None
        perft_depth = None

        i = 1
        while i < len(tokens):
            if tokens[i] == "wtime":
                w_time = int(tokens[i+1])
                i += 2
            elif tokens[i] == "btime":
                b_time = int(tokens[i+1])
                i += 2
            elif tokens[i] == "movestogo":
                movestogo = int(tokens[i+1])
                i += 2
            elif tokens[i] == "depth":
                s_depth = int(tokens[i+1])
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
          
        if s_depth:
            search.set_time_limit(1e8)
            search.set_depth(s_depth)
        else:
            search.set_depth(50)
            side_time = (w_time if board.white_to_move else b_time) / 1000
            
            move_time = max(2.2, side_time / 28)
            
            search.set_time_limit(move_time)
            
        t_move, score = search.iterative_search()
        
        if not t_move:
            search.set_depth(1)
            t_move, score = search.iterative_search()
            
        if t_move:
            print(f"bestmove {board.move_to_uci(t_move)}", flush=True)
    elif line.startswith('print'):
        board.print_board()
    # elif line.startswith('fen'):
    #     print(board.get_fen(), flush=True)
