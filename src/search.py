import math, time

class TTEntry:
    __slots__ = ('key', 'g_score', 's_depth', 'flag', 't_move')
    def __init__(self, key=0, g_score=0, s_depth=0, flag='EXACT', t_move=None):
        self.key = key
        self.g_score = g_score
        self.s_depth = s_depth
        self.flag = flag
        self.t_move = t_move

class TranspositionTable:
    def __init__(self):
        entry_size = 32  # approximate bytes per entry
        self.size = 2**31 // entry_size
        self.table = [None] * self.size

    def tt_index(self, zobrist_key):
        return zobrist_key % self.size

    def store(self, key, s_depth, g_score, flag, t_move):
        idx = self.tt_index(key)
        entry = self.table[idx]
        
        # New, safer replacement criteria:
        if entry is None or \
           entry.key != key or \
           entry.s_depth < s_depth or \
           (entry.s_depth == s_depth and flag == 'EXACT'):
           
           # If the position already exists but is shallower, or if the new score is EXACT
           # at the same depth, replace it.
           self.table[idx] = TTEntry(key, g_score, s_depth, flag, t_move)

    def probe(self, key, ply, MATE_SCORE_UPPER): # Must pass MATE_SCORE_UPPER
        idx = self.tt_index(key)
        entry = self.table[idx]
        if entry is not None and entry.key == key:
            if entry.g_score > MATE_SCORE_UPPER - 1e3:
                entry.g_score -= ply 
            elif entry.g_score < -MATE_SCORE_UPPER + 1e3:
                entry.g_score += ply 
            return entry
        return None

class Search:
    MATE_SCORE_UPPER = 32e4
    TIME_CUT = 0
    
    def __init__(self, board):
        self.board = board
        self.s_nodes = 0
        self.tt = TranspositionTable()
        self.time_limit = None      # seconds
        self.end_time = None
        self.time_up = False
        self.s_depth = 50
        self.clear_tables()

    def clear_tables(self):
        """Called at the start of a new top-level search."""
        self.killer_moves = [[None, None] for _ in range(64)]
        self.history_table = [[0] * 64 for _ in range(64)]

    def set_time_limit(self, seconds):
        self.time_limit = seconds
        self.end_time = time.time() + seconds
        self.time_up = False
        
    def set_depth(self, s_depth):
        self.s_depth = s_depth

    def set_board(self, board):
        self.board = board

    def print_stats(self, s_depth, g_score, time, s_nodes, nps, pv):
        print(f"info depth {s_depth} score cp {g_score} time {time} nodes {s_nodes} nps {nps} pv {pv}", flush=True)

    # def score_killer_move(self, t_move, ply, tt_move):
    #     # 1. Transposition Table Move (Highest Priority)
    #     if tt_move and t_move == tt_move:
    #         return 9e6  # Highest possible score

    #     # 2. Promotions
    #     if t_move[2]:
    #         # Use a high score, prioritizing Queen
    #         return 8e6 + self.board.PIECE_VALUES[t_move[2]] * 10
        
    #     # 3. Captures (MVV-LVA - Your existing logic)
    #     if t_move[3]:
    #         # NOTE: Your board needs a PIECE_VALUES property
    #         # Consider using a higher base score for captures than for quiet moves
    #         victim_value = self.board.PIECE_VALUES[t_move[3]]
    #         attacker_value = self.board.PIECE_VALUES[t_move[4]]
    #         # Simple scaling to keep this range between 7M and 8M
    #         return 7e6 + 10 * victim_value - attacker_value
    #         # *For maximum strength, this should be replaced by Static Exchange Evaluation (SEE)*
        
    #     # --- Quiet Moves (Lower Priority) ---
        
    #     # 4. Killer Moves
    #     if t_move == self.killer_moves[ply][0]:
    #         return 6e5  # High score for primary killer
    #     if t_move == self.killer_moves[ply][1]:
    #         return 5e5  # Slightly lower for secondary killer

    #     # 5. History Heuristic
    #     # Assuming move provides from_sq and to_sq indices (0-63)
    #     from_sq_idx = t_move[0]
    #     to_sq_idx = t_move[1]
        
    #     # History scores are typically much smaller, e.g., max 1e30.
    #     return self.history_table[from_sq_idx][to_sq_idx]

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        best_score = None
        
        self.s_nodes = 0
        self.clear_tables()

        all_moves = self.board.gen_legal_moves()
        if not all_moves:
            # Position is Checkmate or Stalemate. Handle this outside the search loop.
            return None, self.board.evaluate() # Or a known terminal score
        
        best_move = all_moves[0]

        for s_depth in range(1, self.s_depth + 1):  # iterative deepening
            if self.time_up:
                break

            current_score = self.search(s_depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            if self.time_up:
                break
            
            best_score = current_score
            
            entry = self.tt.probe(self.board.hash, 1, self.MATE_SCORE_UPPER)
            if entry and entry.t_move:
                best_move = entry.t_move

            elapsed_time = time.time() - start_time
            nps = math.ceil(self.s_nodes / elapsed_time) if elapsed_time > 0 else 1

            uci_move = self.board.move_to_uci(best_move) if best_move else None
            self.print_stats(str(s_depth), str(math.ceil(best_score)), str(math.ceil(elapsed_time * 1e3)), str(self.s_nodes), str(nps), str(uci_move))
            
            if s_depth >= self.s_depth:
                break

        # When time expires, return the best move/eval found
        return best_move, best_score

    def threefold(self):
        count = 1
        
        for entry in self.board.stack:
            count += entry[-1] == self.board.hash
            if count >= 3:
                return True
            
        return False

    # def has_sufficient_material(self):
    #     if self.board.white_to_move:
    #         pawns  = bin(self.board.P[0]).count('1')
    #         minors = bin(self.board.P[1]).count('1') + bin(self.board.P[2]).count('1')
    #         majors = bin(self.board.P[3]).count('1') + bin(self.board.P[4]).count('1')
    #     else:
    #         pawns  = bin(self.board.P[6]).count('1')
    #         minors = bin(self.board.P[7]).count('1') + bin(self.board.P[8]).count('1')
    #         majors = bin(self.board.P[9]).count('1') + bin(self.board.P[10]).count('1')

    #     return pawns > 0 or minors + majors >= 2

    def search(self, s_depth, alpha=-MATE_SCORE_UPPER, beta=MATE_SCORE_UPPER, ply=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
            
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if s_depth == 0:
            return self.q_search(alpha, beta)
        
        is_pv_node = beta > alpha + 1
        alpha_orig = alpha

        self.s_nodes += 1
        
        # --- TT lookup ---
        entry = self.tt.probe(self.board.hash, ply, self.MATE_SCORE_UPPER)
        if entry and entry.s_depth >= s_depth and not is_pv_node:
            if entry.flag == 'EXACT' or \
                entry.flag == 'LOWERBOUND' and entry.g_score >= beta or \
                entry.flag == 'UPPERBOUND' and entry.g_score <= alpha:
                    return entry.g_score

        in_check = self.board.in_check()
        # stand_pat = self.board.evaluate()

        # if not is_pv_node and not in_check:
        #     # Futility pruning (low eval)
        #     if s_depth <= 2 and stand_pat + 100 * s_depth <= alpha:
        #         return stand_pat

        #     # Razor pruning (high eval)
        #     if s_depth <= 3 and stand_pat >= beta - 80 * s_depth:
        #         return stand_pat

        # if not is_pv_node and not in_check and s_depth <= 5:
        #     cut_boundary = alpha - (150 * s_depth)
        #     if stand_pat <= cut_boundary:
        #         if s_depth <= 2:
        #             return self.q_search(alpha, alpha + 1)

        #         local_score = self.q_search(cut_boundary, cut_boundary + 1)

        #         if local_score <= cut_boundary:
        #             return local_score

        # # Null move pruning (only when safe)
        # if (
        #     not is_pv_node
        #     and not in_check
        #     and s_depth >= 3
        #     and self.has_sufficient_material()
        # ):
        #     reduction = 2 + s_depth // 6 # typical reduction
        #     self.board.nullmove()

        #     # skip if nullmove leaves us in check (can happen in some custom rulesets)
        #     if not self.board.in_check(False): # Check for null move legality
        #         null_score = -self.search(s_depth - reduction - 1, -beta, -beta + 1, ply + 1) # Note ply+1 added

        #         # If the null move proves a cutoff, return immediately (beta cutoff)
        #         if null_score >= beta:
        #             self.board.unmake_move() # Unmake before returning
        #             return beta

        #     self.board.unmake_move() # Guaranteed unmake for all other cases

        # if not is_pv_node and not in_check and entry and entry.t_move and entry.s_depth >= s_depth and abs(entry.g_score) < self.MATE_SCORE_UPPER:
        #     self.board.make_move(entry.t_move)
        #     local_score = -self.search(s_depth - 1, -beta, -alpha)
        #     self.board.unmake_move()

        #     if local_score >= beta:
        #         return beta

        best_score = -1e9
        best_move = None

        played_moves = 0
        
        all_moves = sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True)
        
        if not all_moves:
            # Position is Checkmate or Stalemate. Handle this outside the search loop.
            return self.board.evaluate()
        
        best_move = entry.t_move if entry and entry.t_move else all_moves[0]
        
        # scored_moves = []
        # for t_move in all_moves:
        #      # Pass the current ply and the tt_move
        #      g_score = self.score_killer_move(t_move, ply, entry.t_move if entry else None)
        #      scored_moves.append((g_score, t_move))
             
        # sorted_moves = sorted(scored_moves, key=lambda x: x[0], reverse=True)

        s_depth += in_check

        # for g_score, t_move in sorted_moves:
        # for t_move in all_moves:
        for t_move in sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True):
            self.board.make_move(t_move)

            played_moves += 1
            #is_quiet = not t_move[3] and not t_move[2]
            
            # 1. Determine Search Depth (Default is full depth)
            # current_depth = s_depth - 1
            # reduction = 0

            # Apply LMR (LMR is only safe if it's NOT the PV move, NOT in check, and a quiet move)
            # if is_quiet and s_depth >= 3 and played_moves > 3:
            #      reduction = int(0.75 + math.log(s_depth) * math.log(played_moves) / 2)
            #      current_depth = s_depth - 1 - reduction

            # # 2. Perform Primary Search (PVS: use a narrow window -alpha-1 for all but the first move)
            # if played_moves == 1:
            #     # First move: Full window search (to find the PV)
            #     g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)
            # else:
            #     # PVS Search (Narrow window, potentially reduced depth)
            #     g_score = -self.search(current_depth, -alpha - 1, -alpha, ply + 1)

            #     # 3. LMR Re-search (if reduced search beat alpha)
            #     if reduction > 0 and g_score > alpha:
            #         # Re-search at full depth (s_depth - 1) but still with the narrow window
            #         g_score = -self.search(s_depth - 1, -alpha - 1, -alpha, ply + 1)

            #     # 4. PV Re-search (if the move beat the current alpha)
            #     if g_score > alpha and g_score < beta:
            #         # Re-search with full window [alpha, beta]
            #         g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)
            
            g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)
            
            self.board.unmake_move()
            
            if self.time_up:
                break
            
            if not best_move:
                best_move = t_move

            if g_score > best_score:
                best_score = g_score
                best_move = t_move
                
                if g_score > alpha:
                    alpha = g_score
                    
                    if alpha >= beta:
                        # if is_quiet:
                        #     # Update Killer Heuristic
                        #     self.killer_moves[ply][1] = self.killer_moves[ply][0] # Move old killer to slot 1
                        #     self.killer_moves[ply][0] = t_move                      # New killer in slot 0
                            
                        #     # Update History Heuristic (e.g., add 1 to the score)
                        #     from_sq_idx = t_move[0]
                        #     to_sq_idx = t_move[1]
                        #     # Increase history score, possibly scaled by s_depth (e.g. s_depth * s_depth)
                        #     self.history_table[from_sq_idx][to_sq_idx] += s_depth * s_depth
                            # Limit the score to prevent overflow/bias (e.g., max 1e30)
                        break
        
        if not played_moves:
            return -self.MATE_SCORE_UPPER + ply if in_check else 0

        # --- Store in TT ---
        if best_score <= alpha_orig:
            flag = 'UPPERBOUND'
            # Note: Do NOT store best_move for UPPERBOUND as it's unreliable
            # tt_move = None 
        elif best_score >= beta:
            flag = 'LOWERBOUND'
            # Store the move that caused the cutoff (Refutation Move)
            # tt_move = best_move 
        else:
            flag = 'EXACT'
            # Store the best move found
            # tt_move = best_move

        if not self.time_up:
            tt_move = best_move if flag != 'UPPERBOUND' else None
            if best_score > self.MATE_SCORE_UPPER - 1e3:
                best_score += ply # Store the score AS IF it were found at the root (ply 0)
            elif best_score < -self.MATE_SCORE_UPPER + 1e3:
                best_score -= ply # Store the score AS IF it were found at the root (ply 0)
            # Pass the appropriate move (tt_move) to the store function
            self.tt.store(self.board.hash, s_depth, best_score, flag, tt_move)

        return best_score
    
    def q_search(self, alpha, beta, q_depth=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
        
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        in_check = self.board.in_check()
        
        stand_pat = self.board.evaluate()
        
        if q_depth >= 30:
            return stand_pat
        
        if not in_check and stand_pat >= beta:
            return beta
        if not in_check and alpha < stand_pat:
            alpha = stand_pat
        
        # if not in_check:
        #     # We need the value of the most valuable piece (typically Queen, around 900-1e3)
        #     # Use a slightly smaller value for safety margin (e.g., Q value - 100)
        #     MAX_GAIN = self.board.PIECE_VALUES['q'] # Assuming 'q' is the key for Queen value
            
        #     # If (current best static eval) + (max possible material gain) is still less than alpha, prune.
        #     if stand_pat + MAX_GAIN <= alpha:
        #         return alpha
            
        #     # Optional: Small check for very deep Q-search
        #     if q_depth > 5 and stand_pat + 200 <= alpha: # 200 is small futility margin
        #         return alpha
        # else:
        #     # If in check, stand_pat is irrelevant, alpha remains the score to beat
        #     stand_pat = -float('inf')
        
        self.s_nodes += 1
        
        # TT lookup
        entry = self.tt.probe(self.board.hash, q_depth, self.MATE_SCORE_UPPER)
        if entry and entry.s_depth == 0:
            if entry.flag == 'EXACT' or \
                entry.flag == 'LOWERBOUND' and entry.g_score >= beta or \
                entry.flag == 'UPPERBOUND' and entry.g_score <= alpha:
                    return entry.g_score
        
        if not in_check and stand_pat >= beta:
            return stand_pat

        for t_move in sorted(self.board.gen_legal_moves(not in_check), key=self.board.score_move, reverse=True):
            self.board.make_move(t_move)
                      
            g_score = -self.q_search(-beta, -alpha, q_depth + 1)
            
            self.board.unmake_move()
            
            if self.time_up:
                break

            if g_score > alpha:
                alpha = g_score
                
                if alpha >= beta:
                    return alpha
            
        return alpha
        