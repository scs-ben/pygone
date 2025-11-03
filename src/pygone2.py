#!/usr/bin/env pypy3
import sys, time

from board2 import Board
from search2 import Search

b2 = Board()
s2 = Search(b2)

# b2.set_fen("r1bqkbnr/pppppppp/8/2N5/8/3n4/PPPPPPPP/RNBQKB1R w KQkq - 0 1")
# b2.uci_move('e2d3')
# b2.print_board()


# moves = b2.generate_pseudo_legal_moves()

# for move in moves:
    # print(b2.move_to_uci(move))
# b2.print_board()
# b2.uci_move('a2a4')
# b2.uci_move('a8a7')
# b2.uci_move('a1a3')
# b2.uci_move('e7e5')
# # b2.uci_move('b8c6')

for depth, move, score in s2.iterative_search():
    if depth >= 5:
        break
    
print(f"{depth} {b2.move_to_uci(move)} {score}")

# b2.move_tuple(move)
# b2.print_board()

# for depth, move, score in s2.iterative_search():
#     if depth >= 3:
#         break
    
# print(f"{depth} {b2.move_to_uci(move)} {score}")

# b2.move_tuple(move)
# b2.print_board()