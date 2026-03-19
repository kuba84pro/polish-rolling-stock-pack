#!/bin/bash

VERSION="0.18.1"
MODNAME="polish-rolling-stock-pack"


set -e

echo "======== START ========"
date

# tmp directories
TMP_DIR="tmp"
OUT_DIR="out"

mkdir -p "$TMP_DIR" "$OUT_DIR"

# files
INPUT="src/pkp.pnml"
INTERMEDIATE="$TMP_DIR/pkp-set.nml"

OUTPUT_GRF="$HOME/.local/share/openttd/newgrf/$MODNAME-$VERSION.grf"

echo "Preprocessing..."
gcc -E -x c "$INPUT" -o "$INTERMEDIATE"

echo "Compiling..."
nmlc -c --grf "$OUTPUT_GRF" "$INTERMEDIATE"

echo "======== DONE ========"
echo "File .grf saved in:"
echo "$OUTPUT_GRF"

rm -r "$TMP_DIR" "$OUT_DIR"