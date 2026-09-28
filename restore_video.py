#!/usr/bin/env python3
"""
Restore original video M2U00577.MPG from split binary chunks.
Bit-exact verification using MD5: 4824f3c98d06aa97522ce7b3db100ec9
"""
import os
import sys
import glob
import hashlib

EXPECTED_MD5 = "4824f3c98d06aa97522ce7b3db100ec9"

script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(script_dir, "video")):
    video_dir = os.path.join(script_dir, "video")
else:
    video_dir = script_dir

target_file = os.path.join(video_dir, "M2U00577.MPG")
part_files = sorted(glob.glob(os.path.join(video_dir, "M2U00577.MPG.part_*")))

if not part_files:
    print(f"Error: No chunk files found in {video_dir}")
    sys.exit(1)

print(f"Found {len(part_files)} chunks. Merging into {target_file}...")

md5 = hashlib.md5()
total_written = 0

with open(target_file, "wb") as out_f:
    for p in part_files:
        p_name = os.path.basename(p)
        p_size = os.path.getsize(p)
        print(f"  Merging {p_name} ({p_size / 1024 / 1024:.1f} MB)...")
        with open(p, "rb") as in_f:
            while True:
                chunk = in_f.read(4 * 1024 * 1024)
                if not chunk:
                    break
                out_f.write(chunk)
                md5.update(chunk)
                total_written += len(chunk)

actual_md5 = md5.hexdigest()
print(f"\nMerge completed: {total_written / 1024 / 1024:.1f} MB written.")
print(f"Computed MD5: {actual_md5}")
print(f"Expected MD5: {EXPECTED_MD5}")

if actual_md5.lower() == EXPECTED_MD5.lower():
    print("\n>>> SUCCESS: Original video M2U00577.MPG restored bit-for-bit perfectly! <<<")
else:
    print("\n>>> ERROR: Checksum mismatch! <<<")
    sys.exit(1)
