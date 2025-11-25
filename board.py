#!/usr/bin/env python3
#  pygone - A Python Chess Engine
#  Copyright (C) 2025 [Your Name/Handle]
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 30, 30, 15,  5,-30,
    -30,  5, 15, 30, 30, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50 
]
PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,   # Rank 1
     5, 10, 10,-20,-20, 10, 10,  5,   # Rank 2
     5, -5,-10,  0,  0,-10, -5,  5,   # Rank 3
     0,  0,  0, 20, 20,  0,  0,  0,   # Rank 4
     5,  5, 10, 25, 25, 10,  5,  5,   # Rank 5
    10, 10, 20, 30, 30, 20, 10, 10,   # Rank 6
    50, 50, 50, 50, 50, 50, 50, 50,   # Rank 7
     0,  0,  0,  0,  0,  0,  0,  0    # Rank 8
]
PST_WEIGHTS = [1, 2, 2, 1, 1, 0]

CENTER_SCORE = [
    -17,-17,-17,-17,-17,-17,-17,-17,
    -17,-12,-12,-12,-12,-12,-17,-17,
    -17,-12, -7, -7, -7, -7,-12,-17,
    -17,-12, -7, -2, -2, -7,-12,-17,
    -17,-12, -7, -2, -2, -7,-12,-17,
    -17,-12, -7, -7, -7, -7,-12,-17,
    -17,-12,-12,-12,-12,-12,-17,-17,
    -17,-17,-17,-17,-17,-17,-17,-17
]

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
            if abs(rr-r)+abs(ff-f) == 3: bm |= (1 << ns)
    KNIGHT_ATK[sq] = bm
    # king
    bm = 0
    # King deltas
    for d in (1,-1,8,-8,9,7,-7,-9):
        ns = sq + d
        if 0 <= ns < 64:
            rr = ns//8; ff = ns%8
            if max(abs(rr-r), abs(ff-f)) == 1: bm |= (1 << ns)
    KING_ATK[sq] = bm
    # pawn attacks
    bm_w = 0
    if f>0 and r<7: bm_w |= (1 << (sq+7))
    if f<7 and r<7: bm_w |= (1 << (sq+9))
    PAWN_ATK_WHITE[sq] = bm_w
    bm_b = 0
    if f>0 and r>0: bm_b |= (1 << (sq-9))
    if f<7 and r>0: bm_b |= (1 << (sq-7))
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
        self.score_mat = 0
        self.score_pst = 0
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
    def recompute_evaluation(self):
        self.score_mat = 0
        self.score_pst = 0
        
        for i in range(12):
            bb = self.P[i]
            while bb:
                lsb = bb & -bb
                sq = lsb.bit_length() - 1
                bb ^= lsb
                m,p = self._get_piece_val(i, sq)
                self.score_mat += m
                self.score_pst += p
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
        h ^= CASTLING_KEYS[self.castle]   # 0-15

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
                self.P[idx] |= (1 << sq)
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
        
        self.recompute_evaluation()
    #UNITendremove

    def algebraic_to_sq(self, s:str):
        return FILES.index(s[0]) + 8*int(s[1])-8

    def _x(self, i, s):
        self.P[i] ^= (1 << s)
        self.hash ^= PIECE_KEYS[i][s]

    # make/unmake minimal for legality checking
    def make_move(self, mv):
        # 1. CACHE OLD STATE
        old_ep, old_castle, old_clock, old_hash, old_mat, old_pst = self.ep, self.castle, self.halfmove_clock, self.hash, self.score_mat, self.score_pst

        # --- NULL MOVE HANDLING ---
        if not mv:
            # Toggle side in hash
            self.hash ^= SIDE_KEY
            
            # Clear EP in hash and state
            if self.ep != -1:
                self.hash ^= EP_KEYS[self.ep & 7]
                self.ep = -1
            
            self.white_to_move = not self.white_to_move
            
            # Push null-move state to stack (mv is None)
            self.stack.append((None, -1, False, old_ep, old_castle, old_clock, old_hash, old_mat, old_pst))
            return
        # --------------------------

        frm, to, promo, _, _, _ = mv
        us = self.white_to_move

        # 2. IDENTIFY MOVING PIECE
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
            
        m,p = self._get_piece_val(moved_piece_idx, frm); self.score_mat -= m; self.score_pst -= p
                
        # 3. HANDLE CAPTURES & EN PASSANT
        captured_idx = -1
        is_ep_capture = False
        
        if moved_piece_type == 0 and to == self.ep:
            is_ep_capture = True
            cap_sq = to - 8 if us else to + 8
            captured_idx = self.side_index(not us, 0)
            
            m,p = self._get_piece_val(captured_idx, cap_sq); self.score_mat -= m; self.score_pst -= p
            
            # USE HELPER: Remove EP Pawn
            self._x(captured_idx, cap_sq) 
            self.piece_map[cap_sq] = -1
        else:
            for p in range(6):
                e_idx = self.side_index(not us, p)
                if self.P[e_idx] & to_mask:
                    captured_idx = e_idx
                    
                    m,p = self._get_piece_val(captured_idx, to); self.score_mat -= m; self.score_pst -= p
                    
                    # USE HELPER: Remove Captured Piece
                    self._x(e_idx, to) 
                    break
        
        # 4. PUSH TO STACK
        # (Assuming you are using the optimized stack from previous steps)
        self.stack.append((mv, captured_idx, is_ep_capture, old_ep, old_castle, old_clock, old_hash, old_mat, old_pst))

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
        
        m,p = self._get_piece_val(target_idx, to); self.score_mat += m; self.score_pst += p

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
            
            m,p = self._get_piece_val(rook_idx, r_from); self.score_mat -= m; self.score_pst -= p
            m,p = self._get_piece_val(rook_idx, r_to); self.score_mat += m; self.score_pst += p
            
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
        mv, c_idx, is_ep, self.ep, self.castle, self.halfmove_clock, self.hash, self.score_mat, self.score_pst = self.stack.pop()
        
        self.white_to_move = not self.white_to_move
        
        # --- NULL MOVE HANDLING ---
        if not mv: return # State variables restored above, no pieces to move
        # --------------------------

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
        # 1. Pawns, Knights, Kings (Step Pieces)
        # Note: side_index(True, 0) is White Pawn (0), False is Black Pawn (6)
        if by_white:
            if PAWN_ATK_BLACK[sq] & self.P[0]: return True
        else:
            if PAWN_ATK_WHITE[sq] & self.P[6]: return True
            
        if KNIGHT_ATK[sq] & self.P[self.side_index(by_white, 1)]: return True
        if KING_ATK[sq] & self.P[self.side_index(by_white, 5)]: return True
        
        # 2. Sliders (Merged Logic)
        occ = self.all_occupied()
        
        # Define attacker groups: (Directions, Bitboard of attackers)
        # Rooks (3) + Queens (4) use Rook Dirs
        # Bishops (2) + Queens (4) use Bishop Dirs
        sliders = [
            (DIRS_ROOK, self.P[self.side_index(by_white, 3)] | self.P[self.side_index(by_white, 4)]),
            (DIRS_BISHOP, self.P[self.side_index(by_white, 2)] | self.P[self.side_index(by_white, 4)])
        ]

        for dirs, attackers in sliders:
            for d in dirs:
                s = sq
                while True:
                    s += d
                    # Bounds Check
                    if s < 0 or s >= 64: break
                    # File Wrap Check
                    if abs((s - d) % 8 - s % 8) > 1: break
                    
                    bit = 1 << s
                    if bit & attackers: return True
                    if bit & occ: break
                    
        return False

    def king_square(self, white):
        bb = self.P[self.side_index(white,5)]
        return (bb & -bb).bit_length()-1 if bb else -1
    
    def in_check(self, white=True):
        return self.attacked(self.king_square(self.white_to_move), not self.white_to_move) if white else self.attacked(self.king_square(not self.white_to_move), self.white_to_move)

    # --- move generation -------------------------------------------------
    def gen_pseudo_legal(self, active=False):
        moves = []
        us = self.white_to_move
        occ = self.all_occupied()
        our = self.pieces_of(us)
        their = self.pieces_of(not us)
        
        # Target masks
        step_targets = their if active else ~our
        
        # --- PAWNS ---
        pawns = self.P[self.side_index(us, 0)]
        
        # Direction & Promotion Rank
        push = 8 if us else -8
        promo_rank = 6 if us else 1
        start_rank = 1 if us else 6
        
        # Pawn Attacks (Pre-calculated directions)
        atk_left = 7 if us else -9
        atk_right = 9 if us else -7
        
        while pawns:
            lsb = pawns & -pawns
            sq = lsb.bit_length() - 1
            pawns ^= lsb
            
            rank = sq // 8
            
            # 1. Pushes
            tgt = sq + push
            if not (occ & (1 << tgt)):
                is_promo = (rank == promo_rank)
                
                if is_promo:
                    # Always generate promotions (active or not)
                    # Score: Promo Value + Center
                    base = CENTER_SCORE[tgt]
                    moves.append((9000 + base, (sq, tgt, 'q', None, 'p', False)))
                    moves.append((5000 + base, (sq, tgt, 'r', None, 'p', False)))
                    moves.append((3300 + base, (sq, tgt, 'b', None, 'p', False)))
                    moves.append((3200 + base, (sq, tgt, 'n', None, 'p', False)))
                elif not active:
                    # Quiet Push
                    score = CENTER_SCORE[tgt]
                    moves.append((score, (sq, tgt, None, None, 'p', False)))
                    
                    # Double Push
                    if rank == start_rank:
                        tgt2 = sq + (push * 2)
                        if not (occ & (1 << tgt2)):
                            score = CENTER_SCORE[tgt2]
                            moves.append((score, (sq, tgt2, None, None, 'p', False)))

            # 2. Captures
            for diff in (atk_left, atk_right):
                tgt = sq + diff
                # Check board bounds for attack diagonal
                # (Simple check: file diff must be 1)
                if not (0 <= tgt < 64): continue
                if abs((sq % 8) - (tgt % 8)) != 1: continue
                
                tgt_bit = 1 << tgt
                if their & tgt_bit:
                    # Capture
                    victim_char = self.piece_on(tgt)
                    victim_val = self.PIECE_VALUES[victim_char] if victim_char else 0
                    
                    # MVV/LVA: Victim * 100 - Attacker (Pawn=100)
                    score = (victim_val * 100) - 100 + CENTER_SCORE[tgt]
                    
                    if rank == promo_rank:
                        # Capture + Promo = Huge Score
                        moves.append((score + 9000, (sq, tgt, 'q', victim_char, 'p', False)))
                        moves.append((score + 5000, (sq, tgt, 'r', victim_char, 'p', False)))
                        moves.append((score + 3300, (sq, tgt, 'b', victim_char, 'p', False)))
                        moves.append((score + 3200, (sq, tgt, 'n', victim_char, 'p', False)))
                    else:
                        moves.append((score, (sq, tgt, None, victim_char, 'p', False)))

                # 3. En Passant
                elif self.ep == tgt:
                    # MVV/LVA: Victim(Pawn=100) * 100 - Attacker(100) = 9900 (+ Center)
                    score = 9900 + CENTER_SCORE[tgt] 
                    moves.append((score, (sq, tgt, None, 'p', 'p', False)))

        # --- KNIGHTS ---
        knights = self.P[self.side_index(us, 1)]
        while knights:
            lsb = knights & -knights
            sq = lsb.bit_length() - 1
            knights ^= lsb
            
            attacks = KNIGHT_ATK[sq] & step_targets
            while attacks:
                lsb_atk = attacks & -attacks
                tgt = lsb_atk.bit_length() - 1
                attacks ^= lsb_atk
                
                victim_char = self.piece_on(tgt)
                if victim_char:
                    score = (self.PIECE_VALUES[victim_char] * 100) - 320 + CENTER_SCORE[tgt]
                else:
                    score = CENTER_SCORE[tgt]
                
                moves.append((score, (sq, tgt, None, victim_char, 'n', False)))

        # --- SLIDERS (Bishops, Rooks, Queens) ---
        # Helper lists
        sliders = [
            (2, DIRS_BISHOP, 330, 'b'),
            (3, DIRS_ROOK, 500, 'r'),
            (4, DIRS_ROOK + DIRS_BISHOP, 900, 'q')
        ]
        
        for p_type, dirs, val_attacker, p_char in sliders:
            pieces = self.P[self.side_index(us, p_type)]
            while pieces:
                lsb = pieces & -pieces
                sq = lsb.bit_length() - 1
                pieces ^= lsb
                
                for d in dirs:
                    curr = sq
                    while True:
                        curr += d
                        if not (0 <= curr < 64): break
                        # Wrap check
                        if abs((curr - d) % 8 - curr % 8) > 1: break
                        
                        bit = 1 << curr
                        if our & bit: break
                        
                        victim_char = self.piece_on(curr)
                        if victim_char:
                            # Capture
                            score = (self.PIECE_VALUES[victim_char] * 100) - val_attacker + CENTER_SCORE[curr]
                            moves.append((score, (sq, curr, None, victim_char, p_char, False)))
                            break # Blocked by capture
                        elif not active:
                            # Quiet
                            score = CENTER_SCORE[curr]
                            moves.append((score, (sq, curr, None, None, p_char, False)))
                        # If active (QSearch) and empty, we continue ray but don't add move
                        elif active:
                            continue

        # --- KING ---
        ksq = self.king_square(us)
        if 0 <= ksq < 64:
            attacks = KING_ATK[ksq] & step_targets
            while attacks:
                lsb_atk = attacks & -attacks
                tgt = lsb_atk.bit_length() - 1
                attacks ^= lsb_atk
                
                victim_char = self.piece_on(tgt)
                if victim_char:
                     # King captures are risky but valuable if safe; simple MVV/LVA here
                    score = (self.PIECE_VALUES[victim_char] * 100) + CENTER_SCORE[tgt]
                else:
                    score = CENTER_SCORE[tgt]
                
                moves.append((score, (ksq, tgt, None, victim_char, 'k', False)))

            # --- CASTLING ---
            if not active:
                if us:
                    if (self.castle & 1) and not (occ & 96): # 96 = f1(32)+g1(64)
                        if not self.attacked(4, False) and not self.attacked(5,False) and not self.attacked(6,False):
                            moves.append((500, (4, 6, None, None, 'k', True)))
                    if (self.castle & 2) and not (occ & 14): # 14 = b1(2)+c1(4)+d1(8)
                        if not self.attacked(4,False) and not self.attacked(3,False) and not self.attacked(2,False):
                            moves.append((500, (4, 2, None, None, 'k', True)))
                else:
                    if (self.castle & 4) and not (occ & (6917529027641081856)): # f8+g8
                        if not self.attacked(60, True) and not self.attacked(61,True) and not self.attacked(62,True):
                            moves.append((500, (60, 62, None, None, 'k', True)))
                    if (self.castle & 8) and not (occ & 1008806316530991104): # b8+c8+d8
                        if not self.attacked(60,True) and not self.attacked(59,True) and not self.attacked(58,True):
                            moves.append((500, (60, 58, None, None, 'k', True)))
        return moves

    def eval_king(self, white):
        k = self.king_square(white)
        f, r = k % 8, k // 8
        d, bb = (1, 0) if white else (-1, 6) 
        
        # 1. Pawn Shield (Defending pawns in front of King)
        # Using generator to save space
        pawn_shield = 10 * sum(
            1 for df in (-1, 0, 1) 
            if 0 <= (nf := f + df) < 8 
            and 0 <= (nr := r + d) < 8
            and (self.P[bb] & (1 << (nr * 8 + nf)))
        )
        
        # 2. Castling Bonus (Huge incentive to castle)
        # King on g/c file (castled positions) gets +60
        castle_pos_score = 0
        if (white and k in (6, 2)) or (not white and k in (62, 58)):
            castle_pos_score += 60
            
        # Penalties for losing rights (remains small)
        if not (self.castle & (1 if white else 4)): castle_pos_score -= 10
        if not (self.castle & (2 if white else 8)): castle_pos_score -= 5
        
        return pawn_shield + castle_pos_score

    def _get_piece_val(self, i, s):
        p = i % 6
        # Flip square for black (i>=6)
        t = s if i < 6 else s ^ 56
        
        # Compact PST logic: Rooks use rank check, others use tables
        # (t >> 3 == 6) is the same as (t // 8 == 6)
        v = 20 * (t >> 3 == 6) if p == 3 else (PAWN_PST if p == 0 else UNIFIED_PST)[t]
        
        m = self.PIECE_VALUES[IDX_TO_PIECE[p]]
        z = v * PST_WEIGHTS[p] // 2
        
        # Return tuple with correct sign
        return (m, z) if i < 6 else (-m, -z)

    def pawn_structure_score(self, pawns):
        # 1. Collapse all pawns to Rank 1 (bits 0-7) to find occupied files
        # We "smear" the bits down: Rank 8->4, then 4->2, then 2->1.
        x = pawns
        x |= x >> 32
        x |= x >> 16
        x |= x >> 8
        file_occ = x & 0xFF  # 8 bits, 1 if file has ANY pawn, 0 otherwise

        # 2. Doubled Pawns Calculation
        # Original Logic: for every file, penalty = (pawn_count - 1) * 15
        # Bitwise Logic: (Total Pawns - Count of Occupied Files) * 15
        # Example: 3 pawns on A-file. bit_count=3, file_occ=1. (3-1) = 2 penalties. Matches.
        doubled_penalty = (pawns.bit_count() - file_occ.bit_count()) * 15

        # 3. Isolated Pawns Calculation
        # A file is isolated if it is occupied (file_occ) but its neighbors (left/right) are empty.
        # We project neighbor occupancy onto the current file slots.
        neighbor_occ = (file_occ << 1) | (file_occ >> 1)
        
        # Isolated = Occupied AND NOT Neighbor_Occupied
        isolated_mask = file_occ & ~neighbor_occ
        
        isolated_penalty = isolated_mask.bit_count() * 15

        return -(doubled_penalty + isolated_penalty)
    
    def is_insufficient_material(self):
        # 1. If any Pawns, Rooks, or Queens exist, it's not insufficient.
        # White Pawns(0) | Black Pawns(6) | W Rooks(3) | W Queens(4) | B Rooks(9) | B Queens(10)
        if (self.P[0] | self.P[6] | self.P[3] | self.P[4] | self.P[9] | self.P[10]):
            return False
        
        # 2. If we are here, only Kings, Knights, and Bishops remain.
        # Calculate total minor pieces.
        # W Knights(1) | W Bishops(2) | B Knights(7) | B Bishops(8)
        minors = (self.P[1] | self.P[2] | self.P[7] | self.P[8])
        
        # If no minors (K vs K) or only 1 minor total (K+N vs K), it's a draw.
        # We can use bit_count() since you already use it in pawn_structure_score
        if minors.bit_count() < 2:
            return True
        
        return False

    def evaluate(self):
        if self.is_insufficient_material() or self.halfmove_clock >= 100: return 0
        
        piece_count = self.all_occupied().bit_count()
        phase = min(1.0, max(0.0, (piece_count - 12) / 20.0))
        
        score = self.score_mat + int(self.score_pst * phase) + self.eval_king(True) - self.eval_king(False) + self.pawn_structure_score(self.P[0]) - self.pawn_structure_score(self.P[6])

        return score if self.white_to_move else -score

    def piece_on(self, sq):
        idx = self.piece_map[sq]
        return IDX_TO_PIECE[idx % 6] if idx != -1 else None

    def move_to_uci(self, mv):
        base = (FILES[mv[0] % 8] + RANKS[mv[0] // 8]) + (FILES[mv[1] % 8] + RANKS[mv[1] // 8])
        if mv[2]: return base + mv[2]
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
                bit = (1 << sq)
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
        
        mat_score = self.eval_score
        king_score = self.eval_king(True) - self.eval_king(False)
        
        pawn_score = self.pawn_structure_score(self.P[0]) - self.pawn_structure_score(self.P[6])

        print(f"Turn: {('W' if self.white_to_move else 'B')} 50c: {self.halfmove_clock} Score: {score} Check: {self.in_check()}  Rev: Check: {self.in_check(False)}")
        print(f"Mat: {mat_score} King: {king_score} Pawn: {pawn_score}")
        print(f"Fen: {self.get_fen()}")
    #endremove