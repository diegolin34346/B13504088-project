from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import pyttsx3
import os
import webbrowser

# 初始化語音引擎
engine = pyttsx3.init()

def speak(text, filename="response.mp3"):
    """將文字轉為語音並存儲為 mp3 文件"""
    engine.save_to_file(text, filename)
    engine.runAndWait()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令"""
    await update.message.reply_text("Hello! How can I assist you?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理用戶文字訊息"""
    command = update.message.text
    if "Open Google" in command:
        await update.message.reply_text("Opening Google...")
        webbrowser.open("https://www.google.com")
    elif "What is your name" in command:
        await update.message.reply_text("I am your personal assistant, JARVIS.")
    elif "exit" in command or "quit" in command or "bye" in command:
        speak("Goodbye!")
        await update.message.reply_text("Goodbye!")
        await update.message.reply_voice(voice=open("response.mp3", "rb"))
    else:
        await update.message.reply_text("Sorry, I can't do that yet.")

def main():
    token = "7829454083:AAG_HABubDeeF1AOG3g2qhYyNMwrkE9rAVc"
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()