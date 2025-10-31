#!/usr/bin/env pypy3
import sys, time
from search import Search
from board import Board

def print_to_terminal(print_string):
    print(print_string, flush=True)

# def fen_to_board_state(fen):
#     # Convert FEN into your engine's 120-square board representation.
#     # Returns the board_state string and metadata (side, castling, ep).
#     parts = fen.split()
#     placement, side, castling, ep = parts[0], parts[1], parts[2], parts[3]

#     # build 120-square board with sentinels (-1 border)
#     board = [' '] * 120
#     rows = placement.split('/')

#     # The top of the board is rank 8 → index 21
#     for rank_idx, row in enumerate(rows):
#         file_idx = 0
#         rank_start = 21 + rank_idx * 10
#         for ch in row:
#             if ch.isdigit():
#                 file_idx += int(ch)
#             else:
#                 board[rank_start + file_idx] = ch
#                 file_idx += 1

#     # Fill sentinels (outer border with '.')
#     for i in range(120):
#         if i < 20 or i >= 100 or i % 10 in (0, 9):
#             board[i] = '.'
#         elif board[i] == ' ':
#             board[i] = '-'

#     board_state = ''.join(board)
#     return board_state, side, castling, ep

def main():
    game_board = Board()
    searcher = Search()

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print_to_terminal("pygone 1.6.5\nuciok")
            elif line == "ucinewgame":
                game_board = Board()
                searcher.reset()
            elif line == "isready":
                print_to_terminal("readyok")
            # elif line.startswith("position fen"):
            #     parts = line.split() 
            #     fen = " ".join(parts[2:])
                
            #     game_board.board_state, side, castling, ep = fen_to_board_state(fen)
            #     game_board.en_passant = ep if ep != '-' else None
            #     game_board.white_to_move = (side == 'w')
            #     game_board.played_move_count = 0 if game_board.white_to_move else 1

            #     # if you track castling rights as [KQ, kq]
            #     game_board.white_castling = ['K' in castling, 'Q' in castling]
            #     game_board.black_castling = ['k' in castling, 'q' in castling]
                
            # elif line.startswith("print"):
            #     for row in range(12):
            #         position = row * 10
            #         print(game_board.board_state[position:position+10])
            #     print(game_board.played_move_count, game_board.in_check(game_board.played_move_count % 2 == 0))
            elif line.startswith("position"):
                moves = line.split()
                game_board = Board()
                for position_move in moves[3:]:
                    game_board = game_board.make_move(position_move)
            elif line.startswith("go"):
                searcher.v_depth = 30
                move_time = 1e8
                is_white = game_board.played_move_count % 2 == 0

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime' and is_white or arg == 'btime' and not is_white:
                        move_time = int(args[key + 1]) / 1e3
                    # depth input can be commented out to save space since engine will be run on time
                    elif arg == 'depth':
                        searcher.v_depth = int(args[key + 1])

                searcher.critical_time = time.time() + max(0.75, move_time - 1)
                move_time = max(2.2, move_time / 28)

                searcher.end_time = time.time() + move_time
                
                searcher.critical_time = min(searcher.end_time, searcher.critical_time)
                
                searcher.v_nodes = 0

                s_move = None

                for v_depth, s_move, best_score in searcher.iterative_search(game_board):
                    if v_depth >= searcher.v_depth or time.time() >= searcher.end_time:
                        break

                print_to_terminal(f"bestmove {str(s_move)}")

        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
