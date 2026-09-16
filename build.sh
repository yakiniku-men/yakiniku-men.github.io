#!/usr/bin/env bash
# 由 iCloud 的成品檔產生 GitHub Pages 用的完整 HTML 文件。
# 用法：./build.sh   （改完內容後執行，再 git commit && git push）
set -e
SRC="/Users/ningchang/Library/Mobile Documents/com~apple~CloudDocs/○山城一鳴/燒肉MEN/燒肉MEN_創作者配合事項表_手機版.html"
[ -f "$SRC" ] || { echo "找不到來源檔：$SRC" >&2; exit 1; }
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/wrap.py" "$SRC" "$DIR/index.html"
