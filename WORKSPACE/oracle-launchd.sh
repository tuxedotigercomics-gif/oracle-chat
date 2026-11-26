#!/bin/bash
echo "=== launchd start $(date) ===" >> "/Users/macbookair/Documents/Default Project/oracle-launchd.log"
echo "whoami=$(whoami) PWD=$PWD" >> "/Users/macbookair/Documents/Default Project/oracle-launchd.log"
cd "/Users/macbookair/Documents/Default Project" || exit 1
exec /opt/homebrew/bin/python3 "/Users/macbookair/Documents/Default Project/oracle_bridge.py" >> "/Users/macbookair/Documents/Default Project/oracle-bridge.log" 2>&1
