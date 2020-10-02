#!/usr/bin/env pypy3
import math, sys, time
import gc
from itertools import chain
from collections import namedtuple

PIECEPOINTS = {'pe': 180, 'p': 90, 'r': 500, 'n': 320, 'b': 330, 'q': 900, 'k': 2e4, 'ke': 2e4}

ALLPSQT = {
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

WHITE_PIECES = ['P', 'R', 'N', 'B', 'Q', 'K']
BLACK_PIECES = ['p', 'r', 'n', 'b', 'q', 'k']

EXACT = 1
UPPER = 2
LOWER = 3

MATE_LOWER = PIECEPOINTS['k'] - 10*PIECEPOINTS['q']
MATE_UPPER = PIECEPOINTS['k'] + 10*PIECEPOINTS['q']

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
    board_state = []
    played_move_count = 0
    move_list = []
    repetitions = []
    valid_moves = [[], []]
    attack_squares = [[], []]
    white_castling = [True, True]
    black_castling = [True, True]
    white_king_position = 'e1'
    black_king_position = 'e8'
    rolling_score = 0
    en_passant = ''

    def __init__(self):
        self.board_state = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['P']*8,
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

    def set_board_state(self, board_state):
        self.board_state = board_state

    def apply_move(self, uci_coordinate):
        # break uci coordinate into location in board state list
        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        from_piece = self.board_state[from_number][from_letter_number]

        is_white = self.played_move_count % 2 == 0

        self.board_state[to_number][to_letter_number] = from_piece
        self.board_state[from_number][from_letter_number] = '-'

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
        board.valid_moves = [x[:] for x in self.valid_moves]
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

        board.repetitions.append(board.str_board())

        board.rolling_score = -board.rolling_score

        return board

    def nullmove(self):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count + 1
        board.board_state = [x[:] for x in self.board_state]
        board.valid_moves = [x[:] for x in self.valid_moves]
        # board.capture_moves = self.capture_moves.copy()
        board.attack_squares = [x[:] for x in self.attack_squares]
        board.move_list = self.move_list.copy()
        board.repetitions = self.repetitions.copy()
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

        from_piece = self.board_state[from_number][from_letter_number]
        from_score_piece = from_piece.lower()
        if self.get_piece_count() <= 16 and from_piece.lower() == 'k':
            from_score_piece = 'ke'
        if self.get_piece_count() <= 16 and from_piece.lower() == 'p':
            from_score_piece = 'pe'

        to_piece = self.board_state[to_number][to_letter_number]

        local_score = ALLPSQT[from_score_piece][abs(to_number - offset)][to_letter_number] - ALLPSQT[from_score_piece][abs(from_number - offset)][from_letter_number]

        # if self.get_piece_count() <= 16 and from_piece.lower() in 'nbrq':
        #     local_score += PIECEPOINTS[from_score_piece] * 0.05

        if to_piece != '-':
            local_score += ALLPSQT[to_piece.lower()][abs(to_number - offset)][to_letter_number]
            # if self.get_piece_count() <= 16:
            #     local_score += 5

        if from_piece in ('K', 'k'):
            if abs(from_number - to_number) == 2:
                if uci_coordinate[2] == 'g':
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 1] - ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1]
                else:
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1] - ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 2]
        elif from_piece in ('P', 'p') and uci_coordinate[2:4] == self.en_passant:
            # add in an extra pawn for EP capture
            local_score += ALLPSQT[from_score_piece][abs(to_number - offset)][abs(to_letter_number - offset)]

        if len(uci_coordinate) > 4:
            # adjust value for promoting from pawn to queen
            local_score += ALLPSQT['q'][abs(to_number - offset)][to_letter_number] - ALLPSQT['p'][abs(to_number - offset)][to_letter_number]

        # local_score += self.score_pawns()

        return local_score

    def score_pawns(self):
        is_white = self.played_move_count % 2 == 0

        piece = 'P' if is_white else 'p'

        local_score = 0

        for column in range(8):
            pawn_column_count = 0
            for row in range(8):
                if self.board_state[row][column] == piece:
                    pawn_column_count += 1

            if pawn_column_count > 1:
                local_score -= (pawn_column_count - 1) * 5

        return local_score

    # def show_board(self):
    #     for i in range(8):
    #         for j in range(8):
    #             print(self.board_state[i][j], end=" ")
    #         print()
    #     print("a b c d e f g h")

    def str_board(self, is_hash=True):
        return ''.join(list(chain.from_iterable(self.board_state))) + str(self.played_move_count % 2 == 0)

    def get_valid_moves(self, is_reverse=False):
        is_white = self.played_move_count % 2 == 0

        if is_reverse:
            is_white = not is_white

        valid_moves = []

        attack_squares = []

        valid_pieces = ['p', 'r', 'n', 'b', 'q', 'k', '-']
        if not is_white:
            valid_pieces = ['P', 'R', 'N', 'B', 'Q', 'K', '-']

        eval_state = self.board_state
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
                        if self.white_castling[1] and start_coordinate == 'e1' and ''.join(eval_state[7][5:8]) == '--R' and \
                            not any(coordinate in self.attack_squares[1] for coordinate in ['e1', 'f1', 'g1']):
                            valid_moves.append(start_coordinate + 'g1')
                        if self.white_castling[0] and start_coordinate == 'e1' and ''.join(eval_state[7][0:4]) == 'R---' and \
                            not any(coordinate in self.attack_squares[1] for coordinate in ['e1', 'd1', 'c1']):
                            valid_moves.append(start_coordinate + 'c1')
                    else:
                        if self.black_castling[1] and start_coordinate == 'e8' and ''.join(eval_state[0][5:8]) == '--r' and \
                            not any(coordinate in self.attack_squares[0] for coordinate in ['e8', 'f8', 'g8']):
                            valid_moves.append(start_coordinate + 'g8')
                        if self.black_castling[0] and start_coordinate == 'e8' and ''.join(eval_state[0][0:4]) == 'r---' and \
                            not any(coordinate in self.attack_squares[0] for coordinate in ['e8', 'd8', 'c8']):
                            valid_moves.append(start_coordinate + 'c8')

                    past_valid_moves = self.valid_moves[is_white]

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
                    if is_white:
                        min_row = 1
                        max_row = 6
                        offset = -1
                    else:
                        min_row = 6
                        max_row = 1
                        offset = 1

                    if row in range(1, 7) and row != min_row and eval_state[row + offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)))
                    if row == max_row and eval_state[row + offset][column] == '-' and eval_state[row + 2*offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset)))
                    if row == min_row and eval_state[row + offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)) + 'q')
                    if ((column - 1) >= 0 and (row + offset) in range(8)) or ((column + 1) < 8 and (row + offset) in range(8)):
                        prom = ''
                        if row == min_row:
                            prom = 'q'
                        if (column - 1) >= 0:
                            dest = number_to_letter(column) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column - 1]
                            if dest_piece in valid_pieces:
                                if dest_piece != '-' or dest == self.en_passant:
                                    valid_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)
                        if (column + 1) < 8:
                            dest = number_to_letter(column + 2) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column + 1]
                            if dest_piece in valid_pieces:
                                if dest_piece != '-' or dest == self.en_passant:
                                    valid_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)

        self.valid_moves[0 if is_white else 1] = valid_moves
        self.attack_squares[0 if is_white else 1] = attack_squares

        return valid_moves

    def in_check(self, is_white):
        if is_white:
            return self.white_king_position in self.attack_squares[1]

        return self.black_king_position in self.attack_squares[0]

# copied from thomasahle/sunfish
# https://github.com/thomasahle/sunfish
TABLE_LIMIT = 9e5
QS_LIMIT = 115
EVAL_ROUGHNESS = 15
Entry = namedtuple('Entry', 'value depth flag')

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    tt_bucket = {}
    tt_moves = {}
    interrupted_search = False

    def reset(self):
        self.v_nodes = 0
        self.v_depth = 0
        self.end_time = 0
        self.tt_bucket.clear()
        self.tt_moves.clear()

    def iterative_search(self, local_board):
        start_time = time.time()

        last_score = -MATE_UPPER

        for v_depth in range(1, 100):
            alpha = -MATE_UPPER

            if v_depth > 5:
                alpha = max(alpha, last_score) - 50

            score = self.search(local_board, alpha, MATE_UPPER, v_depth)

            last_score = max(score, last_score)

            picked_move = self.tt_moves[local_board.str_board()]

            elapsed_time = time.time() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time)

            print_stats(str(v_depth), str(math.ceil(score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(picked_move))

            yield v_depth, picked_move, score

    def search(self, local_board, alpha, beta, v_depth, q_count=0, root=True):
        self.v_nodes += 1

        original_alpha = alpha

        is_pv_node = alpha != beta - 1

        v_depth = max(1, v_depth)

        is_in_check = local_board.in_check(local_board.played_move_count %2 != 0)

        if not root and local_board.repetitions.count(local_board.str_board()) > 2:
            return 0

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        tt_entry = self.tt_bucket.get((local_board.str_board(), v_depth, root), Entry(-MATE_UPPER, v_depth, LOWER))

        if tt_entry.flag == EXACT:
            return tt_entry.value
        if tt_entry.flag == LOWER:
            alpha = max(alpha, tt_entry.value)
        elif tt_entry.flag == UPPER:
            beta = min(beta, tt_entry.value)

        if alpha >= beta:
            return tt_entry.value

        # local_eval = tt_entry.value if tt_entry.value > -MATE_UPPER else local_board.rolling_score

        # if not is_pv_node and not is_in_check and v_depth <= 6 and (local_eval - 85 * v_depth > beta):
        #     return local_eval

        if v_depth <= 1:
            return local_board.rolling_score

        best_score = -MATE_UPPER

        played_moves = 0

        current_piece_count = local_board.get_piece_count()

        initial_score = -1e8

        if v_depth > 0:
            local_score = -self.search(local_board.nullmove(), -beta, -alpha, v_depth-3, root=False)

        killer = self.tt_moves.get(local_board.str_board())
        if killer:
            killer_board = local_board.make_move(killer)
            if v_depth > 0 and current_piece_count == killer_board.get_piece_count():
                local_score = max(local_score, -self.search(killer_board, -beta, -alpha, v_depth-1, root=False))
            elif current_piece_count != killer_board.get_piece_count():
                local_score = max(local_score, -self.q_search(killer_board, -beta, -alpha, 8))

        for s_move in sorted(local_board.get_valid_moves(), key=local_board.calculate_score, reverse=True):
            current_move_score = local_board.calculate_score(s_move)

            moved_board = local_board.make_move(s_move)
            moved_board.get_valid_moves()
            moved_piece_count = moved_board.get_piece_count()

            if moved_board.in_check(moved_board.played_move_count % 2 != 0) or current_move_score <= -MATE_UPPER:
                continue

            played_moves += 1

            if current_piece_count != moved_piece_count:
                local_score = max(local_score, -self.q_search(moved_board, -beta, -alpha, 8))
            elif v_depth > 0:
                local_score = max(local_score, -self.search(moved_board, -alpha-1, -alpha, v_depth-1, root=False))

                if local_score > alpha:
                    local_score = max(local_score, -self.search(moved_board, -beta, -alpha, v_depth-1))

            if local_score > best_score:
                best_score = local_score
                self.tt_moves[local_board.str_board()] = s_move

            alpha = max(alpha, local_score)

            if alpha >= beta:
                break;

        # Stalemate/checkmate
        if v_depth > 0 and played_moves == 0:
            return -MATE_UPPER if is_in_check else 0

        #update TT
        if best_score <= original_alpha:
            flag = UPPER
        elif best_score >= beta:
            flag = LOWER
        else:
            flag = EXACT

        self.tt_bucket[local_board.str_board(), v_depth, root] = Entry(best_score, v_depth, flag)

        return best_score

    def q_search(self, local_board, alpha, beta, v_depth):
        self.v_nodes += 1

        if v_depth <= 0:
            return local_board.rolling_score

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if local_board.rolling_score >= beta:
            return beta

        alpha = max(local_board.rolling_score, alpha)

        current_piece_count = local_board.get_piece_count()

        local_score = -1e8

        # loop through current list of captures
        for s_move in local_board.get_valid_moves():
            moved_board = local_board.make_move(s_move)
            moved_piece_count = moved_board.get_piece_count()

            if moved_piece_count == current_piece_count:
                continue

            local_score = -self.q_search(local_board.make_move(s_move), -beta, -alpha, v_depth - 1)

            if local_score >= beta:
                return beta

            alpha = max(local_score, alpha)

        return alpha

def main():
    game_board = Board()
    searcher = Search()

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            # elif line == "print":
            #     game_board.show_board()
            elif line == "uci":
                print_to_terminal("pygone 1.3\nuciok")
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
                game_board.get_valid_moves(True)
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
                    move_time = (white_time / 20000)

                if game_board.played_move_count < 13:
                    move_time += 10

                move_time = max(move_time, 3)

                if move_time <= 4:
                    search.v_depth = 3

                searcher.end_time = time.time() + move_time - 2

                searcher.v_nodes = 0

                s_move = None

                start = time.time()
                for _depth, s_move, score in searcher.iterative_search(game_board):
                    if _depth >= searcher.v_depth or time.time() > searcher.end_time:
                        break

                # s_move = searcher.iterative_search(game_board)

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
