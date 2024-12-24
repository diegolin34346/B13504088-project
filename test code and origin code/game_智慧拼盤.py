#智慧拼盤
#未來延伸：可以亂數出題
import random

#這一題答案658
#盤面，因為太多人要存取盤面，所以放在外面當全域變數
#同學可以改題目
board=[
  [1,2,3],
  [4,0,6],
  [7,5,8]
]

#印出盤面的函數
def print_board():
    #用雙層迴圈印出資料
    for i in range(0,3):
        for j in range(0,3):
            #如果陣列資料是0，印出空白鍵:
            if board[i][j]==0:
              print(" ",end='')
            #不然的話印出該數字
            else:
              print(board[i][j],end='')
        #美觀用換行
        print()

#判斷盤面是否完成
def judge_board():

    #True是完成、False未完成，無罪推定
    complete=True

    #答案，預期的目標
    answer=[
    [1,2,3],
    [4,5,6],
    [7,8,0],
    ]

    #循序檢查3*3的盤面資料
    for i in range(0,3):
        for j in range(0,3):
            #假如盤面的數字跟答案有一個不一樣，就是未完成，可以跳離迴圈省時間
            if board[i][j]!=answer[i][j]:
              complete=False
              break
    #把判斷的結果傳回
    if complete==True:
        return "已完成"
    else:
        return "未完成"

#判斷該數字是否可以動
def check_and_move(user_input):

    #使用者輸入的數字在哪裡？取得列、行
    for i in range(0,3):
        for j in range(0,3):
            #a是指使用者指的數字
            #假如在盤面上找到使用者個輸入
            if board[i][j]==user_input:
              a_x=i
              a_y=j
            #b是指空白的位子，在陣列中以0儲存，避免使用空字串    
            #假如在盤面上找到0，空位處
            if board[i][j]==0:
               b_x=i
               b_y=j
    #如何判斷可以移動
    if abs(a_x-b_x)+abs(a_y-b_y)==1:
        #Python特有交換語法
        #盤面交換
        board[a_x][a_y],board[b_x][b_y]=board[b_x][b_y],board[a_x][a_y]
    else:
        print("不可移動")

def main():
   
    #先印出題目
    print_board()

    while (judge_board()=="未完成"):

        #取得使用者輸入
        user_input=eval(input("你要移動哪個數字"))

        #判斷這個數字是否可以移動，如果可以就移動，然後印出來等待下一次輸入
        #user_input沒有做範圍檢查，請小心
        check_and_move(user_input)
        print_board()
    
    #能夠跳離迴圈走到88行，代表盤面完成，所以遊戲結束
    print("遊戲結束")

if __name__ == "__main__":
    main()