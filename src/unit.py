#!/usr/bin/env pypy3

class Unit:
    def unit_hash(self, b):
        orig_hash = b.hash
        mv = list(b.gen_pseudo_legal())[0]   # some legal move
        b.make_move(mv)
        b.unmake_move()

        print("Check hash")
        assert b.hash == orig_hash, "Zobrist mismatch after make/unmake"

        # 2) Compute from scratch vs incremental
        orig_hash = b.compute_hash()
        # do a sequence of moves
        moves = list(b.gen_pseudo_legal())[:4]
        for m in moves:
            b.make_move(m)
            b.unmake_move()
        # now compute from scratch and compare
        h_inc = b.hash
        h_scratch = b.compute_hash()
        
        assert h_inc == h_scratch, "Incremental != recompute"

    def parse_move(self, mv, b):
        from_sq = b.algebraic_to_sq(mv[:2])
        to_sq = b.algebraic_to_sq(mv[2:4])

        return (from_sq, to_sq, None, None, None, False)


    def unit_perft(self, perft):
        print("Perft")
        results = perft.run(1, True)
        assert results == (1, 20, 0, 0)
        results = perft.run(2, True)
        assert results == (2, 400, 0, 0)
        results = perft.run(3, True)
        assert results == (3, 8902, 34, 12)
        results = perft.run(4, True)
        assert results == (4, 197281, 1576, 469)

    def unit_perft2(self, perft):
        results = perft.run(1, True)
        assert results == (1, 48, 8, 0)
        results = perft.run(2, True)
        assert results == (2, 2039, 351, 3)
        results = perft.run(3, True)
        assert results == (3, 97862, 17102, 993)

    def unit_moves(self, b):
        print("Check moves")
        # 3) Board State Integrity Check
        b.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        orig_fen = b.get_fen() # Assuming you have a get_fen() method

        # Simple non-capture move
        mv = self.parse_move("e2e4", b) 
        b.make_move(mv)
        b.unmake_move()

        assert b.get_fen() == orig_fen, "Board FEN mismatch after quiet make/unmake"

        # Test a capture move
        b.set_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        orig_fen = b.get_fen()
        mv = self.parse_move("g8f6", b) # Test a non-capture
        b.make_move(mv)
        b.unmake_move()
        assert b.get_fen() == orig_fen, "Board FEN mismatch after capture make/unmake"

    def unit_scoring(self, b):
        print('Scoring')
        # 4) Basic Evaluation Consistency
        b.set_fen("8/8/8/8/8/8/8/R7 w - - 0 1") # Rook vs no pieces
        score_r = b.evaluate()

        b.set_fen("8/8/8/8/8/8/8/N7 w - - 0 1") # Knight vs no pieces
        score_n = b.evaluate()

        # A Rook is worth more than a Knight
        assert score_r > score_n, "Material scoring error: Rook should be worth more than Knight"

        # Check symmetry (White score should be -Black score)
        b.set_fen("r7/8/8/8/8/8/8/8 w - - 0 1") # Black Rook vs no pieces
        score_br = b.evaluate()
        assert score_r + score_br == 0, "Evaluation is not symmetrical"

    def unit_castling(self, b):
        print("Testing Castling & EP")
        # ---------------------------------------
        # 5) Castling Integrity (Tests CR_MASK & Rook Move)
        # ---------------------------------------
        # White has full rights. Rooks on a1/h1, King e1.
        b.set_fen("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1") 
        orig_hash = b.hash
        
        # Move: White Castles Queenside (e1 -> c1)
        # Indices: e1=4, c1=2
        mv = (4, 2, None, None, None, None)
        b.make_move(mv)
        
        # Checks:
        assert b.piece_map[2] == 5, "King not on c1"
        assert b.piece_map[3] == 3, "Rook not on d1 (auto-move failed)"
        assert b.piece_map[0] == -1, "Rook still on a1"
        assert (b.castle & 3) == 0, "White castling rights not cleared"
        
        b.unmake_move()
        
        # Restore checks:
        assert b.piece_map[4] == 5, "King not back on e1"
        assert b.piece_map[0] == 3, "Rook not back on a1"
        assert b.piece_map[2] == -1, "c1 not empty"
        assert b.hash == orig_hash, "Hash mismatch after Castle Unmake"

    def unit_ep(self, b):
        # ---------------------------------------
        # 6) En Passant Integrity (Tests _x helper & Capture)
        # ---------------------------------------
        # White Pawn e5, Black Pawn d5. EP Target is d6 (index 21)
        # White to move.
        b.set_fen("8/8/8/3pP3/8/8/8/k6K w - d6 0 1")
        orig_hash = b.hash
        
        # Move: e5 -> d6 (En Passant Capture)
        # Indices: e5=36, d6=43
        mv = (36, 43, None, None, None, None)
        b.make_move(mv)
        
        # Checks:
        assert b.piece_map[43] == 0, "White pawn not on d6"
        assert b.piece_map[35] == -1, "Black pawn on d5 (35) not removed"
        
        b.unmake_move()
        
        # Restore checks:
        assert b.piece_map[36] == 0, "White pawn not back on e5"
        assert b.piece_map[35] == 6, "Black pawn not back on d5"
        assert b.ep == 43, "EP Square not restored"
        assert b.hash == orig_hash, "Hash mismatch after EP Unmake"
        
    def unit_promo(self, b):
        print("Testing Promotion & Reversal")
        # ---------------------------------------
        # 7) Promotion Integrity
        # ---------------------------------------
        # White Pawn on a7, Black King far away.
        b.set_fen("8/P7/8/8/8/8/8/k6K w - - 0 1")
        orig_hash = b.hash

        # Find the move: a7 -> a8 (Queen promotion)
        # Algebraic: a7=48, a8=56
        # Gen pseudo legal moves to find the specific promotion tuple
        moves = list(b.gen_pseudo_legal())
        promo_move = None
        for m in moves:
            # m format: (from, to, promo, capture, piece, is_castle)
            # We look for promo == 'q' (Queen)
            if m[0] == 48 and m[1] == 56 and m[2] == 'q':
                promo_move = m
                break
        
        assert promo_move is not None, "Could not generate a7a8q move"
        
        # --- EXECUTE MAKE ---
        b.make_move(promo_move)

        # Checks after Make:
        # 1. Target square (a8/56) should have White Queen (index 4)
        # If the bug exists, this will likely fail or crash before here
        assert b.piece_map[56] == 4, f"Expected White Queen (4) at a8, got {b.piece_map[56]}"
        
        # 2. Source square (a7/48) should be empty (-1)
        assert b.piece_map[48] == -1, "Source square a7 was not cleared"
        
        # 3. Bitboard check: The White Queen bitboard (P[4]) should have bit 56 set
        assert (b.P[4] & (1 << 56)), "White Queen bitboard not updated"
        
        # 4. Bitboard check: The White Pawn bitboard (P[0]) should NOT have bit 48 set
        assert not (b.P[0] & (1 << 48)), "White Pawn bitboard not cleared"

        # --- EXECUTE UNMAKE ---
        b.unmake_move()

        # Checks after Unmake:
        # 1. Target square (a8/56) should be empty
        assert b.piece_map[56] == -1, "Promotion square a8 not cleared after unmake"
        
        # 2. Source square (a7/48) should be a White Pawn (index 0) again
        assert b.piece_map[48] == 0, f"Expected White Pawn (0) at a7, got {b.piece_map[48]}"
        
        # 3. Hash check
        assert b.hash == orig_hash, "Hash mismatch after Promotion Unmake"

        print("Promotion unit test passed.")

    def unit_search(self, b, s):
        # Check Search
        orig_fen = b.get_fen()

        orig_hash = b.hash

        s.set_time_limit(1e8)
        s.set_depth(6)
        s.iterative_search()

        assert b.hash == orig_hash, "Hash mismatch after search"
        print(b.get_fen())
        assert b.get_fen() == orig_fen, "FEN mismatch (Board corruption) after search"

        print ("Unit complete")