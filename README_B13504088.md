# Telegram bot 

![contribution](https://img.shields.io/badge/contributions-welcome-blue)
![python](https://img.shields.io/badge/Python-3.9_or_later-green)
![pillow](https://img.shields.io/badge/Pillow-9.0_or_later-green)

此文檔說明telegram bot的功能及設計過程。該程式旨在為使用者提供便利的方式，讓使用者能夠定時從指定網址下載檔案，並能夠增加指令的方式迅速開啟指定網頁，此外，也提供內建的小遊戲供使用者遊玩。

## (1) 程式的功能 Features

1.定時下載指定網址的檔案，此程式以台灣銀行牌告匯率的csv檔為例.

2.匯率查詢：透過即時下載匯率資料，使用者可以快速查詢特定貨幣的匯率.

3.遊戲功能：

    (1)拼圖遊戲：簡單直觀的圖形介面，挑戰使用者的邏輯與思考能力。
    
    (2)井字遊戲：經典的井字遊戲，支援玩家對戰電腦。
    
4.網站快捷指令：使用者可以自定義指令，快速開啟常用網站。


## (2) 使用方式 Usage

### 1. Set Up Your Environment

```bash
# 下載
pip install python-telegram-bot[ext]
pip install apscheduler
pip install pandas
pip install requests

```
### 2. 創建一個telegram bot，並獲取Bot API
於telegramn搜尋Bot Father，並透過Bot Father創建一個新的telegram bot(創建完新的telegram bot後需與之對話才能啟用)

### 3. 注意事項

1.啟用程式後即可使用telegram bot的各項功能

2.需將主程式中的token換為自己的API後才可使用

3.示範用的匯率檔案預設為早上8點自動載入，若欲調整下載時間則需於主程式中的啟動排程器部分調整時間

### 4. 指令介紹

/start：顯示歡迎訊息與可用指令清單。

/query_rate：查詢匯率，格式：/query_rate <貨幣代碼>，例如 /query_rate USD。

/game：顯示可用遊戲清單。

/game_puzzle：開始拼圖遊戲。

/game_ooxx：開始井字遊戲。

/command：進入網站快捷指令管理介面。

/add_command <指令名稱> <網址>：新增快捷指令。

/open <指令名稱>：開啟對應的網站。

/list_commands：顯示目前所有的快捷指令。


## (3) 程式的架構 Program Architecture

The project is organized as follows:

```
project_directory/
├── telegram_bot.py               # 程式主文件
├── exchange_rate.csv      # 匯率資料檔案 (由程式自動生成)
└── README.md              # 使用說明文件
```

- **核心組件**:
  - `telegram_bot.py`: 處理所有函式
    
## (4) 開發過程 Development Process

開發過程分為以下幾個步驟：

1.**功能規劃**：確定程式的主要功能，包括匯率查詢、遊戲設計與快捷指令。

2.**核心功能開發**:
    (1)定時下載csv檔 : 透過 `request` 向指定網站要求下載檔案，並透過 `scheduler` 使之能夠定時運行

    (2)處理csv檔 : 透過 `pandas` 將csv檔讀入後，使用 `loc` 選出指定行並讓使用者指定列，最後透過     `update.message.reply_text`向使用者輸出資料
    
    (3)智慧拼盤遊戲 : 透過 `random` 產生隨機盤面並確認是否是可解答的，透過telegram bot中的按鈕系統達成與使用者互動，並讓使用者觸碰的方塊進行移動

    (4)井字遊戲 : 透過telegram bot中的按鈕系統達成與使用者互動，並讓使用者選擇要添加符號的方塊，再用 `random` 使產生符號於未填入之空格直至遊戲結束

    (5)快捷指令 : 先建立 `dictionary` 當使用者需新增指令時，便將新指令與指定網址寫入 `dictionary`，使telegram bot 接收到特定指令時，能找到指定網址，並透過 `webbrowser` 開啟指定網頁
    
3**程式實現**：先自己按照發想出的需求寫出程式，再透過chatgpt轉換為 python-telegram-bot 能運行方式以實現功能。

4**測試與優化**：針對不同指令進行測試，並新增 /game_menu 及 /command_menu 使程式確保穩定性與也增加程式介面的易用性。

5**文檔與說明** : 編寫 `README.md` 文件，使新使用者能理解程式的運作並增加易用性

## (5) 參考資料來源 References

1. ChatGPT - 協助編寫內容 <https://chatgpt.com/share/676aff22-0b1c-8013-a19f-3ee02a89241c> <https://chatgpt.com/share/676aff50-4f08-8013-9e02-33eb648b8084> <https://chatgpt.com/share/676aff72-5598-800a-97ad-2d1b34afdcb6>

2. 上課助教提供之panda檔案

## (6) 程式修改或增強的內容 Enhancements and Contributions

1.**自動更新匯率資料**：透過定時器每天自動下載最新匯率。

2.**遊戲功能擴展**：支援拼圖遊戲與井字遊戲，提升互動性。

3.**快捷指令功能**：允許用戶新增和管理自定義指令以快速訪問網站。

4.**錯誤處理**：加入對指令錯誤或缺失的友善提示，增強用戶體驗。
3. Developed comprehensive usage examples and structured documentation.
4. Added error handling for unsupported file types and missing inputs.
