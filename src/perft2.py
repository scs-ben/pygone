#!/usr/bin/env python3
import sys, time
from board2 import Board  # adjust imports to your setup

perft_captures = 0
perft_checks = 0

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def perft(board, depth):
    """Bitboard-based perft with captures/checks counters."""
    global perft_captures, perft_checks

    if depth == 0:
        return 1

    total = 0
    
    for move in board.generate_pseudo_legal_moves():
        board.move_tuple(move)  # apply tuple-based move

        if board.in_check(False):
            board.unmove()
            continue

        # Track captures
        if move.capture:  # captured piece is not None
            perft_captures += 1

        # Track checks
        if board.in_check():  # check after move
            perft_checks += 1

        total += perft(board, depth - 1)

        board.unmove()  # undo move

    return total


def perft_divide(board, depth):
    """Perft divide for debugging: prints per-move counts."""
    global perft_captures, perft_checks
    total = 0

    for move in board.generate_pseudo_legal_moves():
        board.move_tuple(move)

        if board.in_check(False):
            board.unmove()
            continue
        
        # Track captures
        if move.capture:  # captured piece is not None
            perft_captures += 1

        # Track checks
        if board.in_check():  # check after move
            perft_checks += 1
            
        count = perft(board, depth - 1)
        print(f"{board.move_to_uci(move)}: {count}")
        total += count
        board.unmove()

    print(f"Total nodes: {total} Captures: {perft_captures} Checks: {perft_checks}")
    return total

def set_fen(board, fen=None):
    """Set the board position from a FEN string. Defaults to starting position."""
    fen = fen or START_FEN
    parts = fen.split()
    placement = parts[0]
    side = parts[1]
    castling = parts[2]
    ep = parts[3]

    # Reset all bitboards
    board.white_pawns   = 0
    board.white_knights = 0
    board.white_bishops = 0
    board.white_rooks   = 0
    board.white_queens  = 0
    board.white_kings   = 0
    board.black_pawns   = 0
    board.black_knights = 0
    board.black_bishops = 0
    board.black_rooks   = 0
    board.black_queens  = 0
    board.black_kings   = 0

    # Map piece chars to bitboards
    piece_map = {
        'P': 'white_pawns',   'N': 'white_knights', 'B': 'white_bishops',
        'R': 'white_rooks',   'Q': 'white_queens',  'K': 'white_kings',
        'p': 'black_pawns',   'n': 'black_knights', 'b': 'black_bishops',
        'r': 'black_rooks',   'q': 'black_queens',  'k': 'black_kings'
    }

    rank_idx = 7
    for row in placement.split('/'):
        file_idx = 0
        for ch in row:
            if ch.isdigit():
                file_idx += int(ch)
            else:
                sq = rank_idx * 8 + file_idx
                setattr(board, piece_map[ch], getattr(board, piece_map[ch]) | (1 << sq))
                file_idx += 1
        rank_idx -= 1

    # Side to move
    board.white_to_move = (side == 'w')

    # Castling rights
    board.castling_rights = [
        'K' in castling,  # White kingside
        'Q' in castling,  # White queenside
        'k' in castling,  # Black kingside
        'q' in castling   # Black queenside
    ]

    # En passant square
    board.en_passant_square = None if ep == '-' else board.SQUARES[ep]

    # Reset move counters
    board.plies_played = 0
    board.moves_played = 0
    board.halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
    
    if not board.white_to_move:
        board.rotate()

def main():
    depth = int(sys.argv[1])
    
    fen = None
    
    if len(sys.argv) > 1:
        fen = " ".join(sys.argv[2:]).strip() or None

    board = Board()
    set_fen(board, fen)

    t0 = time.time()
    nodes = perft_divide(board, depth)
    elapsed = time.time() - t0

    print(f"\nDepth {depth}: {nodes} nodes in {elapsed:.2f}s ({nodes/elapsed:.0f} NPS)")


if __name__ == "__main__":
    main()
