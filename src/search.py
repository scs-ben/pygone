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
    MATE_SCORE_UPPER = 32000
    TIME_CUT = 1e8
    Q_MAX_DEPTH = 20
    
    def __init__(self, board, tt_size_bytes=2_147_483_648):
        self.board = board
        self.nodes = 0
        self.tt = TranspositionTable(size_bytes=tt_size_bytes)
        self.time_limit = None      # seconds
        self.end_time = None
        self.time_up = False
        self.depth = 50
        self.killer_moves = [[None, None] for _ in range(64)]
        self.history_table = [[0] * 64 for _ in range(64)]

    def clear_tables(self):
        """Called at the start of a new top-level search."""
        self.killer_moves = [[None, None] for _ in range(64)]
        self.history_table = [[0] * 64 for _ in range(64)]

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

    def score_killer_move(self, move, ply, tt_move):
        # 1. Transposition Table Move (Highest Priority)
        if tt_move and move == tt_move:
            return 9000000  # Highest possible score

        # 2. Promotions
        if move.promo:
            # Use a high score, prioritizing Queen
            return 8000000 + self.board.PIECE_VALUES[move.promo] * 10
        
        # 3. Captures (MVV-LVA - Your existing logic)
        if move.capture:
            # NOTE: Your board needs a PIECE_VALUES property
            # Consider using a higher base score for captures than for quiet moves
            victim_value = self.board.PIECE_VALUES[move.capture]
            attacker_value = self.board.PIECE_VALUES[move.piece]
            # Simple scaling to keep this range between 7M and 8M
            return 7000000 + 10 * victim_value - attacker_value
            # *For maximum strength, this should be replaced by Static Exchange Evaluation (SEE)*
        
        # --- Quiet Moves (Lower Priority) ---
        
        # 4. Killer Moves
        if move == self.killer_moves[ply][0]:
            return 600000  # High score for primary killer
        if move == self.killer_moves[ply][1]:
            return 500000  # Slightly lower for secondary killer

        # 5. History Heuristic
        # Assuming move provides from_sq and to_sq indices (0-63)
        from_sq_idx = move.from_sq
        to_sq_idx = move.to_sq
        
        # History scores are typically much smaller, e.g., max 10000.
        return self.history_table[from_sq_idx][to_sq_idx]

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        best_score = None
        
        self.nodes = 0
        self.clear_tables()

        for depth in range(1, self.depth + 1):  # iterative deepening
            if self.time_up:
                break

            best_score = self.search(depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            if not self.time_up:
                entry = self.tt.probe(self.board.hash)
                if entry and entry.move:
                    best_move = entry.move

                elapsed_time = time.time() - start_time
                nps = math.ceil(self.nodes / elapsed_time) if elapsed_time > 0 else 1

                uci_move = self.board.move_to_uci(best_move) if best_move else None
                self.print_stats(str(depth), str(math.ceil(best_score)), str(math.ceil(elapsed_time * 1000)), str(self.nodes), str(nps), str(uci_move))

            if self.time_up or self.time_limit and time.time() >= self.end_time:
                self.time_up = True
                break
            
            if depth >= self.depth:
                break

        # When time expires, return the best move/eval found
        return best_move, best_score

    def threefold(self):
        count = 1
        
        for entry in self.board.history:
            count += entry[-1] == self.board.hash
            if count >= 3:
                return True
            
        return False

    def has_sufficient_material(self):
        """
        board: object with bitboards like board.white_pawns, board.white_knights, etc.
        is_white: whether to check for white or black
        """
        pawns  = bin(self.board.white_pawns).count('1')
        minors = bin(self.board.white_knights).count('1') + bin(self.board.white_bishops).count('1')
        majors = bin(self.board.white_rooks).count('1') + bin(self.board.white_queens).count('1')

        return pawns > 0 or minors + majors >= 2

    def search(self, depth, alpha=-MATE_SCORE_UPPER, beta=MATE_SCORE_UPPER, ply=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
            
        in_check = self.board.in_check()
        
        depth += in_check
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if depth == 0:
            return self.q_search(alpha, beta)
        
        is_pv_node = beta > alpha + 1
        alpha_orig = alpha

        self.nodes += 1
        
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
                return alpha # if entry.flag == 'UPPERBOUND' else beta

        if not is_pv_node and not in_check:
            stand_pat = self.board.evaluate()
            
            # Futility pruning (low eval)
            if depth <= 2 and stand_pat + 100 * depth <= alpha:
                return stand_pat

            # Razor pruning (high eval)
            if depth <= 3 and stand_pat >= beta - 80 * depth:
                return stand_pat

        if not is_pv_node and not in_check and depth <= 5:
            cut_boundary = alpha - (150 * depth)
            if stand_pat <= cut_boundary:
                if depth <= 2:
                    return self.q_search(alpha, alpha + 1)

                local_score = self.q_search(cut_boundary, cut_boundary + 1)

                if local_score <= cut_boundary:
                    return local_score

        # Null move pruning (only when safe)
        if (
            not is_pv_node
            and not in_check
            and depth >= 3
            and self.has_sufficient_material()
        ):
            reduction = 2 + depth / 6 # typical reduction
            self.board.nullmove()

            # skip if nullmove leaves us in check (can happen in some custom rulesets)
            if not self.board.in_check(False):
                null_score = -self.search(depth - reduction - 1, -beta, -beta + 1)

                if null_score >= beta:
                    self.board.unmove()
                    return beta
                
                self.board.unmove()

        if not is_pv_node and not in_check and entry and entry.move and entry.depth >= depth and abs(entry.score) < self.MATE_SCORE_UPPER:
            self.board.move_tuple(entry.move)
            local_score = -self.search(depth - 1, -beta, -alpha)
            self.board.unmove()

            if local_score >= beta:
                return beta

        best_score = -float('inf')
        best_move = None

        played_moves = 0
        
        all_moves = list(sorted(self.board.generate_pseudo_legal_moves(), key=self.board.score_move, reverse=True))
        
        scored_moves = []
        for move in all_moves:
             # Pass the current ply and the tt_move
             score = self.score_killer_move(move, ply, entry.move if entry else None)
             scored_moves.append((score, move))
             
        sorted_moves = sorted(scored_moves, key=lambda x: x[0], reverse=True)

        for score, move in sorted_moves:
            self.board.move_tuple(move)
                      
            if self.board.in_check(False):
                self.board.unmove()
                continue

            played_moves += 1
            
            is_quiet = not move.capture and not move.promo

            reduction = 1
            if is_quiet and depth >= 3 and played_moves > 3:
                reduction = int(0.75 + math.log(depth) * math.log(played_moves) / 2)

            if reduction > 0:
                score = -self.search(depth - reduction, -alpha-1, -alpha, ply + 1)

            if score > alpha:
                score = -self.search(depth - 1, -alpha-1, -alpha, ply + 1)
                if is_pv_node and score > alpha:
                    score = -self.search(depth - 1, -beta, -alpha, ply + 1)
            
            # score = -self.search(depth - 1, -beta, -alpha)
            
            if self.time_up:
                self.board.unmove()
                break
            
            self.board.unmove()

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            
            if alpha >= beta:
                if is_quiet:
                    # Update Killer Heuristic
                    self.killer_moves[ply][1] = self.killer_moves[ply][0] # Move old killer to slot 1
                    self.killer_moves[ply][0] = move                      # New killer in slot 0
                    
                    # Update History Heuristic (e.g., add 1 to the score)
                    from_sq_idx = move.from_sq
                    to_sq_idx = move.to_sq
                    # Increase history score, possibly scaled by depth (e.g. depth * depth)
                    self.history_table[from_sq_idx][to_sq_idx] += depth * depth
                    # Limit the score to prevent overflow/bias (e.g., max 10000)
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
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
        
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # if q_depth >= self.Q_MAX_DEPTH:
        #     # Stop searching noisy moves and return the static evaluation
        #     return self.board.evaluate()
        
        in_check = self.board.in_check()
        
        stand_pat = self.board.evaluate()
        
        if not in_check:
            stand_pat = self.board.evaluate()
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            # If in check, stand_pat is irrelevant, alpha remains the score to beat
            stand_pat = -float('inf')
        
        self.nodes += 1
        
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
                return alpha
        
        if not in_check and stand_pat >= beta:
            return stand_pat
        
        alpha_orig = alpha

        for move in sorted(self.board.generate_pseudo_legal_moves(active=not in_check), key=self.board.score_move, reverse=True):
            self.board.move_tuple(move)
            
            if self.board.in_check(False):
                self.board.unmove()
                continue
            
            score = -self.q_search(-beta, -alpha, q_depth + 1)
            
            if self.time_up:
                self.board.unmove()
                break
            
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
        