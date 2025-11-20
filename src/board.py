import random
# from typing import Tuple

# U64 = int
# SQ = int
# Move = Tuple[int,int,str,str,str]  # from, to, promotion or None, capture or None, piece moving

# --- helpers --------------------------------------------------------------
FILES = "abcdefgh"
RANKS = "12345678"
IDX_TO_PIECE = ['p','n','b','r','q','k','p','n','b','r','q','k']

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
    
    #remove
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    #endremove
    
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
        #remove
        if not fen:
            self.set_fen(self.START_FEN)
        else:
            self.set_fen(fen)
        #endremove

    #remove
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
    #endremove

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

    #remove
    def set_fen(self, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        self.P = [0]*12
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
    #endremove

    def algebraic_to_sq(self, s:str):
        return FILES.index(s[0]) + 8*int(s[1])-8

    # make/unmake minimal for legality checking
    def make_move(self, mv):
        frm, to, promo, _, _ = mv
        # save state
        self.stack.append((self.P[:], self.piece_map[:], self.white_to_move, self.castle, self.ep, self.halfmove_clock, self.hash))
        
        us = self.white_to_move
        
        self.hash ^= SIDE_KEY

        if self.ep != -1:
            self.hash ^= EP_KEYS[self.ep & 7]

        self.hash ^= CASTLING_KEYS[self.castle]

        # find moving piece type
        from_mask = get_bit(frm); to_mask = get_bit(to)
        moved_piece = None
        for p in range(6):
            idx = self.side_index(us,p)
            if self.P[idx] & from_mask:
                self.hash ^= PIECE_KEYS[idx][frm]
                moved_piece = p; self.P[idx] ^= from_mask; self.piece_map[frm] = -1; break
        # capture (including en-passant)
        captured = False
        #remove
        if moved_piece is None:
            # sanity
            return
        #endremove
        
        # en-passant capture
        if moved_piece == 0 and to == self.ep:
            captured = True
            cap_sq = to - 8 if us else to + 8
            # remove enemy pawn
            self.hash ^= PIECE_KEYS[self.side_index(not us, 0)][cap_sq]
            self.P[self.side_index(not us, 0)] ^= get_bit(cap_sq)
            self.piece_map[cap_sq] = -1
        else:
            # capture any piece on 'to'
            for p in range(6):
                idx = self.side_index(not us, p)
                if self.P[idx] & to_mask:
                    self.hash ^= PIECE_KEYS[idx][to]
                    self.P[idx] ^= to_mask; self.piece_map[to] = -1; captured = True; break
        
        # Update halfmove clock, base clearing on actual board updates
        self.halfmove_clock += 1
        
        if captured or moved_piece == 0:
            self.halfmove_clock = 0
        
        # place moved piece (promotion?)
        if promo:
            prom_map = {'q':4,'r':3,'b':2,'n':1}
            prom_idx = self.side_index(us, prom_map[promo])
            self.P[self.side_index(us, prom_map[promo])] |= to_mask
            self.hash ^= PIECE_KEYS[prom_idx][to]
            self.piece_map[to] = prom_idx
        else:
            final_idx = self.side_index(us, moved_piece)
            self.P[self.side_index(us, moved_piece)] |= to_mask
            self.hash ^= PIECE_KEYS[final_idx][to]
            self.piece_map[to] = final_idx
        # update castle rights if king/rook moved or captured
        if moved_piece == 5:
            if us: self.castle &= ~3
            else: self.castle &= ~12
        if moved_piece == 3:
            if us and frm==0: self.castle &= ~2
            if us and frm==7: self.castle &= ~1
            if (not us) and frm==56: self.castle &= ~8
            if (not us) and frm==63: self.castle &= ~4
        if captured:
            # if rook captured update opponent castle rights
            # check to-square for rook initial squares
            if to == 0: self.castle &= ~2
            if to == 7: self.castle &= ~1
            if to == 56: self.castle &= ~8
            if to == 63: self.castle &= ~4
        
        # handle castling rook move
        cfr = 4; ct1 = 6; ct2 = 2
        if not us:
            cfr = 60; ct1 = 62; ct2 = 58
        
        if moved_piece==5 and frm==cfr and to==ct1:
            self.hash ^= PIECE_KEYS[self.side_index(us,3)][ct1+1]; self.hash ^= PIECE_KEYS[self.side_index(us,3)][ct1-1]
            self.P[self.side_index(us,3)] ^= get_bit(ct1+1); self.P[self.side_index(us,3)] |= get_bit(ct1-1)
            self.piece_map[ct1+1] = -1; self.piece_map[ct1-1] = self.side_index(us,3) 
        if moved_piece==5 and frm==cfr and to==ct2:
            self.hash ^= PIECE_KEYS[self.side_index(us,3)][ct2-2]; self.hash ^= PIECE_KEYS[self.side_index(us,3)][ct2+1]          
            self.P[self.side_index(us,3)] ^= get_bit(ct2-2); self.P[self.side_index(us,3)] |= get_bit(ct2+1)
            self.piece_map[ct2-2] = -1; self.piece_map[ct2+1] = self.side_index(us,3) 
            
        self.hash ^= CASTLING_KEYS[self.castle]
        
        # en-passant target update
        if moved_piece == 0 and abs(to - frm) == 16:
            # pawn double push
            self.ep = (frm + to)//2
        else:
            self.ep = -1
        
        if self.ep != -1:
            self.hash ^= EP_KEYS[self.ep & 7]
            
        # switch side
        self.white_to_move = not self.white_to_move

    # def nullmove(self):
    #     # Save state including current hash
    #     self.stack.append((self.P[:], self.piece_map[:], self.white_to_move, self.castle, self.ep, self.halfmove_clock, self.hash))
        
    #     self.halfmove_clock += 1
        
    #     # --- INCREMENTAL HASHING FOR NULLMOVE ---
        
    #     # 1. XOR OUT Side Key (turn always flips)
    #     self.hash ^= SIDE_KEY
        
    #     # 2. XOR OUT OLD EP Key (EP square is always cleared)
    #     if self.ep != -1:
    #         self.hash ^= EP_KEYS[self.ep & 7]
            
    #     self.ep = -1 
        
    #     # 3. Apply state changes
    #     self.white_to_move = not self.white_to_move

    def unmake_move(self):
        if not self.stack: return
        # The saved hash is restored directly
        P, piece_map, wtm, castle, ep, hc, hash = self.stack.pop()
        self.P = P # Restores all pieces
        self.piece_map = piece_map
        self.white_to_move = wtm
        self.castle = castle
        self.ep = ep
        self.halfmove_clock = hc
        self.hash = hash # Restores the hash

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
    def gen_legal_moves(self, active=False):
        moves = []
        for mv in self.gen_pseudo_legal():
            self.make_move(mv)
            # Check for legality (King is not in check after move)
            if not self.in_check(False) and (not active or mv[3] or mv[2]): moves.append(mv)
                    
            self.unmake_move()
        return moves

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
                        for p in ('q','r','b','n'): yield (sq, sq+8, p, None, 'p')
                    else:
                        yield (sq, sq+8, None, None, 'p')
                        if sq//8 == 1 and not (occ & get_bit(sq+16)):
                            yield (sq, sq+16, None, None, 'p')
                # captures
                for t in (sq+7, sq+9):
                    if 0<=t<64:
                        if (PAWN_ATK_WHITE[sq] & get_bit(t)) and (their & get_bit(t)):
                            if sq//8 == 6:
                                for p in ('q','r','b','n'): yield (sq,t,p,  self.piece_on(t), 'p')
                            else: yield (sq,t,None,  self.piece_on(t), 'p')
                # ep
                if self.ep != -1:
                    if PAWN_ATK_WHITE[sq] & get_bit(self.ep):
                        yield (sq,self.ep,None,'p', 'p')
            else:
                if not (occ & get_bit(sq-8)) and sq//8 > 0:
                    if sq//8 == 1:
                        for p in ('q','r','b','n'): yield (sq, sq-8, p, None, 'p')
                    else:
                        yield (sq, sq-8, None, None, 'p')
                        if sq//8 == 6 and not (occ & get_bit(sq-16)):
                            yield (sq, sq-16, None, None, 'p')
                for t in (sq-7, sq-9):
                    if 0<=t<64:
                        if (PAWN_ATK_BLACK[sq] & get_bit(t)) and (their & get_bit(t)):
                            if sq//8 == 1:
                                for p in ('q','r','b','n'): yield (sq,t,p,  self.piece_on(t), 'p')
                            else: yield (sq,t,None,  self.piece_on(t), 'p')
                if self.ep != -1:
                    if PAWN_ATK_BLACK[sq] & get_bit(self.ep):
                        yield (sq,self.ep,None,'p', 'p')
        # knights
        knights = self.P[self.side_index(us,1)]
        while knights:
            knights, sq = pop_lsb(knights)
            atk = KNIGHT_ATK[sq] & ~our
            bb = atk
            while bb:
                bb, t = pop_lsb(bb)
                yield (sq,t,None,  self.piece_on(t), 'n')
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
                    yield (sq,s,None,  self.piece_on(s), 'b')
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
                    yield (sq,s,None,  self.piece_on(s), 'r')
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
                    yield (sq,s,None,  self.piece_on(s), 'q')
                    if m & their: break
        # king
        ksq = self.king_square(us)
        if 0 <= ksq < 64:
            for t_bb in (KING_ATK[ksq] & ~our,):
                bb = t_bb
                while bb:
                    bb, t = pop_lsb(bb)
                    yield (ksq,t,None,  self.piece_on(t), 'k')
            # castling (basic tests: empty squares + not attacked)
            if us:
                # white king e1=4
                if (self.castle & 1) and not (occ & (get_bit(5)|get_bit(6))):
                    # ensure no squares attacked f1/e1/g1
                    if not self.attacked(4, False) and not self.attacked(5,False) and not self.attacked(6,False):
                        yield (4,6,None, None, 'k')
                if (self.castle & 2) and not (occ & (get_bit(1)|get_bit(2)|get_bit(3))):
                    if not self.attacked(4,False) and not self.attacked(3,False) and not self.attacked(2,False):
                        yield (4,2,None, None, 'k')
            else:
                if (self.castle & 4) and not (occ & (get_bit(61)|get_bit(62))):
                    if not self.attacked(60, True) and not self.attacked(61,True) and not self.attacked(62,True):
                        yield (60,62,None, None, 'k')
                if (self.castle & 8) and not (occ & (get_bit(57)|get_bit(58)|get_bit(59))):
                    if not self.attacked(60,True) and not self.attacked(59,True) and not self.attacked(58,True):
                        yield (60,58,None, None, 'k')

    # def doubled_pawns(self, pawns):
    #     score = 0
    #     for file in range(8):
    #         mask = 0x0101010101010101 << file
    #         count = (pawns & mask).bit_count()
    #         if count > 1:
    #             score -= (count - 1) * 15
    #     return score
    
    # def isolated_pawns(self, pawns):
    #     score = 0
    #     for file in range(8):
    #         mask = 0x0101010101010101 << file
    #         if pawns & mask:
    #             left = (mask >> 1) & 0x7F7F7F7F7F7F7F7F
    #             right = (mask << 1) & 0xFEFEFEFEFEFEFEFE
    #             if (pawns & (left | right)) == 0:
    #                 score -= 15
    #     return score

    # def passed_pawns(self, white):
    #     wp = self.P[0]
    #     bp = self.P[6]
    #     score = 0
    #     bb = wp if white else bp
    #     ebb = bp if white else wp
    #     while bb:
    #         bb, sq = pop_lsb(bb)
    #         file = sq % 8
    #         rank = sq // 8
    #         mask = 0
    #         for f in (file-1, file, file+1):
    #             if 0 <= f < 8:
    #                 r_range = range(rank+1, 8) if white else range(0, rank)
    #                 for r in r_range:
    #                     mask |= get_bit(r*8 + f)
    #         if ebb & mask == 0:
    #             if white:
    #                 score += (rank * 10 + 20)  # stronger closer to promotion
    #             else:
    #                 score += ((7-rank) * 10 + 20)
    #     return score

    # def eval_pawn_structure(self):
    #     wp =  self.P[0]
    #     bp =  self.P[6]
        
    #     return (
    #         self.doubled_pawns(wp) - self.doubled_pawns(bp)
    #         + self.isolated_pawns(wp) - self.isolated_pawns(bp)
    #         + self.passed_pawns(True) - self.passed_pawns(False)
    #     )

    # def king_safety(self, white):
    #     k = self.king_square(white)
    #     file = k % 8
    #     rank = k // 8

    #     direction = 1 if white else -1
    #     bb = 0 if white else 6 # Pawn bitboard index
        
    #     # Castle masks: 1 = White K-side, 2 = White Q-side, 4 = Black K-side, 8 = Black Q-side
    #     castle_mask_k_side = 1 if white else 4 # Mask for King-side castle
    #     castle_mask_q_side = 2 if white else 8 # Mask for Queen-side castle

    #     shield = 0
        
    #     # 1. Pawn Shield Calculation (FIXED for boundary errors)
    #     # squares in front of king (rank + direction)
    #     for df in (-1, 0, 1):
    #         f = file + df
    #         r = rank + direction # Calculate the new rank

    #         # Ensure both file (f) and rank (r) are ON THE BOARD (0-7)
    #         if 0 <= f < 8 and 0 <= r < 8:
    #             sq = r * 8 + f
                
    #             # Check for friendly pawns in the protective zone
    #             if self.P[bb] & get_bit(sq):  
    #                 shield += 10 # Bonus for a pawn shield
                    
    #     # 2. King Location/Castling Bonuses
        
    #     # A. Bonus for having successfully castled (King on g1/g8 or c1/c8)
    #     # This is a strong proxy for safety, rewarding a closed King position.
    #     if (white and k in (6, 2)) or (not white and k in (62, 58)):
    #         shield += 15
            
    #     # B. Penalty for lost castling rights (Using the castle masks)
    #     # If the side *cannot* castle, it usually means the king has moved or 
    #     # a rook was captured/moved, leading to potential danger.
        
    #     # Check if Kingside castling rights are LOST (mask & self.castle == 0)
    #     if (self.castle & castle_mask_k_side) == 0:
    #         shield -= 10
            
    #     # Check if Queenside castling rights are LOST
    #     if (self.castle & castle_mask_q_side) == 0:
    #         shield -= 5 # Queenside is often less critical
            
    #     return shield

    # def eval_king_safety(self):
    #     return self.king_safety(True) - self.king_safety(False)

    def eval_material(self):
        score = 0
        for idx, bb in enumerate(self.P):
            if bb == 0:
                continue
            piece_char = IDX_TO_PIECE[idx]
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

    def evaluate(self):
        score = self.eval_material()
        # score += self.king_safety(True) - self.king_safety(False)
        
        # wp =  self.P[0]
        # bp =  self.P[6]
        
        # score += self.doubled_pawns(wp) - self.doubled_pawns(bp)
        # score += self.isolated_pawns(wp) - self.isolated_pawns(bp)
        # score += self.passed_pawns(True) - self.passed_pawns(False)
        
        score += self.eval_position()

        return score if self.white_to_move else -score

    def score_move(self, t_move):
        g_score = 0
        if t_move[3]:
            # MVV-LVA: Most valuable victim - least valuable attacker
            g_score += self.PIECE_VALUES[t_move[3]] - self.PIECE_VALUES[t_move[4]] / 10
        if t_move[2]:
            # Promote to queen highest
            g_score += self.PIECE_VALUES[t_move[2]] * 10
        return g_score

    def piece_on(self, sq):
        idx = self.piece_map[sq]
        return IDX_TO_PIECE[idx] if idx != -1 else None

    def move_to_uci(self, mv):
        base = (FILES[mv[0] % 8] + RANKS[mv[0] // 8]) + (FILES[mv[1] % 8] + RANKS[mv[1] // 8])
        if mv[2]:
            return base + mv[2]
        return base
    
    #remove
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
    #endremove
    
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
        
        wp =  self.P[0]
        bp =  self.P[6]
        
        dp_score = self.doubled_pawns(wp) - self.doubled_pawns(bp)
        ip_score = self.isolated_pawns(wp) - self.isolated_pawns(bp)
        pp_score = self.passed_pawns(True) - self.passed_pawns(False)
        
        pos_score = self.eval_position()
        
        print(f"Turn: {('W' if self.white_to_move else 'B')} 50c: {self.halfmove_clock} Score: {score} Check: {self.in_check()}  Rev: Check: {self.in_check(False)}")
        print(f"Mat: {mat_score} King: {king_score} DP: {dp_score} IP: {ip_score} PP: {pp_score} Pos: {pos_score}")
        print(f"Fen: {self.get_fen()}")
    #endremove