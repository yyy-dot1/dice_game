from sugoroku1 import Rule, Player1, Player2, PointState

rules = Rule()
player1 = Player1(rules.players)
player2 = Player2(rules.players)
game_state = PointState(player1, player2)

print("ゲーム開始")
print(f"目標地点: {game_state.goal}")

while True:
    print(f" {player1.player_name}の順番")
    input()
    player1.dice_roll() #player1オブジェクトのdice_rollメソッドを呼び出す
    
    print(f"{player1.player_name}の現在位置: {player1.position}")
    print(f"{player2.player_name}の現在位置: {player2.position}")

    if player1.position >= game_state.goal:
        print(f" {player1.player_name}の勝ち！")
        break

    print(f"{player2.player_name}の順番")
    player2.dice_roll() #player2オブジェクトのdice_rollメソッドを呼び出す
    
    print(f"{player1.player_name}の現在位置: {player1.position}")
    print(f"{player2.player_name}の現在位置: {player2.position}")

    if player2.position >= game_state.goal:
        print(f"{player2.player_name}の勝ち！")
        break

print("ゲーム終了")