# WordPress 嵌入方式

這三個檔案各自獨立：

1. 將 `adopt-pet.html` 全部內容貼到文章或頁面的「自訂 HTML」區塊。
2. 將 `adopt-pet.css` 全部內容貼到 WordPress「外觀 → 自訂 → 額外 CSS」，或你的主題自訂 CSS 欄位。
3. 將 `adopt-pet.js` 全部內容加入網站的頁尾 JavaScript 欄位，例如 WPCode 的 Custom JavaScript（Footer）。不要在「自訂 HTML」區塊內貼 JavaScript。

JavaScript 只控制預覽圖的左右按鈕；即使網站停用 JavaScript，訪客仍能左右滑動圖片，下載連結也能使用。所有樣式都限制在 `.nap-wp` 區塊內，避免影響部落格其他內容。

版型沿用 GitHub Pages 首頁的暖色主視覺、功能卡片、引言、畫面預覽和下載區。此區塊會填滿 WordPress 父容器寬度；若要讓背景延伸到整個螢幕，頁面請選「全寬」範本。若主題限制內容寬度，區塊會依容器寬度自動改成單欄。

圖片由 `https://qn5566.github.io/newAdoptPet/` 載入。若將來搬移 GitHub Pages 網址，需同步替換 HTML 中的圖片 URL。

新增 WordPress 頁面時，SEO 外掛欄位和社群分享圖片請參考 `seo.md`。
