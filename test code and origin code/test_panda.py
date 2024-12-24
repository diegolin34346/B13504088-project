import pandas as pd

# 讀取資料
df = pd.read_csv('exchange_rate.csv')

# 顯示資料概覽
print("資料表概覽：")
print(df.head())

# 輸入範圍
start_row = int(input("請輸入起始行號（從0開始計算）："))
end_row = int(input("請輸入結束行號（包含）："))

# 提取指定範圍的 '現金' 欄位
try:
    selected_data = df.iloc[start_row:end_row + 1][['現金','現金.1']]
    print("\n選取的資料：")
    print(selected_data)
except KeyError:
    print("欄位 '現金' 不存在，請檢查資料表內容。")
except Exception as e:
    print(f"發生錯誤：{e}")