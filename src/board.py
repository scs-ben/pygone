import random
# from typing import Tuple

# U64 = int
# SQ = int
# Move = Tuple[int,int,str,str,str]  # from, to, promotion or None, capture or None, piece moving

# --- helpers --------------------------------------------------------------
FILES = "abcdefgh"
RANKS = "12345678"
IDX_TO_PIECE = ['p','n','b','r','q','k','p','n','b','r','q','k']
# START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# --- utilities -------------------------------------------------------------
MASK = [(1 << i) for i in range(64)]
def get_bit(s): return 1 << s
def lsb_index(bb):
    return (bb & -bb).bit_length() - 1
def pop_lsb(bb):
    lsb = bb & -bb
    idx = lsb.bit_length() - 1
    return bb ^ lsb, idx

# --- board constants ------------------------------------------------------
AFILE = 0x0101010101010101
HFILE = 0x8080808080808080
RANK1 = 0xFF
RANK8 = RANK1 << (7*8)

# direction offsets in square index (used for ray walking)
N, S, E, W, NE, NW, SE, SW = 8, -8, 1, -1, 9, 7, -7, -9
DIRS_ROOK = (N,S,E,W)
DIRS_BISHOP = (NE,NW,SE,SW)

# --- precomputed non-slider attacks --------------------------------------
KNIGHT_DELTAS = (17,15,10,6,-6,-10,-15,-17)
KING_DELTAS   = (1,-1,8,-8,9,7,-7,-9)

KNIGHT_ATK = [0]*64
KING_ATK   = [0]*64
PAWN_ATK_WHITE = [0]*64
PAWN_ATK_BLACK = [0]*64

for sq in range(64):
    r = sq//8; f = sq%8
    # knight
    bm = 0
    for d in KNIGHT_DELTAS:
        ns = sq + d
        if 0 <= ns < 64:
            rr = ns//8; ff = ns%8
            if abs(rr-r)+abs(ff-f) == 3: bm |= get_bit(ns)
    KNIGHT_ATK[sq] = bm
    # king
    bm = 0
    for d in KING_DELTAS:
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
    
    def __init__(self, fen = None):
        # piece bitboards: WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK
        self.P = [0]*12
        self.white_to_move = True
        self.castle = 0  # bits: wk(1), wq(2), bk(4), bq(8)
        self.ep = -1
        self.halfmove_clock = 0
        # state stack for unmake
        self.stack = []
        self.P = [65280, 66, 36, 129, 8, 16, 71776119061217280, 4755801206503243776, 2594073385365405696, 9295429630892703744, 576460752303423488, 1152921504606846976]
        # if fen:
        #     self.set_fen(fen)
        # else:
        #     self.set_fen(START_FEN)

        self.compute_hash()

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

    # def set_fen(self, fen):
    #     parts = fen.split()
    #     rows = parts[0].split('/')
    #     self.P = [0]*12
    #     for r, row in enumerate(rows):
    #         sq = (7-r)*8
    #         for ch in row:
    #             if ch.isdigit(): sq += int(ch); continue
    #             piece_map = {'P':0,'N':1,'B':2,'R':3,'Q':4,'K':5,
    #                          'p':6,'n':7,'b':8,'r':9,'q':10,'k':11}
    #             idx = piece_map[ch]
    #             self.P[idx] |= get_bit(sq)
    #             sq += 1
    #     self.white_to_move = (parts[1] == 'w')
    #     self.castle = 0
    #     if 'K' in parts[2]: self.castle |= 1
    #     if 'Q' in parts[2]: self.castle |= 2
    #     if 'k' in parts[2]: self.castle |= 4
    #     if 'q' in parts[2]: self.castle |= 8
    #     self.ep = -1 if parts[3] == '-' else self.algebraic_to_sq(parts[3])
    #     # ignore halfmove/fullmove counters

    # make/unmake minimal for legality checking
    def make_move(self, mv):
        frm, to, promo, _, _ = mv
        # save state
        self.stack.append((self.P[:], self.white_to_move, self.castle, self.ep, self.halfmove_clock, self.hash))
        
        self.halfmove_clock += 1
        
        if mv[3] or mv[4] == 'p':
            self.halfmove_clock = 0
            
        
        us = self.white_to_move
        # find moving piece type
        from_mask = get_bit(frm); to_mask = get_bit(to)
        moved_piece = None
        for p in range(6):
            idx = self.side_index(us,p)
            if self.P[idx] & from_mask:
                moved_piece = p; self.P[idx] ^= from_mask; break
        # capture (including en-passant)
        captured = False
        if moved_piece is None:
            # sanity
            return
        # en-passant capture
        if moved_piece == 0 and to == self.ep:
            captured = True
            if us:
                cap_sq = to - 8
            else:
                cap_sq = to + 8
            # remove enemy pawn
            self.P[self.side_index(not us, 0)] ^= get_bit(cap_sq)
        else:
            # capture any piece on 'to'
            for p in range(6):
                idx = self.side_index(not us, p)
                if self.P[idx] & to_mask:
                    self.P[idx] ^= to_mask; captured = True; break
        # place moved piece (promotion?)
        if promo:
            prom_map = {'q':4,'r':3,'b':2,'n':1}
            self.P[self.side_index(us, prom_map[promo])] |= to_mask
        else:
            self.P[self.side_index(us, moved_piece)] |= to_mask
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
        # white king-side: e1(4)->g1(6) move rook h1->f1
        if moved_piece==5 and us and frm==4 and to==6:
            self.P[self.side_index(us,3)] ^= get_bit(7); self.P[self.side_index(us,3)] |= get_bit(5)
        # white queen-side
        if moved_piece==5 and us and frm==4 and to==2:
            self.P[self.side_index(us,3)] ^= get_bit(0); self.P[self.side_index(us,3)] |= get_bit(3)
        # black castling
        if moved_piece==5 and (not us) and frm==60 and to==62:
            self.P[self.side_index(us,3)] ^= get_bit(63); self.P[self.side_index(us,3)] |= get_bit(61)
        if moved_piece==5 and (not us) and frm==60 and to==58:
            self.P[self.side_index(us,3)] ^= get_bit(56); self.P[self.side_index(us,3)] |= get_bit(59)
        # en-passant target update
        if moved_piece == 0 and abs(to - frm) == 16:
            # pawn double push
            self.ep = (frm + to)//2
        else:
            self.ep = -1
        # switch side
        self.white_to_move = not self.white_to_move
        
        self.compute_hash()

    def unmake_move(self):
        if not self.stack: return
        P, wtm, castle, ep, hc, hash = self.stack.pop()
        self.P = P
        self.white_to_move = wtm
        self.castle = castle
        self.ep = ep
        self.halfmove_clock = hc
        self.hash = hash

    # attack detection
    def attacked(self, sq, by_white):
        occ = self.all_occupied()
        # pawn
        if by_white:
            if PAWN_ATK_WHITE[sq] & self.P[self.side_index(True,0)]: return True
        else:
            if PAWN_ATK_BLACK[sq] & self.P[self.side_index(False,0)]: return True
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
                s = ns
                m = get_bit(s)
                if m & occ:
                    # stopped on piece
                    if m & (self.P[self.side_index(by_white,3)] | self.P[self.side_index(by_white,4)]):
                        return True
                    break
        for d in DIRS_BISHOP:
            s = sq
            while True:
                ns = s + d
                if ns < 0 or ns >= 64: break
                # file wrap
                if d in (NE,SE) and ns%8 == 0: break
                if d in (NW,SW) and ns%8 == 7: break
                s = ns
                m = get_bit(s)
                if m & occ:
                    if m & (self.P[self.side_index(by_white,2)] | self.P[self.side_index(by_white,4)]):
                        return True
                    break
        return False

    def king_square(self, white):
        bb = self.P[self.side_index(white,5)]
        if bb: return (bb & -bb).bit_length()-1
        return -1
    
    def in_check(self, white=True):
        if white:
            ksq = self.king_square(self.white_to_move)
            return self.attacked(ksq, not self.white_to_move)
        else:
            ksq = self.king_square(not self.white_to_move)
            return self.attacked(ksq, self.white_to_move)

    # --- move generation -------------------------------------------------
    def gen_legal_moves(self, active=False):
        moves = []
        for mv in self.gen_pseudo_legal():
            self.make_move(mv)
            if not self.in_check():
                if not active or mv[3]:
                    moves.append(mv)
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
    #     bb = 0 if white else 6
    #     castle = 1 if white else 4

    #     shield = 0
    #     # squares in front of king (rank+1)
    #     for df in (-1, 0, 1):
    #         f = file + df
    #         if 0 <= f < 8:
    #             sq = (rank + direction) * 8 + f
    #             if self.P[bb] & get_bit(sq):  # white pawns
    #                 shield += 10
    #     # bonus for castling
    #     if self.castle & castle == 0 and self.castle & (castle * 2) == 0:
    #         shield += 15
    #     return shield

    # def eval_king_safety(self):
    #     return self.king_safety(True) - self.king_safety(False)

    def eval_material(self):
        score = 0
        for idx, bb in enumerate(self.P):
            if bb == 0:
                continue
            piece_char = 'pnbrqk'[idx % 6]
            val = self.PIECE_VALUES[piece_char]
            # population count
            cnt = bb.bit_count()
            if idx < 6:   # white piece
                score += val * cnt
            else:         # black piece
                score -= val * cnt
        return score

    def evaluate(self):
        score  = self.eval_material()
        # score += self.eval_pawn_structure()
        # score += self.eval_king_safety()

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
        m = 1 << sq
        for idx, bb in enumerate(self.P):
            if bb & m:
                return IDX_TO_PIECE[idx]   # always lowercase
        return None

    def algebraic_to_sq(self, s:str):
        return FILES.index(s[0]) + 8*int(s[1])-8

    def sq_to_uci(self, sq):
        return FILES[sq % 8] + RANKS[sq // 8]

    def move_to_uci(self, mv):
        frm, to, promo, _, _ = mv
        base = self.sq_to_uci(frm) + self.sq_to_uci(to)
        if promo:
            return base + promo.lower()
        return base