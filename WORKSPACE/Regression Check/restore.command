#!/bin/bash
# Roll back the working chat file to the frozen known-good baseline.
# Double-click this file in Finder. A backup of the current working file is
# saved as Oracle-Chat-Offline.broken.html before the restore.

cd "$(dirname "$0")" || exit 1
BASE="baseline/Oracle-Chat-Offline.html"
WORK="../Oracle-Chat-Offline.html"
BAK="../Oracle-Chat-Offline.broken.html"

if [ ! -f "$BASE" ]; then
  echo "ERROR: baseline file not found at $BASE"
  read -r -p "Press Enter to close..."
  exit 1
fi

if [ -f "$WORK" ]; then
  cp "$WORK" "$BAK"
  echo "Saved current working file to: $BAK"
fi

cp "$BASE" "$WORK"
echo "Restored: $WORK"

echo
echo "SHA-256 of restored file:"
shasum -a 256 "$WORK"

echo
echo "Expected: 320603d7585d1192685c1bff83c66257e6119aacc9c3b5db6cbeb5e94d96c191"
echo
read -r -p "Press Enter to close..."
