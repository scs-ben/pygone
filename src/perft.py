#!/usr/bin/env python3
import time

# Updated Perft Class (Focus on the Perft method changes)
class Perft:
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    # Initialize counters to 0, but they are now only used for the final result aggregation
    def __init__(self, board):
        self.board = board
        # These are now only for the final output in perft_divide/run
        self.total_captures = 0
        self.total_checks = 0

    def perft(self, depth):
        # Bitboard-based perft. Returns (total_nodes, captures, checks).
        # Captures/Checks are counted for moves *into* this position if depth is 0.
        if depth == 0:
            # Base case: Returns 1 node, 0 captures, 0 checks
            return 1, 0, 0 

        nodes = 0
        captures = 0
        checks = 0
        
        for move in self.board.generate_pseudo_legal_moves():
            is_capture = move.capture
            
            self.board.move_tuple(move)
            
            # 1. Legal check (Must NOT be in check *after* the move for the side whose turn it is now, 
            # which is the original side's opponent)
            if self.board.in_check(False): # 'False' means checking if the side who just moved is in check
                self.board.unmove()
                continue
            
            is_check = self.board.in_check() # Check if the *opponent* is in check
            
            # Recursive call
            sub_nodes, sub_captures, sub_checks = self.perft(depth - 1)
            
            # Aggregate counts from the subtree
            nodes += sub_nodes
            captures += sub_captures
            checks += sub_checks
            
            # If at the terminal level (depth 1), count the events for the current move.
            # *However*, the standard Perft logic is simplified by having the base case 
            # return 1 and aggregating the events on the way up. 
            
            # The correct Perft counting should track the events for the *current move*
            # only if the recursion is at the level *before* the terminal nodes (depth 1).
            # The most robust way is to do the counting in the base case for depth 1, 
            # but since we are accumulating, we count them here:
            if depth == 1:
                if is_capture:
                    captures += 1
                if is_check:
                    checks += 1
                
            self.board.unmove()

        return nodes, captures, checks

    def perft_divide(self, depth):
        # Perft divide for debugging: prints per-move counts.
        self.total_captures = 0
        self.total_checks = 0
        total_nodes = 0

        for move in self.board.generate_pseudo_legal_moves():
            is_capture = move.capture
            
            self.board.move_tuple(move)
            
            if self.board.in_check(False):
                self.board.unmove()
                continue
            
            is_check = self.board.in_check()
            
            # Recursive call (depth-1) returns counts for the subtree
            count, cap_count, check_count = self.perft(depth - 1)
            
            # Add the event from the *current* move if depth is 1 or more
            # Standard Perft only counts at the depth specified.
            if depth == 1:
                if is_capture:
                    cap_count += 1
                if is_check:
                    check_count += 1
            
            print(f"{self.board.move_to_uci(move)}: {count}")
            
            total_nodes += count
            self.total_captures += cap_count
            self.total_checks += check_count
            
            self.board.unmove()

        print(f"Total nodes: {total_nodes} Captures: {self.total_captures} Checks: {self.total_checks}")
        return total_nodes

    def run(self, depth): 
        # run resets the counters, which are now instance variables used for final result
        self.total_captures = 0
        self.total_checks = 0
        
        t0 = time.time()
        # perft_divide aggregates the results into instance variables and returns total nodes
        nodes = self.perft_divide(depth)
        elapsed = time.time() - t0

        print(f"Depth {depth}: {nodes} nodes in {elapsed:.2f}s ({nodes/elapsed:.0f} NPS)")