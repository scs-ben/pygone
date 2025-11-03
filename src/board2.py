import random

KNIGHT_ATTACKS = [0] * 64
KING_ATTACKS = [0] * 64
WHITE_PAWN_ATTACKS = [0] * 64
BLACK_PAWN_ATTACKS = [0] * 64

for sq in range(64):
    r, f = divmod(sq, 8)

    # Knight attacks
    for dr, df in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
        tr, tf = r+dr, f+df
        if 0 <= tr < 8 and 0 <= tf < 8:
            KNIGHT_ATTACKS[sq] |= 1 << (tr*8 + tf)

    # King attacks
    for dr in [-1,0,1]:
        for df in [-1,0,1]:
            if dr==0 and df==0: continue
            tr, tf = r+dr, f+df
            if 0 <= tr < 8 and 0 <= tf < 8:
                KING_ATTACKS[sq] |= 1 << (tr*8 + tf)

    # Pawn attacks
    for df in [-1,1]:
        if 0 <= f+df < 8:
            if r+1 < 8: WHITE_PAWN_ATTACKS[sq] |= 1 << ((r+1)*8 + f+df)
            if r-1 >= 0: BLACK_PAWN_ATTACKS[sq] |= 1 << ((r-1)*8 + f+df)

class Zobrist:
    PIECE_KEYS = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
    CASTLING_KEYS = [random.getrandbits(64) for _ in range(4)]  # KQkq
    EP_KEYS = [random.getrandbits(64) for _ in range(8)]        # files a-h
    SIDE_TO_MOVE = random.getrandbits(64)

    PIECE_INDEX = {
        'white_pawns': 0,
        'white_knights': 1,
        'white_bishops': 2,
        'white_rooks': 3,
        'white_queens': 4,
        'white_kings': 5,
        'black_pawns': 6,
        'black_knights': 7,
        'black_bishops': 8,
        'black_rooks': 9,
        'black_queens': 10,
        'black_kings': 11
    }

class Move:
    __slots__ = ('from_sq', 'to_sq', 'promo', 'capture', 'piece', 'white_to_move')
    
    def __init__(self, from_sq=0, to_sq=0, promo=None, capture=None, piece=None, white_to_move=True):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.promo = promo
        self.capture = capture
        self.piece = piece
        self.white_to_move = white_to_move

class Board:
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    SQUARES = {f"{file}{rank}": 8*(int(rank)-1)+ord(file)-ord('a') 
               for rank in '12345678' for file in 'abcdefgh'}
    
    INDEX_TO_SQUARE = {idx: sq for sq, idx in SQUARES.items()}
    
    BLACK_SQUARES = {sq: (7 - (ord(sq[1]) - ord('1'))) * 8 + (7 - (ord(sq[0]) - ord('a')))
                 for sq in [f"{f}{r}" for r in '12345678' for f in 'abcdefgh']}
    
    BLACK_INDEX_TO_SQUARE = {idx: sq for sq, idx in BLACK_SQUARES.items()}
    
    PIECE_VALUES = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 27000
    }
    
    PIECE_MAP = {'q': 'queen', 'r': 'rook', 'b': 'bishop', 'n': 'knight', 'p': 'pawn', 'k': 'king'}
    
    RANK_8 = 0xFF00000000000000
    RANK_2 = 0x000000000000FF00
    
    WHITE_KING_START = 4
    WHITE_ROOK_KINGSIDE = 7
    WHITE_ROOK_QUEENSIDE = 0
    BLACK_KING_START = 60
    BLACK_ROOK_KINGSIDE = 63
    BLACK_ROOK_QUEENSIDE = 56
    
    KNIGHT_OFFSETS = [-17, -15, -10, -6, 6, 10, 15, 17]
    KING_OFFSETS = [-9, -8, -7, -1, 1, 7, 8, 9]
    BISHOP_OFFSETS = [-9, -7, 7, 9]
    ROOK_OFFSETS = [-8, -1, 1, 8]
    QUEEN_OFFSETS = BISHOP_OFFSETS + ROOK_OFFSETS
    
    def __init__(self):
        # White pieces are always "on bottom"
        self.white_pawns   = 0x000000000000FF00
        self.white_knights = 0x0000000000000042
        self.white_bishops = 0x0000000000000024
        self.white_rooks   = 0x0000000000000081
        self.white_queens   = 0x0000000000000008
        self.white_kings    = 0x0000000000000010

        self.black_pawns   = 0x00FF000000000000
        self.black_knights = 0x4200000000000000
        self.black_bishops = 0x2400000000000000
        self.black_rooks   = 0x8100000000000000
        self.black_queens   = 0x0800000000000000
        self.black_kings    = 0x1000000000000000

        # Indexes: [white_kingside, white_queenside, black_kingside, black_queenside]
        self.castling_rights = [True, True, True, True]

        self.en_passant_square = None

        self.white_to_move = True
        self.plies_played = 0
        self.moves_played = 0
        self.halfmove_clock = 0
        self.init_hash()
        self.history = []

    def set_fen(self, fen=None):
        """Set the board position from a FEN string. Defaults to starting position."""
        fen = fen or self.START_FEN
        parts = fen.split()
        placement = parts[0]
        side = parts[1]
        castling = parts[2]
        ep = parts[3]

        # Reset all bitboards
        self.white_pawns   = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks   = 0
        self.white_queens  = 0
        self.white_kings   = 0
        self.black_pawns   = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks   = 0
        self.black_queens  = 0
        self.black_kings   = 0

        # Map piece chars to bitboards
        piece_map = {
            'P': 'white_pawns',   'N': 'white_knights', 'B': 'white_bishops',
            'R': 'white_rooks',   'Q': 'white_queens',  'K': 'white_kings',
            'p': 'black_pawns',   'n': 'black_knights', 'b': 'black_bishops',
            'r': 'black_rooks',   'q': 'black_queens',  'k': 'black_kings'
        }

        rank_idx = 7
        for row in placement.split('/'):
            file_idx = 0
            for ch in row:
                if ch.isdigit():
                    file_idx += int(ch)
                else:
                    sq = rank_idx * 8 + file_idx
                    setattr(self, piece_map[ch], getattr(self, piece_map[ch]) | (1 << sq))
                    file_idx += 1
            rank_idx -= 1

        # Side to move
        self.white_to_move = (side == 'w')

        # Castling rights
        self.castling_rights = [
            'K' in castling,  # White kingside
            'Q' in castling,  # White queenside
            'k' in castling,  # Black kingside
            'q' in castling   # Black queenside
        ]

        # En passant square
        self.en_passant_square = None if ep == '-' else self.SQUARES[ep]


        # Reset move counters
        self.plies_played = 0
        self.moves_played = 0
        self.halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
        
        if not self.white_to_move:
            self.rotate()

    def move_to_uci(self, move):
        if move.white_to_move:
            return self.INDEX_TO_SQUARE[move.from_sq] + self.INDEX_TO_SQUARE[move.to_sq] + (move.promo or '')
        else:
            return self.BLACK_INDEX_TO_SQUARE[move.from_sq] + self.BLACK_INDEX_TO_SQUARE[move.to_sq] + (move.promo or '')

    def move_tuple(self, move):
        self.move(move.from_sq, move.to_sq, move.promo)

    def uci_move(self, uci):
        """Apply a move in UCI format (e2e4, g7g8q)"""
        if self.white_to_move:
            from_sq = self.SQUARES[uci[:2]]
            to_sq = self.SQUARES[uci[2:4]] 
        else:
            from_sq = self.BLACK_SQUARES[uci[:2]]
            to_sq = self.BLACK_SQUARES[uci[2:4]]
            
        promo = uci[4] if len(uci) == 5 else None
        
        self.move(from_sq, to_sq, promo)

    def move(self, from_sq, to_sq, promo):
        """Apply a move with incremental hash update."""
        # Save current state for undo
        self.push()
        self.halfmove_clock += 1

        # Determine which piece is moving (white always on bottom)
        for name in 'pawn knight bishop rook queen king'.split():
            bb_name = "".join(["white_",name,"s"])
            
            bb = getattr(self, bb_name)
            if bb & (1 << from_sq):
                # Incrementally update hash: remove piece from from_sq
                self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[bb_name]][from_sq]

                # Move the piece
                bb ^= (1 << from_sq) | (1 << to_sq)
                setattr(self, bb_name, bb)

                # Update hash for to_sq
                if promo:
                    # Remove pawn hash for to_sq (already XORed in move above)
                    setattr(self, bb_name, getattr(self, bb_name) & ~(1 << to_sq))
                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[bb_name]][to_sq]

                    # Add promoted piece hash
                    bb_name_promo = "".join(["white_",self.PIECE_MAP[promo],"s"])
                    promoted_bb = getattr(self, bb_name_promo)
                    promoted_bb |= (1 << to_sq)
                    setattr(self, bb_name_promo, promoted_bb)
                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[bb_name_promo]][to_sq]
                else:
                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[bb_name]][to_sq]

                break            

        # Handle capture
        for name, idx in [('pawn', 6), ('knight', 7), ('bishop', 8),
                        ('rook', 9), ('queen', 10), ('king', 11)]:
            bb_name = "".join(["black_",name,"s"])
            bb = getattr(self, bb_name)
            if bb & (1 << to_sq):
                # Remove captured piece from hash and bitboard
                self.hash ^= Zobrist.PIECE_KEYS[idx][to_sq]
                setattr(self, bb_name, bb & ~(1 << to_sq))
                self.halfmove_clock = 0
                break

        # Handle castling rights
        old_rights = self.castling_rights.copy()
        if from_sq == self.WHITE_KING_START:
            self.castling_rights[0] = False
            self.castling_rights[1] = False
        elif from_sq == self.WHITE_ROOK_KINGSIDE:
            self.castling_rights[0] = False
        elif from_sq == self.WHITE_ROOK_QUEENSIDE:
            self.castling_rights[1] = False
        if to_sq == self.BLACK_ROOK_KINGSIDE:
            self.castling_rights[2] = False
        elif to_sq == self.BLACK_ROOK_QUEENSIDE:
            self.castling_rights[3] = False

        # Update hash for castling rights changes
        for i in range(4):
            if old_rights[i] != self.castling_rights[i]:
                self.hash ^= Zobrist.CASTLING_KEYS[i]

        # En-passant
        if self.en_passant_square is not None:
            self.hash ^= Zobrist.EP_KEYS[self.en_passant_square % 8]
        
        # Set new en-passant square for double pawn push
        from_rank = from_sq // 8
        to_rank = to_sq // 8
        if (1 << from_sq) & self.RANK_2 and to_rank - from_rank == 2:
            self.en_passant_square = from_sq + 8
        else:
            self.en_passant_square = None
            
        # En-passant
        if self.en_passant_square is not None:
            self.hash ^= Zobrist.EP_KEYS[self.en_passant_square % 8]

        # Side to move
        self.hash ^= Zobrist.SIDE_TO_MOVE

        # Update plies and moves
        self.plies_played += 1
        if not self.white_to_move:
            self.moves_played += 1

        # Toggle side to move
        self.white_to_move = not self.white_to_move

        # Rotate board
        self.rotate()

    def nullmove(self):
        self.push()
        self.halfmove_clock += 1
        
        # Side to move
        self.hash ^= Zobrist.SIDE_TO_MOVE

        # Update plies and moves
        self.plies_played += 1
        if not self.white_to_move:
            self.moves_played += 1

        # Toggle side to move
        self.white_to_move = not self.white_to_move

        # Rotate board
        self.rotate()

    def push(self):
        """Save board state and hash to history."""
        self.history.append((
            self.white_pawns, self.white_knights, self.white_bishops,
            self.white_rooks, self.white_queens, self.white_kings,
            self.black_pawns, self.black_knights, self.black_bishops,
            self.black_rooks, self.black_queens, self.black_kings,
            self.castling_rights.copy(), self.en_passant_square,
            self.white_to_move, self.plies_played, self.moves_played,
            self.halfmove_clock, self.hash
        ))

    def unmove(self):
        """Undo last move with incremental hash restored."""
        if not self.history:
            return
        (
            self.white_pawns, self.white_knights, self.white_bishops,
            self.white_rooks, self.white_queens, self.white_kings,
            self.black_pawns, self.black_knights, self.black_bishops,
            self.black_rooks, self.black_queens, self.black_kings,
            self.castling_rights, self.en_passant_square,
            self.white_to_move, self.plies_played, self.moves_played,
            self.halfmove_clock, self.hash
        ) = self.history.pop()
        self.castling_rights = self.castling_rights.copy()

    def rotate(self):
        """Rotate all bitboards 180 degrees (flip board for side to move)"""
        def flip(bb):
            # Flip rank-wise and file-wise using bitwise ops
            bb = ((bb >> 1) & 0x5555555555555555) | ((bb & 0x5555555555555555) << 1)
            bb = ((bb >> 2) & 0x3333333333333333) | ((bb & 0x3333333333333333) << 2)
            bb = ((bb >> 4) & 0x0F0F0F0F0F0F0F0F) | ((bb & 0x0F0F0F0F0F0F0F0F) << 4)
            bb = ((bb >> 8) & 0x00FF00FF00FF00FF) | ((bb & 0x00FF00FF00FF00FF) << 8)
            bb = ((bb >> 16) & 0x0000FFFF0000FFFF) | ((bb & 0x0000FFFF0000FFFF) << 16)
            bb = (bb >> 32) | ((bb & 0xFFFFFFFF) << 32)
            return bb

        # Swap white/black and rotate their boards
        self.white_pawns, self.black_pawns = flip(self.black_pawns), flip(self.white_pawns)
        self.white_knights, self.black_knights = flip(self.black_knights), flip(self.white_knights)
        self.white_bishops, self.black_bishops = flip(self.black_bishops), flip(self.white_bishops)
        self.white_rooks, self.black_rooks = flip(self.black_rooks), flip(self.white_rooks)
        self.white_queens, self.black_queens = flip(self.black_queens), flip(self.white_queens)
        self.white_kings, self.black_kings = flip(self.black_kings), flip(self.white_kings)
        
        self.castling_rights = [
            self.castling_rights[2],  # new white_kingside ← old black_kingside
            self.castling_rights[3],  # new white_queenside ← old black_queenside
            self.castling_rights[0],  # new black_kingside ← old white_kingside
            self.castling_rights[1],  # new black_queenside ← old white_queenside
        ]
        
        if self.en_passant_square:
            self.en_passant_square = 63 - self.en_passant_square

    def init_hash(self):
        h = 0
        # Pieces
        for name, idx in Zobrist.PIECE_INDEX.items():
            bb = getattr(self, name)
            while bb:
                sq = (bb & -bb).bit_length() - 1  # get LSB index
                bb &= bb - 1  # clear LSB
                h ^= Zobrist.PIECE_KEYS[idx][sq]

        # Castling rights
        for i, allowed in enumerate(self.castling_rights):
            if allowed:
                h ^= Zobrist.CASTLING_KEYS[i]

        # En-passant
        if self.en_passant_square is not None:
            file = self.en_passant_square % 8
            h ^= Zobrist.EP_KEYS[file]

        # Side to move
        if self.white_to_move:
            h ^= Zobrist.SIDE_TO_MOVE

        self.hash = h

    def all_pieces(self):
       return (self.white_pawns | self.white_knights | self.white_bishops |
                  self.white_rooks | self.white_queens | self.white_kings |
                  self.black_pawns | self.black_knights | self.black_bishops |
                  self.black_rooks | self.black_queens | self.black_kings)
       
    def friendly_pieces(self):
        return (self.white_pawns | self.white_knights | self.white_bishops |
                    self.white_rooks | self.white_queens | self.white_kings)
       
    def enemy_pieces(self):
        return (self.black_pawns | self.black_knights | self.black_bishops |
                    self.black_rooks | self.black_queens | self.black_kings)

    def generate_pseudo_legal_moves(self, active=False):      
        # Sliding pieces
        for piece_type, bb, offsets in [
            ('b', self.white_bishops, self.BISHOP_OFFSETS),
            ('r', self.white_rooks, self.ROOK_OFFSETS),
            ('q', self.white_queens, self.QUEEN_OFFSETS)
        ]:
            yield from self.generate_sliding_moves(bb, offsets, piece_type, active=active)

        # Knights
        yield from self.generate_knight_moves(active=active)

        if not active:
            for move in self.generate_castling_moves():
                yield move

        # King
        yield from self.generate_king_moves(active=active)

        # Pawns
        yield from self.generate_pawn_moves(active=active)

    def generate_pawn_moves(self, active=False):
        """Generate pseudo-legal pawn moves for rotated board."""
        all_pieces = self.all_pieces()
        enemy_pieces = self.enemy_pieces()
        pawns = self.white_pawns
        
        while pawns:
            sq = (pawns & -pawns).bit_length() - 1  # get LSB index
            pawns &= pawns - 1  # clear LSB
            
            # Single push
            to_sq = sq + 8
            if to_sq < 64 and not (all_pieces & (1 << to_sq)):
                # Check promotion
                if (1 << to_sq) & self.RANK_8:
                    for p in 'qrbn':
                        yield Move(sq, to_sq, p, None, 'p', self.white_to_move)
                else:
                    if not active:
                        yield Move(sq, to_sq, None, None, 'p', self.white_to_move)
                # Double push from rank 2
                if (1 << sq) & self.RANK_2:
                    to_sq2 = sq + 16
                    if not (all_pieces & (1 << to_sq2)):
                        if not active:
                            yield Move(sq, to_sq2, None, None, 'p', self.white_to_move)

            # Captures
            for df in [-1, 1]:
                file = sq % 8
                target_file = file + df
                if 0 <= target_file <= 7:
                    capture_sq = sq + 8 + df
                    if capture_sq < 64 and (enemy_pieces & (1 << capture_sq)):
                        # Promotion capture
                        if (1 << capture_sq) & self.RANK_8:
                            for p in 'qrbn':
                                yield Move(sq, capture_sq, p, self.determine_capture(capture_sq), 'p', self.white_to_move)
                        else:
                            yield Move(sq, capture_sq, None, self.determine_capture(capture_sq), 'p', self.white_to_move)
                    elif capture_sq == self.en_passant_square:
                        yield Move(sq, self.en_passant_square, None, self.determine_capture(self.en_passant_square), 'p', self.white_to_move)

    def generate_knight_moves(self, active=False):
        """Generate pseudo-legal knight moves for rotated board."""
        knights = self.white_knights
        all_pieces = self.all_pieces()
        enemy_pieces = self.enemy_pieces()

        while knights:
            sq = (knights & -knights).bit_length() - 1  # get LSB index
            knights &= knights - 1  # clear LSB
            r, f = divmod(sq, 8)
            for offset in self.KNIGHT_OFFSETS:
                to_sq = sq + offset
                if 0 <= to_sq < 64:
                    tr, tf = divmod(to_sq, 8)
                    if abs(tr - r) <= 2 and abs(tf - f) <= 2:
                        if not (all_pieces & (1 << to_sq)):
                            # Empty square — quiet move
                            if not active:
                                yield Move(sq, to_sq, None, None, 'n', self.white_to_move)
                        elif enemy_pieces & (1 << to_sq):
                            # Capture — figure out which piece
                            yield Move(sq, to_sq, None, self.determine_capture(to_sq), 'n', self.white_to_move)

    def generate_sliding_moves(self, piece_bb, directions, piece, active=False):
        """Generate pseudo-legal sliding moves for bishops, rooks, or queens."""
        friendly_pieces = self.friendly_pieces()
        enemy_pieces = self.enemy_pieces()

        while piece_bb:
            sq = (piece_bb & -piece_bb).bit_length() - 1  # get LSB index
            piece_bb &= piece_bb - 1  # clear LSB
            
            r, f = divmod(sq, 8)

            for offset in directions:
                to_sq = sq

                while True:
                    to_sq += offset
                    if not (0 <= to_sq < 64):
                        break

                    tr, tf = divmod(to_sq, 8)

                    # Check wraparound: horizontal or vertical/diagonal
                    dr = tr - r
                    df = tf - f

                    if offset in self.BISHOP_OFFSETS and abs(dr) != abs(df):
                        break  # diagonal wrap
                    if offset in [-1, 1] and dr != 0:
                        break  # horizontal wrap
                    if offset in [-8, 8] and df != 0:
                        break  # vertical wrap

                    # Blocked by friendly piece
                    if friendly_pieces & (1 << to_sq):
                        break

                    # Capture enemy
                    if enemy_pieces & (1 << to_sq):
                        yield Move(sq, to_sq, None, self.determine_capture(to_sq), piece, self.white_to_move)
                        break  # stop sliding after capture

                    if not active:
                        # Quiet move
                        yield Move(sq, to_sq, None, None, piece, self.white_to_move)


    def generate_king_moves(self, active=False):
        """Generate pseudo-legal king moves for rotated board."""
        king = self.white_kings
        all_pieces = self.all_pieces()
        enemy_pieces = self.enemy_pieces()

        while king:
            sq = (king & -king).bit_length() - 1  # get LSB index
            king &= king - 1  # clear LSB
            r, f = divmod(sq, 8)
            for offset in self.KING_OFFSETS:
                to_sq = sq + offset
                if 0 <= to_sq < 64:
                    tr, tf = divmod(to_sq, 8)
                    # Must stay within 1 rank/file for adjacency
                    if abs(tr - r) <= 1 and abs(tf - f) <= 1:
                        if not (all_pieces & (1 << to_sq)):
                            # Empty square → quiet move
                            if not active:
                                yield Move(sq, to_sq, None, None, 'k', self.white_to_move)
                        elif enemy_pieces & (1 << to_sq):
                            # Capture → determine piece type
                            yield Move(sq, to_sq, None, self.determine_capture(to_sq), 'k', self.white_to_move)
    
    def generate_castling_moves(self):
        """Generate white castling moves (assuming we only play as white)."""
        all_pieces = self.all_pieces()

        # e1 = 4, f1 = 5, g1 = 6, d1 = 3, c1 = 2, b1 = 1
        if self.castling_rights[0]:  # white kingside
            kp1 = 4 if self.white_to_move else 3
            kp2 = 5 if self.white_to_move else 2
            kp3 = 6 if self.white_to_move else 1
            # f1, g1 must be empty and not attacked
            if not (all_pieces & ((1 << kp2) | (1 << kp3))):
                if not self.is_square_attacked(kp1, False) and not self.is_square_attacked(kp2, False) and not self.is_square_attacked(kp3, False):
                    yield Move(kp1, kp3, None, None, 'k', self.white_to_move)

        if self.castling_rights[1]:  # white queenside
            kp1 = 4 if self.white_to_move else 3
            kp2 = 3 if self.white_to_move else 4
            kp3 = 2 if self.white_to_move else 5
            kp4 = 1 if self.white_to_move else 6
            
            # d1, c1, b1 must be empty and not attacked
            if not (all_pieces & ((1 << kp2) | (1 << kp3) | (1 << kp4))):
                if not self.is_square_attacked(kp1, False) and not self.is_square_attacked(kp2, False) and not self.is_square_attacked(kp3, False):
                    yield Move(kp1, kp3, None, None, 'k', self.white_to_move)

    def king_square(self, for_white=True):
        """Return the square index of the king for the side to move (ours)."""
        if for_white:
            return self.white_kings.bit_length() - 1  # get index of single 1-bit
        else:
            return self.black_kings.bit_length() - 1  # get index of single 1-bit

    def in_check(self, for_white=True):
        """Return True if the side to move is in check."""
        king_sq = self.king_square(for_white)  # our king
        if king_sq is None:
            return False  # or raise an error if king is missing
        # Check if enemy (after rotation, always black) attacks the square             
        return self.is_square_attacked(king_sq, not for_white)

    def is_square_attacked(self, sq, by_white=True):
        all_pieces = self.all_pieces()

        if by_white:
            pawns = self.white_pawns
            knights = self.white_knights
            bishops = self.white_bishops
            rooks = self.white_rooks
            queens = self.white_queens
            king = self.white_kings
            pawn_attack_table = WHITE_PAWN_ATTACKS
        else:
            pawns = self.black_pawns
            knights = self.black_knights
            bishops = self.black_bishops
            rooks = self.black_rooks
            queens = self.black_queens
            king = self.black_kings
            pawn_attack_table = BLACK_PAWN_ATTACKS

        # Pawn attacks
        if pawns & pawn_attack_table[sq]:
            return True

        # Knight attacks
        if knights & KNIGHT_ATTACKS[sq]:
            return True

        # King attacks
        if king & KING_ATTACKS[sq]:
            return True

        # Sliding pieces
        if by_white:
            for bb, offsets in [(bishops|queens, self.BISHOP_OFFSETS),(rooks|queens, self.ROOK_OFFSETS)]:
                for sqp in range(64):
                    if not (bb & (1 << sqp)):
                        continue
                    r, f = divmod(sqp, 8)
                    for offset in offsets:
                        tr, tf = r, f
                        while True:
                            tr += offset // 8
                            tf += offset % 8
                            if not (0 <= tr < 8 and 0 <= tf < 8):
                                break
                            tsq = tr*8 + tf
                            if tsq == sq:
                                return True  # check detected
                            if all_pieces & (1 << tsq):
                                break  # blocked
        else:
            for bb, offsets in [(bishops|queens, self.BISHOP_OFFSETS), (rooks|queens, self.ROOK_OFFSETS)]:
                for offset in offsets:
                    tsq = sq
                    while True:
                        tr, tf = divmod(tsq, 8)
                        tr += offset // 8
                        tf += offset % 8
                        if not (0 <= tr < 8 and 0 <= tf < 8):
                            break
                        tsq = tr*8 + tf
                        if all_pieces & (1 << tsq):
                            if bb & (1 << tsq):
                                return True
                            break

        return False

    def determine_capture(self, sq):
        for piece, bb in [('p', self.black_pawns),
                        ('n', self.black_knights),
                        ('b', self.black_bishops),
                        ('r', self.black_rooks),
                        ('q', self.black_queens),
                        ('k', self.black_kings)]:
            if bb & (1 << sq):
                return piece
        return None

    def score_move(self, move):
        score = 0
        if move.capture:
            # MVV-LVA: Most valuable victim - least valuable attacker
            score += self.PIECE_VALUES[move.capture] - self.PIECE_VALUES[move.piece] / 10
        if move.promo:
            # Promote to queen highest
            score += self.PIECE_VALUES[move.promo] * 10
        return score
            
    def evaluate(self):
        return (self.evaluate_material() +
                self.evaluate_pawn_structure() +
                self.evaluate_king_safety() +
                self.evaluate_mobility())
            
    def evaluate_material(self):
        score = 0
        for name, value in self.PIECE_VALUES.items():
            score += value * bin(getattr(self, "".join(["white_",self.PIECE_MAP[name],"s"]))).count('1')
            score -= value * bin(getattr(self, "".join(["black_",self.PIECE_MAP[name],"s"]))).count('1')
        return score
            
    def evaluate_pawn_structure(self):
        score = 0
        for file in range(8):
            file_mask = 0x0101010101010101 << file
            white_file = self.white_pawns & file_mask
            black_file = self.black_pawns & file_mask
            
            # Doubled pawns
            if bin(white_file).count('1') > 1:
                score -= 25
            if bin(black_file).count('1') > 1:
                score += 25
            
            # Isolated pawns
            left = file_mask << 1 if file < 7 else 0
            right = file_mask >> 1 if file > 0 else 0
            if white_file and not (self.white_pawns & (left | right)):
                score -= 15
            if black_file and not (self.black_pawns & (left | right)):
                score += 15
        return score
    
    def evaluate_king_safety(self):
        score = 0
        
        # Find king square
        king_sq = self.king_square()
        k_rank, k_file = divmod(king_sq, 8)
        
        # Pawn shield: friendly pawns in front of king
        shield_mask = 0
        if k_rank < 7:
            for df in [-1, 0, 1]:
                f = k_file + df
                if 0 <= f <= 7:
                    shield_mask |= (1 << ((k_rank + 1) * 8 + f))
        pawns_in_shield = bin(self.white_pawns & shield_mask).count('1')
        score += 10 * pawns_in_shield  # each pawn in shield gives small bonus
        
        # Enemy proximity: enemy pieces around king
        prox_mask = 0
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0:
                    continue
                r, f = k_rank + dr, k_file + df
                if 0 <= r < 8 and 0 <= f < 8:
                    prox_mask |= (1 << (r * 8 + f))
        enemy_near = bin(self.black_pawns & prox_mask).count('1')
        enemy_near += bin(self.black_knights & prox_mask).count('1')
        enemy_near += bin(self.black_bishops & prox_mask).count('1')
        enemy_near += bin(self.black_rooks & prox_mask).count('1')
        enemy_near += bin(self.black_queens & prox_mask).count('1')
        score -= 15 * enemy_near  # penalty for enemy pieces close
        
        return score
    
    def evaluate_mobility(self): 
        score = 0 
        
        # Generate moves for all white pieces (pseudo-legal) 
        moves = list(self.generate_pseudo_legal_moves()) 
        score += len(moves) # 1 point per pseudo-legal move 
        
        # Optionally subtract black mobility 
        # Generate moves for black by rotating board 
        self.rotate() 
        self.white_to_move = not self.white_to_move
        moves = list(self.generate_pseudo_legal_moves())
        score -= len(moves) 
        self.rotate() # rotate back
        self.white_to_move = not self.white_to_move
        
        return score

    def print_board(self):
        """Print board in human-readable format (for debugging)"""
        board = ['.'] * 64
        bb_map = [
            (self.white_pawns, 'P'),
            (self.white_knights, 'N'),
            (self.white_bishops, 'B'),
            (self.white_rooks, 'R'),
            (self.white_queens, 'Q'),
            (self.white_kings, 'K'),
            (self.black_pawns, 'p'),
            (self.black_knights, 'n'),
            (self.black_bishops, 'b'),
            (self.black_rooks, 'r'),
            (self.black_queens, 'q'),
            (self.black_kings, 'k')
        ]
        for bb, char in bb_map:
            for i in range(64):
                if bb & (1 << i):
                    board[i] = char
        for rank in range(7, -1, -1):
            print(' '.join(board[rank*8:(rank+1)*8]))
            
        score = self.evaluate()
        print(f"White?: {(self.white_to_move)} Plies: {self.plies_played} Moves: {self.moves_played} Score: {score}")