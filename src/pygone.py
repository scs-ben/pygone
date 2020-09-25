#!/usr/bin/env pypy3
import math, sys, time
from itertools import chain

PIECEPOINTS = {'p': 100, 'r': 480, 'n': 280, 'b': 320, 'q': 960, 'k': 6e4}

ALLPSQT = {
    'p': [[0]*8,
          [78, 83, 86, 73, 102, 82, 85, 90],
          [7, 29, 21, 44, 40, 31, 44, 7],
          [-17, 16, -2, 15, 14, 0, 15, -13],
          [-26, 3, 10, 9, 6, 1, 0, -23],
          [-22, 9, 5, -11, -10, -2, 3, -19],
          [-31, 8, -7, -37, -36, -14, 3, -31],
          [0]*8],
    'n': [[-66, -53, -75, -75, -10, -55, -58, -70],
          [-3, -6, 100, -36, 4, 62, -4, -14],
          [10, 67, 1, 74, 73, 27, 62, -2],
          [24, 24, 45, 37, 33, 41, 25, 17],
          [-1, 5, 31, 21, 22, 35, 2, 0],
          [-18, 10, 13, 22, 18, 15, 11, -14],
          [-23, -15, 2, 0, 2, 0, -23, -20],
          [-74, -23, -26, -24, -19, -35, -22, -69]],
    'b': [[-59, -78, -82, -76, -23, -107, -37, -50],
          [-11, 20, 35, -42, -39, 31, 2, -22],
          [-9, 39, -32, 41, 52, -10, 28, -14],
          [25, 17, 20, 34, 26, 25, 15, 10],
          [13, 10, 17, 23, 17, 16, 0, 7],
          [14, 25, 24, 15, 8, 25, 20, 15],
          [19, 20, 11, 6, 7, 6, 20, 16],
          [-7, 2, -15, -12, -14, -15, -10, -10]],
    'r': [[35, 29, 33, 4, 37, 33, 56, 50],
          [55, 29, 56, 67, 55, 62, 34, 60],
          [19, 35, 28, 33, 45, 27, 25, 15],
          [0, 5, 16, 13, 18, -4, -9, -6],
          [-28, -35, -16, -21, -13, -29, -46, -30],
          [-42, -28, -42, -25, -25, -35, -26, -46],
          [-53, -38, -31, -26, -29, -43, -44, -53],
          [-30, -24, -18, 5, -2, -18, -31, -32]],
    'q': [[6, 1, -8, -104, 69, 24, 88, 26],
          [14, 32, 60, -10, 20, 76, 57, 24],
          [-2, 43, 32, 60, 72, 63, 43, 2],
          [1, -16, 22, 17, 25, 20, -13, -6],
          [-14, -15, -2, -5, -1, -10, -20, -22],
          [-30, -6, -13, -11, -16, -11, -16, -27],
          [-36, -18, 0, -19, -15, -15, -21, -38],
          [-39, -30, -31, -13, -31, -36, -34, -42]],
    'k': [[4, 54, 47, -99, -99, 60, 83, -62],
          [-32, 10, 45, 56, 56, 55, 10, 3],
          [-62, 12, -57, 44, -67, 28, 37, -31],
          [-55, 50, 11, -4, -19, 13, 0, -49],
          [-55, -43, -52, -28, -51, -47, -8, -50],
          [-47, -42, -43, -79, -64, -32, -29, -32],
          [-4, 3, -14, -50, -57, -18, 13, 4],
          [22, 30, -3, -14, 6, -1, 40, 26]]
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

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)

def number_to_letter(number):
    return chr(number + 96)

def print_to_terminal(letter):
    print(letter, flush=True)

def get_perf_counter():
    return time.perf_counter()

def print_stats(v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
    print_to_terminal("info depth " + v_depth + " score cp " + v_score + " time " + v_time + " nodes " + v_nodes + " nps " + v_nps + " pv " + v_pv)

class Board:
    # represent the board state as it is
    board_state = []
    played_move_count = 0
    move_list = []
    valid_moves = [[],[]]
    capture_moves = []
    attack_squares = [[],[]]
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
        from_letter_number = letter_to_number(uci_coordinate[0:1])
        from_number = abs(int(uci_coordinate[1:2]) - 8)
        to_letter_number = letter_to_number(uci_coordinate[2:3])
        to_number = abs(int(uci_coordinate[3:4]) - 8)

        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]

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

    def make_move(self, uci_coordinate, calculate_next=False):
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = Board()
        board.played_move_count = self.played_move_count
        board.board_state = [x[:] for x in self.board_state]
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
        if calculate_next:
            board.get_valid_moves()

        board.rolling_score = -board.rolling_score

        return board

    def calculate_score(self, uci_coordinate):
        offset = 0 if self.played_move_count % 2 == 0 else 7

        from_letter_number = letter_to_number(uci_coordinate[0:1])
        from_number = abs(int(uci_coordinate[1:2]) - 8)
        to_letter_number = letter_to_number(uci_coordinate[2:3])
        to_number = abs(int(uci_coordinate[3:4]) - 8)
        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]

        local_score = ALLPSQT[from_piece.lower()][abs(to_number - offset)][abs(to_letter_number - offset)] - ALLPSQT[from_piece.lower()][abs(from_number - offset)][abs(from_letter_number - offset)]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece.lower()][abs(to_number - offset)][abs(to_letter_number - offset)]

        if (from_piece in ('K', 'k') and uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8')):
            if uci_coordinate[2] == 'g':
                local_score += ALLPSQT['r'][abs(to_number - offset)][abs(to_letter_number - 1 - offset)] - ALLPSQT['r'][abs(to_number - offset)][abs(to_letter_number + 1 - offset)]
            else:
                local_score += ALLPSQT['r'][abs(to_number - offset)][abs(to_letter_number + 1 - offset)] - ALLPSQT['r'][abs(to_number - offset)][abs(to_letter_number - 2 - offset)]
        elif from_piece in ('P', 'p') and uci_coordinate[2:4] == self.en_passant:
            # add in an extra pawn for EP capture
            local_score += ALLPSQT[from_piece.lower()][abs(to_number - offset)][abs(to_letter_number - offset)]

        if len(uci_coordinate) > 4:
            local_score += ALLPSQT['q'][abs(to_number - offset)][abs(to_letter_number - offset)] - ALLPSQT['p'][abs(to_number - offset)][abs(to_letter_number - offset)]

        return local_score

    # def show_board(self):
    #     for i in range(8):
    #         for j in range(8):
    #             print(self.board_state[i][j], end=" ")
    #         print()
    #     print("a b c d e f g h")

    def str_board(self):
        return hash(''.join(list(chain.from_iterable(self.board_state))) + str(self.played_move_count % 2 == 0))

    def get_valid_moves(self, previous_turn=False):
        is_white = self.played_move_count % 2 == 0

        if previous_turn:
            is_white = not is_white

        valid_moves = []
        capture_moves = []

        attack_squares = []

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
                    for _, k_move in king_moves.items():
                        if k_move['column'] in range(8) and k_move['row'] in range(8):
                            eval_piece = eval_state[k_move['row']][k_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())

                            dest = number_to_letter(k_move['column'] + 1) + str(abs(k_move['row'] - 8))

                            if eval_piece == '-' or can_capture:
                                valid_moves.append(start_coordinate + dest)
                            if can_capture:
                                capture_moves.append(start_coordinate + dest)
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

                            can_capture = (is_white and eval_piece in BLACK_PIECES) or (not is_white and eval_piece in WHITE_PIECES)

                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                valid_moves.append(start_coordinate + dest)
                                attack_squares.append(dest)
                                if can_capture:
                                    capture_moves.append(start_coordinate + dest)
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
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())
                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
                                valid_moves.append(start_coordinate + dest)
                                if can_capture:
                                    capture_moves.append(start_coordinate + dest)

                                attack_squares.append(dest)
                if piece.lower() == 'p':
                    if is_white:
                        min_row = 1
                        max_row = 6
                        offset = -1
                        piece_set = BLACK_PIECES
                    else:
                        min_row = 6
                        max_row = 1
                        offset = 1
                        piece_set = WHITE_PIECES

                    if row in range(1, 7) and eval_state[row + offset ][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)))
                    if row == max_row and eval_state[row + offset ][column] == '-' and eval_state[row + 2*offset][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + 2*offset)))
                    if row == min_row and eval_state[row + offset ][column] == '-':
                        valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 8 + offset)) + 'q')
                    if ((column - 1) >= 0 and (row + offset) in range(8)) or ((column + 1) < 8 and (row + offset) in range(8)):
                        prom = ''
                        if row == min_row:
                            prom = 'q'
                        if (column - 1) >= 0:
                            dest = number_to_letter(column) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column - 1]
                            if dest_piece == '-' or dest_piece in piece_set or dest == self.en_passant:
                                if dest_piece != '-':
                                    valid_moves.append(start_coordinate + dest + prom)
                                    capture_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)
                        if (column + 1) < 8:
                            dest = number_to_letter(column + 2) + str(abs(row - 8 + offset))
                            dest_piece = eval_state[row + offset][column + 1]
                            if dest_piece == '-' or dest_piece in piece_set or dest == self.en_passant:
                                if dest_piece != '-':
                                    valid_moves.append(start_coordinate + dest + prom)
                                    capture_moves.append(start_coordinate + dest + prom)
                                attack_squares.append(dest)

        self.capture_moves.append(capture_moves)

        self.valid_moves[0 if is_white else 1] = valid_moves
        self.attack_squares[0 if is_white else 1] = attack_squares

        return valid_moves

    def in_check(self, is_white):
        if is_white:
            return self.white_king_position in self.attack_squares[1]

        return self.black_king_position in self.attack_squares[0]

class Search:
    v_nodes = 0
    v_tthits = 0
    v_depth = 0
    end_time = 0
    tt_bucket = {}

    def reset(self):
        # reset to base state
        self.v_nodes = 0
        self.v_tthits = 0
        self.tt_bucket = {}

    def iterative_search(self, local_board, v_depth):
        start_time = get_perf_counter()

        alpha = -1e8
        beta = 1e8

        iterative_score = -1e8
        iterative_move = None

        self.v_depth = 0
        while v_depth > 0:
            self.v_depth += 1
            v_depth -= 1

            (iterative_score, iterative_move) = self.search(local_board, self.v_depth, alpha, beta)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            v_nps = math.ceil(self.v_nodes / elapsed_time)

            print_stats(str(self.v_depth), str(math.ceil(iterative_score)), str(elapsed_time), str(self.v_nodes), str(v_nps), iterative_move)

        return [iterative_score, iterative_move]

    def search(self, local_board, v_depth, alpha, beta):
        global_score = -1e8
        chosen_move = None

        local_score = -1e8

        v_depth = max(v_depth, 1)

        print_time = get_perf_counter() + 5

        for s_move in sorted(local_board.get_valid_moves(), key=local_board.calculate_score, reverse=True):
            self.v_nodes += 1

            temp_board = local_board.make_move(s_move, True)

            if temp_board.in_check(local_board.played_move_count % 2 == 0):
                continue

            local_score = -self.pvs(temp_board, -beta, -alpha, v_depth - 1)

            if local_score >= global_score:
                global_score = local_score
                chosen_move = s_move

            if get_perf_counter() > print_time:
                print_to_terminal("info nodes " + str(self.v_nodes))
                print_time = get_perf_counter() + 5

        return [global_score, chosen_move]

    def pvs(self, local_board, alpha, beta, v_depth):
        if v_depth < 1:
            # check to see if last move was in previous list of captures
            if local_board.move_list[-1] in local_board.capture_moves[-1] + local_board.capture_moves[-2]:
                return self.q_search(local_board, alpha, beta, 8)
            else:
                return local_board.rolling_score

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        original_alpha = alpha

        tt_entry = self.tt_lookup(local_board)
        if tt_entry['tt_depth'] >= v_depth:
            if tt_entry['tt_flag'] == EXACT:
                self.v_nodes += 1
                return tt_entry['tt_value']
            if tt_entry['tt_flag'] == LOWER:
                alpha = max(alpha, tt_entry['tt_value'])
            elif tt_entry['tt_flag'] == UPPER:
                beta = min(beta, tt_entry['tt_value'])

            if alpha >= beta:
                self.v_nodes += 1
                return tt_entry['tt_value']

        local_score = -1e8

        for s_move in sorted(local_board.get_valid_moves(), key=local_board.calculate_score, reverse=True):
            self.v_nodes += 1

            temp_board = local_board.make_move(s_move)

            local_score = -self.pvs(temp_board, -alpha - 1, -alpha, v_depth - 1)
            if alpha < local_score < beta:
                local_score = -self.pvs(temp_board, -beta, -local_score, v_depth - 1)

            alpha = max(alpha, local_score)

            if alpha >= beta:
                break

        tt_entry['tt_value'] = alpha
        if alpha <= original_alpha:
            tt_entry['tt_flag'] = UPPER
        elif alpha >= beta:
            tt_entry['tt_flag'] = LOWER
        else:
            tt_entry['tt_flag'] = EXACT
        tt_entry['tt_depth'] = v_depth
        self.store_tt(local_board, tt_entry)

        return alpha

    def q_search(self, local_board, alpha, beta, v_depth):
        if v_depth <= 0 or len(local_board.capture_moves[-1]) == 0:
            return local_board.rolling_score

        if local_board.rolling_score <= -MATE_LOWER:
            return -MATE_UPPER

        if local_board.rolling_score >= beta:
            return beta

        alpha = max(local_board.rolling_score, alpha)

        local_board.get_valid_moves()

        local_score = -1e8

        # loop through current list of captures
        for s_move in local_board.capture_moves[-1]:
            self.v_nodes += 1

            local_score = -self.q_search(local_board.make_move(s_move), -beta, -alpha, v_depth - 1)

            if local_score >= beta:
                return beta

            alpha = max(local_score, alpha)

        return alpha

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

def main():
    searcher = Search()

    game_board = Board()

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            # elif line == "print":
            #     game_board.show_board()
            elif line == "uci":
                print_to_terminal("pygone 1.1\nuciok")
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
                game_board.get_valid_moves(True)
                # game_board.show_board()
            elif line.startswith("go"):
                white_time = 1e8
                black_time = 1e8
                go_depth = 7
                input_depth = 0

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    elif arg == 'btime':
                        black_time = int(args[key + 1])
                    # these are commented out to save space since engine will be run on time
                    # elif arg == 'depth':
                    #     go_depth = int(args[key + 1])
                    # elif arg == 'infinite':
                    #     input_depth = 30

                time_move_calc = max(25 - game_board.played_move_count, 2)

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0

                if is_white:
                    move_time = (white_time / (time_move_calc * 1e3))
                else:
                    move_time = (black_time / (time_move_calc * 1e3))

                searcher.end_time = get_perf_counter() + move_time

                # go_depth = max(input_depth, go_depth)

                if move_time < 40:
                    go_depth = 6
                if move_time < 20:
                    go_depth = 5
                if move_time < 15:
                    go_depth = 4
                if move_time < 4:
                    go_depth = 2

                searcher.v_nodes = 0
                searcher.v_tthits = 0

                (_, s_move) = searcher.iterative_search(game_board, go_depth)

                print_to_terminal("bestmove " + s_move)
        except (KeyboardInterrupt, SystemExit):
            print_to_terminal('quit')
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
