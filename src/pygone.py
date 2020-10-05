#!/usr/bin/env pypy3
import math, sys, time
<<<<<<< HEAD
from itertools import chain
=======
import gc
from itertools import chain
from collections import namedtuple
>>>>>>> master

PIECEPOINTS = {'pe': 100, 'p': 90, 'r': 500, 'n': 320, 'b': 330, 'q': 900, 'k': 2e4, 'ke': 2e4}

ALLPSQT = {
<<<<<<< HEAD
    'p': (0, 0, 0, 0, 0, 0, 0, 0,
          78, 83, 86, 73, 102, 82, 85, 90,
          7, 29, 21, 44, 40, 31, 44, 7,
          -17, 16, -2, 15, 14, 0, 15, -13,
          -26, 3, 10, 9, 6, 1, 0, -23,
          -22, 9, 5, -11, -10, -2, 3, -19,
          -31, 8, -7, -37, -36, -14, 3, -31,
          0, 0, 0, 0, 0, 0, 0, 0),
    'n': (-66, -53, -75, -75, -10, -55, -58, -70,
          -3, -6, 100, -36, 4, 62, -4, -14,
          10, 67, 1, 74, 73, 27, 62, -2,
          24, 24, 45, 37, 33, 41, 25, 17,
          -1, 5, 31, 21, 22, 35, 2, 0,
          -18, 10, 13, 22, 18, 15, 11, -14,
          -23, -15, 2, 0, 2, 0, -23, -20,
          -74, -23, -26, -24, -19, -35, -22, -69),
    'b': (-59, -78, -82, -76, -23, -107, -37, -50,
          -11, 20, 35, -42, -39, 31, 2, -22,
          -9, 39, -32, 41, 52, -10, 28, -14,
          25, 17, 20, 34, 26, 25, 15, 10,
          13, 10, 17, 23, 17, 16, 0, 7,
          14, 25, 24, 15, 8, 25, 20, 15,
          19, 20, 11, 6, 7, 6, 20, 16,
          -7, 2, -15, -12, -14, -15, -10, -10),
    'r': (35, 29, 33, 4, 37, 33, 56, 50,
          55, 29, 56, 67, 55, 62, 34, 60,
          19, 35, 28, 33, 45, 27, 25, 15,
          0, 5, 16, 13, 18, -4, -9, -6,
          -28, -35, -16, -21, -13, -29, -46, -30,
          -42, -28, -42, -25, -25, -35, -26, -46,
          -53, -38, -31, -26, -29, -43, -44, -53,
          -30, -24, -18, 5, -2, -18, -31, -32),
    'q': (6, 1, -8, -104, 69, 24, 88, 26,
          14, 32, 60, -10, 20, 76, 57, 24,
          -2, 43, 32, 60, 72, 63, 43, 2,
          1, -16, 22, 17, 25, 20, -13, -6,
          -14, -15, -2, -5, -1, -10, -20, -22,
          -30, -6, -13, -11, -16, -11, -16, -27,
          -36, -18, 0, -19, -15, -15, -21, -38,
          -39, -30, -31, -13, -31, -36, -34, -42),
    'k': (4, 54, 47, -99, -99, 60, 83, -62,
          -32, 10, 45, 56, 56, 55, 10, 3,
          -62, 12, -57, 44, -67, 28, 37, -31,
          -55, 50, 11, -4, -19, 13, 0, -49,
          -55, -43, -52, -28, -51, -47, -8, -50,
          -47, -42, -43, -79, -64, -32, -29, -32,
          -4, 3, -14, -50, -57, -18, 13, 4,
          22, 30, -3, -14, 6, -1, 40, 2)
}

# Pad tables and join piece and pst dictionaries
for set_piece, set_table in ALLPSQT.items():
    padrow = lambda row: (0,) + tuple(x+PIECEPOINTS[set_piece] for x in row) + (0,)
    ALLPSQT[set_piece] = sum((padrow(set_table[i*8:i*8+8]) for i in range(8)), ())
    ALLPSQT[set_piece] = (0,)*20 + ALLPSQT[set_piece] + (0,)*20
=======
    'p': [[0, 0, 0, 0, 0, 0, 0, 0],
          [50, 50, 50, 50, 50, 50, 50, 50],
          [10, 10, 20, 30, 30, 20, 10, 10],
          [5, 5, 10, 25, 25, 10, 5, 5],
          [0, 0, 0, 20, 20, 0, 0, 0],
          [5, -5, -10, 0, 0, -10, -5, 5],
          [5, 10, 10, -20, -20, 10, 10, 5],
          [0, 0, 0, 0, 0, 0, 0, 0]],
    'pe': [[0, 0, 0, 0, 0, 0, 0, 0],
           [50, 50, 50, 50, 50, 50, 50, 50],
           [10, 10, 20, 30, 30, 20, 10, 10],
           [5, 5, 10, 25, 25, 10, 5, 5],
           [5, 5, 10, 25, 25, 10, 5, 5],
           [5, 5, 10, 25, 25, 10, 5, 5],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]],
    'n': [[-50, -40, -30, -30, -30, -30, -40, -50],
          [-40, -20, 0, 0, 0, 0, -20, -40],
          [-30, 0, 10, 15, 15, 10, 0, -30],
          [-30, 5, 15, 20, 20, 15, 5, -30],
          [-30, 0, 15, 20, 20, 15, 0, -30],
          [-30, 5, 10, 15, 15, 10, 5, -30],
          [-40, -20, 0, 5, 5, 0, -20, -40],
          [-50, -40, -30, -30, -30, -30, -40, -50]],
    'b': [[-20, -10, -10, -10, -10, -10, -10, -20],
          [-10, 0, 0, 0, 0, 0, 0, -10],
          [-10, 0, 5, 10, 10, 5, 0, -10],
          [-10, 5, 5, 10, 10, 5, 5, -10],
          [-10, 0, 10, 10, 10, 10, 0, -10],
          [-10, 10, 10, 10, 10, 10, 10, -10],
          [-10, 5, 0, 0, 0, 0, 5, -10],
          [-20, -10, -10, -10, -10, -10, -10, -20]],
    'r': [[0, 0, 0, 0, 0, 0, 0, 0],
          [5, 10, 10, 10, 10, 10, 10, 5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [0, 0, 0, 5, 5, 0, 0, 0]],
    'q': [[-20, -10, -10, -5, -5, -10, -10, -20],
          [-10, 0, 0, 0, 0, 0, 0, -10],
          [-10, 0, 5, 5, 5, 5, 0, -10],
          [-5, 0, 5, 5, 5, 5, 0, -5],
          [0, 0, 5, 5, 5, 5, 0, -5],
          [-10, 5, 5, 5, 5, 5, 0, -10],
          [-10, 0, 5, 0, 0, 0, 0, -10],
          [-20, -10, -10, -5, -5, -10, -10, -20]],
    'k': [[-30, -40, -40, -50, -50, -40, -40, -30],
          [-30, -40, -40, -50, -50, -40, -40, -30],
          [-30, -40, -40, -50, -50, -40, -40, -30],
          [-30, -40, -40, -50, -50, -40, -40, -30],
          [-20, -30, -30, -40, -40, -30, -30, -20],
          [-10, -20, -20, -20, -20, -20, -20, -10],
          [20, 20, -10, -10, -10, -10, 20, 20],
          [20, 30, 10, 0, 0, 10, 30, 20]],
    'ke': [[-50, -40, -30, -20, -20, -30, -40, -50],
           [-30, -20, -10, 0, 0, -10, -20, -30],
           [-30, -10, 20, 30, 30, 20, -10, -30],
           [-30, -10, 30, 40, 40, 30, -10, -30],
           [-30, -10, 30, 40, 40, 30, -10, -30],
           [-30, -10, 20, 30, 30, 20, -10, -30],
           [-30, -30, 0, 0, 0, 0, -30, -30],
           [-50, -30, -30, -30, -30, -30, -30, -50]]
}

for set_piece, _ in ALLPSQT.items():
    for set_row in range(8):
        for set_column in range(8):
            ALLPSQT[set_piece][set_row][set_column] += PIECEPOINTS[set_piece]
>>>>>>> master

WHITE_PIECES = ['P', 'R', 'N', 'B', 'Q', 'K']
BLACK_PIECES = ['p', 'r', 'n', 'b', 'q', 'k']

EXACT = 1
UPPER = 2
LOWER = 3

MATE_LOWER = PIECEPOINTS['k'] - 10*PIECEPOINTS['q']
MATE_UPPER = PIECEPOINTS['k'] + 10*PIECEPOINTS['q']
<<<<<<< HEAD

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)
=======
>>>>>>> master

def number_to_letter(number):
    return chr(number + 96)

def print_to_terminal(letter):
    print(letter, flush=True)

def print_stats(v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
    print_to_terminal("info depth " + v_depth + " score cp " + v_score + " time " + v_time + " nodes " + v_nodes + " nps " + v_nps + " pv " + v_pv)

def unpack_coordinate(uci_coordinate):
    return (abs((ord(uci_coordinate[0:1]) - 96) - 1),
            abs(int(uci_coordinate[1:2]) - 8),
            abs((ord(uci_coordinate[2:3]) - 96) - 1),
            abs(int(uci_coordinate[3:4]) - 8))

class Board:
    # represent the board state as it is
    board_state = ''
    played_move_count = 0
    move_list = []
<<<<<<< HEAD
    valid_moves = [[],[]]
    capture_moves = []
    attack_squares = [[],[]]
=======
    repetitions = []
    valid_moves = []
    attack_squares = [[], []]
>>>>>>> master
    white_castling = [True, True]
    black_castling = [True, True]
    white_king_position = 'e1'
    black_king_position = 'e8'
    rolling_score = 0
    en_passant = ''

    def __init__(self):
<<<<<<< HEAD
        self.board_state = ('          '
                            '          '
                            ' rnbqkbnr '
                            ' pppppppp '
                            ' -------- '
                            ' -------- '
                            ' -------- '
                            ' -------- '
                            ' PPPPPPPP '
                            ' RNBQKBNR '
                            '          '
                            '          ')
=======
        self.board_state = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['P']*8,
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        # self.generate_valid_moves()
>>>>>>> master

    def set_board_state(self, board_state):
        self.board_state = board_state

    def apply_move(self, uci_coordinate):
<<<<<<< HEAD
=======
        # break uci coordinate into location in board state list
        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        from_piece = self.board_state[from_number][from_letter_number]
>>>>>>> master

        put = lambda board, i, p: board[:i] + p + board[i+1:]

        # break uci coordinate into location in board state list
        from_number = self.from_coordinate(uci_coordinate[0:2])
        to_number = self.from_coordinate(uci_coordinate[2:4])

<<<<<<< HEAD
        from_piece = self.board_state[from_number]
=======
        set_en_passant = False

        if from_piece in ('P', 'p'):
            set_en_passant = abs(from_number - to_number) == 2
            en_passant_offset = -1 if is_white else 1
            if set_en_passant:
                self.en_passant = uci_coordinate[0:1] + str(int(uci_coordinate[3:4]) + en_passant_offset)
            elif uci_coordinate[2:4] == self.en_passant:
                self.board_state[to_number - en_passant_offset][to_letter_number] = '-'

        if not set_en_passant:
            self.en_passant = ''

        if from_piece in ('K', 'k'):
            if from_piece == 'K':
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            if uci_coordinate in ('e1g1', 'e8g8'):
                self.board_state[to_number][to_letter_number + 1] = '-'
                self.board_state[from_number][from_letter_number + 1] = 'R' if from_piece == 'K' else 'r'
            elif uci_coordinate in ('e1c1', 'e8c8'):
                self.board_state[to_number][to_letter_number - 2] = '-'
                self.board_state[from_number][from_letter_number - 1] = 'R' if from_piece == 'K' else 'r'
        elif len(uci_coordinate) > 4:
            self.board_state[to_number][to_letter_number] = uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5]

    def make_move(self, uci_coordinate):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state = [x[:] for x in self.board_state]
        board.valid_moves = self.valid_moves.copy()
        # board.capture_moves = self.capture_moves.copy()
        board.attack_squares = [x[:] for x in self.attack_squares]
        board.move_list = self.move_list.copy()
        board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        board.white_king_position = self.white_king_position
        board.black_king_position = self.black_king_position
        board.en_passant = self.en_passant
        # should calc score before moving
        board.rolling_score = self.rolling_score + self.calculate_score(uci_coordinate)

        # set castling rights
        if 'e1' in uci_coordinate:
            board.white_castling = [False, False]
>>>>>>> master

        if 'a1' in uci_coordinate:
            board.white_castling[0] = False

<<<<<<< HEAD
        self.board_state = put(self.board_state, to_number, from_piece)
        self.board_state = put(self.board_state, from_number, '-')

        set_en_passant = False

        if from_piece in ('P', 'p'):
            set_en_passant = abs(from_number - to_number) == 2
            en_passant_offset = -1 if is_white else 1
            if set_en_passant:
                self.en_passant = uci_coordinate[0:1] + str(int(uci_coordinate[3:4]) + en_passant_offset)
            elif uci_coordinate[2:4] == self.en_passant:
                self.board_state = put(self.board_state, to_number - en_passant_offset, '-')

        if not set_en_passant:
            self.en_passant = ''

        if from_piece in ('K', 'k'):
            if from_piece == 'K':
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            if uci_coordinate in ('e1g1', 'e8g8'):
                self.board_state = put(self.board_state, to_number + 1, '-')
                self.board_state = put(self.board_state, from_number + 1, 'R' if from_piece == 'K' else 'r')
            elif uci_coordinate in ('e1c1', 'e8c8'):
                self.board_state = put(self.board_state, to_number - 2, '-')
                self.board_state = put(self.board_state, from_number - 1, 'R' if from_piece == 'K' else 'r')
        elif len(uci_coordinate) > 4:
            self.board_state = put(self.board_state, to_number, uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5])



    def make_move(self, uci_coordinate, calculate_next=False):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state = self.board_state
        board.valid_moves = [x[:] for x in self.valid_moves]
        board.capture_moves = self.capture_moves.copy()
        board.attack_squares = [x[:] for x in self.attack_squares]
        board.move_list = self.move_list.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        board.white_king_position = self.white_king_position
        board.black_king_position = self.black_king_position
        board.en_passant = self.en_passant
        # should calc score before moving
        board.rolling_score = self.rolling_score + self.calculate_score(uci_coordinate)

        # set castling rights
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

        board.get_valid_moves()
=======
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

        board.repetitions.append(board.str_board())

        board.rolling_score = -board.rolling_score

        return board

    def nullmove(self):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count + 1
        board.board_state = [x[:] for x in self.board_state]
        # board.valid_moves = self.valid_moves.copy()
        # board.capture_moves = self.capture_moves.copy()
        # board.attack_squares = [x[:] for x in self.attack_squares]
        # board.move_list = self.move_list.copy()
        # board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        # clear positions and ep for nullmove
        board.white_king_position = ''
        board.black_king_position = ''
        board.en_passant = ''
        board.rolling_score = -self.rolling_score

        return board

    def get_piece_count(self):
        return 64 - (self.str_board()).count('-')

    def calculate_score(self, uci_coordinate):
        is_white = self.played_move_count % 2 == 0
        offset = 0 if is_white else 7

        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        local_score = 0

        from_piece = self.board_state[from_number][from_letter_number]
        from_score_piece = from_piece.lower()
        if self.get_piece_count() <= 14:
            if from_piece.lower() == 'k':
                # credit king or pawn moves in end game
                local_score += 2
                from_score_piece = 'ke'
            if from_piece.lower() == 'p':
                # credit king or pawn moves in end game
                local_score += 2
                from_score_piece = 'pe'

        to_piece = self.board_state[to_number][to_letter_number]
>>>>>>> master

        local_score += ALLPSQT[from_score_piece][abs(to_number - offset)][to_letter_number] - ALLPSQT[from_score_piece][abs(from_number - offset)][from_letter_number]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece.lower()][abs(to_number - offset)][to_letter_number]

        if from_piece in ('K', 'k'):
            if abs(from_number - to_number) == 2:
                if uci_coordinate[2] == 'g':
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 1] - ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1]
                else:
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1] - ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 2]
        elif from_piece in ('P', 'p'):
            p_offset = -1 if is_white else 1
            p_piece = 'P' if is_white else 'p'

            protected_pawns = 0

            if to_number > 0 and to_number < 7:
                if to_letter_number > 0:
                    protected_pawns += self.board_state[to_number + p_offset][to_letter_number - 1] == p_piece
                if to_letter_number < 7:
                    protected_pawns += self.board_state[to_number + p_offset][to_letter_number + 1] == p_piece

            if protected_pawns > 0:
                local_score += 10

            if uci_coordinate[2:4] == self.en_passant:
                # add in an extra pawn for EP capture
                local_score += ALLPSQT[from_score_piece][abs(to_number - offset)][to_letter_number]

        if len(uci_coordinate) > 4:
            # adjust value for promoting from pawn to queen
            local_score += ALLPSQT['q'][abs(to_number - offset)][to_letter_number] - ALLPSQT['p'][abs(to_number - offset)][to_letter_number]

        return local_score

    def nullmove(self):
        board = Board()
        board.played_move_count = self.played_move_count + 1
        board.move_list = self.move_list.copy()
        board.board_state = self.board_state
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        board.rolling_score = -self.rolling_score

        board.get_valid_moves()

        return board


    def calculate_score(self, uci_coordinate):
        # break uci coordinate into location in board state list
        from_number = self.from_coordinate(uci_coordinate[0:2])
        to_number = self.from_coordinate(uci_coordinate[2:4])

        offset = 0 if self.played_move_count % 2 == 0 else 120

        from_piece = self.board_state[from_number]
        to_piece = self.board_state[to_number]

        local_score = ALLPSQT[from_piece.lower()][abs(offset - to_number)] - ALLPSQT[from_piece.lower()][abs(offset - from_number)]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece.lower()][abs(offset - to_number)]

        if (from_piece in ('K', 'k') and uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8')):
            if uci_coordinate[2] == 'g':
                local_score += ALLPSQT['r'][abs(offset - to_number - 1)] - ALLPSQT['r'][abs(offset - to_number + 1)]
            else:
                local_score += ALLPSQT['r'][abs(offset - to_number + 1)] - ALLPSQT['r'][abs(offset - to_number - 2)]
        elif from_piece in ('P', 'p') and uci_coordinate[2:4] == self.en_passant:
            # add in an extra pawn for EP capture
            local_score += ALLPSQT[from_piece.lower()][abs(offset - to_number)]

        if len(uci_coordinate) > 4:
            local_score += ALLPSQT['q'][abs(offset - to_number)] - ALLPSQT['p'][abs(offset - to_number)]

        return local_score

    def show_board(self):
        for row in self.board_state.split():
            print(row)

    def str_board(self):
<<<<<<< HEAD
        return hash(''.join(list(chain.from_iterable(self.board_state))) + str(self.played_move_count % 2 == 0))

    def get_coordinate(self, board_position):
        board_position = abs(119 - board_position)

        row = math.floor(board_position / 10) - 1
        column = abs(10 - board_position % 10) - 1

        return number_to_letter(column) + str(row)

    def from_coordinate(self, coordinate):
        column, row = ord(coordinate[0]) - ord('a'), int(coordinate[1]) - 1
        return 91 + column - 10*row
=======
        return ''.join(list(chain.from_iterable(self.board_state))) + str(self.played_move_count % 2 == 0)
>>>>>>> master

    def generate_valid_moves(self, reverse=False):
        is_white = self.played_move_count % 2 == 0

        if reverse:
            is_white = not is_white

        valid_moves = []
<<<<<<< HEAD
        capture_moves = []

        attack_squares = []

        eval_state = self.board_state
        for row, piece in enumerate(eval_state):
            if piece.isspace() or piece == "-" or (is_white and piece in BLACK_PIECES) or (not is_white and piece in WHITE_PIECES):
                continue

            start_coordinate = self.get_coordinate(row)

            if piece.lower() in ('b', 'r', 'q', 'k'):
                all_moves = {
                    # rook/queen - horizontal/vertical
                    1: -10,
                    2: +10,
                    3: -1,
                    4: +1,
                    # bish/queen - diagonal
                    5: -11,
                    6: +11,
                    7: -9,
                    8: +9,
                }

                for key, a_move in all_moves.items():
                    if (key <= 4 and piece.lower() == 'b') or (key >= 5 and piece.lower() == 'r'):
                        continue
                    temp_row = row + a_move
                    while temp_row >= 21 and temp_row < 99:
                        eval_piece = eval_state[temp_row]

                        can_capture = (is_white and eval_piece in BLACK_PIECES) or (not is_white and eval_piece in WHITE_PIECES)

                        if piece.lower() == 'k':
                            if is_white:
                                if self.white_castling[1] and start_coordinate == 'e1' and eval_state[96:99] == '--R' and \
                                    not any(coordinate in self.attack_squares[1] for coordinate in ['e1', 'f1', 'g1']):
                                    valid_moves.append(start_coordinate + 'g1')
                                if self.white_castling[0] and start_coordinate == 'e1' and eval_state[91:95] == 'R---' and \
                                    not any(coordinate in self.attack_squares[1] for coordinate in ['e1', 'd1', 'c1']):
                                    valid_moves.append(start_coordinate + 'c1')
                            else:
                                if self.black_castling[1] and start_coordinate == 'e8' and eval_state[26:29] == '--r' and \
                                    not any(coordinate in self.attack_squares[0] for coordinate in ['e8', 'f8', 'g8']):
                                    valid_moves.append(start_coordinate + 'g8')
                                if self.black_castling[0] and start_coordinate == 'e8' and eval_state[21:25] == 'r---' and \
                                    not any(coordinate in self.attack_squares[0] for coordinate in ['e8', 'd8', 'c8']):
                                    valid_moves.append(start_coordinate + 'c8')

                        if eval_piece == '-' or can_capture:
                            dest = self.get_coordinate(temp_row)
                            valid_moves.append(start_coordinate + dest)
                            attack_squares.append(dest)
                            if can_capture:
                                capture_moves.append(start_coordinate + dest)
                                break
                        else:
                            break

                        if piece.lower() == 'k':
                            # king can only move one space
                            break
                        temp_row += a_move
            if piece.lower() == 'n':
                night_moves = {
                    1: row - 21,
                    2: row - 19,
                    3: row - 12,
                    4: row - 8,
                    5: row + 8,
                    6: row + 12,
                    7: row + 19,
                    8: row + 21,
                }

                for _, n_move in night_moves.items():
                    if n_move >= 21 and n_move < 99:
                        eval_piece = eval_state[n_move]
                        if is_white:
                            can_capture = (eval_piece != '-' and eval_piece.islower())
                        else:
                            can_capture = (eval_piece != '-' and eval_piece.isupper())
                        if eval_piece == '-' or can_capture:
                            dest = self.get_coordinate(n_move)
                            valid_moves.append(start_coordinate + dest)
                            if can_capture:
                                capture_moves.append(start_coordinate + dest)

                            attack_squares.append(dest)
            if piece.lower() == 'p':
                if is_white:
                    start_row = 81
                    end_row = 31
                    offset = -10
                    piece_set = BLACK_PIECES
                else:
                    start_row = 31
                    end_row = 81
                    offset = 10
                    piece_set = WHITE_PIECES

                prom = ''
                if row in range(end_row, end_row + 10):
                    prom = 'q'

                if eval_state[row + offset] == '-':
                    valid_moves.append(start_coordinate + self.get_coordinate(row + offset) + prom)
                    if row in range(start_row, start_row + 10) and eval_state[row + 2*offset] == '-':
                        valid_moves.append(start_coordinate + self.get_coordinate(row + 2*offset))

                if eval_state[row + offset + 1] == '-':
                    dest = self.get_coordinate(row + offset + 1)
                    dest_piece = eval_state[row + offset  + 1]
                    if dest_piece == '-' or dest_piece in piece_set or dest == self.en_passant:
                        if dest_piece != '-':
                            valid_moves.append(start_coordinate + dest + prom)
                            capture_moves.append(start_coordinate + dest + prom)
                        attack_squares.append(dest)
                if eval_state[row + offset - 1] == '-':
                    dest = self.get_coordinate(row + offset - 1)
                    dest_piece = eval_state[row + offset - 1]
                    if dest_piece == '-' or dest_piece in piece_set or dest == self.en_passant:
                        if dest_piece != '-':
                            valid_moves.append(start_coordinate + dest + prom)
                            capture_moves.append(start_coordinate + dest + prom)
                        attack_squares.append(dest)

        self.capture_moves.append(capture_moves)

        self.valid_moves[0 if is_white else 1] = valid_moves
        self.attack_squares[0 if is_white else 1] = attack_squares
=======

        attack_squares = []

        valid_pieces = ['p', 'r', 'n', 'b', 'q', 'k', '-']
        if not is_white:
            valid_pieces = ['P', 'R', 'N', 'B', 'Q', 'K', '-']

        eval_state = self.board_state
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-" or (is_white and piece.islower()) or (not is_white and piece.isupper()):
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
                        if self.white_castling[1] and start_coordinate == 'e1' and ''.join(eval_state[7][5:8]) == '--R' and \
                            not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'f1', 'g1']):
                            valid_moves.append(start_coordinate + 'g1')
                        if self.white_castling[0] and start_coordinate == 'e1' and ''.join(eval_state[7][0:4]) == 'R---' and \
                            not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'd1', 'c1']):
                            valid_moves.append(start_coordinate + 'c1')
                    else:
                        if self.black_castling[1] and start_coordinate == 'e8' and ''.join(eval_state[0][5:8]) == '--r' and \
                            not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'f8', 'g8']):
                            valid_moves.append(start_coordinate + 'g8')
                        if self.black_castling[0] and start_coordinate == 'e8' and ''.join(eval_state[0][0:4]) == 'r---' and \
                            not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'd8', 'c8']):
                            valid_moves.append(start_coordinate + 'c8')

                    for _, k_move in king_moves.items():
                        if k_move['column'] in range(8) and k_move['row'] in range(8):
                            eval_piece = eval_state[k_move['row']][k_move['column']]

                            dest = number_to_letter(k_move['column'] + 1) + str(abs(k_move['row'] - 8))

                            if eval_piece in valid_pieces:
                                valid_moves.append(start_coordinate + dest)

                            attack_squares.append(dest)
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

                            if eval_piece in valid_pieces:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                valid_moves.append(start_coordinate + dest)
                                attack_squares.append(dest)
                                if eval_piece != '-':
                                    break
                            else:
                                break
                            temp_row += a_move['rowIncrement']
                            temp_col += a_move['colIncrement']
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
                            if eval_piece in valid_pieces:
                                dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
                                valid_moves.append(start_coordinate + dest)

                                attack_squares.append(dest)
                if piece.lower() == 'p':
                    min_row = 1
                    max_row = 6
                    offset = -1
                    if not is_white:
                        min_row = 6
                        max_row = 1
                        offset = 1

                    if eval_state[row + offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)))
                    if row == max_row and eval_state[row + offset][column] == '-' and eval_state[row + 2*offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset)))
                    if row == min_row and eval_state[row + offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)) + 'q')
                    if row + offset in range(8) and 1 <= column < 7:
                        prom = ''
                        if row == min_row:
                            prom = 'q'
                        if column > 0:
                            dest = number_to_letter(column) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column - 1]
                            if dest_piece in valid_pieces:
                                if dest_piece != '-' or dest == self.en_passant:
                                    valid_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)
                        if column < 7:
                            dest = number_to_letter(column + 2) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column + 1]
                            if dest_piece in valid_pieces:
                                if dest_piece != '-' or dest == self.en_passant:
                                    valid_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)

        self.valid_moves = valid_moves
        self.attack_squares[is_white] = attack_squares
>>>>>>> master

        return valid_moves

    def in_check(self, is_white):
        if is_white:
<<<<<<< HEAD
            return self.white_king_position in self.attack_squares[1]

        return self.black_king_position in self.attack_squares[0]
=======
            return self.white_king_position in self.attack_squares[not is_white]

        return self.black_king_position in self.attack_squares[not is_white]

TABLE_LIMIT = 9e5
Entry = namedtuple('Entry', 'lower upper')
>>>>>>> master

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    tt_bucket = {}
    tt_moves = {}

    def reset(self):
        self.v_nodes = 0
<<<<<<< HEAD
        self.v_tthits = 0
        self.tt_bucket = {}

    def iterative_search(self, local_board, v_depth):
        start_time = get_perf_counter()

        alpha = -1e8
        beta = 1e8

        iterative_score = -1e8
        iterative_move = None

=======
>>>>>>> master
        self.v_depth = 0
        self.end_time = 0
        self.tt_bucket.clear()
        self.tt_moves.clear()

<<<<<<< HEAD
            (iterative_score, iterative_move) = self.search(local_board, self.v_depth, alpha, beta)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            v_nps = math.ceil(self.v_nodes / elapsed_time)
=======
    # search is mostly based on thomasahle's sunfish
    # https://github.com/thomasahle/sunfish
    def iterative_search(self, local_board):
        start_time = time.time()
>>>>>>> master

        initial_move = self.tt_moves.get(local_board.str_board())

        # castling being cached can override the "in check" check
        if initial_move:
            if initial_move in ('e1c1', 'e1g1', 'e8c8', 'e8g8') and local_board.in_check(local_board.played_move_count % 2 == 0):
                self.tt_moves[local_board.str_board()] = None

        for v_depth in range(1, 100):
            lower_bound = -MATE_UPPER
            upper_bound = MATE_UPPER

            while lower_bound < upper_bound - 10:
                score_cutoff = (lower_bound + upper_bound + 1) // 2

<<<<<<< HEAD
        v_depth = max(v_depth, 1)

        print_time = get_perf_counter() + 5

        for s_move in sorted(local_board.get_valid_moves(), key=local_board.calculate_score, reverse=True):
            self.v_nodes += 1
=======
                local_score = self.search(local_board, score_cutoff, v_depth)

                if local_score >= score_cutoff:
                    lower_bound = local_score

                if local_score < score_cutoff:
                    upper_bound = local_score
>>>>>>> master

            self.search(local_board, lower_bound, v_depth)

<<<<<<< HEAD
            if temp_board.in_check(local_board.played_move_count % 2 == 0):
                continue
=======
            best_move = self.tt_moves.get(local_board.str_board())
>>>>>>> master

            score = self.tt_bucket.get((local_board.str_board(), v_depth, True)).lower

            elapsed_time = time.time() - start_time

<<<<<<< HEAD
            if get_perf_counter() > print_time:
                print_to_terminal("info nodes " + str(self.v_nodes))
                print_time = get_perf_counter() + 5

        return [global_score, chosen_move]

    def pvs(self, local_board, alpha, beta, v_depth):
        v_depth = max(0, v_depth)

        if v_depth < 1 or local_board.rolling_score > (beta + 60 * v_depth):
            # check to see if last move was in previous list of captures
            if local_board.move_list[-1] in local_board.capture_moves[-1]:
                return self.q_search(local_board, alpha, beta, 8)
            else:
                return local_board.rolling_score

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        original_alpha = alpha

        tt_entry = self.tt_lookup(local_board)
        if tt_entry['tt_depth'] >= v_depth:
            if tt_entry['tt_flag'] == EXACT:
                return tt_entry['tt_value']
            if tt_entry['tt_flag'] == LOWER:
                alpha = max(alpha, tt_entry['tt_value'])
            elif tt_entry['tt_flag'] == UPPER:
                beta = min(beta, tt_entry['tt_value'])

            if alpha >= beta:
                return tt_entry['tt_value']
=======
            v_nps = math.ceil(self.v_nodes / elapsed_time)
>>>>>>> master

            print_stats(str(v_depth), str(math.ceil(score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move))

<<<<<<< HEAD
        pieces = 'RBNQ' if local_board.played_move_count % 2 == 0 else 'rnbq'

        # test null move
        if any(piece in local_board.board_state for piece in pieces):
            alpha = max(alpha, -self.pvs(local_board.nullmove(), -beta, -alpha, v_depth - 3))

        for s_move in sorted(local_board.get_valid_moves(), key=local_board.calculate_score, reverse=True):
            self.v_nodes += 1

            local_score = -self.pvs(local_board.make_move(s_move, True), -alpha - 1, -alpha, v_depth - 1)
            if alpha < local_score < beta:
                local_score = -self.pvs(local_board.make_move(s_move, True), -beta, -local_score, v_depth - 1)
=======
            yield v_depth, best_move, score

    # search is mostly based on thomasahle's sunfish
    # https://github.com/thomasahle/sunfish
    def search(self, local_board, score_cutoff, v_depth, parent_search=True, root=True):
        self.v_nodes += 1

        v_depth = max(0, v_depth)
>>>>>>> master

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if not root and local_board.repetitions.count(local_board.str_board()) >= 2:
            return 0

        tt_entry = self.tt_bucket.get((local_board.str_board(), v_depth, root), Entry(-MATE_UPPER, MATE_UPPER))

        if tt_entry.lower >= score_cutoff and (not root or self.tt_moves.get(local_board.str_board()) is not None):
            return tt_entry.lower
        if tt_entry.upper < score_cutoff:
            return tt_entry.upper

<<<<<<< HEAD
    def q_search(self, local_board, alpha, beta, v_depth):
        if v_depth <= 0 or len(local_board.capture_moves[-1]) == 0:
            return local_board.rolling_score

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if local_board.rolling_score >= beta:
            return beta
=======
        def moves():
            current_piece_count = local_board.get_piece_count()

            # if v_depth > 0:
            #     yield None, -self.search(local_board.nullmove(), 1-score_cutoff, v_depth-3, root=False)
>>>>>>> master

            if v_depth == 0:
                yield None, local_board.rolling_score

<<<<<<< HEAD
        # local_board.get_valid_moves()
=======
            killer = self.tt_moves.get(local_board.str_board())
            if killer:
                killer_score = local_board.calculate_score(killer)
                killer_board = local_board.make_move(killer)
>>>>>>> master

                if v_depth > 0 or killer_score > 800 or current_piece_count != killer_board.get_piece_count():
                    yield killer, -self.search(killer_board, 1-score_cutoff, v_depth-1, root=False)

<<<<<<< HEAD
        # loop through current list of captures
        for s_move in local_board.capture_moves[-1]:
            self.v_nodes += 1
=======
            for s_move in sorted(local_board.generate_valid_moves(), key=local_board.calculate_score, reverse=parent_search):
                current_move_score = local_board.calculate_score(s_move)
>>>>>>> master

                moved_board = local_board.make_move(s_move)
                moved_piece_count = moved_board.get_piece_count()

                if v_depth > 0 or current_move_score > 800 or current_piece_count != moved_piece_count:
                    yield s_move, -self.search(moved_board, 1-score_cutoff, v_depth-1, root=False)

        best_score = -MATE_UPPER
        for s_move, local_score in moves():
            best_score = max(best_score, local_score)

            if best_score >= score_cutoff:
                # we will only wait for parent to search all, otehrwise we don't want partial move in TB
                if parent_search:
                    self.tt_moves[local_board.str_board()] = s_move
                break

<<<<<<< HEAD

    def tt_lookup(self, local_board):
        board_string = local_board.str_board()
        if board_string not in self.tt_bucket:
            self.tt_bucket[board_string] = {
                'tt_depth': 0,
                'tt_value': -1e5,
                'tt_flag': 2
            }
=======
        if best_score < score_cutoff and best_score < 0 and v_depth > 0:
            is_dead = lambda local_board: any(local_board.calculate_score(m) >= MATE_LOWER for m in local_board.generate_valid_moves())
            if all(is_dead(local_board.make_move(m)) for m in local_board.generate_valid_moves()):
                in_check = is_dead(local_board.nullmove())
                best_score = -MATE_UPPER if in_check else 0
>>>>>>> master

        #update TT
        if best_score >= score_cutoff:
            self.tt_bucket[local_board.str_board(), v_depth, root] = Entry(best_score, tt_entry.upper)
        if best_score < score_cutoff:
            self.tt_bucket[local_board.str_board(), v_depth, root] = Entry(tt_entry.lower, best_score)

        return best_score

def main():
    game_board = Board()
<<<<<<< HEAD
=======
    searcher = Search()
>>>>>>> master

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            # elif line == "print":
            #     game_board.show_board()
            elif line == "uci":
                print_to_terminal("pygone 1.4\nuciok")
            elif line == "ucinewgame":
                game_board = Board()
                searcher.reset()
                gc.collect()
            elif line == "isready":
                print_to_terminal("readyok")
            elif line.startswith("position"):
                moves = line.split()
                game_board = Board()
                for position_move in moves[3:]:
                    game_board = game_board.make_move(position_move)
                game_board.generate_valid_moves()
                game_board.generate_valid_moves(True)
                # print(game_board.attack_squares)
                # game_board.show_board()
            elif line.startswith("go"):
                white_time = 1e8
                black_time = 1e8
                searcher.v_depth = 30

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    elif arg == 'btime':
                        black_time = int(args[key + 1])
                    # these are commented out to save space since engine will be run on time
                    elif arg == 'depth':
                        searcher.v_depth = int(args[key + 1])

                time_move_calc = max(40 - game_board.played_move_count, 2)

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0

                move_time = (black_time / 20000)
                if is_white:
<<<<<<< HEAD
                    move_time = (white_time / (time_move_calc * 1e3))
                else:
                    move_time = (black_time / (time_move_calc * 1e3))

                searcher.end_time = get_perf_counter() + move_time

                go_depth = max(input_depth, go_depth)

                print(move_time)

                if move_time < 30:
                    go_depth = 5
                if move_time < 7:
                    go_depth = 4
                if move_time < 4:
                    go_depth = 3
=======
                    move_time = (white_time / 20000)

                if game_board.played_move_count < 13:
                    move_time += 10

                move_time = max(move_time, 3)

                searcher.end_time = time.time() + move_time - 1
>>>>>>> master

                searcher.v_nodes = 0

<<<<<<< HEAD
                (_, s_move) = searcher.iterative_search(game_board, go_depth)
=======
                s_move = None

                start = time.time()
                for _depth, s_move, score in searcher.iterative_search(game_board):
                    if game_board.played_move_count > 13 and (searcher.end_time - time.time()) < 25:
                        searcher.v_depth = 5
                    if game_board.played_move_count > 13 and (searcher.end_time - time.time()) < 4:
                        searcher.v_depth = 3

                    if _depth >= searcher.v_depth or time.time() > searcher.end_time:
                        break
>>>>>>> master

                print_to_terminal("bestmove " + s_move)

                if len(searcher.tt_moves) > TABLE_LIMIT:
                    searcher.tt_moves.clear()
                if len(searcher.tt_bucket) > TABLE_LIMIT:
                    searcher.tt_bucket.clear()

        except (KeyboardInterrupt, SystemExit):
            print_to_terminal('quit')
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
