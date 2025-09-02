#포켓몬스터 게임 만들기

import random
import sys
import time

def typewrite(text, delay=0.008, end="\n"):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

player_max_hp = 200
monster_max_hp = 250
player_moves = [("몸통박치기", 35), ("파도타기", 55), ("물대포", 45), ("제비반환", 40)]
monster_moves = [("땅고르기", 40), ("불꽃세례", 35), ("마하펀치", 50)]
crit_rate = 0.2 #치명타확률(20%)
crit_mult = 2 #치명타배율(2배)
player_hp = player_max_hp #초기체력설정
monster_hp = monster_max_hp #초기체력설정
exp = random.randint(50,100)

typewrite("앗! 야생의 파이숭이가 나타났다!\n팽태자는 무엇을 할까?")

def show_status():
    typewrite(f"팽태자 {player_hp}/{player_max_hp} | 파이숭이 {monster_hp}/{monster_max_hp}")

def show_menu():
    typewrite("===기술 선택===")
    for i, (name, power) in enumerate(player_moves, start=1):
        typewrite(f"{i}. {name}")
    typewrite("q: 도망친다")

show_status()
show_menu()

while True:
    cmd = input("행동을 선택하세요: ").strip().lower()

    if cmd == 'q':
        typewrite('무사히 도망쳤다!')
        break
    
    if cmd not in ("1","2","3","4"):
        typewrite("잘못된 입력입니다.")
        continue

    index = int(cmd) - 1
    move_name, base_dmg = player_moves[index]
    dmg = base_dmg + random.randint(-5,5)
    if random.random() < crit_rate:
        dmg *= crit_mult
        typewrite(f"팽태자의 {move_name}!")
        typewrite("급소에 맞았다!")
    else:
        typewrite(f"팽태자의 {move_name}!")

    monster_hp = max(0, monster_hp - dmg)
    typewrite(f"파이숭이의 남은 체력 : {monster_hp}/{monster_max_hp}")
    if monster_hp == 0:
        typewrite(f"상대 파이숭이는 쓰러졌다! 팽태자는 {exp}의 경험치를 얻었다.")
        break

    monster_move_name, monster_base_dmg = random.choice(monster_moves)
    monster_dmg = monster_base_dmg + random.randint(-5,5)
    if random.random() < crit_rate:
        monster_dmg *= crit_mult
        typewrite(f"파이숭이의 {monster_move_name}!")
        typewrite("팽태자의 급소에 맞았다!")
    else:
        typewrite(f"파이숭이의 {monster_move_name}!")

    player_hp = max(0, player_hp - monster_dmg)
    typewrite(f"팽태자의 남은 체력: {player_hp}/{player_max_hp}")
    if player_hp == 0:
        typewrite("팽태자가 쓰러졌다! 지환은 쓰러진 포켓몬을 안고 포켓몬센터로 향했다.")
        break
    show_status()
    show_menu()