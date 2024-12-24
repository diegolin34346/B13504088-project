import random
#盤面，用二維list做，因為太多人要存取盤面，所以放在外面當全域變數
board=[
[0,0,0],
[0,0,0],
[0,0,0]
]

#印出盤面的函數
#盤面內的資料　：0、1、-1
#顯示出來的樣子：_、0、X
def print_board():
    for i in range(0,3):
        for j in range(0,3):
            #分三種情況輸出對應的符號
            if board[i][j]==0:
              print("_",end='')
            elif board[i][j]==1:
              print("O",end='')
            else:
              print("X",end='')
        #美觀用換行，為什麼？
        print()
    #美觀用換行，為什麼？
    print()


#判斷獲勝的函式，傳入盤面來檢查
def judge_board():
    #判斷的原理是，8種情況，以8個變數分別表示
    #8種情況：橫三線、縱三線、交叉兩線

    #宣告變數並給予初值
    a,b,c,d,e,f,g,h=0,0,0,0,0,0,0,0

    for i in range(0,3):
        #橫三線，請看學習單的規律
        a=a+board[0][i]
        b=b+board[1][i]
        c=c+board[2][i]
        #縱三線
        d=d+board[i][0]
        e=e+board[i][1]
        f=f+board[i][2]
        #交叉線
        g=g+board[i][i]
        h=h+board[i][2-i]
    #判斷方法：交放到集合判斷是否有3和-3
    ans_set={a,b,c,d,e,f,g,h}
        
    if 3 in ans_set:
        return "玩家獲勝"
    if -3 in ans_set:
        print(ans_set)
        return "電腦獲勝"

#電腦下棋
def computer_play():
    
    #r_x亂數從0到2抽一個當成x座標
    #r_y亂數從0到2抽一個當成y座標
    #亂數挑一個沒用到的格子
    r_x=random.randint(0,2)
    r_y=random.randint(0,2)
    
    #如果這格不是空位0，就要再抽一次，直到抽中
    while board[r_x][r_y]!=0: 
        #再抽一次，直到抽中空位
        r_x = random.randint(0,2)
        r_y = random.randint(0,2)

    #能離開while代表找到一格空位，填上代表電腦的-1
    board[r_x][r_y]=-1
    
    #棋，下下去之後，印出來看，列印盤面
    print()
    #副程式結束
    return 

#玩家下棋
def player_play():

    #user_x，落子的x座標
    #user_y，落子的y座標
    #轉換資料型態
    user_x, user_y =map(int,input("請玩家輸入x y座標，中間用空白間隔").split())
    #判斷使用者下的地方合法
    if 0<=user_x<=2 and 0<=user_y<=2 and board[user_x][user_y]==0:
        board[user_x][user_y]=1
        
        #棋，下下去之後，印出來看，列印盤面
        print_board()
    else:
        print("不合法的輸入，機會讓給電腦")


def main():
    
    #遊戲開始，先列印盤面一次
    print_board()
    
    #主程式從這裡開始    
    for i in range(0,5):
      computer_play()
      #電腦下棋
      if judge_board()=="電腦獲勝":
        print("電腦獲勝")
        break
      #判斷
      player_play()  
      #玩家下棋
      if judge_board()=="玩家獲勝":
        print("玩家獲勝")
        break
      #判斷
    #迴圈結束的原因是經過了十步
    print("遊戲結束")
        
if __name__ == "__main__":
  choice=input("開始玩(y/n)?")
  if choice=="y":
    main()