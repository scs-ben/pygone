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

                print("Check hash")
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

                print("Perft")
                b = Board()
                perft = Perft(b)
                results = perft.run(1, True)
                assert results == (1, 20, 0, 0)
                results = perft.run(2, True)
                assert results == (2, 400, 0, 0)
                results = perft.run(3, True)
                assert results == (3, 8902, 34, 12)
                results = perft.run(4, True)
                assert results == (4, 197281, 1576, 469)

                b = Board()
                b.set_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ")
                
                perft = Perft(b)
                results = perft.run(1, True)
                assert results == (1, 48, 8, 0)
                results = perft.run(2, True)
                assert results == (2, 2039, 351, 3)
                results = perft.run(3, True)
                assert results == (3, 97862, 17102, 993)

                def parse_move(mv):
                    b = Board()
                    from_sq = b.algebraic_to_sq(mv[:2])
                    to_sq = b.algebraic_to_sq(mv[2:4])

                    return (from_sq, to_sq, None, None, None, False)

                print("Check moves")
                # 3) Board State Integrity Check
                b = Board()
                b.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                orig_fen = b.get_fen() # Assuming you have a get_fen() method

                # Simple non-capture move
                mv = parse_move("e2e4") 
                b.make_move(mv)
                b.unmake_move()

                assert b.get_fen() == orig_fen, "Board FEN mismatch after quiet make/unmake"

                # Test a capture move
                b.set_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
                orig_fen = b.get_fen()
                mv = parse_move("g8f6") # Test a non-capture
                b.make_move(mv)
                b.unmake_move()
                assert b.get_fen() == orig_fen, "Board FEN mismatch after capture make/unmake"

                print('Scoring')
                # 4) Basic Evaluation Consistency
                b = Board()
                b.set_fen("8/8/8/8/8/8/8/R7 w - - 0 1") # Rook vs no pieces
                score_r = b.eval_position()

                b.set_fen("8/8/8/8/8/8/8/N7 w - - 0 1") # Knight vs no pieces
                score_n = b.eval_position()

                # A Rook is worth more than a Knight
                assert score_r > score_n, "Material scoring error: Rook should be worth more than Knight"

                # Check symmetry (White score should be -Black score)
                b.set_fen("r7/8/8/8/8/8/8/8 w - - 0 1") # Black Rook vs no pieces
                score_br = b.eval_position()
                assert score_r + score_br == 0, "Evaluation is not symmetrical"

                print ("Unit complete")
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
