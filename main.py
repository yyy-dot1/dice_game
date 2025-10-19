import random
import time
from abc import ABC, abstractmethod
#サイコロの目の値を決めます
class Dice():
    def __init__(self, min_val=1, max_val=6):
        self.min_val = min_val
        self.max_val = max_val
        self.current_value: int = -1

    """
    サイコロの目の値を管理しよう。
    """
    def roll(self):
        self.current_value = random.randint(self.min_val, self.max_val)
        return self.current_value
    
    def is_twice(self):
        return self.current_value == 5
    
    """
    サイコロを振り、出た目と効果を適用した最終的な移動量を返す。
    """
    def get_effected_value(self):
        """
        3の目が出たら、マスを戻す
        """
        if self.current_value == 3:
            return -self.current_value
        return self.current_value
    
#継承基底クラス
class PlayerBase(ABC):
    def __init__(self, name: str):
        #名前の文字数制約
        if not (1 <= len(name) <= 10):
            #エラーハンドリングで呼び出し元に戻す
            raise ValueError("名前は1文字から10文字の間で入力してください。")
        #文字数制約をクリアしたもののみ、self.nameに外部からのnameを渡す
        self.name = name

    #継承メソッド
    #このメソッドでは、こういう引数を使うだろう〜という設計を決める
    @abstractmethod
    def dice_roll(self, game, dice_instance):
        pass

    ## def __dece_role(self):

#PlayerBaseの実装クラス
class Player(PlayerBase):
    def __init__(self, name: str):
        super().__init__(name)

#人間用
# dice_rollメソッドを宣言する
    def dice_roll(self, game, dice: Dice):
        print(f"人間: {self.name}の番です。")
        input("サイコロを振るにはエンターキーを押してください。")
        
        # dice_instanceから最終的な移動量を取得する
        dice.roll()
        if dice.is_twice():
            game.setPosition(self, dice.get_effected_value())
            self.dice_roll(game, dice)
        else:
            # ゲームクラスに移動を任せる
            game.setPosition(self, dice.get_effected_value())
            game.countup()

#CPU用
# dice_rollメソッドを宣言する
class CPU(PlayerBase):
    def __init__(self, name: str):
        super().__init__(name)

    def dice_roll(self, game, dice):
        print(f"CPU: {self.name}の番です。")
        #inputの代わりに待ちを発生させる
        time.sleep(1)
        
        # dice_instanceから最終的な移動量を取得する
        dice.roll()
        if dice.is_twice():
            game.setPosition(self, dice.get_effected_value())
            self.dice_roll(game, dice)
        else:
            # ゲームクラスに移動を任せる
            game.setPosition(self, dice.get_effected_value())
            game.countup()



class Game():
    def __init__(self, players, goal: int):
        #プレイヤーの人数の制約
        if not (2 <= len(players) <= 4):
            #エラーハンドリング
            #raiseで呼び出し元へ戻す
            raise ValueError("プレイヤーの人数は2人から4人の間で入力してください。")
        #ゴール値の制約
        if not (6 <= goal <= 30):
            #エラーハンドリング
            #raiseで呼び出し元へ戻す
            raise ValueError("ゴールのマスは6から30の間で設定してください。")
        
        #制約の範囲内だった場合、引数で渡されたものをselfに取得する
        self.goal = goal
        self.count = 0
        #playerとpositionはセットで管理したいため、辞書型を使う
        self.players = [{'player': p, 'position': 0} for p in players]
        self.player_len = len(self.players)

    #各プレイヤー・CPUのコマの状態を管理する
    def processing(self) -> bool:
        for p in self.players:
            #対戦中はtrue
            if p.get('position') >= self.goal:
                return False
        return True

    #今、サイコロを投げるプレイヤーorCPUを管理する
    #countを人数で割る(ex: 4/4=0　→ players[0]="Yuki")
    #countはcountupメソッドで加算する
    def current_player(self):
        num = self.count % self.player_len
        return self.players[num]['player']

    #勝者を管理する
    def winner(self):
        for p in self.players:
            if p.get('position') >= self.goal:
                return p.get('player')
    #countの加算を行う
    def countup(self):
        self.count += 1

    #コマの進みを管理する
    def setPosition(self, player, total_move):
        for p in self.players:
            if p.get('player') == player:
                # 最終的な移動量を使ってコマを進める
                p['position'] += total_move
                
                print(f"{p.get('player').name}のコマの状態：{p.get('position')}")
                
                # ゴールを過ぎたらコマを戻す
                if self.goal < p.get('position'):
                    tmp = p['position'] - self.goal
                    p['position'] = self.goal - tmp
                    print(f"{tmp}マス戻ります。")
                break
#main関数
def main() -> None:
    print("すごろくゲームを開始します。")
    players = [
        Player("Yuki"),
        Player("Yui"),
        CPU("CPU"),
        CPU("CPU2")
    ]
    
    dice = Dice()
    #Gameクラスの引数: players, goal
    game = Game(players, 20)

    #ゲームが進行中の間、
    while game.processing():
        #current_playerメソッドを呼び出して、サイコロを振る順番を決める
        player = game.current_player()
        #サイコロをふる
        # dice_rollの引数: game, dice_instance
        player.dice_roll(game, dice)

    print(f"{game.winner().name}の勝ちです！")

if __name__ == '__main__':
    main()
