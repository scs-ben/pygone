#!/usr/bin/env pypy3
<<<<<<< HEAD
import gc, math, sys, time
import itertools
import re
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
=======
import copy, math, sys, time

PIECEPOINTS = {'p': 100, 'r': 480, 'n': 280, 'b': 320, 'q': 960, 'k': 6e4}

PPSQT = [[0]*8,
         [78, 83, 86, 73, 102, 82, 85, 90],
         [7, 29, 21, 44, 40, 31, 44, 7],
         [-17, 16, -2, 15, 14, 0, 15, -13],
         [-26, 3, 10, 9, 6, 1, 0, -23],
         [-22, 9, 5, -11, -10, -2, 3, -19],
         [-31, 8, -7, -37, -36, -14, 3, -31],
         [0]*8]
NPSQT = [[-66, -53, -75, -75, -10, -55, -58, -70],
         [-3, -6, 100, -36, 4, 62, -4, -14],
         [10, 67, 1, 74, 73, 27, 62, -2],
         [24, 24, 45, 37, 33, 41, 25, 17],
         [-1, 5, 31, 21, 22, 35, 2, 0],
         [-18, 10, 13, 22, 18, 15, 11, -14],
         [-23, -15, 2, 0, 2, 0, -23, -20],
         [-74, -23, -26, -24, -19, -35, -22, -69]]
BPSQT = [[-59, -78, -82, -76, -23, -107, -37, -50],
         [-11, 20, 35, -42, -39, 31, 2, -22],
         [-9, 39, -32, 41, 52, -10, 28, -14],
         [25, 17, 20, 34, 26, 25, 15, 10],
         [13, 10, 17, 23, 17, 16, 0, 7],
         [14, 25, 24, 15, 8, 25, 20, 15],
         [19, 20, 11, 6, 7, 6, 20, 16],
         [-7, 2, -15, -12, -14, -15, -10, -10]]
RPSQT = [[35, 29, 33, 4, 37, 33, 56, 50],
         [55, 29, 56, 67, 55, 62, 34, 60],
         [19, 35, 28, 33, 45, 27, 25, 15],
         [0, 5, 16, 13, 18, -4, -9, -6],
         [-28, -35, -16, -21, -13, -29, -46, -30],
         [-42, -28, -42, -25, -25, -35, -26, -46],
         [-53, -38, -31, -26, -29, -43, -44, -53],
         [-30, -24, -18, 5, -2, -18, -31, -32]]
QPSQT = [[6, 1, -8, -104, 69, 24, 88, 26],
         [14, 32, 60, -10, 20, 76, 57, 24],
         [-2, 43, 32, 60, 72, 63, 43, 2],
         [1, -16, 22, 17, 25, 20, -13, -6],
         [-14, -15, -2, -5, -1, -10, -20, -22],
         [-30, -6, -13, -11, -16, -11, -16, -27],
         [-36, -18, 0, -19, -15, -15, -21, -38],
         [-39, -30, -31, -13, -31, -36, -34, -42]]
KPSQT = [[4, 54, 47, -99, -99, 60, 83, -62],
         [-32, 10, 45, 56, 56, 55, 10, 3],
         [-62, 12, -57, 44, -67, 28, 37, -31],
         [-55, 50, 11, -4, -19, 13, 0, -49],
         [-55, -43, -52, -28, -51, -47, -8, -50],
         [-47, -42, -43, -79, -64, -32, -29, -32],
         [-4, 3, -14, -50, -57, -18, 13, 4],
         [22, 30, -3, -14, 6, -1, 40, 26]]

ALLPSQT = {'p': PPSQT, 'n': NPSQT, 'b':BPSQT, 'r':RPSQT, 'q':QPSQT, 'k':KPSQT}

WHITE_PIECES = ['P', 'R', 'N', 'B', 'Q', 'K']
BLACK_PIECES = ['p', 'r', 'n', 'b', 'q', 'k']
>>>>>>> master

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)

def number_to_letter(number):
    return chr(number + 96)

def print_to_terminal(letter):
<<<<<<< HEAD
    print(letter, flush=1)
=======
    print(letter, flush=True)
>>>>>>> master

def get_perf_counter():
    return time.perf_counter()

<<<<<<< HEAD
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

class Search:
    nodes = 0
    end_time = 0
    v_depth = 0
    tt_bucket = {}

    def iterative_search(self, position, v_depth, move_time):
        start_time = time.perf_counter()
        self.end_time = time.perf_counter() + move_time

        self.v_depth = 0

        local_score = -1e8
        local_move = None

        while True:
            self.v_depth += 1
            v_depth -= 1

            (iterative_score, iterative_move) = self.first_search(position, self.v_depth)

            local_score = iterative_score
            local_move = mrender(position, iterative_move)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            nps = math.ceil(self.v_nodes / elapsed_time)

            print_to_terminal("info depth " + str(self.v_depth) + " score cp " + str(math.ceil(local_score)) + " time " + str(elapsed_time) + " nodes " + str(self.v_nodes) + " nps " + str(nps) + " pv " + str(local_move))
=======
class Board:
    board_state = []
    played_move_count = 0
    move_list = []
    white_attack_pieces = []
    black_attack_pieces = []
    white_castling = [True, True]
    black_castling = [True, True]

    def reset(self):
        self.set_default_board_state()
        self.played_move_count = 0
        self.move_list = []
        self.white_attack_pieces = []
        self.black_attack_pieces = []
        self.white_castling = [True, True]
        self.black_castling = [True, True]

    def set_default_board_state(self):
        self.board_state = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['P']*8,
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

    def set_board_state(self, state):
        self.board_state = state

    def apply_move(self, uci_coordinate, reverse_promotion=0, reverse_castle=0, override_from_piece='', override_to_piece=''):
        from_letter_number = letter_to_number(uci_coordinate[0:1])
        from_number = abs(int(uci_coordinate[1:2]) - 8)
        to_letter_number = letter_to_number(uci_coordinate[2:3])
        to_number = abs(int(uci_coordinate[3:4]) - 8)
        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]

        is_white = self.played_move_count % 2 == 0

        if len(override_from_piece) > 0:
            from_piece = override_from_piece
        if len(override_to_piece) > 0:
            to_piece = override_to_piece
        if reverse_promotion:
            from_piece = '-'
            to_piece = 'P' if is_white else 'p'
        if reverse_castle:
            rook_offset = 1
            if uci_coordinate[0:1] == 'c':
                rook_offset = -2
                self.board_state[to_number][to_letter_number - 1] = '-'
            else:
                self.board_state[to_number][to_letter_number + 2] = '-'
            self.board_state[from_number][from_letter_number + rook_offset] = 'R' if from_piece == 'K' else 'r'
            self.board_state[to_number][to_letter_number] = 'K' if from_piece == 'K' else 'k'
            self.board_state[to_number][to_letter_number + rook_offset] = '-'
            return [from_piece, to_piece]
        promote = ""
        if len(uci_coordinate) > 4:
            promote = uci_coordinate[4:5]
        if (from_piece in ('P', 'p') and to_piece == '-' and uci_coordinate[0:1] != uci_coordinate[2:3] and len(override_from_piece) == 0 and len(override_to_piece) == 0):
            self.board_state[from_number][from_letter_number] = '-'
            self.board_state[to_number][to_letter_number] = from_piece
            self.board_state[from_number][to_letter_number] = '-'
        elif (from_piece in ('K', 'k') and uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8')):
            self.board_state[from_number][from_letter_number] = '-'
            if uci_coordinate[2] == 'g':
                self.board_state[to_number][to_letter_number + 1] = '-'
                self.board_state[from_number][from_letter_number + 1] = 'R' if from_piece == 'K' else 'r'
            else:
                self.board_state[to_number][to_letter_number - 2] = '-'
                self.board_state[from_number][from_letter_number - 1] = 'R' if from_piece == 'K' else 'r'
            self.board_state[to_number][to_letter_number] = from_piece
        else:
            if len(override_to_piece) == 0:
                self.board_state[from_number][from_letter_number] = '-'
            else:
                self.board_state[from_number][from_letter_number] = override_to_piece
            if promote != "":
                if is_white:
                    self.board_state[to_number][to_letter_number] = promote.upper()
                else:
                    self.board_state[to_number][to_letter_number] = promote
            else:
                if len(override_from_piece) == 0:
                    self.board_state[to_number][to_letter_number] = from_piece
                else:
                    self.board_state[to_number][to_letter_number] = override_from_piece

        return [from_piece, to_piece]

    def make_move(self, uci_coordinate):
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state = [x[:] for x in self.board_state]
        board.white_attack_pieces = self.white_attack_pieces
        board.black_attack_pieces = self.black_attack_pieces
        board.move_list = self.move_list.copy()
        board.white_castling = self.white_castling
        board.black_castling = self.black_castling

        if uci_coordinate is not None:
            if 'e1' in uci_coordinate:
                board.white_castling = [False, False]

            if 'a1' in uci_coordinate:
                board.white_castling[0] = False

            if 'h1' in uci_coordinate:
                board.white_castling[1] = False

            if 'e8' in uci_coordinate:
                board.black_castling = [False, False]

            if 'a8' in uci_coordinate:
                board.black_castling[0] = False

            if 'h8' in uci_coordinate:
                board.black_castling[1] = False

            board.apply_move(uci_coordinate)
            board.move_list.append(uci_coordinate)

        board.played_move_count += 1

        return board

    def str_board(self):
        s_board = ''
        for i in range(8):
            for j in range(8):
                s_board += self.board_state[i][j]
        return s_board + str(self.played_move_count % 2 == 0)

    def get_valid_moves(self):
        is_white = self.played_move_count % 2 == 0

        # Null Move
        yield None

        valid_moves = []
        attack_pieces = []

        if (is_white):
            self.white_attack_pieces = []
        else:
            self.black_attack_pieces = []

        eval_state = self.board_state.copy()
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-" or (is_white and piece in BLACK_PIECES) or (not is_white and piece in WHITE_PIECES):
                    continue
                start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))
                if piece.lower() == 'k':
                    king_moves = {
                        1: {'column': (column + 0), 'row': (row + 1)},
                        2: {'column': (column + 0), 'row': (row - 1)},
                        3: {'column': (column + 1), 'row': (row + 0)},
                        4: {'column': (column - 1), 'row': (row + 0)},
                        5: {'column': (column + 1), 'row': (row + 1)},
                        6: {'column': (column + 1), 'row': (row - 1)},
                        7: {'column': (column - 1), 'row': (row + 1)},
                        8: {'column': (column - 1), 'row': (row - 1)},
                    }
                    if is_white:
                        if self.white_castling[1] and start_coordinate == 'e1' and eval_state[7][5] == '-' and eval_state[7][6] == '-' and eval_state[7][7] == 'R':
                            yield (start_coordinate + 'g1')
                        if self.white_castling[0] and start_coordinate == 'e1' and eval_state[7][1] == '-' and eval_state[7][2] == '-' and eval_state[7][3] == '-' and eval_state[7][0] == 'R':
                            yield (start_coordinate + 'c1')
                    else:
                        if self.black_castling[0] and start_coordinate == 'e8' and eval_state[0][1] == '-' and eval_state[0][2] == '-' and eval_state[0][3] == '-' and eval_state[0][0] == 'r':
                            yield (start_coordinate + 'c8')
                        if self.black_castling[1] and start_coordinate == 'e8' and eval_state[0][5] == '-' and eval_state[0][6] == '-' and eval_state[0][7] == 'r':
                            yield (start_coordinate + 'g8')
                    for _, k_move in king_moves.items():
                        if k_move['column'] in range(8) and k_move['row'] in range(8):
                            eval_piece = eval_state[k_move['row']][k_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())

                            dest = number_to_letter(k_move['column'] + 1) + str(abs(k_move['row'] - 8))

                            if eval_piece == '-' or can_capture:
                                yield (start_coordinate + dest)
                if piece.lower() == 'p':
                    if is_white:
                        if row > 1 and eval_state[row - 1][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)))
                        if row == 6 and eval_state[row - 1][column] == '-' and eval_state[row - 2][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 10)))
                        if row == 1 and eval_state[row - 1][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)) + 'q')
                        if ((column - 1) >= 0 and (row - 1) >= 0) or ((column + 1) < 8 and (row - 1) >= 0):
                            prom = ''
                            if row == 1:
                                prom = 'q'
                            if (column - 1) >= 0 and eval_state[row - 1][column - 1] != '-' and eval_state[row - 1][column - 1].islower():
                                dest = number_to_letter(column) + str(abs(row - 9))
                                attack_pieces.append(eval_state[row - 1][column - 1])
                                yield (start_coordinate + dest + prom)
                            if (column + 1) < 8 and eval_state[row - 1][column + 1] != '-' and eval_state[row - 1][column + 1].islower():
                                dest = number_to_letter(column + 2) + str(abs(row - 9))
                                attack_pieces.append(eval_state[row - 1][column + 1])
                                yield (start_coordinate + dest + prom)
                    else:
                        if row < 6 and eval_state[row + 1][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)))
                        if row == 1 and eval_state[row + 1][column] == '-' and eval_state[row + 2][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 6)))
                        if row == 6 and eval_state[row + 1][column] == '-':
                            yield (start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)) + 'q')
                        if ((column - 1) >= 0 and (row + 1) < 8) or ((column + 1) < 8 and (row + 1) < 8):
                            prom = ''
                            if row == 6:
                                prom = 'q'

                            if (column + 1) < 8 and eval_state[row + 1][column + 1] != '-' and eval_state[row + 1][column + 1].isupper():
                                dest = number_to_letter(column + 2) + str(abs(row - 7))
                                attack_pieces.append(eval_state[row + 1][column + 1])
                                yield (start_coordinate + dest + prom)
                            if (column - 1) >= 0 and eval_state[row + 1][column - 1] != '-' and eval_state[row + 1][column - 1].isupper():
                                dest = number_to_letter(column) + str(abs(row - 7))
                                attack_pieces.append(eval_state[row + 1][column - 1])
                                yield (start_coordinate + dest + prom)
                if piece.lower() == 'n':
                    night_moves = {
                        1: {'column': (column + 1), 'row': (row - 2)},
                        2: {'column': (column - 1), 'row': (row - 2)},
                        3: {'column': (column + 2), 'row': (row - 1)},
                        4: {'column': (column - 2), 'row': (row - 1)},
                        5: {'column': (column + 1), 'row': (row + 2)},
                        6: {'column': (column - 1), 'row': (row + 2)},
                        7: {'column': (column + 2), 'row': (row + 1)},
                        8: {'column': (column - 2), 'row': (row + 1)}
                    }
                    for _, n_move in night_moves.items():
                        if n_move['column'] in range(8) and n_move['row'] in range(8):
                            eval_piece = eval_state[n_move['row']][n_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())
                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
                                yield (start_coordinate + dest)
                                if can_capture:
                                    attack_pieces.append(eval_piece)
                if piece.lower() in ('b', 'r', 'q'):
                    all_moves = {
                        # rook/queen
                        1: {'column': column, 'row': (row - 1), 'colIncrement': 0, 'rowIncrement': -1},
                        2: {'column': column, 'row': (row + 1), 'colIncrement': 0, 'rowIncrement': 1},
                        3: {'column': (column - 1), 'row': row, 'colIncrement': -1, 'rowIncrement': 0},
                        4: {'column': (column + 1), 'row': row, 'colIncrement': 1, 'rowIncrement': 0},
                        # bish/queen
                        5: {'column': (column - 1), 'row': (row - 1), 'colIncrement': -1, 'rowIncrement': -1},
                        6: {'column': (column + 1), 'row': (row + 1), 'colIncrement': 1, 'rowIncrement': 1},
                        7: {'column': (column - 1), 'row': (row + 1), 'colIncrement': -1, 'rowIncrement': 1},
                        8: {'column': (column + 1), 'row': (row - 1), 'colIncrement': 1, 'rowIncrement': -1},
                    }

                    for key, a_move in all_moves.items():
                        if (key <= 4 and piece.lower() == 'b') or (key >= 5 and piece.lower() == 'r'):
                            continue
                        temp_row = a_move['row']
                        temp_col = a_move['column']
                        while temp_row in range(8) and temp_col in range(8):
                            eval_piece = eval_state[temp_row][temp_col]

                            can_capture = (is_white and eval_piece in BLACK_PIECES) or (not is_white and eval_piece in WHITE_PIECES)

                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                yield (start_coordinate + dest)
                                if can_capture:
                                    attack_pieces.append(eval_piece)
                                    break
                            else:
                                break
                            temp_row += a_move['rowIncrement']
                            temp_col += a_move['colIncrement']

    def in_check(self, is_white):
        if is_white:
            return 'K' in self.black_attack_pieces
        else:
            return 'k' in self.white_attack_pieces

    def board_evaluation(self):
        b_eval = 0
        for table in range(64):
            row = math.floor(table / 8)
            column = table % 8
            piece = self.board_state[row][column]
            is_white = piece.isupper()
            if piece != '-':
                if is_white:
                    b_eval += PIECEPOINTS[piece.lower()]
                    b_eval += (ALLPSQT[piece.lower()][row][column] / 50)
                else:
                    b_eval -= PIECEPOINTS[piece]
                    b_eval -= (ALLPSQT[piece][abs(row-7)][abs(column-7)] / 50)

        return b_eval

class Search:
    v_nodes = 0
    v_tthits = 0
    v_depth = 0
    end_time = 0
    tt_bucket = {}

    def reset(self):
        self.v_nodes = 0
        self.v_tthits = 0
        self.tt_bucket = {}

    def iterative_search(self, local_board, v_depth, move_time):
        start_time = get_perf_counter()
        self.end_time = get_perf_counter() + move_time

        alpha = -1e8

        iterative_score = 0
        iterative_move = None

        initial_score = local_board.board_evaluation()

        self.v_depth = 1
        while v_depth > 1:
            self.v_depth += 1
            v_depth -= 1

            (iterative_score, iterative_move) = self.aspiration_window(local_board, self.v_depth, iterative_score)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            v_nps = math.ceil(self.v_nodes / elapsed_time)

            self.print_stats(str(self.v_depth), str(math.ceil(iterative_score)), str(elapsed_time), str(self.v_nodes), str(v_nps), iterative_move)

            # if get_perf_counter() >= self.end_time or v_depth < 1:
            #     break
>>>>>>> master

            if get_perf_counter() >= self.end_time or v_depth < 1:
                break

<<<<<<< HEAD
        return [local_score, local_move]

    def first_search(self, position, depth):
=======
    def print_stats(self, v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
        print_to_terminal("info depth " + v_depth + " score cp " + v_score + " time " + v_time + " nodes " + v_nodes + " nps " + v_nps + " pv " + v_pv)

    def aspiration_window(self, local_board, v_depth, initial_score):
        alpha = -1e8
        beta = 1e8

        delta = 10

        depth = v_depth

        if depth > 3:
            alpha = max(-1e8, initial_score - delta)
            beta = min(1e8, initial_score + delta)

        local_score = -1e8
        local_move = None

        while True:
            (local_score, local_move) = self.search(local_board, depth, alpha, beta)

            if local_score > alpha and local_score < beta:
                print_to_terminal("info nodes " + str(self.v_nodes))

            if local_score > alpha and local_score < beta:
                return [local_score, local_move]

            if local_score <= alpha:
                beta = (alpha + beta) / 2
                alpha = max(-1e8, alpha - delta)
                depth = v_depth
            elif local_score >= beta:
                beta = min(1e8, beta + delta)
                depth = min(1, depth - min(1e8, local_score) / 2)

            # print(alpha, beta, delta, depth)

            delta = delta + delta / 2

    def search(self, local_board, v_depth, alpha, beta):
        global_score = -1e8
        chosen_move = None
>>>>>>> master

        local_score = -1e8

        # alpha = -1e8
        # beta = 1e8

<<<<<<< HEAD
        local_score = -1e8
        best_move = None

        for s_move in sorted(position.gen_moves(), key=position.value, reverse=True):
            self.v_nodes += 1
            temp_score = self.pvs(position.move(s_move), -beta, -alpha, depth)

            print(mrender(position, s_move), temp_score)
=======
        is_white = local_board.played_move_count % 2 == 0

        v_depth = max(v_depth, 1)

        for s_move in local_board.get_valid_moves():
            if s_move is None:
                continue

            self.v_nodes += 1

            local_score = -self.pvs(local_board.make_move(s_move), -beta, -alpha, v_depth - 1)

            if local_score >= global_score:
                global_score = local_score
                chosen_move = s_move
>>>>>>> master

            if temp_score >= local_score:
                local_score = temp_score
                best_move = s_move

<<<<<<< HEAD
        return [local_score, best_move]

    def pvs(self, position, alpha, beta, depth):
        if depth <= 0:
            # if get_color(position):
            return position.score
            # return -position.score

        alpha_orig = alpha

        tt_entry = self.tt_lookup(position)
        if tt_entry['tt_depth'] >= depth:
            if tt_entry['tt_flag'] == EXACT:
                return tt_entry['tt_value']
            elif tt_entry['tt_flag'] == LOWER:
                alpha = max(alpha, tt_entry['tt_value'])
            elif tt_entry['tt_flag'] == UPPER:
                beta = min(beta, tt_entry['tt_value'])

            if alpha >= beta:
=======
    def tt_lookup(self, local_board):
        board_string = local_board.str_board()
        if board_string not in self.tt_bucket:
            self.tt_bucket[board_string] = {
                'tt_depth': 0,
                'tt_value': -1e5,
                'tt_flag': 2
            }

        return self.tt_bucket[board_string]

    def store_tt(self, local_board, tt_entry):
        board_string = local_board.str_board()
        if len(self.tt_bucket) > 1e7:
            self.tt_bucket.clear()
        self.tt_bucket[board_string] = tt_entry

    def pvs(self, local_board, alpha, beta, v_depth):
        is_white = local_board.played_move_count % 2 == 0

        b_eval = local_board.board_evaluation()

        if b_eval >= 5e4:
            return 1e8 if is_white else -1e8
        if v_depth < 1:
            return b_eval if is_white else -b_eval

        alpha_orig = alpha

        tt_entry = self.tt_lookup(local_board)
        if tt_entry['tt_depth'] >= v_depth:
            if tt_entry['tt_flag'] == EXACT:
                self.v_nodes += 1
                return tt_entry['tt_value']
            elif tt_entry['tt_flag'] == LOWER:
                alpha = max(alpha, tt_entry['tt_value'])
            elif tt_entry['tt_flag'] == UPPER:
                beta = min(beta, tt_entry['tt_value'])

            if alpha >= beta:
                self.v_nodes += 1
>>>>>>> master
                return tt_entry['tt_value']

        local_score = -1e8

<<<<<<< HEAD
        for s_move in sorted(position.gen_moves(), key=position.value, reverse=True):
            self.v_nodes += 1
            local_score = -self.pvs(position.move(s_move), -alpha - 1, -alpha, depth - 1)
            if local_score > alpha and local_score < beta:
                local_score = -self.pvs(position.move(s_move), -beta, -local_score, depth - 1)

=======
        for s_move in local_board.get_valid_moves():
            self.v_nodes += 1

            local_score = -self.pvs(local_board.make_move(s_move), -alpha - 1, -alpha, v_depth - 1)
            if local_score > alpha and local_score < beta:
                local_score = -self.pvs(local_board.make_move(s_move), -beta, -local_score, v_depth - 1)

>>>>>>> master
            alpha = max(alpha, local_score)

            if alpha >= beta:
                break

        tt_entry['tt_value'] = alpha
        if alpha <= alpha_orig:
            tt_entry['tt_flag'] = UPPER
        elif alpha >= beta:
            tt_entry['tt_flag'] = LOWER
        else:
            tt_entry['tt_flag'] = EXACT
<<<<<<< HEAD
        tt_entry['tt_depth'] = depth
        self.store_tt(position, tt_entry)

        return alpha

    def tt_lookup(self, position):
        board_string = position.board + str(get_color(position))
        if board_string not in self.tt_bucket:
            self.tt_bucket[board_string] = {
                'tt_depth': 0,
                'tt_value': -1e5,
                'tt_flag': 2
            }
        return self.tt_bucket[board_string]

    def store_tt(self, position, tt_entry):
        board_string = position.board + str(get_color(position))
        if len(self.tt_bucket) > 1e7:
            self.tt_bucket = {}
        self.tt_bucket[board_string] = tt_entry

WHITE = 0
BLACK = 1

UPPER = 1
LOWER = 2
EXACT = 3

MATE_LOWER = piece['K'] - 10*piece['Q']
MATE_UPPER = piece['K'] + 10*piece['Q']

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

def renderFEN(pos, half_move_clock=0, full_move_clock=1):
    color = 'wb'[get_color(pos)]
    if get_color(pos) == BLACK:
        pos = pos.rotate()
    board = '/'.join(pos.board.split())
    board = re.sub(r'\.+', (lambda m: str(len(m.group(0)))), board)
    castling = ''.join(itertools.compress('KQkq', pos.wc[::-1]+pos.bc)) or '-'
    ep = render(pos.ep) if not pos.board[pos.ep].isspace() else '-'
    clock = '{} {}'.format(half_move_clock, full_move_clock)
    return ' '.join((board, color, castling, ep, clock))

def main():
    hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
=======
        tt_entry['tt_depth'] = v_depth
        self.store_tt(local_board, tt_entry)

        return alpha

EXACT=1
UPPER=2
LOWER=3

def main():
>>>>>>> master
    searcher = Search()

    game_board = Board()
    game_board.reset()

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
<<<<<<< HEAD
                print("pygone 1.0 by rcostheta")
                print("uciok")
            elif line == "print":
                print(renderFEN(hist[-1], len(hist), math.ceil(len(hist) / 2)))
            elif line == "ucinewgame":
                hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
                # searcher.reset()
                gc.collect()
=======
                print_to_terminal("pygone 1.0\nuciok")
            elif line == "ucinewgame":
                game_board.reset()
                searcher.reset()
>>>>>>> master
            elif line == "isready":
                print_to_terminal("readyok")
            elif line.startswith("position"):
                color = WHITE
                moves = line.split()
<<<<<<< HEAD
                hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
                for position_move in moves[3:]:
                    hist.append(hist[-1].move(mparse(color, position_move)))
                    color = 1 - color
=======
                game_board.reset()
                for position_move in moves[3:]:
                    game_board = game_board.make_move(position_move)
>>>>>>> master
            elif line.startswith("go"):
                white_time = 1e8
                black_time = 1e8
                go_depth = 8
                input_depth = 0

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    elif arg == 'btime':
                        black_time = int(args[key + 1])
                    elif arg == 'depth':
                        go_depth = int(args[key + 1])
                    elif arg == 'infinite':
                        input_depth = 30

<<<<<<< HEAD
                time_move_calc = max(40 - len(hist), 2)

                time_move_calc = 40
                if len(hist) > 38:
                    time_move_calc = 2
                else:
                    time_move_calc = 40 - len(hist)

                is_white = len(hist) % 2 == 0
=======
                time_move_calc = max(40 - game_board.played_move_count, 2)

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0
>>>>>>> master

                if is_white:
                    move_time = white_time / (time_move_calc * 1e3)
                else:
                    move_time = black_time / (time_move_calc * 1e3)

                if move_time < 15:
                    go_depth = 6
                if move_time < 4:
                    move_time = 2
                    go_depth = 4

                go_depth = max(input_depth, go_depth)

                searcher.v_nodes = 0
                searcher.v_tthits = 0

                (score, s_move) = searcher.iterative_search(game_board, go_depth, move_time)

<<<<<<< HEAD
                searcher.v_nodes = 0
                searcher.v_tthits = 0
                start_time = get_perf_counter()
                (score, s_move) = searcher.iterative_search(hist[-1], go_depth, move_time)
=======
                (score, s_move) = searcher.search(game_board, go_depth, score - 10, score + 10)

>>>>>>> master
                print_to_terminal("bestmove " + s_move)
        except (KeyboardInterrupt, SystemExit):
            print_to_terminal('quit')
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
