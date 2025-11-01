#PIECEPOINTS = {'p': 85, 'n': 295, 'b': 300, 'r': 700, 'q': 1350, 'k': 32767}
PIECEPOINTS = {'p': 100, 'n': 320, 'b': 325, 'r': 500, 'q': 975, 'k': 32767}

ALLPSQT = {
    'p': (
        0,0,0,0,0,0,0,0,
        30,30,30,30,30,30,30,30,
        8,8,17,26,26,17,8,8,
        5, 5,8,24,24,8, 5, 5,
        0, 0, 0,24,24, 0, 0, 0,
        5,-5,-8, 6, 6,-8,-5, 5,
        5,8,8,-22,-22,8,8, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ),
    'n': (
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20, 0, 0, 0, 0,-20,-40,
        -30, 0,8,13,13,8, 0,-30,
        -30, 5,13,18,18,13, 5,-30,
        -30, 0,13,18,18,13, 0,-30,
        -30, 5,7,13,13,7, 5,-30,
        -40,-20, 0, 5, 5, 0,-20,-40,
        -50,-40,-20,-30,-30,-20,-40,-50,
    ),
    'b': (
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10, 0, 0, 0, 0, 0, 0,-10,
        -10, 0, 5,10,10, 5, 0,-10,
        -10, 5, 5,10,10, 5, 5,-10,
        -10, 0,10,10,10,10, 0,-10,
        -10,10,10,10,10,10,10,-10,
        -10, 5, 0, 0, 0, 0, 5,-10,
        -20,-10,-40,-10,-10,-40,-10,-20,
    ),
    'r': (
        10,20,20,20,20,20,20, 10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0, 0, 0, 0, 0,-10 ,
        -10, 0, 0,10,10, 10, 0,-10,
    ),
    'q': (
        -40,-20,-20,-10,-10,-20,-20,-40 ,
        -20, 0, 0, 0, 0, 0, 0,-20 ,
        -20, 0,10,10,10,10, 0,-20 ,
        -10, 0,10,10,10,10, 0,-10 ,
        0, 0,10,10,10,10, 0,-10 ,
        -20,10,10,10,10,10, 0,-20 ,
        -20, 0,10, 0, 0, 0, 0,-20 ,
        -40,-20,-20,-10,-10,-20,-20,-40
    ),
    'k': (
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10, 0, 0,-10,-20,-30,
        -30,-10,20,30,30,20,-10,-30,
        -30,-10,30,40,40,30,-10,-30,
        -30,-10,30,40,40,30,-10,-30,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20,20,0,0,0,0,20,20,
        20,20,35,0,0,10,35,20),
}

for set_piece, set_board in ALLPSQT.items():
    prow = lambda row: (0,) + tuple(piece+PIECEPOINTS[set_piece] for piece in row) + (0,)
    ALLPSQT[set_piece] = sum((prow(set_board[column*8:column*8+8]) for column in range(8)), ())
    ALLPSQT[set_piece] = (0,)*20 + ALLPSQT[set_piece] + (0,)*20

def get_moves(piece):
    if piece == 'k':
        return [(0, 10), (0, -10), (1, 0), (-1, 0), (1, 10), (1, -10), (-1, 10), (-1, -10)]
    elif piece == 'q':
        return [(0, 10), (0, -10), (1, 0), (-1, 0), (1, 10), (1, -10), (-1, 10), (-1, -10)]
    elif piece == 'r':
        return [(0, 10), (0, -10), (1, 0), (-1, 0)]
    elif piece == 'b':
        return [(1, 10), (1, -10), (-1, 10), (-1, -10)]
    elif piece == 'n':
        return [(1, -20), (-1, -20), (2, -10), (-2, -10), (1, 20), (-1, 20), (2, 10), (-2, 10)]
    else:
        return [(0, -10), (1, -10), (-1, -10)]

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

class Board:
    board_string = ''
    played_move_count = 0
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
        l_board_state = self.board_state;
        self.board_state = l_board_state[:board_position] + piece + l_board_state[board_position + 1:]

    def apply_move(self, uci_coordinate):
        l_board_state = self.board_state;

        is_white = self.played_move_count % 2 == 0

        self.move_counter += 1

        # break uci coordinate into location in board state list
        (from_number, to_number) = unpack_coordinate(uci_coordinate)

        from_piece = l_board_state[from_number].lower()

        if l_board_state[to_number] != '-':
            self.move_counter = 0

        self.mutate_board(to_number, l_board_state[from_number])
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
            elif len(uci_coordinate) > 4:
                self.mutate_board(to_number, uci_coordinate[4:5].upper() if is_white else uci_coordinate[4:5])
        elif from_piece == 'k':
            if is_white:
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            if abs(to_number - from_number) == 2:
                self.mutate_board(to_number + (1 if to_number > from_number else -2), '-')
                self.mutate_board(from_number + ((to_number - from_number) // 2), 'R' if is_white else 'r')

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

        board.played_move_count += 1
        board.rolling_score = -board.rolling_score

        board.repetitions.append(board.board_string)

        return board

    def nullmove(self):
        """ allows for a quick way to let other side move """
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = self.board_copy()
        board.played_move_count += 1
        board.rolling_score = -self.rolling_score

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
        board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()

        return board

    def get_piece_count(self):
        return 64 - self.board_string.count('-')

    def is_endgame(self):
        return self.piece_count < 14 or (self.piece_count < 20 and 'q' not in self.board_string.lower())

    def move_sort(self, uci_coordinate):
        return self.calculate_score(uci_coordinate, True)

    def calculate_score(self, uci_coordinate, sorting=False):
        is_white = self.played_move_count % 2 == 0
        p_offset = -10 if is_white else 10
        p_piece = 'P' if is_white else 'p'
        is_endgame = self.is_endgame()

        l_board_state = self.board_state

        (from_number, to_number) = unpack_coordinate(uci_coordinate)

        # to_offset = to_number if is_white else abs(to_number - 119) + ((to_number % 10) - (abs(to_number - 119) % 10))
        # from_offset = from_number if is_white else abs(from_number - 119) + (from_number % 10) - (abs(from_number - 119) % 10)

        offset = 0 if is_white else 119
        to_offset = abs(to_number - offset)
        from_offset = abs(from_number - offset)

        local_score = 0

        from_piece = l_board_state[from_number].lower()

        to_piece = l_board_state[to_number].lower()

        local_score += ALLPSQT[from_piece][to_offset] - \
                        ALLPSQT[from_piece][from_offset]

        if to_piece != '-':
            local_score += ALLPSQT[to_piece][to_offset]

        if from_piece == 'p':
            if uci_coordinate[2:4] == self.en_passant:
                # add in an extra pawn for EP capture
                local_score += ALLPSQT[from_piece][to_offset]
            elif len(uci_coordinate) > 4:
                promote = uci_coordinate[4:5]
                # adjust value for promoting from pawn to queen
                local_score += ALLPSQT[promote][to_offset] - \
                                ALLPSQT['p'][to_offset]

            #if self.passer_pawn(from_number):
            #    local_score += 8
            #if self.stacked_pawn(from_number):
            #    local_score -= 5
        elif from_piece == 'k':
            #local_score += self.king_safety(is_white)
            if abs(to_number - from_number) == 2:
                if to_number > from_number:
                    local_score += ALLPSQT['r'][to_offset - 1] - \
                                    ALLPSQT['r'][to_offset + 1]
                else:
                    local_score += ALLPSQT['r'][to_offset + 1] - \
                                    ALLPSQT['r'][to_offset - 2]

                # put castling higher up
                local_score += 10
            else:
                local_score -= 20

        return local_score

    def passer_pawn(self, pos):
        piece = self.board_state[pos]
        if piece not in ('P', 'p'):
            return False  # not a pawn

        is_white = piece == 'P'
        forward = -10 if is_white else 10
        enemy_pawn = 'p' if is_white else 'P'

        # Check all squares ahead (including diagonals) for blocking/capturing enemy pawns
        offset_dirs = [forward - 1, forward, forward + 1]  # left, center, right columns

        check_pos = pos + forward
        while 20 <= check_pos <= 99:
            for offset in offset_dirs:
                test_square = check_pos + (offset - forward)  # adjust for diagonals
                if 20 <= test_square <= 99 and self.board_state[test_square] == enemy_pawn:
                    return False
            check_pos += forward

        return True

    def stacked_pawn(self, pos):
        piece = self.board_state[pos]
        if piece not in ('P', 'p'):
            return False

        is_white = piece == 'P'
        offset = -10 if is_white else 10

        # Look ahead on same file
        current = pos + offset
        while 20 <= current <= 99:
            if self.board_state[current] == piece:
                return True
            current += offset

        # Optionally also check behind (if you want either pawn to register as stacked)
        current = pos - offset
        while 20 <= current <= 99:
            if self.board_state[current] == piece:
                return True
            current -= offset

        return False
   
    def king_safety(self, is_white):
        king_pos = coordinate_to_position(self.white_king_position if is_white else self.black_king_position)

        forward = -10 if is_white else 10
        pawn = 'P' if is_white else 'p'

        # 1 Pawn shield directly in front of the king
        pawn_cover = 0
        for side in (-1, 0, 1):  # left, center, right
            sq = king_pos + forward + side
            if 20 <= sq <= 99 and self.board_state[sq] == pawn:
                pawn_cover += 1

        # 2 Open files / semi-open files near king
        open_file_penalty = 0
        for side in (-1, 0, 1):
            fwd = king_pos + forward
            while 20 <= fwd <= 99:
                piece = self.board_state[fwd]
                if piece in ('P', 'p'):
                    break  # blocked by any pawn
                fwd += forward
            else:
                # No blocking pawn found: open file in front of king
                open_file_penalty += 10

        # 3 Score: more pawn cover = safe, open file = unsafe
        score = pawn_cover * 10 - open_file_penalty - 20
        return score
    
    def str_board(self):
        return self.board_state + \
          str(self.played_move_count % 2)

    def generate_valid_captures(self):
        return self.generate_valid_moves(True)

    def generate_valid_moves(self, captures_only=False):
        """Return list of valid (maybe illegal) moves"""
        offset = 1

        if self.played_move_count % 2 == 0:
            is_white = True

            max_row = 81
            min_row = 31
            valid_pieces = 'prnbqk-'
        else:
            is_white = False

            max_row = 31
            min_row = 81
            valid_pieces = 'PRNBQK-'

        for board_position, piece in enumerate(self.board_state):
            if piece in "-." or is_white == piece.islower():
                continue

            start_coordinate = position_to_coordinate(board_position)

            piece_lower = piece.lower()

            if piece == 'p':
                offset = -1

            # castling
            if not captures_only:
                if piece == 'K':
                    if self.white_castling[1] and self.board_state[96:99] == '--R' and \
                        not any(self.attack_position(is_white, coordinate) for coordinate in ['e1', 'f1', 'g1']):
                        yield start_coordinate + 'g1'
                    if self.white_castling[0] and self.board_state[91:95] == 'R---' and \
                        not any(self.attack_position(is_white, coordinate) for coordinate in ['e1', 'd1', 'c1']):
                        yield start_coordinate + 'c1'
                elif piece == 'k':
                    if self.black_castling[1] and self.board_state[26:29] == '--r' and \
                        not any(self.attack_position(is_white, coordinate) for coordinate in ['e8', 'f8', 'g8']):
                        yield start_coordinate + 'g8'
                    if self.black_castling[0] and self.board_state[21:25] == 'r---' and \
                        not any(self.attack_position(is_white, coordinate) for coordinate in ['e8', 'd8', 'c8']):
                        yield start_coordinate + 'c8'
                elif piece_lower == 'p' and \
                    max_row <= board_position < max_row + 8 and \
                    self.board_state[board_position + -10*offset] == '-' and \
                    self.board_state[board_position + -20*offset] == '-':
                    yield start_coordinate + position_to_coordinate(board_position + -20*offset)

            for piece_move in get_moves(piece_lower):
                to_position = board_position + piece_move[0] + (piece_move[1] * offset)

                while 20 < to_position < 99:
                    eval_piece = self.board_state[to_position]

                    if not captures_only or (captures_only and eval_piece not in '-.'):

                        dest = position_to_coordinate(to_position)

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
        valid_pieces = 'PRNBQK-' if is_white else 'prnbqk-'

        attack_position = coordinate_to_position(coordinate)

        for board_position, piece in enumerate(self.board_state):
            if piece in "-." or is_white == piece.isupper():
                continue

            if piece == 'p':
                offset = -1

            piece = piece.lower()

            for piece_move in get_moves(piece):
                if piece == 'p' and not piece_move[0]:
                    continue

                to_position = board_position + piece_move[0] + (offset * piece_move[1])

                while 20 < to_position < 99:
                    eval_piece = self.board_state[to_position]

                    if eval_piece in valid_pieces and to_position == attack_position:
                        return True

                    if eval_piece != '-' or piece in 'knp':
                        break

                    to_position = to_position + piece_move[0] + offset * piece_move[1]

        return False
