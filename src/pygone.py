#!/usr/bin/env pypy3
import math, sys, time
import gc
from itertools import chain
from collections import namedtuple

PIECEPOINTS = {'pe': 100, 'p': 90, 'r': 500, 'n': 320, 'b': 330, 'q': 900, 'k': 2e4, 'ke': 2e4}

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

TO_MOVES = {
    # (column, row, can_capture)
    'k': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), (1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'q': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), (1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'r': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1)],
    'b': [(1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'n': [(1, -2, 1), (-1, -2, 1), (2, -1, 1), (-2, -1, 1), (1, 2, 1), (-1, 2, 1), (2, 1, 1), (-2, 1, 1)],
    'p': [(0, 1, 0), (1, 1, 1), (-1, 1, 1)]
}

def number_to_letter(to_number):
    return chr(to_number + 96)

def print_to_terminal(print_string):
    print(print_string, flush=True)

def print_stats(v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
    print_to_terminal("info depth " + v_depth + " score cp " + v_score + " time " + v_time + " nodes " + v_nodes + " nps " + v_nps + " pv " + v_pv)

def unpack_coordinate(uci_coordinate):
    return (abs((ord(uci_coordinate[0:1]) - 96) - 1),
            abs(int(uci_coordinate[1:2]) - 8),
            abs((ord(uci_coordinate[2:3]) - 96) - 1),
            abs(int(uci_coordinate[3:4]) - 8))

def is_dead(local_board):
    return any(local_board.calculate_score(m) >= MATE_LOWER for m in local_board.generate_valid_moves())

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

            if len(uci_coordinate) > 4:
                self.board_state[to_number][to_letter_number] = uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5]

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

    def make_move(self, uci_coordinate):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state = [x[:] for x in self.board_state]
        board.valid_moves = [x[:] for x in self.valid_moves]
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
        elif 'a1' in uci_coordinate:
            board.white_castling[0] = False
        elif 'h1' in uci_coordinate:
            board.white_castling[1] = False

        if 'e8' in uci_coordinate:
            board.black_castling = [False, False]
        elif 'a8' in uci_coordinate:
            board.black_castling[0] = False
        elif 'h8' in uci_coordinate:
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
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        # clear positions and ep for nullmove
        board.white_king_position = ''
        board.black_king_position = ''
        board.en_passant = ''
        board.rolling_score = -self.rolling_score

        return board

    def get_piece_count(self):
        return 64 - self.str_board().count('-')

    def is_endgame(self):
        total_pieces = self.get_piece_count()
        total_pawns = self.str_board().lower().count('p')

        return total_pieces <= 14 or total_pawns <= 8

    def calculate_score(self, uci_coordinate):
        is_white = self.played_move_count % 2 == 0
        offset = 0 if is_white else 7

        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        local_score = 0

        from_piece = self.board_state[from_number][from_letter_number]
        from_score_piece = from_piece.lower()

        if self.is_endgame():
            if from_piece.lower() == 'k':
                from_score_piece = 'ke'
            if from_piece.lower() == 'p':
                local_score += 6
                from_score_piece = 'pe'

        to_piece = self.board_state[to_number][to_letter_number]

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
                promote = uci_coordinate[4:5]
                # adjust value for promoting from pawn to queen
                local_score += ALLPSQT[promote][abs(to_number - offset)][to_letter_number] - ALLPSQT['p'][abs(to_number - offset)][to_letter_number]

        if self.is_endgame():
            enemy_king_position = self.black_king_position if is_white else self.white_king_position

            if enemy_king_position in self.valid_moves[is_white]:
                local_score += 8

        return local_score + self.score_pawns(is_white)

    def score_pawns(self, is_white):
        pawn_piece = 'P' if is_white else 'p'

        pawns = 0
        pawn_columns = 0

        for column in range(8):
            has_pawn = False
            for row in range(8):
                if self.board_state[row][column] == pawn_piece:
                    pawns += 1
                    has_pawn = True

            pawn_columns += has_pawn

        return (pawn_columns - pawns) * 5

    def str_board(self):
        return ''.join(list(chain.from_iterable(self.board_state))) + str(self.played_move_count % 2 == 0)

    def generate_valid_moves(self, is_reverse=False):
        is_white = self.played_move_count % 2 == 0

        if is_reverse:
            is_white = not is_white

        self.valid_moves[is_white] = []
        self.attack_squares[is_white] = []

        valid_pieces = ['p', 'r', 'n', 'b', 'q', 'k', '-']
        if not is_white:
            valid_pieces = ['P', 'R', 'N', 'B', 'Q', 'K', '-']

        min_row = 1
        max_row = 6
        offset = 1

        if not is_white:
            min_row = 6
            max_row = 1

        eval_state = self.board_state
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-" or (is_white and piece.islower()) or (not is_white and piece.isupper()):
                    continue
                start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))

                if piece == 'P':
                    offset = -1

                # castling
                if piece == 'K':
                    if self.white_castling[1] and start_coordinate == 'e1' and ''.join(eval_state[7][5:8]) == '--R':
                        self.valid_moves[is_white].append(start_coordinate + 'g1')
                        yield start_coordinate + 'g1'
                    if self.white_castling[0] and start_coordinate == 'e1' and ''.join(eval_state[7][0:4]) == 'R---':
                        self.valid_moves[is_white].append(start_coordinate + 'c1')
                        yield start_coordinate + 'c1'
                elif piece == 'k':
                    if self.black_castling[1] and start_coordinate == 'e8' and ''.join(eval_state[0][5:8]) == '--r':
                        self.valid_moves[is_white].append(start_coordinate + 'g8')
                        yield start_coordinate + 'g8'
                    if self.black_castling[0] and start_coordinate == 'e8' and ''.join(eval_state[0][0:4]) == 'r---':
                        self.valid_moves[is_white].append(start_coordinate + 'c8')
                        yield start_coordinate + 'c8'
                elif piece.lower() == 'p' and row == max_row and eval_state[row + offset][column] == '-' and eval_state[row + 2*offset][column] == '-':
                    self.valid_moves[is_white].append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset)))
                    yield start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset))

                for piece_move in TO_MOVES[piece.lower()]:
                    to_column = column + piece_move[0]
                    to_row = row + (piece_move[1] * offset)

                    while to_column in range(8) and  to_row in range(8):
                        eval_piece = eval_state[to_row][to_column]

                        dest = number_to_letter(to_column + 1) + str(abs(to_row - 8))

                        if piece.lower() == 'p':
                            if (row == min_row and piece_move[0] == 0 and eval_piece == '-') or \
                                (row == min_row and piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces):
                                for prom in ('q', 'r', 'b', 'n'):
                                    self.valid_moves[is_white].append(start_coordinate + dest + prom)
                                    yield start_coordinate + dest + prom
                            else:
                                if (piece_move[0] == 0 and eval_piece == '-') or \
                                    (piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces) or \
                                    dest == self.en_passant:
                                    self.valid_moves[is_white].append(start_coordinate + dest)
                                    yield start_coordinate + dest
                        elif eval_piece in valid_pieces:
                            self.valid_moves[is_white].append(start_coordinate + dest)
                            yield start_coordinate + dest

                        if piece_move[2]:
                            self.attack_squares[is_white].append(dest)

                        if eval_piece != '-' or piece.lower() in ('k', 'n', 'p'):
                            break

                        to_column += piece_move[0]
                        to_row += (piece_move[1] * offset)

    def in_check(self, is_white):
        if is_white:
            return self.white_king_position in self.attack_squares[0]

        return self.black_king_position in self.attack_squares[1]

    def is_legal(self, s_move):
        # 0 - Black Moves
        # 1 - White Moves
        if self.white_king_position == 'e1' and s_move == 'e1g1':
            return not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'f1', 'g1'])
        elif self.white_king_position == 'e1' and s_move == 'e1c1':
            return not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'd1', 'c1'])
        elif self.black_king_position == 'e8' and s_move == 'e8g8':
            return not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'f8', 'g8'])
        elif self.black_king_position == 'e8' and s_move == 'e8c8':
            return not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'd8', 'c8'])

        return True

TABLE_LIMIT = 9e5
Entry = namedtuple('Entry', 'lower upper')

CONTEMPT=0

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    critical_time = 0
    tt_bucket = {}
    tt_moves = {}
    # perft_captures = 0
    # perft_checks = 0

    def reset(self):
        self.v_nodes = 0
        self.v_depth = 0
        self.end_time = 0
        self.critical_time = 0
        self.tt_bucket.clear()
        self.tt_moves.clear()

    # def run_perft(self, local_board, original_depth, v_depth):
    #     if v_depth == 0: return 1

    #     if v_depth != original_depth:
    #         total = 0
    #         for s_move in local_board.generate_valid_moves():
    #             moved_board = local_board.make_move(s_move)
    #             all(moved_board.generate_valid_moves(True))

    #             if moved_board.in_check(local_board.played_move_count % 2 == 0) or not local_board.is_legal(s_move):
    #                 continue

    #             if local_board.get_piece_count() != moved_board.get_piece_count():
    #                 self.perft_captures += 1

    #             if moved_board.in_check(moved_board.played_move_count % 2 == 0):
    #                 self.perft_checks += 1

    #             total += self.run_perft(local_board.make_move(s_move), original_depth, v_depth-1)
    #         return total

    #     per_moves = []
    #     for s_move in local_board.generate_valid_moves():
    #         moved_board = local_board.make_move(s_move)
    #         all(moved_board.generate_valid_moves())
    #         all(moved_board.generate_valid_moves(True))

    #         if moved_board.in_check(local_board.played_move_count % 2 == 0) or not local_board.is_legal(s_move):
    #             continue

    #         if local_board.get_piece_count() != moved_board.get_piece_count():
    #             self.perft_captures += 1

    #         if moved_board.in_check(moved_board.played_move_count % 2 == 0):
    #             self.perft_checks += 1

    #         print (s_move + ": ", end=" ")
    #         x = self.run_perft(local_board.make_move(s_move), original_depth, v_depth-1)
    #         print(x)
    #         per_moves.append(x)

    #     print("Nodes searched: ", sum(per_moves))
    #     print("Captures: ", self.perft_captures, " Checks: ", self.perft_checks)

    # search is mostly based on thomasahle's sunfish
    # https://github.com/thomasahle/sunfish
    def iterative_search(self, local_board):
        start_time = time.time()

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

                local_score = self.search(local_board, score_cutoff, v_depth)

                if local_score >= score_cutoff:
                    lower_bound = local_score

                if local_score < score_cutoff:
                    upper_bound = local_score

            self.search(local_board, lower_bound, v_depth)

            best_move = self.tt_moves.get(local_board.str_board())

            if self.tt_bucket.get((local_board.str_board(), v_depth, True)) is not None:
                result_score = self.tt_bucket.get((local_board.str_board(), v_depth, True)).lower
            else:
                result_score = local_score

            elapsed_time = time.time() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time)

            print_stats(str(v_depth), str(math.ceil(result_score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move))

            yield v_depth, best_move, result_score

    # search is mostly based on thomasahle's sunfish
    # https://github.com/thomasahle/sunfish
    def search(self, local_board, score_cutoff, v_depth, parent_search=True, root=True):
        self.v_nodes += 1

        if time.time() > self.critical_time:
            return local_board.rolling_score

        v_depth = max(0, v_depth)

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if not root and local_board.repetitions.count(local_board.str_board()) >= 2:
            return CONTEMPT

        tt_entry = self.tt_bucket.get((local_board.str_board(), v_depth, root), Entry(-MATE_UPPER, MATE_UPPER))

        if tt_entry is not None and tt_entry.lower >= score_cutoff and (not root or self.tt_moves.get(local_board.str_board()) is not None):
            return tt_entry.lower
        if tt_entry is not None and tt_entry.upper < score_cutoff:
            return tt_entry.upper

        is_white = local_board.played_move_count % 2 == 0

        def moves():
            current_piece_count = local_board.get_piece_count()

            # if v_depth > 0:
            #     yield None, -self.search(local_board.nullmove(), 1-score_cutoff, v_depth-3, root=False)

            if v_depth == 0:
                yield None, local_board.rolling_score

            killer = self.tt_moves.get(local_board.str_board())
            if killer:
                killer_score = local_board.calculate_score(killer)
                killer_board = local_board.make_move(killer)

                if v_depth > 0 or killer_score > 800 or current_piece_count != killer_board.get_piece_count():
                    yield killer, -self.search(killer_board, 1-score_cutoff, v_depth-1, root=False)

            for s_move in sorted(local_board.generate_valid_moves(), key=local_board.calculate_score, reverse=parent_search):
                current_move_score = local_board.calculate_score(s_move)

                if not local_board.is_legal(s_move):
                    continue

                moved_board = local_board.make_move(s_move)
                moved_piece_count = moved_board.get_piece_count()

                if local_board.in_check(is_white):
                    if is_dead(moved_board.nullmove()):
                        continue

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

        if best_score < score_cutoff and best_score < 0 and v_depth >= 0:
            if all(is_dead(local_board.make_move(m)) for m in local_board.generate_valid_moves()):
                in_check = is_dead(local_board.nullmove())
                best_score = -MATE_UPPER if in_check else CONTEMPT

        #update TT
        if best_score >= score_cutoff:
            self.tt_bucket[local_board.str_board(), v_depth, root] = Entry(best_score, tt_entry.upper)
        if best_score < score_cutoff:
            self.tt_bucket[local_board.str_board(), v_depth, root] = Entry(tt_entry.lower, best_score)

        return best_score

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
                all(game_board.generate_valid_moves())
                all(game_board.generate_valid_moves(True))
                # print(game_board.attack_squares)
                # game_board.show_board()
            elif line.startswith("go"):
                white_time = 1e8
                black_time = 1e8
                searcher.v_depth = 30

                # is_perft = False

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    elif arg == 'btime':
                        black_time = int(args[key + 1])
                    # these are commented out to save space since engine will be run on time
                    elif arg == 'depth':
                        searcher.v_depth = int(args[key + 1])
                #     elif arg == 'perft':
                #         searcher.v_depth = int(args[key + 1])
                #         is_perft = True

                # if is_perft:
                #     # 1) start pos
                #     # 2) Kiwipete: position startpos moves b1c3 b7b5 d2d4 e7e6 e2e4 c8a6 c1d2 h7h5 d1f3 g7g6 f1e2 h5h4 g1h3 f8g7 h3f4 g8e7 f4d3 e7d5 d3e5 d5f6 d4d5 d8e7 d2e3 b5b4 e3d2 b8c6 d2e3 c6a5 e3d2 a5c4 d2e3 c4b6 e3d2 h4h3
                #     # 3) Tricky Steve: position startpos moves d2d3 c7c6 e2e4 e7e5 d3d4 f8e7 d4e5 d7d6 e5d6 g8f6 f1c4 f6e4 d6d7 e8f8 g1e2 e4f2
                #     start_time = time.time()
                #     searcher.perft_checks = 0
                #     searcher.perft_captures = 0
                #     searcher.run_perft(game_board, searcher.v_depth, searcher.v_depth)
                #     # elapsed_time = time.time() - start_time
                #     # v_nps = math.ceil(searcher.v_nodes / elapsed_time)
                #     # print('captures: ', searcher.perft_captures)
                #     # print('checks: ', searcher.perft_checks)
                #     # print_to_terminal("Nodes searched: " + str(searcher.v_nodes) + " in " + str(elapsed_time) + " at " + str(v_nps) + " nps")
                #     continue

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0

                move_time = (black_time / 20000)
                searcher.critical_time = time.time() + (black_time / 1000) - 3
                if is_white:
                    move_time = (white_time / 20000)
                    searcher.critical_time = time.time() + (white_time / 1000) - 3

                if game_board.played_move_count < 13:
                    move_time += 10

                move_time = max(move_time, 3)

                searcher.end_time = time.time() + move_time

                searcher.v_nodes = 0

                s_move = None

                start = time.time()
                for _depth, s_move, score in searcher.iterative_search(game_board):
                    if game_board.played_move_count > 13:
                        if (searcher.end_time - time.time()) < 25:
                            searcher.v_depth = 5
                        # if (searcher.end_time - time.time()) < 10:
                        #     searcher.v_depth = 4
                        # if (searcher.end_time - time.time()) < 2:
                        #     searcher.v_depth = 3

                    if _depth >= searcher.v_depth or time.time() > searcher.end_time:
                        break

                print_to_terminal("bestmove " + s_move)

                if len(searcher.tt_moves) > TABLE_LIMIT:
                    searcher.tt_moves.clear()
                if len(searcher.tt_bucket) > TABLE_LIMIT:
                    searcher.tt_bucket.clear()

        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
