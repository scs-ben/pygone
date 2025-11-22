#!/usr/bin/env python3
import re
import tokenize
import io
import python_minifier
from pathlib import Path

# --- 1. AGGRESSIVE REPLACEMENT MAP (Your Dictionary) ---
# I removed 'self' and local vars (idx, frm) because pyminifier
# renames them to 1-char ('a', 'b') which is smaller than 2-chars ('AA', 'U').
# I kept ALL attributes, methods, and global constants.
REPLACEMENTS = {
    # Constants / dictionaries
    "idx": "U",
    "frm": "V",
    "self": "AA",
    "algebraic_to_sq": "AB",
    "from_sq": "AC",
    "all_pieces": "AD",
    # E is a position
    "set_board": "G1",
    "board": "AG",
    "s_depth": "AH",
    "entry": "AI",
    "reduced_depth": "AJ",
    "to_sq": "AK",
    
    "white_to_move": "A1",
    "white_file": "A2",
    "black_file": "A3",
    "by_white": "A4",
    "moves_section": "A5",
    "played_moves": "A6",
    "sorted_moves": "A7",
    "scored_moves": "A8",
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
    
    "gen_legal_moves": "aW",
    "moves": "aw",
    "Move": "ax",
    "white_": "ay",
    "black_": "az",
    
    "g_score": "B1",
    "t_move": "B2",
    "s_move": "B3",
    "init_hash": "B4",
    "is_en_passant": "B5",

    "alpha_orig": "C1",
    "en_passant_square": "C2",
    "compute_hash": "C31",
    "hash": "C3",
    "active": "C4",
    "castling_rights": "C5",
    "promo": "C6",
    "q_search": "C7",
    "flag": "C8",
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
    
    "TIME_CUT": "dZ",
    "KNIGHT_ATTACKS": "D2",
    "KING_ATTACKS": "D3",
    "WHITE_PAWN_ATTACKS": "D4",
    "BLACK_PAWN_ATTACKS": "D5",
    "RAYS": "D6",
    "DIRECTIONS": "D7",
    "PIECE_KEYS": "D8",
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
    "A_FILE_MASK": "dz",
    "CR_MASK": "dA",
    
    "piece_bb": "F1",
    "piece_index": "F2",
    "piece_keys": "F3",
    "piece_values": "F4",
    "enemy_pieces": "F5",
    "capture": "F6",
    "to_rank": "F7",
    "from_rank": "F8",
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
    "pieces_of": "fA",
    "moved_piece": "fB",
    "piece": "fz",
    
    "TranspositionTable": "G1",
    "TTEntry": "G2",
    "Search": "G3",
    "Board": "G4",
    "doubled": "G5",
    "isolated": "G6",
    "enemy": "G7",
    
    "best_move": "H2",
    "halfmove_clock": "H3",
    "killer_moves": "H4",
    "tt_move": "H5",
    "unmove": "H6",
    "uci_move": "H7",
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
    "knights": "pA",
    "knight": "p2",
    "bishop": "p3",
    "rook": "p4",
    "queens": "pB",
    "queen": "p5",
    "king_safety": "p6",
    "king": "p7",
    "pawn_structure_penalty": "p8",
    "get_square_indices": "p9",
    
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
}

def remove_blank_lines(text):
    return '\n'.join([line for line in text.splitlines() if line.strip()])

def process_fstring(text, mapping):
    """
    Parses an f-string (e.g. f"Value: {s_depth}") and replaces 
    identifiers inside the curly braces only.
    """
    # Regex to match {expression} inside the string
    # Looks for { followed by anything that isn't a } followed by }
    # (?<!\{) and (?!\}) handle double brace escaping {{ }}
    pattern = re.compile(r'(?<!\{)\{(.*?)\}(?!\})')
    
    # Regex to match whole words in the mapping
    # We compile this once for efficiency
    keys = sorted(mapping.keys(), key=len, reverse=True) 
    map_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, keys)) + r')\b')

    def replace_expression_content(match):
        content = match.group(1)
        # Replace identifiers inside the content
        new_content = map_pattern.sub(lambda m: mapping[m.group(0)], content)
        return f"{{{new_content}}}"

    return pattern.sub(replace_expression_content, text)

def apply_safe_replacements(source_code, mapping):
    """
    Uses tokenize to replace identifiers AND variables inside f-strings.
    """
    tokens = list(tokenize.tokenize(io.BytesIO(source_code.encode('utf-8')).readline))
    
    modified_tokens = []
    for t in tokens:
        # 1. Handle Standard Variables
        if t.type == tokenize.NAME and t.string in mapping:
            new_t = (t.type, mapping[t.string], t.start, t.end, t.line)
            modified_tokens.append(new_t)
            
        # 2. Handle 'print' if mapped (optional)
        elif t.type == tokenize.NAME and t.string == 'print' and 'print' in mapping:
            new_t = (t.type, mapping[t.string], t.start, t.end, t.line)
            modified_tokens.append(new_t)
            
        # 3. Handle F-STRINGS (The fix!)
        elif t.type == tokenize.STRING:
            # Check for f-string prefix (f', f", F', F")
            prefix = t.string[:2].lower()
            if 'f' in prefix and (prefix.startswith('f') or prefix.startswith('fr') or prefix.startswith('rf')):
                new_val = process_fstring(t.string, mapping)
                new_t = (t.type, new_val, t.start, t.end, t.line)
                modified_tokens.append(new_t)
            else:
                modified_tokens.append(t)
                
        else:
            modified_tokens.append(t)

    return tokenize.untokenize(modified_tokens)

def main():
    # 1. Read input
    input_path = Path("pygone-combined.py") 
    if not input_path.exists():
        print("Error: Run pyshrink.py first to generate pygone-combined.py")
        return

    raw_code = input_path.read_text()

    # 2. Apply Safe Renaming (Tokenizer + F-String Parser)
    print("Applying safe attribute renaming (including f-strings)...")
    renamed_code = apply_safe_replacements(raw_code, REPLACEMENTS)

    # 3. Minify
    print("Running pyminifier...")
    minified_code = python_minifier.minify(
        renamed_code,
        rename_locals=True,
        rename_globals=False,
        hoist_literals=False,
        remove_annotations=True,
        remove_literal_statements=True,
    )

    # 4. Final Cleanup (Tabs/Blank Lines)
    print("Performing final cleanup...")
    final_code = minified_code.replace('\t', ' ')
    final_code = remove_blank_lines(final_code)

    # 5. Write Output
    output_path = Path("pygone-final.py")
    # Ensure we only have one shebang
    if final_code.startswith("#!"):
        final_code = "\n".join(final_code.splitlines()[1:])
        
    output_path.write_text("#!/usr/bin/env python3\n" + final_code)
    
    print(f"Original: {len(raw_code)} bytes")
    print(f"Final:    {len(final_code) + len('#!/usr/bin/env python3')} bytes")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()