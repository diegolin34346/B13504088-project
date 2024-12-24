import time
import requests

def download_csv():
    url = "https://rate.bot.com.tw/xrt/flcsv/0/day"  # 此為該網站的 CSV 檔案 URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否有 HTTP 錯誤
        filename = "exchange_rate.csv"  # 儲存的檔案名稱
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"{filename} 已成功下載")
    except Exception as e:
        print(f"下載失敗: {e}")

# 設定每天早上9點執行下載

download_csv()