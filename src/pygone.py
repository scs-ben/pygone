#!/usr/bin/env python3
import math
import sys
import time

PIECEPOINTS = {'p': 100.0, 'r': 479.0, 'n': 280.0, 'b': 320.0, 'q': 929.0, 'k': 60000.0}
ATTACKPOINTS = {'p': 5.0, 'r': 18.0, 'n': 10.0, 'b': 10.0, 'q': 20.0, 'k': 30.0}

PPSQT = [[0, 0, 0, 0, 0, 0, 0, 0],
         [78, 83, 86, 73, 102, 82, 85, 90],
         [7, 29, 21, 44, 40, 31, 44, 7],
         [-17, 16, -2, 15, 14, 0, 15, -13],
         [-26, 3, 10, 9, 6, 1, 0, -23],
         [-22, 9, 5, -11, -10, -2, 3, -19],
         [-31, 8, -7, -37, -36, -14, 3, -31],
         [0, 0, 0, 0, 0, 0, 0, 0]]
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
         [-32, 10, 55, 56, 56, 55, 10, 3],
         [-62, 12, -57, 44, -67, 28, 37, -31],
         [-55, 50, 11, -4, -19, 13, 0, -49],
         [-55, -43, -52, -28, -51, -47, -8, -50],
         [-47, -42, -43, -79, -64, -32, -29, -32],
         [-4, 3, -14, -50, -57, -18, 13, 4],
         [22, 30, -3, -14, 6, -1, 40, 26]]

ALLPSGT = {'p': PPSQT, 'n': NPSQT, 'b':BPSQT, 'r':RPSQT, 'q':QPSQT, 'k':KPSQT}

isupper = lambda c: 'A' <= c <= 'Z'
islower = lambda c: 'a' <= c <= 'z'

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)

def number_to_letter(number):
    return chr(number + 96)

class Board:

    board_state = []
    played_move_count = 0
    white_valid_moves = []
    black_valid_moves = []
    white_attack_locations = ''
    black_attack_locations = ''
    white_king_location = 'e1'
    black_king_location = 'e8'
    moveList = []
    last_move = ''
    nodes = 0
    depth = 0

    def __init__(self):
        self.set_default_board_state()
        self.played_move_count = 0
        self.white_valid_moves = []
        self.black_valid_moves = []
        self.white_attack_pieces = []
        self.black_attack_pieces = []
        self.white_attack_locations = ''
        self.black_attack_locations = ''

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

    def make_move(self, uci_coordinate):
        from_letter_number = letter_to_number(uci_coordinate[0:1])
        from_number = abs(int(uci_coordinate[1:2]) - 8)
        to_letter_number = letter_to_number(uci_coordinate[2:3])
        to_number = abs(int(uci_coordinate[3:4]) - 8)
        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]
        promote = ""
        if len(uci_coordinate) > 4:
            promote = uci_coordinate[4:5]
        if (from_piece in ('P', 'p') and to_piece == '-' and \
            uci_coordinate[0:1] != uci_coordinate[2:3]):
            self.board_state[from_number][from_letter_number] = '-'
            self.board_state[to_number][to_letter_number] = from_piece
            self.board_state[from_number][to_letter_number] = '-'
        elif (from_piece in ('K', 'k') and uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8')):
            self.board_state[from_number][from_letter_number] = '-'
            if uci_coordinate[2] == 'g':
                self.board_state[to_number][to_letter_number + 1] = '-'

                if self.played_move_count % 2 == 0:
                    self.board_state[from_number][from_letter_number + 1] = 'R'
                else:
                    self.board_state[from_number][from_letter_number + 1] = 'r'
            else:
                self.board_state[from_number][to_letter_number - 2] = '-'
                if self.played_move_count % 2 == 0:
                    self.board_state[from_number][from_letter_number - 1] = 'R'
                else:
                    self.board_state[from_number][from_letter_number - 1] = 'r'

            if self.played_move_count % 2 == 0:
                self.board_state[from_number][to_letter_number] = 'K'
            else:
                self.board_state[from_number][to_letter_number] = 'k'
        else:
            self.board_state[from_number][from_letter_number] = '-'
            if promote != "":
                if self.played_move_count % 2 == 0:
                    self.board_state[to_number][to_letter_number] = promote.upper()
                else:
                    self.board_state[to_number][to_letter_number] = promote
            else:
                self.board_state[to_number][to_letter_number] = from_piece

        self.moveList.append(uci_coordinate)
        self.played_move_count += 1

    def show_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board_state[i][j], end=" ")
            print()

    def get_valid_moves(self):
        white_valid_moves = []
        black_valid_moves = []
        white_attack_pieces = []
        black_attack_pieces = []
        self.white_attack_locations = ''
        self.black_attack_locations = ''
        eval_state = self.board_state.copy()
        for row in range(8):
            for column in range(8):
                piece = eval_state[row][column]
                if piece == "-":
                    continue
                white_start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))
                black_start_coordinate = number_to_letter(column + 1) + str(abs(row - 8))
                if piece in ('k', 'K'):
                    if piece == 'K':
                        is_white = True
                        self.white_king_location = white_start_coordinate
                    else:
                        is_white = False
                        self.black_king_location = black_start_coordinate
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
                        if white_start_coordinate == 'e1' and eval_state[7][5] == '-' and \
                        eval_state[7][6] == '-' and eval_state[7][7] == 'R':
                            white_valid_moves.append(white_start_coordinate + 'g1')
                        if white_start_coordinate == 'e1' and eval_state[7][1] == '-' and \
                        eval_state[7][2] == '-' and eval_state[7][3] == '-' and \
                        eval_state[7][0] == 'R':
                            white_valid_moves.append(white_start_coordinate + 'c1')
                    else:
                        if black_valid_moves == 'e8' and eval_state[0][1] == '-' and \
                        eval_state[0][1] == '-' and eval_state[0][2] == '-' and \
                        eval_state[0][0] == 'r':
                            black_valid_moves.append(black_start_coordinate + 'c8')
                        if black_valid_moves == 'e8' and eval_state[0][5] == '-' and \
                        eval_state[0][6] == '-' and eval_state[0][7] == 'r':
                            black_valid_moves.append(black_start_coordinate + 'g8')
                    for n_move in king_moves.items():
                        if (n_move['column'] >= 0 and n_move['column'] <= 7 and \
                            n_move['row'] >= 0 and n_move['row'] <= 7):
                            eval_piece = eval_state[n_move['row']][n_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())

                            dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))

                            if eval_piece == '-' or can_capture:
                                if is_white:
                                    white_valid_moves.append(white_start_coordinate + dest)
                                else:
                                    black_valid_moves.append(black_start_coordinate + dest)
                            if can_capture:
                                if is_white:
                                    white_attack_pieces.append([eval_piece, piece])
                                    self.white_attack_locations += dest
                                else:
                                    black_attack_pieces.append([eval_piece, piece])
                                    self.black_attack_locations += dest
                if piece in ('p', 'P'):
                    if piece == 'P':
                        if row > 1 and eval_state[row - 1][column] == '-':
                            white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)))
                        if row == 6 and eval_state[row - 1][column] == '-' and eval_state[row - 2][column] == '-':
                            white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 10)))
                        if row == 1 and eval_state[row - 1][column] == '-':
                            white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)) + 'q')
                        if ((column - 1) >= 0 and (row - 1) >= 0) or ((column + 1) < 8 and (row - 1) >= 0):
                            prom = ''
                            if row == 1:
                                prom = 'q'
                            if (column - 1) >= 0 and eval_state[row - 1][column - 1] != '-' and eval_state[row - 1][column - 1].islower():
                                white_valid_moves.append(white_start_coordinate + number_to_letter(column) + str(abs(row - 9)) + prom)
                                self.white_attack_locations += number_to_letter(column) + str(abs(row - 9))
                                white_attack_pieces.append([eval_state[row - 1][column - 1], piece])
                            if (column + 1) < 8 and eval_state[row - 1][column + 1] != '-' and eval_state[row - 1][column + 1].islower():
                                white_valid_moves.append(white_start_coordinate + number_to_letter(column + 2) + str(abs(row - 9)) + prom)
                                self.white_attack_locations += number_to_letter(column + 2) + str(abs(row - 9))
                                white_attack_pieces.append([eval_state[row - 1][column + 1], piece])
                    else:
                        if row < 6 and eval_state[row + 1][column] == '-':
                            black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)))
                        if row == 1 and eval_state[row + 1][column] == '-' and eval_state[row + 2][column] == '-':
                            black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 6)))
                        if row == 6 and eval_state[row + 1][column] == '-':
                            black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)) + 'q')
                        if ((column - 1) >= 0 and (row + 1) < 8) or ((column + 1) < 8 and (row + 1) < 8):
                            prom = ''
                            if row == 6:
                                prom = 'q'

                            if (column + 1) < 8 and eval_state[row + 1][column + 1] != '-' and eval_state[row + 1][column + 1].isupper():
                                black_valid_moves.append(black_start_coordinate + number_to_letter(column + 2) + str(abs(row - 7)) + prom)
                                self.black_attack_locations += number_to_letter(column + 2) + str(abs(row - 7))
                                black_attack_pieces.append([eval_state[row + 1][column + 1], piece])
                            if (column - 1) >= 0 and eval_state[row + 1][column - 1] != '-' and eval_state[row + 1][column - 1].isupper():
                                black_valid_moves.append(black_start_coordinate + number_to_letter(column) + str(abs(row - 7)) + prom)
                                self.black_attack_locations += number_to_letter(column) + str(abs(row - 7))
                                black_attack_pieces.append([eval_state[row + 1][column - 1], piece])
                if piece in ('n', 'N'):
                    is_white = (piece == 'N')
                    night_moves = {
                        1: {'column': (column + 1), 'row': (row - 2)},
                        2: {'column': (column - 1), 'row': (row - 2)},
                        3: {'column': (column + 2), 'row': (row - 1)},
                        4: {'column': (column - 2), 'row': (row - 1)},
                        5: {'column': (column + 1), 'row': (row + 2)},
                        6: {'column': (column - 1), 'row': (row + 2)},
                        7: {'column': (column + 2), 'row': (row + 1)},
                        8: {'column': (column - 2), 'row': (row + 1)},
                    }
                    for n_move in night_moves.items():
                        if n_move['column'] >= 0 and n_move['column'] <= 7 and n_move['row'] >= 0 and n_move['row'] <= 7:
                            eval_piece = eval_state[n_move['row']][n_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())
                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
                                if is_white:
                                    white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        white_attack_pieces.append([eval_piece, piece])
                                else:
                                    black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        black_attack_pieces.append([eval_piece, piece])
                if piece in ('r', 'R') or piece in ('q', 'Q'):
                    is_white = piece in ('R', 'Q')

                    horizontal_moves = {
                        1: {'column': column, 'row': (row - 1), 'colIncrement': 0, 'rowIncrement': -1},
                        2: {'column': column, 'row': (row + 1), 'colIncrement': 0, 'rowIncrement': 1},
                        3: {'column': (column - 1), 'row': row, 'colIncrement': -1, 'rowIncrement': 0},
                        4: {'column': (column + 1), 'row': row, 'colIncrement': 1, 'rowIncrement': 0}
                    }

                    for _, h_move in horizontal_moves.items():
                        temp_row = h_move['row']
                        temp_col = h_move['column']
                        while temp_row in range(8) and temp_col in range(8):
                            eval_piece = eval_state[temp_row][temp_col]
                            can_capture = (is_white and eval_piece != '-' and eval_piece.islower()) or (not is_white and eval_piece != '-' and eval_piece.isupper())

                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                if is_white:
                                    white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        white_attack_pieces.append([eval_piece, piece])
                                else:
                                    black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        black_attack_pieces.append([eval_piece, piece])
                                if can_capture:
                                    break
                            else:
                                break
                            temp_row += h_move['rowIncrement']
                            temp_col += h_move['colIncrement']

                if piece in ('b', 'B') or piece in ('q', 'Q'):
                    is_white = piece in ('B', 'Q')

                    diag_moves = {
                        1: {'column': (column - 1), 'row': (row - 1), 'colIncrement': -1, 'rowIncrement': -1},
                        2: {'column': (column + 1), 'row': (row + 1), 'colIncrement': 1, 'rowIncrement': 1},
                        3: {'column': (column - 1), 'row': (row + 1), 'colIncrement': -1, 'rowIncrement': 1},
                        4: {'column': (column + 1), 'row': (row - 1), 'colIncrement': 1, 'rowIncrement': -1}
                    }

                    for _, d_move in diag_moves.items():
                        temp_row = d_move['row']
                        temp_col = d_move['column']
                        while temp_row in range(8) and temp_col in range(8):
                            eval_piece = eval_state[temp_row][temp_col]
                            can_capture = (is_white and eval_piece != '-' and eval_piece.islower()) or (not is_white and eval_piece != '-' and eval_piece.isupper())

                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                if is_white:
                                    white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        white_attack_pieces.append([eval_piece, piece])
                                else:
                                    black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        black_attack_pieces.append([eval_piece, piece])
                                if can_capture:
                                    break
                            else:
                                break
                            temp_row += d_move['rowIncrement']
                            temp_col += d_move['colIncrement']

        sep = ''
        if self.played_move_count % 2 == 0:
            move_copy = white_valid_moves.copy()

            move_string = sep.join(black_valid_moves)

            for move in move_copy:
                override_remove = ((move == 'e1g1' and ('e1' in move_string or 'f1' in move_string or 'g1' in move_string)) or (move == 'e1c1' and ('e1' in move_string or 'd1' in move_string or 'c1' in move_string)))

                if override_remove:
                    try:
                        white_valid_moves.remove(move)
                    except Exception:
                        continue
        else:
            move_copy = black_valid_moves.copy()

            move_string = sep.join(white_valid_moves)

            for move in move_copy:
                override_remove = ((move == 'e8g8' and ('e8' in move_string or 'f8' in move_string or 'g8' in move_string)) or (move == 'e8c8' and ('e8' in move_string or 'd8' in move_string or 'c8' in move_string)))

                if override_remove:
                    try:
                        black_valid_moves.remove(move)
                    except Exception:
                        continue

        self.white_valid_moves = white_valid_moves
        self.black_valid_moves = black_valid_moves
        self.white_attack_pieces = white_attack_pieces
        self.black_attack_pieces = black_attack_pieces
        return {'white_valid_moves': white_valid_moves, 'black_valid_moves': black_valid_moves}

    def get_side_moves(self, is_white):
        if is_white:
            return self.white_valid_moves.copy()

        return self.black_valid_moves.copy()

    def board_evaluation(self):
        b_eval = 0
        for row in range(8):
            for column in range(8):
                piece = self.board_state[row][column]
                is_white = piece.isupper()
                if piece != '-':
                    if is_white:
                        b_eval += PIECEPOINTS[piece.lower()]
                        b_eval += (ALLPSGT[piece.lower()][row][column] / 10)
                    else:
                        b_eval -= PIECEPOINTS[piece]
                        b_eval -= (ALLPSGT[piece][abs(row-7)][abs(column-7)] / 10)

        # for (attacked, attacker) in self.white_attack_pieces:
        #   b_eval += ATTACKPOINTS[attacked.lower()] / 10
        # for (attacked, attacker) in self.black_attack_pieces:
        #   b_eval -= ATTACKPOINTS[attacked.lower()] / 10


        return b_eval

    def minimax_root(self, depth, local_board, max_time):
        lgl_mvs = local_board.get_side_moves(local_board.played_move_count % 2 == 0)
        poss_mvs = lgl_mvs
        if len(poss_mvs) == 1:
            local_board.depth = 1
            return [local_board.board_evaluation(), poss_mvs[0]]

        is_maxing_white = (local_board.played_move_count % 2 == 0)
        global_score = -50000 if is_maxing_white else 50000
        chosen_move = None

        original_state = [x[:] for x in local_board.board_state]

        local_board.depth = depth

        max_time = max_time / len(poss_mvs)
        # if max_time < 2:
        #   max_time = 20

        for move in poss_mvs:
            local_board.nodes += 1
            local_board.make_move(move)

            local_start_time = time.perf_counter() + max_time

            local_score = self.minimax(depth - 1, -50000, 50000, local_board, local_start_time, move)

            if is_maxing_white and local_score > global_score:
                global_score = local_score
                chosen_move = move
            elif not is_maxing_white and local_score < global_score:
                global_score = local_score
                chosen_move = move

            local_board.set_board_state([x[:] for x in original_state])
            local_board.played_move_count -= 1

        GAMEBOARD.last_move = chosen_move
        return [global_score, chosen_move]

    def minimax(self, depth, alpha, beta, local_board, end_time, last_move):
        is_maxing_white = (local_board.played_move_count % 2 == 0)
        local_board.get_valid_moves()
        poss_mvs = local_board.get_side_moves(is_maxing_white)
        local_start_time = time.perf_counter()

        if depth == 0 or local_start_time >= end_time or len(poss_mvs) == 0:
            offset = 0
            if last_move == GAMEBOARD.last_move:
                if is_maxing_white:
                    offset = -30.0
                else:
                    offset = 30.0
            return local_board.board_evaluation() + offset

        initial_score = local_board.board_evaluation()

        if (is_maxing_white and initial_score < -50000) or (not is_maxing_white and initial_score > 50000):
            return local_board.board_evaluation()

        original_state = [x[:] for x in local_board.board_state]
        best_score = -50000 if is_maxing_white else 50000
        for move in poss_mvs:
            local_board.nodes += 1
            local_board.make_move(move)

            local_score = self.minimax(depth - 1, alpha, beta, local_board, end_time, move)

            if is_maxing_white:
                best_score = max(best_score, local_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, local_score)
                beta = min(beta, best_score)

            local_board.set_board_state([x[:] for x in original_state])
            local_board.played_move_count -= 1

            if beta <= alpha:
                break

        return best_score

GAMEBOARD = Board()

while True:
    try:
        LINE = input()
        if LINE == "quit":
            sys.exit()
        elif LINE == "uci":
            print("pygone 1.0 by rcostheta")
            print("uciok")
        elif LINE == "ucinewgame":
            GAMEBOARD = Board()
            GAMEBOARD.played_move_count = 0
        elif LINE == "eval":
            GAMEBOARD.get_valid_moves()
            GAMEBOARD.get_side_moves(1)
            # GAMEBOARD.get_side_moves(0)
            print(GAMEBOARD.board_evaluation())
            GAMEBOARD.show_board()
        elif LINE == "isready":
            print("readyok")
        elif LINE.startswith("position"):
            MOVES = LINE.split()
            OFFSETMOVES = GAMEBOARD.played_move_count + 3
            for position_move in MOVES[OFFSETMOVES:]:
                GAMEBOARD.make_move(position_move)
                OFFSETMOVES += 1
            GAMEBOARD.played_move_count = (OFFSETMOVES - 3)
        elif LINE.startswith("go"):
            GOBOARD = Board()
            GOBOARD.set_board_state([x[:] for x in GAMEBOARD.board_state.copy()])
            GOBOARD.played_move_count = GAMEBOARD.played_move_count
            GOBOARD.get_valid_moves()

            WHITETIME = 300
            BLACKTIME = 300
            GODEPTH = 3

            ARGS = LINE.split()
            for key, arg in enumerate(ARGS):
                if arg == 'wtime':
                    WHITETIME = int(ARGS[key + 1])
                if arg == 'btime':
                    BLACKTIME = int(ARGS[key + 1])
                # if arg == 'depth':
                #   depth = int(ARGS[key + 1])

            TIMEMOVECALC = 40
            if GAMEBOARD.played_move_count > 38:
                TIMEMOVECALC = 2
            else:
                TIMEMOVECALC = 40 - GAMEBOARD.played_move_count

            if GAMEBOARD.played_move_count % 2 == 0:
                MOVETIME = WHITETIME / (TIMEMOVECALC * 1000)
            else:
                MOVETIME = BLACKTIME / (TIMEMOVECALC * 1000)

            MOVETIME -= 3

            if MOVETIME < 5:
                MOVETIME = 5

            STARTTIME = time.perf_counter()
            (SCORE, MOVE) = GOBOARD.minimax_root(GODEPTH, GOBOARD, MOVETIME)
            ELAPSEDTIME = math.ceil(time.perf_counter() - STARTTIME)
            NPS = math.ceil(GOBOARD.nodes / ELAPSEDTIME)
            # if GAMEBOARD.played_move_count % 2 != 0:
            #   score = score * -1
            print("info depth " + str(GOBOARD.depth) + " score cp " + str(math.ceil(SCORE)) + " time " + str(ELAPSEDTIME) + " nodes " + str(GOBOARD.nodes) + " nps " + str(NPS) + " pv " + MOVE)
            print("bestmove " + MOVE)
    except (KeyboardInterrupt, SystemExit):
        print('quit')
        sys.exit()
    except Exception as exc:
        print(exc)
        raise
