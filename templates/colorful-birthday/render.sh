#!/usr/bin/env bash
set -euo pipefail

TEXT_DIR="$1"
OUTPUT="$2"

magick colorful-birthday.webp  \
  -font "./Lavinia.otf" \
  -fill "#000000" \
  -gravity center \
  -pointsize 64 \
  -annotate +0-180 @"$TEXT_DIR/recp.txt" \
  -pointsize 58 \
  -annotate +0+0 @"$TEXT_DIR/wish.txt" \
  -pointsize 52 \
  -annotate +0+250 @"$TEXT_DIR/from.txt" \
  -pointsize 44 \
  -annotate +0+360 @"$TEXT_DIR/dat.txt" \
  "$OUTPUT"