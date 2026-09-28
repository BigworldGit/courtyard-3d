#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$DIR/video" ]; then
    VIDEO_DIR="$DIR/video"
else
    VIDEO_DIR="$DIR"
fi
TARGET="$VIDEO_DIR/M2U00577.MPG"
echo "Reassembling $TARGET from 50MB parts..."
cat "$VIDEO_DIR"/M2U00577.MPG.part_* > "$TARGET"
echo "Done! Output size: $(ls -lh "$TARGET" | awk '{print $5}')"
echo "Verifying MD5 checksum..."
ACTUAL_MD5=$(md5 -q "$TARGET" 2>/dev/null || md5sum "$TARGET" | awk '{print $1}')
echo "Result: $ACTUAL_MD5"
