#pip install python-telegram-bot[ext]
#pip install apscheduler
#pip install pandas
#pip install requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import requests
import random
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
import webbrowser


# 初始化调度器
scheduler = AsyncIOScheduler()


# === 通用指令 ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("歡迎使用 Telegram Bot！請輸入指令。\n"
                                    "/query_rate - 查詢匯率\n"
                                    "/game - 開始遊戲\n"
                                    "/command - 網站指令")

# === 匯率 ===
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

#處理匯率.csv
async def query_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # 讀取 CSV 檔案，將第一列作為索引
        df = pd.read_csv("exchange_rate.csv", index_col=0)
        if not context.args:
            available_indexes = "\n".join(df.index.tolist())
            await update.message.reply_text(f"可查詢的索引值有：\n{available_indexes}\n\n"
                "請使用指令 `/query_rate 索引值` 進行查詢，例如 `/query_rate USD`")
            return
        
        # 使用者輸入索引值
        query_index = context.args[0]
        
        # 檢查索引是否存在
        if query_index in df.index:
            row = df.loc[query_index, ['現金', '現金.1']]
            await update.message.reply_text(
                f"查詢結果：\n現金買入{row['現金']}\n現金賣出{row['現金.1']}"
            )
        else:
            await update.message.reply_text("無效的索引值，請檢查輸入內容。")
    except FileNotFoundError:
        await update.message.reply_text("尚未找到 CSV 檔案，請先上傳或執行 /download_csv")
    except Exception as e:
        await update.message.reply_text(f"發生錯誤：{e}")

#處理未知指令
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("抱歉，我不認識這個指令。")

# === 拼圖遊戲 ===

def generate_solvable_board():
    numbers = list(range(9))
    while True:
        random.shuffle(numbers)
        if is_solvable(numbers):
            return [numbers[i:i + 3] for i in range(0, 9, 3)]

def is_solvable(numbers):
    inversions = sum(
        1 for i in range(len(numbers)) for j in range(i + 1, len(numbers))
        if numbers[i] > numbers[j] and numbers[i] != 0 and numbers[j] != 0
    )
    return inversions % 2 == 0

def create_puzzle_markup(board):
    keyboard = [
        [
            InlineKeyboardButton(
                text=str(cell) if cell != 0 else "⬜", callback_data=f"puzzle,{i},{j}"
            )
            for j, cell in enumerate(row)
        ]
        for i, row in enumerate(board)
    ]
    return InlineKeyboardMarkup(keyboard)

async def game_puzzle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    board = generate_solvable_board()
    context.user_data["puzzle_board"] = board
    await update.message.reply_text(
        "遊戲開始！請點擊按鈕移動。",
        reply_markup=create_puzzle_markup(board),
    )

async def handle_puzzle_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    board = context.user_data["puzzle_board"]
    i, j = map(int, query.data.split(",")[1:])

    # 找到空格位置
    empty_pos = next((x, y) for x in range(3) for y in range(3) if board[x][y] == 0)

    # 檢查是否可以移動
    if abs(empty_pos[0] - i) + abs(empty_pos[1] - j) == 1:
        board[empty_pos[0]][empty_pos[1]], board[i][j] = board[i][j], board[empty_pos[0]][empty_pos[1]]

    # 檢查是否完成
    if board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
        await query.edit_message_text("恭喜！你完成了拼圖！")
    else:
        await query.edit_message_reply_markup(reply_markup=create_puzzle_markup(board))

# === 井字遊戲 ===

def initialize_ooxx_board():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def create_ooxx_markup(board):
    keyboard = [
        [
            InlineKeyboardButton(
                text="_" if cell == 0 else "O" if cell == 1 else "X", callback_data=f"ooxx,{i},{j}"
            )
            for j, cell in enumerate(row)
        ]
        for i, row in enumerate(board)
    ]
    return InlineKeyboardMarkup(keyboard)

def judge_ooxx_board(board):
    lines = (
        board[0], board[1], board[2],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    )
    for line in lines:
        if line.count(1) == 3:
            return "玩家獲勝"
        if line.count(-1) == 3:
            return "電腦獲勝"
    if all(cell != 0 for row in board for cell in row):
        return "平局"
    return None

def computer_play(board):
    empty_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
    if empty_positions:
        x, y = random.choice(empty_positions)
        board[x][y] = -1

async def game_ooxx(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    board = initialize_ooxx_board()
    context.user_data["ooxx_board"] = board
    await update.message.reply_text(
        "遊戲開始！請選擇一格下棋。",
        reply_markup=create_ooxx_markup(board),
    )

async def handle_ooxx_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    board = context.user_data["ooxx_board"]
    i, j = map(int, query.data.split(",")[1:])

    if board[i][j] == 0:
        board[i][j] = 1
        result = judge_ooxx_board(board)
        if result:
            await query.edit_message_text(f"{result}！", reply_markup=None)
            return
        computer_play(board)
        result = judge_ooxx_board(board)
        if result:
            await query.edit_message_text(f"{result}！", reply_markup=None)
            return
        await query.edit_message_reply_markup(reply_markup=create_ooxx_markup(board))
    else:
        await query.answer("該格已被佔用！", show_alert=True)

#==遊戲清單==
async def game_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("請選擇遊戲\n"
                                    "/game_puzzle - 開始拼圖遊戲\n"
                                    "/game_ooxx - 開始井字遊戲\n")

#==指令==
custom_commands = {
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "fb": "https://www.facebook.com",
    "ntucool": "https://cool.ntu.edu.tw/",
    "sds" : "https://teaching.ch.ntu.edu.tw/"
}
async def command_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("請選擇\n"
                                    "/list_commands - 已有的指令\n"
                                    "/add_command <command> <url> - 新增指令\n"
                                    "/open <command> - 開啟網站")
    
async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /add_command 指令以新增自定義指令"""
    try:
        # 提取用戶輸入的指令及網址
        if len(context.args) < 2:
            await update.message.reply_text("格式錯誤！使用方式：/add_command <command> <url>")
            return
        
        command = context.args[0]  # 自定義指令名稱
        url = context.args[1]  # 自定義對應網址

        # 儲存自定義指令
        custom_commands[command] = url
        await update.message.reply_text(f"成功新增指令：/{command} -> {url}")
    except Exception as e:
        await update.message.reply_text(f"發生錯誤：{e}")

async def open(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理執行自定義指令"""
    command = context.args[0] if context.args else None
    if not command:
        await update.message.reply_text("請提供要執行的指令名稱！")
        return

    if command in custom_commands:
        url = custom_commands[command]
        await update.message.reply_text(f"Opening {url}...")
        webbrowser.open(url)
    else:
        await update.message.reply_text(f"未知的指令：/{command}，請確認是否已新增！")

async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /list_commands 指令，列出所有自定義指令"""
    if custom_commands:
        commands_list = "\n".join([f"/{cmd} -> {url}" for cmd, url in custom_commands.items()])
        await update.message.reply_text(f"以下是可用的指令：\n{commands_list}")
    else:
        await update.message.reply_text("尚未新增任何指令！")

# === 主程式 ===
async def main():
        token = "7829454083:AAG_HABubDeeF1AOG3g2qhYyNMwrkE9rAVc"
        app = Application.builder().token(token).build()

        print("[INFO] Bot 開始運行")

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("download_csv", download_csv))
        app.add_handler(CommandHandler("query_rate", query_rate))
        app.add_handler(CommandHandler("game_puzzle", game_puzzle))
        app.add_handler(CommandHandler("game_ooxx", game_ooxx))
        app.add_handler(CommandHandler("game", game_menu))
        app.add_handler(CallbackQueryHandler(handle_puzzle_move, pattern="^puzzle,"))
        app.add_handler(CallbackQueryHandler(handle_ooxx_move, pattern="^ooxx,"))
        app.add_handler(CommandHandler("unknown", unknown_command))
        app.add_handler(CommandHandler("command", command_menu))
        app.add_handler(CommandHandler("add_command", add_command))
        app.add_handler(CommandHandler("open",open))
        app.add_handler(CommandHandler("list_commands", list_commands))

        # 啟動排程器
        scheduler.add_job(download_csv, "cron", hour=8, minute=0)
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