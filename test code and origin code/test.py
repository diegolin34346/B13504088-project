import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# 初始化调度器
scheduler = AsyncIOScheduler()

# === 通用指令 ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "歡迎使用 Telegram Bot！請輸入指令。\n"
        "/query_rate - 查詢匯率\n"
        "/download_csv - 下載匯率資料"
    )

async def download_csv(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None) -> None:
    try:
        url = "https://rate.bot.com.tw/xrt/flcsv/0/day"
        response = requests.get(url)
        response.raise_for_status()
        filename = "exchange_rate.csv"
        with open(filename, "wb") as file:
            file.write(response.content)
        if update:
            await update.message.reply_text(f"匯率資料已下載到檔案：{filename}")
        else:
            print(f"[{datetime.now()}] 匯率資料已自動下載到檔案：{filename}")
    except Exception as e:
        if update:
            await update.message.reply_text(f"下載失敗：{e}")
        else:
            print(f"[{datetime.now()}] 自動下載失敗：{e}")

async def query_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        df = pd.read_csv("exchange_rate.csv", index_col=0)
        if not context.args:
            await update.message.reply_text("請輸入索引值，例如：/query_rate USD")
            return

        query_index = context.args[0]
        if query_index in df.index:
            row = df.loc[query_index, ['現金', '現金.1']]
            await update.message.reply_text(
                f"查詢結果：\n現金買入: {row['現金']}\n現金賣出: {row['現金.1']}"
            )
        else:
            await update.message.reply_text("無效的索引值，請檢查輸入內容。")
    except FileNotFoundError:
        await update.message.reply_text("尚未找到 CSV 檔案，請先上傳或執行 /download_csv")
    except Exception as e:
        await update.message.reply_text(f"發生錯誤：{e}")

# === 主程式 ===
async def main():
    token = "7829454083:AAG_HABubDeeF1AOG3g2qhYyNMwrkE9rAVc"
    app = Application.builder().token(token).build()

    print("[INFO] Bot 開始運行")

    # 添加指令處理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download_csv", download_csv))
    app.add_handler(CommandHandler("query_rate", query_rate))

    # 啟動排程器
    scheduler.add_job(download_csv, "cron", hour=12, minute=13)
    scheduler.start()

    # 开始运行 Bot
    try:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        print("[INFO] Bot 正在運行...")
        await asyncio.Event().wait()  # 保持程序运行
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

if __name__ == "__main__":
    # 不使用 asyncio.run，而是使用已有的事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
