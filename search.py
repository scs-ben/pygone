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
import time
#remove
from board import PIECE_VAL_BY_IDX
#endremove

class Search:
    def __init__(self, board):
        self.board = board
        # Pre-allocated flat list: 3 integers per slot
        self.tt = [0] * (3 * 2**20) 
        self.s_nodes = 0
        self.time_up = False
        self.end_time = 0
        self.s_depth = 50
        self.killers = [[None, None] for _ in range(64)]

    #UNITremove
    def set_depth(self, depth): 
        self.s_depth = depth
    #UNITendremove



    #remove
    def get_pv_line(self, max_depth):
        pv_moves = []
        for _ in range(max_depth):
            tt_idx = 3 * (self.board.hash & 0xFFFFF)
            if self.tt[tt_idx] != self.board.hash:
                break
            move = self.tt[tt_idx + 2]
            if not move:
                break
            
            if move not in [m[1] for m in self.board.gen_pseudo_legal()]:
                break

            pv_moves.append(move)
            self.board.make_move(move)

        for _ in range(len(pv_moves)):
            self.board.unmake_move()
            
        return pv_moves
    #endremove

    def iterative_search(self):
        start_time = time.time()
        self.s_nodes = 0
        best_move = None

        for _, mv in self.board.gen_pseudo_legal():
            self.board.make_move(mv)
            if not self.board.in_check(False):
                best_move = mv
            self.board.unmake_move()
            if best_move: break

        for depth in range(1, self.s_depth + 1):
            if self.time_up: break
            
            score = self.search(depth, -320000, 320000, 0)
            if self.time_up: break
            
            tt_idx = 3 * (self.board.hash & 0xFFFFF)
            if self.tt[tt_idx] == self.board.hash:
                entry_move = self.tt[tt_idx + 2]
                if entry_move:
                    for _, pm in self.board.gen_pseudo_legal():
                        if pm == entry_move:
                            self.board.make_move(pm)
                            if not self.board.in_check(False):
                                best_move = pm
                            self.board.unmake_move()
                            break
            
            output = f"info depth {depth} score cp {score}"

            #remove
            elapsed = max(1, int((time.time() - start_time) * 1000))
            nps = int(self.s_nodes * 1000 / elapsed)
            pv_moves = self.get_pv_line(depth)
            
            if pv_moves:
                best_move = pv_moves[0]
                pv_str = " ".join([self.board.move_to_uci(m) for m in pv_moves])
            else:
                pv_str = ""

            output = f"info depth {depth} score cp {int(score)} time {elapsed} nodes {self.s_nodes} nps {nps} pv {pv_str}"
            #endremove

            print(output, flush=True)

        print(f"bestmove {self.board.move_to_uci(best_move)}", flush=True)

    def drawn(self, ply=0):
        h = self.board.halfmove_clock
        if h >= 100: return True
        if not h: return False
        s = self.board.stack
        hsh = self.board.hash
        n = 2 - bool(ply)
        for i in range(2, min(h, len(s)) + 1, 2):
            if s[-i][6] == hsh:
                n -= 1
                if not n: return True
        return False

    def search(self, s_depth, alpha, beta, ply):
        if self.time_up or ((self.s_nodes & 1023) == 0 and time.time() > self.end_time):
            self.time_up = True
            return 0
            
        if self.drawn(ply): 
            return 0
 
        in_check = self.board.in_check()
 
        # --- CHECK EXTENSION ---
        s_depth += in_check and s_depth < 4
            
        if s_depth <= 0: 
            return self.q_search(alpha, beta)
        
        self.s_nodes += 1
        
        # --- TT PROBE ---
        tt_idx = 3 * (self.board.hash & 0xFFFFF)
        h = self.tt[tt_idx]
        hash_move = None
        w = False
        if h == self.board.hash:
            packed = self.tt[tt_idx + 1]
            score = (packed & 0xFFFFF) - 320000
            depth = (packed >> 20) & 0x7F
            flag = (packed >> 27) & 3
            entry_ply = (packed >> 29) & 0x7F
            hash_move = self.tt[tt_idx + 2] or None
            w = not self.time_up and (s_depth > depth or (s_depth == depth and ply > entry_ply))
            if depth >= s_depth:
                if flag == 0 or (flag == 1 and score >= beta) or (flag == 2 and score <= alpha):
                    return score
        else:
            w = not self.time_up
 
        # --- NULL MOVE PRUNING ---
        us = self.board.white_to_move; p = self.board.P
        if s_depth >= 3 and not in_check and (sum(p[1:5]) if us else sum(p[7:11])):
            self.board.make_move(None)
            score = -self.search(s_depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            
            if self.time_up: return 0
            if score >= beta: return score
 
        # --- REVERSE FUTILITY PRUNING ---
        stand_pat = self.board.evaluate()
        if s_depth < 4 and not in_check and stand_pat >= beta + s_depth * 80:
            return stand_pat
 
        best_score = -320000
        best_move = None
        
        # Generate and sort moves
        moves = self.board.gen_pseudo_legal(killers=self.killers[ply], hash_move=hash_move); moves.sort(reverse=True)

        moves_played = 0
        original_alpha = alpha
        
        for _, move in moves:
            self.board.make_move(move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
            
            moves_played += 1
            
            # --- LMR + PVS LOGIC ---
            reduction = 0
            if s_depth > 2 and moves_played > 4 and not (in_check or ((move >> 12) & 7) or self.board.piece_map[(move >> 6) & 63] != -1 or ((move >> 6) & 63) == self.board.ep):
                reduction = 1 + (moves_played > 15)
            
            new_depth = s_depth - 1 - reduction
            
            if moves_played > 1:
                score = -self.search(new_depth, -alpha - 1, -alpha, ply + 1)
                if not self.time_up and score > alpha and (score < beta or new_depth != s_depth - 1):
                    score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)
            else:
                score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            self.board.unmake_move()
            
            if self.time_up: return 0
            
            if score > best_score:
                best_score = score
                best_move = move
                
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    if not (((move >> 12) & 7) or self.board.piece_map[(move >> 6) & 63] != -1 or ((move >> 6) & 63) == self.board.ep):
                        _, k0 = self.killers[ply]
                        if move != k0:
                            self.killers[ply] = [move, k0]

                    if w:
                        self.tt[tt_idx] = self.board.hash
                        self.tt[tt_idx + 1] = (alpha + 320000) | (s_depth << 20) | (1 << 27) | (ply << 29)
                        self.tt[tt_idx + 2] = move or 0
                    return alpha
        
        if moves_played == 0:
            return -320000 + ply if in_check else 0

        flag = 0 if alpha > original_alpha else 2
        if w:
            self.tt[tt_idx] = self.board.hash
            self.tt[tt_idx + 1] = (alpha + 320000) | (s_depth << 20) | (flag << 27) | (ply << 29)
            self.tt[tt_idx + 2] = best_move or 0
        
        return alpha

    def q_search(self, alpha, beta):
        if self.time_up or ((self.s_nodes & 1023) == 0 and time.time() > self.end_time):
            self.time_up = True
            return 0
        
        if self.drawn(1): 
            return 0

        self.s_nodes += 1
        
        in_check = self.board.in_check()

        stand_pat = self.board.evaluate()
        if not in_check and stand_pat >= beta: return beta
        if not in_check and stand_pat > alpha: alpha = stand_pat
        
        moves = self.board.gen_pseudo_legal(not in_check); moves.sort(reverse=True)
        
        moves_played = 0

        # Active Moves Only (Captures/Promotions)
        for _, move in moves:
            to_sq = (move >> 6) & 63
            cap_idx = self.board.piece_map[to_sq] if to_sq != self.board.ep else (6 if self.board.white_to_move else 0)
            if not in_check and cap_idx != -1 and stand_pat + PIECE_VAL_BY_IDX[cap_idx] + 50 < alpha and not ((move >> 12) & 7): continue

            self.board.make_move(move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
            
            moves_played += 1
            score = -self.q_search(-beta, -alpha)
            self.board.unmake_move()
            
            if self.time_up: return 0
            if score >= beta: return beta
            if score > alpha: alpha = score
        
        return -320000 if in_check and not moves_played else alpha