#!/usr/bin/env pypy3
import sys
from search import Search
from board import Board
from perft import Perft

def print_to_terminal(print_string):
    print(print_string, flush=True)

def main():
    game_board = Board()
    searcher = Search(game_board)

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print_to_terminal("pygone2.0\nuciok")
            elif line == "ucinewgame":
                game_board = Board()
                searcher = Search(game_board)
            elif line == "isready":
                print_to_terminal("readyok")
            elif line.startswith("position fen"):
                cmd = line[9:]
                
                game_board = Board()
                searcher = Search(game_board)
                # Extract FEN before the "moves" keyword if present
                fen_section = cmd[len("fen "):]
                if " moves " in fen_section:
                    fen, moves_section = fen_section.split(" moves ", 1)
                else:
                    fen, moves_section = fen_section, ""
                game_board.set_fen(fen)
                
                cmd = moves_section
                
                for position_move in cmd:
                    from_sq = game_board.algebraic_to_sq(position_move[:2])
                    to_sq = game_board.algebraic_to_sq(position_move[2:4])
                    promo = position_move[4] if len(position_move) == 5 else None
                    
                    game_board.make_move((from_sq, to_sq, promo, None, None))
                
            elif line.startswith("position"):
                moves = line.split()
                
                for position_move in moves[3:]:
                    from_sq = game_board.algebraic_to_sq(position_move[:2])
                    to_sq = game_board.algebraic_to_sq(position_move[2:4])
                    promo = position_move[4] if len(position_move) == 5 else None
                    
                    game_board.make_move((from_sq, to_sq, promo, None, None))
            elif line.startswith("go"):
                move_time = 1e8
                is_white = game_board.white_to_move
                v_depth = 0
                perft_depth = 0
                
                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime' and is_white or arg == 'btime' and not is_white:
                        side_time = int(args[key + 1]) / 1e3
                    # depth input can be commented out to save space since engine will be run on time
                    elif arg == 'depth':
                        v_depth = int(args[key + 1])
                    elif arg == 'perft':
                        perft_depth = int(args[key + 1])

                
                if perft_depth:
                    perft = Perft(game_board)
                    perft.run(perft_depth)
                    continue
                    
                if v_depth > 0:
                    searcher.set_time_limit(1e8)
                    searcher.set_depth(v_depth)
                else:
                    searcher.set_depth(50)
                    
                    move_time = side_time / 20
                    
                    searcher.set_time_limit(move_time)

                t_move, _ = searcher.iterative_search()

                print_to_terminal(f"bestmove {str(game_board.move_to_uci(t_move))}")
            elif line.startswith('print'):
                game_board.print_board()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
