import random

class Player():
    def __init__(self,name):
        self.name = name
    
    def dice_roll(self,game):
        input(f"{self.name}の番です。")
        dice = random.randint(1,6)
        print(f"{self.name}の出た目：{dice}")
        game.countup()
        game.setPosition(self,dice)

    #予期せぬデータが入ってきたときにエラーを防ぐためのもの
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False


class Game():
    def __init__(self):

        self.goal = 20
        self.players = [
            {'player':Player("Yuki"),'position':0},
            {'player':Player("Yui"),'position':0},
            {'player':Player("CPU"),'position':0},
            {'player':Player("CPU2"),'position':0}
            ]
        self.count = 0  
        self.player_len = len(self.players)
    
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
            if(p.get('player') == player):
                p['position'] += dice
                
                print(f"{p.get('player').name}のコマの状態：{p.get('position')}")      

game = Game()

while game.processing():
    player = game.current_player()
    player.dice_roll(game)

print(f"{game.winner().name}の勝ち")
