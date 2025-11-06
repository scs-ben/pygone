#!/usr/bin/env pypy3
from pathlib import Path
import python_minifier

file = Path("pygone-mini.py")
code = file.read_text()

# Define all replacements here
replacements = {
    # Constants / dictionaries
    "self": "AA",
    "to_sq": "AB",
    "from_sq": "AC",
    "all_pieces": "AD",
    # E is a position
    "set_board": "G1",
    "board": "AG",
    "s_depth": "AH",
    "entry": "AI",
    
    "white_to_move": "a1",
    "white_file": "a2",
    "black_file": "a3",
    "by_white": "a4",
    "moves_section": "a5",
    "played_moves": "a6",
    "sorted_moves": "a7",
    "scored_moves": "a8",
    "is_pv_node": "a9",
    "null_score": "aa",
    "cut_boundary": "ab",
    "has_sufficient_material": "ac",
    "nullmove": "ad",
    "minors": "ae",
    "majors": "af",
    "moves_played": "ag",
    "plies_played": "ah",
    "move_to_uci": "ai",
    "do_move": "aj",
    "rotate": "ak",
    "history": "al",
    
    "moves": "aw",
    "Move": "ax",
    "white_": "ay",
    "black_": "az",
    
    "g_score": "b1",
    "t_move": "b2",
    "s_move": "b3",
    "init_hash": "b4",
    "is_en_passant": "b5",

    "alpha_orig": "c1",
    "en_passant_square": "c2",
    "hash": "c3",
    "active": "c4",
    "castling_rights": "c5",
    "promo": "c6",
    "q_search": "c7",
    "flag": "c8",
    "file": "c9",
    "in_check": "ca",
    "time_up": "cb",
    "stand_pat": "cc",
    "old_rights": "cd",
    "flip": "ce",
    "line": "cf",
    "get_ray_mask": "cg",
    "is_square_attacked": "ch",
    "best_score": "ci",
    "mate_score_upper": "cj",
    "local_score": "ck",
    "iterative_search": "cl",
    "q_depth": "cm",
    "score_move": "cn",
    "time_limit": "co",
    "end_time": "cp",
    
    "search": "cu",
    "Zobrist": "cv",
    "alpha": "cw",
    "beta": "cx",
    
    "BLACK_SQUARES": "D1",
    
    "TIME_CUT": "d1",
    "KNIGHT_ATTACKS": "d2",
    "KING_ATTACKS": "d3",
    "WHITE_PAWN_ATTACKS": "d4",
    "BLACK_PAWN_ATTACKS": "d5",
    "RAYS": "d6",
    "DIRECTIONS": "d7",
    "PIECE_KEYS": "d8",
    "WHITE_KING_START": "d9",
    "WHITE_ROOK_KINGSIDE": "da",
    "WHITE_ROOK_QUEENSIDE": "db",
    "BLACK_ROOK_KINGSIDE": "dc",
    "BLACK_ROOK_QUEENSIDE": "dd",
    "MATE_SCORE_UPPER": "de",
    "PIECE_VALUES": "df",
    "BLACK_INDEX_TO_SQUARE": "dg",
    "INDEX_TO_SQUARE": "dh",
    "SQUARES": "di",
    "CASTLING_KEYS": "dj",
    "EP_KEYS": "dk",
    "PIECE_INDEX": "dl",
    "SIDE_TO_MOVE": "dm",
    "EXACT": "dn",
    "LOWERBOUND": "do",
    "UPPERBOUND": "dp",
    "PIECE_MAP": "dq",
    "RANK_8": "dr",
    "RANK_2": "ds",
    "WHITE_KING_START": "dt",
    "WHITE_ROOK_KINGSIDE": "du",
    "WHITE_ROOK_QUEENSIDE": "dv",
    "BLACK_KING_START": "dw",
    "BLACK_ROOK_KINGSIDE": "dx",
    "BLACK_ROOK_QUEENSIDE": "dy",
    "KNIGHT_OFFSETS": "dz",
    "KING_OFFSETS": "da1",
    "BISHOP_OFFSETS": "da2",
    "ROOK_OFFSETS": "da3",
    "QUEEN_OFFSETS": "da4",
    
    "piece_bb": "f1",
    "piece_index": "f2",
    "piece_keys": "f3",
    "piece_values": "f4",
    "enemy_pieces": "f5",
    "capture": "f6",
    "to_rank": "f7",
    "from_rank": "f8",
    "ray": "f9",
    "sq_idx": "fa",
    "w_time": "fb",
    "b_time": "fc",
    "tokens": "fd",
    "side_time": "fe",
    "move_time": "ff",
    "set_time_limit": "fg",
    "set_depth": "fh",
    "history_table": "fi",
    "is_quiet": "fj",
    "s_nodes": "fk",
    "evaluate": "fl",
    "threefold": "fm",
    "reduction": "fn",
    "friendly_pieces": "fo",
    
    "ply": "fx",
    "rank": "fy",
    "piece": "fz",
    
    "TranspositionTable": "g1",
    "TTEntry": "g2",
    "Search": "g3",
    "Board": "g4",
    
    "best_move": "h2",
    "halfmove_clock": "h3",
    "killer_moves": "h4",
    "tt_move": "h5",
    "unmove": "h6",
    "uci_move": "h7",
    "generate_sliding_moves": "h9",
    "generate_pseudo_legal_moves": "ha",
    "generate_piece_moves": "hb",
    "generate_castling_moves": "hc",
    "generate_pawn_moves": "hd",
    "move_tuple": "he",
    "clear_tables": "hf",
    "score_killer_move": "hg",
    "size_bytes": "hh",
    "zobrist_key": "hi",
    
    "rook_from": "o1",
    "rook_to": "o2",
    "king_square": "o3",
    
    "pawn": "p1",
    "knight": "p2",
    "bishop": "p3",
    "rook": "p4",
    "queen": "p5",
    "king": "p6",
    
    "bb_name": "q1",
    
    "name": "qz",

    # Built-ins / keywords
    "True": "1",
    "False": "0",

}

# Apply replacements (longest first to prevent partial overlaps)
for old, new in sorted(replacements.items(), key=lambda kv: -len(kv[0])):
    code = code.replace(old, new)

# Write back
file.write_text(code)

# replacements = {
#     "info H": "info depth",
# }

# # Apply replacements (longest first to prevent partial overlaps)
# for old, new in sorted(replacements.items(), key=lambda kv: -len(kv[0])):
#     code = code.replace(old, new)

# # Write back
# file.write_text(code)

minified = python_minifier.minify(
    code,
    rename_locals=True,      # shrink local variables inside functions/classes
    rename_globals=False,    # leave module-level globals/constants intact
    combine_imports=True,
    hoist_literals=False,
    remove_annotations=True,
    remove_literal_statements=True
)

with open("pygone-mini.py", "w") as f:
    f.write(minified)