#!/usr/bin/env bash
# 由 iCloud 的成品檔產生 GitHub Pages 用的完整 HTML 文件。
# 用法：./build.sh   （改完內容後執行，再 git commit && git push）
set -e

# 來源檔固定叫這個名字，但上層資料夾被改過好幾次（○山城一鳴 → ◼︎山城一鳴），
# 所以用搜尋的，不要寫死路徑。找到多個就報錯，不要猜。
FILENAME="燒肉MEN_創作者配合事項表_手機版.html"
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

# 可用 SRC 環境變數直接指定，略過搜尋
if [ -z "$SRC" ]; then
  MATCHES=$(find "$ICLOUD" -maxdepth 3 -name "$FILENAME" -not -name "*_2026.*" 2>/dev/null)
  COUNT=$(printf '%s' "$MATCHES" | grep -c . || true)
  if [ "$COUNT" -eq 0 ]; then
    echo "找不到來源檔 $FILENAME（已搜尋 $ICLOUD 下三層）" >&2
    echo "若檔案在別處，用 SRC=/完整/路徑 ./build.sh 指定" >&2
    exit 1
  elif [ "$COUNT" -gt 1 ]; then
    echo "找到多個同名來源檔，請用 SRC=/完整/路徑 ./build.sh 指定要用哪一份：" >&2
    printf '%s\n' "$MATCHES" >&2
    exit 1
  fi
  SRC="$MATCHES"
fi

[ -f "$SRC" ] || { echo "找不到來源檔：$SRC" >&2; exit 1; }
echo "來源：$SRC"

DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/wrap.py" "$SRC" "$DIR/index.html"
