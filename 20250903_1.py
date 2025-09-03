#20250902_1 + HP바 표시

import random #랜덤 모듈
import sys #시스템 모듈
import time #시간 모듈

def typewrite(text, delay=0.03, end="\n"): #타자기 효과
    text = str(text) #문자열로 강제변환
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def hp_bar(cur,mx,bar_len=20): #cur:현재체력, mx:최대체력, bar_len:바길이
    if mx <= 0: return "-" * bar_len #예외처리(체력이 0이하일떄 모두 -표시)
    cur = max(0,min(cur,mx)) #클램핑
    filled = int(bar_len * cur / mx) #채워진 길이(int: 정수로 표시, 바 길이 = 20 * 현재체력 / 최대체력)
    return "█" * filled + "-" * (bar_len - filled) #채워진 부분 + 빈 부분(바 길이 - 채워진 길이는 '-'로 표시)

def show_status(): #체력창
    typewrite(f"팽태자 {player_hp}/{player_max_hp}\n[{hp_bar(player_hp, player_max_hp)}]")
    typewrite(f"파이숭이 {monster_hp}/{monster_max_hp}\n[{hp_bar(monster_hp, monster_max_hp)}]")

def show_menu(): #메뉴창
    typewrite("===기술 선택===")
    for i, (name, power) in enumerate(player_moves, start=1):
        print(f"{i}. {name}")
    print("q: 도망친다")

player_max_hp = 200 #플레이어최대체력
monster_max_hp = 250 #몬스터최대체력
player_moves = [("몸통박치기", 35), ("파도타기", 55), ("물대포", 45), ("제비반환", 40)] #플레이어 기술명, 위력
monster_moves = [("땅고르기", 40), ("불꽃세례", 35), ("마하펀치", 50)] #몬스터 기술명, 위력
crit_rate = 0.2 #치명타확률(20%)
crit_mult = 2 #치명타배율(2배)

player_hp = player_max_hp #초기체력설정
monster_hp = monster_max_hp #초기체력설정
exp = random.randint(50,100) #경험치 범위설정

typewrite("앗! 야생의 파이숭이가 나타났다!\n팽태자는 무엇을 할까?") #게임시작
show_status()
show_menu()

while True: #반복
    cmd = input("행동을 선택하세요: ").strip().lower() #입력값공백제거, 소문자변환

    if cmd == 'q': #도망치기
        typewrite('무사히 도망쳤다!')
        break
    
    if cmd not in ("1","2","3","4"): #잘못된입력
        typewrite("잘못된 입력입니다.")
        continue

    index = int(cmd) - 1 #입력값을 인덱스로 변환
    move_name, base_dmg = player_moves[index] #기술명, 위력
    dmg = base_dmg + random.randint(-5,5) #데미지변동설정
    if random.random() < crit_rate: #치명타확률설정
        dmg *= crit_mult #치명타배율설정
        typewrite(f"팽태자의 {move_name}!")
        typewrite("급소에 맞았다!")
    else:
        typewrite(f"팽태자의 {move_name}!")

    monster_hp = max(0, monster_hp - dmg) #클램핑
    typewrite(f"파이숭이의 남은 체력 : {monster_hp}/{monster_max_hp}[{hp_bar(monster_hp, monster_max_hp)}]") #체력출력
    if monster_hp == 0:
        typewrite(f"상대 파이숭이는 쓰러졌다! 팽태자는 {exp}의 경험치를 얻었다.") #아군 포켓몬의 승리로 게임 종료
        break

    monster_move_name, monster_base_dmg = random.choice(monster_moves) #몬스터기술랜덤선택
    monster_dmg = monster_base_dmg + random.randint(-5,5) #몬스터데미지변동설정
    if random.random() < crit_rate: #치명타확률설정
        monster_dmg *= crit_mult #치명타배율설정
        typewrite(f"파이숭이의 {monster_move_name}!")
        typewrite("팽태자의 급소에 맞았다!")
    else:
        typewrite(f"파이숭이의 {monster_move_name}!")

    player_hp = max(0, player_hp - monster_dmg) #클램핑
    typewrite(f"팽태자의 남은 체력: {player_hp}/{player_max_hp}[{hp_bar(player_hp, player_max_hp)}]") #체력출력
    if player_hp == 0: 
        typewrite("팽태자가 쓰러졌다! 지환은 쓰러진 포켓몬을 안고 포켓몬센터로 향했다.") #적 포켓몬의 승리로 게임 종료
        break
    show_status() #반복
    show_menu()