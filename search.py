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
import time

class Search:
    def __init__(self, board):
        self.board = board
        # Optimized TT: Simple list (2^20 entries). 
        # Entry: [hash, score, depth, flag(0=Exact, 1=Lower, 2=Upper), best_move]
        self.tt = [None] * (2**20) 
        self.s_nodes = 0
        self.time_up = False
        self.end_time = 0
        self.s_depth = 50

    def set_time_limit(self, seconds): 
        self.end_time = time.time() + seconds
        self.time_up = False

    #UNITremove
    def set_depth(self, depth): 
        self.s_depth = depth
    #UNITendremove

    def set_board(self, board): 
        self.board = board

    #remove
    def get_pv_line(self, max_depth):
        pv_moves = []
        
        # We will make moves on the board to traverse the TT, 
        # so we must count them to unmake them later.
        for _ in range(max_depth):
            tt_idx = self.board.hash % 1048576
            entry = self.tt[tt_idx]
            
            # Stop if: 
            # 1. No entry
            # 2. Hash collision (entry doesn't match current board)
            # 3. No best_move stored in entry
            if not entry or entry[0] != self.board.hash or not entry[4]:
                break
            
            move = entry[4]
            
            if move not in [m[1] for m in self.board.gen_pseudo_legal()]:
                break

            pv_moves.append(move)
            self.board.make_move(move)
            
            # If the move we just made ends the game (mate/stalemate), stop.
            if self.board.is_insufficient_material(): # or checkmate check
                break

        # RESTORE THE BOARD
        # We must unmake every move we made to return the board to the root state
        for _ in range(len(pv_moves)):
            self.board.unmake_move()
            
        return pv_moves
    #endremove

    def iterative_search(self):
        start_time = time.time()
        self.s_nodes = 0
        best_move = None

        for depth in range(1, self.s_depth + 1):
            if self.time_up: break
            
            # Search with Aspiration Windows (or infinite window)
            score = self.search(depth, -320000, 320000, 0)
            
            if self.time_up: break
            
            # Retrieve Best Move from TT using current hash
            entry = self.tt[self.board.hash % 1048576]

            if entry and entry[0] == self.board.hash: 
                best_move = entry[4]
            
            # Minimal UCI Reporting
            elapsed = max(1, int((time.time() - start_time) * 1000))
            pv_str = self.board.move_to_uci(best_move) if best_move else ""
            nps = int(self.s_nodes * 1000 / elapsed)
            
            #remove
            pv_moves = self.get_pv_line(depth)
            
            if pv_moves:
                best_move = pv_moves[0] # The first move is the one we'll actually play
                # Convert all moves in the list to UCI strings and join them
                pv_str = " ".join([self.board.move_to_uci(m) for m in pv_moves])
            else:
                pv_str = ""
            #endremove
            
            print(f"info depth {depth} score cp {int(score)} time {elapsed} nodes {self.s_nodes} nps {nps} pv {pv_str}", flush=True)

        # Final Best Move
        print(f"bestmove {self.board.move_to_uci(best_move)}", flush=True)

    def drawn(self):
        if self.board.halfmove_clock >= 100 or self.board.is_insufficient_material():
            return True
        # Check every 2nd ply up to the halfmove clock (irreversible move) limit
        current_hash = self.board.hash
        limit = min(self.board.halfmove_clock, len(self.board.stack))
        
        count = 0
        for i in range(2, limit + 1, 2):
            if self.board.stack[-i][6] == current_hash: 
                count += 1
                # We need 2 past occurrences + current one = 3 total
                if count >= 2: return True
                
        return False

    def search(self, s_depth, alpha, beta, ply):
        # Check time every 2048 nodes
        if (self.s_nodes & 2047) == 0 and time.time() > self.end_time:
            self.time_up = True
            return 0
            
        if self.drawn(): 
            return 0

        in_check = self.board.in_check()

        # --- CHECK EXTENSION ---
        if in_check and s_depth < 4: 
             s_depth += 1
            
        if s_depth <= 0: 
            return self.q_search(alpha, beta)
        
        self.s_nodes += 1
        
        # --- TT PROBE ---
        tt_idx = self.board.hash % 1048576
        entry = self.tt[tt_idx]
        if entry and entry[0] == self.board.hash and entry[2] >= s_depth:
            if entry[3] == 0: return entry[1]
            if entry[3] == 1 and entry[1] >= beta: return entry[1]
            if entry[3] == 2 and entry[1] <= alpha: return entry[1]

        # --- NULL MOVE PRUNING ---
        # Disable NMP if in check
        if s_depth >= 3 and not in_check:
            self.board.make_move(None)
            score = -self.search(s_depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            
            if self.time_up: return 0
            if score >= beta: return score

        # --- REVERSE FUTILITY PRUNING ---
        # Disable RFP if in check
        stand_pat = self.board.evaluate()
        if s_depth < 4 and not in_check and stand_pat >= beta + s_depth * 80:
            return stand_pat

        best_score = -320000
        best_move = None
        
        # Generate and sort moves
        moves = self.board.gen_pseudo_legal(); moves.sort(reverse=True)

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
            # Don't reduce if in check, or if the move gives check (heuristic), or captures
            if s_depth > 2 and moves_played > 4 and not (in_check or move[2] or move[3]):
                reduction = 1 + (moves_played > 15)
            
            new_depth = s_depth - 1 - reduction
            
            if moves_played > 1:
                score = -self.search(new_depth, -alpha - 1, -alpha, ply + 1)
                if score > alpha and (score < beta or new_depth != s_depth - 1):
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
                    self.tt[tt_idx] = [self.board.hash, alpha, s_depth, 1, move]
                    return alpha
        
        if moves_played == 0:
            return -320000 + ply if in_check else 0

        flag = 0 if alpha > original_alpha else 2
        self.tt[tt_idx] = [self.board.hash, alpha, s_depth, flag, best_move]
        
        return alpha

    def q_search(self, alpha, beta):
        if (self.s_nodes & 2047) == 0 and time.time() > self.end_time:
            self.time_up = True
            return 0
        
        if self.drawn(): 
            return 0

        self.s_nodes += 1
        
        # TT Probe (Q-Search)
        entry = self.tt[self.board.hash % 1048576]
        if entry and entry[0] == self.board.hash:
            if entry[3] == 0: return entry[1]
            if entry[3] == 1 and entry[1] >= beta: return entry[1]
            if entry[3] == 2 and entry[1] <= alpha: return entry[1]

        in_check = self.board.in_check()

        stand_pat = self.board.evaluate()
        if not in_check and stand_pat >= beta: return beta
        if not in_check and stand_pat > alpha: alpha = stand_pat
        
        moves = self.board.gen_pseudo_legal(not in_check); moves.sort(reverse=True)
        
        moves_played = 0

        # Active Moves Only (Captures/Promotions)
        for _, move in moves:
            if not in_check and move[3] and (stand_pat + self.board.PIECE_VALUES[move[3]] + 200) < alpha and not move[2]: continue

            self.board.make_move(move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
            
            moves_played += 1
            score = -self.q_search(-beta, -alpha)
            self.board.unmake_move()
            
            if score >= beta: return beta
            if score > alpha: alpha = score
        
        if moves_played == 0 and in_check:
            return -320000
        
        return alpha