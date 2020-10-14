#!/usr/bin/env pypy3
import math, sys, time

PIECEPOINTS = {'pe': 100, 'p': 90, 'n': 290, 'b': 300, 'r': 500, 'q': 900, 'k': 2e4, 'ke': 2e4}

ALLPSQT = {
    'p': [[0]*8,
          [50]*8,
          [40]*8,
          [5, 5, 10, 25, 25, 10, 5, 5],
          [0, 0, 0, 20, 20, 0, 0, 0],
          [5, -5, -10, 0, 0, -10, -5, 5],
          [5, 10, 10, -20, -20, 10, 10, 5],
          [0]*8],
    'pe': [[0]*8,
           [50]*8,
           [40]*8,
           [30]*8,
           [20]*8,
           [10]*8,
           [0]*8,
           [0]*8],
    'n': [[-50, -40, -30, -30, -30, -30, -40, -50],
          [-40, -20, 0, 0, 0, 0, -20, -40],
          [-30, 5, 10, 15, 15, 10, 5, -30],
          [-30, 10, 15, 20, 20, 15, 10, -30],
          [-30, 5, 15, 25, 25, 15, 5, -30],
          [-30, 10, 10, 10, 10, 10, 10, -30],
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
    'r': [[0]*8,
          [5, 10, 10, 10, 10, 10, 10, 5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 0, 0, 0, 0, -5],
          [-5, 0, 0, 5, 0, 5, 0, -5],
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
          [20, 10, 30, 0, 0, 10, 30, 20]],
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
    return ((ord(uci_coordinate[0:1]) - 97),
            abs(int(uci_coordinate[1:2]) - 8),
            (ord(uci_coordinate[2:3]) - 97),
            abs(int(uci_coordinate[3:4]) - 8))

def string_join(in_list):
    out_string = ''
    for ch in in_list:
        out_string += ch

    return out_string

def string_count(haystack, needle):
    s_count = 0
    for c in haystack:
        if c == needle:
            s_count += 1

    return s_count

class Board:
    # represent the board state as it is
    board_state = []
    board_string = ''
    played_move_count = 0
    move_list = []
    repetitions = []
    attack_squares = [[], []]
    white_castling = [True, True]
    black_castling = [True, True]
    white_king_position = 'e1'
    black_king_position = 'e8'
    rolling_score = 0
    piece_count = 32
    en_passant = ''
    move_counter = 0

    def __init__(self):
        self.board_state = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['-']*8,
                            ['P']*8,
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self.board_string = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNRTrue"

    def apply_move(self, uci_coordinate):
        is_white = self.played_move_count % 2 == 0

        self.move_counter += 1

        # break uci coordinate into location in board state list
        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]

        self.board_state[to_number][to_letter_number] = from_piece
        self.board_state[from_number][from_letter_number] = '-'

        set_en_passant = False

        if from_piece in ('P', 'p'):
            self.move_counter = 0
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

        if to_piece != '-':
            self.move_counter = 0

        self.board_string = self.str_board()
        self.piece_count = self.get_piece_count()

    def make_move(self, uci_coordinate):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state[0] = self.board_state[0].copy()
        board.board_state[1] = self.board_state[1].copy()
        board.board_state[2] = self.board_state[2].copy()
        board.board_state[3] = self.board_state[3].copy()
        board.board_state[4] = self.board_state[4].copy()
        board.board_state[5] = self.board_state[5].copy()
        board.board_state[6] = self.board_state[6].copy()
        board.board_state[7] = self.board_state[7].copy()
        board.attack_squares[0] = self.attack_squares[0].copy()
        board.attack_squares[1] = self.attack_squares[1].copy()
        board.move_list = self.move_list.copy()
        board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        board.white_king_position = self.white_king_position
        board.black_king_position = self.black_king_position
        board.en_passant = self.en_passant
        board.move_counter = self.move_counter
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

        board.repetitions.append(board.board_string)

        board.rolling_score = -board.rolling_score

        return board

    def nullmove(self):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count + 1
        board.board_state[0] = self.board_state[0].copy()
        board.board_state[1] = self.board_state[1].copy()
        board.board_state[2] = self.board_state[2].copy()
        board.board_state[3] = self.board_state[3].copy()
        board.board_state[4] = self.board_state[4].copy()
        board.board_state[5] = self.board_state[5].copy()
        board.board_state[6] = self.board_state[6].copy()
        board.board_state[7] = self.board_state[7].copy()
        board.attack_squares[0] = self.attack_squares[0].copy()
        board.attack_squares[1] = self.attack_squares[1].copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        # clear positions and ep for nullmove
        board.white_king_position = ''
        board.black_king_position = ''
        board.en_passant = ''
        board.rolling_score = -self.rolling_score
        board.move_list = [None]

        return board

    def get_piece_count(self):
        return 64 - string_count(self.board_string, '-')

    def is_endgame(self):
        return self.piece_count <= 16

    def move_sort(self, uci_coordinate):
        return self.calculate_score(uci_coordinate, True)

    def calculate_score(self, uci_coordinate, sorting=False):
        if len(uci_coordinate) == 0:
            return 0

        played_move_count = self.played_move_count

        is_white = True
        offset = 0
        if played_move_count % 2 != 0:
            is_white = False
            offset = 7

        p_offset = -1 if is_white else 1
        row = 7 if is_white else 0

        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        local_score = 0

        from_piece = self.board_state[from_number][from_letter_number].lower()
        from_score_piece = from_piece

        if self.is_endgame():
            if from_score_piece == 'k':
                from_score_piece = 'ke'
            if from_score_piece == 'p':
                local_score += 20
                from_score_piece = 'pe'

        to_piece = self.board_state[to_number][to_letter_number].lower()

        local_score += ALLPSQT[from_score_piece][abs(to_number - offset)][to_letter_number] - \
                        ALLPSQT[from_score_piece][abs(from_number - offset)][from_letter_number]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece][abs(to_number - offset)][to_letter_number]

            if sorting:
                local_score += 100

        if from_piece == 'k':
            if abs(from_letter_number - to_letter_number) == 2:
                if sorting:
                    local_score += 200

                if uci_coordinate[2] == 'g':
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 1] - \
                                    ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1]
                else:
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1] - \
                                    ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 2]
            elif from_piece in ('K', 'k') and played_move_count > 15 and not self.is_endgame():
                if sorting:
                    local_score -= 200
            if to_number + p_offset in range(8):
                if self.board_state[to_number + p_offset][to_letter_number].lower() == 'p':
                    local_score += 10
                if (to_letter_number - 1 > 0) and self.board_state[to_number + p_offset][to_letter_number - 1].lower() == 'p':
                    local_score += 10
                if (to_letter_number + 1 < 8) and self.board_state[to_number + p_offset][to_letter_number + 1].lower() == 'p':
                    local_score += 10
        elif sorting and from_piece == 'b' and played_move_count < 20 and abs(to_number - from_number) > 4:
            local_score -= 300
        elif sorting and from_piece == 'q' and played_move_count < 20 and abs(to_number - from_number) > 2:
            local_score -= 500
        elif from_piece == 'p':
            if uci_coordinate[2:4] == self.en_passant:
                # add in an extra pawn for EP capture
                local_score += ALLPSQT[from_score_piece][abs(to_number - offset)][to_letter_number]
            # else:
                # if not EP, credit pawn structure
                # if to_letter_number > 0:
                #     if self.board_state[to_number - p_offset][to_letter_number - 1].lower() == 'p':
                #         local_score += 30
                # if to_letter_number < 7:
                #     if self.board_state[to_number - p_offset][to_letter_number + 1].lower() == 'p':
                #         local_score += 30

            if len(uci_coordinate) > 4:
                promote = uci_coordinate[4:5]
                # adjust value for promoting from pawn to queen
                local_score += ALLPSQT[promote][abs(to_number - offset)][to_letter_number] - \
                                ALLPSQT['p'][abs(to_number - offset)][to_letter_number]

                # re-set from-piece for check scoring detection
                from_piece = promote

        if sorting and from_piece != 'k':
            local_score += (from_number == row) * 15

            enemy_king_position = self.black_king_position if is_white else self.white_king_position

            for piece_move in TO_MOVES[from_piece]:
                to_column = to_letter_number + piece_move[0]
                to_row = to_number + (piece_move[1] * p_offset)

                dest = ''

                while to_column in range(8) and  to_row in range(8):
                    eval_piece = self.board_state[to_row][to_column]

                    dest = number_to_letter(to_column + 1) + str(abs(to_row - 8))

                    if dest == enemy_king_position or eval_piece != '-' or from_piece in ('n', 'p'):
                        self.attack_squares[is_white].append(dest)
                        break

                    to_column += piece_move[0]
                    to_row += (piece_move[1] * p_offset)

                if dest == enemy_king_position:
                    local_score += 400
                    break

        return local_score

    def str_board(self):
        return string_join(self.board_state[0]) + \
        string_join(self.board_state[1]) + \
        string_join(self.board_state[2]) + \
        string_join(self.board_state[3]) + \
        string_join(self.board_state[4]) + \
        string_join(self.board_state[5]) + \
        string_join(self.board_state[6]) + \
        string_join(self.board_state[7]) + \
        str(self.played_move_count % 2 == 0)

    def generate_valid_moves(self, is_reverse=False):
        is_white = self.played_move_count % 2 == 0

        if is_reverse:
            is_white = not is_white

        self.attack_squares[is_white] = []

        valid_moves = []

        offset = 1
        min_row = 1
        max_row = 6

        valid_pieces = 'prnbqk-'
        if not is_white:
            valid_pieces = 'PRNBQK-'
            min_row = 6
            max_row = 1

        eval_state = self.board_state
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-" or (is_white and piece.islower()) or (not is_white and piece.isupper()):
                    continue
                start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))

                piece_lower = piece.lower()

                if piece == 'P':
                    offset = -1

                # castling
                if piece == 'K':
                    if self.white_castling[1] and start_coordinate == 'e1' and string_join(eval_state[7][5:8]) == '--R' and \
                        not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'f1', 'g1']):
                        valid_moves.append(start_coordinate + 'g1')
                    if self.white_castling[0] and start_coordinate == 'e1' and string_join(eval_state[7][0:4]) == 'R---' and \
                        not any(coordinate in self.attack_squares[0] for coordinate in ['e1', 'd1', 'c1']):
                        valid_moves.append(start_coordinate + 'c1')
                elif piece == 'k':
                    if self.black_castling[1] and start_coordinate == 'e8' and string_join(eval_state[0][5:8]) == '--r' and \
                        not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'f8', 'g8']):
                        valid_moves.append(start_coordinate + 'g8')
                    if self.black_castling[0] and start_coordinate == 'e8' and string_join(eval_state[0][0:4]) == 'r---' and \
                        not any(coordinate in self.attack_squares[1] for coordinate in ['e8', 'd8', 'c8']):
                        valid_moves.append(start_coordinate + 'c8')
                elif piece_lower == 'p' and row == max_row and eval_state[row + offset][column] == '-' and eval_state[row + 2*offset][column] == '-':
                    valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset)))

                for piece_move in TO_MOVES[piece_lower]:
                    to_column = column + piece_move[0]
                    to_row = row + (piece_move[1] * offset)

                    while to_column in range(8) and  to_row in range(8):
                        eval_piece = eval_state[to_row][to_column]

                        dest = number_to_letter(to_column + 1) + str(abs(to_row - 8))

                        if piece_lower == 'p':
                            if (row == min_row and piece_move[0] == 0 and eval_piece == '-') or \
                                (row == min_row and piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces):
                                for prom in ('q', 'r', 'b', 'n'):
                                    valid_moves.append(start_coordinate + dest + prom)
                            else:
                                if (piece_move[0] == 0 and eval_piece == '-') or \
                                    (piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces) or \
                                    dest == self.en_passant:
                                    valid_moves.append(start_coordinate + dest)
                        elif eval_piece in valid_pieces:
                            valid_moves.append(start_coordinate + dest)

                        if piece_move[2]:
                            self.attack_squares[is_white].append(dest)

                        if eval_piece != '-' or piece_lower in ('k', 'n', 'p'):
                            break

                        to_column += piece_move[0]
                        to_row += (piece_move[1] * offset)

        return valid_moves

    def in_check(self, is_white):
        if is_white:
            return self.white_king_position in self.attack_squares[0]

        return self.black_king_position in self.attack_squares[1]

# Entry = namedtuple('Entry', 'value flag depth')

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    critical_time = 0
    tt_bucket = {}

    def reset(self):
        self.v_nodes = 0
        self.v_depth = 0
        self.end_time = 0
        self.critical_time = 0
        self.tt_bucket.clear()

    # def run_perft(self, local_board, original_depth, v_depth):
    #     if v_depth == 0:
    #         return 1

    #     if v_depth != original_depth:
    #         total = 0
    #         for s_move in local_board.generate_valid_moves():
    #             is_in_check = local_board.in_check(local_board.played_move_count % 2 == 0)
    #             moved_board = local_board.make_move(s_move)
    #             all(moved_board.generate_valid_moves(True))

    #             if moved_board.in_check(local_board.played_move_count % 2 == 0):
    #                 continue

    #             if local_board.piece_count != moved_board.piece_count:
    #                 self.perft_captures += 1

    #             if moved_board.in_check(moved_board.played_move_count % 2 == 0):
    #                 self.perft_checks += 1

    #             total += self.run_perft(local_board.make_move(s_move), original_depth, v_depth-1)
    #         return total

    #     per_moves = []
    #     for s_move in local_board.generate_valid_moves():
    #         is_in_check = local_board.in_check(local_board.played_move_count % 2 == 0)
    #         moved_board = local_board.make_move(s_move)
    #         all(moved_board.generate_valid_moves(True))
    #         all(moved_board.generate_valid_moves())

    #         if moved_board.in_check(local_board.played_move_count % 2 == 0):
    #             continue

    #         if local_board.piece_count != moved_board.piece_count:
    #             self.perft_captures += 1

    #         if moved_board.in_check(moved_board.played_move_count % 2 == 0):
    #             self.perft_checks += 1

    #         print (s_move + ": ", end=" ")
    #         x = self.run_perft(local_board.make_move(s_move), original_depth, v_depth-1)
    #         print(x)
    #         per_moves.append(x)

    #     print("Nodes searched: ", sum(per_moves))
    #     print("Captures: ", self.perft_captures, " Checks: ", self.perft_checks)

    def iterative_search(self, local_board):
        start_time = time.time()

        # initial_move = self.tt_moves.get(local_board.board_string)

        # # castling being cached can override the "in check" check
        # if initial_move:
        #     if initial_move in ('e1c1', 'e1g1', 'e8c8', 'e8g8') and local_board.in_check(local_board.played_move_count % 2 == 0):
        #         self.tt_moves[local_board.board_string] = None

        for v_depth in range(1, 100):
            local_board.generate_valid_moves(True)
            local_board.generate_valid_moves()

            local_score = self.search(local_board, v_depth, -MATE_UPPER, MATE_UPPER)

            best_move = self.tt_bucket.get(local_board.board_string)['move']

            elapsed_time = time.time() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time)

            print_stats(str(v_depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move))

            yield v_depth, best_move, local_score

    def search(self, local_board, v_depth, alpha, beta, root_search=True):
        if time.time() > self.critical_time:
            return local_board.rolling_score

        self.v_nodes += 1

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        is_white = local_board.played_move_count % 2 == 0
        pv_node = (alpha != beta - 1)
        is_in_check = local_board.in_check(is_white)

        v_depth = max(0, v_depth)

        if v_depth == 0:
            return self.q_search(local_board, alpha, beta)

        if not root_search and local_board.repetitions.count(local_board.board_string) > 1 or local_board.move_counter >= 100:
            return 0

        tt_entry = self.tt_bucket.get((local_board.board_string), {'value': 2*MATE_UPPER, 'flag': UPPER, 'depth': 0, 'move': None})

        if tt_entry['depth'] >= v_depth and not pv_node and abs(tt_entry['value']) < MATE_UPPER:
            if tt_entry['flag'] == EXACT or \
            (tt_entry['flag'] == LOWER and tt_entry['value'] >= beta) or \
            (tt_entry['flag'] == UPPER and tt_entry['value'] <= alpha):
                return tt_entry['value']

        original_alpha = alpha

        current_eval = tt_entry['value'] if tt_entry['value'] < MATE_UPPER else local_board.rolling_score

        if not pv_node and not is_in_check and v_depth <= 8 and current_eval - 85 * v_depth > beta:
            return current_eval

        best_score = local_board.rolling_score if v_depth == 0 else -MATE_UPPER - 1
        local_score = -MATE_UPPER

        pieces = 'RNBQ' if is_white else 'rnbq'

        if not pv_node and not is_in_check and current_eval >= beta and \
            v_depth >= 2 and pieces in local_board.board_string and \
            local_board.move_list[0]:

            local_score = -self.search(local_board.nullmove(), v_depth - 3, -beta, -beta+1, False)

            if local_score >= beta:
                return beta

        if not pv_node and not is_in_check and local_board.move_list[0] is not None:
            if tt_entry['move'] and local_board.calculate_score(tt_entry['move']) > 220:
                local_score = max(local_score, -self.search(local_board.make_move(tt_entry['move']), v_depth - 1, -beta, -alpha, False))

                if local_score >= beta:
                    return beta

        played_moves = 0

        best_move = None

        v_depth += is_in_check

        for s_move in sorted(local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
            current_move_score = local_board.calculate_score(s_move)

            moved_board = local_board.make_move(s_move)
            # check for check
            moved_board.generate_valid_moves(True)
            moved_board.generate_valid_moves()

            if moved_board.in_check(is_white):
                continue

            played_moves += 1

            is_quiet = current_move_score < 200 and local_board.piece_count == moved_board.piece_count and not moved_board.in_check(not is_white)

            reduce_depth = 2 if not is_quiet and v_depth > 2 and played_moves > 3 else 0

            if reduce_depth > 0:
                local_score = -self.search(moved_board, v_depth - reduce_depth, -alpha-1, -alpha, False)

            if (reduce_depth > 0 and local_score > alpha) or (not reduce_depth and not(pv_node and played_moves <= 3)):
                local_score = -self.search(moved_board, v_depth - 1, -alpha-1, -alpha, False)

            if pv_node and (played_moves <= 3 or local_score > alpha):
                local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha, False)

            if local_score > best_score:
                best_move = s_move
                best_score = local_score

                if local_score > alpha:
                    alpha = local_score

                    if alpha >= beta:
                        break

        if played_moves == 0:
            return -MATE_UPPER if is_in_check else 0

        #update TT
        tt_entry['value'] = best_score
        tt_entry['move'] = best_move
        if best_score <= original_alpha:
            tt_entry['flag'] = UPPER
        elif best_score >= beta:
            tt_entry['flag'] = LOWER
        else:
            tt_entry['flag'] = EXACT

        self.tt_bucket[local_board.board_string] = tt_entry

        return best_score

    def q_search(self, local_board, alpha, beta):
        tt_entry = self.tt_bucket.get((local_board.board_string), {'value': 2*MATE_UPPER, 'flag': UPPER, 'depth': 0, 'move': None})

        if tt_entry['flag'] == EXACT or \
            (tt_entry['flag'] == LOWER and tt_entry['value'] >= beta) or \
            (tt_entry['flag'] == UPPER and tt_entry['value'] <= alpha):
            if abs(tt_entry['value']) < MATE_UPPER:
                return tt_entry['value']

        stand_pat = local_board.rolling_score
        best_score = stand_pat
        is_white = local_board.played_move_count % 2 == 0

        alpha = max(alpha, best_score)

        if alpha >= beta:
            return stand_pat

        for s_move in sorted(local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
            current_move_score = local_board.calculate_score(s_move)

            moved_board = local_board.make_move(s_move)
            # check for check
            moved_board.generate_valid_moves(True)
            moved_board.generate_valid_moves()

            is_quiet = current_move_score < 200 and local_board.piece_count == moved_board.piece_count and not moved_board.in_check(not is_white)

            if moved_board.in_check(is_white) or is_quiet:
                continue

            local_score = -self.q_search(moved_board, -beta, -alpha)

            if local_score > best_score:
                best_score = local_score

                if local_score > alpha:
                    alpha = local_score

            if alpha > beta:
                return best_score

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
            elif line == "isready":
                print_to_terminal("readyok")
            elif line.startswith("position"):
                moves = line.split()
                game_board = Board()
                for position_move in moves[3:]:
                    game_board = game_board.make_move(position_move)
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
                    # depth input can be commented out to save space since engine will be run on time
                    elif arg == 'depth':
                        searcher.v_depth = int(args[key + 1])
                    # elif arg == 'perft':
                    #     searcher.v_depth = int(args[key + 1])
                    #     is_perft = True

                # if is_perft:
                #     # 1) start pos
                #     # 2) Kiwipete: position startpos moves b1c3 b7b5 d2d4 e7e6 e2e4 c8a6 c1d2 h7h5 d1f3 g7g6 f1e2 h5h4 g1h3 f8g7 h3f4 g8e7 f4d3 e7d5 d3e5 d5f6 d4d5 d8e7 d2e3 b5b4 e3d2 b8c6 d2e3 c6a5 e3d2 a5c4 d2e3 c4b6 e3d2 h4h3
                #     # 3) Tricky Steve: position startpos moves d2d3 c7c6 e2e4 e7e5 d3d4 f8e7 d4e5 d7d6 e5d6 g8f6 f1c4 f6e4 d6d7 e8f8 g1e2 e4f2
                #     start_time = time.time()
                #     searcher.perft_checks = 0
                #     searcher.perft_captures = 0
                #     searcher.run_perft(game_board, searcher.v_depth, searcher.v_depth)
                #     continue

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0

                move_time = (black_time / 20000)
                searcher.critical_time = time.time() + (black_time / 1000) - 3
                if is_white:
                    move_time = (white_time / 20000)
                    searcher.critical_time = time.time() + (white_time / 1000) - 3

                move_time = max(move_time, 3)

                searcher.end_time = time.time() + move_time

                searcher.v_nodes = 0

                s_move = None

                start = time.time()
                for v_depth, s_move, best_score in searcher.iterative_search(game_board):
                    if (searcher.end_time - time.time()) < 2:
                        searcher.v_depth = 3

                    if v_depth >= searcher.v_depth or time.time() > searcher.end_time:
                        break

                print_to_terminal("bestmove " + str(s_move))

                # if len(searcher.tt_moves) > 9e5:
                #     searcher.tt_moves.clear()
                if len(searcher.tt_bucket) > 2e6:
                    searcher.tt_bucket.clear()

        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()