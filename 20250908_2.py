#20250903_2.py + 상태이상 지속 데미지

import random #랜덤 모듈
import sys #시스템 모듈
import time #시간 모듈

player_max_hp = 200 #플레이어최대체력
monster_max_hp = 250 #몬스터최대체력
player_moves = [("몸통박치기", 35), ("파도타기", 55), ("물대포", 45), ("제비반환", 40)] #플레이어 기술명, 위력
monster_moves = [("도꺠비불", 0), ("땅고르기", 40), ("불꽃세례", 35), ("마하펀치", 50)] #몬스터 기술명, 위력
crit_rate = 0.2 #치명타확률(20%)
crit_mult = 2 #치명타배율(2배)
burn_turn, burn_damage = 3, 20
player_burn = 0

player_hp = player_max_hp #초기체력설정
monster_hp = monster_max_hp #초기체력설정
exp = random.randint(50,100) #경험치 범위설정

inventory = {"상처약":5, "좋은상처약":2}
HEAL = {"상처약":20, "좋은상처약":50}

def status_tag():
    return f" [BURN x{player_burn}]" if player_burn>0 else ""

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
    print(f"팽태자 {player_hp}/{player_max_hp}\n[{hp_bar(player_hp, player_max_hp)}]")
    print(f"파이숭이 {monster_hp}/{monster_max_hp}\n[{hp_bar(monster_hp, monster_max_hp)}]")

def show_menu(): #메뉴창
    typewrite("===기술 선택===")
    for i, (name, power) in enumerate(player_moves, start=1):
        print(f"{i}. {name}")
    print("i: 가방")
    print("q: 도망친다")

def use_item():
    global player_hp
    usable = [(name, count) for name, count in inventory.items() if count > 0] #리스트 내포 방식으로 사용가능한 아이템만 갯수와 함꼐 표시
    if not usable:
        typewrite("가방이 비어 있습니다.")
        return None #아무 값도 돌려주지 않는다 (return: 함수의 결과값 출력)
    typewrite("\n=== 가방 ===")
    for i,(name, count) in enumerate(usable, start=1):
        print(f"{i}. {name} (x{count})")
    typewrite("b: 돌아가기\n")
    select = input("사용할 아이템: ").strip().lower()
    if select == "b":
        typewrite("가방을 닫았다.")
        return None
    if not select.isdigit(): #잘못된 입력을 했을때
        typewrite("잘못된 입력입니다! \n")
        return None
    index_item = int(select) -1 #아이템 하나 소진
    if index_item < 0 or index_item >= len(usable): #아이템이 존재하지 않을때(len:리스트의 길이), 입력한 번호가 리스트 범위 밖이라는 뜻
        typewrite("아이템이 존재하지 않습니다!")
        return None
    item = usable[index_item][0] #아이템은 usable이라는 튜플의 첫번쨰 값(이름)
    heal = HEAL.get(item,0)
    if heal <= 0:
        typewrite("써도 효과가 없다!")
        return None
    missing = player_max_hp - player_hp
    healed = min(heal, max(0, missing))
    if healed == 0:
        typewrite("써도 효과가 없다!")
        return None
    player_hp += healed
    player_hp = min(player_max_hp, player_hp+healed)
    inventory[item]-=1
    typewrite(f"{item}을 썼다! \n팽태자의 체력이 {healed} 회복되었다.\n")
    return True
    
def end_of_turn_effects():
    global player_hp, player_burn
    if player_burn > 0:
        player_hp = max(0, player_hp - burn_damage)
        typewrite(f"팽태자는 화상 데미지를 입고 있다")
        player_burn -= 1
        if player_burn == 0:
            typewrite("팽태자의 화상이 풀렸다!")
        return player_hp == 0
    return False

def monster_turn():
    global player_hp,player_burn
    move_name, base = random.choice(monster_moves)
    dmg = base + random.randint(-5,5)
    if move_name == "도꺠비불":
        typewrite("파이숭이의 도깨비불!")
        if player_burn == 0:
            player_burn = burn_turn
            typewrite("팽태자는 화상을 입었다!")
        else:
            typewrite("그러나 팽태자는 이미 화상 데미지를 입고 있다...")
        return player_hp == 0

    if random.random() < crit_rate:
        dmg *= crit_mult
        typewrite(f"파이숭이의 {move_name}!\n급소에 맞았다!")
    else:
        typewrite(f"파이숭이의 {move_name}!")
    player_hp = max(0, player_hp - dmg)
    typewrite(f"팽태자의 남은 체력: {player_hp}/{player_max_hp}[{hp_bar(player_hp, player_max_hp)}]")
    return player_hp == 0        

typewrite("앗! 야생의 파이숭이가 나타났다!\n팽태자는 무엇을 할까?") #게임시작
show_status()
show_menu()


while True: #반복
    cmd = input("행동을 선택하세요: ").strip().lower() #입력값공백제거, 소문자변환

    if cmd == 'q': #도망치기
        typewrite('무사히 도망쳤다!')
        break
    
    if cmd == 'i':
        used = use_item()
        if used is None:
            show_status()
            show_menu()
            continue
        if monster_turn():
            typewrite("팽태자가 쓰러졌다! 지환은 쓰러진 포켓몬을 안고 포켓몬센터로 향했다.")
            break
        if end_of_turn_effects():
            typewrite("팽태자가 쓰러졌다!"); break
        typewrite("")
        show_status()
        show_menu()
        continue
    
    if cmd not in ("1","2","3","4","q","i"): #잘못된입력
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

    if monster_turn():
        typewrite("팽태자가 쓰러졌다! 지환은 쓰러진 포켓몬을 안고 포켓몬센터로 향했다.")
        break
    if end_of_turn_effects():
        typewrite("팽태자가 쓰러졌다! 지환은 쓰러진 포켓몬을 안고 포켓몬센터로 향했다.")
    
    show_status()
    show_menu()

