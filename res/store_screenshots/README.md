# 商店展示截圖

使用 `res/screenshot` 內最新介面，製作繁體中文暖色系介紹圖。每組依檔名前綴 `01` 至 `06` 上傳。

- `preview.jpg`：六張展示圖總覽，方便快速檢查。
- `google_play/`：1080 × 2340 PNG，適用 Google Play 手機截圖。
- `app_store/`：1290 × 2796 PNG，適用 App Store 6.7 吋截圖欄位。

依序介紹領養列表、條件篩選、認養詳情、遺失寵物、收藏、寵物紀錄。請先以預覽圖確認文案與畫面，再上傳商店。未提供 iPhone 原始畫面；App Store 圖片使用現有 Android 介面截圖合成，送審前請確認與 iOS 版顯示一致。

在 macOS 上安裝 Pillow 後執行 `python3 tools/generate_store_screenshots.py` 可重新產生圖片。
