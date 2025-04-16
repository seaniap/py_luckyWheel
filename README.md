# 幸運輪盤應用程式

這是一個基於 Streamlit 的幸運輪盤應用程式，可以從 Excel 或 CSV 檔案讀取參與者名單，並進行抽獎。

## 特點

- 從 Excel/CSV 檔案匯入參與者名單
- 支援手動輸入參與者名單
- 生動的輪盤動畫效果
- 旋轉音效和獲獎音效
- 記錄獲獎歷史

## 安裝

1. 確保您已安裝 Python 3.7 或更高版本

2. 安裝所需的套件：

```bash
pip install -r requirements.txt
```

## 運行應用程式

```bash
streamlit run app.py
```

## 使用方法

1. 上傳包含參與者名單的 Excel 或 CSV 檔案（檔案中應該有一個名為 "name"、"Name" 或 "姓名" 的欄位，或者使用第一欄作為名稱欄位）

2. 或者在文字區域中手動輸入名單（每行一個名稱）並點擊「確認名單」

3. 點擊「開始抽獎」按鈕進行抽獎

4. 查看側邊欄中的獲獎歷史

## 部署

此應用程式可以部署到以下雲端平台：

- Heroku
- Streamlit Sharing
- Railway
- Fly.io

部署時，只需確保使用 `requirements.txt` 檔案中列出的依賴項。

## 資料儲存

獲獎歷史會保存在 `data/winners.json` 檔案中。

## 許可證

MIT 