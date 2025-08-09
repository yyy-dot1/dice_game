import random

class Rule():
    def __init__(self):
        self.players = ['私', 'CPU']
        self.goal = 20

class PlayerBase(Rule):
    def __init__(self, player_name):
        super().__init__()
        self.player_name = player_name
        self.position = 0
        
    def dice_roll(self):
        dice = random.randint(1, 6)
        print(f"サイコロの目: {dice}")
        self.position += dice

class Player1(PlayerBase):
    # player_listにはRuleのplayersが渡されているよ
    def __init__(self, players_list):
        super().__init__(players_list[0])

class Player2(PlayerBase):
    def __init__(self, players_list):
        super().__init__(players_list[1])

class PointState():
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.goal = player2.goal