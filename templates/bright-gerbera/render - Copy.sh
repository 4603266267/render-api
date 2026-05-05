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
  \( -size 1920x1080 xc:none \
     -fill "#576436" \
     -interline-spacing 34 \
     -gravity Center \
     -kerning 13 \
     -draw "text 0,0 '$(cat "$TEXT_DIR/wish.txt")'" \
  \) -geometry +35-4 -composite \
  -gravity southeast \
  -pointsize 30 -fill white -stroke black -strokewidth 1 -kerning 3 \
  -annotate +40+30 "MyCongrat.com" \
  "$OUTPUT"