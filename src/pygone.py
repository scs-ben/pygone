#!/usr/bin/env pypy3
import gc, math, sys, time
from itertools import count
from collections import namedtuple

piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }
pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}
# Pad tables and join piece and pst dictionaries
for k, table in pst.items():
    padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
    pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
    pst[k] = (0,)*20 + pst[k] + (0,)*20

# Lists of possible moves for each piece type.
N, E, S, W = -10, 1, 10, -1
directions = {
    'P': (N, N+N, N+W, N+E),
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'B': (N+E, S+E, S+W, N+W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
    'K': (N, E, S, W, N+E, S+E, S+W, N+W)
}

# Mate value must be greater than 8*queen + 2*(rook+knight+bishop)
# King value is set to twice this value such that if the opponent is
# 8 queens up, but we got the king, we still exceed MATE_VALUE.
# When a MATE is detected, we'll set the score to MATE_UPPER - plies to get there
# E.g. Mate in 3 will be MATE_UPPER - 6
MATE_LOWER = piece['K'] - 10*piece['Q']
MATE_UPPER = piece['K'] + 10*piece['Q']

###############################################################################
# Global constants
###############################################################################

# Our board is represented as a 120 character string. The padding allows for
# fast detection of moves that don't stay within the board.
A1, H1, A8, H8 = 91, 98, 21, 28
initial = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' rnbqkbnr\n'  #  20 - 29
    ' pppppppp\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
)

WHITE_PIECES = ['P', 'R', 'N', 'B', 'Q', 'K']
BLACK_PIECES = ['p', 'r', 'n', 'b', 'q', 'k']

TTEXACT = 1
TTLOWER = 2
TTUPPER = 3

isupper = lambda c: 'A' <= c <= 'Z'
islower = lambda c: 'a' <= c <= 'z'

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)

def number_to_letter(number):
    return chr(number + 96)

def print_to_terminal(letter):
    print(letter, flush=1)

def get_perf_counter():
    return time.perf_counter()

class Position(namedtuple('Position', 'board score wc bc ep kp')):
    """ A state of a chess game
    board -- a 120 char representation of the board
    score -- the board evaluation
    wc -- the castling rights, [west/queen side, east/king side]
    bc -- the opponent castling rights, [west/king side, east/queen side]
    ep - the en passant square
    kp - the king passant square
    """

    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if not p.isupper(): continue
            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board, and off friendly pieces
                    if q.isspace() or q.isupper(): break
                    # Pawn move, double move and capture
                    if p == 'P' and d in (N, N+N) and q != '.': break
                    if p == 'P' and d == N+N and (i < A1+N or self.board[i+N] != '.'): break
                    if p == 'P' and d in (N+W, N+E) and q == '.' \
                            and j not in (self.ep, self.kp, self.kp-1, self.kp+1): break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding, and sliding after captures
                    if p in 'PNK' or q.islower(): break
                    # Castling, by sliding the rook next to the king
                    if i == A1 and self.board[j+E] == 'K' and self.wc[0]: yield (j+E, j+W)
                    if i == H1 and self.board[j+W] == 'K' and self.wc[1]: yield (j+W, j+E)

    def rotate(self):
        ''' Rotates the board, preserving enpassant '''
        return Position(
            self.board[::-1].swapcase(), -self.score, self.bc, self.wc,
            119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        return Position(
            self.board[::-1].swapcase(), -self.score,
            self.bc, self.wc, 0, 0)

    def move(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        # Copy variables and reset ep and kp
        board = self.board
        wc, bc, ep, kp = self.wc, self.bc, 0, 0
        score = self.score + self.value(move)
        # Actual move
        board = put(board, j, board[i])
        board = put(board, i, '.')
        # Castling rights, we move the rook or capture the opponent's
        if i == A1: wc = (False, wc[1])
        if i == H1: wc = (wc[0], False)
        if j == A8: bc = (bc[0], False)
        if j == H8: bc = (False, bc[1])
        # Castling
        if p == 'K':
            wc = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                board = put(board, A1 if j < i else H1, '.')
                board = put(board, kp, 'R')
        # Pawn promotion, double move and en passant capture
        if p == 'P':
            if A8 <= j <= H8:
                board = put(board, j, 'Q')
            if j - i == 2*N:
                ep = i + N
            if j == self.ep:
                board = put(board, j+S, '.')
        # We rotate the returned position, so it's ready for the next player
        return Position(board, score, wc, bc, ep, kp).rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        # Actual move
        score = pst[p][j] - pst[p][i]
        # Capture
        if q.islower():
            score += pst[q.upper()][119-j]
        # Castling check detection
        if abs(j-self.kp) < 2:
            score += pst['K'][119-j]
        # Castling
        if p == 'K' and abs(i-j) == 2:
            score += pst['R'][(i+j)//2]
            score -= pst['R'][A1 if j < i else H1]
        # Special pawn stuff
        if p == 'P':
            if A8 <= j <= H8:
                score += pst['Q'][j] - pst['P'][j]
            if j == self.ep:
                score += pst['P'][119-(j+S)]
        return score

# class Board:
#     board_state = []
#     played_move_count = 0
#     white_valid_moves = []
#     black_valid_moves = []
#     white_attack_locations = ''
#     black_attack_locations = ''
#     white_king_location = 'e1'
#     black_king_location = 'e8'
#     move_list_pieces = []
#     move_list = []

#     def reset(self):
#         self.set_default_board_state()
#         self.played_move_count = 0
#         self.white_valid_moves = []
#         self.black_valid_moves = []
#         self.white_attack_pieces = []
#         self.black_attack_pieces = []
#         self.white_attack_locations = ''
#         self.black_attack_locations = ''
#         self.white_king_location = 'e1'
#         self.black_king_location = 'e8'
#         self.move_list_pieces = []
#         self.move_list = []

#     def set_default_board_state(self):
#         self.board_state = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
#                             ['p']*8,
#                             ['-']*8,
#                             ['-']*8,
#                             ['-']*8,
#                             ['-']*8,
#                             ['P']*8,
#                             ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

#     def set_board_state(self, state):
#         self.board_state = state

#     def apply_move(self, uci_coordinate, reverse_promotion=0, reverse_castle=0, override_from_piece='', override_to_piece=''):
#         from_letter_number = letter_to_number(uci_coordinate[0:1])
#         from_number = abs(int(uci_coordinate[1:2]) - 8)
#         to_letter_number = letter_to_number(uci_coordinate[2:3])
#         to_number = abs(int(uci_coordinate[3:4]) - 8)
#         from_piece = self.board_state[from_number][from_letter_number]
#         to_piece = self.board_state[to_number][to_letter_number]

#         is_white = self.played_move_count % 2 == 0

#         if len(override_from_piece) > 0:
#             from_piece = override_from_piece
#         if len(override_to_piece) > 0:
#             to_piece = override_to_piece
#         if reverse_promotion:
#             from_piece = '-'
#             to_piece = 'P' if is_white else 'p'
#         if reverse_castle:
#             rook_offset = 1
#             if uci_coordinate[0:1] == 'c':
#                 rook_offset = -2
#                 self.board_state[to_number][to_letter_number - 1] = '-'
#             else:
#                 self.board_state[to_number][to_letter_number + 2] = '-'
#             self.board_state[from_number][from_letter_number + rook_offset] = 'R' if from_piece == 'K' else 'r'
#             self.board_state[to_number][to_letter_number] = 'K' if from_piece == 'K' else 'k'
#             self.board_state[to_number][to_letter_number + rook_offset] = '-'
#             return [from_piece, to_piece]
#         promote = ""
#         if len(uci_coordinate) > 4:
#             promote = uci_coordinate[4:5]
#         if (from_piece in ('P', 'p') and to_piece == '-' and uci_coordinate[0:1] != uci_coordinate[2:3] and len(override_from_piece) == 0 and len(override_to_piece) == 0):
#             self.board_state[from_number][from_letter_number] = '-'
#             self.board_state[to_number][to_letter_number] = from_piece
#             self.board_state[from_number][to_letter_number] = '-'
#         elif (from_piece in ('K', 'k') and uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8')):
#             self.board_state[from_number][from_letter_number] = '-'
#             if uci_coordinate[2] == 'g':
#                 self.board_state[to_number][to_letter_number + 1] = '-'
#                 self.board_state[from_number][from_letter_number + 1] = 'R' if from_piece == 'K' else 'r'
#             else:
#                 self.board_state[to_number][to_letter_number - 2] = '-'
#                 self.board_state[from_number][from_letter_number - 1] = 'R' if from_piece == 'K' else 'r'
#             self.board_state[to_number][to_letter_number] = from_piece
#         else:
#             if len(override_to_piece) == 0:
#                 self.board_state[from_number][from_letter_number] = '-'
#             else:
#                 self.board_state[from_number][from_letter_number] = override_to_piece
#             if promote != "":
#                 if is_white:
#                     self.board_state[to_number][to_letter_number] = promote.upper()
#                 else:
#                     self.board_state[to_number][to_letter_number] = promote
#             else:
#                 if len(override_from_piece) == 0:
#                     self.board_state[to_number][to_letter_number] = from_piece
#                 else:
#                     self.board_state[to_number][to_letter_number] = override_from_piece

#         return [from_piece, to_piece]

#     def make_move(self, uci_coordinate):
#         (from_piece, to_piece) = self.apply_move(uci_coordinate)
#         self.move_list.append(uci_coordinate)
#         self.move_list_pieces.append([uci_coordinate, from_piece, to_piece])
#         self.played_move_count += 1
#         self.get_valid_moves()

#     def undo_move(self):
#         self.move_list.pop()
#         old_move = self.move_list_pieces.pop()
#         uci_coordinate = old_move[0]
#         from_piece = old_move[1]
#         to_piece = old_move[2]

#         reverse_castle = uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8') and from_piece in ('K', 'k')

#         self.played_move_count -= 1
#         self.apply_move(uci_coordinate[2:4] + uci_coordinate[0:2], len(uci_coordinate) > 4, reverse_castle, from_piece, to_piece)

#     #def show_board(self):
#     #    for i in range(8):
#     #        for j in range(8):
#     #            print(self.board_state[i][j], end=" ")
#     #        print()

#     def str_board(self):
#         s_board = ''
#         for i in range(8):
#             for j in range(8):
#                 s_board += self.board_state[i][j]
#         return hash(s_board + str(self.played_move_count % 2 == 0))

#     def get_valid_moves(self):
#         is_white = self.played_move_count % 2 == 0

#         valid_moves = []
#         attack_pieces = []
#         attack_locations = ''

#         if (is_white):
#             self.white_valid_moves = []
#             self.white_attack_pieces = []
#             self.white_attack_locations = ''
#         else:
#             self.black_valid_moves = []
#             self.black_attack_pieces = []
#             self.black_attack_locations = ''

#         eval_state = self.board_state

#         direction = -1 if is_white else 1
#         start_row = 6 if is_white else 1
#         end_row = 1 if is_white else 6
#         case_eval = 0 if is_white else 1
#         side_attack_pieces = BLACK_PIECES if is_white else WHITE_PIECES

#         for row in range(8):
#             for column in range(8):
#                 piece = eval_state[row][column]
#                 if piece == "-":
#                     continue
#                 if (is_white and piece in BLACK_PIECES) or (not is_white and piece in WHITE_PIECES):
#                     continue
#                 start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))
#                 if piece.lower() == 'k':
#                     king_moves = {
#                         1: {'column': (column + 0), 'row': (row + 1)},
#                         2: {'column': (column + 0), 'row': (row - 1)},
#                         3: {'column': (column + 1), 'row': (row + 0)},
#                         4: {'column': (column - 1), 'row': (row + 0)},
#                         5: {'column': (column + 1), 'row': (row + 1)},
#                         6: {'column': (column + 1), 'row': (row - 1)},
#                         7: {'column': (column - 1), 'row': (row + 1)},
#                         8: {'column': (column - 1), 'row': (row - 1)},
#                     }
#                     if is_white:
#                         self.white_king_location = start_coordinate
#                         if start_coordinate == 'e1' and eval_state[7][5] == '-' and eval_state[7][6] == '-' and eval_state[7][7] == 'R':
#                             valid_moves.append(start_coordinate + 'g1')
#                         if start_coordinate == 'e1' and eval_state[7][1] == '-' and eval_state[7][2] == '-' and eval_state[7][3] == '-' and eval_state[7][0] == 'R':
#                             valid_moves.append(start_coordinate + 'c1')
#                     else:
#                         self.black_king_location = start_coordinate
#                         if start_coordinate == 'e8' and eval_state[0][1] == '-' and eval_state[0][2] == '-' and eval_state[0][3] == '-' and eval_state[0][0] == 'r':
#                             valid_moves.append(start_coordinate + 'c8')
#                         if start_coordinate == 'e8' and eval_state[0][5] == '-' and eval_state[0][6] == '-' and eval_state[0][7] == 'r':
#                             valid_moves.append(start_coordinate + 'g8')
#                     for _, k_move in king_moves.items():
#                         if k_move['column'] in range(8) and k_move['row'] in range(8):
#                             eval_piece = eval_state[k_move['row']][k_move['column']]

#                             can_capture = eval_piece in side_attack_pieces

#                             dest = number_to_letter(k_move['column'] + 1) + str(abs(k_move['row'] - 8))

#                             if eval_piece == '-' or can_capture:
#                                 valid_moves.append(start_coordinate + dest)
#                                 if can_capture:
#                                     attack_pieces.append([eval_piece, piece, start_coordinate + dest])
#                                     attack_locations += dest
#                 elif piece.lower() == 'p' and row not in (0,7):
#                     prom = ''
#                     if row != end_row:
#                         # can pawn advance 1 time
#                         if eval_state[row + direction][column] == '-':
#                             dest = number_to_letter(column + 1) + str(abs(row - 8 + direction))
#                             valid_moves.append(start_coordinate + dest)
#                         if row == start_row:
#                             # can pawn advance 2 times?
#                             if eval_state[row + 2 * direction][column] == '-':
#                                 dest = number_to_letter(column + 1) + str(abs(row - 8 + 2 * direction))
#                                 valid_moves.append(start_coordinate + dest)
#                     else:
#                         prom = 'q'

#                     if column > 0:
#                         # attack location 1
#                         attack_piece = eval_state[row + direction][column - 1]
#                         if attack_piece != '-' and attack_piece.islower() == case_eval:
#                             dest = number_to_letter(column) + str(abs(row - 8 + direction))
#                             valid_moves.append(start_coordinate + dest + prom)
#                             attack_locations += dest
#                             attack_pieces.append([attack_piece, piece, start_coordinate + dest + prom])

#                     if column < 7:
#                         # attack location 2
#                         attack_piece = eval_state[row + direction][column + 1]
#                         if attack_piece != '-' and attack_piece.islower() == case_eval:
#                             dest = number_to_letter(column + 2) + str(abs(row - 8 + direction))
#                             valid_moves.append(start_coordinate + dest + prom)
#                             attack_locations += dest
#                             attack_pieces.append([attack_piece, piece, start_coordinate + dest + prom])
#                 elif piece.lower() == 'n':
#                     night_moves = {
#                         1: {'column': (column + 1), 'row': (row - 2)},
#                         2: {'column': (column - 1), 'row': (row - 2)},
#                         3: {'column': (column + 2), 'row': (row - 1)},
#                         4: {'column': (column - 2), 'row': (row - 1)},
#                         5: {'column': (column + 1), 'row': (row + 2)},
#                         6: {'column': (column - 1), 'row': (row + 2)},
#                         7: {'column': (column + 2), 'row': (row + 1)},
#                         8: {'column': (column - 2), 'row': (row + 1)}
#                     }
#                     for _, n_move in night_moves.items():
#                         if n_move['column'] in range(8) and n_move['row'] in range(8):
#                             eval_piece = eval_state[n_move['row']][n_move['column']]

#                             can_capture = eval_piece in side_attack_pieces

#                             if eval_piece == '-' or can_capture:
#                                 dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
#                                 valid_moves.append(start_coordinate + dest)
#                                 if can_capture:
#                                     attack_locations += dest
#                                     attack_pieces.append([eval_piece, piece, start_coordinate + dest])
#                 elif piece.lower() in ('b', 'r', 'q'):
#                     all_moves = {
#                         # rook/queen
#                         1: {'column': column, 'row': (row - 1), 'colIncrement': 0, 'rowIncrement': -1},
#                         2: {'column': column, 'row': (row + 1), 'colIncrement': 0, 'rowIncrement': 1},
#                         3: {'column': (column - 1), 'row': row, 'colIncrement': -1, 'rowIncrement': 0},
#                         4: {'column': (column + 1), 'row': row, 'colIncrement': 1, 'rowIncrement': 0},
#                         # bish/queen
#                         5: {'column': (column - 1), 'row': (row - 1), 'colIncrement': -1, 'rowIncrement': -1},
#                         6: {'column': (column + 1), 'row': (row + 1), 'colIncrement': 1, 'rowIncrement': 1},
#                         7: {'column': (column - 1), 'row': (row + 1), 'colIncrement': -1, 'rowIncrement': 1},
#                         8: {'column': (column + 1), 'row': (row - 1), 'colIncrement': 1, 'rowIncrement': -1},
#                     }

#                     for key, a_move in all_moves.items():
#                         if (key <= 4 and piece.lower() == 'b') or (key >= 5 and piece.lower() == 'r'):
#                             continue
#                         temp_row = a_move['row']
#                         temp_col = a_move['column']
#                         while temp_row in range(8) and temp_col in range(8):
#                             eval_piece = eval_state[temp_row][temp_col]

#                             can_capture = eval_piece in side_attack_pieces

#                             if eval_piece == '-' or can_capture:
#                                 dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
#                                 valid_moves.append(start_coordinate + dest)
#                                 if can_capture:
#                                     attack_locations += dest
#                                     attack_pieces.append([eval_piece, piece, start_coordinate + dest])
#                                     break
#                             else:
#                                 break
#                             temp_row += a_move['rowIncrement']
#                             temp_col += a_move['colIncrement']

#         if (is_white):
#             self.white_valid_moves = valid_moves
#             self.white_attack_locations = attack_locations
#             self.white_attack_pieces = attack_pieces
#         else:
#             self.black_valid_moves = valid_moves
#             self.black_attack_locations = attack_locations
#             self.black_attack_pieces = attack_pieces

#         if is_white:
#             if 'e1g1' in self.white_valid_moves:
#                 move_string = ''.join(self.move_list)
#                 check_string = ''.join(self.black_valid_moves)
#                 if 'e1' in move_string or 'h1' in move_string or 'e1' in check_string or 'f1' in check_string or 'g1' in check_string:
#                     self.white_valid_moves.remove('e1g1')
#             if 'e1c1' in self.white_valid_moves:
#                 move_string = ''.join(self.move_list)
#                 check_string = ''.join(self.black_valid_moves)
#                 if 'e1' in move_string or 'a1' in move_string or 'c1' in check_string or 'd1' in check_string or 'e1' in check_string:
#                     self.white_valid_moves.remove('e1c1')
#         else:
#             if 'e8g8' in self.black_valid_moves:
#                 move_string = ''.join(self.move_list)
#                 check_string = ''.join(self.white_valid_moves)
#                 if 'e8' in move_string or 'h8' in move_string or 'e8' in check_string or 'f8' in check_string or 'g8' in check_string:
#                     self.black_valid_moves.remove('e8g8')
#             if 'e8c8' in self.black_valid_moves:
#                 move_string = ''.join(self.move_list)
#                 check_string = ''.join(self.white_valid_moves)
#                 if 'e8' in move_string or 'a8' in move_string or 'c8' in check_string or 'd8' in check_string or 'e8' in check_string:
#                     self.black_valid_moves.remove('e8c8')

#     def in_check(self, is_white):
#         if is_white:
#             check_pieces = self.black_attack_pieces
#         else:
#             check_pieces = self.white_attack_pieces

#         for (attacked, attacker, _) in check_pieces:
#             if is_white and attacked == 'K' or not is_white and attacked == 'k':
#                 return 1
#         return 0

#     def get_side_moves(self, is_white):
#         if is_white:
#             return self.white_valid_moves

#         return self.black_valid_moves

#     def board_evaluation(self):
#         b_eval = 0
#         for row in range(8):
#             for column in range(8):
#                 piece = self.board_state[row][column]
#                 if piece != '-':
#                     is_white = piece.isupper()
#                     if is_white:
#                         b_eval += PIECEPOINTS[piece.lower()] + (ALLPSQT[piece.lower()][row][column] / 50)
#                     else:
#                         b_eval -= PIECEPOINTS[piece] - (ALLPSQT[piece][abs(row-7)][abs(column-7)] / 50)

#         return b_eval

class Search:
    nodes = 0
    depth = 0
    end_time = 0

    def iterative_search(self, local_board, depth, move_time):
        start_time = time.perf_counter()
        self.end_time = time.perf_counter() + move_time

        self.depth = 0
        while True:
            self.depth += 1
            depth -= 1

            (iterative_score, iterative_move) = self.search(local_board, self.depth)

            elapsed_time = math.ceil(time.perf_counter() - start_time)
            nps = math.ceil(self.nodes / elapsed_time)
            print("info depth " + str(self.depth) + " score cp " + str(math.ceil(iterative_score)) + " time " + str(elapsed_time) + " nodes " + str(self.nodes) + " nps " + str(nps) + " pv " + str(iterative_move))

            str_move = mrender(local_board[-1], iterative_move)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            nps = math.ceil(self.v_nodes / elapsed_time)

            print_to_terminal("info depth " + str(self.v_depth) + " score cp " + str(math.ceil(iterative_score)) + " time " + str(elapsed_time) + " nodes " + str(self.v_nodes) + " nps " + str(nps) + " pv " + str_move)

            if get_perf_counter() >= self.end_time or v_depth < 1:
                break

        return [iterative_score, str_move]

    def search(self, local_board, depth):
        is_white = local_board.played_move_count % 2 == 0

        global_score = -1e8
        chosen_move = None

        alpha = -1e8
        beta = 1e8

        # is_white = local_board.played_move_count % 2 == 0
        # local_board.get_valid_moves()
        # poss_mvs = local_board.get_side_moves(is_white)
        position = local_board[-1]

        v_depth = max(v_depth, 1)

        for s_move in position.gen_moves():
            self.v_nodes += 1

            # local_board.make_move(s_move)
            # if not local_board.in_check(is_white):
            local_score = -self.negamax(position.move(s_move), -beta, -alpha, v_depth - 1)

            if local_score >= global_score:
                global_score = local_score
                chosen_move = s_move

            alpha = max(alpha, global_score)

            # local_board.undo_move()

        return [global_score, chosen_move]

    def tt_lookup(self, local_board):
        board_string = local_board.board + str(get_color(local_board))
        if board_string not in self.tt_bucket:
            self.tt_bucket[board_string] = {
                'tt_depth': 0,
                'tt_value': -1e5,
                'tt_flag': 2
            }

    def negamax(self, local_board, alpha, beta, depth):
        original_alpha = alpha

    def store_tt(self, local_board, tt_entry):
        board_string = local_board.board + str(get_color(local_board))
        if len(self.tt_bucket) > 1e7:
            self.tt_bucket = {}
        self.tt_bucket[board_string] = tt_entry

    def negamax(self, local_board, alpha, beta, v_depth):
        # is_white = local_board.played_move_count % 2 == 0

        alpa_orig = alpha

        # poss_mvs = local_board[-1].gen_moves()

        tt_entry = self.tt_lookup(local_board)
        if tt_entry['tt_depth'] >= v_depth:
            self.v_tthits += 1
            if tt_entry['tt_flag'] == 1:
                return tt_entry['tt_value']
            elif tt_entry['tt_flag'] == 2:
                alpha = max(alpha, tt_entry['tt_value'])
            elif tt_entry['tt_flag'] == 3:
                beta = min(beta, tt_entry['tt_value'])

            if alpha >= beta:
                return tt_entry['tt_value']

        # local_board.get_valid_moves()
        # poss_mvs = local_board.get_side_moves(is_white)

        if v_depth <= 0:
            return local_board.score
            # b_eval = local_board.board_evaluation()
            # return b_eval if is_white else -b_eval

        value = -1e8

        for move in poss_mvs:
            local_board.make_move(move)
            local_board.get_valid_moves()

        for s_move in local_board.gen_moves():
            # local_board.make_move(s_move)

            # if not local_board.in_check(is_white):
            self.v_nodes += 1

            # local_score = -self.negamax(local_board.move(s_move), -b, -alpha, v_depth - 1)
            # if local_score > alpha and local_score < beta and v_depth > 1:
            local_score = -self.negamax(local_board.move(s_move), -beta, -alpha, v_depth - 1)

            alpha = max(local_score, alpha)

            if self.v_nodes % 1e5 == 0:
                print_to_terminal("info nodes " + str(self.v_nodes) + " tthits " + str(self.v_tthits))

            # local_board.undo_move()

            if alpha >= beta:
                break

        return value

        tt_entry['tt_value'] = alpha
        if alpha <= alpa_orig:
            tt_entry['tt_flag'] = 3
        elif alpha >= beta:
            tt_entry['tt_flag'] = 2
        else:
            tt_entry['tt_flag'] = 1
        tt_entry['tt_depth'] = v_depth
        self.store_tt(local_board, tt_entry)

        return alpha

# game_board = Board()
# game_board.reset()

WHITE = 0
BLACK = 1

gc.enable()

def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank

def mparse(color, move):
    m = (parse(move[0:2]), parse(move[2:4]))
    return m if color == WHITE else (119-m[0], 119-m[1])

def render(i):
    rank, fil = divmod(i - A1, 10)
    return chr(fil + ord('a')) + str(-rank + 1)

def mrender(pos, m):
    # Sunfish always assumes promotion to queen
    p = 'q' if A8 <= m[1] <= H8 and pos.board[m[0]] == 'P' else ''
    m = m if get_color(pos) == WHITE else (119-m[0], 119-m[1])
    return render(m[0]) + render(m[1]) + p

def get_color(pos):
    ''' A slightly hacky way to to get the color from a sunfish position '''
    return BLACK if pos.board.startswith('\n') else WHITE

def main():
    hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
    searcher = Search()

    while True:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print("pygone 1.0 by rcostheta")
                print("uciok")
            elif line == "ucinewgame":
                hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
                searcher.reset()
                gc.collect()
            elif line == "isready":
                print("readyok")
            elif line.startswith("position"):
                color = 0
                moves = line.split()
                hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
                for position_move in moves[3:]:
                    hist.append(hist[-1].move(mparse(color, position_move)))
                    color = not color
            elif line.startswith("go"):
                white_time = 1000000
                black_time = 1000000
                go_depth = 8

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    if arg == 'btime':
                        black_time = int(args[key + 1])
                    if arg == 'depth':
                      go_depth = int(args[key + 1])

                time_move_calc = max(40 - len(hist), 2)

                time_move_calc = 40
                if game_board.played_move_count > 38:
                    time_move_calc = 2
                else:
                    time_move_calc = 40 - game_board.played_move_count

                is_white = len(hist) % 2 == 0

                if is_white:
                    move_time = white_time / (time_move_calc * 1e3)
                else:
                    move_time = black_time / (time_move_calc * 1000)

                move_time -= 3

                if move_time < 8:
                    move_time = 8

                if move_time < 10 and go_depth > 4:
                    go_depth = 4

                searcher.v_nodes = 0
                searcher.v_tthits = 0
                start_time = get_perf_counter()
                (score, s_move) = searcher.iterative_search(hist, go_depth, move_time)
                print_to_terminal("bestmove " + s_move)
        except (KeyboardInterrupt, SystemExit):
            print('quit')
            sys.exit()
        except Exception as exc:
            print(exc)
            raise

main()
