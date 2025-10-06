
> **本程式僅供技術研究與學習用途!**
> **使用者須遵守目標網站之服務條款與相關法規!** 
> **嚴禁商業用途、濫用或任何違法行為!**

# TicketBot – 自動化搶票機器人

一個以 **Python + Selenium** 建立的自動化搶票工具，  
能自動開啟瀏覽器、登入帳號、模糊比對座位名稱並自動選取票區。

---

## 專案功能
- 自動登入 TixCraft（支援 Facebook 登入）
- 模糊比對目標票區名稱並自動點擊
- 自動選擇票數、勾選同意條款
- 可搭配 OCR（pytesseract）驗證碼辨識擴充
- 模組化結構，方便修改與擴充

---

## 執行步驟

1. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
2.下載並安裝 ChromeDriver，並確認與瀏覽器版本相符。

3.執行主程式：
   ```bash
   python main.py
   ```
4.依照提示輸入 Facebook 帳號密碼。
