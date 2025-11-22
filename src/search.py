import math, time

#class TTEntry:
#    entry ('key', 'g_score', 's_depth', 'flag', 't_move')

class TranspositionTable:
    size = 2**20
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

            current_score = self.search(s_depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER, 0)

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
            # We only need to check back as far as the last irreversible move
            # (pawn move or capture), which is tracked by the halfmove_clock.
            limit = min(self.board.halfmove_clock, len(self.board.stack))
            
            if limit < 4: # Need at least 4 plies (2 full moves) to repeat start pos
                return False

            h = self.board.hash
            count = 0
            
            # Iterate backwards only up to the limit
            # stack entry: (mv, captured_idx, is_ep, old_ep, old_castle, old_clock, old_hash)
            # We want entry[6] -> old_hash
            for i in range(1, limit + 1):
                # Look at the N-th most recent entry
                entry = self.board.stack[-i]
                
                if entry[6] == h:
                    count += 1
                    if count >= 1: # Found 1 previous instance + current = 2 repetitions? 
                        # NOTE: Strict rules require 3 occurrences (count >= 2 here).
                        # However, many engines prune at 2 to avoid the draw trap early.
                        # Use '>= 2' for strict rule compliance, '>= 1' for safety.
                        return True
                        
            return False

    def search(self, s_depth, alpha, beta, ply):
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
            local_score = -self.search(s_depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            if local_score >= beta:
                return local_score
        
        is_pv_node = beta > alpha + 1
        stand_pat = self.board.evaluate()

        if not is_pv_node and not in_check:
            # Futility pruning (low eval)
            if s_depth <= 2 and stand_pat + 100 * s_depth <= alpha:
                return stand_pat

            # Razor pruning (high eval)
            if s_depth <= 3 and stand_pat >= beta - 80 * s_depth:
                return stand_pat
            
            if s_depth <= 4 and self.board.eval_material() <= -500:
                return stand_pat

        best_score = -1e9
        best_move = None
        played_moves = 0
        alpha_orig = alpha

        for t_move in sorted(self.board.gen_pseudo_legal(), key=self.board.score_move, reverse=True):
            played_moves += 1
            
            self.board.make_move(t_move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue

            d = s_depth - 1
            if d > 1 and played_moves > 4 and not (in_check or t_move[2] or t_move[3]):
                d -= 1 + (played_moves > 15) + (s_depth > 7)

            # 2. First Search (PV gets full window, others get Zero Window + Reduced Depth)
            g_score = -self.search(d, -alpha - 1 if played_moves > 1 else -beta, -alpha, ply + 1)

            # 3. Re-Searches (Only if the cheap search failed low/high incorrectly)
            if played_moves > 1 and g_score > alpha:
                # Research 1: If we reduced depth but the move is good, verify at full depth (Zero Window)
                if d < s_depth - 1:
                    g_score = -self.search(s_depth - 1, -alpha - 1, -alpha, ply + 1)
                
                # Research 2: If the move beats Alpha (and we are in a PV node), verify at Full Window
                if g_score < beta:
                    g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            # g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)

            # print(f"{self.board.move_to_uci(t_move)} {self.board.evaluate()} {g_score}")

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

        if played_moves == 0:
            return -self.MATE_SCORE_UPPER + ply if in_check else 0

        if not self.time_up:
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

        if q_depth >= 8 or stand_pat >= beta:
            return stand_pat

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        alpha = max(alpha, stand_pat)

        for t_move in sorted(self.board.gen_pseudo_legal(True), key=self.board.score_move, reverse=True):
            self.board.make_move(t_move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
            
            g_score = -self.q_search(-beta, -alpha, q_depth + 1)
            
            self.board.unmake_move()
            
            if self.time_up:
                break

            if g_score >= beta:
                return g_score
            if g_score > alpha:
                alpha = g_score
            
        return alpha
    