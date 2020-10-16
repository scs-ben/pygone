#!/usr/bin/env pypy3
import math, sys, time

t = time.time

# values are copied from SF
PIECEPOINTS = {'p': 136, 'n': 782, 'b': 830, 'r': 1289, 'q': 2529, 'k': 32e4}

ALLPSQT = {
    'p':  [[0, 0, 0, 0, 0, 0, 0, 0],
           [-10, 6, -5, -11, -2, -14, 12, -1],
           [-6, -8, 5, 11, -14, 0, -12, -14],
           [6, -3, -10, 1, 12, 6, -12, 1],
           [-9, -18, 8, 22, 33, 25, -4, -16],
           [-11, -10, 15, 22, 26, 28, 4, -24],
           [0, -5, 10, 13, 21, 17, 6, -3],
           [0, 0, 0, 0, 0, 0, 0, 0]],
    'n': [[-200, -80, -53, -32, -32, -53, -80, -200],
          [-67, -21, 6, 37, 37, 6, -21, -67],
          [-11, 28, 63, 55, 55, 63, 28, -11],
          [-29, 13, 42, 52, 52, 42, 13, -29],
          [-28, 5, 41, 47, 47, 41, 5, -28],
          [-64, -20, 4, 19, 19, 4, -20, -64],
          [-79, -39, -24, -9, -9, -24, -39, -79],
          [-169, -96, -80, -79, -79, -80, -96, -169]],
    'b': [[-48, -3, -12, -25, -25, -12, -3, -48],
          [-21, -19, 10, -6, -6, 10, -19, -21],
          [-17, 4, -1, 8, 8, -1, 4, -17],
          [-7, 30, 23, 28, 28, 23, 30, -7],
          [1, 8, 26, 37, 37, 26, 8, 1],
          [-8, 24, -3, 15, 15, -3, 24, -8],
          [-18, 7, 14, 3, 3, 14, 7, -18],
          [-44, -4, -11, -28, -28, -11, -4, -44]],
    'r': [[-22, -24, -6, 4, 4, -6, -24, -22],
          [-8, 6, 10, 12, 12, 10, 6, -8],
          [-24, -4, 4, 10, 10, 4, -4, -24],
          [-24, -12, -1, 6, 6, -1, -12, -24],
          [-13, -5, -4, -6, -6, -4, -5, -13],
          [-21, -7, 3, -1, -1, 3, -7, -21],
          [-18, -10, -5, 9, 9, -5, -10, -18],
          [-24, -13, -7, 2, 2, -7, -13, -24]],
    'q': [[-2, -2, 1, -2, -2, 1, -2, -2],
          [-5, 6, 10, 8, 8, 10, 6, -5],
          [-4, 10, 6, 8, 8, 6, 10, -4],
          [0, 14, 12, 5, 5, 12, 14, 0],
          [4, 5, 9, 8, 8, 9, 5, 4],
          [-3, 6, 13, 7, 7, 13, 6, -3],
          [-3, 5, 8, 12, 12, 8, 5, -3],
          [3, -5, -5, 4, 4, -5, -5, 3]],
    'k': [[64, 87, 49, 0, 0, 49, 87, 64],
          [87, 120, 64, 25, 25, 64, 120, 87],
          [122, 159, 85, 36, 36, 85, 159, 122],
          [145, 176, 112, 69, 69, 112, 176, 145],
          [169, 191, 136, 108, 108, 136, 191, 169],
          [198, 253, 168, 120, 120, 168, 253, 198],
          [277, 305, 241, 183, 183, 241, 305, 277],
          [272, 325, 273, 190, 190, 273, 325, 272]],
}

for set_piece, _ in ALLPSQT.items():
    for set_row in range(8):
        for set_column in range(8):
            ALLPSQT[set_piece][set_row][set_column] += PIECEPOINTS[set_piece]

EXACT = 1
UPPER = 2
LOWER = 3

MATE_LOWER = PIECEPOINTS['k'] - 10*PIECEPOINTS['q'] #11e3
MATE_UPPER = PIECEPOINTS['k'] + 10*PIECEPOINTS['q'] #29e3

TO_MOVES = {
    # (column, row, can_capture)
    'k': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), (1, 1, 1), \
          (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'q': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), (1, 1, 1), \
          (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'r': [(0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1)],
    'b': [(1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1)],
    'n': [(1, -2, 1), (-1, -2, 1), (2, -1, 1), (-2, -1, 1), (1, 2, 1), \
          (-1, 2, 1), (2, 1, 1), (-2, 1, 1)],
    'p': [(0, 1, 0), (1, 1, 1), (-1, 1, 1)]
}

def number_to_letter(to_number):
    return chr(to_number + 96)

def print_to_terminal(print_string):
    print(print_string, flush=True)

def print_stats(v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
    print_to_terminal(f"info depth {v_depth} score cp {v_score} time {v_time} nodes {v_nodes} nps {v_nps} pv {v_pv}")

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
    for ch in haystack:
        if ch == needle:
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

        if self.board_state[to_number][to_letter_number] != '-':
            self.move_counter = 0

        self.board_state[to_number][to_letter_number] = from_piece
        self.board_state[from_number][from_letter_number] = '-'

        set_en_passant = False

        if from_piece.lower() == 'p':
            self.move_counter = 0
            set_en_passant = abs(from_number - to_number) == 2
            en_passant_offset = -1 if is_white else 1
            if set_en_passant:
                self.en_passant = uci_coordinate[0:1] + str(int(uci_coordinate[3:4]) + en_passant_offset)
            elif uci_coordinate[2:4] == self.en_passant:
                self.board_state[to_number - en_passant_offset][to_letter_number] = '-'

            if len(uci_coordinate) > 4:
                self.board_state[to_number][to_letter_number] = uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5]
        elif from_piece.lower() == 'k':
            if is_white:
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            if uci_coordinate in ('e1g1', 'e8g8'):
                self.board_state[to_number][to_letter_number + 1] = '-'
                self.board_state[from_number][from_letter_number + 1] = 'R' if is_white else 'r'
            elif uci_coordinate in ('e1c1', 'e8c8'):
                self.board_state[to_number][to_letter_number - 2] = '-'
                self.board_state[from_number][from_letter_number - 1] = 'R' if is_white else 'r'

        if not set_en_passant:
            self.en_passant = ''

        self.board_string = self.str_board()
        self.piece_count = self.get_piece_count()

    def make_move(self, uci_coordinate):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        for row in range(8):
            board.board_state[row] = self.board_state[row].copy()
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
        board.rolling_score = -(self.rolling_score + self.calculate_score(uci_coordinate))

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

        # board.rolling_score = -board.rolling_score

        return board

    def nullmove(self):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count + 1
        for row in range(8):
            board.board_state[row] = self.board_state[row].copy()
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
        return self.piece_count < 16

    def move_sort(self, uci_coordinate):
        return self.calculate_score(uci_coordinate, True)

    def calculate_score(self, uci_coordinate, sorting=False, reverse_capture=False):
        if not uci_coordinate:
            return 0

        is_white = self.played_move_count % 2 == 0
        offset = 0 if is_white else 7
        p_offset = -1 if is_white else 1
        p_piece = 'P' if is_white else 'p'

        (from_letter_number, from_number, to_letter_number, to_number) = unpack_coordinate(uci_coordinate)

        local_score = 0

        from_piece = self.board_state[from_number][from_letter_number].lower()

        to_piece = self.board_state[to_number][to_letter_number].lower()

        local_score += ALLPSQT[from_piece][abs(to_number - offset)][to_letter_number] - \
                        ALLPSQT[from_piece][abs(from_number - offset)][from_letter_number]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece][abs(to_number - offset)][to_letter_number]

            if sorting:
                local_score += min(2, (PIECEPOINTS[to_piece] / 10) - (PIECEPOINTS[from_piece] / 10))

        if from_piece == 'k':
            if abs(from_letter_number - to_letter_number) == 2:
                if sorting:
                    local_score += 500

                if uci_coordinate[2] == 'g':
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 1] - \
                                    ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1]
                else:
                    local_score += ALLPSQT['r'][abs(to_number - offset)][to_letter_number + 1] - \
                                    ALLPSQT['r'][abs(to_number - offset)][to_letter_number - 2]
            elif sorting and not self.is_endgame():
                local_score -= 1000
        elif sorting and self.played_move_count < 30 and from_piece == 'q' and abs(to_number - offset) > 3:
            local_score -= 300
        elif from_piece == 'p':
            if sorting and self.played_move_count < 30:
                local_score += ALLPSQT[from_piece][abs(to_number - offset)][to_letter_number] / 10
            if uci_coordinate[2:4] == self.en_passant:
                # add in an extra pawn for EP capture
                local_score += ALLPSQT[from_piece][abs(to_number - offset)][to_letter_number]
            elif len(uci_coordinate) > 4:
                promote = uci_coordinate[4:5]
                # adjust value for promoting from pawn to queen
                local_score += ALLPSQT[promote][abs(to_number - offset)][to_letter_number] - \
                                ALLPSQT['p'][abs(to_number - offset)][to_letter_number]

                # re-set from-piece for check scoring detection
                from_piece = promote

        return local_score

    def str_board(self):
        """Return string reprsentation of board state"""
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
        """Return list of valid (maybe illegal) moves"""
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
                elif piece_lower == 'p' and row == max_row and eval_state[row + offset][column] == '-' and \
                    eval_state[row + 2*offset][column] == '-':
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
        king_position = self.white_king_position if is_white else self.black_king_position
        offset = 1

        eval_state = self.board_state
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-" or (is_white and piece.isupper()) or (not is_white and piece.islower()):
                    continue

                if piece == 'P':
                    offset = -1

                piece = piece.lower()

                for piece_move in TO_MOVES[piece]:
                    to_column = column + piece_move[0]
                    to_row = row + (piece_move[1] * offset)

                    while to_column in range(8) and  to_row in range(8):
                        eval_piece = eval_state[to_row][to_column]

                        dest = number_to_letter(to_column + 1) + str(abs(to_row - 8))

                        if piece_move[2] and dest == king_position:
                            return True

                        if eval_piece != '-' or piece in ('k', 'n', 'p'):
                            break

                        to_column += piece_move[0]
                        to_row += (piece_move[1] * offset)

        return False



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
    #             # all(moved_board.generate_valid_moves(True))

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
    #         # all(moved_board.generate_valid_moves(True))
    #         # all(moved_board.generate_valid_moves())

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
        start_time = t()

        # initial_move = self.tt_moves.get(local_board.board_string)

        # # castling being cached can override the "in check" check
        # if initial_move:
        #     if initial_move in ('e1c1', 'e1g1', 'e8c8', 'e8g8') and local_board.in_check(local_board.played_move_count % 2 == 0):
        #         self.tt_moves[local_board.board_string] = None

        alpha = -MATE_UPPER
        beta = MATE_UPPER

        for v_depth in range(1, 100):
            all(local_board.generate_valid_moves(True))
            all(local_board.generate_valid_moves())

            if v_depth > 2:
                alpha = local_score - 10
                beta = local_score + 10

            local_score = self.search(local_board, v_depth, alpha, beta)

            if local_score <= alpha or local_score >= beta:
                local_score = self.search(local_board, v_depth, -MATE_UPPER, MATE_UPPER)

            if t() < self.critical_time:
                best_move = self.tt_bucket.get(local_board.board_string)
                if best_move:
                    best_move = best_move['tt_move']
            else:
                break

            elapsed_time = t() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time)

            print_stats(str(v_depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move))

            yield v_depth, best_move, local_score

    def search(self, local_board, v_depth, alpha, beta, root_search=True, q_search=True):
        if t() > self.critical_time:
            return local_board.rolling_score

        self.v_nodes += 1

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        is_white = local_board.played_move_count % 2 == 0
        pv_node = (alpha != beta - 1)
        is_in_check = local_board.in_check(is_white)

        v_depth = max(0, v_depth)

        # if v_depth == 0:
        #     if q_search:
        #         return self.q_search(local_board, alpha, beta)
        #     else:
        #         return local_board.rolling_score

        if not root_search and (local_board.repetitions.count(local_board.board_string) > 1 or local_board.move_counter >= 100):
            return 0

        tt_entry = self.tt_bucket.get((local_board.board_string), {'tt_value': 2*MATE_UPPER, 'tt_flag': UPPER, 'tt_depth': 0, 'tt_move': None})

        if tt_entry['tt_depth'] >= v_depth: # and not pv_node:
            if tt_entry['tt_flag'] == EXACT or \
            (tt_entry['tt_flag'] == LOWER and tt_entry['tt_value'] >= beta) or \
            (tt_entry['tt_flag'] == UPPER and tt_entry['tt_value'] <= alpha):
                return tt_entry['tt_value']

        original_alpha = alpha

        current_eval = tt_entry['tt_value'] if tt_entry['tt_value'] < MATE_UPPER else local_board.rolling_score

        if not pv_node and not is_in_check and v_depth <= 7 and current_eval - 85 * v_depth > beta:
            return current_eval

        best_score = local_board.rolling_score if v_depth == 0 else -MATE_UPPER - 1
        local_score = -MATE_UPPER

        pieces = 'RNBQ' if is_white else 'rnbq'

        if v_depth > 0 and not pv_node and not is_in_check and current_eval >= beta and \
            v_depth >= 2 and pieces in local_board.board_string and \
            local_board.move_list[0]:

            local_score = -self.search(local_board.nullmove(), v_depth - 3, -beta, -beta+1, False, False)

            if local_score >= beta:
                return beta

        if v_depth > 0 and not pv_node and not is_in_check and local_board.move_list[0] and tt_entry['tt_move']:
            local_score = -self.search(local_board.make_move(tt_entry['tt_move']), v_depth - 1, -beta, -alpha, False, True)

            if local_score >= beta:
                return beta

        played_moves = 0

        best_move = None

        v_depth += is_in_check

        for s_move in sorted(local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
            current_move_score = local_board.calculate_score(s_move)

            moved_board = local_board.make_move(s_move)
            # check for check
            # moved_board.generate_valid_moves(True)
            # moved_board.generate_valid_moves()

            if moved_board.in_check(is_white):
                continue

            played_moves += 1

            is_noisy = current_move_score > 220 # local_board.piece_count != moved_board.piece_count or current_move_score > 800 # or moved_board.in_check(not is_white)

            if (v_depth > 0 and played_moves < 3) or (v_depth == 0 and is_noisy):
                local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha, False, is_noisy)
            elif v_depth > 0:
                reduce_depth = 1

                if v_depth > 2 and not is_noisy:
                    reduce_depth = 2

                local_score = -self.search(moved_board, v_depth - reduce_depth, -alpha-1, -alpha, False, is_noisy)
                if reduce_depth > 1 and local_score > alpha:
                    local_score = -self.search(moved_board, v_depth - 1, -alpha-1, -alpha, False, is_noisy)

                if alpha < local_score < beta:
                    local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha, False, is_noisy)

            if local_score > best_score:
                best_move = s_move
                best_score = local_score

                if local_score > alpha:
                    alpha = local_score

                    if alpha >= beta:
                        break

        if played_moves == 0:
            return -MATE_UPPER if is_in_check else 0

        #update TT only if we are not in time cut
        if t() < self.critical_time and v_depth > 0:
            tt_entry['tt_value'] = best_score
            tt_entry['tt_move'] = best_move
            if best_score <= original_alpha:
                tt_entry['tt_flag'] = UPPER
            elif best_score >= beta:
                tt_entry['tt_flag'] = LOWER
            else:
                tt_entry['tt_flag'] = EXACT

            self.tt_bucket[local_board.board_string] = tt_entry

        return best_score

    # def q_search(self, local_board, alpha, beta):
    #     tt_entry = self.tt_bucket.get((local_board.board_string), {'tt_value': 2*MATE_UPPER, 'tt_flag': UPPER, 'tt_depth': 0, 'tt_move': None})

    #     if tt_entry['tt_flag'] == EXACT or \
    #         (tt_entry['tt_flag'] == LOWER and tt_entry['tt_value'] >= beta) or \
    #         (tt_entry['tt_flag'] == UPPER and tt_entry['tt_value'] <= alpha):
    #         return tt_entry['tt_value']

    #     stand_pat = local_board.rolling_score
    #     best_score = stand_pat
    #     is_white = local_board.played_move_count % 2 == 0

    #     alpha = max(alpha, best_score)

    #     if alpha >= beta:
    #         return stand_pat

    #     for s_move in sorted(local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
    #         current_move_score = local_board.calculate_score(s_move)

    #         moved_board = local_board.make_move(s_move)
    #         # check for check
    #         moved_board.generate_valid_moves(True)
    #         moved_board.generate_valid_moves()

    #         is_noisy = local_board.piece_count != moved_board.piece_count or current_move_score > 800 or moved_board.in_check(not is_white)

    #         if moved_board.in_check(is_white) or not is_noisy:
    #             continue

    #         local_score = -self.q_search(moved_board, -beta, -alpha)

    #         if local_score > best_score:
    #             best_score = local_score

    #             if local_score > alpha:
    #                 alpha = local_score

    #         if alpha > beta:
    #             return best_score

    #     return best_score

game_board = Board()
searcher = Search()

while 1:
    try:
        line = input()
        if line == "quit":
            sys.exit()
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
            searcher.v_depth = 30
            move_time = 1e8
            is_white = game_board.played_move_count % 2 == 0

            # is_perft = False

            args = line.split()
            for key, arg in enumerate(args):
                if arg == 'wtime' and is_white or arg == 'btime' and not is_white:
                    move_time = int(args[key + 1]) / 1e3
                # depth input can be commented out to save space since engine will be run on time
                elif arg == 'depth':
                    searcher.v_depth = int(args[key + 1])
            #     elif arg == 'perft':
            #         searcher.v_depth = int(args[key + 1])
            #         is_perft = True

            # if is_perft:
            #     # 1) start pos
            #     # 2) Kiwipete: position startpos moves b1c3 b7b5 d2d4 e7e6 e2e4 c8a6 c1d2 h7h5 d1f3 g7g6 f1e2 h5h4 g1h3 f8g7 h3f4 g8e7 f4d3 e7d5 d3e5 d5f6 d4d5 d8e7 d2e3 b5b4 e3d2 b8c6 d2e3 c6a5 e3d2 a5c4 d2e3 c4b6 e3d2 h4h3
            #     # 3) Tricky Steve: position startpos moves d2d3 c7c6 e2e4 e7e5 d3d4 f8e7 d4e5 d7d6 e5d6 g8f6 f1c4 f6e4 d6d7 e8f8 g1e2 e4f2
            #     start_time = t()
            #     searcher.perft_checks = 0
            #     searcher.perft_captures = 0
            #     searcher.run_perft(game_board, searcher.v_depth, searcher.v_depth)
            #     continue

            div_time = 12 if game_board.played_move_count < 30 else 4

            searcher.critical_time = t() + (move_time) - 1
            move_time = max(3, move_time / div_time)

            searcher.end_time = t() + move_time

            searcher.v_nodes = 0

            s_move = None

            start = t()
            for v_depth, s_move, best_score in searcher.iterative_search(game_board):
                if (searcher.end_time - t()) < 1:
                    searcher.v_depth = 3

                if v_depth >= searcher.v_depth or t() > searcher.end_time:
                    break

            ponder_board = game_board.make_move(s_move)
            ponder_bucket = searcher.tt_bucket.get(ponder_board.board_string)
            ponder = ""
            if ponder_bucket:
                ponder = f" ponder {ponder_bucket['tt_move']}"

            print_to_terminal(f"bestmove {str(s_move)}{ponder}")

            # print_to_terminal(f"bestmove {str(s_move)}")

            # if len(searcher.tt_moves) > 9e5:
            #     searcher.tt_moves.clear()
            if len(searcher.tt_bucket) > 2e6:
                searcher.tt_bucket.clear()

    except (KeyboardInterrupt, SystemExit):
        sys.exit()
    except Exception as exc:
        print_to_terminal(exc)
        raise
