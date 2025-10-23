import python_minifier

with open("pygone.py") as f:
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