#!/usr/bin/env python3
#  pygone - A Python Chess Engine
#  Copyright (C) 2026 scs-ben
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
    -30,  5, 15, 30, 30, 15,  5,-30
]
UNIFIED_PST += UNIFIED_PST[::-1]
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

CENTER_SCORE = [
    -17,-17,-17,-17,-17,-17,-17,-17,
    -17,-12,-12,-12,-12,-12,-17,-17,
    -17,-12, -7, -7, -7, -7,-12,-17,
    -17,-12, -7, -2, -2, -7,-12,-17
]
CENTER_SCORE += CENTER_SCORE[::-1]

# direction offsets in square index (used for ray walking)
DIRS_ROOK = (8, -8, 1, -1)
DIRS_BISHOP = (9, 7, -7, -9)


KNIGHT_ATK, KING_ATK, PAWN_ATK_WHITE, PAWN_ATK_BLACK = [[0]*64 for _ in range(4)]

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
            ff = ns%8
            if abs(ff-f) <= 1: bm |= (1 << ns)
    KING_ATK[sq] = bm
    # pawn attacks
    bm_w = 0
    if r<7:
        if f>0: bm_w |= (1 << (sq+7))
        if f<7: bm_w |= (1 << (sq+9))
    PAWN_ATK_WHITE[sq] = bm_w
    bm_b = 0
    if r>0:
        if f>0: bm_b |= (1 << (sq-9))
        if f<7: bm_b |= (1 << (sq-7))
    PAWN_ATK_BLACK[sq] = bm_b


ROOK_RAYS = []
BISHOP_RAYS = []
QUEEN_RAYS = []

for sq in range(64):
    r_rays = []
    for d in DIRS_ROOK:
        ray = []
        curr = sq
        while True:
            curr += d
            if not (0 <= curr < 64) or abs((curr - d) % 8 - curr % 8) > 1: break
            ray.append(curr)
        r_rays.append(tuple(ray))
    ROOK_RAYS.append(r_rays)

    b_rays = []
    for d in DIRS_BISHOP:
        ray = []
        curr = sq
        while True:
            curr += d
            if not (0 <= curr < 64) or abs((curr - d) % 8 - curr % 8) > 1: break
            ray.append(curr)
        b_rays.append(tuple(ray))
    BISHOP_RAYS.append(b_rays)

    QUEEN_RAYS.append(r_rays + b_rays)


random.seed(2025)  # deterministic

PIECE_KEYS = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
CASTLING_KEYS = [random.getrandbits(64) for _ in range(16)]
EP_KEYS = [random.getrandbits(64) for _ in range(8)]
SIDE_KEY = random.getrandbits(64)


PIECE_VAL_BY_IDX = [100, 320, 330, 500, 900, 0] * 2
FILE_MASKS = [0x0101010101010101 << i for i in range(8)]

# --- board class ----------------------------------------------------------
class Board:
    
    #UNITremove
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    #UNITendremove
    
    def __init__(self, fen = None):
        # piece bitboards: WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK
        self.piece_map = [3, 1, 2, 4, 5, 2, 1, 3] + [0]*8 + [-1]*32 + [6]*8 + [9, 7, 8, 10, 11, 8, 7, 9]
        self.white_to_move = True
        self.castle = 15  # bits: wk(1), wq(2), bk(4), bq(8)
        self.ep = -1
        self.halfmove_clock = 0
        self.eval_score = 0
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
        self.eval_score = 0
        
        for i in range(12):
            bb = self.P[i]
            while bb:
                lsb = bb & -bb
                sq = lsb.bit_length() - 1
                bb ^= lsb
                m = self._get_piece_val(i, sq)
                self.eval_score += m
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

    def algebraic_to_sq(self, s):
        return ord(s[0]) + 8 * ord(s[1]) - 489

    def _x(self, i, s):
        self.P[i] ^= (1 << s)
        self.hash ^= PIECE_KEYS[i][s]



    # make/unmake minimal for legality checking
    def make_move(self, mv):
        # 1. CACHE OLD STATE
        old_ep, old_castle, old_clock, old_hash, old_eval_score = self.ep, self.castle, self.halfmove_clock, self.hash, self.eval_score

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
            self.stack.append((None, -1, False, old_ep, old_castle, old_clock, old_hash, old_eval_score))
            return
        # --------------------------

        frm = mv & 63
        to = (mv >> 6) & 63
        promo_code = (mv >> 12) & 7
        us = self.white_to_move

        # 2. IDENTIFY MOVING PIECE
        moved_piece_idx = self.piece_map[frm]
        moved_piece_type = moved_piece_idx % 6

        self.eval_score -= self._get_piece_val(moved_piece_idx, frm)

        # 3. HANDLE CAPTURES & EN PASSANT
        captured_idx = -1
        is_ep_capture = False

        if moved_piece_type == 0 and to == self.ep:
            is_ep_capture = True
            cap_sq = to - 8 if us else to + 8
            captured_idx = 6 * us

            self.eval_score -= self._get_piece_val(captured_idx, cap_sq)

            # USE HELPER: Remove EP Pawn
            self._x(captured_idx, cap_sq)
            self.piece_map[cap_sq] = -1
        else:
            captured_idx = self.piece_map[to]
            if captured_idx != -1:
                self.eval_score -= self._get_piece_val(captured_idx, to)
                self._x(captured_idx, to)

        # 4. PUSH TO STACK
        self.stack.append((mv, captured_idx, is_ep_capture, old_ep, old_castle, old_clock, old_hash, old_eval_score))

        # 5. UPDATE MOVING PIECE
        # USE HELPER: Remove from 'from'
        self._x(moved_piece_idx, frm)
        self.piece_map[frm] = -1

        # Determine target piece (handle promotion)
        target_idx = moved_piece_idx
        if promo_code:
            target_idx = promo_code + 6 - 6 * us

        # USE HELPER: Place on 'to'
        self._x(target_idx, to)
        self.piece_map[to] = target_idx

        self.eval_score += self._get_piece_val(target_idx, to)

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
            r_from, r_to = (frm + 3, frm + 1) if to > frm else (frm - 4, frm - 1)

            rook_idx = 3 if us else 9

            self.eval_score -= self._get_piece_val(rook_idx, r_from)
            self.eval_score += self._get_piece_val(rook_idx, r_to)

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
        mv, c_idx, is_ep, self.ep, self.castle, self.halfmove_clock, self.hash, self.eval_score = self.stack.pop()
        
        self.white_to_move = not self.white_to_move
        
        # --- NULL MOVE HANDLING ---
        if not mv: return
        # --------------------------

        f = mv & 63
        t = (mv >> 6) & 63
        pr = (mv >> 12) & 7
        
        # 1. Pull piece back (t -> f)
        pc = self.piece_map[t]                  # Get piece at 'to' (could be promoted Queen)
        self.P[pc] ^= (1 << t)                  # Remove from 'to'
        self.piece_map[t] = -1

        real_p = pc if not pr else 6 - 6 * self.white_to_move
        self.P[real_p] |= (1 << f)              # Place on 'from'
        self.piece_map[f] = real_p

        # 2. Restore Capture
        if c_idx != -1:
            # If En Passant, capture is shifted. Else it's at 't'
            c_sq = t if not is_ep else t + 8 - 16 * self.white_to_move
            self.P[c_idx] |= (1 << c_sq)
            self.piece_map[c_sq] = c_idx

        # 3. Un-Castle (Move Rook back)
        if (real_p == 5 or real_p == 11) and abs(f - t) == 2:
            r_new, r_old = (f + 1, f + 3) if t > f else (f - 1, f - 4)
            r_idx = 3 if self.white_to_move else 9
            self.P[r_idx] ^= (1 << r_new) | (1 << r_old) # Toggle both rook squares at once
            self.piece_map[r_new], self.piece_map[r_old] = -1, r_idx


    # attack detection
    def attacked(self, sq, by_white):
        # 1. Pawns, Knights, Kings (Step Pieces)
        # Note: side_index(True, 0) is White Pawn (0), False is Black Pawn (6)
        if (PAWN_ATK_BLACK[sq] if by_white else PAWN_ATK_WHITE[sq]) & self.P[0 if by_white else 6]: return True
            
        if KNIGHT_ATK[sq] & self.P[1 if by_white else 7]: return True
        if KING_ATK[sq] & self.P[5 if by_white else 11]: return True
        
        # 2. Sliders (Merged Logic)
        occ = sum(self.P)

        for rays, attackers in (
            (ROOK_RAYS[sq], self.P[3 if by_white else 9] | self.P[4 if by_white else 10]),
            (BISHOP_RAYS[sq], self.P[2 if by_white else 8] | self.P[4 if by_white else 10])
        ):
            for ray in rays:
                for s in ray:
                    bit = 1 << s
                    if bit & attackers: return True
                    if bit & occ: break
                    
        return False

    def king_square(self, white):
        return self.P[5 if white else 11].bit_length() - 1
    
    def in_check(self, white=True):
        u = self.white_to_move if white else not self.white_to_move
        return self.attacked(self.king_square(u), not u)
    # --- move generation -------------------------------------------------
    def gen_pseudo_legal(self, active=False, killers=None, hash_move=None):
        moves = []
        us = self.white_to_move
        occ = sum(self.P)
        our = sum(self.P[:6]) if us else sum(self.P[6:])
        their = sum(self.P[6:]) if us else sum(self.P[:6])
        
        # Target masks
        step_targets = their if active else ~our
        
        # --- PAWNS ---
        pawns = self.P[0 if us else 6]
        
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
                    moves.append((9000 + base, sq | (tgt << 6) | (4 << 12)))
                    moves.append((5000 + base, sq | (tgt << 6) | (3 << 12)))
                    moves.append((3300 + base, sq | (tgt << 6) | (2 << 12)))
                    moves.append((3200 + base, sq | (tgt << 6) | (1 << 12)))
                elif not active:
                    # Quiet Push
                    score = CENTER_SCORE[tgt]

                    moves.append((score, sq | (tgt << 6)))
                    
                    # Double Push
                    if rank == start_rank:
                        tgt2 = sq + (push * 2)
                        if not (occ & (1 << tgt2)):
                            score = CENTER_SCORE[tgt2]
                            moves.append((score, sq | (tgt2 << 6)))

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
                    cap_idx = self.piece_map[tgt]
                    score = PIECE_VAL_BY_IDX[cap_idx] - 100
                    
                    if rank == promo_rank:
                        moves.append((score + 20900 + CENTER_SCORE[tgt], sq | (tgt << 6) | (4 << 12)))
                        moves.append((score + 20500 + CENTER_SCORE[tgt], sq | (tgt << 6) | (3 << 12)))
                        moves.append((score + 20330 + CENTER_SCORE[tgt], sq | (tgt << 6) | (2 << 12)))
                        moves.append((score + 20320 + CENTER_SCORE[tgt], sq | (tgt << 6) | (1 << 12)))
                    else:
                        score = (100000 if score >= 0 else 0) + score + CENTER_SCORE[tgt]
                        moves.append((score, sq | (tgt << 6)))

                # 3. En Passant
                elif self.ep == tgt:
                    # MVV/LVA: Victim(Pawn=100) * 100 - Attacker(100) = 9900 (+ Center)
                    score = 9900 + CENTER_SCORE[tgt] 
                    moves.append((score, sq | (tgt << 6)))

        # --- KNIGHTS ---
        knights = self.P[1 if us else 7]
        while knights:
            lsb = knights & -knights
            sq = lsb.bit_length() - 1
            knights ^= lsb
            
            attacks = KNIGHT_ATK[sq] & step_targets
            while attacks:
                lsb = attacks & -attacks
                tgt = lsb.bit_length() - 1
                attacks ^= lsb

                cap_idx = self.piece_map[tgt]
                if cap_idx != -1:
                    score = PIECE_VAL_BY_IDX[cap_idx] - 320
                    score = (100000 if score >= 0 else 0) + score + CENTER_SCORE[tgt]
                else:
                    score = CENTER_SCORE[tgt]

                moves.append((score, sq | (tgt << 6)))

        # --- SLIDERS (Bishops, Rooks, Queens) ---
        # Helper lists
        sliders = [
            (2, BISHOP_RAYS, 330),
            (3, ROOK_RAYS, 500),
            (4, QUEEN_RAYS, 900)
        ]
        
        for p_type, rays_table, own_val in sliders:
            pieces = self.P[p_type if us else p_type + 6]
            while pieces:
                lsb = pieces & -pieces
                sq = lsb.bit_length() - 1
                pieces ^= lsb
                
                for ray in rays_table[sq]:
                    for s in ray:
                        bit = 1 << s
                        if our & bit: break

                        cap_idx = self.piece_map[s]
                        if cap_idx != -1:
                            score = PIECE_VAL_BY_IDX[cap_idx] - own_val
                            score = (100000 if score >= 0 else 0) + score + CENTER_SCORE[s]
                            moves.append((score, sq | (s << 6)))
                            break
                        elif not active:
                            score = CENTER_SCORE[s]
                            moves.append((score, sq | (s << 6)))

        # --- KING ---
        ksq = self.king_square(us)
        if 0 <= ksq < 64:
            attacks = KING_ATK[ksq] & step_targets
            while attacks:
                lsb = attacks & -attacks
                tgt = lsb.bit_length() - 1
                attacks ^= lsb

                cap_idx = self.piece_map[tgt]
                if cap_idx != -1:
                    score = PIECE_VAL_BY_IDX[cap_idx]
                    score = (100000 if score >= 0 else 0) + score + CENTER_SCORE[tgt]
                else:
                    score = CENTER_SCORE[tgt]

                moves.append((score, ksq | (tgt << 6)))

            # --- CASTLING ---
            if not active:
                if us:
                    if (self.castle & 1) and not (occ & 96): # 96 = f1(32)+g1(64)
                        if not self.attacked(4, False) and not self.attacked(5,False) and not self.attacked(6,False):
                            moves.append((500, 4 | (6 << 6)))
                    if (self.castle & 2) and not (occ & 14): # 14 = b1(2)+c1(4)+d1(8)
                        if not self.attacked(4,False) and not self.attacked(3,False) and not self.attacked(2,False):
                            moves.append((500, 4 | (2 << 6)))
                else:
                    if (self.castle & 4) and not (occ & (6917529027641081856)): # f8+g8
                        if not self.attacked(60, True) and not self.attacked(61,True) and not self.attacked(62,True):
                            moves.append((500, 60 | (62 << 6)))
                    if (self.castle & 8) and not (occ & 1008806316530991104): # b8+c8+d8
                        if not self.attacked(60,True) and not self.attacked(59,True) and not self.attacked(58,True):
                            moves.append((500, 60 | (58 << 6)))
        
        if killers or hash_move:
            k0, k1 = killers or [None, None]
            new_moves = []
            for score, move in moves:
                if move == hash_move: score += 2000000
                elif move == k0: score += 1000000
                elif move == k1: score += 900000
                new_moves.append((score, move))
            moves = new_moves

        return moves

    def _get_piece_val(self, i, s):
        p = i % 6
        # Flip square for black (i>=6)
        t = s if i < 6 else s ^ 56
        
        # Compact PST logic: Rooks use rank check, others use tables
        # (t >> 3 == 6) is the same as (t // 8 == 6)
        v = 20 * (t >> 3 == 6) if p == 3 else (PAWN_PST if p == 0 else UNIFIED_PST)[t]
        
        m = PIECE_VAL_BY_IDX[p] + v * [1, 2, 2, 1, 1, 0][p] // 2
        
        # Return tuple with correct sign
        return m if i < 6 else -m

    # def pawn_structure_score(self, pawns):
    #     # 1. Collapse all pawns to Rank 1 (bits 0-7) to find occupied files
    #     # We "smear" the bits down: Rank 8->4, then 4->2, then 2->1.
    #     x = pawns
    #     x |= x >> 32
    #     x |= x >> 16
    #     x |= x >> 8
    #     file_occ = x & 0xFF  # 8 bits, 1 if file has ANY pawn, 0 otherwise

    #     # 2. Doubled Pawns Calculation
    #     # Original Logic: for every file, penalty = (pawn_count - 1) * 15
    #     # Bitwise Logic: (Total Pawns - Count of Occupied Files) * 15
    #     # Example: 3 pawns on A-file. bit_count=3, file_occ=1. (3-1) = 2 penalties. Matches.
    #     doubled_penalty = (pawns.bit_count() - file_occ.bit_count()) * 15

    #     # 3. Isolated Pawns Calculation
    #     # A file is isolated if it is occupied (file_occ) but its neighbors (left/right) are empty.
    #     # We project neighbor occupancy onto the current file slots.
    #     neighbor_occ = (file_occ << 1) | (file_occ >> 1)
        
    #     # Isolated = Occupied AND NOT Neighbor_Occupied
    #     isolated_mask = file_occ & ~neighbor_occ
        
    #     isolated_penalty = isolated_mask.bit_count() * 15

    #     return -(doubled_penalty + isolated_penalty)
    
    def evaluate(self):
        def eval_rooks(white):
            rooks = self.P[3 if white else 9]
            my_pawns = self.P[0 if white else 6]
            their_pawns = self.P[6 if white else 0]
            score = 0
            while rooks:
                lsb = rooks & -rooks
                sq = lsb.bit_length() - 1
                rooks ^= lsb
                m = FILE_MASKS[sq % 8]
                if not (my_pawns & m):
                    score += 10
                    if not (their_pawns & m):
                        score += 15
            return score

        def eval_king(white):
            k = self.king_square(white)
            castle_pos_score = 60 if k % 56 in (2, 6) else 0
            c = self.castle >> (0 if white else 2)
            if not (c & 1): castle_pos_score -= 10
            if not (c & 2): castle_pos_score -= 5
            return castle_pos_score

        if self.halfmove_clock >= 100: return 0
        score = self.eval_score + (eval_king(True) - eval_king(False) if self.P[4] | self.P[10] else 2 * (CENTER_SCORE[self.king_square(True)] - CENTER_SCORE[self.king_square(False)])) + eval_rooks(True) - eval_rooks(False)
        score += 50 * ((self.P[2].bit_count() > 1) - (self.P[8].bit_count() > 1)) + 10 * ((self.P[6] >> 8 & self.P[6]).bit_count() - (self.P[0] >> 8 & self.P[0]).bit_count())
        return score if self.white_to_move else -score
    
    def move_to_uci(self, mv):
        f = mv & 63
        t = (mv >> 6) & 63
        pr = (mv >> 12) & 7
        return chr(97+f%8)+chr(49+f//8)+chr(97+t%8)+chr(49+t//8)+('', 'n', 'b', 'r', 'q')[pr]
    
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
            fen_ep = "abcdefgh"[self.ep % 8] + "12345678"[self.ep // 8]
            
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

        def eval_rooks(white):
            rooks = self.P[3 if white else 9]
            my_pawns = self.P[0 if white else 6]
            their_pawns = self.P[6 if white else 0]
            s = 0
            while rooks:
                lsb = rooks & -rooks
                sq = lsb.bit_length() - 1
                rooks ^= lsb
                m = 0x0101010101010101 << (sq % 8)
                if not (my_pawns & m):
                    s += 10
                    if not (their_pawns & m):
                        s += 15
            return s

        def eval_king(white):
            k = self.king_square(white)
            s = 60 if k % 56 in (2, 6) else 0
            c = self.castle >> (0 if white else 2)
            if not (c & 1): s -= 10
            if not (c & 2): s -= 5
            return s

        rook_score = eval_rooks(True) - eval_rooks(False)
        king_score = eval_king(True) - eval_king(False)
        bishop_pair_score = 50 * (self.P[2].bit_count() >= 2) - 50 * (self.P[8].bit_count() >= 2)
        doubled_pawn_score = 10 * ((self.P[6] >> 8 & self.P[6]).bit_count() - (self.P[0] >> 8 & self.P[0]).bit_count())

        print(f"Turn: {('W' if self.white_to_move else 'B')} 50c: {self.halfmove_clock} Score: {score} Check: {self.in_check()}  Rev: Check: {self.in_check(False)}")
        print(f"Mat: {mat_score} Rook: {rook_score} King: {king_score} BishPair: {bishop_pair_score} DblPawn: {doubled_pawn_score}")
        print(f"Fen: {self.get_fen()}")
    #endremove