import unittest
import sys
import io
from main2 import Player, Game

class Test_PlayerPositionCount(unittest.TestCase):

    #setUp()は、テストメソッドが実行されるたびに毎回呼び出されるため、
    #テストごとに新しい、クリーンなオブジェクト（インスタンス）を生成する。

    def setUp(self):
        """
        インスタンス初期化。
        """
        self.players_list = [
            Player("Yuki"),
            Player("Yui"),
            Player("CPU"),
            Player("CPU2")
        ]

        self.game = Game(self.players_list)
        self.player_yuki = self.players_list[0]
        
    def tearDown(self):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def test_array_length(self):
        """
        プレイヤーとポジションのリストの要素数が同じであることをテストする。
        """
        player_list = [d['player'] for d in self.game.players]
        position_list = [d['position'] for d in self.game.players]
        self.assertEqual(len(player_list), len(position_list))
    
    def test_player_and_game_attributes(self):
        """
        プレイヤーの数や名前の長さが適切であることをテストする。
        """
        self.assertEqual(len(self.game.players), 4)
        self.assertGreaterEqual(len(self.game.players), 2)
        
        for player in self.players_list:
            self.assertGreaterEqual(len(player.name), 1)
            self.assertLessEqual(len(player.name), 10)
        
    def test_goal_scale(self):
        """
        ゴールの範囲が適切かどうか
        """
        self.assertGreaterEqual(self.game.goal,6)
        self.assertLessEqual(self.game.goal, 30)

    def test_position_integrate(self):
        """
        newしたときにpositionが０かどうか
        """
        for player_data in self.game.players:
            self.assertEqual(player_data.get('position'),0)

    def test_winner_null(self):
        self.assertIsNotNone(self.game.winner)

    def test_name_type(self):
        for player in self.players_list:
            self.assertIsInstance(player.name, str)

    def test_correct_position(self):
        
        self.assertEqual(self.game.players[0].get('position'),0)
        player = Player("Yuki")
        self.game.setPosition(player,7) #異常値：７
        self.assertEqual(self.game.players[0].get('position'),7)
    
    def test_output(self):
        # 標準入力をダミーの入力に置き換える
        sys.stdin = io.StringIO('¥n')
        # 標準出力をキャプチャするための変数に置き換える
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.player_yuki.dice_roll(self.game)
        # キャプチャした出力を取得
        output = captured_output.getvalue()
        self.assertIn("Yukiの番です。", output)
        self.assertIn("Yukiの出た目：", output)

if __name__ == '__main__':
    unittest.main()