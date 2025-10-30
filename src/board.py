#!/usr/bin/env python3
import random

# New numerical piece constants (0x88 friendly)
# Pieces 1-6 are Black, 7-12 are White. This is just one convention.
EMPTY = 0
OFF_BOARD = 99 # Using a high number for off-board squares

# Black Pieces (Lower-case)
p, n, b, r, q, k = 1, 2, 3, 4, 5, 6
# White Pieces (Upper-case)
P, N, B, R, Q, K = 7, 8, 9, 10, 11, 12

# Mapping for initialization and Zobrist key
CHAR_TO_NUM = {
    '.': OFF_BOARD, '-': EMPTY,
    'p': p, 'n': n, 'b': b, 'r': r, 'q': q, 'k': k,
    'P': P, 'N': N, 'B': B, 'R': R, 'Q': Q, 'K': K
}
NUM_TO_CHAR = {v: k for k, v in CHAR_TO_NUM.items()}

PIECEPOINTS = {'p': 85, 'n': 295, 'b': 300, 'r': 700, 'q': 1350, 'k': 32767}

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

# 1. Remap the dictionary keys using the CHAR_TO_NUM mapping
NUMERICAL_ALLPSQT = {}
for char_piece, psqt_values in ALLPSQT.items():
    # We use the corresponding *numerical* piece constant as the key
    # We only need the lowercase piece, as the array logic handles the side-to-move offset later
    num_piece = CHAR_TO_NUM[char_piece]
    NUMERICAL_ALLPSQT[num_piece] = psqt_values

# 2. **CRITICAL:** Update the global PSQT name
ALLPSQT = NUMERICAL_ALLPSQT

# 3. Update the initialization logic (which must run *after* the remapping)
# The PIECEPOINTS must also be remapped to numerical keys.

NUMERICAL_PIECEPOINTS = {}
for char_piece, value in PIECEPOINTS.items():
    NUMERICAL_PIECEPOINTS[CHAR_TO_NUM[char_piece]] = value

PIECEPOINTS = NUMERICAL_PIECEPOINTS

# Run the PSQT pre-calculation, using the numerical keys
for set_piece_num, set_board in ALLPSQT.items():
    # Use PIECEPOINTS with numerical key
    prow = lambda row: (0,) + tuple(piece + PIECEPOINTS[set_piece_num] for piece in row) + (0,)
    ALLPSQT[set_piece_num] = sum((prow(set_board[column*8:column*8+8]) for column in range(8)), ())
    ALLPSQT[set_piece_num] = (0,)*20 + ALLPSQT[set_piece_num] + (0,)*20

class Board:
    board_string = ''
    hash = 0
    ZOBRIST = {}
    ZOBRIST_CASTLE = []
    ZOBRIST_EP = []
    ZOBRIST_SIDE = 0
    played_move_count = 0
    repetitions = []
    white_castling = [True, True]
    black_castling = [True, True]
    white_king_position = 'e1'
    black_king_position = 'e8'
    rolling_score = 0
    piece_count = 32
    en_passant = ''
    en_passant_file_index = 0
    move_counter = 0

    def __init__(self):
        initial_board_string = (
            '..........' #  0 -  9
            '..........' # 10 - 19
            '.rnbqkbnr.' # 20 - 29
            '.pppppppp.' # 30 - 39
            '.--------.' # 40 - 49
            '.--------.' # 50 - 59
            '.--------.' # 60 - 69
            '.--------.' # 70 - 79
            '.PPPPPPPP.' # 80 - 89
            '.RNBQKBNR.' # 90 - 99
            '..........' # 100 -109
            '..........' # 110 -119
            )
        
        self.board_state = [CHAR_TO_NUM[char] for char in initial_board_string]
        
        self.hash = 0
        self.init_zobrist()
        
        # Iterate through the numerical list
        for pos, piece_num in enumerate(self.board_state):
            if piece_num != EMPTY and piece_num != OFF_BOARD:
                # Need to use the piece character for the ZOBRIST dict key
                self.hash ^= self.ZOBRIST[(piece_num, pos)]
                
        # Initialize board_string for str_board compatibility
        self.board_string = self.str_board()

    def init_zobrist(self):
        # Initializes Zobrist hash keys using numerical piece IDs instead of character strings.
        global CHAR_TO_NUM # Ensure the mapping is accessible

        random.seed(42)  # deterministic for testing
        self.ZOBRIST = {}
        
        # Iterate over all piece character strings
        for piece_char in "prnbqkPRNBQK":
            # *** CORE CHANGE: Get the numerical ID for the piece ***
            piece_num = CHAR_TO_NUM[piece_char]
            
            # Use the numerical ID as the first part of the dictionary key
            for square in range(120):
                # The Zobrist key is now a tuple: (numerical_piece_ID, square_index)
                self.ZOBRIST[(piece_num, square)] = random.getrandbits(64)
        
        # Other Zobrist keys remain the same (they are already numerical lists/variables)
        self.ZOBRIST_CASTLE = [random.getrandbits(64) for _ in range(4)]
        self.ZOBRIST_EP = [random.getrandbits(64) for _ in range(8)]
        self.ZOBRIST_SIDE = random.getrandbits(64)

    def unpack_coordinate(self, uci_coordinate):
        return (self.coordinate_to_position(uci_coordinate[0:2]),
                self.coordinate_to_position(uci_coordinate[2:4]))
        
    def position_to_coordinate(self, board_position):
        return self.number_to_letter(board_position % 10) + str(abs(board_position // 10 - 10))

    def coordinate_to_position(self, coordinate):
        if len(coordinate) == 2:
            return 10 * (abs(int(coordinate[1]) - 8) + 2) + (ord(coordinate[0]) - 97) + 1

    def mutate_board(self, pos, new_piece_num):
        # pos is the 120-square index, new_piece_num is an integer (e.g., K=12)
        old_piece_num = self.board_state[pos]
        
        # Only XOR out pieces that actually exist on the board (not empty or off-board)
        if old_piece_num != EMPTY and old_piece_num != OFF_BOARD:
            self.hash ^= self.ZOBRIST[(old_piece_num, pos)]
            
        if new_piece_num != EMPTY and new_piece_num != OFF_BOARD:
            self.hash ^= self.ZOBRIST[(new_piece_num, pos)]

        self.hash ^= self.ZOBRIST_EP[self.en_passant_file_index] if self.en_passant else 0

        # *** CORE CHANGE: Update board state using list assignment (fast!) ***
        self.board_state[pos] = new_piece_num

    def str_board(self):
        # Convert the numerical board state back to a string
        board_str = "".join(NUM_TO_CHAR[p] for p in self.board_state)
        return board_str + str(self.played_move_count % 2)

    def get_moves(self, piece):
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
            return [(0, 10), (1, 10), (-1, 10)]

    def number_to_letter(self, to_number):
        return chr(to_number + 96)

    def apply_move(self, uci_coordinate):
        
        global EMPTY, P, R, CHAR_TO_NUM # Ensure access to global constants/mappings
        
        is_white = self.played_move_count % 2 == 0

        self.move_counter += 1

        # break uci coordinate into location in board state list
        (from_number, to_number) = self.unpack_coordinate(uci_coordinate)

        # Get piece number from board state
        from_piece_num = self.board_state[from_number]
        # Get its character representation (for logic like 'pawn', 'king')
        # This remains necessary for pawn/king logic checks
        from_piece_char = NUM_TO_CHAR[from_piece_num].lower()

        to_piece_num = self.board_state[to_number]

        # Half-move clock reset check
        if to_piece_num != EMPTY:
            self.move_counter = 0

        # 1. Move the piece (Uses numerical codes: from_piece_num, EMPTY)
        self.mutate_board(to_number, from_piece_num)
        self.mutate_board(from_number, EMPTY)

        set_en_passant = False

        if from_piece_char == 'p':
            self.move_counter = 0
            set_en_passant = abs(from_number - to_number) == 20
            en_passant_offset = -1 if is_white else 1
            
            if set_en_passant:
                # Set en passant target square
                self.en_passant = uci_coordinate[0:1] + str(int(uci_coordinate[3:4]) + en_passant_offset)
                self.en_passant_file_index = ord(uci_coordinate[0]) - ord('a')
            
            elif uci_coordinate[2:4] == self.en_passant:
                # En Passant Capture: Remove the captured pawn.
                # *** FIX 1: Pass numerical EMPTY instead of '-' ***
                self.mutate_board(to_number - 10 * en_passant_offset, EMPTY)
                
            elif len(uci_coordinate) > 4:
                # Promotion: Get the numerical code for the promoted piece.
                promote_char = uci_coordinate[4:5]
                # *** FIX 2: Use CHAR_TO_NUM to get the correct numerical code ***
                promote_num = CHAR_TO_NUM[promote_char.upper() if is_white else promote_char]
                self.mutate_board(to_number, promote_num)
                
        elif from_piece_char == 'k':
            # King position update
            if is_white:
                self.white_king_position = uci_coordinate[2:4]
            else:
                self.black_king_position = uci_coordinate[2:4]

            # Castling Rook Move
            if abs(to_number - from_number) == 2:
                rook_num = R if is_white else r # Use numerical Rook constants
                
                # 1. Clear the original rook square
                # *** FIX 3: Pass numerical EMPTY instead of '-' ***
                self.mutate_board(to_number + (1 if to_number > from_number else -2), EMPTY)
                
                # 2. Place the rook on its new square
                self.mutate_board(from_number + ((to_number - from_number) // 2), rook_num)

        # Reset en passant target if not set by a double pawn push
        if not set_en_passant:
            self.en_passant = ''
            self.en_passant_file_index = 0

        # Flip the side-to-move Zobrist hash
        self.hash ^= self.ZOBRIST_SIDE

        # Update secondary data fields (using the new numerical methods)
        self.board_string = self.str_board()
        self.piece_count = self.get_piece_count()
        
    def make_move(self, uci_coordinate):
        
        # Making the move will return an altered copy of the current state
        board = self.board_copy()
        
        # Unpack coordinates once for efficiency
        (from_number, to_number) = self.unpack_coordinate(uci_coordinate)
        to_coordinate = uci_coordinate[2:4]
        
        # Calculate score (using the new numerical methods)
        board.rolling_score = self.rolling_score + self.calculate_score(uci_coordinate)

        # --- Zobrist Hash and Castling Right Updates ---
        
        # 1. Check for **Capture of a Rook** (Opponent's Rook is captured)
        # If the destination is a rook's starting square, the opponent loses that castling right.
        
        # White Rooks (White captures Black Rook)
        if to_coordinate == 'a8' and board.black_castling[0]: # Queenside Black Rook
            board.hash ^= board.ZOBRIST_CASTLE[2]
            board.black_castling[0] = False
        elif to_coordinate == 'h8' and board.black_castling[1]: # Kingside Black Rook
            board.hash ^= board.ZOBRIST_CASTLE[3]
            board.black_castling[1] = False
            
        # Black Rooks (Black captures White Rook)
        elif to_coordinate == 'a1' and board.white_castling[0]: # Queenside White Rook
            board.hash ^= board.ZOBRIST_CASTLE[0]
            board.white_castling[0] = False
        elif to_coordinate == 'h1' and board.white_castling[1]: # Kingside White Rook
            board.hash ^= board.ZOBRIST_CASTLE[1]
            board.white_castling[1] = False


        # 2. Check for **Moving the King or Rook** (Mover loses their own castling rights)
        
        # Moving White King or moving to/from a white rook's square
        if 'e1' in uci_coordinate:
            # remove white castling rights
            for i, right in enumerate(board.white_castling):
                if right:
                    board.hash ^= board.ZOBRIST_CASTLE[i]  # XOR out previous right
            board.white_castling = [False, False]
        elif 'a1' in uci_coordinate: # White Queenside Rook moves
            if board.white_castling[0]:
                board.hash ^= board.ZOBRIST_CASTLE[0]
                board.white_castling[0] = False
        elif 'h1' in uci_coordinate: # White Kingside Rook moves
            if board.white_castling[1]:
                board.hash ^= board.ZOBRIST_CASTLE[1]
                board.white_castling[1] = False

        # Moving Black King or moving to/from a black rook's square
        if 'e8' in uci_coordinate:
            for i, right in enumerate(board.black_castling):
                if right:
                    board.hash ^= board.ZOBRIST_CASTLE[i + 2]
            board.black_castling = [False, False]
        elif 'a8' in uci_coordinate: # Black Queenside Rook moves
            if board.black_castling[0]:
                # NOTE: The original code used index 2 for a8. Let's assume indices are: 
                # [W_Q, W_K, B_Q, B_K] -> [0, 1, 2, 3]
                board.hash ^= board.ZOBRIST_CASTLE[2] 
                board.black_castling[0] = False
        elif 'h8' in uci_coordinate: # Black Kingside Rook moves
            if board.black_castling[1]:
                # NOTE: The original code used index 3 for h8.
                board.hash ^= board.ZOBRIST_CASTLE[3]
                board.black_castling[1] = False
                
        # --- Apply the Move ---
        board.apply_move(uci_coordinate)

        board.played_move_count += 1
        # Flip the sign of the score, as it's now the opponent's turn
        board.rolling_score = -board.rolling_score 

        # *** NUMERICAL UPDATE: Use Zobrist Hash for repetition check ***
        # This is much faster than string/board array comparison for transposition tables.
        board.repetitions.append(board.hash)

        return board

    def nullmove(self):
        # allows for a quick way to let other side move
        # making the move will return an altered copy of the current state
        # this allows us to avoid "undoing" the move
        board = self.board_copy()
        board.played_move_count += 1
        board.rolling_score = -self.rolling_score

        return board

    def board_copy(self):
        # copy the board, does not copy the score
        board = Board()
        board.played_move_count = self.played_move_count
        board.white_king_position = self.white_king_position
        board.black_king_position = self.black_king_position
        board.board_string = self.board_string
        board.piece_count = self.piece_count
        board.en_passant = self.en_passant
        board.move_counter = self.move_counter
        board.board_state = self.board_state[:]
        board.repetitions = self.repetitions.copy()
        board.white_castling = self.white_castling.copy()
        board.black_castling = self.black_castling.copy()
        board.hash = self.hash
        board.ZOBRIST = self.ZOBRIST
        board.ZOBRIST_CASTLE = self.ZOBRIST_CASTLE
        board.ZOBRIST_SIDE = self.ZOBRIST_SIDE
        board.ZOBRIST_EP = self.ZOBRIST_EP

        return board

    def get_piece_count(self):
        # Counts the number of pieces on the 8x8 playing area (excluding empty and off-board squares).
        # We assume pieces are represented by numbers 1 through 12.
        
        # OFF_BOARD = 99 and EMPTY = 0.
        count = 0
        # Iterate over the 120-square array
        for piece_num in self.board_state:
            # Check if the number represents an actual piece (1-12)
            if piece_num != EMPTY and piece_num != OFF_BOARD:
                count += 1
                
        # NOTE: If you are only interested in the 64 squares, you could slice the list 
        # based on the 0x88 inner board indices (21-98), but the above method is simpler 
        # and correct given how the board is initialized.
        return count

    def is_endgame(self):
        # Determines if the position is an endgame based on piece count and Queen presence.
        # Requires piece_count to be updated first.
        
        # Ensure piece_count is up-to-date
        self.piece_count = self.get_piece_count() 
        
        # --- Queen Check ---
        # Queen pieces are represented by q (5) and Q (11)
        # Check if either numerical Queen is present in the board state
        has_queen = 5 in self.board_state or 11 in self.board_state
        
        # --- Endgame Logic ---
        # Original logic: piece_count < 14 OR (piece_count < 20 AND no queen)
        
        return self.piece_count < 14 or (self.piece_count < 20 and not has_queen)

    def move_sort(self, uci_coordinate):
        return self.calculate_score(uci_coordinate, True)

    # def print_board(self):
    #     # Prints the 120-square numerical board state, converting numbers back to chars.
        
    #     # Ensure the mapping is accessible (assuming NUM_TO_CHAR is defined globally)
    #     global NUM_TO_CHAR 
        
    #     for i in range(12):
    #         # 1. Slice the numerical list into a 10-element row
    #         numerical_row = self.board_state[i*10:(i+1)*10]
            
    #         # 2. Convert each numerical piece code back to its character string
    #         char_row = [NUM_TO_CHAR[num] for num in numerical_row]
            
    #         # 3. Join and print the row
    #         print(' '.join(char_row))

    def calculate_score(self, uci_coordinate, sorting=False):
        # Access numerical constants for pieces
        global EMPTY, p, k, r, ALLPSQT, NUM_TO_CHAR 
        
        is_white = self.played_move_count % 2 == 0
        l_board_state = self.board_state # This is the list of numerical IDs (1-12, 0, 99)

        (from_number, to_number) = self.unpack_coordinate(uci_coordinate)

        # Calculate PSQT offsets (already correctly numerical)
        offset = 0 if is_white else 119
        to_offset = abs(to_number - offset)
        from_offset = abs(from_number - offset)

        local_score = 0

        # Get piece numbers directly from the board list
        from_piece_num = l_board_state[from_number]
        to_piece_num = l_board_state[to_number] # Captured piece number

        # Get the *base* piece numerical ID (1-6) for PSQT lookup
        # If White (7-12), convert to Black equivalent (1-6)
        from_piece_base_num = from_piece_num if from_piece_num <= 6 else from_piece_num - 6
        to_piece_base_num = to_piece_num if to_piece_num <= 6 else to_piece_num - 6
        
        # We need the character for Pawn/King logic checks, but not for scoring lookups
        from_piece_char = NUM_TO_CHAR[from_piece_num].lower() 
        

        # 1. PSQT score for the moving piece (from -> to)
        # *** FIX 1: Check against EMPTY and use numerical PSQT key ***
        if from_piece_num != EMPTY:
            local_score += ALLPSQT[from_piece_base_num][to_offset] - \
                           ALLPSQT[from_piece_base_num][from_offset]

        # 2. PSQT score for the captured piece (Value added to score)
        # *** FIX 2: Check against EMPTY and use numerical PSQT key ***
        if to_piece_num != EMPTY:
            local_score += ALLPSQT[to_piece_base_num][to_offset]

        # 3. Special Move Handling (Pawn and King)

        # Pawn Moves
        # *** FIX 3: Use numerical constant p=1 for base type check ***
        if from_piece_base_num == p:
            
            # En Passant Capture
            if uci_coordinate[2:4] == self.en_passant:
                # Add score for the captured pawn (base piece p=1)
                local_score += ALLPSQT[p][to_offset] 
                
            # Promotion
            elif len(uci_coordinate) > 4:
                # Get the promoted piece's base numerical ID (e.g., q=5)
                promote_char = uci_coordinate[4:5].lower()
                promote_base_num = CHAR_TO_NUM[promote_char]
                
                # Adjust value: Add promoted piece value, subtract original pawn value
                local_score += ALLPSQT[promote_base_num][to_offset] - \
                               ALLPSQT[p][to_offset]

            # Pawn Features (Assumes passer_pawn and stacked_pawn are updated)
            if self.passer_pawn(from_number):
                local_score += 10
            if self.stacked_pawn(from_number):
                local_score -= 15
                
        # King Castling
        # *** FIX 4: Use numerical constant k=6 for base type check ***
        elif from_piece_base_num == k:
            if abs(to_number - from_number) == 2:
                # Rook PSQT adjustment for castling (base piece r=4)
                if to_number > from_number: # Kingside
                    # *** FIX 5: Use numerical r=4 for PSQT lookup ***
                    local_score += ALLPSQT[r][to_offset - 1] - ALLPSQT[r][to_offset + 1]
                else: # Queenside
                    # *** FIX 5: Use numerical r=4 for PSQT lookup ***
                    local_score += ALLPSQT[r][to_offset + 1] - ALLPSQT[r][to_offset - 2]

                if sorting:
                    local_score += 60

        return local_score

    def passer_pawn(self, board_position):
        is_white_to_move = self.played_move_count % 2 == 0
        
        # p_offset: The numerical change to advance one rank on the 120-board
        # White (P) advances to lower index numbers (e.g., 81 -> 71), so -10
        # Black (p) advances to higher index numbers (e.g., 31 -> 41), so +10
        p_offset = -10 if is_white_to_move else 10
        
        # Define the numerical range of the OPPONENT'S pieces
        # We are checking for *any* opponent piece, not just pawns, that blocks the rank.
        if is_white_to_move:
            # White pawn is moving: opponent is Black (p, n, b, r, q, k)
            opponent_min, opponent_max = p, k  # 1 through 6
            # The piece we are looking for is an *opponent's* piece.
        else:
            # Black pawn is moving: opponent is White (P, N, B, R, Q, K)
            opponent_min, opponent_max = P, K  # 7 through 12
        
        # Start checking the rank ahead, on the same file and adjacent files
        start_positions = [
            board_position + p_offset,      # same file
            board_position + p_offset - 1,  # left file
            board_position + p_offset + 1   # right file
        ]

        # Loop until we hit the opponent's back rank or off-board squares
        # The condition (20 <= pos <= 99) checks if the position is on the 8x8 inner board
        while all(20 <= pos <= 99 for pos in start_positions):
            for pos in start_positions:
                piece_num = self.board_state[pos]
                
                # Check if an opponent's piece is on the path (Blocking piece check)
                # The piece must be on the board (not EMPTY or OFF_BOARD)
                if piece_num != EMPTY and (opponent_min <= piece_num <= opponent_max):
                    # For passed pawn, we only care if an OPPONENT's pawn blocks the file or adjacent files
                    # If this is any other piece, it's not a passed pawn.
                    
                    # CRITICAL: A passed pawn is defined by the *absence* of opposing **pawns**
                    # on its file or adjacent files. We must refine the check to only look for pawns.
                    
                    # If it's a pawn: Black Pawn (p=1), White Pawn (P=7)
                    if piece_num == p or piece_num == P:
                         return False # Blocked by an opponent's pawn

            # Advance the checking positions to the next rank
            start_positions = [pos + p_offset for pos in start_positions]

        # If the loop finishes without finding an opposing pawn, it is a passer.
        return True

    def stacked_pawn(self, board_position):
        is_white = self.played_move_count % 2 == 0
        p_piece = 'P' if is_white else 'p'
        p_offset = -10 if is_white else 10

        pos = board_position + p_offset
        while 20 <= pos <= 100:
            if self.board_state[pos] == p_piece:
                return True
            pos += p_offset
        return False

    def str_board(self):
        # Converts the numerical board state (list of ints) back to a string 
        # and appends the side-to-move indicator.
        global NUM_TO_CHAR # Access the global mapping
        
        # 1. Convert the numerical list (self.board_state) to a list of characters/strings
        char_list = [NUM_TO_CHAR[piece_num] for piece_num in self.board_state]
        
        # 2. Join the list of characters into a single string
        board_str = "".join(char_list)
        
        # 3. Concatenate the side-to-move indicator (which is already a string)
        # Note: Your original code appended the side-to-move as '0' or '1'
        return board_str + str(self.played_move_count % 2)

    def generate_valid_captures(self):
        return self.generate_valid_moves(True)

    def generate_valid_moves(self, captures_only=False):
        # Return list of valid (maybe illegal) moves
        
        is_white_to_move = self.played_move_count % 2 == 0
        
        # Define the numerical ranges for the current player's pieces (movers)
        # and the opponent's pieces (targets).
        if is_white_to_move:
            # White is moving: pieces are (7-12)
            player_piece_min, player_piece_max = P, K
            # Opponent is Black: pieces are (1-6)
            opponent_piece_min, opponent_piece_max = p, k
            # Pawn offsets remain -1 for the 10-based system (up)
            pawn_offset_multiplier = -1 
            # Pawn starting rank (Row 80)
            pawn_start_row_min = 81
            pawn_start_row_max = 89
        else:
            # Black is moving: pieces are (1-6)
            player_piece_min, player_piece_max = p, k
            # Opponent is White: pieces are (7-12)
            opponent_piece_min, opponent_piece_max = P, K
            # Pawn offsets remain 1 for the 10-based system (up)
            pawn_offset_multiplier = 1
            # Pawn starting rank (Row 30)
            pawn_start_row_min = 31
            pawn_start_row_max = 39

        for board_position, piece_num in enumerate(self.board_state):
            # *** Numerical Check for Player's Pieces ***
            if not (player_piece_min <= piece_num <= player_piece_max):
                continue # Skip if empty, off-board, or opponent's piece

            start_coordinate = self.position_to_coordinate(board_position)
            
            # Determine the base piece type (1-6) for move lookup
            piece_base_num = piece_num if piece_num <= 6 else piece_num - 6
            
            # The piece character is only needed for King/Pawn special logic
            piece_char = NUM_TO_CHAR[piece_num].lower()
            
            # --- Castling and Pawn Double-Step Logic (Simplified for clarity) ---
            # Castling logic must be updated to use numerical checks on self.board_state
            if not captures_only:
                # White Castling
                if piece_num == K and self.white_king_position == 'e1':
                    # Kingside
                    if self.white_castling[0] and self.board_state[96] == EMPTY and \
                       self.board_state[97] == EMPTY and self.board_state[98] == R and \
                        not any(self.attack_position(is_white_to_move, coordinate) for coordinate in ['e1', 'f1', 'g1']):
                        # (Attack position checks omitted for brevity but should also use numerical logic)
                        yield start_coordinate + 'g1'
                    # Queenside
                    if self.white_castling[1] and self.board_state[91] == R and \
                       self.board_state[92] == EMPTY and self.board_state[93] == EMPTY and self.board_state[94] == EMPTY and \
                        not any(self.attack_position(is_white_to_move, coordinate) for coordinate in ['e1', 'd1', 'c1']):
                        # (Attack position checks omitted for brevity but should also use numerical logic)
                        yield start_coordinate + 'c1'
                
                if piece_num == k and self.black_king_position == 'e8':
                    # Kingside
                    if self.black_castling[0] and self.board_state[26] == EMPTY and \
                       self.board_state[27] == EMPTY and self.board_state[28] == r and \
                        not any(self.attack_position(is_white_to_move, coordinate) for coordinate in ['e8', 'f8', 'g8']):
                        # (Attack position checks omitted for brevity but should also use numerical logic)
                        yield start_coordinate + 'g8'
                    # Queenside
                    if self.black_castling[1] and self.board_state[21] == r and \
                       self.board_state[22] == EMPTY and self.board_state[23] == EMPTY and self.board_state[24] == EMPTY and \
                        not any(self.attack_position(is_white_to_move, coordinate) for coordinate in ['e8', 'd8', 'c8']):
                        # (Attack position checks omitted for brevity but should also use numerical logic)
                        yield start_coordinate + 'c8'
                
                # Pawn Double Push
                if piece_base_num == p and pawn_start_row_min <= board_position <= pawn_start_row_max:
                    # Check the square immediately ahead
                    one_step = board_position + pawn_offset_multiplier * 10
                    # Check the square two steps ahead
                    two_step = board_position + pawn_offset_multiplier * 20
                    
                    if self.board_state[one_step] == EMPTY and self.board_state[two_step] == EMPTY:
                        yield start_coordinate + self.position_to_coordinate(two_step)

            # --- General Move Generation Loop ---
            for file_offset, rank_offset in self.get_moves(piece_char):
                # Calculate the rank offset correctly for the 10-based board
                to_position = board_position + file_offset + (rank_offset * pawn_offset_multiplier) 

                while True:
                    eval_piece_num = self.board_state[to_position]

                    # *** Boundary Check ***
                    if eval_piece_num == OFF_BOARD:
                        break # Hit the off-board sentinel

                    # Check if the destination is a valid target based on captures_only flag
                    is_opponent_piece = opponent_piece_min <= eval_piece_num <= opponent_piece_max
                    is_empty_square = eval_piece_num == EMPTY
                    
                    # If captures_only, we must capture an opponent's piece
                    if captures_only and not is_opponent_piece:
                        if not (piece_base_num == p and to_position == self.coordinate_to_position(self.en_passant)):
                           break # Stop if not a capture (unless it's a special pawn move)
                    
                    dest = self.position_to_coordinate(to_position)
                    
                    # --- Pawn Moves ---
                    if piece_base_num == p:
                        is_promotion_rank = to_position in range(21, 29) or to_position in range(91, 99)
                        
                        if is_empty_square and file_offset == 0: # Forward move
                            if is_promotion_rank: # Check promotion rank
                                for prom in ['q', 'r', 'b', 'n']:
                                    yield start_coordinate + dest + prom
                            else:
                                yield start_coordinate + dest
                            
                        elif is_opponent_piece and file_offset != 0: # Diagonal capture
                            if is_promotion_rank: # <--- ADD THIS CHECK
                                for prom in ['q', 'r', 'b', 'n']:
                                    yield start_coordinate + dest + prom
                            else: # <--- ADD THIS ELSE BLOCK
                                yield start_coordinate + dest
                            
                        elif dest == self.en_passant: # En Passant capture
                            yield start_coordinate + dest
                        else:
                            break # Blocked or illegal pawn move
                    
                    # --- All Other Pieces ---
                    else:
                        if is_empty_square or is_opponent_piece:
                             yield start_coordinate + dest
                    
                    # If a capture occurred or a non-slider piece moved, stop
                    if not is_empty_square or piece_base_num in (n, k) or piece_base_num == p:
                        break
                    
                    # Continue for sliders (r, b, q)
                    to_position = to_position + file_offset + (rank_offset * pawn_offset_multiplier)

    def in_check(self, is_white):
        king_position = self.white_king_position if is_white else self.black_king_position

        return self.attack_position(is_white, king_position)

    def attack_position(self, is_white_king_side, coordinate):
        
        # Determine the numerical range of the attackers (opponent)
        if is_white_king_side:
            # King is White: Attackers are Black pieces (1-6)
            attacker_min, attacker_max = p, k
            pawn_offset_multiplier = 1 # Black pawn moves 'up' the board (positive index change)
        else:
            # King is Black: Attackers are White pieces (7-12)
            attacker_min, attacker_max = P, K
            pawn_offset_multiplier = -1 # White pawn moves 'up' the board (negative index change)

        attack_position = self.coordinate_to_position(coordinate)

        for board_position, piece_num in enumerate(self.board_state):
            
            # *** Numerical Check for Attacking Pieces (Opponent's Pieces) ***
            if not (attacker_min <= piece_num <= attacker_max):
                continue # Skip if empty, off-board, or own piece

            # Get the base piece type (1-6) for move generation
            piece_base_num = piece_num if piece_num <= 6 else piece_num - 6
            piece_char = NUM_TO_CHAR[piece_num].lower() # For get_moves lookup
            
            # --- Special Pawn Attack Check (fast path) ---
            if piece_base_num == p:
                # Pawns only attack diagonally one square
                attack_offsets = [pawn_offset_multiplier * 10 - 1, pawn_offset_multiplier * 10 + 1]
                for offset in attack_offsets:
                    if board_position + offset == attack_position:
                        return True
                continue # Pawns are done

            # --- General Move Generation Check ---
            for file_offset, rank_offset in self.get_moves(piece_char):
                
                # Calculate the 120-square offset for the direction
                offset = file_offset + (rank_offset * pawn_offset_multiplier) 
                to_position = board_position + offset

                while self.board_state[to_position] != OFF_BOARD:
                    
                    if to_position == attack_position:
                        return True

                    # If the square is blocked by *any* piece, break (unless it's a non-slider)
                    if self.board_state[to_position] != EMPTY:
                        break 
                        
                    # Break after first check for non-sliders (K, N)
                    if piece_base_num in (k, n):
                        break

                    # Continue for sliders
                    to_position += offset

        return False