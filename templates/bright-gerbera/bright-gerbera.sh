magick bright-gerbera.webp \
  -font "./FORTE.TTF" \
  -fill "#C22745" -pointsize 60 -kerning 8 -annotate +620+370 "Dear Molly & Jordan" \
  -fill "#C22745" -pointsize 60 -kerning 13 -annotate +730+750 "Janet & Larry" \
  -fill "#FFFFFF" -pointsize 52 -kerning 8 -annotate +698+920 "November 10, 2024" \
  \( -size 1920x1080 xc:none \
     -fill "#576436" \
     -interline-spacing 34 \
     -gravity Center \
     -kerning 13 \
     -draw "text 0,0 ' We raise our glasses \nin celebration of your \nenduring love'" \
  \) -geometry +35-4 -composite \
  -gravity southeast \
  -pointsize 30 -fill white -stroke black -strokewidth 1 -kerning 3 \
  -annotate +40+30 "MyCongrat.com" \
  bright-gerbera-order-number.webp


