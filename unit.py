#!/usr/bin/env pypy3
#  pygone - A Python Chess Engine
#  Copyright (C) 2025 [Your Name/Handle]
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import io
import contextlib

class Unit:
    def _fail(self, msg):
        print(f"\nFAILED: {msg}")

    def unit_hash(self, b):
        print("Testing Hashing...", end="", flush=True)
        orig_hash = b.hash
        moves = b.gen_pseudo_legal()
        mv = moves[0][1]   # some legal move
        b.make_move(mv)
        b.unmake_move()

        if b.hash != orig_hash:
            self._fail(f"Zobrist mismatch after make/unmake. Start: {orig_hash}, End: {b.hash}")
            return

        orig_hash = b.compute_hash()
        moves = b.gen_pseudo_legal()
        moves = [m[1] for m in moves[:4]]
        for m in moves:
            b.make_move(m)
            b.unmake_move()
            
        h_inc = b.hash
        h_scratch = b.compute_hash()
        
        if h_inc != h_scratch:
            self._fail(f"Incremental != recompute. Inc: {h_inc}, Scratch: {h_scratch}")
            return
            
        print(" Passed!", flush=True)

    def parse_move(self, mv, b):
        from_sq = b.algebraic_to_sq(mv[:2])
        to_sq = b.algebraic_to_sq(mv[2:4])
        return (from_sq, to_sq, None, None, None, False)

    def unit_perft(self, perft, b):
        print("Testing Perft (Extended Suite)...", end="", flush=True)
        
        # Format: (FEN, Depth, (Depth, Nodes, Captures, Checks))
        test_cases = [
            # 1 Start Pos
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4, (4, 197281, 1576, 469)),
            # 2 Kiwipete
            ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ", 3, (3, 97862, 17102, 993)),
            # Position 3: Tricky En Passant & Pins
            # 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1
            ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", 4, (4, 43238, 3348, 1680)),

            # Position 4: "The Mirror" - Complex Castling & Promotions
            # r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1
            ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", 4, (4, 422333, 131393, 15492)),

            # Position 4*: "The Mirror" - Complex Castling & Promotions Mirrored
            # r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1 
            ("r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1 ", 4, (4, 422333, 131393, 15492)),

            # Position 5: "Buggy" - Promotions out of check
            # rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8
            ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", 3, (3, 62379, 8517, 1201)),

            # Position 6:
            # r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10 
            ("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10 ", 3, (3, 89890, 9470, 1783)),
        ]

        for fen, depth, expected in test_cases:
            b.set_fen(fen)
            results = perft.run(depth, True) # Assumes perft tracks context from board
            
            if results != expected:
                self._fail(f"\nFEN: {fen}\nDepth {depth}. Expected {expected}, Got {results}")
                return

        print(" Passed!", flush=True)

    def unit_moves(self, b):
        print("Testing Move Gen Integrity...", end="", flush=True)
        # 3) Board State Integrity Check
        b.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        orig_fen = b.get_fen()

        # Simple non-capture move
        mv = self.parse_move("e2e4", b) 
        b.make_move(mv)
        b.unmake_move()

        if b.get_fen() != orig_fen:
            self._fail("Board FEN mismatch after quiet make/unmake")
            return

        # Test a capture move
        b.set_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        orig_fen = b.get_fen()
        mv = self.parse_move("g8f6", b) # Test a non-capture
        b.make_move(mv)
        b.unmake_move()
        
        if b.get_fen() != orig_fen:
            self._fail("Board FEN mismatch after capture make/unmake")
            return

        print(" Passed!", flush=True)

    def unit_scoring(self, b):
        print('Testing Scoring...', end="", flush=True)
        
        b.set_fen("8/8/8/8/8/8/8/R7 w - - 0 1") # Rook vs no pieces
        score_r = b.evaluate()

        b.set_fen("8/8/8/8/8/8/8/N7 w - - 0 1") # Knight vs no pieces
        score_n = b.evaluate()

        if score_r <= score_n:
            self._fail(f"Material Error: Rook ({score_r}) <= Knight ({score_n})")
            return

        # Check symmetry (White score should be -Black score)
        b.set_fen("r7/8/8/8/8/8/8/8 w - - 0 1") # Black Rook vs no pieces
        score_br = b.evaluate()
        
        if score_r + score_br != 0:
            self._fail(f"Symmetry Error: White {score_r} + Black {score_br} != 0")
            return

        print(" Passed!", flush=True)

    def unit_castling(self, b):
        print("Testing Castling...", end="", flush=True)
        # ---------------------------------------
        # 5) Castling Integrity
        # ---------------------------------------
        b.set_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1") 
        orig_hash = b.hash
        
        # Move: White Castles Queenside (e1 -> c1)
        mv = (4, 2, None, None, None, None)
        b.make_move(mv)
        
        # Checks:
        if b.piece_map[2] != 5:  self._fail("King not on c1"); return
        if b.piece_map[3] != 3:  self._fail("Rook not on d1"); return
        if b.piece_map[0] != -1: self._fail("Rook still on a1"); return
        if (b.castle & 3) != 0:  self._fail("White castling rights not cleared"); return
        
        b.unmake_move()
        
        # Restore checks:
        if b.piece_map[4] != 5:  self._fail("King not back on e1"); return
        if b.piece_map[0] != 3:  self._fail("Rook not back on a1"); return
        if b.piece_map[2] != -1: self._fail("c1 not empty"); return
        if b.hash != orig_hash:  self._fail("Hash mismatch after Castle Unmake"); return

        print(" Passed!", flush=True)

    def unit_ep(self, b):
        print("Testing En Passant...", end="", flush=True)
        # ---------------------------------------
        # 6) En Passant Integrity
        # ---------------------------------------
        b.set_fen("8/8/8/3pP3/8/8/8/k6K w - d6 0 1")
        orig_hash = b.hash
        
        # Move: e5 -> d6 (En Passant Capture)
        mv = (36, 43, None, None, None, None)
        b.make_move(mv)
        
        # Checks:
        if b.piece_map[43] != 0:  self._fail("White pawn not on d6"); return
        if b.piece_map[35] != -1: self._fail("Black pawn on d5 not removed"); return
        
        b.unmake_move()
        
        # Restore checks:
        if b.piece_map[36] != 0:  self._fail("White pawn not back on e5"); return
        if b.piece_map[35] != 6:  self._fail("Black pawn not back on d5"); return
        if b.ep != 43:            self._fail("EP Square not restored"); return
        if b.hash != orig_hash:   self._fail("Hash mismatch after EP Unmake"); return
        
        print(" Passed!", flush=True)

    def unit_promo(self, b):
        print("Testing Promotion...", end="", flush=True)
        b.set_fen("8/P7/8/8/8/8/8/k6K w - - 0 1")
        orig_hash = b.hash

        # Find the move: a7 -> a8 (Queen promotion)
        moves = b.gen_pseudo_legal()
        promo_move = None
        for _, m in moves:
            if m[0] == 48 and m[1] == 56 and m[2] == 'q':
                promo_move = m
                break
        
        if promo_move is None:
            self._fail("Could not generate a7a8q move")
            return
        
        # --- EXECUTE MAKE ---
        b.make_move(promo_move)

        if b.piece_map[56] != 4:
            self._fail(f"Expected White Queen (4) at a8, got {b.piece_map[56]}")
            return
        
        if b.piece_map[48] != -1:
            self._fail("Source square a7 was not cleared")
            return
        
        if not (b.P[4] & (1 << 56)):
            self._fail("White Queen bitboard not updated")
            return

        if (b.P[0] & (1 << 48)):
            self._fail("White Pawn bitboard not cleared")
            return

        # --- EXECUTE UNMAKE ---
        b.unmake_move()

        if b.piece_map[56] != -1:
            self._fail("Promotion square a8 not cleared after unmake")
            return
        
        if b.piece_map[48] != 0:
            self._fail(f"Expected White Pawn (0) at a7, got {b.piece_map[48]}")
            return
        
        if b.hash != orig_hash:
            self._fail("Hash mismatch after Promotion Unmake")
            return

        print(" Passed!", flush=True)

    def unit_search(self, s, b):
        print("Testing Search Stability...", end="", flush=True)
        orig_fen = b.get_fen()
        orig_hash = b.hash

        # Silent search (suppress prints inside search if possible, or just ignore output)
        s.set_time_limit(1e8)
        s.set_depth(6)
        
        # Capture stdout to a dummy stream
        captured_output = io.StringIO()
        
        try:
            # Everything printed inside this 'with' block goes to captured_output
            with contextlib.redirect_stdout(captured_output):
                s.iterative_search()
        except Exception as e:
            self._fail(f"Search crashed with exception: {e}")
            return

        if b.hash != orig_hash:
            self._fail("Hash mismatch after search")
            return
            
        if b.get_fen() != orig_fen:
            self._fail("FEN mismatch (Board corruption) after search")
            return

        print(" Passed!", flush=True)

    def unit_threefold(self, s, b):
        print("Testing Threefold Repetition...", end="", flush=True)
        
        def make_uci(move_str, b):
            found = False
            for _, m in b.gen_pseudo_legal():
                if b.move_to_uci(m) == move_str:
                    b.make_move(m)
                    found = True
                    break
            return found

        repeat_seq = ["g1f3", "g8f6", "f3g1", "f6g8"]

        if s.threefold():
            self._fail("Start pos is not 3-fold")
            return

        # --- OCCURRENCE 2 ---
        for m in repeat_seq: 
            if not make_uci(m, b): self._fail(f"Illegal move {m}"); return
        
        if s.threefold():
            self._fail("2nd occurrence should not trigger strict 3-fold")
            return

        # --- OCCURRENCE 3 ---
        for m in repeat_seq: 
            if not make_uci(m, b): self._fail(f"Illegal move {m}"); return
        
        if not s.threefold():
            self._fail("3rd occurrence must trigger 3-fold")
            return
        
        # --- IRREVERSIBLE MOVE TEST ---
        if not make_uci("e2e4", b): self._fail("e2e4 illegal"); return
        if not make_uci("e7e5", b): self._fail("e7e5 illegal"); return
        
        # Repeat knights again
        for m in repeat_seq: make_uci(m, b)
        for m in repeat_seq: make_uci(m, b)
        
        if s.threefold():
            self._fail("Irreversible move (pawn push) should have reset counter")
            return

        print(" Passed!", flush=True)

    def unit_insufficient_material(self, b):
        print("Testing Insufficient Material...", end="", flush=True)
        
        test_cases = [
            ("8/8/8/8/8/4k3/8/4K3 w - - 0 1", True, "K vs K"),
            ("8/8/8/8/8/4k3/8/4K1N1 w - - 0 1", True, "K+N vs K"),
            ("8/8/8/8/8/4k3/8/4K1B1 w - - 0 1", True, "K+B vs K"),
            ("8/8/8/8/8/4k3/8/4K1n1 w - - 0 1", True, "K vs K+n"),
            ("8/8/8/8/8/4k3/8/4K1b1 w - - 0 1", True, "K vs K+b"),
            
            ("8/8/8/8/8/4k3/8/4K1Q1 w - - 0 1", False, "K+Q vs K"),
            ("8/8/8/8/8/4k3/8/4K1R1 w - - 0 1", False, "K+R vs K"),
            ("8/8/8/8/8/4k3/8/4K1P1 w - - 0 1", False, "K+P vs K"),
            ("8/8/8/8/8/4k3/8/4K1nn w - - 0 1", False, "K vs K+n+n"), 
            ("8/8/8/8/8/4k3/3b4/4K1N1 w - - 0 1", False, "K+N vs K+b")
        ]

        for fen, expected_draw, desc in test_cases:
            b.set_fen(fen)
            
            is_draw = b.is_insufficient_material()
            if is_draw != expected_draw:
                self._fail(f"{desc}. Expected {expected_draw}, got {is_draw}")
                return

            if expected_draw:
                score = b.evaluate()
                if score != 0:
                    self._fail(f"Score Error {desc}. Expected 0, got {score}")
                    return

        print(" Passed!", flush=True)

    def unit_game_end(self, b):
        print("Testing Game End Detection...", end="", flush=True)
        
        # Helper to count strictly legal moves
        def count_legal_moves(board):
            count = 0
            # active=False generates all pseudo-legal moves (quiet + captures)
            for _, m in board.gen_pseudo_legal(active=False):
                board.make_move(m)
                
                # FIX: check(False) checks the "passive" side (the one that just moved)
                if not board.in_check(False):
                    count += 1
                
                board.unmake_move()
            return count

        # 1. Checkmate (Fool's Mate Pattern)
        # White is in checkmate
        b.set_fen("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
        
        if not b.in_check(): 
            self._fail("Fool's Mate: White should be in check"); return
        if count_legal_moves(b) != 0: 
            self._fail("Fool's Mate: White should have 0 legal moves"); return

        # 2. Stalemate
        # White King at h1, Black Queen at g3. White to move.
        b.set_fen("8/8/8/8/8/6q1/8/7K w - - 0 1")
        
        if b.in_check(): 
            self._fail("Stalemate: White should NOT be in check"); return
        if count_legal_moves(b) != 0: 
            self._fail("Stalemate: White should have 0 legal moves"); return

        print(" Passed!", flush=True)

    def unit_mate_in_n(self, s, b):
        print("Testing Mate Search...", end="", flush=True)
        import io
        import sys
        
        # (FEN, Depth, Expected Move String)
        tests = [
            # Mate in 1: White Rook to a8 (The only winning move)
            ("7k/R7/8/8/8/8/8/7K w - - 0 1", 2, "a7a8"),
            
            # Mate in 1: Scholar's Mate (Qf7#)
            ("r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 4 4", 2, "f3f7")
        ]

        for fen, depth, expected in tests:
            b.set_fen(fen)
            s.set_board(b)
            s.set_depth(depth)
            s.set_time_limit(1000) # 1 second is plenty

            # Capture standard output to read "bestmove"
            capture = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = capture
            
            try:
                s.iterative_search()
            finally:
                # Always restore stdout so we can see errors if it crashes
                sys.stdout = old_stdout
            
            # Parse output
            output = capture.getvalue()
            found_move = ""
            for line in output.splitlines():
                if line.startswith("bestmove"):
                    parts = line.split()
                    if len(parts) > 1:
                        found_move = parts[1]
                    break
            
            if found_move != expected:
                self._fail(f"FEN: {fen}\nExpected {expected}, Got '{found_move}'")
                return

        print(" Passed!", flush=True)

    def unit_fifty_move(self, b):
        print("Testing Fifty-Move Rule...", end="", flush=True)
        
        # 1. Verify Draw at 100
        b.set_fen("8/8/8/8/8/4k3/4P3/4K3 w - - 0 1")
        b.halfmove_clock = 99
        
        # Make a quiet king move: e1 -> f1
        f = b.algebraic_to_sq("e1")
        t = b.algebraic_to_sq("f1")
        b.make_move((f, t, None, None, 'k', False))
        
        if b.halfmove_clock != 100:
            self._fail(f"Clock did not increment to 100. Got {b.halfmove_clock}")
            return
        
        # In search/eval, this should now score 0 (Draw)
        score = b.evaluate()
        if score != 0:
            self._fail(f"Board did not evaluate to 0 (Draw) at 100 halfmoves. Got {score}")
            return
            
        b.unmake_move()
        
        # 2. Verify Reset on Pawn Move
        b.halfmove_clock = 99
        # Move pawn: e2 -> e4
        f = b.algebraic_to_sq("e2")
        t = b.algebraic_to_sq("e4")
        b.make_move((f, t, None, None, 'p', False))
        
        if b.halfmove_clock != 0:
            self._fail(f"Clock did not reset on pawn move. Got {b.halfmove_clock}")
            return
            
        print(" Passed!", flush=True)

    def unit_legality(self, b):
        print("Testing Legality Checking...", end="", flush=True)

        # ABSOLUTE PIN
        # White King on e1, White Rook on e2, Black Rook on e8.
        b.set_fen("4r3/8/8/8/8/8/4R3/4K3 w - - 0 1")

        # Try to move the pinned Rook (e2 -> d2)
        f = b.algebraic_to_sq("e2")
        t = b.algebraic_to_sq("d2")
        illegal_move = (f, t, None, None, 'r', False)
        
        b.make_move(illegal_move)
        
        # After move, we check if the PASSIVE side (White, who just moved) is in check
        if not b.in_check(False):
            self._fail("Failed to detect illegal move (Moving pinned piece)")
            return
            
        b.unmake_move()

        # KING INTO CHECK
        # White King e1. Black Rook d8.
        b.set_fen("3r4/8/8/8/8/8/8/4K3 w - - 0 1")
        
        # Try moving King into check (e1 -> d1)
        f = b.algebraic_to_sq("e1")
        t = b.algebraic_to_sq("d1")
        illegal_king_move = (f, t, None, None, 'k', False)
        
        b.make_move(illegal_king_move)
        
        if not b.in_check(False):
            self._fail("Failed to detect illegal move (King moving into check)")
            return
            
        b.unmake_move()
        
        print(" Passed!", flush=True)

    def unit_attack_resolution(self, b):
        print("Testing Attack Resolution...", end="", flush=True)

        # White Rook on a1. Black Pawn on a4.
        b.set_fen("8/8/8/8/p7/8/8/R7 w - - 0 1")
        
        sq_a2 = b.algebraic_to_sq("a2")
        sq_a3 = b.algebraic_to_sq("a3")
        sq_a4 = b.algebraic_to_sq("a4")
        sq_a5 = b.algebraic_to_sq("a5")
        
        # 1. Rook should attack a2, a3, a4.
        if not b.attacked(sq_a2, True): self._fail("Rook a1 should attack a2"); return
        if not b.attacked(sq_a3, True): self._fail("Rook a1 should attack a3"); return
        if not b.attacked(sq_a4, True): self._fail("Rook a1 should attack capture target a4"); return
        
        # 2. Rook should NOT attack a5 (Blocked by pawn at a4)
        if b.attacked(sq_a5, True): self._fail("Rook a1 should be blocked at a5"); return

        # 3. X-Ray / Battery Check
        b.set_fen("k7/8/8/8/8/8/R7/R7 w - - 0 1")
        # King a8, Rooks a2, a1
        sq_k = b.algebraic_to_sq("a8")
        
        if not b.attacked(sq_k, True): self._fail("Battery: King a8 not attacked"); return
        
        # Check diagonal blocking
        # White Bishop a1. Black Pawn b2. Square c3.
        b.set_fen("8/8/8/8/8/8/1p6/B7 w - - 0 1")
        sq_b2 = b.algebraic_to_sq("b2")
        sq_c3 = b.algebraic_to_sq("c3")
        
        if not b.attacked(sq_b2, True): self._fail("Bishop a1 should attack b2 (capture)"); return
        if b.attacked(sq_c3, True): self._fail("Bishop a1 should NOT attack c3 (blocked)"); return

        print(" Passed!", flush=True)