import random

class Player():
    def __init__(self,name):
        self.name = name
    
    def dice_roll(self,game):
        dice = random.randint(1,6)
        print(f"{self.name}の出た目：{dice}")
        game.countup()
        game.setPosition(self,dice)


class Game():
    def __init__(self):
        #self.p1 = Player("Yuki")
        #self.p2 = Player("Yui")

        self.goal = 20
        self.players = [{'player':Player("Yuki"),'position':0},{'player':Player("Yui"),'position':0}]
        self.count = 0        
    
    def processing(self) -> bool:
        return self.players[0].get('position') < self.goal and self.players[1].get('position') < self.goal #試合中
        

    def player(self) -> Player:
        if self.count % 2 == 0:
            return self.players[0].get('player')
        else:
            return self.players[1].get('player')

    def winner(self) -> Player:
        for p in self.players:
            if(p.get('position') >= self.goal):
                return p.get('player')

    def countup(self):
        self.count +=1

    def setPosition(self,player,dice):
        for p in self.players:
            if(p.get('player') == player):
                p['position'] = p.get('position') + dice
                
                print(f"{p.get('player').name}のコマの状態：{p.get('position')}")      

game = Game()

while game.processing():
    player = game.player()
    player.dice_roll(game)

print(f"{game.winner().name}の勝ち")
