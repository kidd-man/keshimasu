import numpy as np
import pickle
from myerrors import *


class KeshimasuError(Exception):
    """Keshimasuに関して起こる例外"""
    pass


class Keshimasu:
    """ひとつの問題に対応するクラス"""
    def __init__(self, ques: np.array, ans, author: str, tag: str,
                 theme='かな３文字で漢字を読め', lang='hiragana', height=4, time=100):
        self.question_table = ques  # 盤面
        self.playing_table = ques   # 動かす用の盤面
        self.shape = ques.shape     # 消しマスの大きさ
        self.answer_set = ans       # 答えの集合
        self.author = author        # 作者
        self.tag = tag              # 問題につけるタグ
        self.theme = theme          # 問題のテーマ
        self.keybord = lang         # 入力キーボードの言語
        self.hei = height           # 表示盤面の高さ
        self.time = time            # 制限時間

    '''
    def set_question(self, arr: np.array):
        self.question_table = arr
        self.playing_table = arr
        self.shape = self.question_table.shape

    def set_answers(self, answers: dict):
        self.answer_set = answers

    def set_author(self, ):
        pass

    def set_tag(self):
        pass

    def set_theme(self, theme: str):
        self.theme = theme
    '''

    def construct_word(self, idxs: np.array):
        """indexから, playing_table を参照して熟語を構成する"""
        return self.playing_table[idxs].astype(object).sum()

    def delete_word(self, choice: np.array):
        """マスを消したときの盤面更新処理 引数は(array([x座標列]),array([y座標列]))"""
        # choice を盤面の座標に変換
        # coordinates = list(map(lambda x: self.choice_to_coordinate(x), choice))
        row_idxs = choice[0]
        clm_idxs = choice[1]

        # 縦か横かの二通りに分ける
        if row_idxs[0] == row_idxs[-1]:
            # 横のとき
            # 順に見ていき, 各マスを潰して上のマスを1つ下ろしてくる
            for row, clm in zip(row_idxs, clm_idxs):
                # 0 <= i <= ey に対応するマスを1個ずつ順に下ろしていく. 真上から順に見ていくのでreverse.
                for r in reversed(range(0, row+1)):
                    if r > 0:
                        # 上の文字をコピーしてくる
                        self.playing_table[r][clm] = self.playing_table[r-1][clm]
                    else:
                        # 上のマスが天井のときは空白にする
                        self.playing_table[r][clm] = '　'  # 全角スペース

        else:
            # 縦のとき(1マスを含む)
            # choiceの最後だけを見て, coordinatesの要素数だけの数上のマスを潰し同じだけ下ろしてくる
            row = choice[0][-1]
            clm = choice[1][0]
            n = len(choice[0])
            # 0 <= i <= ey に対応するマスをn個ずつ順に下ろしていく. 真上から順に見ていくのでreverse.
            for r in reversed(range(0, row+1)):
                if r - n >= 0:
                    # n個上の文字をコピーしてくる
                    self.playing_table[r][clm] = self.playing_table[r-n][clm]
                else:
                    # n個上がないときは空白にする
                    self.playing_table[r][clm] = '　'  # 全角スペース

    def choice_to_coordinate(self, num):
        """ユーザーが指定する数字を引数に取り,
           盤面行列を扱う際の座標への変換を行う"""
        return num // self.shape[1] + self.shape[0] - self.hei, num % self.shape[1]

    def check_answer(self, choice, in_ans: str):
        """選択したマスに対する入力が正解リストに含まれるかチェックし真偽値を返す.
           choice は入力数値配列でもそれに対応する熟語文字列でも良い."""
        try:
            if type(choice) is list:
                choice_word = self.construct_word(choice)
            elif type(choice) is str:
                choice_word = choice
            else:
                # choicedに予期しない型の変数を入れている例外処理
                raise TypeError
            # 選択ワードが正解リストに存在し, かつ入力がその正解集合に含まれる場合のみTrue それ以外はFalse
            if (choice_word in self.answer_set) and (in_ans in self.answer_set[choice_word]):
                return True
            else:
                return False
        except TypeError:
            pass

    def save(self, overwrite=False):
        """消しマスの問題(このクラスのオブジェクト)を外部ファイルに保存する.
           overwriteがFalseのとき,
           同じ(author, tag)の問題がすでに存在している場合は警告し、保存しない."""
        try:
            try:
                # binファイルの読み込み
                with open('questions_data.bin', 'rb') as f:
                    keshimasus = pickle.load(f)
            except FileNotFoundError:
                # ファイルが見つからなければ新規作成
                keshimasus = []

            # 問題集内の問題の(author, tag)のリスト
            author_tags = [(k.author, k.tag) for k in keshimasus]

            # すでに同じ(author, tag)で登録されたものがないか確認
            if (self.author, self.tag) in author_tags:
                # 同じものがある場合
                if overwrite:
                    # 上書き保存がTrueなら削除
                    del keshimasus[author_tags.index((self.author, self.tag))]

                else:
                    # 上書き保存がTrueなら重複不可なのでエラー
                    raise SaveDuplicationError\
                    (f'author: {self.author}, tag: {self.tag} の問題はすでに登録されています.')

            # 問題リストへこのインスタンスを追加
            keshimasus.append(self)

            # binファイルへの書き込み
            with open('questions_data.bin', 'wb') as f:
                pickle.dump(keshimasus, f)

        except FileNotFoundError as e:
            print(e)
        except SaveDuplicationError as e:
            print(e)

    def display(self, number_is=False):
        """コマンドラインにプレイングテーブルを表示する.
           ただし縦は下からHEI行までしか表示しない."""
        # number_format は '{0} {1} {2} {3}' のような文字列
        # マスを指定する際の数字を表示するために用いる
        number_format = ' '.join(list(map(lambda x: '{0[' + str(x) + ']:>2}', list(range(self.shape[1])))))

        print("---"*self.shape[1]*2)  # 罫線

        # 問題の描画
        for i, e in enumerate(self.playing_table[-self.hei:]):
            print(*e, end='')

            # 番号対応表の描画
            if number_is:
                print('  ', number_format.format(range(i*self.shape[1], (i+1)*self.shape[1])))
            else:
                print()

        print("---"*self.shape[1]*2)  # 罫線
