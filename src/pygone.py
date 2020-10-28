#!/usr/bin/env pypy3
import copy, math, sys, time
from multiprocessing import Process

t = time.time

# values are copied from SF
PIECEPOINTS = {'p': 100, 'n': 290, 'b': 300, 'r': 600, 'q': 1250, 'k': 2e4}

ALLPSQT = {
    'p': (0, 0, 0, 0, 0, 0, 0, 0,
          50, 50, 50, 50, 50, 50, 50, 50,
          20, 20, 20, 20, 20, 20, 20, 20,
          10, 10, 15, 25, 25, 15, 10, 10,
          0, 0, 0, 20, 20, 0, 0, 0,
          5, -5, -5, 5, 5, -5, -5, 5,
          5, 10, 10, -20, -20, 10, 10, 5,
          0, 0, 0, 0, 0, 0, 0, 0),
    'n': (-50, -40, -30, -30, -30, -30, -40, -50,
          -40, -20, 5, 5, 5, 5, -20, -40,
          -30, 5, 10, 15, 15, 10, 5, -30,
          -30, 5, 15, 25, 25, 15, 5, -30,
          -30, 5, 15, 25, 25, 15, 5, -30,
          -30, 10, 10, 10, 10, 10, 10, -30,
          -40, -20, 0, 5, 5, 0, -20, -40,
          -50, -40, -30, -30, -30, -30, -40, -50),
    'b': (-20, -10, -10, -10, -10, -10, -10, -20,
          -10, 0, 0, 0, 0, 0, 0, -10,
          -10, 0, 5, 10, 10, 5, 0, -10,
          0, 5, 5, 10, 10, 5, 5, 0,
          0, 0, 10, 10, 10, 10, 0, 0,
          -10, 10, 10, 10, 10, 10, 10, -10,
          -10, 5, 0, 0, 0, 0, 5, -10,
          -20, -10, -10, -10, -10, -10, -10, -20),
    'r': (0, 0, 0, 0, 0, 0, 0, 0,
          5, 10, 10, 10, 10, 10, 10, 5,
          -10, 0, 5, 5, 5, 5, 0, -10,
          -5, 0, 5, 5, 5, 5, 0, -5,
          0, 0, 5, 5, 5, 5, 0, -5,
          -10, 5, 5, 5, 5, 5, 0, -10,
          -5, 0, 0, 5, 0, 5, 0, -5,
          0, 0, 0, 5, 5, 0, 0, 0),
    'q': (-20, -10, -10, -5, -5, -10, -10, -20,
          -10, 5, 5, 5, 5, 5, 5, -10,
          -10, 5, 5, 5, 5, 5, 5, -10,
          -5, 5, 5, 5, 5, 5, 5, -5,
          -5, 5, 5, 5, 5, 5, 5, -5,
          -10, 5, 5, 5, 5, 5, 5, -10,
          -10, 0, 5, 0, 0, 0, 0, -10,
          -20, -10, -10, -5, -5, -10, -10, -20),
    'k': (-50, -40, -30, -20, -20, -30, -40, -50,
          -20, -20, -10, 0, 0, -10, -20, -20,
          -20, -10, 20, 30, 30, 20, -10, -20,
          -20, -10, 30, 40, 40, 30, -10, -20,
          -20, -10, 30, 40, 40, 30, -10, -20,
          -20, -10, 20, 30, 30, 20, -10, -20,
          20, 20, -40, -40, -40, -40, 20, 20,
          0, 10, 30, 0, 0, 10, 30, 0)
}

for set_piece, board in ALLPSQT.items():
    prow = lambda row: (0,) + tuple(piece+PIECEPOINTS[set_piece] for piece in row) + (0,)
    ALLPSQT[set_piece] = sum((prow(board[column*8:column*8+8]) for column in range(8)), ())
    ALLPSQT[set_piece] = (0,)*20 + ALLPSQT[set_piece] + (0,)*20

EXACT = 1
UPPER = 2
LOWER = 3

MATE_LOWER = PIECEPOINTS['k'] - 10*PIECEPOINTS['q']
MATE_UPPER = PIECEPOINTS['k'] + 10*PIECEPOINTS['q']

PROTECTED_PAWN_VALUE = 30
STACKED_PAWN_VALUE = 40

TO_MOVES = {
    # (column, row, can_capture)
    'k': [(0, 10), (0, -10), (1, 0), (-1, 0), (1, 10), \
          (1, -10), (-1, 10), (-1, -10)],
    'q': [(0, 10), (0, -10), (1, 0), (-1, 0), (1, 10), \
          (1, -10), (-1, 10), (-1, -10)],
    'r': [(0, 10), (0, -10), (1, 0), (-1, 0)],
    'b': [(1, 10), (1, -10), (-1, 10), (-1, -10)],
    'n': [(1, -20), (-1, -20), (2, -10), (-2, -10), (1, 20), \
          (-1, 20), (2, 10), (-2, 10)],
    'p': [(0, -10), (1, -10), (-1, -10)]
}

def number_to_letter(to_number):
    return chr(to_number + 96)

def print_to_terminal(print_string):
    print(print_string, flush=True)

def print_stats(v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
    print_to_terminal(f"info depth {v_depth} score cp {v_score} time {v_time} nodes {v_nodes} nps {v_nps} pv {v_pv}")

def unpack_coordinate(uci_coordinate):
    return (coordinate_to_position(uci_coordinate[0:2]),
            coordinate_to_position(uci_coordinate[2:4]))

def position_to_coordinate(board_position):
    return number_to_letter(board_position % 10) + str(abs(board_position // 10 - 10))

def coordinate_to_position(coordinate):
    return 10 * (abs(int(coordinate[1]) - 8) + 2) + (ord(coordinate[0]) - 97) + 1

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
    board_string = ''
    played_move_count = 0
    move_list = []
    repetitions = []
    white_castling = [True, True]
    black_castling = [True, True]
    white_king_position = 'e1'
    black_king_position = 'e8'
    rolling_score = 0
    piece_count = 32
    en_passant = ''
    move_counter = 0

    def __init__(self):
        self.board_state = (
            '..........' #   0 -  9
            '..........' #  10 - 19
            '.rnbqkbnr.' #  20 - 29
            '.pppppppp.' #  30 - 39
            '.--------.' #  40 - 49
            '.--------.' #  50 - 59
            '.--------.' #  60 - 69
            '.--------.' #  70 - 79
            '.PPPPPPPP.' #  80 - 89
            '.RNBQKBNR.' #  90 - 99
            '..........' # 100 -109
            '..........' # 110 -119
            )

    def mutate_board(self, board_position, piece):
      self.board_state = self.board_state[:board_position] + piece + self.board_state[board_position + 1:]

    def apply_move(self, uci_coordinate):
        is_white = self.played_move_count % 2 == 0

        self.move_counter += 1

        # break uci coordinate into location in board state list
        (from_number, to_number) = unpack_coordinate(uci_coordinate)

        from_piece = self.board_state[from_number].lower()

        if self.board_state[to_number] != '-':
            self.move_counter = 0

        self.mutate_board(to_number, self.board_state[from_number])
        self.mutate_board(from_number, '-')

        set_en_passant = False

        if from_piece == 'p':
            self.move_counter = 0
            set_en_passant = abs(from_number - to_number) == 20
            en_passant_offset = -1 if is_white else 1
            if set_en_passant:
                self.en_passant = uci_coordinate[0:1] + str(int(uci_coordinate[3:4]) + en_passant_offset)
            elif uci_coordinate[2:4] == self.en_passant:
                self.mutate_board(to_number - 10 * en_passant_offset, '-')

            if len(uci_coordinate) > 4:
                self.mutate_board(to_number, uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5])
        elif from_piece == 'k':
            if is_white:
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            if uci_coordinate in ('e1g1', 'e8g8'):
                self.mutate_board(to_number + 1, '-')
                self.mutate_board(from_number + 1, 'R' if is_white else 'r')
            elif uci_coordinate in ('e1c1', 'e8c8'):
                self.mutate_board(to_number - 2, '-')
                self.mutate_board(from_number - 1, 'R' if is_white else 'r')

        if not set_en_passant:
            self.en_passant = ''

        self.board_string = self.str_board()
        self.piece_count = self.get_piece_count()

    def make_move(self, uci_coordinate):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = self.board_copy()
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
        board.rolling_score = -board.rolling_score

        board.repetitions.append(board.board_string)

        return board

    def nullmove(self):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = self.board_copy()
        board.played_move_count += 1
        board.rolling_score = -self.rolling_score
        board.move_list = [None]

        return board

    def board_copy(self):
        """ copy the board, does not copy the score """
        board = Board()
        board.played_move_count = self.played_move_count
        board.white_king_position = self.white_king_position
        board.black_king_position = self.black_king_position
        board.board_string = self.board_string
        board.piece_count = self.piece_count
        board.en_passant = self.en_passant
        board.move_counter = self.move_counter
        board.board_state = self.board_state
        board.move_list = self.move_list.copy()
        board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()

        return board

    def get_piece_count(self):
        return 64 - string_count(self.board_string, '-')

    def is_endgame(self):
        return self.piece_count < 14 or (self.piece_count < 20 and 'q' not in self.board_string.lower())

    def move_sort(self, uci_coordinate):
        return self.calculate_score(uci_coordinate, True)

    def calculate_score(self, uci_coordinate, sorting=False):
        if not uci_coordinate:
            return 0

        is_white = self.played_move_count % 2 == 0
        offset = 0 if is_white else 119
        p_offset = -10 if is_white else 10
        p_piece = 'P' if is_white else 'p'
        is_endgame = self.is_endgame()

        (from_number, to_number) = unpack_coordinate(uci_coordinate)

        local_score = 0

        from_piece = self.board_state[from_number].lower()

        to_piece = self.board_state[to_number].lower()

        local_score += ALLPSQT[from_piece][abs(to_number - offset)] - \
                        ALLPSQT[from_piece][abs(from_number - offset)]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece][abs(to_number - offset)]

            # prioritize captures by piece value
            if sorting:
                local_score += (PIECEPOINTS[to_piece] - PIECEPOINTS[from_piece])

            # 20cp bonus for breaking up the bishop pair
            if to_piece == 'b' and self.board_state.count(self.board_state[to_number]) == 2:
                local_score += PROTECTED_PAWN_VALUE
            elif to_piece == 'p':
                # if we capture a protected pawn, need to credit bonus for protected pawn
                if self.protected_pawn(to_number, -p_offset, to_piece):
                    local_score += PROTECTED_PAWN_VALUE

                # if we capture a stacked pawn, incur the penalty
                if self.count_piece(to_number, to_piece) == 2 or self.count_piece(to_number, p_piece) == 1:
                    local_score -= STACKED_PAWN_VALUE

                if self.count_piece(to_number, p_piece) == 0:
                    local_score += STACKED_PAWN_VALUE

        if from_piece == 'k':
            if abs(from_number - to_number) == 2:
                if uci_coordinate[2] == 'g':
                    local_score += ALLPSQT['r'][abs(to_number - offset) - 1] - \
                                    ALLPSQT['r'][abs(to_number - offset) + 1]
                else:
                    local_score += ALLPSQT['r'][abs(to_number - offset) + 1] - \
                                    ALLPSQT['r'][abs(to_number - offset) - 2]
        # elif from_piece == 'r':
        #     count1 = self.count_piece(from_number, '-')
        #     count2 = self.count_piece(to_number, '-')

        #     #check for open files
        #     # credit if we are moving from a closed file to an open one
        #     if count1 < 7 and count2 == 8:
        #         local_score += PROTECTED_PAWN_VALUE
        #     # in this case, we are moving from an open file to a non-open file
        #     elif count1 == 7 and count2 < 8:
        #         local_score -= PROTECTED_PAWN_VALUE

        elif from_piece == 'p':
            if uci_coordinate[2:4] == self.en_passant:
                # add in an extra pawn for EP capture
                local_score += ALLPSQT[from_piece][abs(to_number - offset)]
            elif len(uci_coordinate) > 4:
                promote = uci_coordinate[4:5]
                # adjust value for promoting from pawn to queen
                local_score += ALLPSQT[promote][abs(to_number - offset)] - \
                                ALLPSQT['p'][abs(to_number - offset)]
            # score for pawn advances only
            if to_piece == '-':
                if self.protected_pawn(to_number, p_offset, p_piece):
                    local_score += PROTECTED_PAWN_VALUE
                if self.protected_pawn(to_number, -p_offset, p_piece):
                    local_score += PROTECTED_PAWN_VALUE
                # leaving protection
                if self.protected_pawn(from_number, p_offset, p_piece):
                    local_score -= PROTECTED_PAWN_VALUE
                # moving the protector
                if self.protected_pawn(from_number, -p_offset, p_piece):
                    local_score -= PROTECTED_PAWN_VALUE
            if (to_piece != '-' and to_piece != 'p') or uci_coordinate[2:4] == self.en_passant:
                if self.protected_pawn(from_number, p_offset, p_piece):
                    local_score -= PROTECTED_PAWN_VALUE
                if self.protected_pawn(to_number, -p_offset, p_piece):
                    local_score += PROTECTED_PAWN_VALUE
                # bonus for unstacking
                if self.count_piece(from_number, p_piece) == 2:
                    local_score += STACKED_PAWN_VALUE
                # only penalize for first stacked pawn
                if self.count_piece(to_number, p_piece) == 1:
                    local_score -= STACKED_PAWN_VALUE

            if not is_endgame:
                # if the pawn is in front of the K, penalize a movement
                if 'k' in self.board_state[(from_number - p_offset - 1):(from_number - p_offset + 1)].lower():
                    local_score -= PROTECTED_PAWN_VALUE

        return local_score

    def protected_pawn(self, board_position, p_offset, p_piece):
        return self.board_state[board_position - p_offset + 1] == p_piece or \
            self.board_state[board_position - p_offset - 1] == p_piece

    def count_piece(self, board_position, p_piece):
        piece_count = 0
        column = board_position % 10
        for row in range(1,9):
            piece_count += self.board_state[(row * 10 + column)] == p_piece

        return piece_count

    def str_board(self):
        return self.board_state + \
          str(self.played_move_count % 2 == 0)

    def generate_valid_captures(self):
        return self.generate_valid_moves(True)

    def generate_valid_moves(self, captures_only=False):
        """Return list of valid (maybe illegal) moves"""
        is_white = self.played_move_count % 2 == 0

        offset = 1
        max_row = 81
        min_row = 31
        valid_pieces = 'prnbqk-'
        if not is_white:
            valid_pieces = 'PRNBQK-'
            max_row = 31
            min_row = 81

        for board_position, piece in enumerate(self.board_state):
            if piece in "-." or (is_white and piece.islower()) or (not is_white and piece.isupper()):
                continue

            start_coordinate = position_to_coordinate(board_position)

            piece_lower = piece.lower()

            if piece == 'p':
                offset = -1

            # castling
            if piece == 'K' and not captures_only:
                if self.white_castling[1] and self.board_state[96:99] == '--R' and \
                    not any(self.attack_position(is_white, coordinate) for coordinate in ['e1', 'f1', 'g1']):
                    yield start_coordinate + 'g1'
                if self.white_castling[0] and self.board_state[91:95] == 'R---' and \
                    not any(self.attack_position(is_white, coordinate) for coordinate in ['e1', 'd1', 'c1']):
                    yield start_coordinate + 'c1'
            elif piece == 'k' and not captures_only:
                if self.black_castling[1] and self.board_state[26:29] == '--r' and \
                    not any(self.attack_position(is_white, coordinate) for coordinate in ['e8', 'f8', 'g8']):
                    yield start_coordinate + 'g8'
                if self.black_castling[0] and self.board_state[21:25] == 'r---' and \
                    not any(self.attack_position(is_white, coordinate) for coordinate in ['e8', 'd8', 'c8']):
                    yield start_coordinate + 'c8'
            elif piece_lower == 'p' and board_position in range(max_row, max_row+8) and self.board_state[board_position + -10*offset] == '-' and \
                self.board_state[board_position + -20*offset] == '-' and not captures_only:
                yield start_coordinate + position_to_coordinate(board_position + -20*offset)

            for piece_move in TO_MOVES[piece_lower]:
                to_position = board_position + piece_move[0] + (piece_move[1] * offset)

                while 20 < to_position < 99:
                    eval_piece = self.board_state[to_position]

                    dest = position_to_coordinate(to_position)

                    if not captures_only or (captures_only and eval_piece not in '-.'):
                        if piece_lower == 'p':
                            if (board_position in range(min_row, min_row+8) and piece_move[0] == 0 and eval_piece == '-') or \
                                (board_position in range(min_row, min_row+8) and piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces):
                                for prom in 'qrbn':
                                    yield start_coordinate + dest + prom
                            else:
                                if (piece_move[0] == 0 and eval_piece == '-') or \
                                    (piece_move[0] != 0 and eval_piece != '-' and eval_piece in valid_pieces) or \
                                    dest == self.en_passant:
                                    yield start_coordinate + dest
                        elif eval_piece in valid_pieces:
                            yield start_coordinate + dest

                    if eval_piece != '-' or piece_lower in 'knp':
                        break

                    to_position = to_position + piece_move[0] + (piece_move[1] * offset)

    def in_check(self, is_white):
        king_position = self.white_king_position if is_white else self.black_king_position

        return self.attack_position(is_white, king_position)

    def attack_position(self, is_white, coordinate):
        offset = 1
        valid_pieces = 'PRNBQK-'
        if not is_white:
            valid_pieces = 'prnbqk-'

        attack_position = coordinate_to_position(coordinate)

        for board_position, piece in enumerate(self.board_state):
            if piece in "-." or (is_white and piece.isupper()) or (not is_white and piece.islower()):
                continue

            start_coordinate = position_to_coordinate(board_position)

            if piece == 'p':
                offset = -1

            piece = piece.lower()

            for piece_move in TO_MOVES[piece]:
                if board_position > attack_position and offset * piece_move[1] > 0 or board_position < attack_position and offset * piece_move[1] < 0:
                    continue

                if piece == 'p' and (not piece_move[0] or abs(board_position - attack_position) > 32):
                    continue

                to_position = board_position + piece_move[0] + offset * piece_move[1]

                while 20 < to_position < 99:
                    eval_piece = self.board_state[to_position]

                    if eval_piece in valid_pieces and to_position == attack_position:
                        return True

                    if eval_piece != '-' or piece in 'knp':
                        break

                    to_position = to_position + piece_move[0] + offset * piece_move[1]

        return False


tt_bucket = {}

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    critical_time = 0

    def reset(self):
        self.v_nodes = 0
        self.v_depth = 0
        self.end_time = 0
        self.critical_time = 0
        tt_bucket.clear()

    # def run_perft(self, local_board, original_depth, v_depth):
    #     if v_depth == 0:
    #         return 1

    #     if v_depth != original_depth:
    #         total = 0
    #         for s_move in local_board.generate_valid_moves():
    #             moved_board = local_board.make_move(s_move)

    #             if moved_board.in_check(local_board.played_move_count % 2 == 0):
    #                 continue

    #             if local_board.piece_count != moved_board.piece_count:
    #                 self.perft_captures += 1

    #             if moved_board.in_check(local_board.played_move_count % 2 != 0):
    #                 self.perft_checks += 1

    #             total += self.run_perft(moved_board, original_depth, v_depth-1)
    #         return total

    #     per_moves = []
    #     for s_move in local_board.generate_valid_moves():
    #         moved_board = local_board.make_move(s_move)

    #         if moved_board.in_check(local_board.played_move_count % 2 == 0):
    #             continue

    #         if local_board.piece_count != moved_board.piece_count:
    #             self.perft_captures += 1

    #         if moved_board.in_check(local_board.played_move_count % 2 != 0):
    #             self.perft_checks += 1

    #         print (f"{s_move}:", end=" ")
    #         x = self.run_perft(moved_board, original_depth, v_depth-1)
    #         print(x)
    #         per_moves.append(x)

    #     print(f"Nodes searched: {sum(per_moves)}")
    #     print(f"Captures: {self.perft_captures} Checks: {self.perft_checks}")

    def iterative_search(self, local_board):
        start_time = t()

        for v_depth in range(1, 100):
            local_score = self.search(local_board, v_depth, -MATE_UPPER, MATE_UPPER)

            if t() < self.critical_time:
                best_move = tt_bucket.get(local_board.board_string)
                if best_move:
                    best_move = best_move['tt_move']
            else:
                break

            elapsed_time = t() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time) if elapsed_time > 0 else 1

            # pv = ''
            # counter = 1
            # pv_board = local_board.make_move(best_move)
            # while counter < v_depth:
            #     counter += 1

            #     pv_entry = tt_bucket.get(pv_board.board_string)

            #     if not pv_entry:
            #         break

            #     pv_board = pv_board.make_move(pv_entry['tt_move'])

            #     pv += ' ' + pv_entry['tt_move']

            # print_stats(str(v_depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move + pv))

            print_stats(str(v_depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time)), str(self.v_nodes), str(v_nps), str(best_move))

            yield v_depth, best_move, local_score

    def search(self, local_board, v_depth, alpha, beta):
        if t() > self.critical_time:
            return local_board.rolling_score

        self.v_nodes += 1

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        is_white = local_board.played_move_count % 2 == 0
        pv_node = (alpha != beta - 1)
        is_in_check = local_board.in_check(is_white)

        v_depth = max(0, v_depth)

        if v_depth == 0 and not is_in_check:
            return self.q_search(local_board, alpha, beta)

        if local_board.repetitions.count(local_board.board_string) >= 2 or local_board.move_counter >= 100:
            return 0

        v_depth += is_in_check

        original_alpha = alpha

        tt_entry = tt_bucket.get((local_board.board_string), {'tt_value': 2*MATE_UPPER, 'tt_flag': UPPER, 'tt_depth': 0, 'tt_move': None})

        if tt_entry['tt_depth'] >= v_depth and not is_in_check:
            if tt_entry['tt_flag'] == EXACT or \
            (tt_entry['tt_flag'] == LOWER and tt_entry['tt_value'] >= beta) or \
            (tt_entry['tt_flag'] == UPPER and tt_entry['tt_value'] <= alpha):
                return tt_entry['tt_value']

        current_eval = tt_entry['tt_value'] if tt_entry['tt_value'] < MATE_UPPER else local_board.rolling_score

        if v_depth <= 7 and not pv_node and not is_in_check and current_eval - (90 * v_depth) >= beta:
            return current_eval

        best_score = -MATE_UPPER - 1
        local_score = -MATE_UPPER

        pieces = 'RNBQ' if is_white else 'rnbq'


        if not pv_node and not is_in_check and current_eval >= beta and \
            v_depth >= 4 and pieces in local_board.board_string and \
            local_board.move_list[0] and \
            tt_entry['tt_flag'] != UPPER and \
            tt_entry['tt_value'] < beta:

            local_score = -self.search(local_board.nullmove(), min(1, v_depth - 4), -beta, -beta+1)

            if local_score >= beta and abs(local_score) < MATE_UPPER:
                return beta

        if not pv_node and not is_in_check and local_board.move_list[0] and tt_entry['tt_move']:
            local_score = -self.search(local_board.make_move(tt_entry['tt_move']), v_depth - 1, -beta, -alpha)

            if local_score >= beta and abs(local_score) < MATE_UPPER:
                return beta

        played_moves = 0

        best_move = None

        for s_move in sorted(local_board.generate_valid_moves(), key=local_board.calculate_score, reverse=True):
            current_move_score = local_board.calculate_score(s_move)

            moved_board = local_board.make_move(s_move)

            # determine legality: if we moved and are in check, it's not legal
            if moved_board.in_check(is_white):
                continue

            played_moves += 1

            if played_moves == 1:
                # full window search for first move
                local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha)
            else:
                reduce_depth = 1

                is_noisy = current_move_score > 800 or local_board.piece_count != moved_board.piece_count

                if v_depth > 2 and not is_noisy:
                    reduce_depth = min(3, v_depth)

                local_score = -self.search(moved_board, v_depth - reduce_depth, -alpha-1, -alpha)
                if reduce_depth > 1 and local_score > alpha:
                    local_score = -self.search(moved_board, v_depth - 1, -alpha-1, -alpha)

                if alpha < local_score < beta:
                    local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha)

            if local_score > best_score:
                best_move = s_move
                best_score = local_score

                alpha = max(alpha, local_score)

                if alpha >= beta:
                    break

        if played_moves == 0:
            return -MATE_UPPER if is_in_check else 0

        #update TT only if we are not in time cut
        if t() < self.critical_time:
            tt_entry['tt_value'] = best_score
            tt_entry['tt_move'] = best_move
            tt_entry['tt_depth'] = v_depth
            if best_score <= original_alpha:
                tt_entry['tt_flag'] = UPPER
            elif best_score >= beta:
                tt_entry['tt_flag'] = LOWER
            else:
                tt_entry['tt_flag'] = EXACT

            tt_bucket[local_board.board_string] = tt_entry

        return best_score

    def q_search(self, local_board, alpha, beta):
        self.v_nodes += 1

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if local_board.repetitions.count(local_board.board_string) >= 2 or local_board.move_counter >= 100:
            return 0

        tt_entry = tt_bucket.get(local_board.board_string)

        if tt_entry:
            if tt_entry['tt_flag'] == EXACT or \
            (tt_entry['tt_flag'] == LOWER and tt_entry['tt_value'] >= beta) or \
            (tt_entry['tt_flag'] == UPPER and tt_entry['tt_value'] <= alpha):
                return tt_entry['tt_value']

        is_white = local_board.played_move_count % 2 == 0
        is_in_check = local_board.in_check(is_white)

        local_score = local_board.rolling_score if not is_in_check else -MATE_UPPER

        if local_score >= beta:
            return beta

        best_score = local_score

        alpha = max(alpha, local_score)

        for s_move in sorted(local_board.generate_valid_captures() if not is_in_check else local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
            moved_board = local_board.make_move(s_move)

            # determine legality: if we moved and are in check, it's not legal
            if moved_board.in_check(is_white):
                continue

            local_score = -self.q_search(moved_board, -beta, -alpha)

            if local_score > best_score:
                best_score = local_score

                if local_score > alpha:
                    alpha = local_score

            if alpha >= beta:
                return best_score

        return best_score

game_board = Board()
searcher = Search()

while 1:
    try:
        line = input()
        if line == "quit":
            sys.exit()
        elif line == "uci":
            print_to_terminal("pygone 1.4\nuciok")
        elif line == "ucinewgame":
            game_board = Board()
            searcher.reset()
        elif line == "isready":
            print_to_terminal("readyok")
        # elif line.startswith("position fen"):
        #     fens = line.split(' ')
        #     position = fens[2].split('/')

        #     position = 21
        #     for piece in fens[2]:
        #         # print(position)
        #         if piece == '/':
        #             position += 2
        #         else:
        #             if piece.isnumeric():
        #                 skip_count = int(piece)
        #                 while skip_count > 0:
        #                     game_board.mutate_board(position, '-')
        #                     position += 1
        #                     skip_count -= 1
        #             else:
        #                 game_board.mutate_board(position, piece)
        #                 if piece.isupper():
        #                     game_board.rolling_score += ALLPSQT[piece.lower()][position]
        #                     if piece == 'K':
        #                         game_board.white_king_position = position_to_coordinate(position)
        #                 else:
        #                     game_board.rolling_score -= ALLPSQT[piece.lower()][abs(position - 119)]
        #                     if piece == 'k':
        #                         game_board.black_king_position = position_to_coordinate(position)
        #                 position += 1

        #     for castling in fens[4]:
        #         if castling == '-':
        #             game_board.white_castling = [False, False]
        #             game_board.black_castling = [False, False]
        #         elif castling == 'K':
        #             game_board.white_castling[1] = True
        #         elif castling == 'Q':
        #             game_board.white_castling[0] = True
        #         elif castling == 'k':
        #             game_board.black_castling[1] = True
        #         elif castling == 'q':
        #             game_board.black_castling[0] = True

        #     game_board.en_passant = fens[5]

        #     game_board.board_string = game_board.str_board()
        #     game_board.piece_count = game_board.get_piece_count()

        #     if len(fens) > 6:
        #         game_board.move_counter = int(fens[6])
        #         game_board.played_move_count = int(fens[7]) * 2
        #     if fens[3] == 'b':
        #         game_board.played_move_count += 1
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

            searcher.critical_time = t() + (move_time) - 0.2
            move_time = max(3, move_time / div_time)

            searcher.end_time = t() + move_time

            searcher.v_nodes = 0

            s_move = None

            start = t()
            for v_depth, s_move, best_score in searcher.iterative_search(game_board):
                if (searcher.end_time - t()) < 1:
                    searcher.v_depth = 3

                if v_depth >= searcher.v_depth or t() > searcher.end_time or abs(best_score) >= MATE_UPPER:
                    break

            # ponder_board = game_board.make_move(s_move)
            # ponder_bucket = searcher.tt_bucket.get(ponder_board.board_string)
            # ponder = ""
            # if ponder_bucket:
            #     ponder = f" ponder {ponder_bucket['tt_move']}"

            # print_to_terminal(f"bestmove {str(s_move)}{ponder}")

            print_to_terminal(f"bestmove {str(s_move)}")

    except (KeyboardInterrupt, SystemExit):
        sys.exit()
    except Exception as exc:
        print_to_terminal(exc)
        raise