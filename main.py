import random
from abc import ABC

class PlayerBase(ABC):
    def dice_roll(self,game):
        pass
class Player(PlayerBase):
    is_numan = True
    def dice_roll(self,game):
        print(f"人間")
        入力する
class CPU(PlayerBase):
    is_numan = False
    def dice_roll(self,game):
        print(f"CPPU")
        自動モード

class Player():
    MIN_NAME: int = 1
    MAX_NAME: int = 10
    def __init__(self,name:str,is_human:bool):
        
        self.is_human = is_human   
        count = len(name)

        if not(Player.MIN_NAME <= count <= Player.MAX_NAME):
            raise ValueError(f"名前は{Player.MIN_NAME}文字から10文字の間で入力してください。")
        
        self.name = name
    
    def dice_roll(self,game):

        if self.is_human:
            input(f"{self.name}の番です。")
            dice = random.randint(1,6)
            if dice == 5:
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice)
            
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)
        else:
            dice = random.randint(1,8)
            if dice == 5:
                ("もう一度サイコロを振りましょう")
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice)
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)

    def test_dice_roll(self,game,dice):
        if self.is_human:
            input(f"{self.name}の番です。")
            if dice == 5:
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice)
            
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)
        else:
            if dice == 5:
                ("もう一度サイコロを振りましょう")
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice)
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)

    def test_dice_roll2(self,game,dice_result):
        dice = dice_result[0]
        if self.is_human:
            input(f"{self.name}の番です。")
            if dice == 5:
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice_result[1])
            
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)
        else:
            if dice == 5:
                ("もう一度サイコロを振りましょう")
                print(f"{self.name}の出た目：{dice}")
                game.setPosition(self,dice_result[1])
            else:
                print(f"{self.name}の出た目：{dice}")
                game.countup()
                game.setPosition(self,dice)

    #予期せぬデータが入ってきたときにエラーを防ぐためのもの
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False

class Game():
    def __init__(self,players,goal:int):
       
        self.count = 0  
        self.players = [] #受け取ったplayersリストをそのまま代入するのではなく、新しいリストを生成。
              
        if not(6 <= self.goal <= 30):
            raise ValueError("無効な範囲の値です。")
        
        self.goal = goal
    
        for i in players:
            self.players.append({'player': i, 'position': 0})
            self.player_len = len(self.players)
            
        #self.playersの中身
        # {'player': Player("A", True), 'position': 0}
    
    def processing(self) -> bool:
        for p in self.players:
            if p.get('position') >= self.goal:
                return False
        return True 

    def current_player(self) -> Player:
        num = self.count % self.player_len
        return self.players[num]['player'] #num番目の要素の'player'を取り出す
            
    def winner(self) -> Player:
        for p in self.players:
            if p.get('position') >= self.goal:
                return p.get('player')

    def countup(self):
         self.count +=1

    def setPosition(self,player,dice):
        for p in self.players:
            if p.get('player') == player:
                if dice != 3:
                    p['position'] += dice
                else:
                    p['position'] -= dice 
                print(f"{p.get('player').name}のコマの状態：{p.get('position')}")

            if self.goal < p.get('position'):
                tmp = p['position'] - self.goal
                p['position'] =  self.goal  - tmp                
                print(f"{tmp}マス戻ります。")                       
PlayerBase players2 = [
    Player("Yuki"),
    CPU("hoge"),
]
players2[0].is_numan: trueが帰る
players2[1].is_numan: falseが帰る

players = [
            Player("Yuki",True),
            Player("Yui",True),
            Player("CPU",False),
            Player("CPU2",False)
            ]

def main() -> None:
    game = Game(players,20) #Playerクラスに変更を加えたため、引数にgoalの値を追加
    while game.processing():
        player = game.current_player()
        player.dice_roll(game)

    print(f"{game.winner().name}の勝ち")

if __name__ == '__main__':
    main()