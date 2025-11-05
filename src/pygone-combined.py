#!/usr/bin/env pypy3
import sys
# === Start of board.py ===
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

N, S, E, W = 0, 1, 2, 3
NE, NW, SE, SW = 4, 5, 6, 7
# Directions (indexing into RAYS)
# Direction constants
RAYS = [{} for _ in range(64)] # RAYS[sq][dir] > bitboard

# Define directions as (dr, df) tuples: (rank_change, file_change)
DIRECTIONS = {
    N: (1, 0), S: (-1, 0), E: (0, 1), W: (0, -1),
    NE: (1, 1), NW: (1, -1), SE: (-1, 1), SW: (-1, -1)
}

def get_ray_mask(r, f, dr, df):
    """Calculates a bitmask for a ray starting at (r, f) and moving by (dr, df)."""
    mask = 0
    rr, ff = r + dr, f + df
    
    # Loop until the coordinates go out of the 8x8 board bounds (0-7)
    while 0 <= rr < 8 and 0 <= ff < 8:
        # Calculate the square index: (rank * 8 + file)
        mask |= 1 << (rr * 8 + ff)
        # Move to the next square in the ray
        rr += dr
        ff += df
    return mask

# --- Main Generation Loop ---

for sq in range(64):
    r, f = divmod(sq, 8)
    
    for direction, (dr, df) in DIRECTIONS.items():
        RAYS[sq][direction] = get_ray_mask(r, f, dr, df)


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
    # START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
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
        'k': 32000
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

        is_pawn = bool(self.white_pawns & (1 << from_sq))
        is_king = bool(self.white_kings & (1 << from_sq))
        
        if is_pawn:
            self.halfmove_clock = 0
            if to_sq == self.en_passant_square and (from_sq == self.en_passant_square - 7 or from_sq == self.en_passant_square - 9):
                    self.black_pawns &= ~(1 << (to_sq - 8))

                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX["black_pawns"]][to_sq - 8]

        # Determine which piece is moving (white always on bottom)
        for name in 'pawn knight bishop rook queen king'.split():
            bb_name = "".join(["white_",name,"s"])

            if is_king and bb_name == "white_kings":
                # Kingside castling
                if abs(to_sq - from_sq) == 2:
                    if to_sq > from_sq: 
                        if from_sq == 4:
                            rook_from = 7
                            rook_to = 5
                        else:
                            rook_from = 7
                            rook_to = 5
                    else: 
                        if from_sq == 4:
                            rook_from = 0
                            rook_to = 3
                        else:
                            rook_from = 0
                            rook_to = 2

                    # Move rook bitboard
                    rook_bb_name = "white_rooks"
                    rook_bb = getattr(self, rook_bb_name)
                    rook_bb ^= (1 << rook_from) | (1 << rook_to)
                    setattr(self, rook_bb_name, rook_bb)

                    # Update Zobrist hash for rook
                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[rook_bb_name]][rook_from]
                    self.hash ^= Zobrist.PIECE_KEYS[Zobrist.PIECE_INDEX[rook_bb_name]][rook_to]
            
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

        if to_sq == self.en_passant_square:
            #handle EP
            self.en_passant_square = self.en_passant_square
        
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
            self.castling_rights[2],  # new white_kingside < old black_kingside
            self.castling_rights[3],  # new white_queenside < old black_queenside
            self.castling_rights[0],  # new black_kingside < old white_kingside
            self.castling_rights[1],  # new black_queenside < old white_queenside
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
        # Bishops
        yield from self.generate_sliding_moves(self.white_bishops, [NE, NW, SE, SW], 'b', active=active)

        # Rooks
        yield from self.generate_sliding_moves(self.white_rooks, [N, S, E, W], 'r', active=active)

        # Queens (all directions)
        yield from self.generate_sliding_moves(self.white_queens, [N, S, E, W, NE, NW, SE, SW], 'q', active=active)

        # Knights
        yield from self.generate_piece_moves(self.white_knights, KNIGHT_ATTACKS, 'n', active=active)

        if not active:
            for move in self.generate_castling_moves():
                yield move

        # King
        yield from self.generate_piece_moves(self.white_kings, KING_ATTACKS, 'k', active=active)

        # Pawns
        yield from self.generate_pawn_moves(active=active)

    def generate_pawn_moves(self, active=False):
        all_pieces = self.all_pieces()
        enemy_pieces = self.enemy_pieces()
        pawns = self.white_pawns

        # single push
        single_push = (pawns << 8) & ~all_pieces
        # promotion
        promo_push = single_push & self.RANK_8
        normal_push = single_push & ~self.RANK_8
        for to_sq in range(64):
            if promo_push & (1 << to_sq):
                from_sq = to_sq - 8
                for p in 'qrbn':
                    yield Move(from_sq, to_sq, p, None, 'p', self.white_to_move)
            elif normal_push & (1 << to_sq):
                from_sq = to_sq - 8
                if not active:
                    yield Move(from_sq, to_sq, None, None, 'p', self.white_to_move)

        # double push
        double_push = ((pawns & self.RANK_2) << 16) & ~all_pieces
        double_push &= ~(all_pieces << 8)  # must be empty in front
        for to_sq in range(64):
            if double_push & (1 << to_sq):
                from_sq = to_sq - 16
                if not active:
                    yield Move(from_sq, to_sq, None, None, 'p', self.white_to_move)

        # captures
        left_attack = ((pawns & ~0x0101010101010101) << 7) & (enemy_pieces | (1 << self.en_passant_square if self.en_passant_square is not None else 0))
        right_attack = ((pawns & ~0x8080808080808080) << 9) & (enemy_pieces | (1 << self.en_passant_square if self.en_passant_square is not None else 0))
        for cap_bb, shift in [(left_attack, 7), (right_attack, 9)]:
            for to_sq in range(64):
                if cap_bb & (1 << to_sq):
                    from_sq = to_sq - shift
                    is_ep = (self.en_passant_square is not None) and (to_sq == self.en_passant_square)
                    capture_piece = None
                    if is_ep:
                        # EP capture: Captured piece is always a pawn, and it is determined by the move type.
                        capture_piece = self.determine_capture(to_sq, is_en_passant=True)
                    elif enemy_pieces & (1 << to_sq):
                        capture_piece = self.determine_capture(to_sq)
                    promo = 'qrbn' if (1 << to_sq) & self.RANK_8 else None
                    if promo:
                        for p in promo:
                            yield Move(from_sq, to_sq, p, capture_piece, 'p', self.white_to_move)
                    else:
                        yield Move(from_sq, to_sq, None, capture_piece, 'p', self.white_to_move)

    def masked_ray(self, sq, d, occupied):
        ray = RAYS[sq][d]
        blockers = ray & occupied
        if blockers:
            first_blocker = (blockers & -blockers).bit_length() - 1 if d in [N, E, NE, NW] else blockers.bit_length() - 1
            ray &= ~(RAYS[first_blocker][d])
        return ray

    def generate_sliding_moves(self, piece_bb, directions, piece, active=False):
        friendly = self.friendly_pieces()
        enemy = self.enemy_pieces()
        occupied = friendly | enemy

        while piece_bb:
            sq = (piece_bb & -piece_bb).bit_length() - 1
            piece_bb &= piece_bb - 1

            for d in directions:
                ray = self.masked_ray(sq, d, occupied)

                # Remove friendly squares
                ray &= ~friendly

                # Yield moves
                while ray:
                    to_sq = (ray & -ray).bit_length() - 1
                    ray &= ray - 1
                    if enemy & (1 << to_sq):
                        yield Move(sq, to_sq, None, self.determine_capture(to_sq), piece, self.white_to_move)
                    else:
                        if not active:
                            yield Move(sq, to_sq, None, None, piece, self.white_to_move)

    def generate_piece_moves(self, piece_bb, attacks_table, piece_char, active=False):
        friendly = self.friendly_pieces()
        enemy = self.enemy_pieces()
        while piece_bb:
            sq = (piece_bb & -piece_bb).bit_length() - 1
            piece_bb &= piece_bb - 1
            for to_sq in range(64):
                if attacks_table[sq] & (1 << to_sq) & ~friendly:
                    capture = self.determine_capture(to_sq) if (enemy & (1 << to_sq)) else None
                    if not active or capture:
                        yield Move(sq, to_sq, None, capture, piece_char, self.white_to_move)
    
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
        """Return the square index of the king for the side to move."""
        king_bb = self.white_kings if for_white else self.black_kings
        # get the index of the single 1-bit (LSB)
        return (king_bb & -king_bb).bit_length() - 1

    def in_check(self, for_white=True):
        """Return True if the side to move is in check."""
        king_sq = self.king_square(for_white)  # our king
        if king_sq is None:
            return False  # or raise an error if king is missing
        # Check if enemy (after rotation, always black) attacks the square  
        return self.is_square_attacked(king_sq, not for_white)

    def is_square_attacked(self, sq, by_white=True):
        # Pawns
        pawns = self.white_pawns if by_white else self.black_pawns
        pawn_attacks = BLACK_PAWN_ATTACKS if by_white else WHITE_PAWN_ATTACKS
        if pawns & pawn_attacks[sq]:
            return True

        # Knights
        knights = self.white_knights if by_white else self.black_knights
        if knights & KNIGHT_ATTACKS[sq]:
            return True

        # King
        king = self.white_kings if by_white else self.black_kings
        if king & KING_ATTACKS[sq]:
            return True

        # Sliding pieces
        sliders = [
            ('bishop', self.white_bishops | self.white_queens if by_white else self.black_bishops | self.black_queens, self.BISHOP_OFFSETS),
            ('rook',   self.white_rooks   | self.white_queens if by_white else self.black_rooks   | self.black_queens, self.ROOK_OFFSETS),
        ]

        all_pieces = self.all_pieces()

        for piece_type, bb, offsets in sliders:
            for from_sq in range(64):
                if not (bb & (1 << from_sq)):
                    continue
                for offset in offsets:
                    to_sq = from_sq
                    while True:
                        to_sq += offset
                        if not (0 <= to_sq < 64):
                            break
                        # check for wrap-around if necessary
                        if piece_type == 'bishop' and abs((to_sq // 8) - (from_sq // 8)) != abs((to_sq % 8) - (from_sq % 8)):
                            break
                        if piece_type == 'rook':
                            # horizontal or vertical wrap
                            dr = (to_sq // 8) - (from_sq // 8)
                            df = (to_sq % 8) - (from_sq % 8)
                            if offset in [-1, 1] and dr != 0:
                                break
                            if offset in [-8, 8] and df != 0:
                                break
                        # blocked
                        if all_pieces & (1 << to_sq):
                            if to_sq == sq:
                                return True
                            break
                        if to_sq == sq:
                            return True
        return False

    def determine_capture(self, to_sq, is_en_passant=False):
        if is_en_passant:
            return 'p' 

        # Non-En Passant Capture: Check enemy piece bitboards directly at to_sq
        sq_mask = 1 << to_sq
        
        if self.black_pawns & sq_mask:
            return 'p'
        if self.black_knights & sq_mask:
            return 'n'
        if self.black_bishops & sq_mask:
            return 'b'
        if self.black_rooks & sq_mask:
            return 'r'
        if self.black_queens & sq_mask:
            return 'q'
        if self.black_kings & sq_mask:
            return 'k' # Should only happen after illegal move, but included for completeness

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
     
    def is_endgame(self):
        # A simple endgame definition: low count of major pieces
        white_majors = bin(self.white_rooks).count('1') + bin(self.white_queens).count('1')
        black_majors = bin(self.black_rooks).count('1') + bin(self.black_queens).count('1')
        
        # Check if fewer than 4 Rooks/Queens total
        if white_majors + black_majors < 4:
            return True
        
        # Alternative: Check if all Queens are off the board AND few minors left
        if not self.white_queens and not self.black_queens:
             return True
        
        return False
     
    def evaluate(self):
        return (self.evaluate_material() +
                 self.evaluate_pawn_structure() +
                 self.evaluate_king_position() +
                 self.evaluate_mobility() +
                 self.eval_development() +
                 self.eval_center_control())
            
    def evaluate_material(self):
        score = 0
        for name, value in self.PIECE_VALUES.items():
            score += value * bin(getattr(self, "".join(["white_",self.PIECE_MAP[name],"s"]))).count('1')
            score -= value * bin(getattr(self, "".join(["black_",self.PIECE_MAP[name],"s"]))).count('1')
            
        # print(f"material score {score}")
            
        return score
            
    def evaluate_pawn_structure(self):
        score = 0
        is_endgame = self.is_endgame()
        
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
                
            black_adj_pawns = 0
            if file > 0: black_adj_pawns |= self.black_pawns & (0x0101010101010101 << (file - 1))
            if file < 7: black_adj_pawns |= self.black_pawns & (0x0101010101010101 << (file + 1))
            
            # Black's potential blockers (White pawns on adjacent files)
            white_adj_pawns = 0
            if file > 0: white_adj_pawns |= self.white_pawns & (0x0101010101010101 << (file - 1))
            if file < 7: white_adj_pawns |= self.white_pawns & (0x0101010101010101 << (file + 1))
        
            if white_file and not black_file: # Pawns on file, but no black pawns on the same file
                if not black_adj_pawns:
                    # Further check: are there any black pawns that could move to block?
                    # Since you only check for adjacent files, this is a basic "no immediate blockers" check.
                    
                    if is_endgame:
                        # Find the highest rank of the passed pawn (closest to rank 8)
                        pawn_rank_idx = (white_file.bit_length() - 1) // 8 # 7 for R8, 0 for R1
                        
                        # Scaling: (pawn_rank_idx - 1) gives 6 for R7, 1 for R2.
                        bonus = (pawn_rank_idx - 1) * (pawn_rank_idx - 1) * 3 
                        score += min(bonus, 250)
                        
            # 2. Black Passed Pawn (Check for NO white pawns on same file OR adjacent files IN FRONT)
            if black_file and not white_file:
                if not white_adj_pawns:
                    
                    if is_endgame:
                        # Find the rank of the MOST ADVANCED black pawn (lowest rank index 0-7)
                        most_advanced_rank_idx = 7 
                        for rank_idx in range(8):
                            sq_idx = rank_idx * 8 + file
                            if black_file & (1 << sq_idx):
                                most_advanced_rank_idx = rank_idx
                                break
                                
                        # Scaling: (7 - rank_idx) gives 7 for R1 (index 0), 0 for R8 (index 7).
                        scaling_factor = 7 - most_advanced_rank_idx 
                        
                        penalty = scaling_factor * scaling_factor * 3
                        score -= min(penalty, 250) # DEDUCT THE PENALTY
        
        return score
    
    def eval_development(self):
        score = 0
        white_developed_minors = 0
        black_developed_minors = 0
        
        # White Minor Pieces
        white_start_squares = [1, 6, 2, 5] # b1, g1 (Knights); c1, f1 (Bishops)
        white_pieces = [self.white_knights, self.white_knights, self.white_bishops, self.white_bishops]

        for sq_idx, bitboard in zip(white_start_squares, white_pieces):
            if not bitboard & (1 << sq_idx):
                # Piece has moved from its starting square
                score += 15 # Increased development bonus (e.g., 15 CP)
                white_developed_minors += 1

        # Black Minor Pieces
        black_start_squares = [57, 62, 58, 61] # b8, g8 (Knights); c8, f8 (Bishops)
        black_pieces = [self.black_knights, self.black_knights, self.black_bishops, self.black_bishops]

        for sq_idx, bitboard in zip(black_start_squares, black_pieces):
            if not bitboard & (1 << sq_idx):
                score -= 15 # Increased development penalty for Black's lack of development
                black_developed_minors += 1 # Count for penalty calculation
        
        # --- QUEEN DEVELOPMENT PENALTY ---

        # 1. White Queen Penalty
        white_queen_start_sq = 3 # D1
        if not self.white_queens & (1 << white_queen_start_sq):
            # Queen has moved off D1
            if white_developed_minors < 2:
                # High penalty if Queen moves before at least two minors
                score -= 40
            elif white_developed_minors < 4:
                # Medium penalty if Queen moves before all minors
                score -= 20
        
        # 2. Black Queen Penalty
        black_queen_start_sq = 59 # D8
        if not self.black_queens & (1 << black_queen_start_sq):
            # Queen has moved off D8
            if black_developed_minors < 2:
                score += 40
            elif black_developed_minors < 4:
                score += 20
                
        return score
    
    def eval_center_control(self):
        white_control = 0
        black_control = 0
        
        for sq in (27, 28, 35, 36):
            white_control += self.is_square_attacked(sq, True)
            black_control += self.is_square_attacked(sq, False)

        return 4 * (white_control - black_control)
    
    def evaluate_king_position(self):
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
        
        if not self.is_endgame():
            # Only apply pawn shield and general safety in the middlegame
            return score # Return the middlegame safety score

        score = 0
        for side in (True, False):
            king_sq = self.king_square(side) # Assuming you have a way to find this
            
            # 1. King Centralization (e.g., Manhattan distance from e4/e5)
            k_rank, k_file = divmod(king_sq, 8)
            # Distance from center square (3, 4) for white's perspective
            center_rank, center_file = 3, 4 
            dist = abs(k_rank - center_rank) + abs(k_file - center_file)
            
            # Bonus for lower distance (closer to the center)
            score += (14 - dist) * (5 if side else -5)
            
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

    # def set_fen(self, fen=None):
    #     """Set the board position from a FEN string. Defaults to starting position."""
    #     fen = fen or self.START_FEN
    #     parts = fen.split()
    #     placement = parts[0]
    #     side = parts[1]
    #     castling = parts[2]
    #     ep = parts[3]

    #     # Reset all bitboards
    #     self.white_pawns   = 0
    #     self.white_knights = 0
    #     self.white_bishops = 0
    #     self.white_rooks   = 0
    #     self.white_queens  = 0
    #     self.white_kings   = 0
    #     self.black_pawns   = 0
    #     self.black_knights = 0
    #     self.black_bishops = 0
    #     self.black_rooks   = 0
    #     self.black_queens  = 0
    #     self.black_kings   = 0

    #     # Map piece chars to bitboards
    #     piece_map = {
    #         'P': 'white_pawns',   'N': 'white_knights', 'B': 'white_bishops',
    #         'R': 'white_rooks',   'Q': 'white_queens',  'K': 'white_kings',
    #         'p': 'black_pawns',   'n': 'black_knights', 'b': 'black_bishops',
    #         'r': 'black_rooks',   'q': 'black_queens',  'k': 'black_kings'
    #     }

    #     rank_idx = 7
    #     for row in placement.split('/'):
    #         file_idx = 0
    #         for ch in row:
    #             if ch.isdigit():
    #                 file_idx += int(ch)
    #             else:
    #                 sq = rank_idx * 8 + file_idx
    #                 setattr(self, piece_map[ch], getattr(self, piece_map[ch]) | (1 << sq))
    #                 file_idx += 1
    #         rank_idx -= 1

    #     # Side to move
    #     self.white_to_move = (side == 'w')

    #     # Castling rights
    #     self.castling_rights = [
    #         'K' in castling,  # White kingside
    #         'Q' in castling,  # White queenside
    #         'k' in castling,  # Black kingside
    #         'q' in castling   # Black queenside
    #     ]

    #     # En passant square
    #     self.en_passant_square = None if ep == '-' else self.SQUARES[ep]


    #     # Reset move counters
    #     self.plies_played = 0
    #     self.moves_played = 0
    #     self.halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
        
    #     if not self.white_to_move:
    #         self.rotate()

    # def get_fen(self):
    #     """Return the FEN string representing the current board state."""
        
    #     if not self.white_to_move:
    #         self.rotate()
        
    #     # Reverse mapping of bitboards to piece characters
    #     bitboard_map = {
    #         'white_pawns': 'P',   'white_knights': 'N', 'white_bishops': 'B',
    #         'white_rooks': 'R',   'white_queens': 'Q',  'white_kings': 'K',
    #         'black_pawns': 'p',   'black_knights': 'n', 'black_bishops': 'b',
    #         'black_rooks': 'r',   'black_queens': 'q',  'black_kings': 'k'
    #     }

    #     rows = []
    #     for rank in range(7, -1, -1):  # rank 8 to 1
    #         row = ''
    #         empty = 0
    #         for file in range(8):  # file a to h
    #             sq = rank * 8 + file
    #             piece_found = False
    #             for bb_attr, piece_char in bitboard_map.items():
    #                 if getattr(self, bb_attr) & (1 << sq):
    #                     if empty > 0:
    #                         row += str(empty)
    #                         empty = 0
    #                     row += piece_char
    #                     piece_found = True
    #                     break
    #             if not piece_found:
    #                 empty += 1
    #         if empty > 0:
    #             row += str(empty)
    #         rows.append(row)
        
    #     placement = '/'.join(rows)

    #     # Side to move
    #     side = 'w' if self.white_to_move else 'b'

    #     # Castling rights
    #     castling = ''
    #     castling += 'K' if self.castling_rights[0] else ''
    #     castling += 'Q' if self.castling_rights[1] else ''
    #     castling += 'k' if self.castling_rights[2] else ''
    #     castling += 'q' if self.castling_rights[3] else ''
    #     if castling == '':
    #         castling = '-'

    #     # En passant square
    #     ep = '-' if self.en_passant_square is None else self.INDEX_TO_SQUARE[self.en_passant_square]

    #     # Halfmove clock
    #     halfmove = str(self.halfmove_clock)

    #     # Fullmove number
    #     fullmove = str((self.plies_played // 2) + 1)

    #     if not self.white_to_move:
    #         self.rotate()

    #     return f"{placement} {side} {castling} {ep} {halfmove} {fullmove}"

    # def print_board(self):
    #     """Print board in human-readable format (for debugging)"""
    #     board = ['.'] * 64
    #     if not self.white_to_move:
    #         self.rotate()
            
    #     bb_map = [
    #         (self.white_pawns, 'P'),
    #         (self.white_knights, 'N'),
    #         (self.white_bishops, 'B'),
    #         (self.white_rooks, 'R'),
    #         (self.white_queens, 'Q'),
    #         (self.white_kings, 'K'),
    #         (self.black_pawns, 'p'),
    #         (self.black_knights, 'n'),
    #         (self.black_bishops, 'b'),
    #         (self.black_rooks, 'r'),
    #         (self.black_queens, 'q'),
    #         (self.black_kings, 'k')
    #     ]
    #     for bb, char in bb_map:
    #         for i in range(64):
    #             if bb & (1 << i):
    #                 board[i] = char
    #     for rank in range(7, -1, -1):
    #         print(' '.join(board[rank*8:(rank+1)*8]))
        
    #     if not self.white_to_move:
    #         self.rotate()
        
    #     score = self.evaluate()
    #     print(f"Turn: {('W' if self.white_to_move else 'B')} Plies: {self.plies_played} Moves: {self.moves_played} Score: {score} Check: {self.in_check()}  Rev: Check: {self.in_check(False)}")
    #     print(f"Fen: {self.get_fen()}")
# === End of board.py ===

# === Start of search.py ===
import math, time

class TTEntry:
    __slots__ = ('key', 'score', 'depth', 'flag', 'move')
    def __init__(self, key=0, score=0, depth=0, flag='EXACT', move=None):
        self.key = key
        self.score = score
        self.depth = depth
        self.flag = flag
        self.move = move

class TranspositionTable:
    def __init__(self, size_bytes=2_147_483_648):
        entry_size = 32  # approximate bytes per entry
        self.size = size_bytes // entry_size
        self.table = [None] * self.size

    def index(self, zobrist_key):
        return zobrist_key % self.size

    def store(self, key, depth, score, flag, move):
        idx = self.index(key)
        entry = self.table[idx]
        # Replace if empty or shallower than current
        if entry is None or entry.depth <= depth:
            self.table[idx] = TTEntry(key, score, depth, flag, move)

    def probe(self, key):
        idx = self.index(key)
        entry = self.table[idx]
        if entry is not None and entry.key == key:
            return entry
        return None

class Search:
    MATE_SCORE_UPPER = 32000
    TIME_CUT = 1e8
    Q_MAX_DEPTH = 20
    
    def __init__(self, board, tt_size_bytes=2_147_483_648):
        self.board = board
        self.nodes = 0
        self.tt = TranspositionTable(size_bytes=tt_size_bytes)
        self.time_limit = None      # seconds
        self.end_time = None
        self.time_up = False
        self.depth = 50
        self.killer_moves = [[None, None] for _ in range(64)]
        self.history_table = [[0] * 64 for _ in range(64)]

    def clear_tables(self):
        """Called at the start of a new top-level search."""
        self.killer_moves = [[None, None] for _ in range(64)]
        self.history_table = [[0] * 64 for _ in range(64)]

    def set_time_limit(self, seconds):
        self.time_limit = seconds
        self.end_time = time.time() + seconds
        self.time_up = False
        
    def set_depth(self, depth):
        self.depth = depth

    def set_board(self, board):
        self.board = board

    def print_stats(self, depth, score, time, notes, nps, pv):
        print(f"info depth {depth} score cp {score} time {time} nodes {notes} nps {nps} pv {pv}", flush=True)

    def score_killer_move(self, move, ply, tt_move):
        # 1. Transposition Table Move (Highest Priority)
        if tt_move and move == tt_move:
            return 9000000  # Highest possible score

        # 2. Promotions
        if move.promo:
            # Use a high score, prioritizing Queen
            return 8000000 + self.board.PIECE_VALUES[move.promo] * 10
        
        # 3. Captures (MVV-LVA - Your existing logic)
        if move.capture:
            # NOTE: Your board needs a PIECE_VALUES property
            # Consider using a higher base score for captures than for quiet moves
            victim_value = self.board.PIECE_VALUES[move.capture]
            attacker_value = self.board.PIECE_VALUES[move.piece]
            # Simple scaling to keep this range between 7M and 8M
            return 7000000 + 10 * victim_value - attacker_value
            # *For maximum strength, this should be replaced by Static Exchange Evaluation (SEE)*
        
        # --- Quiet Moves (Lower Priority) ---
        
        # 4. Killer Moves
        if move == self.killer_moves[ply][0]:
            return 600000  # High score for primary killer
        if move == self.killer_moves[ply][1]:
            return 500000  # Slightly lower for secondary killer

        # 5. History Heuristic
        # Assuming move provides from_sq and to_sq indices (0-63)
        from_sq_idx = move.from_sq
        to_sq_idx = move.to_sq
        
        # History scores are typically much smaller, e.g., max 10000.
        return self.history_table[from_sq_idx][to_sq_idx]

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        best_score = None
        
        self.nodes = 0
        self.clear_tables()

        for depth in range(1, self.depth + 1):  # iterative deepening
            if self.time_up:
                break

            best_score = self.search(depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            if not self.time_up:
                entry = self.tt.probe(self.board.hash)
                if entry and entry.move:
                    best_move = entry.move

                elapsed_time = time.time() - start_time
                nps = math.ceil(self.nodes / elapsed_time) if elapsed_time > 0 else 1

                uci_move = self.board.move_to_uci(best_move) if best_move else None
                self.print_stats(str(depth), str(math.ceil(best_score)), str(math.ceil(elapsed_time * 1000)), str(self.nodes), str(nps), str(uci_move))

            if self.time_up or self.time_limit and time.time() >= self.end_time:
                self.time_up = True
                break
            
            if depth >= self.depth:
                break

        # When time expires, return the best move/eval found
        return best_move, best_score

    def threefold(self):
        count = 1
        
        for entry in self.board.history:
            count += entry[-1] == self.board.hash
            if count >= 3:
                return True
            
        return False

    def has_sufficient_material(self):
        """
        board: object with bitboards like board.white_pawns, board.white_knights, etc.
        is_white: whether to check for white or black
        """
        pawns  = bin(self.board.white_pawns).count('1')
        minors = bin(self.board.white_knights).count('1') + bin(self.board.white_bishops).count('1')
        majors = bin(self.board.white_rooks).count('1') + bin(self.board.white_queens).count('1')

        return pawns > 0 or minors + majors >= 2

    def search(self, depth, alpha=-MATE_SCORE_UPPER, beta=MATE_SCORE_UPPER, ply=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
            
        in_check = self.board.in_check()
        
        depth += in_check
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if depth == 0:
            return self.q_search(alpha, beta)
        
        is_pv_node = beta > alpha + 1
        alpha_orig = alpha

        self.nodes += 1
        
        # --- TT lookup ---
        entry = self.tt.probe(self.board.hash)
        if entry and entry.depth >= depth:
            if entry.flag == 'EXACT':
                return entry.score
            elif entry.flag == 'LOWERBOUND':
                alpha = max(alpha, entry.score)
            elif entry.flag == 'UPPERBOUND':
                beta = min(beta, entry.score)
            if alpha >= beta:
                return alpha # if entry.flag == 'UPPERBOUND' else beta

        if not is_pv_node and not in_check:
            stand_pat = self.board.evaluate()
            
            # Futility pruning (low eval)
            if depth <= 2 and stand_pat + 100 * depth <= alpha:
                return stand_pat

            # Razor pruning (high eval)
            if depth <= 3 and stand_pat >= beta - 80 * depth:
                return stand_pat

        if not is_pv_node and not in_check and depth <= 5:
            cut_boundary = alpha - (150 * depth)
            if stand_pat <= cut_boundary:
                if depth <= 2:
                    return self.q_search(alpha, alpha + 1)

                local_score = self.q_search(cut_boundary, cut_boundary + 1)

                if local_score <= cut_boundary:
                    return local_score

        # Null move pruning (only when safe)
        if (
            not is_pv_node
            and not in_check
            and depth >= 3
            and self.has_sufficient_material()
        ):
            reduction = 2 + depth / 6 # typical reduction
            self.board.nullmove()

            # skip if nullmove leaves us in check (can happen in some custom rulesets)
            if not self.board.in_check(False):
                null_score = -self.search(depth - reduction - 1, -beta, -beta + 1)

                if null_score >= beta:
                    self.board.unmove()
                    return beta
                
                self.board.unmove()

        if not is_pv_node and not in_check and entry and entry.move and entry.depth >= depth and abs(entry.score) < self.MATE_SCORE_UPPER:
            self.board.move_tuple(entry.move)
            local_score = -self.search(depth - 1, -beta, -alpha)
            self.board.unmove()

            if local_score >= beta:
                return beta

        best_score = -float('inf')
        best_move = None

        played_moves = 0
        
        all_moves = list(sorted(self.board.generate_pseudo_legal_moves(), key=self.board.score_move, reverse=True))
        
        scored_moves = []
        for move in all_moves:
             # Pass the current ply and the tt_move
             score = self.score_killer_move(move, ply, entry.move if entry else None)
             scored_moves.append((score, move))
             
        sorted_moves = sorted(scored_moves, key=lambda x: x[0], reverse=True)

        for score, move in sorted_moves:
            self.board.move_tuple(move)
                      
            if self.board.in_check(False):
                self.board.unmove()
                continue

            played_moves += 1
            
            is_quiet = not move.capture and not move.promo

            reduction = 1
            if is_quiet and depth >= 3 and played_moves > 3:
                reduction = int(0.75 + math.log(depth) * math.log(played_moves) / 2)

            if reduction > 0:
                score = -self.search(depth - reduction, -alpha-1, -alpha, ply + 1)

            if score > alpha:
                score = -self.search(depth - 1, -alpha-1, -alpha, ply + 1)
                if is_pv_node and score > alpha:
                    score = -self.search(depth - 1, -beta, -alpha, ply + 1)
            
            # score = -self.search(depth - 1, -beta, -alpha)
            
            if self.time_up:
                self.board.unmove()
                break
            
            self.board.unmove()

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            
            if alpha >= beta:
                if is_quiet:
                    # Update Killer Heuristic
                    self.killer_moves[ply][1] = self.killer_moves[ply][0] # Move old killer to slot 1
                    self.killer_moves[ply][0] = move                      # New killer in slot 0
                    
                    # Update History Heuristic (e.g., add 1 to the score)
                    from_sq_idx = move.from_sq
                    to_sq_idx = move.to_sq
                    # Increase history score, possibly scaled by depth (e.g. depth * depth)
                    self.history_table[from_sq_idx][to_sq_idx] += depth * depth
                    # Limit the score to prevent overflow/bias (e.g., max 10000)
                break  # beta cutoff
            
        if not played_moves:
            return -self.MATE_SCORE_UPPER + depth if self.board.in_check() else 0

        # --- Store in TT ---
        if best_score <= alpha_orig:
            flag = 'UPPERBOUND'
            # Note: Do NOT store best_move for UPPERBOUND as it's unreliable
            tt_move = None 
        elif best_score >= beta:
            flag = 'LOWERBOUND'
            # Store the move that caused the cutoff (Refutation Move)
            tt_move = best_move 
        else:
            flag = 'EXACT'
            # Store the best move found
            tt_move = best_move

        if not self.time_up:
            # Pass the appropriate move (tt_move) to the store function
            self.tt.store(self.board.hash, depth, best_score, flag, tt_move)

        return best_score
    
    def q_search(self, alpha, beta, q_depth=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
        
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # if q_depth >= self.Q_MAX_DEPTH:
        #     # Stop searching noisy moves and return the static evaluation
        #     return self.board.evaluate()
        
        in_check = self.board.in_check()
        
        stand_pat = self.board.evaluate()
        
        if not in_check:
            stand_pat = self.board.evaluate()
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            # If in check, stand_pat is irrelevant, alpha remains the score to beat
            stand_pat = -float('inf')
        
        self.nodes += 1
        
        # TT lookup
        entry = self.tt.probe(self.board.hash)
        if entry and entry.depth == 0:  # q-search "depth"
            if entry.flag == 'EXACT':
                return entry.score
            elif entry.flag == 'LOWERBOUND':
                alpha = max(alpha, entry.score)
            elif entry.flag == 'UPPERBOUND':
                beta = min(beta, entry.score)
            if alpha >= beta:
                return alpha
        
        if not in_check and stand_pat >= beta:
            return stand_pat
        
        alpha_orig = alpha

        for move in sorted(self.board.generate_pseudo_legal_moves(active=not in_check), key=self.board.score_move, reverse=True):
            self.board.move_tuple(move)
            
            if self.board.in_check(False):
                self.board.unmove()
                continue
            
            score = -self.q_search(-beta, -alpha, q_depth + 1)
            
            if self.time_up:
                self.board.unmove()
                break
            
            self.board.unmove()

            if score >= beta:
                # Store cutoff in TT
                if not self.time_up:
                    self.tt.store(self.board.hash, 0, beta, 'LOWERBOUND', move)
                return beta
            if score > alpha:
                alpha = score

        # --- Store in TT ---
        if alpha <= stand_pat: # If the best score is the stand-pat, or was not improved
            flag = 'EXACT' # Treat stand-pat or slight improvement as exact in Q-Search
            tt_move = None
        # If the score was reduced from a previous TT value (rare/edge case for Q-search)
        elif alpha <= alpha_orig: 
            flag = 'UPPERBOUND'
            tt_move = None
        else:
            flag = 'EXACT' # Or if alpha was improved
            tt_move = None
            
        if not self.time_up:
            # Note: TT for Q-search usually stores the stand_pat/final alpha
            self.tt.store(self.board.hash, 0, alpha, flag, tt_move)
            
        return alpha
# === End of search.py ===

# from perft import Perft

board = Board()
search = Search(board)

for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    if line.lower() == "quit":
        break
    
    if line.startswith("position"):
        board = Board()
        
        # Strip the "position " prefix
        cmd = line[9:]

        # Default to the starting position if nothing else is provided
        if cmd.startswith("startpos"):
            cmd = cmd[len("startpos"):]
        # elif cmd.startswith("fen"):
        #     board = Board()
        #     search = Search(board)
        #     # Extract FEN before the "moves" keyword if present
        #     fen_section = cmd[len("fen "):]
        #     if " moves " in fen_section:
        #         fen, moves_section = fen_section.split(" moves ", 1)
        #     else:
        #         fen, moves_section = fen_section, ""
        #     board.set_fen(fen)
        #     cmd = moves_section
        else:
            moves_section = ""

        # Apply moves if given
        if "moves" in cmd:
            moves_section = cmd.split("moves ", 1)[1]

        if moves_section:
            moves = moves_section.split()
            for move in moves:
                board.uci_move(move)
                
        search.set_board(board)
    elif line.lower() == "ucinewgame":
            board = Board()
            search = Search(board)
    elif line.lower() == "uci":
        print("pygone2.0\nuciok", flush=True)
    elif line.startswith("isready"):
        print("readyok", flush=True)
    elif line.startswith("go "):
        tokens = line.split()
        wtime = btime = movestogo = None
        depth = None
        # perft_depth = None

        i = 1
        while i < len(tokens):
            if tokens[i] == "wtime":
                wtime = int(tokens[i+1])
                i += 2
            elif tokens[i] == "btime":
                btime = int(tokens[i+1])
                i += 2
            # elif tokens[i] == "movestogo":
            #     movestogo = int(tokens[i+1])
            #     i += 2
            # elif tokens[i] == "depth":
            #     depth = int(tokens[i+1])
            #     i += 2
            # elif tokens[i] == "perft":
            #     perft_depth = int(tokens[i+1])
            #     i += 2
            else:
                i += 1
              
        # if perft_depth:
        #     perft = Perft(board)
        #     perft.run(perft_depth)
        #     continue
              
        search.set_board(board)
          
        if depth:
            search.set_time_limit(1e8)
            search.set_depth(depth)
        else:
            search.set_depth(50)
            side_time = (wtime if board.white_to_move else btime) / 1000
            
            move_time = max(2.2, side_time / 28)
            
            search.set_time_limit(move_time)
            
        move, score = search.iterative_search()
        
        if not move:
            search.set_depth(1)
            move, score = search.iterative_search()
            
        if move:
            print(f"bestmove {board.move_to_uci(move)}", flush=True)
    # elif line.startswith('print'):
    #     board.print_board()
    # elif line.startswith('fen'):
    #     print(board.get_fen(), flush=True)
