# 燒肉MEN 創作者合作企劃（手機版）

KOL / KOC 配合事項表 v17 的手機版單頁網站，照片已內嵌於 HTML，單一檔案即可離線瀏覽。

公開網址：https://yakiniku-men.github.io/

- `index.html` — 產出的網頁（勿直接手改，會被 build.sh 覆蓋）
- `build.sh` / `wrap.py` — 由 iCloud「○山城一鳴」資料夾中的成品檔重新產生 index.html
- 已設定 `noindex` 與 `robots.txt`，有連結的人可以打開，但不會被搜尋引擎收錄

更新流程：改好 iCloud 的成品檔 → `./build.sh` → `git commit -am "更新" && git push`
