import tkinter as tk
import numpy as np
import keshimasu as ksms
import signal
from myerrors import *
from math import ceil

#
# テスト用問題
#

test1_author = "satomi"
test1_tag = "test1"
test1_theme = "読みがひらがな３文字の漢字"
test1_question = [['御', '神', '酒', '洋'],
                  ['渾', '名', '息', '墨'],
                  ['意', '稲', '吹', '何'],
                  ['気', '桜', '荷', '処'],
                  ['地', '深', '合', '扉'],
                  ['大', '人', '傷', '図']]
test1_answers = {'大人': {'おとな'}, '桜': {'さくら'}, '深傷': {'ふかで'},
                 '傷': {'しょう'}, '意気地': {'いくじ', 'いきじ'}, '意': {'こころ'},
                 '地': {'ところ'}, '合図': {'あいず'}, '扉': {'とびら'},
                 '稲荷': {'いなり'}, '息吹': {'いぶき'}, '渾名': {'あだな'},
                 '名': {'みょう'}, '御神酒': {'おみき'}, '洋墨': {'いんく'},
                 '何処': {'いずこ', 'いずく', 'いづく', 'いずく', 'いどこ'}}

kesimasu1 = ksms.Keshimasu()
kesimasu1.set_question(test1_question)
kesimasu1.set_answers(test1_answers)
kesimasu1.set_theme(test1_theme)

TIME_LIMIT = 100  # 制限時間
SIZ = 100  # 1マスの大きさ
HEI = 4    # 画面に表示する高さ

KANA = ['あぁ', 'いぃ', 'うぅ', 'えぇ', 'おぉ',
        'かが', 'きぎ', 'くぐ', 'けげ', 'こご',
        'さざ', 'しじ', 'すず', 'せぜ', 'そぞ',
        'ただ', 'ちぢ', 'つづっ', 'てで', 'とど',
        'な', 'に', 'ぬ', 'ね', 'の',
        'はばぱ', 'ひびぴ', 'ふぶぷ', 'へべぺ', 'ほぼぽ',
        'ま', 'み', 'む', 'め', 'も',
        'やゃ', 'ゆゅ', 'よょ',
        'ら', 'り', 'る', 'れ', 'ろ',
        'わゎ', 'を', 'ん']


#
# 本体画面
#

class MenuFrame(tk.Frame):
    """メニュー画面"""
    pass


class QuestionsFrame(tk.Frame):
    """問題一覧画面"""
    pass


class PlayFrame(tk.Frame):
    """プレイ画面"""
    def __init__(self, keshimasu: ksms.Keshimasu, master=None, width=800, height=550):
        super().__init__(master, width=width, height=height)
        self.playboad = MasusFrame(keshimasu, master=self, width=800, height=900)
        self.keyboad = Keyboad(self, width=600, height=800, submit_func=self.delete_masu)
        self.ksms = keshimasu

        self.play()
        self.playboad.pack()
        self.keyboad.pack()

    def delete_masu(self):
        """正答によりマスを消す"""
        # 選択語
        select = self.playboad.choice_word
        # 入力
        in_ans = self.keyboad.txt.get()
        # 正答か否かのチェック
        if self.ksms.check_answer(select, in_ans):
            print("正解")
            # 入力のクリア
            self.keyboad.txt.set('')
            # 消去処理の呼び出し
            self.playboad.update()

    def play(self):
        # タイマーの設定
        signal.signal(signal.SIGALRM, signal_handler)
        signal.setitimer(signal.ITIMER_REAL, TIME_LIMIT)  # 100秒後に例外を起こす
        # 残り時間
        r_time = TIME_LIMIT
        header = HeaderFrame(r_time, self.ksms, master=self)
        header.pack()
        header.update_timer()
        try:
            self.mainloop()
        except TimeUpException as e:
            print(e)


class HeaderFrame(tk.Frame):
    """制限時間とテーマの表示"""
    def __init__(self, time: int, keshimasu: ksms.Keshimasu, master=None, width=600, height=90):
        super().__init__(master, width=width, height=height)
        # タイマー表示の作成
        self.timer = tk.Canvas(self, width=100, height=90)
        self.timer.create_text(45, 45, font=("Helvetica", 50), text=time, tag='time')
        # 枠
        self.timer.create_rectangle(5, 5, 85, 85)

        # テーマ表示の作成
        self.theme = tk.Label(self, text=keshimasu.theme, font=('fammily', 30))
        self.timer.pack(side='left')
        self.theme.pack(side='left')

    def update_timer(self):
        """残り時間の更新"""
        self.timer.delete('time')
        r_time = ceil(signal.getitimer(signal.ITIMER_REAL)[0])
        self.timer.create_text(45, 45, font=("Helvetica", 50), text=r_time, tag='time')
        self.after(100, self.update_timer)


class MasusFrame(tk.Frame):
    """マスの配置画面"""
    def __init__(self, keshimasu: ksms.Keshimasu, master=None, width=800, height=800):
        super().__init__(master, width=width, height=height)

        # 問題
        self.ksms = keshimasu
        self.q = self.ksms.playing_table

        # マスを描画するオブジェクトのリスト
        self.masu_list = []

        # 盤面の大きさを取得する
        self.row = self.ksms.shape[0]
        self.clm = self.ksms.shape[1]

        # 各マスのスイッチ状態を保持する行列
        self.switches = np.zeros((self.row, self.clm), dtype=bool)

        # スイッチ状態から選択語を生成
        self.choice_word = ''

        # 盤面の大きさに応じた大きさのキャンバスを作成
        self.cvs = tk.Canvas(self, width=SIZ*self.clm+SIZ, height=SIZ*HEI, bg='gray')

        # 画面表示・配置
        self.display(isclear=True)

        # クリックイベントを設定
        self.cvs.bind("<Button-1>", self.click)

    def display(self, isclear=False):
        if isclear:
            # キャンバスのクリア
            self.cvs.delete('text')
            self.cvs.delete('frame')

            for m in self.masu_list:
                m.delete()
            self.masu_list = []
            # 各マスのオブジェクト列を生成
            for i in range(self.row):
                for j in range(self.clm):
                    self.masu_list.append(
                        Masu(self.cvs, x=100 * j, y=100 * (i - self.row + HEI), size=100, text=self.q[i][j]))

        # 配置
        self.cvs.pack()

    def click(self, event):
        """クリック時のマス選択をマスの背景色を変えることで表現する"""
        # マスの左上からの座標
        x = event.x-SIZ//2
        y = event.y

        if 0 < x < SIZ*self.clm:
            # いずれかのマスをクリックしている場合
            # クリックされたマスを特定
            c_row = y // SIZ + self.row - HEI
            c_clm = x // SIZ

            # クリックされたマスがスイッチ可能マスかどうかを
            # その時のスイッチ数に応じて調べる
            swi_num = np.count_nonzero(self.switches)
            switchable = False
            if swi_num == 0:
                # 0スイッチの場合->無条件
                switchable = True
            elif swi_num == 1:
                # 1スイッチの場合->そのマスor隣接マスのみ可能
                on_x = int(np.where(self.switches)[0])
                on_y = int(np.where(self.switches)[1])

                # ユークリッド距離が1.0以下かどうかで判定
                if np.linalg.norm(np.array([c_row, c_clm])-np.array([on_x, on_y])) <= 1.0:
                    switchable = True

            else:
                # 2スイッチ以上の場合->
                #   1: 該当マスのうち上下のxor or 左右のxorがTrue(端マス)
                #   2: 同行同列の隣接マス
                #   のみ可能

                # onのマスのリストからswitch可能なマスを生成する
                ons = np.where(self.switches)
                switchable_set = set()

                if max(ons[0]) - min(ons[0]) > 0:
                    # 縦に連続している場合
                    column = max(ons[1])
                    # 両端とその両隣がスイッチ可能
                    switchable_set.add((max(ons[0]), column))
                    switchable_set.add((max(ons[0]+1), column))
                    switchable_set.add((min(ons[0]), column))
                    switchable_set.add((min(ons[0]-1), column))
                else:
                    # 横に連続している場合
                    row = max(ons[0])
                    # 両端とその両隣がスイッチ可能
                    switchable_set.add((row, max(ons[1])))
                    switchable_set.add((row, max(ons[1]) + 1))
                    switchable_set.add((row, min(ons[1])))
                    switchable_set.add((row, min(ons[1]) - 1))

                # 以上のパターンに当てはまればスイッチ可にする
                if (c_row, c_clm) in switchable_set:
                    switchable = True

            if switchable:
                # スイッチ
                self.masu_list[c_row*self.clm+c_clm].switch()

                # スイッチ行列の対応する要素を同様に書き換え
                self.switches[c_row][c_clm] = not self.switches[c_row][c_clm]

                # スイッチ行列に応じて選択語を生成
                choice_idx = np.where(self.switches)
                self.choice_word = self.q[choice_idx].astype(object).sum()

    def update(self):
        """正答によるマスの削除と盤面の更新"""
        # ドロップアニメーションの描画

        # 選択番号を内部的削除・盤面更新処理
        self.ksms.delete_word(np.where(self.switches))
        self.switches = np.zeros((self.row, self.clm), dtype=bool)
        self.display(isclear=True)


class Masu:
    """1マスの表現"""
    def __init__(self, master, x=0, y=0, size=SIZ, text=u'　'):
        self.master = master
        self.x = x
        self.y = y

        # 枠線
        self.frame_id = self.master.create_rectangle(x+SIZ//2, y, x+size+SIZ//2, y+size, fill='white')
        # 文字
        self.text_id = self.master.create_text(x+size//2+SIZ//2, y+size//2, text=text, font=('family', size), tag='text')

        self.size = size
        self.choiced = False  # 選択されているか否か
        self.row = -1
        self.column = -1

    def drop(self, n):
        pass

    def switch(self):
        """選択状態を切り替える"""
        # 選択状態を反転
        self.choiced = not self.choiced
        # 今ある枠を消去
        self.master.delete(self.frame_id)

        # 選択状態に応じて枠を新たに描画
        if self.choiced:
            self.draw_frame('yellow')
        else:
            self.draw_frame('white')

        # 文字を上部に移動
        self.master.lift(self.text_id)

    # 枠の描画
    def draw_frame(self, color):
        self.frame_id = self.master.create_rectangle(self.x + SIZ // 2, self.y,
                                                     self.x + self.size + SIZ // 2, self.y + self.size,
                                                     fill=color, tag='frame')

    # マスの削除
    def delete(self):
        """正答によるマスの削除処理"""
        self.master.delete(self.frame_id)
        self.master.delete(self.text_id)


class Keyboad(tk.Frame):
    """回答に用いるキーボード"""
    def __init__(self, master=None, width=600, height=400, submit_func=None):
        #
        # ウィジェット定義
        #

        # 親の初期化処理
        super().__init__(master, width=width, height=height)
        # 入力表示
        self.txt = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.txt, font=('family', 30), bg='gray', width=12)
        # 五十音ボタン
        self.buttons = [tk.Button(self, text=e[0], font=('fammily', 15), command=self.push_kana(e[0]), width=3)
                        for e in KANA]
        # 変換ボタン
        self.hb = tk.Button(self, text='変換', width=10, command=self.henkan)
        # 1文字クリアボタン
        self.cb = tk.Button(self, text='1字消去', width=10, command=self.clear_char)
        # 提出ボタン
        self.sb = tk.Button(self, text='決定', width=20, command=submit_func)

        #
        # ウィジェットの配置
        #

        self.label.grid(row=0, column=0, columnspan=10)

        for i, b in enumerate(self.buttons):
            if i < 35:
                # ま行までの配置
                b.grid(row=i%5+1, column=9-i//5)
            elif i < 38:
                # や行の配置
                b.grid(row=(2*i)%5+1, column=2)
            else:
                # ら行以降の配置
                b.grid(row=(i+2)%5+1, column=9-(i+2)//5)

        self.hb.grid(row=6, column=1, columnspan=2)
        self.cb.grid(row=6, column=7, columnspan=2)
        self.sb.grid(row=6, column=3, columnspan=4)

    def clear_label(self):
        self.txt.set('')

    def clear_char(self):
        """末尾の1文字を消す"""
        if self.txt.get() != '':
            self.txt.set(self.txt.get()[:-1])

    def push_kana(self, kana):
        """かな入力 commandに引数付きで渡すために関数をネスト"""
        def x():
            if len(self.txt.get()) < 8:
                self.txt.set(self.txt.get()+kana)
        return x

    def henkan(self):
        """変換ボタン 拗音化・濁音半濁音への変換"""
        if self.txt.get() != '':
            # 末尾の文字を取得
            last_kana = self.txt.get()[-1]
            # 末尾までの文字の取得
            b_last_kanas = self.txt.get()[:-1]
            for i in KANA:
                # 50音表から入力文字を検索し変換したものに末尾を置き換える
                if last_kana in i:
                    new_txt = b_last_kanas+i[(i.find(last_kana)+1)%len(i)]
                    self.txt.set(new_txt)


#
# GUIの設定
#

root = tk.Tk()
root.title(u"けしマス")
# root.geometry('800x450')

#
# GUIの末端
#

# f1 = PlayFrame(root)
f1 = PlayFrame(kesimasu1, master=root)
f1.pack()
f1.mainloop()