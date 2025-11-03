#!/usr/bin/env python3
import sys, time
from board2 import Board  # adjust imports to your setup

class Perft:
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    def __init__(self, board):
        self.board = board
        self.perft_captures = 0
        self.perft_checks = 0

    def perft(self, depth):
        """Bitboard-based perft with captures/checks counters."""
        if depth == 0:
            return 1

        total = 0
        
        for move in self.board.generate_pseudo_legal_moves():
            self.board.move_tuple(move)  # apply tuple-based move

            if self.board.in_check(False):
                self.board.unmove()
                continue

            # Track captures
            if move.capture:  # captured piece is not None
                self.perft_captures += 1

            # Track checks
            if self.board.in_check():  # check after move
                self.perft_checks += 1

            total += self.perft(depth - 1)

            self.board.unmove()  # undo move

        return total

    def perft_divide(self, depth):
        """Perft divide for debugging: prints per-move counts."""
        total = 0

        for move in self.board.generate_pseudo_legal_moves():
            self.board.move_tuple(move)
            
            if self.board.in_check(False):
                print(self.board.move_to_uci(move))
                self.board.unmove()
                continue
            
            # Track captures
            if move.capture:  # captured piece is not None
                self.perft_captures += 1

            # Track checks
            if self.board.in_check():  # check after move
                self.perft_checks += 1
                
            count = self.perft(depth - 1)
            print(f"{self.board.move_to_uci(move)}: {count}")
            total += count
            self.board.unmove()

        print(f"Total nodes: {total} Captures: {self.perft_captures} Checks: {self.perft_checks}")
        return total

    def run(self, depth): 
        self.perft_captures = 0
        self.perft_checks = 0
        
        t0 = time.time()
        nodes = self.perft_divide(depth)
        elapsed = time.time() - t0

        print(f"\nDepth {depth}: {nodes} nodes in {elapsed:.2f}s ({nodes/elapsed:.0f} NPS)")
