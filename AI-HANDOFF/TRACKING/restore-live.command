#!/bin/bash
# Roll back the LIVE Oracle Chat UI to the frozen known-good live baseline.
# Double-click this file in Finder. A backup of the current file is saved as
# Oracle-Chat-Live.broken.html before the restore.

cd "$(dirname "$0")" || exit 1
BASE="baseline/Oracle-Chat-Live.html"
WORK="../Oracle-Chat-Live.html"
BAK="../Oracle-Chat-Live.broken.html"

if [ ! -f "$BASE" ]; then
  echo "ERROR: baseline file not found at $BASE"
  read -r -p "Press Enter to close..."
  exit 1
fi

if [ -f "$WORK" ]; then
  cp "$WORK" "$BAK"
  echo "Saved current live UI to: $BAK"
fi

cp "$BASE" "$WORK"
echo "Restored: $WORK"
echo
echo "SHA-256 of restored file:"
shasum -a 256 "$WORK"
echo
echo "Expected: 7e83fe68bcef9e7b2b409639d177365bb8d5f864845a1957f75ce370325bb78b"
echo
read -r -p "Press Enter to close..."
