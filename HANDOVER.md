# 交接手冊 — 燒肉MEN 創作者合作企劃（手機版網頁）

最後更新：2026-08-22

---

## 一、這是什麼

燒肉MEN 給 KOL / KOC 看的合作說明頁，由原本的簡報 `燒肉MEN_KOL_KOC_配合事項表_v17.pptx` 改成手機瀏覽友善的單頁網站。12 個章節、19 張實拍照片全部內嵌在同一個 HTML 檔裡，沒有外部相依，離線也打得開。

**正式網址：https://yakiniku-men.github.io/**

網頁上有一份可勾選的拍攝檢核表，勾選狀態存在瀏覽者自己的手機（localStorage），不會回傳給任何人，也不會跨裝置同步。

---

## 二、東西放在哪

| 用途 | 位置 |
|---|---|
| **內容來源（真正要改的那一份）** | iCloud 雲端硬碟 → `○山城一鳴/燒肉MEN_創作者配合事項表_手機版.html` |
| 網站程式庫（本機） | `~/Projects/yakiniku-men-brief/` |
| 網站程式庫（GitHub） | https://github.com/yakiniku-men/yakiniku-men.github.io |
| 原始簡報與照片素材 | iCloud → `○山城一鳴/燒肉MEN_KOL_KOC_配合事項表_v17.pptx` |

程式庫裡的 `index.html` 是**產生出來的**，不要直接手改，下一次執行 `build.sh` 就會被覆蓋。要改內容一律改 iCloud 那一份。

---

## 三、GitHub 帳號（最容易踩雷的地方）

這台電腦的 `gh` 同時登入**兩個互不隸屬**的 GitHub 帳號：

| 帳號 | 與本專案的關係 |
|---|---|
| **ningchangggg** | ✅ 組織 `yakiniku-men` 的擁有者，**本專案要用這一個** |
| MamiBuyAma | ❌ 與這個組織完全無關，用它推會被拒絕 |

推送前先確認使用中的是哪一個：

```bash
gh auth status
```

若不是 ningchangggg：

```bash
gh auth switch -u ningchangggg
```

**用錯帳號時的症狀**：API 回 `You need admin access to the organization before adding a repository to it`（HTTP 403）。這個錯誤沒辦法靠調整組織權限或授權 OAuth App 解決 —— 唯一的解法就是換成正確的帳號。曾經在這裡卡了很久，請直接跳過那些權限設定頁。

---

## 四、怎麼更新內容

1. 修改 iCloud 的 `燒肉MEN_創作者配合事項表_手機版.html`
2. 執行：

```bash
cd ~/Projects/yakiniku-men-brief && ./build.sh && git commit -am "更新內容" && git push
```

3. 約 1 分鐘後 https://yakiniku-men.github.io/ 生效，網址不變

`build.sh` 做的事：呼叫 `wrap.py`，把 iCloud 那份 HTML 片段補上 `<!DOCTYPE html>`、`<html lang="zh-Hant">`、`<head>`、`<body>` 等外層標籤，加上 `noindex`，輸出成 `index.html`。

確認有沒有上線成功：

```bash
curl -sI https://yakiniku-men.github.io/ | head -1     # 應該回 HTTP/2 200
gh api repos/yakiniku-men/yakiniku-men.github.io/pages --jq .status   # 應該是 built
```

---

## 五、照片怎麼來的

照片是從 `燒肉MEN_KOL_KOC_配合事項表_v17.pptx` 裡取出來的（Google Drive 上的 PDF 被關閉下載權限，抓不到原圖），縮到寬 760px、JPEG 品質 72，再以 base64 直接寫進 HTML。所以整個檔案 1.8 MB，但只需要一個檔、不用管圖片路徑。

簡報若出了新版要換照片，用附的工具列出「投影片 → 圖片 → 位置」對照表：

```bash
python3 tools/extract-pptx-images.py 新版簡報.pptx ~/Desktop/新照片
```

它會把所有圖片複製出來，並印出每張圖屬於第幾張投影片、由左至右第幾個位置，以及該頁的文字，方便對回菜名。**注意**：投影片裡圖片的排列順序和 XML 裡的順序不一致，一定要看位置欄位，不要照檔名編號猜。

---

## 六、幾個要知道的設計決定

**網址為什麼這麼短** — repo 名稱刻意取成 `yakiniku-men.github.io`，和組織同名。GitHub Pages 遇到這種命名會把網站掛在根目錄，所以網址沒有後面那串路徑，也不必手動去開啟 Pages。

**搜尋引擎** — 已加 `<meta name="robots" content="noindex, nofollow, noarchive">` 與 `robots.txt`。有連結的人打得開，但 Google 不會收錄。這份手冊含內部行銷策略、禁語清單與口徑規範，不適合被搜到。

**原始碼是公開的** — 免費 GitHub Pages 需要 public repo，所以任何人都能在 GitHub 上讀到 HTML 原始碼（也就等於讀到禁語清單，雖然網頁本身也看得到）。要藏起來的話有兩條路：升級 GitHub Pro（私有 repo + Pages），或改用 Cloudflare Pages。

**章節編號** — 原始簡報的頁序與頁碼編號對不起來（第 4 頁標 05、第 5 頁標 04、第 6 頁標 03）。網頁是照**簡報自己的編號 01→12** 排列，不是照 PDF 翻頁順序。

---

## 七、踩過的坑

**`wrap.py` 曾經把 `<header>` 標籤吃掉** — 原本清除外層標籤的正則寫成 `</?(html|head|body)[^>]*>`，結果 `<header class="hero">` 開頭的 `<head` 也被匹配，整個首屏排版垮掉。已改成 `</?(?:html|head|body)(?![a-zA-Z])[^>]*>`。之後若再動這支腳本，改完務必確認：

```bash
grep -c '<header' index.html    # 應該是 1
```

**檔案編碼** — HTML 片段一定要保留開頭的 `<meta charset="utf-8">`，少了它中文會變成亂碼。`wrap.py` 會把它移進 `<head>`。

**內容可能被別的地方改動** — 這份 HTML 也同時是 Claude Artifact 的來源檔，可能在別的工作階段被更新。動手前先看一下 iCloud 檔案的修改時間，確認你手上的是最新版。

---

## 八、其他相關位置

| | 網址 | 狀態 |
|---|---|---|
| 正式對外 | https://yakiniku-men.github.io/ | 使用中，發給創作者用這個 |
| 舊版（MamiBuyAma 帳號下） | https://mamibuyama.github.io/yakiniku-men-brief/ | 搬家前的舊位置，還開著。確認新網址沒問題後可轉為 private 或刪除 |
| Claude Artifact | 內容相同的另一個版本 | 分享連結是釘選版本，之後重新發佈時舊連結不會自動更新 |

本機 repo 的 `origin` 已指向新組織；舊位置保留成名為 `mamibuy-old` 的 remote，內容沒有被更動過。

---

## 九、聯絡與帳務

- 組織 `yakiniku-men` 為 GitHub **Free** 方案，這個用途不會產生費用
- 組織擁有者：ningchangggg
- 網站沒有後端、沒有資料庫、沒有分析追蹤，不需要維運
