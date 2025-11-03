import math, time
import numpy as np

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
        self.table = np.empty(self.size, dtype=object)

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
    def __init__(self, board, tt_size_bytes=2_147_483_648):
        self.board = board
        self.nodes = 0
        self.tt = TranspositionTable(size_bytes=tt_size_bytes)

    def print_stats(self, depth, score, time, notes, nps, pv):
        print(f"info depth {depth} score cp {score} time {time} nodes {notes} nps {nps} pv {pv}", flush=True)

    def iterative_search(self):
        start_time = time.time()

        local_score = self.board.evaluate()
        for depth in range(1, 100):
            local_score = self.search(depth, -float('inf'), float('inf'))

            # if time.time() < self.critical_time:
            entry = self.tt.probe(self.board.hash)
            # else:
                # break

            elapsed_time = time.time() - start_time

            nps = math.ceil(self.nodes / elapsed_time) if elapsed_time > 0 else 1

            uci_move = self.board.move_to_uci(entry.move)

            self.print_stats(str(depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time * 1000)), str(self.nodes), str(nps), str(uci_move))

            yield depth, entry.move, local_score

    def search(self, depth, alpha=-float('inf'), beta=float('inf')):
        self.nodes += 1
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

        # --- Leaf node ---
        if depth == 0:
            return self.board.evaluate()

        best_score = -float('inf')
        best_move = None

        for move in sorted(self.board.generate_pseudo_legal_moves(), key=self.board.score_move, reverse=True):
            self.board.move_tuple(move)
            score = -self.search(depth - 1, -beta, -alpha)
            self.board.unmove()

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # beta cutoff

        # --- Store in TT ---
        if best_score <= alpha_orig:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'
        else:
            flag = 'EXACT'

        self.tt.store(self.board.hash, depth, best_score, flag, best_move)

        return best_score