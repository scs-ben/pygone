import python_minifier
from pathlib import Path
import re

# --- configuration ---
main_file = Path("pygone.py")
combined_file = Path("pygone-combined.py")

# Files to inline, in dependency order (helpers first)
imports_to_inline = [
    ("search", Path("search.py")),
    ("board", Path("board.py")),
]

# --- read main file ---
main_code = main_file.read_text()

# --- replace each import with the corresponding file contents ---
for module_name, module_path in imports_to_inline:
    if not module_path.exists():
        print(f"⚠️  Skipping {module_name} — {module_path} not found")
        continue

    module_code = module_path.read_text().strip()
    wrapped = (
        f"# === Start of {module_name}.py ===\n"
        f"{module_code}\n"
        f"# === End of {module_name}.py ===\n"
    )

    # Match either "from x import ..." or "import x"
    pattern = rf"(^|\n)\s*(from\s+{module_name}\s+import\s+\w+|import\s+{module_name})([^\S\r\n]*\n)"
    main_code = re.sub(pattern, f"\n{wrapped}\n", main_code)

# --- write output ---
combined_file.write_text(main_code)

with open("pygone-combined.py") as f:
    code = f.read()

minified = python_minifier.minify(
    code,
    rename_locals=False,      # shrink local variables inside functions/classes
    rename_globals=False,    # leave module-level globals/constants intact
    combine_imports=True,
    hoist_literals=False
)

with open("pygone-mini.py", "w") as f:
    f.write(minified)