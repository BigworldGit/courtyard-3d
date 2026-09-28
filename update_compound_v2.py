import os

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'r', encoding='utf-8') as f:
    orig_code = f.read()

# Let's inspect where key replacements should happen
print("Read orig_code, length:", len(orig_code))
