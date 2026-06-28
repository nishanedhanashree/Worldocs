#!/bin/bash
# Downloads Noto fonts for multi-language PDF rendering.
# Run once from the Worldocs project root: bash download_fonts.sh

BASE="https://cdn.jsdelivr.net/gh/googlefonts/noto-fonts@main/hinted/ttf"

download() {
  local file="$1"
  local url="$2"
  if [ -f "$file" ]; then
    echo "SKIP  $file"
    return
  fi
  echo "DOWN  $file ..."
  curl -sL "$url" -o "$file"
  if [ $? -eq 0 ] && [ -s "$file" ]; then
    echo "OK    $file"
  else
    echo "FAIL  $file"
    rm -f "$file"
  fi
}

download "NotoSansBengali-Regular.ttf"   "$BASE/NotoSansBengali/NotoSansBengali-Regular.ttf"
download "NotoSansGujarati-Regular.ttf"  "$BASE/NotoSansGujarati/NotoSansGujarati-Regular.ttf"
download "NotoSansGurmukhi-Regular.ttf"  "$BASE/NotoSansGurmukhi/NotoSansGurmukhi-Regular.ttf"
download "NotoSansTamil-Regular.ttf"     "$BASE/NotoSansTamil/NotoSansTamil-Regular.ttf"
download "NotoSansTelugu-Regular.ttf"    "$BASE/NotoSansTelugu/NotoSansTelugu-Regular.ttf"
download "NotoSansKannada-Regular.ttf"   "$BASE/NotoSansKannada/NotoSansKannada-Regular.ttf"
download "NotoSansMalayalam-Regular.ttf" "$BASE/NotoSansMalayalam/NotoSansMalayalam-Regular.ttf"
download "NotoSansArabic-Regular.ttf"    "$BASE/NotoSansArabic/NotoSansArabic-Regular.ttf"
download "NotoSans-Regular.ttf"          "$BASE/NotoSans/NotoSans-Regular.ttf"

echo ""
echo "Done. Restart uvicorn to pick up new fonts."
