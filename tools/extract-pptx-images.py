#!/usr/bin/env python3
"""從 .pptx 取出所有圖片，並列出「第幾張投影片、左到右第幾個位置」的對照表。

當簡報出了新版、需要重換網頁裡的照片時用這支。
用法：python3 tools/extract-pptx-images.py 某某簡報.pptx 輸出資料夾
"""
import os, shutil, sys, zipfile
import xml.etree.ElementTree as ET

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

pptx, outdir = sys.argv[1], sys.argv[2]
work = os.path.join(outdir, "_pptx")
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work, exist_ok=True)
with zipfile.ZipFile(pptx) as z:
    z.extractall(work)

media = os.path.join(work, "ppt", "media")
shutil.copytree(media, os.path.join(outdir, "media"), dirs_exist_ok=True)

print(f"圖片已複製到 {os.path.join(outdir, 'media')}\n")
print("投影片  位置(由左至右)  檔名                 該投影片的文字")
print("-" * 78)

n = 1
while True:
    slide = os.path.join(work, "ppt", "slides", f"slide{n}.xml")
    if not os.path.exists(slide):
        break
    rels_path = os.path.join(work, "ppt", "slides", "_rels", f"slide{n}.xml.rels")
    rels = {}
    if os.path.exists(rels_path):
        for rel in ET.parse(rels_path).getroot():
            rels[rel.get("Id")] = os.path.basename(rel.get("Target"))

    root = ET.parse(slide).getroot()
    pics = []
    for pic in root.iter(f"{{{NS['p']}}}pic"):
        blip = pic.find(f".//{{{NS['a']}}}blip")
        off = pic.find(f".//{{{NS['a']}}}off")
        rid = blip.get(f"{{{NS['r']}}}embed") if blip is not None else None
        x = int(off.get("x")) if off is not None and off.get("x") else 0
        pics.append((x, rels.get(rid, "?")))
    pics.sort()

    texts = []
    for sp in root.iter(f"{{{NS['p']}}}sp"):
        t = "".join(e.text or "" for e in sp.iter(f"{{{NS['a']}}}t")).strip()
        if t:
            texts.append(t)
    caption = " / ".join(texts[:6])

    for i, (_, fn) in enumerate(pics, 1):
        print(f"{n:>4}  {i:>10}      {fn:<20} {caption[:40]}")
    n += 1

shutil.rmtree(work, ignore_errors=True)
