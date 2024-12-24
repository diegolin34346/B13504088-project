from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import webbrowser

# 用於存儲使用者自定義指令及網址的字典
custom_commands = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令"""
    await update.message.reply_text("Hello! How can I assist you?\n"
                                    "Use /add_command <command> <url> to add custom commands.\n"
                                    "Use /list_commands to view available commands.")

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

async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

def main():
    token = "7829454083:AAG_HABubDeeF1AOG3g2qhYyNMwrkE9rAVc"
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_command", add_command))
    app.add_handler(CommandHandler("execute_command", execute_command))
    app.add_handler(CommandHandler("list_commands", list_commands))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
