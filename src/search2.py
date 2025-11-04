import math, time

class TTEntry:
    __slots__ = ('key', 'score', 'depth', 'flag', 'move')
    def __init__(self, key=0, score=0, depth=0, flag='EXACT', move=None):
        self.key = key
        self.score = score
        self.depth = depth
        self.flag = flag
        self.move = move

class TranspositionTable:
    def __init__(self, size_bytes=2_147_483_648):
        entry_size = 32  # approximate bytes per entry
        self.size = size_bytes // entry_size
        self.table = [None] * self.size

    def index(self, zobrist_key):
        return zobrist_key % self.size

    def store(self, key, depth, score, flag, move):
        idx = self.index(key)
        entry = self.table[idx]
        # Replace if empty or shallower than current
        if entry is None or entry.depth <= depth:
            self.table[idx] = TTEntry(key, score, depth, flag, move)

    def probe(self, key):
        idx = self.index(key)
        entry = self.table[idx]
        if entry is not None and entry.key == key:
            return entry
        return None

class Search:
    MATE_SCORE_UPPER = 270000
    Q_MAX_DEPTH = 200
    
    def __init__(self, board, tt_size_bytes=2_147_483_648):
        self.board = board
        self.nodes = 0
        self.tt = TranspositionTable(size_bytes=tt_size_bytes)
        self.time_limit = None      # seconds
        self.end_time = None
        self.time_up = False
        self.depth = 50

    def set_time_limit(self, seconds):
        self.time_limit = seconds
        self.end_time = time.time() + seconds
        self.time_up = False
        
    def set_depth(self, depth):
        self.depth = depth

    def set_board(self, board):
        self.board = board

    def print_stats(self, depth, score, time, notes, nps, pv):
        print(f"info depth {depth} score cp {score} time {time} nodes {notes} nps {nps} pv {pv}", flush=True)

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        best_score = None
        
        self.nodes = 0

        for depth in range(1, 100):  # iterative deepening
            if self.time_up:
                break

            best_score = self.search(depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            entry = self.tt.probe(self.board.hash)
            if entry and entry.move:
                best_move = entry.move

            elapsed_time = time.time() - start_time
            nps = math.ceil(self.nodes / elapsed_time) if elapsed_time > 0 else 1

            uci_move = self.board.move_to_uci(best_move) if best_move else None
            self.print_stats(str(depth), str(math.ceil(best_score)), str(math.ceil(elapsed_time * 1000)), str(self.nodes), str(nps), str(uci_move))

            if self.time_limit and time.time() >= self.end_time:
                self.time_up = True
                break
            
            if depth >= self.depth:
                break

        # When time expires, return the best move/eval found
        return best_move, best_score

    def threefold(self):
        count = 0
        
        for entry in self.board.history:
            count += entry[-1] == self.board.hash
            if count >= 3:
                break
            
        return count >= 3

    def search(self, depth, alpha=-MATE_SCORE_UPPER, beta=MATE_SCORE_UPPER):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return alpha
            
        in_check = self.board.in_check()
        
        depth += in_check
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if depth == 0:
            return self.q_search(alpha, beta)
        
        # is_pv_node = beta > alpha + 1
        alpha_orig = alpha

        # --- TT lookup ---
        entry = self.tt.probe(self.board.hash)
        if entry and entry.depth >= depth:
            if entry.flag == 'EXACT':
                return entry.score
            elif entry.flag == 'LOWERBOUND':
                alpha = max(alpha, entry.score)
            elif entry.flag == 'UPPERBOUND':
                beta = min(beta, entry.score)
            if alpha >= beta:
                return entry.score

        self.nodes += 1

        best_score = -float('inf')
        best_move = None

        played_moves = 0

        for move in sorted(self.board.generate_pseudo_legal_moves(), key=self.board.score_move, reverse=True):
            self.board.move_tuple(move)
                      
            if self.board.in_check(False):
                self.board.unmove()
                continue

            played_moves += 1
            
            score = -self.search(depth - 1, -beta, -alpha)
            
            self.board.unmove()

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # beta cutoff
            
        if not played_moves:
            return -self.MATE_SCORE_UPPER + depth if self.board.in_check() else 0

        # --- Store in TT ---
        if best_score <= alpha_orig:
            flag = 'UPPERBOUND'
            # Note: Do NOT store best_move for UPPERBOUND as it's unreliable
            tt_move = None 
        elif best_score >= beta:
            flag = 'LOWERBOUND'
            # Store the move that caused the cutoff (Refutation Move)
            tt_move = best_move 
        else:
            flag = 'EXACT'
            # Store the best move found
            tt_move = best_move

        if not self.time_up:
            # Pass the appropriate move (tt_move) to the store function
            self.tt.store(self.board.hash, depth, best_score, flag, tt_move)

        return best_score
    
    def q_search(self, alpha, beta, q_depth=0):
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        if q_depth >= self.Q_MAX_DEPTH:
            # Stop searching noisy moves and return the static evaluation
            return self.board.evaluate()
        
        in_check = self.board.in_check()
        
        if not in_check:
            stand_pat = self.board.evaluate()
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            # If in check, stand_pat is irrelevant, alpha remains the score to beat
            stand_pat = -float('inf')
        
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return alpha
        
        # TT lookup
        entry = self.tt.probe(self.board.hash)
        if entry and entry.depth == 0:  # q-search "depth"
            if entry.flag == 'EXACT':
                return entry.score
            elif entry.flag == 'LOWERBOUND':
                alpha = max(alpha, entry.score)
            elif entry.flag == 'UPPERBOUND':
                beta = min(beta, entry.score)
            if alpha >= beta:
                return entry.score

        self.nodes += 1
        
        alpha_orig = alpha
        
        if not in_check and stand_pat >= beta:
            return beta

        for move in sorted(self.board.generate_pseudo_legal_moves(active=not in_check), key=self.board.score_move, reverse=True):
            self.board.move_tuple(move)
            
            if self.board.in_check(False):
                self.board.unmove()
                continue
            
            score = -self.q_search(-beta, -alpha, q_depth + 1)
            
            self.board.unmove()

            if score >= beta:
                # Store cutoff in TT
                if not self.time_up:
                    self.tt.store(self.board.hash, 0, beta, 'LOWERBOUND', move)
                return beta
            if score > alpha:
                alpha = score

        # --- Store in TT ---
        if alpha <= stand_pat: # If the best score is the stand-pat, or was not improved
            flag = 'EXACT' # Treat stand-pat or slight improvement as exact in Q-Search
            tt_move = None
        # If the score was reduced from a previous TT value (rare/edge case for Q-search)
        elif alpha <= alpha_orig: 
            flag = 'UPPERBOUND'
            tt_move = None
        else:
            flag = 'EXACT' # Or if alpha was improved
            tt_move = None
            
        if not self.time_up:
            # Note: TT for Q-search usually stores the stand_pat/final alpha
            self.tt.store(self.board.hash, 0, alpha, flag, tt_move)
            
        return alpha
        