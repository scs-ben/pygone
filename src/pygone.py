#!/usr/bin/env pypy3
import math, sys, time

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

def letter_to_number(letter):
    return abs((ord(letter) - 96) - 1)

def number_to_letter(number):
    return chr(number + 96)

def print_to_terminal(letter):
    print(letter, flush=True)

def get_perf_counter():
    return time.perf_counter()

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

    def reset(self):
        self.set_default_board_state()
        self.played_move_count = 0
        self.white_valid_moves = []
        self.black_valid_moves = []
        self.white_attack_pieces = []
        self.black_attack_pieces = []
        self.white_attack_locations = ''
        self.black_attack_locations = ''
        self.white_king_location = 'e1'
        self.black_king_location = 'e8'
        self.move_list_pieces = []
        self.move_list = []

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
        (from_piece, to_piece) = self.apply_move(uci_coordinate)
        self.move_list.append(uci_coordinate)
        self.move_list_pieces.append([uci_coordinate, from_piece, to_piece])
        self.played_move_count += 1
        self.get_valid_moves()

    def undo_move(self):
        self.move_list.pop()
        old_move = self.move_list_pieces.pop()
        uci_coordinate = old_move[0]
        from_piece = old_move[1]
        to_piece = old_move[2]

        reverse_castle = uci_coordinate in ('e1g1', 'e1c1', 'e8g8', 'e8c8') and from_piece in ('K', 'k')

        self.played_move_count -= 1
        self.apply_move(uci_coordinate[2:4] + uci_coordinate[0:2], len(uci_coordinate) > 4, reverse_castle, from_piece, to_piece)

    #def show_board(self):
    #    for i in range(8):
    #        for j in range(8):
    #            print(self.board_state[i][j], end=" ")
    #        print()

    def str_board(self):
        s_board = ''
        for i in range(8):
            for j in range(8):
                s_board += self.board_state[i][j]
        return s_board

    def get_valid_moves(self):
        is_white = self.played_move_count % 2 == 0

        valid_moves = []
        attack_pieces = []
        attack_locations = ''

        if (is_white):
            self.white_valid_moves = []
            self.white_attack_pieces = []
            self.white_attack_locations = ''
        else:
            self.black_valid_moves = []
            self.black_attack_pieces = []
            self.black_attack_locations = ''

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
                        self.white_king_location = start_coordinate
                        if start_coordinate == 'e1' and eval_state[7][5] == '-' and eval_state[7][6] == '-' and eval_state[7][7] == 'R':
                            valid_moves.append(start_coordinate + 'g1')
                        if start_coordinate == 'e1' and eval_state[7][1] == '-' and eval_state[7][2] == '-' and eval_state[7][3] == '-' and eval_state[7][0] == 'R':
                            valid_moves.append(start_coordinate + 'c1')
                    else:
                        self.black_king_location = start_coordinate
                        if start_coordinate == 'e8' and eval_state[0][1] == '-' and eval_state[0][2] == '-' and eval_state[0][3] == '-' and eval_state[0][0] == 'r':
                            valid_moves.append(start_coordinate + 'c8')
                        if start_coordinate == 'e8' and eval_state[0][5] == '-' and eval_state[0][6] == '-' and eval_state[0][7] == 'r':
                            valid_moves.append(start_coordinate + 'g8')
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
                                attack_pieces.append([eval_piece, piece, start_coordinate + dest])
                                attack_locations += dest
                if piece.lower() == 'p':
                    if is_white:
                        if row > 1 and eval_state[row - 1][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)))
                        if row == 6 and eval_state[row - 1][column] == '-' and eval_state[row - 2][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 10)))
                        if row == 1 and eval_state[row - 1][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 9)) + 'q')
                        if ((column - 1) >= 0 and (row - 1) >= 0) or ((column + 1) < 8 and (row - 1) >= 0):
                            prom = ''
                            if row == 1:
                                prom = 'q'
                            if (column - 1) >= 0 and eval_state[row - 1][column - 1] != '-' and eval_state[row - 1][column - 1].islower():
                                dest = number_to_letter(column) + str(abs(row - 9))
                                valid_moves.append(start_coordinate + dest + prom)
                                attack_locations += dest
                                attack_pieces.append([eval_state[row - 1][column - 1], piece, start_coordinate + dest + prom])
                            if (column + 1) < 8 and eval_state[row - 1][column + 1] != '-' and eval_state[row - 1][column + 1].islower():
                                dest = number_to_letter(column + 2) + str(abs(row - 9))
                                valid_moves.append(start_coordinate + dest + prom)
                                attack_locations += dest
                                attack_pieces.append([eval_state[row - 1][column + 1], piece, start_coordinate + dest + prom])
                    else:
                        if row < 6 and eval_state[row + 1][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)))
                        if row == 1 and eval_state[row + 1][column] == '-' and eval_state[row + 2][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 6)))
                        if row == 6 and eval_state[row + 1][column] == '-':
                            valid_moves.append(start_coordinate + number_to_letter(column + 1) + str(abs(row - 7)) + 'q')
                        if ((column - 1) >= 0 and (row + 1) < 8) or ((column + 1) < 8 and (row + 1) < 8):
                            prom = ''
                            if row == 6:
                                prom = 'q'

                            if (column + 1) < 8 and eval_state[row + 1][column + 1] != '-' and eval_state[row + 1][column + 1].isupper():
                                dest = number_to_letter(column + 2) + str(abs(row - 7))
                                valid_moves.append(start_coordinate + dest + prom)
                                attack_locations += dest
                                attack_pieces.append([eval_state[row + 1][column + 1], piece, start_coordinate + dest + prom])
                            if (column - 1) >= 0 and eval_state[row + 1][column - 1] != '-' and eval_state[row + 1][column - 1].isupper():
                                dest = number_to_letter(column) + str(abs(row - 7))
                                valid_moves.append(start_coordinate + dest + prom)
                                attack_locations += dest
                                attack_pieces.append([eval_state[row + 1][column - 1], piece, start_coordinate + dest + prom])
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
                                    attack_locations += dest
                                    attack_pieces.append([eval_piece, piece, start_coordinate + dest])
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
                                if can_capture:
                                    attack_locations += dest
                                    attack_pieces.append([eval_piece, piece, start_coordinate + dest])
                                    break
                            else:
                                break
                            temp_row += a_move['rowIncrement']
                            temp_col += a_move['colIncrement']

        if (is_white):
            self.white_valid_moves = valid_moves
            self.white_attack_locations = attack_locations
            self.white_attack_pieces = attack_pieces
        else:
            self.black_valid_moves = valid_moves
            self.black_attack_locations = attack_locations
            self.black_attack_pieces = attack_pieces

        move_string = ''.join(self.move_list)
        if is_white:
            move_copy = self.white_valid_moves.copy()
            check_string = ''.join(self.black_valid_moves.copy())

            for s_move in move_copy:
                override_remove = ((s_move == 'e1g1' and ('e1' in move_string or 'h1' in move_string or 'e1' in check_string or 'f1' in check_string or 'g1' in check_string)) or \
                    (s_move == 'e1c1' and ('e1' in move_string or 'a1' in move_string or 'c1' in check_string or 'd1' in check_string or 'e1' in check_string)))

                if override_remove:
                    try:
                        self.white_valid_moves.remove(s_move)
                    except Exception:
                        continue
        else:
            move_copy = self.black_valid_moves.copy()
            check_string = ''.join(self.white_valid_moves.copy())

            for s_move in move_copy:
                override_remove = ((s_move == 'e8g8' and ('e8' in move_string or 'h8' in move_string or 'e8' in check_string or 'f8' in check_string or 'g8' in check_string)) or \
                    (s_move == 'e8c8' and ('e8' in move_string or 'a8' in move_string or 'c8' in check_string or 'd8' in check_string or 'e8' in check_string)))

                if override_remove:
                    try:
                        self.black_valid_moves.remove(s_move)
                    except Exception:
                        continue

    def in_check(self, is_white):
        if is_white:
            for (attacked, attacker, _) in self.black_attack_pieces:
                if attacked == 'K':
                    return 1
            return 0
        else:
            for (attacked, attacker, _) in self.white_attack_pieces:
                if attacked == 'k':
                    return 1
            return 0

    def get_side_moves(self, is_white):
        if is_white:
            return self.white_valid_moves

        return self.black_valid_moves

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

        self.v_depth = 0
        while v_depth > 0:
            self.v_depth += 1
            v_depth -= 1

            (iterative_score, iterative_move) = self.search(local_board, self.v_depth)

            elapsed_time = math.ceil(get_perf_counter() - start_time)
            v_nps = math.ceil(self.v_nodes / elapsed_time)

            self.print_stats(str(self.v_depth), str(math.ceil(iterative_score)), str(elapsed_time), str(self.v_nodes), str(v_nps), iterative_move)

            if get_perf_counter() >= self.end_time or v_depth < 1:
                break

        # (iterative_score, iterative_move) = self.search(local_board, self.v_depth)

        return [iterative_score, iterative_move]

    def print_stats(self, v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
        print_to_terminal("info depth " + v_depth + " score cp " + v_score + " time " + v_time + " nodes " + v_nodes + " nps " + v_nps + " pv " + v_pv)

    def search(self, local_board, v_depth):
        global_score = -1e8
        chosen_move = None

        local_score = -1e8

        alpha = -1e8
        beta = 1e8

        is_white = local_board.played_move_count % 2 == 0
        local_board.get_valid_moves()
        poss_mvs = local_board.get_side_moves(is_white)
        v_depth = max(v_depth, 1)

        for s_move in poss_mvs:
            self.v_nodes += 1

            local_board.make_move(s_move)
            if not local_board.in_check(is_white):
                local_score = -self.pvs(local_board, -beta, -alpha, v_depth - 1)

                if local_score >= global_score:
                    global_score = local_score
                    chosen_move = s_move

            local_board.undo_move()

        return [global_score, chosen_move]

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
            print('bucket dump')
            self.tt_bucket = {}
        self.tt_bucket[board_string] = tt_entry

    def pvs(self, local_board, alpha, beta, v_depth):
        is_white = local_board.played_move_count % 2 == 0

        local_board.get_valid_moves()
        poss_mvs = local_board.get_side_moves(is_white)

        if len(poss_mvs) == 0 or v_depth <= 0:
            b_eval = local_board.board_evaluation()
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
                return tt_entry['tt_value']

        local_score = -1e8

        for s_move in poss_mvs:
            self.v_nodes += 1

            local_board.make_move(s_move)

            if not local_board.in_check(is_white):
                local_score = -self.pvs(local_board, -alpha - 1, -alpha, v_depth - 1)
                if local_score > alpha and local_score < beta:
                    local_score = -self.pvs(local_board, -beta, -local_score, v_depth - 1)

            local_board.undo_move()

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
        tt_entry['tt_depth'] = v_depth
        self.store_tt(local_board, tt_entry)

        return alpha

EXACT=1
UPPER=2
LOWER=3

game_board = Board()
game_board.reset()

def main():
    searcher = Search()

    while 1:
        try:
            line = input()
            if line == "quit":
                sys.exit()
            elif line == "uci":
                print_to_terminal("pygone 1.0\nuciok")
            elif line == "ucinewgame":
                game_board.reset()
                searcher.reset()
            elif line == "isready":
                print_to_terminal("readyok")
            elif line.startswith("position"):
                moves = line.split()
                game_board.reset()
                for position_move in moves[3:]:
                    game_board.make_move(position_move)
            elif line.startswith("go"):
                white_time = 1e8
                black_time = 1e8
                go_depth = 8

                args = line.split()
                for key, arg in enumerate(args):
                    if arg == 'wtime':
                        white_time = int(args[key + 1])
                    if arg == 'btime':
                        black_time = int(args[key + 1])
                    if arg == 'depth':
                      go_depth = int(args[key + 1])

                time_move_calc = max(40 - game_board.played_move_count, 2)

                move_time = 1e8

                is_white = game_board.played_move_count % 2 == 0

                if is_white:
                    move_time = white_time / (time_move_calc * 1e3)
                else:
                    move_time = black_time / (time_move_calc * 1e3)

                if move_time < 15:
                    go_depth = 5
                if move_time < 4:
                    move_time = 2
                    go_depth = 4

                searcher.v_nodes = 0
                searcher.v_tthits = 0
                (score, s_move) = searcher.iterative_search(game_board, go_depth, move_time)
                print_to_terminal("bestmove " + s_move)
        except (KeyboardInterrupt, SystemExit):
            print_to_terminal('quit')
            sys.exit()
        except Exception as exc:
            print_to_terminal(exc)
            raise

main()
