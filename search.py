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

    def set_depth(self, depth): 
        self.s_depth = depth

    def set_board(self, board): 
        self.board = board

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
            if entry: 
                best_move = entry[4]
            
            # Minimal UCI Reporting
            elapsed = max(1, int((time.time() - start_time) * 1000))
            pv_str = self.board.move_to_uci(best_move) if best_move else ""
            nps = int(self.s_nodes * 1000 / elapsed)
            
            print(f"info depth {depth} score cp {int(score)} time {elapsed} nodes {self.s_nodes} nps {nps} pv {pv_str}", flush=True)

        # Final Best Move
        final_move = self.board.move_to_uci(best_move) if best_move else "0000"
        print(f"bestmove {final_move}", flush=True)

    def threefold(self):
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

    def search(self, depth, alpha, beta, ply):
        # Check time every 2048 nodes
        if (self.s_nodes & 2047) == 0 and time.time() > self.end_time:
            self.time_up = True
            return 0
            
        if self.threefold() or self.board.halfmove_clock >= 100 or self.board.is_insufficient_material(): 
            return 0

        in_check = self.board.in_check()

        # --- CHECK EXTENSION ---
        if in_check and depth < 4: 
             depth += 1
            
        if depth <= 0: 
            return self.q_search(alpha, beta)
        
        self.s_nodes += 1
        
        # --- TT PROBE ---
        tt_idx = self.board.hash % 1048576
        entry = self.tt[tt_idx]
        if entry and entry[0] == self.board.hash and entry[2] >= depth:
            if entry[3] == 0: return entry[1]
            if entry[3] == 1 and entry[1] >= beta: return entry[1]
            if entry[3] == 2 and entry[1] <= alpha: return entry[1]

        # --- NULL MOVE PRUNING ---
        # Disable NMP if in check
        if depth >= 3 and not in_check:
            self.board.make_move(None)
            score = -self.search(depth - 3, -beta, -beta + 1, ply + 1)
            self.board.unmake_move()
            
            if self.time_up: return 0
            if score >= beta: return score

        # --- REVERSE FUTILITY PRUNING ---
        # Disable RFP if in check
        stand_pat = self.board.evaluate()
        if depth < 4 and not in_check and stand_pat >= beta + depth * 80:
            return stand_pat

        best_score = -320000
        best_move = None
        
        # Generate and sort moves
        moves = sorted(self.board.gen_pseudo_legal(), key=self.board.score_move, reverse=True)
        
        if not moves:
            return -320000 + ply if in_check else 0

        moves_played = 0
        original_alpha = alpha
        
        for move in moves:
            self.board.make_move(move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
            
            moves_played += 1
            
            # --- LMR + PVS LOGIC ---
            reduction = 0
            # Don't reduce if in check, or if the move gives check (heuristic), or captures
            if depth > 2 and moves_played > 4 and not (in_check or move[2] or move[3]):
                reduction = 1 + (moves_played > 15)
            
            new_depth = depth - 1 - reduction
            
            if moves_played > 1:
                score = -self.search(new_depth, -alpha - 1, -alpha, ply + 1)
                if score > alpha and (score < beta or new_depth != depth - 1):
                    score = -self.search(depth - 1, -beta, -alpha, ply + 1)
            else:
                score = -self.search(depth - 1, -beta, -alpha, ply + 1)

            self.board.unmake_move()
            
            if self.time_up: return 0
            
            if score > best_score:
                best_score = score
                best_move = move
                
            if score > alpha:
                alpha = score
                if alpha >= beta:
                    self.tt[tt_idx] = [self.board.hash, alpha, depth, 1, move]
                    return alpha
        
        if moves_played == 0:
            return -320000 + ply

        flag = 0 if alpha > original_alpha else 2
        self.tt[tt_idx] = [self.board.hash, alpha, depth, flag, best_move]
        
        return alpha

    def q_search(self, alpha, beta):
        if (self.s_nodes & 2047) == 0 and time.time() > self.end_time:
            self.time_up = True
            return 0
        
        if self.threefold() or self.board.halfmove_clock >= 100 or self.board.is_insufficient_material(): 
            return 0

        self.s_nodes += 1
        
        # TT Probe (Q-Search)
        entry = self.tt[self.board.hash % 1048576]
        if entry and entry[0] == self.board.hash:
            if entry[3] == 0: return entry[1]
            if entry[3] == 1 and entry[1] >= beta: return entry[1]
            if entry[3] == 2 and entry[1] <= alpha: return entry[1]

        stand_pat = self.board.evaluate()
        if stand_pat >= beta: return beta
        if stand_pat > alpha: alpha = stand_pat
        
        # Active Moves Only (Captures/Promotions)
        for move in sorted(self.board.gen_pseudo_legal(True), key=self.board.score_move, reverse=True):
            if move[3] and (stand_pat + self.board.PIECE_VALUES[move[3]] + 200) < alpha and not move[2]: continue

            self.board.make_move(move)
            
            if self.board.in_check(False):
                self.board.unmake_move()
                continue
                
            score = -self.q_search(-beta, -alpha)
            self.board.unmake_move()
            
            if score >= beta: return beta
            if score > alpha: alpha = score
            
        return alpha