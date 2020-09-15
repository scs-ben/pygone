#!/usr/bin/env python3
import math, sys, time

PIECEPOINTS = {'p': 100.0, 'r': 500.0, 'n': 300.0, 'b': 300.0, 'q': 1000.0, 'k': 60000.0}

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

ALLPSQT = {'p': PPSQT, 'n': NPSQT, 'b':BPSQT, 'r':RPSQT, 'q':QPSQT, 'k':KPSQT}

MATESCORE = 50000

TTEXACT = 1
TTLOWER = 2
TTUPPER = 3

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
    move_list_pieces = []
    move_list = []
    tt_set = {}

    def __init__(self):
        self.reset()

    def reset(self):
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

    def apply_move(self, uci_coordinate, reverse_promotion=False, reverse_castle=False, override_from_piece='', override_to_piece=''):
        from_letter_number = letter_to_number(uci_coordinate[0:1])
        from_number = abs(int(uci_coordinate[1:2]) - 8)
        to_letter_number = letter_to_number(uci_coordinate[2:3])
        to_number = abs(int(uci_coordinate[3:4]) - 8)
        from_piece = self.board_state[from_number][from_letter_number]
        to_piece = self.board_state[to_number][to_letter_number]
        if len(override_from_piece) > 0:
            from_piece = override_from_piece
        if len(override_to_piece) > 0:
            to_piece = override_to_piece
        if reverse_promotion:
            from_piece = '-'
            to_piece = 'P' if (self.played_move_count % 2 == 0) else 'p'
        if reverse_castle:
            rook_offset = 1
            if uci_coordinate[0:1] == 'c':
                rook_offset = -2
                self.board_state[to_number][to_letter_number - 1] = '-'
            else:
                self.board_state[to_number][to_letter_number + 2] = '-'
            self.board_state[from_number][from_letter_number + rook_offset] = 'R' if (self.played_move_count % 2 == 0) else 'r'
            self.board_state[to_number][to_letter_number] = 'K' if (self.played_move_count % 2 == 0) else 'k'
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

                if self.played_move_count % 2 == 0:
                    self.board_state[from_number][from_letter_number + 1] = 'R'
                else:
                    self.board_state[from_number][from_letter_number + 1] = 'r'
            else:
                self.board_state[to_number][to_letter_number - 2] = '-'
                if self.played_move_count % 2 == 0:
                    self.board_state[from_number][from_letter_number - 1] = 'R'
                else:
                    self.board_state[from_number][from_letter_number - 1] = 'r'

            if self.played_move_count % 2 == 0:
                self.board_state[to_number][to_letter_number] = 'K'
            else:
                self.board_state[to_number][to_letter_number] = 'k'
        else:
            if len(override_to_piece) == 0:
                self.board_state[from_number][from_letter_number] = '-'
            else:
                self.board_state[from_number][from_letter_number] = override_to_piece
            if promote != "":
                if self.played_move_count % 2 == 0:
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
        (from_piece, to_piece) = self.apply_move(uci_coordinate)
        self.move_list.append(uci_coordinate)
        self.move_list_pieces.append([uci_coordinate, from_piece, to_piece])
        self.played_move_count += 1


    def undo_move(self):
        self.move_list.pop()
        old_move = self.move_list_pieces.pop()
        uci_coordinate = old_move[0]
        from_piece = old_move[1]
        to_piece = old_move[2]

        reverse_castle = (uci_coordinate in ('e1g1', 'e1c1') and from_piece == 'K' and to_piece == 'R') or (uci_coordinate in ('e8g8', 'e8c8') and from_piece == 'k' and to_piece == 'r')

        self.apply_move(uci_coordinate[2:4] + uci_coordinate[0:2], len(uci_coordinate) > 4, reverse_castle, from_piece, to_piece)
        self.played_move_count -= 1


    def show_board(self):
        for i in range(8):
            for j in range(8):
                pr(self.board_state[i][j], end=" ")
            pr()

    def board_to_hash(self):
        result = []
        for _list in self.board_state:
            result += _list
        return hash(''.join(result))

    def get_valid_moves(self):
        self.white_valid_moves = []
        self.black_valid_moves = []
        self.white_attack_pieces = []
        self.black_attack_pieces = []
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
                        if white_start_coordinate == 'e1' and eval_state[7][5] == '-' and eval_state[7][6] == '-' and eval_state[7][7] == 'R':
                            self.white_valid_moves.append(white_start_coordinate + 'g1')
                        if white_start_coordinate == 'e1' and eval_state[7][1] == '-' and eval_state[7][2] == '-' and eval_state[7][3] == '-' and eval_state[7][0] == 'R':
                            self.white_valid_moves.append(white_start_coordinate + 'c1')
                    else:
                        if black_start_coordinate == 'e8' and eval_state[0][1] == '-' and eval_state[0][1] == '-' and eval_state[0][2] == '-' and eval_state[0][0] == 'r':
                            self.black_valid_moves.append(black_start_coordinate + 'c8')
                        if black_start_coordinate == 'e8' and eval_state[0][5] == '-' and eval_state[0][6] == '-' and eval_state[0][7] == 'r':
                            self.black_valid_moves.append(black_start_coordinate + 'g8')
                    for _, k_move in king_moves.items():
                        if (k_move['column'] >= 0 and k_move['column'] <= 7 and k_move['row'] >= 0 and k_move['row'] <= 7):
                            eval_piece = eval_state[k_move['row']][k_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())

                            dest = number_to_letter(k_move['column'] + 1) + str(abs(k_move['row'] - 8))

                            if eval_piece == '-' or can_capture:
                                if is_white:
                                    self.white_valid_moves.append(white_start_coordinate + dest)
                                else:
                                    self.black_valid_moves.append(black_start_coordinate + dest)
                            if can_capture:
                                if is_white:
                                    self.white_attack_pieces.append([eval_piece, piece])
                                    self.white_attack_locations += dest
                                else:
                                    self.black_attack_pieces.append([eval_piece, piece])
                                    self.black_attack_locations += dest
                if piece in ('p', 'P'):
                    if piece == 'P':
                        if row > 1 and eval_state[row - 1][column] == '-':
                            self.white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)))
                        if row == 6 and eval_state[row - 1][column] == '-' and eval_state[row - 2][column] == '-':
                            self.white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 10)))
                        if row == 1 and eval_state[row - 1][column] == '-':
                            self.white_valid_moves.append(white_start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)) + 'q')
                        if ((column - 1) >= 0 and (row - 1) >= 0) or ((column + 1) < 8 and (row - 1) >= 0):
                            prom = ''
                            if row == 1:
                                prom = 'q'
                            if (column - 1) >= 0 and eval_state[row - 1][column - 1] != '-' and eval_state[row - 1][column - 1].islower():
                                self.white_valid_moves.append(white_start_coordinate + number_to_letter(column) + str(abs(row - 9)) + prom)
                                self.white_attack_locations += number_to_letter(column) + str(abs(row - 9))
                                self.white_attack_pieces.append([eval_state[row - 1][column - 1], piece])
                            if (column + 1) < 8 and eval_state[row - 1][column + 1] != '-' and eval_state[row - 1][column + 1].islower():
                                self.white_valid_moves.append(white_start_coordinate + number_to_letter(column + 2) + str(abs(row - 9)) + prom)
                                self.white_attack_locations += number_to_letter(column + 2) + str(abs(row - 9))
                                self.white_attack_pieces.append([eval_state[row - 1][column + 1], piece])
                    else:
                        if row < 6 and eval_state[row + 1][column] == '-':
                            self.black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)))
                        if row == 1 and eval_state[row + 1][column] == '-' and eval_state[row + 2][column] == '-':
                            self.black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 6)))
                        if row == 6 and eval_state[row + 1][column] == '-':
                            self.black_valid_moves.append(black_start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)) + 'q')
                        if ((column - 1) >= 0 and (row + 1) < 8) or ((column + 1) < 8 and (row + 1) < 8):
                            prom = ''
                            if row == 6:
                                prom = 'q'

                            if (column + 1) < 8 and eval_state[row + 1][column + 1] != '-' and eval_state[row + 1][column + 1].isupper():
                                self.black_valid_moves.append(black_start_coordinate + number_to_letter(column + 2) + str(abs(row - 7)) + prom)
                                self.black_attack_locations += number_to_letter(column + 2) + str(abs(row - 7))
                                self.black_attack_pieces.append([eval_state[row + 1][column + 1], piece])
                            if (column - 1) >= 0 and eval_state[row + 1][column - 1] != '-' and eval_state[row + 1][column - 1].isupper():
                                self.black_valid_moves.append(black_start_coordinate + number_to_letter(column) + str(abs(row - 7)) + prom)
                                self.black_attack_locations += number_to_letter(column) + str(abs(row - 7))
                                self.black_attack_pieces.append([eval_state[row + 1][column - 1], piece])
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
                        8: {'column': (column - 2), 'row': (row + 1)}
                    }
                    for _, n_move in night_moves.items():
                        if n_move['column'] >= 0 and n_move['column'] <= 7 and n_move['row'] >= 0 and n_move['row'] <= 7:
                            eval_piece = eval_state[n_move['row']][n_move['column']]
                            if is_white:
                                can_capture = (eval_piece != '-' and eval_piece.islower())
                            else:
                                can_capture = (eval_piece != '-' and eval_piece.isupper())
                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(n_move['column'] + 1) + str(abs(n_move['row'] - 8))
                                if is_white:
                                    self.white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        self.white_attack_pieces.append([eval_piece, piece])
                                else:
                                    self.black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        self.black_attack_pieces.append([eval_piece, piece])
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
                                    self.white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        self.white_attack_pieces.append([eval_piece, piece])
                                else:
                                    self.black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        self.black_attack_pieces.append([eval_piece, piece])
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
                            can_capture = (is_white and eval_piece in ('p', 'r', 'b', 'q', 'k')) or (not is_white and eval_piece in ('P', 'R', 'B', 'Q', 'K'))

                            if eval_piece == '-' or can_capture:
                                dest = number_to_letter(temp_col + 1) + str(abs(temp_row - 8))
                                if is_white:
                                    self.white_valid_moves.append(white_start_coordinate + dest)
                                    if can_capture:
                                        self.white_attack_locations += dest
                                        self.white_attack_pieces.append([eval_piece, piece])
                                else:
                                    self.black_valid_moves.append(black_start_coordinate + dest)
                                    if can_capture:
                                        self.black_attack_locations += dest
                                        self.black_attack_pieces.append([eval_piece, piece])
                                if can_capture:
                                    break
                            else:
                                break
                            temp_row += d_move['rowIncrement']
                            temp_col += d_move['colIncrement']

        move_string = ''.join(self.move_list)
        if self.played_move_count % 2 == 0:
            move_copy = self.white_valid_moves.copy()

            for move in move_copy:
                override_remove = ((move == 'e1g1' and ('e1' in move_string or 'f1' in move_string or 'g1' in move_string)) or (move == 'e1c1' and ('e1' in move_string or 'd1' in move_string or 'c1' in move_string)))

                if override_remove:
                    try:
                        self.white_valid_moves.remove(move)
                    except Exception:
                        continue
        else:
            move_copy = self.black_valid_moves.copy()

            for move in move_copy:
                override_remove = ((move == 'e8g8' and ('e8' in move_string or 'f8' in move_string or 'g8' in move_string)) or (move == 'e8c8' and ('e8' in move_string or 'd8' in move_string or 'c8' in move_string)))

                if override_remove:
                    try:
                        self.black_valid_moves.remove(move)
                    except Exception:
                        continue

    def in_check(self, is_white, debug=False):
        if is_white:
            for (attacked, attacker) in self.black_attack_pieces:
                if attacked == 'K':
                    return True
            return False
        else:
            for (attacked, attacker) in self.white_attack_pieces:
                if attacked == 'k':
                    return True
            return False

    def get_side_moves(self, is_white):
        if is_white:
            return self.white_valid_moves

        return self.black_valid_moves

    def order_moves(self, moves, is_white):
        sort_moves = {}

        for move in moves:
            self.make_move(move)
            sort_moves[self.board_evaluation()] = move
            self.undo_move()

        sort_moves = sorted(sort_moves.items(), key=lambda x:x[0], reverse=not is_white)

        return_moves = []
        for sort_move in sort_moves:
            return_moves.append(sort_move[1])

        return return_moves

    def board_evaluation(self):
        b_eval = 0
        for row in range(8):
            for column in range(8):
                piece = self.board_state[row][column]
                is_white = piece.isupper()
                if piece != '-':
                    if is_white:
                        b_eval += PIECEPOINTS[piece.lower()]
                        b_eval += (ALLPSQT[piece.lower()][row][column] / 100)
                    else:
                        b_eval -= PIECEPOINTS[piece]
                        b_eval -= (ALLPSQT[piece][abs(row-7)][abs(column-7)] / 100)

        return b_eval

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

            if time.perf_counter() >= self.end_time or depth < 1:
                break

        return [iterative_score, iterative_move]

    def search(self, local_board, depth):
        is_white = local_board.played_move_count % 2 == 0

        global_score = -1e8
        chosen_move = None

        alpha = -1e8
        beta = 1e8

        local_board.get_valid_moves()
        poss_mvs = local_board.get_side_moves(is_white)
        poss_mvs = local_board.order_moves(poss_mvs, is_white)
        depth = max(depth, 1)

        for move in poss_mvs:
            self.nodes += 1

            local_board.make_move(move)
            local_board.get_valid_moves()

            if not local_board.in_check(is_white):
                local_score = self.negamax(local_board, alpha, beta, depth - 1)
                if local_score >= global_score:
                    global_score = local_score
                    chosen_move = move

            local_board.undo_move()

        return [global_score, chosen_move]


    def negamax(self, local_board, alpha, beta, depth):
        original_alpha = alpha

        tt_entry = self.transposition_table_lookup(local_board)
        if tt_entry.depth >= depth:
            if tt_entry.flag == TTEXACT:
                return tt_entry.value
            elif tt_entry.flag == TTLOWER:
                alpha = max(alpha, tt_entry.value)
            elif tt_entry.flag == TTUPPER:
                beta = min(beta, tt_entry.value)

            if alpha >= beta:
                return tt_entry.value

        is_white = local_board.played_move_count % 2 == 0

        local_board.get_valid_moves()
        poss_mvs = local_board.get_side_moves(is_white)
        poss_mvs = local_board.order_moves(poss_mvs, is_white)

        if len(poss_mvs) == 0 or (depth <= 0):
            if is_white:
                return local_board.board_evaluation()
            else:
                return -1 * local_board.board_evaluation()

        value = -1e8

        for move in poss_mvs:
            local_board.make_move(move)
            local_board.get_valid_moves()

            if not local_board.in_check(is_white):
                self.nodes += 1
                value = max(value, -self.negamax(local_board, -beta, -alpha, depth - 1))
                alpha = max(alpha, value)
            local_board.undo_move()

            if alpha >= beta:
                break

        tt_entry.value = value
        if value <= original_alpha:
            tt_entry.flag = TTUPPER
        elif value >= beta:
            tt_entry.flag = TTLOWER
        else:
            tt_entry.flag = TTEXACT
        tt_entry.depth = depth
        self.update_transposition_table_entry(tt_entry)

        return value

    def transposition_table_lookup(self, local_board):
        board_hash = local_board.board_to_hash()

        if board_hash in game_board.tt_set.keys():
            tt_entry = game_board.tt_set[board_hash]
        else:
            tt_entry = TranspositionTableEntry()
            tt_entry.board_hash = board_hash
            game_board.tt_set[board_hash] = tt_entry

        return tt_entry

    def update_transposition_table_entry(self, tt_entry):
        game_board.tt_set[tt_entry.board_hash].value = tt_entry.value
        game_board.tt_set[tt_entry.board_hash].flag = tt_entry.flag
        game_board.tt_set[tt_entry.board_hash].depth = tt_entry.depth
        game_board.tt_set[tt_entry.board_hash].value = tt_entry.value

class TranspositionTableEntry:
    value = -1e8
    flag = TTLOWER
    depth = 0
    board_hash = ''

game_board = Board()

def main():

    while True:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print("pygone 1.0 by rcostheta")
                print("uciok")
            elif line == "ucinewgame":
                game_board.reset()
            elif line == "eval":
                game_board.get_valid_moves()
                print('wval: ', game_board.get_side_moves(1))
                print('bval: ', game_board.get_side_moves(0))
                print(game_board.board_evaluation(1))
                print(game_board.tt_set)
                game_board.show_board()
            elif line == "isready":
                print("readyok")
            elif line.startswith("position"):
                moves = line.split()
                offset_moves = game_board.played_move_count + 3
                for position_move in moves[offset_moves:]:
                    game_board.make_move(position_move)
                    offset_moves += 1
                game_board.played_move_count = (offset_moves - 3)
            elif line.startswith("go"):
                go_board = Board()
                go_board.set_board_state([x[:] for x in game_board.board_state.copy()])
                go_board.played_move_count = game_board.played_move_count
                go_board.get_valid_moves()

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

                # if go_depth < 2:
                #     go_depth = 2

                time_move_calc = 40
                if game_board.played_move_count > 38:
                    time_move_calc = 2
                else:
                    time_move_calc = 40 - game_board.played_move_count

                if game_board.played_move_count % 2 == 0:
                    move_time = white_time / (time_move_calc * 1000)
                else:
                    move_time = black_time / (time_move_calc * 1000)

                move_time -= 3

                if move_time < 8:
                    move_time = 8

                if move_time < 10 and go_depth > 4:
                    go_depth = 4

                searcher = Search()

                start_time = time.perf_counter()
                (score, move) = searcher.iterative_search(go_board, go_depth, move_time)
                print("bestmove " + move)
        except (KeyboardInterrupt, SystemExit):
            print('quit')
            sys.exit()
        except Exception as exc:
            print(exc)
            raise

main()
