#!/usr/bin/env bash
set -euo pipefail

TEXT_DIR="$1"
OUTPUT="$2"

magick bright-gerbera.webp \
  -font "./FORTE.TTF" \
  -fill "#C22745" -pointsize 60 -kerning 8 \
  -annotate +620+370 @"$TEXT_DIR/recp.txt" \
  -fill "#C22745" -pointsize 60 -kerning 13 \
  -annotate +730+750 @"$TEXT_DIR/from.txt" \
  -fill "#FFFFFF" -pointsize 52 -kerning 8 \
  -annotate +698+920 @"$TEXT_DIR/dat.txt" \
  -gravity center \
  -fill "#576436" \
  -pointsize 60 \
  -kerning 13 \
  -interline-spacing 34 \
  -annotate +0+0 @"$TEXT_DIR/wish.txt" \
  -gravity southeast \
  -pointsize 30 -fill white -stroke black -strokewidth 1 -kerning 3 \
  -annotate +40+30 "MyCongrat.com" \
  "$OUTPUT"