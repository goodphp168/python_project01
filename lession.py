import random

def guess_number_game():
    print("====== 歡迎來到猜數字遊戲 ======")
    
    # 隨機產生 1 到 100 之間的整數
    target = random.randint(1, 100)
    
    # 設定初始範圍與猜測次數
    min_val = 1
    max_val = 100
    count = 0
    
    while True:
        # 提示使用者輸入數字
        try:
            guess = int(input(f"請輸入一個 {min_val} ~ {max_val} 之間的數字："))
        except ValueError:
            print("請輸入有效的整數數字喔！")
            continue
            
        # 檢查輸入的數字是否在當前範圍內
        if guess < min_val or guess > max_val:
            print(f"超出範圍了！請輸入 {min_val} ~ {max_val} 之間的數字。")
            continue
            
        count += 1
        
        # 判斷結果
        if guess == target:
            print(f"🎉 恭喜你答對了！答案就是 {target}。")
            print(f"你總共猜了 {count} 次。")
            break
        elif guess < target:
            print("太小了！再大一點。")
            min_val = guess + 1  # 動態縮小下限
        else:
            print("太大了！再小一點。")
            max_val = guess - 1  # 動態縮小上限

if __name__ == "__main__":
    guess_number_game()