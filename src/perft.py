#!/usr/bin/env python3
import sys, time
from board import Board  # adjust to match your file name

perft_captures = 0
perft_checks = 0
perft_en_passant = 0
perft_checkmates = 0

def fen_to_board_state(fen):
    """
    Convert FEN into your engine's 120-square board representation.
    Returns the board_state string and metadata (side, castling, ep).
    """
    parts = fen.split()
    placement, side, castling, ep = parts[0], parts[1], parts[2], parts[3]

    # build 120-square board with sentinels (-1 border)
    board = [' '] * 120
    rows = placement.split('/')

    # The top of the board is rank 8 → index 21
    for rank_idx, row in enumerate(rows):
        file_idx = 0
        rank_start = 21 + rank_idx * 10
        for ch in row:
            if ch.isdigit():
                file_idx += int(ch)
            else:
                board[rank_start + file_idx] = ch
                file_idx += 1

    # Fill sentinels (outer border with '.')
    for i in range(120):
        if i < 20 or i >= 100 or i % 10 in (0, 9):
            board[i] = '.'
        elif board[i] == ' ':
            board[i] = '-'

    board_state = ''.join(board)
    return board_state, side, castling, ep


def perft(board, depth):
    global perft_captures, perft_checks, perft_en_passant, perft_checkmates
    
    if depth == 0:
        return 1
    
    total = 0
    # Determine if the current side (board) is white
    is_white_to_move = board.played_move_count % 2 == 0
    
    for move in board.generate_valid_moves():
        # board.make_move(move) creates a NEW board object with the move applied
        moved_board = board.make_move(move)
        
        # --- CRITICAL VALIDATION CHECK (King Safety) ---
        # After make_move, the 'moved_board' side-to-move has flipped.
        # We check if the king of the side that just moved (the 'previous' side) is in check.
        # The 'previous' side is defined by is_white_to_move.
        if moved_board.in_check(is_white_to_move):
            continue
        # ------------------------------------------------
            
        # --- Tracking Metrics (Happens BEFORE recursion) ---
        
        # A. Captures and En Passant
        if board.get_piece_count() > moved_board.get_piece_count():
            # Check for En Passant using the move object (assuming a method/property)
            # This is highly dependent on your 'move' object structure!
            if len(moved_board.en_passant) > 0:  # Adjust this check to fit your move representation
                perft_en_passant += 1
                
            perft_captures += 1 # Count EP as a capture
        
        # Check: Is the NEXT side-to-move in check?
        is_next_side_in_check = moved_board.in_check(not is_white_to_move)

        # Checkmate: Is the NEXT side-to-move in check AND has no legal moves?
        # Checkmate/Stalemate can only happen when depth-1 is reached (i.e., when we check terminal nodes)
        if is_next_side_in_check:
            # We must check for checkmate only if the game is over
            # Check if the next side to move has any legal moves
            if len([m for m in moved_board.generate_valid_moves() if not moved_board.make_move(m).in_check(not is_white_to_move)]) == 0:
                 perft_checkmates += 1
                 total += 1 # A checkmate/stalemate is a node
                 continue # Stop recursion for terminal node
            else:
                 perft_checks += 1
            
        total += perft(moved_board, depth - 1)
        
    return total

def perft_divide(board, depth):
    global perft_captures, perft_checks, perft_en_passant, perft_checkmates
    total = 0
    
    # Reset globals for the initial divide call
    perft_captures = 0
    perft_checks = 0
    
    # Determine if the current side (board) is white
    is_white_to_move = board.played_move_count % 2 == 0
        
    for move in board.generate_valid_moves():
        moved_board = board.make_move(move)

        # --- CRITICAL VALIDATION CHECK (King Safety) ---
        if moved_board.in_check(is_white_to_move):
            continue
        # ------------------------------------------------
        
        if depth == 1:
            # A. Captures and En Passant
            if board.get_piece_count() > moved_board.get_piece_count():
                # Check for En Passant using the move object (assuming a method/property)
                # This is highly dependent on your 'move' object structure!
                if len(moved_board.en_passant) > 0:  # Adjust this check to fit your move representation
                    perft_en_passant += 1
                    
                perft_captures += 1 # Count EP as a capture
            
            # Check: Is the NEXT side-to-move in check?
            is_next_side_in_check = moved_board.in_check(not is_white_to_move)

            # Checkmate: Is the NEXT side-to-move in check AND has no legal moves?
            # Checkmate/Stalemate can only happen when depth-1 is reached (i.e., when we check terminal nodes)
            if is_next_side_in_check:
                # We must check for checkmate only if the game is over
                # Check if the next side to move has any legal moves
                if len([m for m in moved_board.generate_valid_moves() if not moved_board.make_move(m).in_check(not is_white_to_move)]) == 0:
                    perft_checkmates += 1
                    total += 1 # A checkmate/stalemate is a node
                    continue # Stop recursion for terminal node
                else:
                    perft_checks += 1
        
        # We call perft(..., depth-1) to get the node count for this move's branch
        count = perft(moved_board, depth-1)
        
        print(f"{move}: {count}")
        total += count

    print(f"\nTotal nodes: {total} Captures: {perft_captures} Checks: {perft_checks} EP: {perft_en_passant} #: {perft_checkmates}")
    return total

def main():
    if len(sys.argv) < 3:
        print("Usage: python perft.py '<FEN>' <depth>")
        sys.exit(1)

    fen = sys.argv[1]
    depth = int(sys.argv[2])

    # --- build board ---
    board = Board() # Creates the board, sets up Zobrist, initializes hash for the starting position
    
    # Unpack FEN data
    board_string_120, side, castling, ep = fen_to_board_state(fen)
    
    # The board.board_state is a LIST of integers, but fen_to_board_state returns a STRING.
    # Convert the FEN string back to the numerical list for board.board_state
    # This assumes CHAR_TO_NUM is available (it is in your original file).
    from board import CHAR_TO_NUM 
    board.board_state = [CHAR_TO_NUM[char] for char in board_string_120]
    
    # Now update board state/metadata and the hash (Crucial!)
    
    # 1. Update side-to-move
    # Assuming white starts move_count at 0 and black at 1.
    board.played_move_count = 0 if side == 'w' else 1
    
    # 2. Update En Passant
    board.en_passant = ep if ep != '-' else ''
    
    # Set en_passant_file_index for Zobrist hashing (a=0, h=7)
    if board.en_passant:
        board.en_passant_file_index = ord(board.en_passant[0]) - ord('a')
    else:
        board.en_passant_file_index = 0 # Default to 0 if no EP
        
    # 3. Update Castling Rights (and Zobrist Hash for them)
    # The initial hash from Board() is for the starting position (all rights present).
    # We must explicitly set the rights and XOR the hash keys for removed rights.
    
    # Clear all initial castling hashes if they were set in Board.__init__
    for i in range(4): board.hash ^= board.ZOBRIST_CASTLE[i] 

    board.white_castling = ['K' in castling, 'Q' in castling]
    board.black_castling = ['k' in castling, 'q' in castling]
    
    # XOR back ONLY the rights that are still present
    if board.white_castling[0]: board.hash ^= board.ZOBRIST_CASTLE[0] # White King Side
    if board.white_castling[1]: board.hash ^= board.ZOBRIST_CASTLE[1] # White Queen Side
    if board.black_castling[1]: board.hash ^= board.ZOBRIST_CASTLE[2] # Black Queen Side (Index 2 for a8 rook)
    if board.black_castling[0]: board.hash ^= board.ZOBRIST_CASTLE[3] # Black King Side (Index 3 for h8 rook)
    
    # 4. Final Hash Recalculation (for pieces and side-to-move)
    # Since we manually loaded the piece positions, we must recalculate the piece hash.
    board.hash = 0
    for pos, piece in enumerate(board.board_state):
        if piece > 0 and piece != 99:
            board.hash ^= board.ZOBRIST[piece, pos]
            
    # XOR side-to-move and EP hash (the side hash is flipped at the start of a game)
    if board.played_move_count % 2 != 0:
        board.hash ^= board.ZOBRIST_SIDE
        
    if board.en_passant:
        board.hash ^= board.ZOBRIST_EP[board.en_passant_file_index]
    
    # --- start perft ---
    t0 = time.time()
    nodes = perft_divide(board, depth)
    elapsed = time.time() - t0

    print(f"\nDepth {depth}: {nodes} nodes in {elapsed:.2f}s ({nodes/elapsed:.0f} NPS)")

if __name__ == '__main__':
    main()