import random
import sys
import time
import json
import os

# 定義終端機彩色輸出字元碼
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"

# 遊戲難度設定
DIFFICULTY_CONFIG = {
    "1": {"name": "簡單 (Easy)", "range": (1, 50), "max_attempts": float('inf')},
    "2": {"name": "中等 (Medium)", "range": (1, 100), "max_attempts": 10},
    "3": {"name": "困難 (Hard)", "range": (1, 500), "max_attempts": 7}
}

SCORE_FILE = "guess_num_highscores.json"

def load_highscores():
    """載入歷史最高分紀錄"""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_highscore(difficulty_name, score):
    """保存最高分紀錄"""
    scores = load_highscores()
    # 如果還沒有紀錄，或者這次的次數更少，則更新
    if difficulty_name not in scores or score < scores[difficulty_name]:
        scores[difficulty_name] = score
        try:
            with open(SCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            pass
    return False

def print_banner():
    """印出精美的遊戲標題"""
    print(f"\n{CYAN}{'='*50}{RESET}")
    print(f"{BOLD}{YELLOW}      ★  歡迎來到終極「猜數字大小」挑戰！ ★      {RESET}")
    print(f"{CYAN}{'='*50}{RESET}")
    print(f"系統會隨機產生一個數字，請根據提示找出它！")
    print(f"提示會包含：{RED}太大/太小{RESET}、{PURPLE}冷熱距離{RESET}、以及{GREEN}動態縮小區間{RESET}。")
    print(f"{CYAN}{'='*50}{RESET}\n")

def show_highscores():
    """顯示目前的最高分排行榜"""
    scores = load_highscores()
    print(f"{BOLD}{BLUE}[ 歷史最高紀錄 - 最少嘗試次數 ]{RESET}")
    if not scores:
        print("目前尚無任何紀錄，快來創立一個吧！")
    else:
        for diff, score in scores.items():
            print(f"  • {diff}: {score} 次嘗試")
    print()

def get_temperature_hint(secret, guess, max_val):
    """根據猜測數與答案的距離，給予類似冷熱的提示"""
    distance = abs(secret - guess)
    pct = distance / max_val
    
    if pct <= 0.02:
        return f"{RED}【超滾燙！】你已經極度接近答案了！{RESET}"
    elif pct <= 0.05:
        return f"{YELLOW}【溫暖】非常接近了，就在附近！{RESET}"
    elif pct <= 0.15:
        return f"{BLUE}【溫和】有一點點接近了。{RESET}"
    else:
        return f"{PURPLE}【冰冷】距離答案還有一大段距離。{RESET}"

def play_game():
    """單次遊戲的主要邏輯"""
    print_banner()
    show_highscores()
    
    # 選擇難度
    print(f"{BOLD}請選擇難度級別：{RESET}")
    for key, val in DIFFICULTY_CONFIG.items():
        limit_desc = f"無限次機會" if val["max_attempts"] == float('inf') else f"最多 {val['max_attempts']} 次機會"
        print(f"  [{key}] {val['name']} (範圍: {val['range'][0]}~{val['range'][1]}, {limit_desc})")
    
    while True:
        choice = input(f"\n請輸入選項 (1/2/3) 或 [Q] 離開: ").strip().lower()
        if choice in ['q', 'quit', 'exit']:
            print(f"\n{YELLOW}感謝您的遊玩，再見！{RESET}")
            sys.exit(0)
        if choice in DIFFICULTY_CONFIG:
            break
        print(f"{RED}輸入錯誤，請輸入 1, 2, 3 或 Q。{RESET}")

    config = DIFFICULTY_CONFIG[choice]
    min_val, max_val = config["range"]
    max_attempts = config["max_attempts"]
    secret_number = random.randint(min_val, max_val)
    
    print(f"\n{GREEN}系統已成功生成數字！遊戲開始！{RESET}")
    print(f"難度：{BOLD}{config['name']}{RESET}")
    
    attempts = 0
    current_min = min_val
    current_max = max_val
    
    while attempts < max_attempts:
        attempts += 1
        # 計算剩餘次數
        remaining = "無限" if max_attempts == float('inf') else (max_attempts - attempts + 1)
        
        print(f"\n{BLUE}--------------------------------------------------{RESET}")
        print(f"第 {attempts} 次嘗試 {CYAN}(剩餘次數: {remaining}){RESET}")
        print(f"當前可能範圍：{BOLD}{GREEN}[{current_min} ~ {current_max}]{RESET}")
        
        # 取得使用者輸入並驗證
        try:
            user_input = input(f"請輸入你的猜測 ({current_min}-{current_max}): ").strip()
            
            # 支援中途退出
            if user_input.lower() in ['q', 'quit']:
                print(f"\n{YELLOW}遊戲已中止。答案其實是: {secret_number}{RESET}")
                return
                
            guess = int(user_input)
        except ValueError:
            print(f"{RED}無效的輸入！請輸入一個「整數」數字。{RESET}")
            attempts -= 1  # 輸入錯誤不扣除次數
            continue
            
        if guess < min_val or guess > max_val:
            print(f"{RED}警告！超出遊戲最初設定範圍 ({min_val} ~ {max_val})，請重新輸入！{RESET}")
            attempts -= 1
            continue

        # 判斷是否猜中
        if guess == secret_number:
            print(f"\n{GREEN}🎉恭喜你！猜對了！答案就是 {BOLD}{secret_number}{RESET}！🎉")
            print(f"你總共嘗試了 {attempts} 次。")
            
            # 儲存分數
            is_new_record = save_highscore(config['name'], attempts)
            if is_new_record:
                print(f"{YELLOW}🏆 恭喜！您刷新了該難度下的「最少嘗試次數」紀錄！{RESET}")
            break
        else:
            # 給予大小方向提示，並動態更新區間
            if guess < secret_number:
                print(f"{RED}➜ 太小了！{RESET}")
                if guess >= current_min:
                    current_min = guess + 1
            else:
                print(f"{RED}➜ 太大了！{RESET}")
                if guess <= current_max:
                    current_max = guess - 1
            
            # 給予距離溫度提示
            temp_hint = get_temperature_hint(secret_number, guess, max_val - min_val)
            print(temp_hint)
            
    else:
        # 當迴圈正常結束（次數用盡）卻沒猜中時執行
        print(f"\n{RED}慘念！你的次數已經用完了...😭{RESET}")
        print(f"正確答案其實是：{BOLD}{YELLOW}{secret_number}{RESET}")

def main():
    """程式入口，處理重新遊玩的迴圈"""
    try:
        while True:
            play_game()
            print(f"\n{CYAN}{'='*50}{RESET}")
            again = input("想要再挑戰一次嗎？ (Y/N): ").strip().lower()
            if again not in ['y', 'yes', '']:
                print(f"\n{YELLOW}感謝您的遊玩，祝您有美好的一天！再見！{RESET}")
                break
            # 清理畫面 (可選)
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}遊戲被強行中斷。再見！{RESET}")

if __name__ == "__main__":
    main()