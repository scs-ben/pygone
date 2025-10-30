#!/usr/bin/env pypy3
from pathlib import Path

file = Path("pygone-mini.py")
code = file.read_text()

# Define all replacements here
replacements = {
    # Constants / dictionaries
    "PIECEPOINTS": "A",
    "ALLPSQT": "B",
    "set_piece": "C",
    "set_row": "D",
    "set_column": "E",
    "WHITE_PIECES": "F",
    "BLACK_PIECES": "G",

    # Search class attributes
    "v_nodes": "H",
    "v_depth": "I",
    "end_time": "J",
    "critical_time": "K",
    "tt_bucket": "L",
    "eval_exact": "M",
    "eval_upper": "N",
    "eval_lower": "O",
    "eval_mate_upper": "P",

    # Board class attributes
    "board_string": "Q",
    "hash": "R",
    "ZOBRIST": "S",
    "ZOBRIST_CASTLE": "T",
    "ZOBRIST_EP": "U",
    "ZOBRIST_SIDE": "V",
    "played_move_count": "W",
    "white_castling": "X",
    "black_castling": "Y",
    "self": "Z",
    "white_king_position": "Z1",
    "black_king_position": "aa",
    "rolling_score": "ab",
    "piece_count": "ac",
    "en_passant_file_index": "ae",
    "move_counter": "af",

    # Board class methods
    "init_zobrist": "ah",
    "unpack_coordinate": "ai",
    "position_to_coordinate": "aj",
    "coordinate_to_position": "ak",
    "mutate_board": "al",
    "get_moves": "am",
    "number_to_letter": "an",
    "apply_move": "ao",
    "make_move": "ap",
    "nullmove": "aq",
    "board_copy": "ar",
    "get_piece_count": "as1",
    "is_endgame": "at",
    "move_sort": "au",
    "print_board": "av",
    "calculate_score": "aw",
    "passer_pawn": "ax",
    "stacked_pawn": "ay",
    "str_board": "az",
    "generate_valid_captures": "ba",
    "generate_valid_moves": "bb",
    "is_in_check": "bc9",
    "in_check": "bc",
    "attack_position": "bd",
    
    "v_score": "be",
    "v_time": "bf",
    "v_nps": "bg",
    "v_pv": "bh",
    "local_board": "bi",
    "local_score": "bj",
    "best_move": "bk",
    "is_pv_node": "bl",
    "reset": "bm",
    "elapsed_time": "bn",
    "counter": "bo",
    "pv_entry": "bp",
    "pv_board": "bq",
    "repetitions": "br",
    "valid_pieces": "bs",
    "cut_boundary": "bt",
    "best_score": "bu",
    "is_white": "bv",
    "pieces": "bw",
    "played_moves": "by",
    "s_move": "bz",
    "moved_board": "ca",
    "is_quiet": "cb",
    "r_depth": "cc",
    "set_board": "cd",
    "prow": "ce",
    "old_piece": "cf",
    "column": "cg",
    "Board": "ch",
    "board_position": "ci",
    "zobrist": "cj",
    "uci_coordinate": "ck",
    "start_coordinate": "cl",
    "new_piece": "cm",
    "to_number": "cn",
    "from_number": "co",
    "from_piece": "cp",
    "to_piece": "cq",
    "to_offset": "cr",
    "from_offset": "cs",
    "promote": "ct",
    "p_offset": "cu",
    "start_positions": "cv",
    "captures_only": "cw",
    "max_row": "cx",
    "min_row": "cy",
    "valid_bw": "cz",
    "piece_lower": "da",
    "piece_move": "db",
    "to_position": "dc",
    "eval_piece": "dd",
    "dest": "de",
    "king_position": "df",
    "prom": "dg",
    "print_string": "dh",
    "print_to_terminal": "di",
    "game_board": "dj",
    "searcher": "dk",
    "Search": "dl",
    "main": "dm",
    "line": "dn",
    "position_move": "do",
    "moves": "dp",
    "move_time": "dq",
    "p_piece": "dr",
    
    "tt_entry": "ta",
    "tt_value": "tb",
    "tt_flag": "tc",
    "tt_depth": "td",
    "tt_move": "te",
    
    "print_stats": "ps",
    "start_time": "st",
    
    "original_alpha": "yc",
    "alpha": "ya",
    "beta": "yb",
    
    "pos": "za",
    "piece": "zb",
    "square": "zc",
    "en_passant_offset": "zd",
    "en_passant": "ze",
    "offset": "zf",
    "coordinate": "zg",
    
    "iterative_search": "zi",
    "q_search": "zq",
    "l_board_state": "zs",
    "board_state": "zt",
    "board": "zu",
    "search": "zz",

    # Built-ins / keywords
    "True": "1",
    "False": "0",
}

# Apply replacements (longest first to prevent partial overlaps)
for old, new in sorted(replacements.items(), key=lambda kv: -len(kv[0])):
    code = code.replace(old, new)

# Write back
file.write_text(code)

replacements = {
    "KeyzuInterrupt": "KeyboardInterrupt",
    "zaition": "position",
}

# Apply replacements (longest first to prevent partial overlaps)
for old, new in sorted(replacements.items(), key=lambda kv: -len(kv[0])):
    code = code.replace(old, new)

# Write back
file.write_text(code)