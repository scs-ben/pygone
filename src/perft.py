#!/usr/bin/env python3
import sys, time
from pygone import Board  # adjust to match your file name

perft_captures = 0
perft_checks = 0

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
    global perft_captures
    global perft_checks
    
    if depth == 0:
        return 1
    
    total = 0
    for move in board.generate_valid_moves():
        moved_board = board.make_move(move)

        if moved_board.in_check(board.played_move_count % 2 == 0):
            continue

        if board.piece_count != moved_board.piece_count:
            perft_captures += 1

        if moved_board.in_check(board.played_move_count % 2 != 0):
            perft_checks += 1
            
        total += perft(moved_board, depth - 1)
        
    return total


def perft_divide(board, depth):
    global perft_captures
    global perft_checks
    total = 0
        
    for move in board.generate_valid_moves():
        moved_board = board.make_move(move)

        if moved_board.in_check(board.played_move_count % 2 == 0):
            continue

        count = perft(moved_board, depth-1)
        
        print(f"{move}: {count}")
        total += count

    print(f"Total nodes: {total} Captures: {perft_captures} Checks: {perft_checks}")
    return total

def main():
    if len(sys.argv) < 3:
        print("Usage: python perft.py '<FEN>' <depth>")
        sys.exit(1)

    fen = sys.argv[1]
    depth = int(sys.argv[2])

    # --- build board ---
    board = Board()
    board.board_state, side, castling, ep = fen_to_board_state(fen)
    board.en_passant = ep if ep != '-' else None
    board.white_to_move = (side == 'w')
    board.played_move_count = 0 if board.white_to_move else 1

    # if you track castling rights as [KQ, kq]
    board.white_castling = ['K' in castling, 'Q' in castling]
    board.black_castling = ['k' in castling, 'q' in castling]

    t0 = time.time()
    nodes = perft_divide(board, depth)
    elapsed = time.time() - t0

    print(f"\nDepth {depth}: {nodes} nodes in {elapsed:.2f}s ({nodes/elapsed:.0f} NPS)")

main()