#!/usr/bin/env pypy3
import sys
from search import Search
from board import Board
#remove
from perft import Perft
#endremove

def main():
    game_board = Board()
    searcher = Search(game_board)

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print("pygone2.0\nuciok", flush=True)
            elif line == "ucinewgame":
                game_board = Board()
                searcher = Search(game_board)
            elif line == "isready":
                print("readyok", flush=True)
            #remove
            elif line == "unit":
                b = Board()
                orig_hash = b.hash
                mv = b.gen_legal_moves()[0]   # some legal move
                b.make_move(mv)
                b.unmake_move()

                assert b.hash == orig_hash, "Zobrist mismatch after make/unmake"

                # 2) Compute from scratch vs incremental
                b = Board()
                orig_hash = b.compute_hash()
                # do a sequence of moves
                moves = b.gen_legal_moves()[:4]
                for m in moves:
                    b.make_move(m)
                    b.unmake_move()
                # now compute from scratch and compare
                h_inc = b.hash
                h_scratch = b.compute_hash()
                
                assert h_inc == h_scratch, "Incremental != recompute"
            #endremove
            #remove
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
                    
                    game_board.make_move((from_sq, to_sq, promo, None, None, False))
            #endremove
            elif line.startswith("position"):
                game_board = Board()
                
                moves = line.split()
                
                for position_move in moves[3:]:
                    from_sq = game_board.algebraic_to_sq(position_move[:2])
                    to_sq = game_board.algebraic_to_sq(position_move[2:4])
                    promo = position_move[4] if len(position_move) == 5 else None
                    
                    game_board.make_move((from_sq, to_sq, promo, None, None, False))
                    
                searcher.set_board(game_board)
            elif line.startswith("go"):
                move_time = 1e8
                side_time = 1e8
                is_white = game_board.white_to_move
                #remove
                v_depth = 0
                perft_depth = 0
                #endremove
                
                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime' and is_white or arg == 'btime' and not is_white:
                        side_time = int(args[key + 1]) / 1e3
                    #remove
                    elif arg == 'depth':
                        v_depth = int(args[key + 1])
                    elif arg == 'perft':
                        perft_depth = int(args[key + 1])
                    #endremove
                #remove
                if perft_depth:
                    perft = Perft(game_board)
                    perft.run(perft_depth)
                    continue
                #endremove
                
                #remove
                searcher.set_depth(50)
                #endremove
                    
                move_time = max(2, side_time / 28)
                
                print(f"{side_time} {move_time}")

                searcher.set_time_limit(move_time)
                
                #remove
                if v_depth > 0:
                    searcher.set_time_limit(1e8)
                    searcher.set_depth(v_depth)
                #endremove

                searcher.iterative_search()
            #remove
            elif line.startswith('print'):
                game_board.print_board()
            #endremove
        except Exception as exc:
            print(exc, flush=True)
            raise

main()
