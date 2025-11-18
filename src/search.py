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
    def __init__(self, size_bytes=2_147_483_648):
        entry_size = 32  # approximate bytes per entry
        self.size = size_bytes // entry_size
        self.table = [None] * self.size

    def tt_index(self, zobrist_key):
        return zobrist_key % self.size

    def store(self, key, s_depth, g_score, flag, t_move):
        idx = self.tt_index(key)
        entry = self.table[idx]
        # Replace if empty or shallower than current
        if entry is None or entry.s_depth <= s_depth:
            self.table[idx] = TTEntry(key, g_score, s_depth, flag, t_move)

    def probe(self, key):
        idx = self.tt_index(key)
        entry = self.table[idx]
        if entry is not None and entry.key == key:
            return entry
        return None

class Search:
    MATE_SCORE_UPPER = 32000
    TIME_CUT = 1e8
    
    def __init__(self, board, tt_size_bytes=2_147_483_648):
        self.board = board
        self.s_nodes = 0
        self.tt = TranspositionTable(size_bytes=tt_size_bytes)
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

    def score_killer_move(self, t_move, ply, tt_move):
        # 1. Transposition Table Move (Highest Priority)
        if tt_move and t_move == tt_move:
            return 9000000  # Highest possible score

        # 2. Promotions
        if t_move[2]:
            # Use a high score, prioritizing Queen
            return 8000000 + self.board.PIECE_VALUES[t_move[2]] * 10
        
        # 3. Captures (MVV-LVA - Your existing logic)
        if t_move[3]:
            # NOTE: Your board needs a PIECE_VALUES property
            # Consider using a higher base score for captures than for quiet moves
            victim_value = self.board.PIECE_VALUES[t_move[3]]
            attacker_value = self.board.PIECE_VALUES[t_move[4]]
            # Simple scaling to keep this range between 7M and 8M
            return 7000000 + 10 * victim_value - attacker_value
            # *For maximum strength, this should be replaced by Static Exchange Evaluation (SEE)*
        
        # --- Quiet Moves (Lower Priority) ---
        
        # 4. Killer Moves
        if t_move == self.killer_moves[ply][0]:
            return 600000  # High score for primary killer
        if t_move == self.killer_moves[ply][1]:
            return 500000  # Slightly lower for secondary killer

        # 5. History Heuristic
        # Assuming move provides from_sq and to_sq indices (0-63)
        from_sq_idx = t_move[0]
        to_sq_idx = t_move[1]
        
        # History scores are typically much smaller, e.g., max 10000.
        return self.history_table[from_sq_idx][to_sq_idx]

    def iterative_search(self):
        start_time = time.time()
        best_move = None
        best_score = None
        
        self.s_nodes = 0
        self.clear_tables()

        for s_depth in range(1, self.s_depth + 1):  # iterative deepening
            if self.time_up:
                break

            best_score = self.search(s_depth, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)

            if not self.time_up:
                entry = self.tt.probe(self.board.hash)
                if entry and entry.t_move:
                    best_move = entry.t_move

                elapsed_time = time.time() - start_time
                nps = math.ceil(self.s_nodes / elapsed_time) if elapsed_time > 0 else 1

                uci_move = self.board.move_to_uci(best_move) if best_move else None
                self.print_stats(str(s_depth), str(math.ceil(best_score)), str(math.ceil(elapsed_time * 1000)), str(self.s_nodes), str(nps), str(uci_move))

            if self.time_up or self.time_limit and time.time() >= self.end_time:
                self.time_up = True
                break
            
            if s_depth >= self.s_depth:
                break

        best_score = self.search(1, -self.MATE_SCORE_UPPER, self.MATE_SCORE_UPPER)
        entry = self.tt.probe(self.board.hash)
        best_move = entry.t_move

        # When time expires, return the best move/eval found
        return best_move, best_score

    def threefold(self):
        count = 1
        
        for entry in self.board.stack:
            count += entry[-1] == self.board.hash
            if count >= 3:
                return True
            
        return False

    def has_sufficient_material(self):
        if self.board.white_to_move:
            pawns  = bin(self.board.P[0]).count('1')
            minors = bin(self.board.P[1]).count('1') + bin(self.board.P[2]).count('1')
            majors = bin(self.board.P[3]).count('1') + bin(self.board.P[4]).count('1')
        else:
            pawns  = bin(self.board.P[6]).count('1')
            minors = bin(self.board.P[7]).count('1') + bin(self.board.P[8]).count('1')
            majors = bin(self.board.P[9]).count('1') + bin(self.board.P[10]).count('1')

        return pawns > 0 or minors + majors >= 2



    def search(self, s_depth, alpha=-MATE_SCORE_UPPER, beta=MATE_SCORE_UPPER, ply=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
            
        in_check = self.board.in_check()
        
        s_depth += in_check
            
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        # --- Leaf node ---
        if s_depth == 0:
            return self.q_search(alpha, beta)
        
        is_pv_node = beta > alpha + 1
        alpha_orig = alpha

        self.s_nodes += 1
        
        # --- TT lookup ---
        entry = self.tt.probe(self.board.hash)
        if entry and entry.s_depth >= s_depth and entry.t_move and not is_pv_node:
            if entry.flag == 'EXACT' or \
                entry.flag == 'LOWERBOUND' and entry.g_score >= beta or \
                entry.flag == 'UPPERBOUND' and entry.g_score <= alpha:
                    return entry.g_score

        if not is_pv_node and not in_check:
            stand_pat = self.board.evaluate()
            
            # Futility pruning (low eval)
            if s_depth <= 2 and stand_pat + 100 * s_depth <= alpha:
                return stand_pat

            # Razor pruning (high eval)
            if s_depth <= 3 and stand_pat >= beta - 80 * s_depth:
                return stand_pat

        if not is_pv_node and not in_check and s_depth <= 5:
            cut_boundary = alpha - (150 * s_depth)
            if stand_pat <= cut_boundary:
                if s_depth <= 2:
                    return self.q_search(alpha, alpha + 1)

                local_score = self.q_search(cut_boundary, cut_boundary + 1)

                if local_score <= cut_boundary:
                    return local_score

        # Null move pruning (only when safe)
        if (
            not is_pv_node
            and not in_check
            and s_depth >= 3
            and self.has_sufficient_material()
        ):
            reduction = 2 + s_depth / 6 # typical reduction
            self.board.nullmove()

            # skip if nullmove leaves us in check (can happen in some custom rulesets)
            if not self.board.in_check(False):
                null_score = -self.search(s_depth - reduction - 1, -beta, -beta + 1)

                self.board.unmake_move()
                
                if null_score >= beta:
                    return beta
            else:
                self.board.unmake_move()

        if not is_pv_node and not in_check and entry and entry.t_move and entry.s_depth >= s_depth and abs(entry.g_score) < self.MATE_SCORE_UPPER:
            self.board.make_move(entry.t_move)
            local_score = -self.search(s_depth - 1, -beta, -alpha)
            self.board.unmake_move()

            if local_score >= beta:
                return beta

        best_score = -float('inf')
        best_move = None

        played_moves = 0
        
        all_moves = list(sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True))
        
        scored_moves = []
        for t_move in all_moves:
             # Pass the current ply and the tt_move
             g_score = self.score_killer_move(t_move, ply, entry.t_move if entry else None)
             scored_moves.append((g_score, t_move))
             
        sorted_moves = sorted(scored_moves, key=lambda x: x[0], reverse=True)

        for g_score, t_move in sorted_moves:
        # for t_move in sorted(self.board.gen_legal_moves(), key=self.board.score_move, reverse=True):
            self.board.make_move(t_move)

            played_moves += 1
            
            is_quiet = not t_move[3] and not t_move[2]

            reduction = 1
            if is_quiet and s_depth >= 3 and played_moves > 3:
                reduction = int(0.75 + math.log(s_depth) * math.log(played_moves) / 2)

            if reduction > 0:
                g_score = -self.search(s_depth - reduction, -alpha-1, -alpha, ply + 1)

            if g_score > alpha:
                g_score = -self.search(s_depth - 1, -alpha-1, -alpha, ply + 1)
                if is_pv_node and g_score > alpha:
                    g_score = -self.search(s_depth - 1, -beta, -alpha, ply + 1)
            
            # g_score = -self.search(s_depth - 1, -beta, -alpha)
            
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
                        break
            
            if alpha >= beta:
                if is_quiet:
                    # Update Killer Heuristic
                    self.killer_moves[ply][1] = self.killer_moves[ply][0] # Move old killer to slot 1
                    self.killer_moves[ply][0] = t_move                      # New killer in slot 0
                    
                    # Update History Heuristic (e.g., add 1 to the score)
                    from_sq_idx = t_move[0]
                    to_sq_idx = t_move[1]
                    # Increase history score, possibly scaled by s_depth (e.g. s_depth * s_depth)
                    self.history_table[from_sq_idx][to_sq_idx] += s_depth * s_depth
                    # Limit the score to prevent overflow/bias (e.g., max 10000)
                break  # beta cutoff
            
        if not played_moves:
            return -self.MATE_SCORE_UPPER + s_depth if self.board.in_check() else 0

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
            # Pass the appropriate move (tt_move) to the store function
            self.tt.store(self.board.hash, s_depth, best_score, flag, best_move)

        return best_score
    
    def q_search(self, alpha, beta, q_depth=0):
        if self.time_up or (self.time_limit and time.time() >= self.end_time):
            self.time_up = True
            return -self.TIME_CUT
        
        if self.threefold() or self.board.halfmove_clock >= 100:
            return 0
        
        in_check = self.board.in_check()
        
        stand_pat = self.board.evaluate()
        
        if not in_check:
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            # If in check, stand_pat is irrelevant, alpha remains the score to beat
            stand_pat = -float('inf')
        
        self.s_nodes += 1
        
        # TT lookup
        entry = self.tt.probe(self.board.hash)
        if entry and entry.s_depth == 0:  # q-search "s_depth"
            if entry.flag == 'EXACT' or \
                entry.flag == 'LOWERBOUND' and entry.g_score >= beta or \
                entry.flag == 'UPPERBOUND' and entry.g_score <= alpha:
                    return entry.g_score
        
        if not in_check and stand_pat >= beta:
            return stand_pat

        for t_move in sorted(self.board.gen_legal_moves(active=not in_check), key=self.board.score_move, reverse=True):
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
        