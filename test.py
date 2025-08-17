import unittest
import sys
import io
from main2 import PlayerBase, Player, CPU, Game, Dice

#Playerクラスのテスト
class Test_Player(unittest.TestCase):

    """
    プレイヤー名の文字数が制約を満たすかどうか、チェックする
    """
    def test_player_name_len_true(self):
        #プレイヤーをYukiにする
        player = Player("Yuki")
        #assertGreaterEqualメソッドでプレイヤー名が1以上かどうかチェック
        self.assertGreaterEqual(len(player.name), 1)
        #assertLessEqualメソッドでプレイヤー名が10未満かどうかチェック
        self.assertLessEqual(len(player.name), 10)

    """
    プレイヤー名の文字数が制約を満足さない場合、エラー処理が実行されるかどうかチェックする
    """
    def test_player_name_len_false(self):
        #エラーハンドリング
        with self.assertRaises(ValueError):
            #プレイヤー名をNULLとする
            Player("")
        #エラーハンドリング
        with self.assertRaises(ValueError):
            #プレイヤー名を10文字以上にする
            Player("abcdefghijklmn")

#CPUクラスのテスト
class Test_CPU(unittest.TestCase):
    
    """
    CPU名の文字数が制約を満足さない場合、エラー処理が実行されるかどうかチェックする
    """
    def test_cpu_name_len_true(self):
        cpu = CPU("CPU")
        self.assertGreaterEqual(len(cpu.name), 1)
        self.assertLessEqual(len(cpu.name), 10)

    def test_player_name_len_false(self):
        #エラーハンドリング
        with self.assertRaises(ValueError):
            #CPU名をNULLとする
            CPU("")
        #エラーハンドリング
        with self.assertRaises(ValueError):
            #CPU名を10文字以上にする
            CPU("abcdefghijklmn")

#Gameクラスのテスト
class Test_Game(unittest.TestCase):

    """
    setUpメソッドで初期化を行う
    """

    def setUp(self):
        self.players_list = [
            Player("Yuki"),
            Player("Yui"),
            CPU("CPU"),
            CPU("CPU2")
        ]

        #Gameクラスをnewする
        self.game = Game(self.players_list, 20)
    
    #リソースのクリーンアップをする
    def tearDown(self):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    """
    辞書型のplayersのplayerとpositionの組み合わせが適切かどうか、チェックする
    """
    def test_array_length(self):
        player_list = [d['player'] for d in self.game.players]
        position_list = [d['position'] for d in self.game.players]
        #要素数のチェック
        #本当にチェックできてる？
        self.assertEqual(len(player_list), len(position_list))
    
    """
    対戦人数が制約を満たすかどうか、チェックする
    """
    def test_player_num_true(self):
        #2名の場合のチェック
        players_2 = [Player("Yuki"), Player("Yui")]
        game_2 = Game(players_2, 20)
        self.assertGreaterEqual(len(game_2.players), 2)
        self.assertLessEqual(len(game_2.players), 4)
        #3名の場合のチェック
        players_list3 = [Player("Yuki"), Player("Yui"), CPU("CPU")]
        game_3 = Game(players_list3, 20)
        self.assertGreaterEqual(len(game_3.players), 2)
        self.assertLessEqual(len(game_3.players), 4)
        #4名の場合のチェック
        self.assertGreaterEqual(len(self.game.players), 2)
        self.assertLessEqual(len(self.game.players), 4)

    """
    対戦人数が制約を満たさない場合、エラー処理が実行されるかどうかチェックする
    """
    def test_player_num_false(self):
        #エラーハンドリング
        #1名の場合のチェック
        with self.assertRaises(ValueError):
            players_list1 = [Player("Yuki")]
            Game(players_list1, 20)
        
        #エラーハンドリング
        #5名の場合のチェック
        with self.assertRaises(ValueError):
            players_list5 = [
                Player("Yuki"), Player("Yui"), CPU("CPU"), CPU("CPU2"), CPU("CPU3")
            ]
            Game(players_list5, 20)
    
    """
    ゴール値が制約を満たしているかどうか、チェックする
    """
    def test_goal_scale_true(self):
        self.assertGreaterEqual(self.game.goal, 6)
        self.assertLessEqual(self.game.goal, 30)

    """
    ゴール値が制約を満たしていない場合、エラー処理が実行されるかどうかチェックする
    """
    def test_goal_scale_false(self):
        #エラーハンドリング
        #ゴール値が5の場合のチェック
        with self.assertRaises(ValueError):
            Game(self.players_list, 5)
        #エラーハンドリング
        #ゴール値が32の場合のチェック
        with self.assertRaises(ValueError):
            Game(self.players_list, 32)

    """
    positionの初期値が0になっているかどうか、チェックする
    """
    def test_position_integrate(self):
        for player_data in self.game.players:
            self.assertEqual(player_data.get('position'), 0)

    """
    勝者がいない場合、NULLと表示されるかどうか、チェックする
    """
    def test_winner_null(self):
        self.assertIsNone(self.game.winner())
    
    """
    サイコロを振って出た目の数だけ、プレイヤー(CPU)のマスを進められているかどうか、チェックする
    """
    def test_correct_position(self):
         #現在のプレイヤー(orCPU)の情報を取得する
        player = self.game.current_player()
        #コマを進める
        self.game.setPosition(player, 7)
        #適切な数だけコマを進められているかどうか、チェックする
        #0(初期値) + 7 = 0
        self.assertEqual(self.game.players[0].get('position'), 7)

    """
    テキストがプロンプト上に適切な形で表示されているかどうか、チェックする
    プレイヤー用
    """
    def test_output_player(self):
        sys.stdin = io.StringIO('\n') #プロンプト上でエンターを押下する作業を自動化する
        #標準出力系の処理
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        #dice_roll系の処理
        test_dice = Dice()
        player = Player("Test")
        player.dice_roll(self.game, test_dice)
        # キャプチャ出力用
        # 標準出力した内容を取得する
        output = captured_output.getvalue()
        self.assertIn("Testの番です。", output)
        self.assertIn("Testの出た目：", output)
        self.assertIn("サイコロを振るにはエンターキーを押してください。", output)

    """
    テキストがプロンプト上に適切な形で表示されているかどうか、チェックする
    CPU用
    """
    def test_output_cpu(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        test_dice = Dice()
        cpu = CPU("TestCPU")
        cpu.dice_roll(self.game, test_dice)
        output = captured_output.getvalue()
        self.assertIn("CPUの番です。", output)
        self.assertIn("TestCPUの出た目：", output)

    """
    サイコロを振って3の目が出たら、3コマ戻す処理ができているかどうか、チェックする
    """
    def test_minus_dice(self):
        #Gameクラスをnewする
        game = Game(self.players_list, 20)
        #Yukiのpositionの初期値を5とする
        game.players[0]['position'] = 5
        #サイコロの目を振って出た目を3とする
        test_dice = Dice(value=[3])
        #現在のプレイヤー(orCPU)の情報を取得する
        player = game.current_player()
        #dice_rollメソッドを実行する
        player.dice_roll(game, test_dice)
        #初期値からサイコロを振って、出た目の数が引かれているかどうか、チェック(5 - 3 = 2)
        self.assertEqual(game.players[0]['position'], 2)

    """
    ゴール値をはみ出した分、コマを戻す処理ができているかどうか、チェックする
    """
    def test_return_dice(self):
        #Gameクラスをnewする
        game = Game(self.players_list, 20)
        #Yukiのpositionの初期値を19とする
        game.players[0]['position'] = 19
        #サイコロの目を振って出た目を3とする
        test_dice = Dice(value=[4])
        #現在のプレイヤー(orCPU)の情報を取得する
        player = game.current_player()
        #dice_rollメソッドを呼び出し、サイコロを投げる
        player.dice_roll(game, test_dice)
        #ゴール値をはみ出した分、コマを戻す処理ができているかどうか、チェックする
        #19 + 4 = 23
        #23 - 20 = 3
        #20 - 3  = 17
        self.assertEqual(game.players[0]['position'], 17)
    
    """
    サイコロを振って5の目が出た場合、もう一度サイコロを振る処理ができているかどうか、チェックする
    """
    def test_lucky_dice(self):
        #Gameクラスをnewする
        game = Game(self.players_list, 20)
        #Yukiのpositionの初期値を0とする
        game.players[0]['position'] = 0
        #Diceをnewする
        #サイコロの目を振って出た目(1回目):5
        #サイコロの目を振って出た目(2回目):8
        test_dice = Dice(value=[5, 8])
        #現在のプレイヤー(orCPU)の情報を取得する
        player = game.current_player()
        #dice_rollメソッドを呼び出し、サイコロを投げる
        player.dice_roll(game, test_dice)
        #サイコロを振って5の目が出た場合、もう一度サイコロを振る処理ができているかどうか、チェックする
        #5 + 8 = 13
        self.assertEqual(game.players[0]['position'], 13)

if __name__ == '__main__':
    unittest.main()