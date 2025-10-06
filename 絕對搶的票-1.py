"""
🎫 Ticket Bot — 自動化搶票機器人
Author: 鄭宇翔
Description: 使用 Selenium、pytesseract、fuzzywuzzy 自動化搶票
Version: Public GitHub Edition (Safe)
本程式僅供技術研究與學習用途!! 使用者須遵守目標網站之服務條款與相關法規!! 嚴禁商業用途、濫用或任何違法行為!!
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fuzzywuzzy import fuzz, process
import time
import os

# ======== 使用者設定區 ======== #
CHROMEDRIVER_PATH = "chromedriver"  # 請確認在 PATH 或指定完整路徑（記得下載ChromeDriver)
TIXCRAFT_URL = "搶票網站網址"
TARGET_TEXT = "想搶的票區名稱"          
TICKET_AMOUNT = "張數"                
ZOOM_RATIO = 70                     # 瀏覽器縮放比例（%）
# ============================ #

def login_facebook(driver):
    """登入 Facebook（使用者輸入帳密）"""
    print("登入 Facebook 中...")

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "pass")

    username = input("請輸入 Facebook 帳號：")
    password = input("請輸入 Facebook 密碼（輸入過程不會顯示）：" if os.name != 'nt' else "請輸入 Facebook 密碼：")

    username_input.clear()
    password_input.clear()
    username_input.send_keys(username)
    password_input.send_keys(password)

    login_btn = driver.find_element(By.NAME, "login")
    login_btn.click()
    print("Facebook 登入完成")

def find_best_ticket(driver):
    """模糊搜尋票區文字並自動點擊"""
    print("搜尋票區中...")
    try:
        buttons = driver.find_elements(By.TAG_NAME, "a")
        button_texts = [b.text for b in buttons if b.text.strip()]
        best_match = process.extractOne(TARGET_TEXT, button_texts, scorer=fuzz.partial_ratio)
        if best_match:
            for b in buttons:
                if b.text == best_match[0]:
                    driver.execute_script("arguments[0].click();", b)
                    print(f" 點擊成功：{best_match[0]}（相似度 {best_match[1]}）")
                    return True
    except Exception as e:
        print(f"找票失敗：{e}")
    return False

def select_ticket(driver):
    """選擇張數與同意條款"""
    print("選擇票數與同意條款中...")
    driver.execute_script(f"document.body.style.zoom='{ZOOM_RATIO}%'")

    for i in range(100):
        element_id = f"TicketForm_ticketPrice_{i:02d}"
        try:
            element = driver.find_element(By.ID, element_id)
            element.send_keys(TICKET_AMOUNT)
            print(f"填寫票數：{TICKET_AMOUNT}")
            break
        except NoSuchElementException:
            continue

    # 同意條款
    try:
        agree = driver.find_element(By.ID, "TicketForm_agree")
        agree.click()
        print("已勾選同意條款")
    except Exception:
        print("找不到同意條款按鈕")

def main():
    """主程式流程"""
    print("啟動搶票機器人...")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get("https://tixcraft.com/")

    # 同意 cookies
    try:
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
    except TimeoutException:
        print("找不到 cookies 按鈕，略過。")

    # 點擊登入
    try:
        login_btn = driver.find_element(By.CLASS_NAME, "justify-content-center")
        login_btn.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "facebook"))).click()
        login_facebook(driver)
    except Exception as e:
        print(f"登入流程出現問題：{e}")

    # 進入活動頁面
    driver.get(TIXCRAFT_URL)
    print(f"進入活動頁面：{TIXCRAFT_URL}")

    if find_best_ticket(driver):
        select_ticket(driver)
    else:
        print("未成功找到目標票區，請手動確認。")

    print("請手動輸入驗證碼後完成流程。")
    input("按 Enter 鍵結束程式...")
    driver.quit()

if __name__ == "__main__":
    main()
