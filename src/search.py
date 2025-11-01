import math, time

class Search:
    v_nodes = 0
    v_depth = 0
    end_time = 0
    critical_time = 0
    tt_bucket = {}

    eval_exact = 1
    eval_upper = 2
    eval_lower = 3

    eval_mate_upper = 32767

    def print_stats(self, v_depth, v_score, v_time, v_nodes, v_nps, v_pv):
        print(f"info depth {v_depth} score cp {v_score} time {v_time} nodes {v_nodes} nps {v_nps} pv {v_pv}", flush=True)

    def reset(self):
        self.v_nodes = 0
        self.v_depth = 0
        self.end_time = 0
        self.critical_time = 0
        self.tt_bucket.clear()

    def iterative_search(self, local_board):
        start_time = time.time()

        local_score = local_board.rolling_score
        for v_depth in range(1, 100):
            local_score = self.search(local_board, v_depth, -self.eval_mate_upper, self.eval_mate_upper)

            if time.time() < self.critical_time:
                best_move = self.tt_bucket.get(local_board.board_string)
                if best_move:
                    best_move = best_move['tt_move']
            else:
                break

            elapsed_time = time.time() - start_time

            v_nps = math.ceil(self.v_nodes / elapsed_time) if elapsed_time > 0 else 1

            pv = ''
            counter = 1
            pv_board = local_board.make_move(best_move)
            while counter < min(6, v_depth):
                counter += 1

                pv_entry = self.tt_bucket.get(pv_board.board_string)

                if not pv_entry or not pv_entry['tt_move']:
                    break

                pv_board = pv_board.make_move(pv_entry['tt_move'])

                pv += ' ' + pv_entry['tt_move']

            self.print_stats(str(v_depth), str(math.ceil(local_score)), str(math.ceil(elapsed_time * 1000)), str(self.v_nodes), str(v_nps), str(best_move + pv))

            yield v_depth, best_move, local_score

    def ordered_moves(self, local_board, tt_move=None):
        if tt_move:
            yield tt_move
        for move in sorted(local_board.generate_valid_moves(), key=local_board.move_sort, reverse=True):
            if move != tt_move:
                yield move

    def search(self, local_board, v_depth, alpha, beta):
        if time.time() > self.critical_time:
            return local_board.rolling_score

        is_pv_node = beta > alpha + 1
        is_in_check = local_board.in_check(local_board.played_move_count % 2 == 0)

        v_depth += is_in_check # and not is_pv_node

        if (local_board.repetitions.count(local_board.board_string) > 2 or local_board.move_counter >= 100):
            return 0

        if v_depth <= 0:
            return self.q_search(local_board, alpha, beta, 200)

        tt_entry = self.tt_bucket.get(local_board.board_string, {'tt_value': 2*self.eval_mate_upper, 'tt_flag': self.eval_upper, 'tt_depth': -1, 'tt_move': None})

        self.v_nodes += 1

        original_alpha = alpha

        if tt_entry['tt_depth'] >= v_depth and tt_entry['tt_move'] and not is_pv_node:
            if tt_entry['tt_flag'] == self.eval_exact or \
            (tt_entry['tt_flag'] == self.eval_lower and tt_entry['tt_value'] >= beta) or \
            (tt_entry['tt_flag'] == self.eval_upper and tt_entry['tt_value'] <= alpha):
                return tt_entry['tt_value']

        if not is_pv_node and not is_in_check and v_depth <= 7 and local_board.rolling_score >= beta + (100 * v_depth):
            return local_board.rolling_score

        # if not is_pv_node and not is_in_check and v_depth <= 2 and local_board.rolling_score <= alpha - (350 * v_depth):
        #     return local_board.rolling_score

        if not is_pv_node and not is_in_check and v_depth <= 5:
            cut_boundary = alpha - (385 * v_depth)
            if local_board.rolling_score <= cut_boundary:
                if v_depth <= 2:
                    return self.q_search(local_board, alpha, alpha + 1, 200)

                local_score = self.q_search(local_board, cut_boundary, cut_boundary + 1, 200)

                if local_score <= cut_boundary:
                    return local_score

        best_score = -self.eval_mate_upper - 1
        local_score = -self.eval_mate_upper

        is_white = local_board.played_move_count % 2 == 0

        pieces = 'RNBQ' if is_white else 'rnbq'

        if not is_pv_node and not is_in_check and any(p in local_board.board_string for p in pieces):
            local_score = -self.search(local_board.nullmove(), v_depth - 4, -beta, -beta+1)

            if local_score >= beta:
                return beta

        if not is_pv_node and not is_in_check and tt_entry['tt_depth'] >= v_depth and abs(tt_entry['tt_value']) < self.eval_mate_upper and tt_entry['tt_move']:
            local_score = -self.search(local_board.make_move(tt_entry['tt_move']), v_depth - 1, -beta, -alpha)

            if local_score >= beta:
                return beta

        played_moves = 0

        best_move = None
    
        for s_move in self.ordered_moves(local_board, tt_entry.get('tt_move')):
            moved_board = local_board.make_move(s_move)

            # print(f"{s_move} {moved_board.rolling_score}")

            # determine legality: if we moved and are in check, it's not legal
            if moved_board.in_check(is_white):
                continue

            is_quiet = local_board.piece_count == moved_board.piece_count

            played_moves += 1

            r_depth = 1
            if is_quiet and v_depth > 2 and played_moves > 1:
                r_depth = max(3, math.ceil(math.sqrt(v_depth-1) + math.sqrt(played_moves-1)))

            if r_depth != 1:
                local_score = -self.search(moved_board, v_depth - r_depth, -alpha-1, -alpha)

            if (r_depth != 1 and local_score > alpha) or (r_depth == 1 and not(is_pv_node and played_moves == 1)):
                local_score = -self.search(moved_board, v_depth - 1, -alpha-1, -alpha)

            if is_pv_node and (played_moves == 1 or local_score > alpha):
                local_score = -self.search(moved_board, v_depth - 1, -beta, -alpha)

            if not best_move:
                best_move = s_move

            if local_score > best_score:
                best_move = s_move
                best_score = local_score

                if local_score > alpha:
                    alpha = local_score

                    if alpha >= beta:
                        break

        if not played_moves:
            return -self.eval_mate_upper + local_board.played_move_count if is_in_check else 0

        #update TT only if we are not in time cut
        if time.time() < self.critical_time:
            tt_entry['tt_value'] = best_score
            if best_move:
                tt_entry['tt_move'] = best_move
            tt_entry['tt_depth'] = v_depth
            if best_score <= original_alpha:
                tt_entry['tt_flag'] = self.eval_upper
            elif best_score >= beta:
                tt_entry['tt_flag'] = self.eval_lower
            else:
                tt_entry['tt_flag'] = self.eval_exact

            self.tt_bucket[local_board.board_string] = tt_entry
        else:
            self.tt_bucket[local_board.board_string] = {'tt_value': 2*self.eval_mate_upper, 'tt_flag': self.eval_upper, 'tt_depth': -1, 'tt_move': None}

        return best_score

    def q_search(self, local_board, alpha, beta, v_depth):
        if time.time() > self.critical_time:
            return -self.eval_mate_upper

        if local_board.repetitions.count(local_board.board_string) > 2 or local_board.move_counter >= 100:
            return 0

        tt_entry = self.tt_bucket.get(local_board.board_string)

        if tt_entry:
            if tt_entry['tt_flag'] == self.eval_exact or \
            (tt_entry['tt_flag'] == self.eval_lower and tt_entry['tt_value'] >= beta) or \
            (tt_entry['tt_flag'] == self.eval_upper and tt_entry['tt_value'] <= alpha):
                return tt_entry['tt_value']

        local_score = local_board.rolling_score

        if v_depth <= 0 or local_score >= beta:
            return local_score

        alpha = max(alpha, local_score)

        played_moves = 0

        if local_board.in_check(local_board.played_move_count % 2 == 0):
            moves = local_board.generate_valid_moves()
        else:
            moves = local_board.generate_valid_captures()

        for s_move in sorted(moves, key=local_board.move_sort, reverse=True):
            moved_board = local_board.make_move(s_move)

            # determine legality: if we moved and are in check, it's not legal
            if moved_board.in_check(local_board.played_move_count % 2 == 0):
                continue

            # only count a node once we have a legal move
            #if played_moves == 0:
            self.v_nodes += 1

            played_moves += 1

            local_score = -self.q_search(moved_board, -beta, -alpha, v_depth - 1)

            if local_score > alpha:
                alpha = local_score

                if alpha >= beta:
                    return alpha

        return alpha