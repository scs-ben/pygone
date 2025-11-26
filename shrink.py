#!/usr/bin/env python3
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
import re
import tokenize
import io
import python_minifier
from pathlib import Path

# --- 1. AGGRESSIVE REPLACEMENT MAP (Your Dictionary) ---
REPLACEMENTS = {
    "board": "A",
    "make_move": "B",
    "unmake_move": "C",
    "FILES": "D",
    # E
    "RANKS": "F",
    "IDX_TO_PIECE": "G",
    "PROMO_MAP": "H",
    "A_FILE_MASK": "I",
    "CR_MASK": "J",
    "UNIFIED_PST": "K",
    "PAWN_PST": "L",
    "PST_WEIGHTS": "M",
    # N
    "CENTER_SCORE": "O",
    "DIRS_ROOK": "P",
    "DIRS_BISHOP": "Q",
    "KNIGHT_ATK": "R",
    # S
    "KING_ATK": "T",
    "PAWN_ATK_WHITE": "U",
    "PAWN_ATK_BLACK": "V",
    #W
    "PIECE_VALUES": "X",
    "white_to_move": "Y",
    "halfmove_clock": "Z",
    
    "PIECE_KEYS": "a0",
    "CASTLING_KEYS": "a1",
    "EP_KEYS": "a2",
    "SIDE_KEY": "a3",
    "Search": "a4",
    "s_nodes": "a5",
    "time_up": "a6",
    "end_time": "a7",
    "s_depth": "a8",
    "set_time_limit": "a9",
    "seconds": "aa",
    "set_board": "ab",
    "iterative_search": "ac",
    "current_hash": "ad",
    "old_hash": "ae",
    "hash": "af",
    "search": "ag",
    "move_to_uci": "ah",
    "drawn": "ai",
    "stack": "aj",
    "original_alpha": "ak",
    "alpha": "al",
    "beta": "am",
    "ply": "an",
    "is_insufficient_material": "ao",
    "in_check": "ap",
    "q_search": "aq",
    "evaluate": "ar",
    # as
    "gen_pseudo_legal": "at",
    "Board": "au",
    "piece_map": "av",
    "castle": "aw",
    "score_pst": "ax",
    "bm_w": "ay",
    "bm_b": "az",
    "side_white": "A0",
    "pieces_of": "A1",
    "all_occupied": "A2",
    "idx": "A3",
    "side_index": "A4",
    "piece_idx": "A5",
    "by_white": "A6",
    "white": "A7",
    "algebraic_to_sq": "A8",
    "_get_piece_val": "A9",
    "attacked": "Aa",
    "king_square": "Ab",
    "piece_on": "Ac",
    "eval_king": "Ad",
    "pawn_structure_score": "Ae",
    "score_mat": "Af",
    "pawns": "Ag",  
    "pst": "Ah",  
    "mobility": "Ai",  

    # Built-ins / keywords
    "True": "1",
    "False": "0",
}

REPLACEMENTS2 = {
    "import random": "",
    "import sys,time": "import sys,time,random",
}

def remove_blank_lines(text):
    return '\n'.join([line for line in text.splitlines() if line.strip()])

def process_fstring(text, mapping):
    """
    Parses an f-string (e.g. f"Value: {s_depth}") and replaces 
    identifiers inside the curly braces only.
    """
    # Regex to match {expression} inside the string
    pattern = re.compile(r'(?<!\{)\{(.*?)\}(?!\})')
    
    # Regex to match whole words in the mapping
    keys = sorted(mapping.keys(), key=len, reverse=True) 
    map_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, keys)) + r')\b')

    def replace_expression_content(match):
        content = match.group(1)
        # Replace identifiers inside the content
        new_content = map_pattern.sub(lambda m: mapping[m.group(0)], content)
        return f"{{{new_content}}}"

    return pattern.sub(replace_expression_content, text)

def replace_literal_string(token_string, mapping):
    """
    Checks if a string literal (e.g. 'EXACT') matches a key in the map.
    If so, replaces it with the mapped value (e.g. 'E').
    """
    # Basic sanity check for quotes
    if len(token_string) < 2: 
        return None
        
    quote = token_string[0]
    # Ensure it's a simple string wrapped in matching quotes
    if quote in ['"', "'"] and token_string.endswith(quote):
        content = token_string[1:-1]
        if content in mapping:
            return f"{quote}{mapping[content]}{quote}"
            
    return None

def apply_safe_replacements(source_code, mapping):
    """
    Uses tokenize to replace identifiers, variables inside f-strings,
    AND exact string literals (e.g. 'EXACT').
    """
    tokens = list(tokenize.tokenize(io.BytesIO(source_code.encode('utf-8')).readline))
    
    modified_tokens = []
    for t in tokens:
        # 1. Handle Standard Variables (NAME tokens)
        if t.type == tokenize.NAME and t.string in mapping:
            new_t = (t.type, mapping[t.string], t.start, t.end, t.line)
            modified_tokens.append(new_t)
            
        # 2. Handle 'print' if mapped
        elif t.type == tokenize.NAME and t.string == 'print' and 'print' in mapping:
            new_t = (t.type, mapping[t.string], t.start, t.end, t.line)
            modified_tokens.append(new_t)
            
        # 3. Handle STRINGS
        elif t.type == tokenize.STRING:
            # Check for f-string prefix (f', f", F', F")
            prefix = t.string[:2].lower()
            
            if 'f' in prefix and (prefix.startswith('f') or prefix.startswith('fr') or prefix.startswith('rf')):
                # It is an f-string: Replace vars inside {}
                new_val = process_fstring(t.string, mapping)
                new_t = (t.type, new_val, t.start, t.end, t.line)
                modified_tokens.append(new_t)
            else:
                # It is a normal string: Check if it's a literal we want to replace (e.g. 'EXACT')
                new_val = replace_literal_string(t.string, mapping)
                if new_val:
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

    # 2. Apply Safe Renaming (Tokenizer + F-String + String Literal)
    print("Applying safe attribute renaming...")
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
        combine_imports=True,
    )

    # 4. Final Cleanup (Tabs/Blank Lines)
    print("Performing final cleanup...")
    
    minified_code = minified_code.replace('import random', '')
    minified_code = minified_code.replace('import time', 'import time,random')
    minified_code = minified_code.replace('__init__(A,fen=None)', '__init__(A)')

    final_code = minified_code.replace('\t', ' ')
    final_code = remove_blank_lines(final_code)

    # 5. Write Output
    output_path = Path("pygone-final.py")
    # Ensure we only have one shebang
    if final_code.startswith("#!"):
        final_code = "\n".join(final_code.splitlines()[1:])
        
    output_path.write_text("#!/usr/bin/env pypy3\n" + final_code)
    
    print(f"Original: {len(raw_code)} bytes")
    print(f"Final:    {len(final_code) + len('#!/usr/bin/env pypy3')} bytes")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()