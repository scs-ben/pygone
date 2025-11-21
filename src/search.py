import math, time

#class TTEntry:
#    entry ('key', 'g_score', 's_depth', 'flag', 't_move')

class TranspositionTable:
    size = 2**31 // 32
    table = [None] * size

    def store(self, key, s_depth, g_score, flag, t_move):
        idx = (key % self.size)
        e = self.table[idx]
        if not e or e[0]!=key or e[2]<s_depth or (e[2]==s_depth and flag=='EXACT'):
            self.table[idx] = [key, g_score, s_depth, flag, t_move]

    def probe(self, key):
        e = self.table[(key % self.size)]
        if e and e[0] == key:
            return e

class Search:
    MATE_SCORE_UPPER = 32e4
    
    def __init__(self, board):
        self.board = board
        self.s_nodes = 0
        self.tt = TranspositionTable()
        self.time_limit = None      # seconds
        self.end_time = None
        self.time_up = False
        self.s_depth = 50
        #self.clear_tables()

    #def clear_tables(self):
    #    """Called at the start of a new top-level search."""
    #    self.killer_moves = [[None, None] for _ in range(64)]
    #    self.history_table = [[0] * 64 for _ in range(64)]

    def set_time_limit(self, seconds):
        self.time_limit = seconds
        self.end_time = time.time() + seconds
        self.time_up = False
    
    #remove
    def set_depth(self, s_depth):
        self.s_depth = s_depth
    #endremove

    def set_board(self, board):
        self.board = board

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
        uci_move = None
        
        self.s_nodes = 0
        # self.clear_tables()

        # all_moves = self.board.gen_legal_moves()
        # if not all_moves:
        #     # Position is Checkmate or Stalemate. Handle this outside the search loop.
        #     return None, self.board.evaluate() # Or a known terminal score
        
        # best_move = all_moves[0]

        for s_depth in range(1, self.s_depth + 1):  # iterative deepening
            if self.time_up:
                break

            current_score = self.search(s_depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            if self.time_up:
                break
            
            entry = self.tt.probe(self.board.hash)
            if entry and entry[4]: best_move = entry[4]

            elapsed_time = time.time() - start_time
            nps = math.ceil(self.s_nodes / elapsed_time) if elapsed_time > 0 else 1

            uci_move = None
            if best_move:
                uci_move = self.board.move_to_uci(best_move)
            
            if uci_move: print(f"info depth {s_depth} score cp {math.ceil(current_score)} time {math.ceil(elapsed_time * 1e3)} nodes {self.s_nodes} nps {nps} pv {uci_move}", flush=True)
            
            if s_depth >= self.s_depth:
                break

        # When time expires, return the best move
        if uci_move: print(f"bestmove {uci_move}", flush=True)
        else: print("quit", flush=True)

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
            return 0
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if s_depth <= 0:
            return self.q_search(alpha, beta)
        
        in_check = self.board.in_check()

        self.s_nodes += 1

        entry = self.tt.probe(self.board.hash)
        if entry:
            if entry[2] >= s_depth:
                if entry[3] == 'EXACT':
                    return entry[1]
                if entry[3] == 'LOWERBOUND' and entry[1] > alpha:
                    alpha = entry[1]
                elif entry[3] == 'UPPERBOUND' and entry[1] < beta:
                    beta = entry[1]
                if alpha >= beta:
                    return entry[1]

        if s_depth >= 3 and not in_check:
            self.board.make_move(None)
            g_score = -self.search(s_depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            if g_score >= beta:
                return g_score
            
        all_moves = sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True)

        if entry and entry[4]:
            all_moves = [entry[4]] + all_moves

        if not all_moves:
            return -self.MATE_SCORE_UPPER + ply if in_check else 0

        best_score = -1e9
        best_move = None
        played_moves = 0
        alpha_orig = alpha

        for t_move in all_moves:
            if played_moves > 0 and entry and entry[4] == t_move:
                continue

            played_moves += 1

            self.board.make_move(t_move)
            is_quiet = not t_move[3] and not t_move[2]

            # -------------------------------
            # Late Move Reductions
            # -------------------------------
            if (played_moves > 1 and is_quiet and not in_check
                and s_depth >= 3 and played_moves >= 4):

                reduction = 1 + (s_depth > 3) + (played_moves > 3)
                reduced_depth = s_depth - 1 - reduction

            else:
                reduced_depth = s_depth - 1

            # -------------------------------
            # PVS / zero-width search
            # -------------------------------
            if played_moves == 1:
                # Full PV window
                score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            else:
                # Zero-width search
                score = -self.search(reduced_depth, -alpha - 1, -alpha, ply + 1)

                # ---------------------------
                # LMR re-search
                # ---------------------------
                if reduced_depth < s_depth - 1 and score > alpha:
                    score = -self.search(s_depth - 1, -alpha - 1, -alpha, ply + 1)

                # ---------------------------
                # Full-window re-search
                # ---------------------------
                if score > alpha and score < beta:
                    score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            self.board.unmake_move()

            # ------------------------------------------------------------------
            # 6. Alpha-beta updates
            # ------------------------------------------------------------------
            if score > best_score:
                best_score = score
                best_move = t_move

            if score > alpha:
                alpha = score
                if alpha >= beta:
                    # Fail-high cutoff — store TT and exit
                    self.tt.store(self.board.hash, s_depth, alpha, 'LOWERBOUND', t_move)
                    return alpha

        flag = 'EXACT' if alpha > alpha_orig else 'UPPERBOUND'
        self.tt.store(self.board.hash, s_depth, alpha, flag, best_move)

        return alpha
    
    def q_search(self, alpha, beta, q_depth=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return 0
        
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        self.s_nodes += 1

        # TT lookup
        entry = self.tt.probe(self.board.hash)
        if entry and entry[2] == 0:
            if entry[3] == 'EXACT' or \
                entry[3] == 'LOWERBOUND' and entry[1] >= beta or \
                entry[3] == 'UPPERBOUND' and entry[1] <= alpha:
                    return entry[1]

        stand_pat = self.board.evaluate()

        if q_depth >= 30 or stand_pat >= beta:
            return stand_pat

        alpha = max(alpha, stand_pat)

        in_check = self.board.in_check()
        
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
    