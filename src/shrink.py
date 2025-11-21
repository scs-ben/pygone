#!/usr/bin/env pypy3
from pathlib import Path
import python_minifier
import re
import tempfile
import shutil
from collections import defaultdict

def combine_imports(file_path: str):
    path = Path(file_path)
    code = path.read_text()

    # Collect imports
    import_lines = []
    other_lines = []

    for line in code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            import_lines.append(stripped)
        elif stripped.startswith("from "):
            import_lines.append(stripped)
        else:
            other_lines.append(line)

    # Combine plain imports
    plain_imports = []
    from_imports = defaultdict(list)

    for line in import_lines:
        if line.startswith("import "):
            modules = line[len("import "):].split(",")
            modules = [m.strip() for m in modules]
            plain_imports.extend(modules)
        elif line.startswith("from "):
            m = re.match(r"from (\S+) import (.+)", line)
            if m:
                module, names = m.groups()
                names = [n.strip() for n in names.split(",")]
                from_imports[module].extend(names)

    # Remove duplicates and sort
    plain_imports = sorted(set(plain_imports))
    combined_plain = f"import {', '.join(plain_imports)}" if plain_imports else ""

    combined_from = []
    for module, names in from_imports.items():
        unique_names = sorted(set(names))
        combined_from.append(f"from {module} import {', '.join(unique_names)}")

    # Combine all imports at top
    new_code = "\n".join([combined_plain] + combined_from + [""] + other_lines)

    path.write_text(new_code)
    print(f"Imports combined and moved to top of {file_path}")

# Define all replacements here
replacements = {
    # Constants / dictionaries
    "self": "AA",
    "algebraic_to_sq": "AB1",
    "to_sq": "AB",
    "from_sq": "AC",
    "all_pieces": "AD",
    # E is a position
    "set_board": "G1",
    "board": "AG",
    "s_depth": "AH",
    "entry": "AI",
    "reduced_depth": "AJ",
    
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
    
    "gen_legal_moves": "aw1",
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
    "compute_hash": "c31",
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
    "IDX_TO_PIECE": "d9",
    "FILES": "da",
    "RANKS": "db",
    "KING_ATK": "dc",
    "DIRS_ROOK": "dd",
    "DIRS_BISHOP": "de",
    "PIECE_VALUES": "df",
    "PAWN_ATK_BLACK": "dg",
    "KNIGHT_ATK": "dh",
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
    "PAWN_ATK_WHITE": "dt",
    "SIDE_KEY": "du",
    "MATE_SCORE_UPPER": "dv",
    "UNIFIED_PST": "dw",
    "PST_WEIGHTS": "dx",
    "START_FEN": "dy",
    
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
    "piece_idx": "fp",
    "eval_position": "fq",
    "piece_on": "fr",
    "piece_map": "fs",
    "set_fen": "ft",
    "fen": "fu",
    
    "ply": "fx",
    "rank": "fy",
    "piece": "fz",
    
    "TranspositionTable": "g1",
    "TTEntry": "g2",
    "Search": "g3",
    "Board": "g4",
    "doubled": "g5",
    "isolated": "g6",
    
    "best_move": "h2",
    "halfmove_clock": "h3",
    "killer_moves": "h4",
    "tt_move": "h5",
    "unmove": "h6",
    "uci_move": "h7",
    "generate_sliding_moves": "h9",
    "generate_pseudo_legal_moves": "ha",
    "generate_piece_moves": "hb",
    "generate_castling_moves": "hc1",
    "generate_pawn_moves": "hd",
    "move_tuple": "he",
    "clear_tables": "hf",
    "score_killer_move": "hg",
    "size_bytes": "hh",
    "zobrist_key": "hi",
    "print_stats": "hj",
    "print_to_terminal": "hk",
    "print_string": "hl",
    "sq_to_uci": "hm",
    "unmake_move": "hn1",
    "make_move": "hn",
    "eval_material": "ho",
    "attacked": "hp",
    "get_bit": "hq",
    "pop_lsb": "hr",
    "side_index": "hs",
    "gen_pseudo_legal": "ht",
    "all_occupied": "hu",
    "hq_length": "hv",
    "castle": "hw",
    "stack": "hx",
    
    "rook_from": "o1",
    "rook_to": "o2",
    "king_square": "o3",
    "tt_index": "o4",
    "probe": "o5",
    "store": "o6",
    "seconds": "o7",
    "table": "o8",
    
    "pawn": "p1",
    "knight": "p2",
    "bishop": "p3",
    "rook": "p4",
    "queen": "p5",
    "king": "p6",
    
    "bb_name": "q1",
    
    "side_white": "qy1",
    "white": "qy",
    "name": "qz",

    "main": "r0",
    "castle_options": "r1",
    "empty_sqs": "r2",
    "attacked_sqs": "r3",
    "start_sq": "r4",
    "end_sq": "r5",
    

    # Built-ins / keywords
    "True": "1",
    "False": "0",
    
    #These have to match up with the assignment/replacements at the end
    "None": "Za",
    "enumerate": "Zb",
    "random.getrandbits": "Zc",
    "time.time": "Zd",
    "range": "Ze",
    "math.ceil": "Zf",
    "sorted": "Zg",

}

path = "pygone-mini.py"
file = Path(path)
code = file.read_text()

# Apply replacements (longest first to prevent partial overlaps)
for old, new in sorted(replacements.items(), key=lambda kv: -len(kv[0])):
    code = code.replace(old, new)

# Write back
file.write_text(code)

minified = python_minifier.minify(
    code,
    rename_locals=False,      # shrink local variables inside functions/classes
    rename_globals=False,    # leave module-level globals/constants intact
    combine_imports=False,
    hoist_literals=False,
    remove_annotations=True,
    remove_literal_statements=True
)

with open(path, "w") as f:
    f.write(minified)

combine_imports(path)

insert_text = "Za=None;Zb=enumerate;Zc=random.getrandbits;Zd=time.time;Ze=range;Zf=math.ceil;Zg=sorted\n"

with tempfile.NamedTemporaryFile("w", delete=False) as tmp, open(path) as f:
    for i, line in enumerate(f, start=0):
        if i == 0:
            tmp.write("#!/usr/bin/env pypy3\n")
        if i == 2:
            tmp.write(insert_text)
        tmp.write(line)

shutil.move(tmp.name, path)

file = Path(path)
code = file.read_text()

minified = python_minifier.minify(
    code,
    rename_locals=False,      # shrink local variables inside functions/classes
    rename_globals=False,    # leave module-level globals/constants intact
    combine_imports=False,
    hoist_literals=False,
    remove_annotations=True,
    remove_literal_statements=True
)

with open(path, "w") as f:
    f.write(minified)