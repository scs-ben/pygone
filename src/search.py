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

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        uci_move = None
        
        self.s_nodes = 0

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
        print(f"bestmove {uci_move}", flush=True)

    def threefold(self):
        count = 1
        
        for entry in self.board.stack:
            count += entry[-1] == self.board.hash
            if count >= 3:
                return True
            
        return False

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

        # Nullmove pruning
        if s_depth >= 3 and not in_check:
            self.board.make_move(None)
            g_score = -self.search(s_depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            if g_score >= beta:
                return g_score
        
        is_pv_node = beta > alpha + 1
        stand_pat = self.board.evaluate()

        if not is_pv_node and not in_check:
            # Futility pruning (low eval)
            if s_depth <= 2 and stand_pat + 100 * s_depth <= alpha:
                return stand_pat

            # Razor pruning (high eval)
            if s_depth <= 3 and stand_pat >= beta - 80 * s_depth:
                return stand_pat
            
        # if not is_pv_node and not in_check and s_depth <= 5:
        #     cut_boundary = alpha - (150 * s_depth)
        #     if stand_pat <= cut_boundary:
        #         if s_depth <= 2:
        #             return self.q_search(alpha, alpha + 1)

        #         local_score = self.q_search(cut_boundary, cut_boundary + 1)

        #         if local_score <= cut_boundary:
        #             return local_score
        
        all_moves = sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True)

        if not all_moves:
            return -self.MATE_SCORE_UPPER + ply if in_check else 0

        if entry and entry[4]:
            all_moves = [entry[4]] + all_moves

        best_score = -1e9
        best_move = None
        played_moves = 0
        alpha_orig = alpha

        for t_move in all_moves:
            played_moves += 1

            self.board.make_move(t_move)

            g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            self.board.unmake_move()

            if self.time_up:
                break

            # ------------------------------------------------------------------
            # Alpha-beta updates
            # ------------------------------------------------------------------
            if g_score > best_score:
                best_score = g_score
                best_move = t_move

            if g_score > alpha:
                alpha = g_score
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
    