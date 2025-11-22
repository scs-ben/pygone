import random
# from typing import Tuple

# U64 = int
# SQ = int
# Move = Tuple[int,int,str,str,str,int]  # from, to, promotion or None, capture or None, piece moving, castling

# --- helpers --------------------------------------------------------------
FILES = "abcdefgh"
RANKS = "12345678"
IDX_TO_PIECE = ['p','n','b','r','q','k']
PROMO_MAP = {'q': 4, 'r': 3, 'b': 2, 'n': 1}
A_FILE_MASK = 0x0101010101010101

CR_MASK = [15] * 64
CR_MASK[0] = 13   # a1 (Remove WQ-2)
CR_MASK[4] = 12   # e1 (Remove WK-1, WQ-2)
CR_MASK[7] = 14   # h1 (Remove WK-1)
CR_MASK[56] = 7   # a8 (Remove BQ-8)
CR_MASK[60] = 3   # e8 (Remove BK-4, BQ-8)
CR_MASK[63] = 11  # h8 (Remove BK-4)

UNIFIED_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50, # Rank 1/8
    -40,-20, 0, 0, 0, 0,-20,-40,
    -30, 0, 10, 15, 15, 10, 0,-30,
    -30, 5, 15, 20, 20, 15, 5,-30, # Center ranks
    -30, 5, 15, 20, 20, 15, 5,-30,
    -30, 0, 10, 15, 15, 10, 0,-30,
    -40,-20, 0, 0, 0, 0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50 # Rank 8/1
]
PST_WEIGHTS = [1, 3, 2, 1, 1, 4]

# --- utilities -------------------------------------------------------------
def get_bit(s): 
    return 1 << s

def pop_lsb(bb):
    lsb = bb & -bb; idx = lsb.bit_length() - 1
    return bb ^ lsb, idx

# direction offsets in square index (used for ray walking)
N, S, E, W, NE, NW, SE, SW = 8, -8, 1, -1, 9, 7, -7, -9
DIRS_ROOK = (N,S,E,W)
DIRS_BISHOP = (NE,NW,SE,SW)

KNIGHT_ATK = [0]*64
KING_ATK   = [0]*64
PAWN_ATK_WHITE = [0]*64
PAWN_ATK_BLACK = [0]*64

for sq in range(64):
    r = sq//8; f = sq%8
    # knight
    bm = 0
    # Knight deltas
    for d in (17,15,10,6,-6,-10,-15,-17):
        ns = sq + d
        if 0 <= ns < 64:
            rr = ns//8; ff = ns%8
            if abs(rr-r)+abs(ff-f) == 3: bm |= get_bit(ns)
    KNIGHT_ATK[sq] = bm
    # king
    bm = 0
    # King deltas
    for d in (1,-1,8,-8,9,7,-7,-9):
        ns = sq + d
        if 0 <= ns < 64:
            rr = ns//8; ff = ns%8
            if max(abs(rr-r), abs(ff-f)) == 1: bm |= get_bit(ns)
    KING_ATK[sq] = bm
    # pawn attacks
    bm_w = 0
    if f>0 and r<7: bm_w |= get_bit(sq+7)
    if f<7 and r<7: bm_w |= get_bit(sq+9)
    PAWN_ATK_WHITE[sq] = bm_w
    bm_b = 0
    if f>0 and r>0: bm_b |= get_bit(sq-9)
    if f<7 and r>0: bm_b |= get_bit(sq-7)
    PAWN_ATK_BLACK[sq] = bm_b

random.seed(2025)  # deterministic

PIECE_KEYS = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
CASTLING_KEYS = [random.getrandbits(64) for _ in range(16)]
EP_KEYS = [random.getrandbits(64) for _ in range(8)]
SIDE_KEY = random.getrandbits(64)

# --- board class ----------------------------------------------------------
class Board:
    PIECE_VALUES = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 0
    }
    
    #UNITremove
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    #UNITendremove
    
    def __init__(self, fen = None):
        # piece bitboards: WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK
        self.P = [0]*12
        self.piece_map = [-1] * 64
        self.white_to_move = True
        self.castle = 0  # bits: wk(1), wq(2), bk(4), bq(8)
        self.ep = -1
        self.halfmove_clock = 0
        # state stack for unmake
        self.stack = []
        # this is for standard start pos, we can remove set_fen and compute hash for 4k
        self.P = [65280, 66, 36, 129, 8, 16, 71776119061217280, 4755801206503243776, 2594073385365405696, 9295429630892703744, 576460752303423488, 1152921504606846976]
        self.hash = 6770668349075704229
        #UNITremove
        if not fen:
            self.set_fen(self.START_FEN)
        else:
            self.set_fen(fen)
        #UNITendremove

    #UNITremove
    def compute_hash(self):
        h = 0

        # pieces
        for idx, bb in enumerate(self.P):   # self.P[0..11] piece bitboards
            b = bb
            while b:
                sq = (b & -b).bit_length() - 1
                b &= b - 1
                h ^= PIECE_KEYS[idx][sq]

        # castling
        h ^= CASTLING_KEYS[self.castle]   # 0–15

        # en-passant
        if self.ep != -1:
            h ^= EP_KEYS[self.ep & 7]

        # side
        if self.white_to_move:
            h ^= SIDE_KEY

        self.hash = h
        return h
    #UNITendremove

    def pieces_of(self, side_white):
        if side_white:
            return self.P[0]|self.P[1]|self.P[2]|self.P[3]|self.P[4]|self.P[5]
        else:
            return self.P[6]|self.P[7]|self.P[8]|self.P[9]|self.P[10]|self.P[11]

    def all_occupied(self):
        occ = 0
        for bb in self.P: occ |= bb
        return occ

    def side_index(self, white, piece_idx):
        return piece_idx if white else piece_idx+6

    #UNITremove
    def set_fen(self, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        self.P = [0]*12
        self.piece_map = [-1] * 64
        for r, row in enumerate(rows):
            sq = (7-r)*8
            for ch in row:
                if ch.isdigit(): sq += int(ch); continue
                piece_map = {'P':0,'N':1,'B':2,'R':3,'Q':4,'K':5,
                             'p':6,'n':7,'b':8,'r':9,'q':10,'k':11}
                idx = piece_map[ch]
                self.P[idx] |= get_bit(sq)
                self.piece_map[sq] = idx # (0-11)
                
                sq += 1
        self.white_to_move = (parts[1] == 'w')
        self.castle = 0
        if 'K' in parts[2]: self.castle |= 1
        if 'Q' in parts[2]: self.castle |= 2
        if 'k' in parts[2]: self.castle |= 4
        if 'q' in parts[2]: self.castle |= 8
        self.ep = -1 if parts[3] == '-' else self.algebraic_to_sq(parts[3])
        # ignore halfmove/fullmove counters
        self.compute_hash()
    #UNITendremove

    def algebraic_to_sq(self, s:str):
        return FILES.index(s[0]) + 8*int(s[1])-8

    def _x(self, i, s):
        self.P[i] ^= (1 << s)
        self.hash ^= PIECE_KEYS[i][s]

    # make/unmake minimal for legality checking
    def make_move(self, mv):
        if not mv:
            return
        frm, to, promo, _, _, _ = mv
        us = self.white_to_move
        
        # 1. CACHE OLD STATE
        old_ep, old_castle, old_clock, old_hash = self.ep, self.castle, self.halfmove_clock, self.hash

        # 2. IDENTIFY MOVING PIECE
        # (We assume you still have get_bit or use 1<<frm)
        from_mask = 1 << frm
        to_mask = 1 << to
        
        moved_piece_type = None
        moved_piece_idx = -1
        
        for p in range(6):
            idx = self.side_index(us, p)
            if self.P[idx] & from_mask:
                moved_piece_type = p
                moved_piece_idx = idx
                break
                
        # 3. HANDLE CAPTURES & EN PASSANT
        captured_idx = -1
        is_ep_capture = False
        
        if moved_piece_type == 0 and to == self.ep:
            is_ep_capture = True
            cap_sq = to - 8 if us else to + 8
            captured_idx = self.side_index(not us, 0)
            # USE HELPER: Remove EP Pawn
            self._x(captured_idx, cap_sq) 
            self.piece_map[cap_sq] = -1
        else:
            for p in range(6):
                e_idx = self.side_index(not us, p)
                if self.P[e_idx] & to_mask:
                    captured_idx = e_idx
                    # USE HELPER: Remove Captured Piece
                    self._x(e_idx, to) 
                    break
        
        # 4. PUSH TO STACK
        # (Assuming you are using the optimized stack from previous steps)
        self.stack.append((mv, captured_idx, is_ep_capture, old_ep, old_castle, old_clock, old_hash))

        # 5. UPDATE MOVING PIECE
        # USE HELPER: Remove from 'from'
        self._x(moved_piece_idx, frm)
        self.piece_map[frm] = -1
        
        # Determine target piece (handle promotion)
        target_idx = moved_piece_idx
        if promo:
            # promo is now an int (1-4) if you updated gen_legal, or use map
            target_idx = self.side_index(us, PROMO_MAP[promo])
            
        # USE HELPER: Place on 'to'
        self._x(target_idx, to)
        self.piece_map[to] = target_idx

        # 6. UPDATE CLOCKS & SIDE
        self.hash ^= SIDE_KEY
        self.halfmove_clock += 1
        if captured_idx != -1 or moved_piece_type == 0:
            self.halfmove_clock = 0
            
        # 7. UPDATE CASTLING RIGHTS (Using CR_MASK)
        self.hash ^= CASTLING_KEYS[old_castle]
        self.castle &= CR_MASK[frm] & CR_MASK[to]
        self.hash ^= CASTLING_KEYS[self.castle]

        # 8. HANDLE CASTLING MOVE (Moving the Rook)
        if moved_piece_type == 5 and abs(frm - to) == 2:
            if to > frm: r_from, r_to = (frm + 3, frm + 1)
            else:        r_from, r_to = (frm - 4, frm - 1)
            
            rook_idx = self.side_index(us, 3)
            # USE HELPER: Move Rook (Remove old, Place new)
            self._x(rook_idx, r_from)
            self._x(rook_idx, r_to)
            self.piece_map[r_from] = -1
            self.piece_map[r_to] = rook_idx

        # 9. UPDATE EP TARGET
        if self.ep != -1: self.hash ^= EP_KEYS[self.ep & 7]
        self.ep = (frm + to) // 2 if (moved_piece_type == 0 and abs(frm - to) == 16) else -1
        if self.ep != -1: self.hash ^= EP_KEYS[self.ep & 7]
            
        self.white_to_move = not self.white_to_move

    def unmake_move(self):
        if not self.stack: return
        # Pop all state. Note: We handle 'is_ep' logic inside the index check now to save vars
        mv, c_idx, is_ep, self.ep, self.castle, self.halfmove_clock, self.hash = self.stack.pop()
        self.white_to_move = not self.white_to_move
        
        f, t, pr, _, _, _ = mv
        
        # 1. Pull piece back (t -> f)
        pc = self.piece_map[t]                  # Get piece at 'to' (could be promoted Queen)
        self.P[pc] ^= (1 << t)                  # Remove from 'to'
        self.piece_map[t] = -1

        # If promo, the piece landing on 'f' is a Pawn (0/6), otherwise it's 'pc'
        real_p = pc if not pr else (0 if self.white_to_move else 6)
        self.P[real_p] |= (1 << f)              # Place on 'from'
        self.piece_map[f] = real_p

        # 2. Restore Capture
        if c_idx != -1:
            # If En Passant, capture is shifted. Else it's at 't'
            c_sq = t if not is_ep else (t - 8 if self.white_to_move else t + 8)
            self.P[c_idx] |= (1 << c_sq)
            self.piece_map[c_sq] = c_idx

        # 3. Un-Castle (Move Rook back)
        # If King moved >1 square, we must revert the Rook
        if (real_p == 5 or real_p == 11) and abs(f - t) == 2:
            # r_old = corner, r_new = center-ish
            # K-side (t>f): r_new=f+1, r_old=f+3. Q-side: r_new=f-1, r_old=f-4
            r_new, r_old = (f + 1, f + 3) if t > f else (f - 1, f - 4)
            r_idx = 3 if self.white_to_move else 9
            self.P[r_idx] ^= (1 << r_new) | (1 << r_old) # Toggle both rook squares at once
            self.piece_map[r_new], self.piece_map[r_old] = -1, r_idx

    # attack detection
    def attacked(self, sq, by_white):
        occ = self.all_occupied()
        # Pre-calculate Attacker Bitboards for Sliding Pieces
        r_q_attacker_bb = self.P[self.side_index(by_white, 3)] | self.P[self.side_index(by_white, 4)]
        b_q_attacker_bb = self.P[self.side_index(by_white, 2)] | self.P[self.side_index(by_white, 4)]
        
        # pawn
        if by_white:
            if PAWN_ATK_BLACK[sq] & self.P[self.side_index(True, 0)]: return True
        else:
            if PAWN_ATK_WHITE[sq] & self.P[self.side_index(False, 0)]: return True
            
        # knight
        if KNIGHT_ATK[sq] & self.P[self.side_index(by_white,1)]: return True
        # king
        if KING_ATK[sq] & self.P[self.side_index(by_white,5)]: return True
        
        # sliding: rook/queen for orthogonals
        for d in DIRS_ROOK:
            s = sq
            while True:
                ns = s + d
                if ns < 0 or ns >= 64: break
                # file wrap checks
                if d == E and ns%8 == 0: break
                if d == W and ns%8 == 7: break
                s = ns; m = get_bit(s)
                
                if m & r_q_attacker_bb: # Is this an attacking Rook or Queen?
                    return True
                    
                if m & occ: # Is this ANY piece (blocking the ray)?
                    break
                    
        # sliding: bishop/queen for diagonals
        for d in DIRS_BISHOP:
            s = sq
            while True:
                ns = s + d
                if ns < 0 or ns >= 64: break
                # file wrap
                if d in (NE,SE) and ns%8 == 0: break
                if d in (NW,SW) and ns%8 == 7: break
                s = ns; m = get_bit(s)
                
                if m & b_q_attacker_bb: # Is this an attacking Bishop or Queen?
                    return True
                    
                if m & occ: # Is this ANY piece (blocking the ray)?
                    break
                    
        return False

    def king_square(self, white):
        bb = self.P[self.side_index(white,5)]
        return (bb & -bb).bit_length()-1 if bb else -1
    
    def in_check(self, white=True):
        return self.attacked(self.king_square(self.white_to_move), not self.white_to_move) if white else self.attacked(self.king_square(not self.white_to_move), self.white_to_move)

    # --- move generation -------------------------------------------------
    def gen_pseudo_legal(self):
        us = self.white_to_move
        occ = self.all_occupied()
        our = self.pieces_of(us)
        their = self.pieces_of(not us)

        # pawns
        pawns = self.P[self.side_index(us,0)]
        while pawns:
            pawns, sq = pop_lsb(pawns)
            if us:
                # single push
                if not (occ & get_bit(sq+8)) and sq//8 < 7:
                    # promotion?
                    if sq//8 == 6:
                        for p in ('q','r','b','n'): yield (sq, sq+8, p, None, 'p', False)
                    else:
                        yield (sq, sq+8, None, None, 'p', False)
                        if sq//8 == 1 and not (occ & get_bit(sq+16)):
                            yield (sq, sq+16, None, None, 'p', False)
                # captures
                for t in (sq+7, sq+9):
                    if 0<=t<64:
                        if (PAWN_ATK_WHITE[sq] & get_bit(t)) and (their & get_bit(t)):
                            if sq//8 == 6:
                                for p in ('q','r','b','n'): yield (sq,t,p,  self.piece_on(t), 'p', False)
                            else: yield (sq,t,None,  self.piece_on(t), 'p', False)
                # ep
                if self.ep != -1:
                    if PAWN_ATK_WHITE[sq] & get_bit(self.ep):
                        yield (sq,self.ep,None,'p', 'p', False)
            else:
                if not (occ & get_bit(sq-8)) and sq//8 > 0:
                    if sq//8 == 1:
                        for p in ('q','r','b','n'): yield (sq, sq-8, p, None, 'p', False)
                    else:
                        yield (sq, sq-8, None, None, 'p', False)
                        if sq//8 == 6 and not (occ & get_bit(sq-16)):
                            yield (sq, sq-16, None, None, 'p', False)
                for t in (sq-7, sq-9):
                    if 0<=t<64:
                        if (PAWN_ATK_BLACK[sq] & get_bit(t)) and (their & get_bit(t)):
                            if sq//8 == 1:
                                for p in ('q','r','b','n'): yield (sq,t,p,  self.piece_on(t), 'p', False)
                            else: yield (sq,t,None,  self.piece_on(t), 'p', False)
                if self.ep != -1:
                    if PAWN_ATK_BLACK[sq] & get_bit(self.ep):
                        yield (sq,self.ep,None,'p', 'p', False)
        # knights
        knights = self.P[self.side_index(us,1)]
        while knights:
            knights, sq = pop_lsb(knights)
            atk = KNIGHT_ATK[sq] & ~our
            bb = atk
            while bb:
                bb, t = pop_lsb(bb)
                yield (sq,t,None,  self.piece_on(t), 'n', False)
        # bishops
        bishops = self.P[self.side_index(us,2)]
        while bishops:
            bishops, sq = pop_lsb(bishops)
            for d in DIRS_BISHOP:
                s = sq
                while True:
                    ns = s + d
                    if ns < 0 or ns >= 64: break
                    if d in (NE,SE) and ns%8 == 0: break
                    if d in (NW,SW) and ns%8 == 7: break
                    s = ns
                    m = get_bit(s)
                    if m & our: break
                    yield (sq,s,None,  self.piece_on(s), 'b', False)
                    if m & their: break
        # rooks
        rooks = self.P[self.side_index(us,3)]
        while rooks:
            rooks, sq = pop_lsb(rooks)
            for d in DIRS_ROOK:
                s = sq
                while True:
                    ns = s + d
                    if ns < 0 or ns >= 64: break
                    if d == E and ns%8 == 0: break
                    if d == W and ns%8 == 7: break
                    s = ns; m = get_bit(s)
                    if m & our: break
                    yield (sq,s,None,  self.piece_on(s), 'r', False)
                    if m & their: break
        # queens
        queens = self.P[self.side_index(us,4)]
        while queens:
            queens, sq = pop_lsb(queens)
            for d in DIRS_ROOK+DIRS_BISHOP:
                s = sq
                while True:
                    ns = s + d
                    if ns < 0 or ns >= 64: break
                    # file wrap checks
                    if d in (E,NE,SE) and ns%8 == 0: break
                    if d in (W,NW,SW) and ns%8 == 7: break
                    s = ns; m = get_bit(s)
                    if m & our: break
                    yield (sq,s,None,  self.piece_on(s), 'q', False)
                    if m & their: break
        # king
        ksq = self.king_square(us)
        if 0 <= ksq < 64:
            bb = KING_ATK[ksq] & ~our
            while bb:
                bb, t = pop_lsb(bb)
                yield (ksq,t,None, self.piece_on(t), 'k', False)
            # castling (basic tests: empty squares + not attacked)
            if us:
                # white king e1=4
                if (self.castle & 1) and not (occ & (get_bit(5)|get_bit(6))):
                    # ensure no squares attacked f1/e1/g1
                    if not self.attacked(4, False) and not self.attacked(5,False) and not self.attacked(6,False):
                        yield (4,6,None, None, 'k', True)
                if (self.castle & 2) and not (occ & (get_bit(1)|get_bit(2)|get_bit(3))):
                    if not self.attacked(4,False) and not self.attacked(3,False) and not self.attacked(2,False):
                        yield (4,2,None, None, 'k', True)
            else:
                if (self.castle & 4) and not (occ & (get_bit(61)|get_bit(62))):
                    if not self.attacked(60, True) and not self.attacked(61,True) and not self.attacked(62,True):
                        yield (60,62,None, None, 'k', True)
                if (self.castle & 8) and not (occ & (get_bit(57)|get_bit(58)|get_bit(59))):
                    if not self.attacked(60,True) and not self.attacked(59,True) and not self.attacked(58,True):
                        yield (60,58,None, None, 'k', True)

    def king_safety(self, white):
        k = self.king_square(white)
        f, r = k % 8, k // 8
        d, bb = (1, 0) if white else (-1, 6) # Direction and Pawn BB index
        
        # Calculate Pawn Shield Score using a generator expression
        pawn_shield = 10 * sum(
            1 for df in (-1, 0, 1) 
            if 0 <= (nf := f + df) < 8 # Check new file
            and 0 <= (nr := r + d) < 8  # Check new rank
            and (self.P[bb] & get_bit(nr * 8 + nf))
        )
        
        # Calculate Castling/Position Score
        castle_pos_score = (
            # 1. Castled Position Bonus (+15 if king on g/c file)
            15 if (white and k in (6, 2)) or (not white and k in (62, 58)) else 0
        ) + (
            # 2. Lost Kingside Rights Penalty (-10)
            -10 if not (self.castle & (1 if white else 4)) else 0
        ) + (
            # 3. Lost Queenside Rights Penalty (-5)
            -5 if not (self.castle & (2 if white else 8)) else 0
        )
        
        return pawn_shield + castle_pos_score

    def eval_material(self):
        score = 0
        for idx, bb in enumerate(self.P):
            if bb == 0:
                continue
            piece_char = IDX_TO_PIECE[idx % 6]
            val = self.PIECE_VALUES[piece_char]
            # population count
            cnt = bb.bit_count()
            
            if idx < 6: score += val * cnt
            else: score -= val * cnt
        return score

    def eval_position(self):
        score = 0
        
        # Loop 12 times: White Pawns (0) to Black King (11)
        for i in range(12): 
            # T: Piece Type Index (0-5)
            piece = i % 6 
            
            # W: Weight based on the piece type
            weight = PST_WEIGHTS[piece] 
            
            # C: Color factor (1 for White, -1 for Black)
            color = 1 if i < 6 else -1
            
            # B: Copy of the Bitboard for the current piece type
            bb = self.P[i] 
            
            # --- Internal Loop: Iterating over set bits (squares) ---
            
            # Loop while the bitboard B has set bits
            while bb:
                # S: Square Index (Find the Least Significant Bit)
                # This bit hack finds the index of the LSB (e.g., using b.bit_length() - 1 
                # or a compiler intrinsic like __builtin_ctz if you were in C).
                # The most common Python implementation for a 64-bit board is this sequence:
                idx = (bb & -bb).bit_length() - 1 
                
                # Clear the LSB (bb &= bb - 1) is the standard fastest way to pop a bit.
                bb &= bb - 1 
                
                # D: PST Index. Mirror for Black pieces (C == -1). 
                # S^56 flips the rank (0 -> 56, 1 -> 57, etc.)
                D = idx if color == 1 else idx ^ 56
                
                # Add/subtract the weighted score
                score += UNIFIED_PST[D] * weight * color
                
        return score / 2
    
    # def pawn_structure_penalty(self, pawns):
    #     return sum(
    #         # Calculate the penalty for the current file 'f'
            
    #         # Determine the number of pawns on this file
    #         (pawn_count := ((pawns >> f) & A_FILE_MASK).bit_count()) > 0
    #         and (
    #             -15 * max(0, pawn_count - 1)
    #             + (-15 if (pawns & (
    #                 (A_FILE_MASK << max(0, f - 1)) | (A_FILE_MASK << min(7, f + 1))
    #             )) == 0 else 0)
    #         )
    #         for f in range(8)
    # )

    def evaluate(self):
        score = self.eval_material()
        score += self.king_safety(True) - self.king_safety(False)
        
        # score += self.pawn_structure_penalty(self.P[0]) - self.pawn_structure_penalty(self.P[6])
        
        score += self.eval_position()

        return score if self.white_to_move else -score

    def score_move(self, t_move):
        g_score = 0
        if t_move[3]:
            # MVV-LVA: Most valuable victim - least valuable attacker
            g_score += self.PIECE_VALUES[t_move[3]] * 100 - self.PIECE_VALUES[t_move[4]]
        if t_move[2]:
            # Promote to queen highest
            g_score += self.PIECE_VALUES[t_move[2]] * 1000
        if t_move[5]: # If the move is castling (assuming t_move[5] is the castling flag)
            g_score += 500
        return g_score

    def piece_on(self, sq):
        idx = self.piece_map[sq]
        return IDX_TO_PIECE[idx % 6] if idx != -1 else None

    def move_to_uci(self, mv):
        base = (FILES[mv[0] % 8] + RANKS[mv[0] // 8]) + (FILES[mv[1] % 8] + RANKS[mv[1] // 8])
        if mv[2]:
            return base + mv[2]
        return base
    
    #UNITremove
    def get_fen(self):
        # --- 1. Piece Placement (Part 1 of FEN) ---
        fen_rows = []
        piece_chars = ['P','N','B','R','Q','K', 'p','n','b','r','q','k']
        
        # Iterate over ranks from 8 down to 1 (r=7 down to 0)
        for r in range(7, -1, -1):
            fen_row = ""
            empty_count = 0
            
            # Iterate over files from a to h (f=0 to 7)
            for f in range(8):
                sq = r * 8 + f
                bit = get_bit(sq)
                piece_found = False
                
                # Check for a piece on the current square
                for idx, char in enumerate(piece_chars):
                    if self.P[idx] & bit:
                        if empty_count > 0:
                            fen_row += str(empty_count)
                            empty_count = 0
                        fen_row += char
                        piece_found = True
                        break
                
                if not piece_found:
                    empty_count += 1
            
            # Add final empty count if the row ends with empty squares
            if empty_count > 0:
                fen_row += str(empty_count)
                
            fen_rows.append(fen_row)
            
        fen_placement = "/".join(fen_rows)
        
        # --- 2. Side to Move (Part 2 of FEN) ---
        fen_turn = 'w' if self.white_to_move else 'b'
        
        # --- 3. Castling Rights (Part 3 of FEN) ---
        fen_castle = ""
        if self.castle & 1: fen_castle += 'K' # White King-side
        if self.castle & 2: fen_castle += 'Q' # White Queen-side
        if self.castle & 4: fen_castle += 'k' # Black King-side
        if self.castle & 8: fen_castle += 'q' # Black Queen-side
        
        if not fen_castle:
            fen_castle = '-'
            
        # --- 4. En-Passant Target Square (Part 4 of FEN) ---
        if self.ep == -1:
            fen_ep = '-'
        else:
            # Assumes you have a method to convert square index to algebraic notation
            fen_ep = FILES[self.ep % 8] + RANKS[self.ep // 8]
            
        # --- 5. Halfmove and Fullmove Clocks (Parts 5 & 6 of FEN) ---
        # These were not in your set_fen, so we default to standard values.
        # You may need to replace these with actual attribute lookups if you track them.
        fen_halfmove = str(self.halfmove_clock) if hasattr(self, 'halfmove_clock') else '0'
        fen_fullmove = str(self.fullmove_number) if hasattr(self, 'fullmove_number') else '1'

        # --- Combine all parts ---
        fen = " ".join([fen_placement, fen_turn, fen_castle, fen_ep, fen_halfmove, fen_fullmove])
        return fen
    #UNITendremove
    
    #remove
    def print_board(self):
        """Print board in human-readable format (for debugging)"""
        board = ['.'] * 64
            
        bb_map = [
            (self.P[0], 'P'),
            (self.P[1], 'N'),
            (self.P[2], 'B'),
            (self.P[3], 'R'),
            (self.P[4], 'Q'),
            (self.P[5], 'K'),
            (self.P[6], 'p'),
            (self.P[7], 'n'),
            (self.P[8], 'b'),
            (self.P[9], 'r'),
            (self.P[10], 'q'),
            (self.P[11], 'k')
        ]
        for bb, char in bb_map:
            for i in range(64):
                if bb & (1 << i):
                    board[i] = char
        for rank in range(7, -1, -1):
            print(' '.join(board[rank*8:(rank+1)*8]))
        
        score = self.evaluate()
        
        mat_score = self.eval_material()
        king_score = self.king_safety(True) - self.king_safety(False)
        
        # wp =  self.P[0]
        # bp =  self.P[6]
        pawn_score = 0
        # pawn_score = self.pawn_structure_penalty(wp) - self.pawn_structure_penalty(bp)

        pos_score = self.eval_position()
        
        print(f"Turn: {('W' if self.white_to_move else 'B')} 50c: {self.halfmove_clock} Score: {score} Check: {self.in_check()}  Rev: Check: {self.in_check(False)}")
        print(f"Mat: {mat_score} King: {king_score} Pawn: {pawn_score} Pos: {pos_score}")
        print(f"Fen: {self.get_fen()}")
    #endremove