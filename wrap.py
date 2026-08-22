#!/usr/bin/env python3
"""把 Artifact 用的 HTML 片段包成獨立網頁（補 doctype / html / head / body 與 noindex）。"""
import io, sys, re

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8").read()

# 去掉可能已存在的外層標籤，永遠從片段狀態重建
s = re.sub(r"(?is)^\s*<!doctype[^>]*>\s*", "", s)
s = re.sub(r"(?is)</?(html|head|body)[^>]*>", "", s)

# 切出 head（meta / title / style）與 body
m = re.search(r"(?is)</style>", s)
head, body = (s[: m.end()], s[m.end():]) if m else ("", s)

if "noindex" not in head:
    head = head.replace(
        '<meta name="theme-color" content="#0B0A09">',
        '<meta name="theme-color" content="#0B0A09">\n<meta name="robots" content="noindex, nofollow, noarchive">',
        1,
    )

out = (
    "<!DOCTYPE html>\n<html lang=\"zh-Hant\">\n<head>\n"
    + head.strip()
    + "\n</head>\n<body>\n"
    + body.strip()
    + "\n</body>\n</html>\n"
)
io.open(dst, "w", encoding="utf-8").write(out)
print(f"wrapped -> {dst} ({len(out)/1024/1024:.2f} MB)")
