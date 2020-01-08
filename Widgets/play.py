import tkinter as tk
from tkinter import messagebox
import numpy as np
import threading as th
import keshimasu as ksms
from myerrors import *

#######
# 定数 #
#######

# TIME_LIMIT = 200  # 制限時間
B_WID = 400  # ボードの横の大きさ
# SIZ = 100  # 1マスの大きさ
UPPER_HEI = B_WID//10  # 残りマスの表示の高さ
SIDE_WID = B_WID//40  # 盤面横の幅
TXT_MAX = 12  # 入力文字数上限
FRM_WID = 5  # 枠の太さ

#
# キーボード用のアルファベットリスト
#

HIRAGANA = [['あぁ', 'いぃ', 'うぅ', 'えぇ', 'おぉ'],
            ['かが', 'きぎ', 'くぐ', 'けげ', 'こご'],
            ['さざ', 'しじ', 'すず', 'せぜ', 'そぞ'],
            ['ただ', 'ちぢ', 'つづっ', 'てで', 'とど'],
            ['な', 'に', 'ぬ', 'ね', 'の'],
            ['はばぱ', 'ひびぴ', 'ふぶぷ', 'へべぺ', 'ほぼぽ'],
            ['ま', 'み', 'む', 'め', 'も'],
            ['やゃ', 'ゆゅ', 'よょ'],
            ['ら', 'り', 'る', 'れ', 'ろ'],
            ['わゎ', 'を', 'ん', 'ー']]

KATAKANA = [['アァ', 'イィ', 'ウゥ', 'エェ', 'オォ'],
            ['カガ', 'キギ', 'クグ', 'ケゲ', 'コゴ'],
            ['サザ', 'シジ', 'スズ', 'セゼ', 'ソゾ'],
            ['タダ', 'チヂ', 'ツヅッ', 'テデ', 'トド'],
            ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'],
            ['ハバパ', 'ヒビピ', 'フブプ', 'ヘベペ', 'ホボポ'],
            ['マ', 'ミ', 'ム', 'メ', 'モ'],
            ['ヤャ', 'ユュ', 'ヨョ'],
            ['ラ', 'リ', 'ル', 'レ', 'ロ'],
            ['ワヮ', 'ヲ', 'ン', 'ー']]

ALPHABET = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]


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
        # 各初期化
        self.master = master
        self.remain_time = keshimasu.time
        self.message = None
        self.clear_flag = False
        size = B_WID // keshimasu.shape[1]  # 1マスの大きさ
        disp_hei = keshimasu.hei  # 表示する高さ

        #
        # ウィジェットの作成
        #

        self.ksms = keshimasu
        self.header = HeaderFrame(self.remain_time, self.ksms, master=self)
        self.playboad = MasusFrame(self, keshimasu, size)
        self.keyboad = Keyboad(self, lang=self.ksms.keybord, width=600, height=800, submit_func=self.update_playboad)

        #
        # ゲーム開始を確認するメッセージボックスを表示する
        #

        # メインウインドウを非表示
        master.withdraw()
        # メッセージボックスに表示するようの盤面
        bord = '\n'.join([' '.join(row) for row in self.ksms.playing_table[-disp_hei:]])
        # メッセージボックスの表示
        messagebox.showinfo(title=self.ksms.theme, message=bord)
        # メインウインドウの表示
        master.deiconify()

        #
        # ウィジェットの配置
        #

        self.header.pack()
        self.playboad.pack()
        self.keyboad.pack()

        # 別スレッドにてタイマーのスタート
        self.th = th.Thread(target=self.timer_start)
        self.th.start()

    def timer_start(self):
        try:
            """タイマーの起動"""
            if self.remain_time <= 0:
                # 時間切れの場合
                # 描画
                self.header.update_timer(self.remain_time)
                # 例外発生
                raise TimeUpException
            else:
                # 時間が残っている場合
                # 描画
                self.header.update_timer(self.remain_time)
                # 時間の更新
                self.remain_time -= 1
                if self.clear_flag:
                    # クリア処理
                    pass
                else:
                    # 1s後に次のループへ
                    self.after(1000, self.timer_start)
        except TimeUpException:
            # タイムアップ時の処理
            # メッセージボックスの表示
            messagebox.showinfo(title="タイムアップ！", message="残念ながら時間切れです。")

    def update_playboad(self):
        """正答によりマスを消す描画"""
        # 選択語
        select = self.playboad.choice_word
        # 入力
        in_ans = self.keyboad.txt.get()
        # 正答か否かのチェック
        if self.ksms.check_answer(select, in_ans):
            # 入力のクリア
            self.keyboad.txt.set('')
            # 消去処理の呼び出し
            self.playboad.update()

        # 全消しのチェック
        if not np.any(np.array(self.playboad.masu_list).astype(bool)):
            # タイマーの停止
            self.clear_flag = True
            # メッセージボックスの表示
            messagebox.showinfo(title="Congratulations！", message="クリア！")
            # ウインドウの削除
            self.master.destroy()

    def timeup_window(self):
        """タイムアップを知らせるメッセージ"""
        # メッセージボックスの表示
        messagebox.showinfo(title="タイムアップ！", message="残念ながら時間切れです。")


class HeaderFrame(tk.Frame):
    """制限時間とテーマの表示"""
    def __init__(self, time: int, keshimasu: ksms.Keshimasu,
                 master, width=B_WID+2*SIDE_WID, height=90):
        super().__init__(master, width=width, height=height)
        # タイマー表示の作成
        self.timer = tk.Canvas(self, width=120, height=100)
        self.timer.create_text(55, 50, font=("Helvetica", 50), text=time, tag='time')
        # 枠
        self.timer.create_rectangle(5, 5, 105, 95)

        # テーマ表示の作成
        self.theme = tk.Label(self, text=keshimasu.theme, font=('fammily', 30))
        self.timer.pack(side='left')
        self.theme.pack(side='left')

    def update_timer(self, time):
        """残り時間の更新"""
        self.timer.delete('time')
        self.timer.create_text(55, 50, font=("Helvetica", 50), text=time, tag='time')


class MasusFrame(tk.Frame):
    """マスの配置画面"""
    def __init__(self, master, keshimasu: ksms.Keshimasu, size):
        # 問題
        self.ksms = keshimasu
        self.q = self.ksms.playing_table

        # マスを描画するオブジェクトのリスト
        self.masu_list = []

        # 盤面の大きさを取得する
        self.row = self.ksms.shape[0]  # 盤面の縦マス数
        self.clm = self.ksms.shape[1]  # 盤面の横マス数
        self.hei = self.ksms.hei       # 表示する高さ(マス数)
        self.size = size               # 1マスの1辺の長さ

        # マスの大きさと周辺枠の太さからフレームの大きさを決定
        width = self.size*self.clm + SIDE_WID*2
        height = self.size*self.hei + UPPER_HEI

        # 親クラスの初期化
        super().__init__(master, width=width, height=height)

        # 残りマス数表示のフォントサイズ
        self.remain_size = int(20*self.size//100)

        # 各マスのスイッチ状態を保持する行列
        self.switches = np.zeros((self.row, self.clm), dtype=bool)

        # スイッチ状態から選択語を生成
        self.choice_word = ''

        # 盤面の大きさに応じた大きさのキャンバスを作成
        self.cvs = tk.Canvas(self,
                             width=width,
                             height=height,
                             bg='white')

        # 画面表示・配置
        self.display(isclear=True)

        # クリックイベントを設定
        self.cvs.bind("<Button-1>", self.click)

    def display(self, isclear=False):
        if isclear:
            # キャンバスのクリア
            self.cvs.delete('text')
            self.cvs.delete('frame')
            self.cvs.delete('remain')

            # 前のマスの初期化
            for m in self.masu_list:
                if m is not None:
                    m.delete()
            self.masu_list = []
            # 各マスのオブジェクト列を生成
            for i in range(self.row-self.hei, self.row):
                for j in range(self.clm):
                    if self.q[i][j] != '　':  # 空白かいなか
                        self.masu_list.append(Masu(self.cvs,
                                                   x=self.size*j,
                                                   y=self.size*(i - self.row + self.hei)+UPPER_HEI,
                                                   size=self.size,
                                                   text=self.q[i][j]))
                    else:
                        self.masu_list.append(None)

        for column in range(self.clm):
            # 残りマス数の計算
            remain = max(np.sum(self.q[:, column] != '　') - self.hei, 0)

            # 残りマス表示の描画
            self.cvs.create_text(self.size*column + self.size // 2 + SIDE_WID,
                                 UPPER_HEI // 2,
                                 text="あと " + str(remain) + " マス",
                                 font=('fammily', self.remain_size), tag='remain')

        # 配置
        self.cvs.pack()

    def click(self, event):
        """クリック時のマス選択をマスの背景色を変えることで表現する"""
        # マスの左上からの座標
        x = event.x-SIDE_WID
        y = event.y-UPPER_HEI

        if 0 < x < self.size*self.clm and 0 < y < self.size*self.hei:
            # 有効エリアをクリックしてる場合
            if self.masu_list[y//self.size*self.clm + x//self.size] is not None:
                # なおかついずれかのマスをクリックしている場合
                # クリックされたマスを特定
                c_row = y // self.size + self.row - self.hei
                c_clm = x // self.size
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
                    self.masu_list[y//self.size*self.clm+c_clm].switch()

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
    def __init__(self, master, x, y, size, text=u'　'):
        self.master = master
        self.x = x
        self.y = y

        # 枠線
        self.frame_id = self.master.create_rectangle(x+SIDE_WID, y,
                                                     x+SIDE_WID+size, y+size,
                                                     width=5)
        # 文字
        self.text_id = self.master.create_text(x+size//2+SIDE_WID,
                                               y+size//2,
                                               text=text,
                                               font=('family', size*3//4),
                                               tag='text')

        self.size = size
        self.chosen = False  # 選択されているか否か
        self.row = -1
        self.column = -1

    def drop(self, n):
        pass

    def switch(self):
        """選択状態を切り替える"""
        # 選択状態を反転
        self.chosen = not self.chosen
        # 今ある枠を消去
        self.master.delete(self.frame_id)

        # 選択状態に応じて枠を新たに描画
        if self.chosen:
            self.draw_frame('yellow')
        else:
            self.draw_frame('white')

        # 文字を上部に移動
        self.master.lift(self.text_id)

    # 枠の描画
    def draw_frame(self, color):
        self.frame_id = self.master.create_rectangle(self.x + SIDE_WID, self.y,
                                                     self.x + SIDE_WID + self.size, self.y + self.size,
                                                     width=FRM_WID,
                                                     fill=color,
                                                     tag='frame')

    # マスの削除
    def delete(self):
        """正答によるマスの削除処理"""
        self.master.delete(self.frame_id)
        self.master.delete(self.text_id)


class Keyboad(tk.Frame):
    """回答に用いるキーボード langでひらがな・カタカナ・アルファベットを指定"""
    def __init__(self, master=None, lang='hiragana', width=600, height=400, submit_func=None):
        #
        # ウィジェット定義
        #

        # 親の初期化処理
        super().__init__(master, width=width, height=height)

        # 入力表示
        self.txt = tk.StringVar()
        labelframe = tk.LabelFrame(self)
        self.label = tk.Label(labelframe, width=int(TXT_MAX*1.5), textvariable=self.txt, font=('family', 30))
        # 変換処理用の内部保持入力文字リスト
        self.inputted = []
        # ひらがな・カタカナ・アルファベットのどれか
        self.lang = 'hiragana'

        # アルファベット入力ボタンの作成
        if lang == 'hiragana':
            # ひらがな
            alph = HIRAGANA
        elif lang == 'katakana':
            # カタカナ
            alph = KATAKANA
        else:
            # アルファベット
            alph = ALPHABET

        # アルファベットボタンの作成
        # [[あ, い, ...], ...] -> [[ボタン(あ), ボタン(い), ...], ...]
        self.buttons = [[tk.Button(self, text=e[0], font=('fammily', 15), command=self.push_kana(e), width=3)
                        for e in line] for line in alph]

        # 変換ボタン
        hb = tk.Button(self, text='変換', command=self.henkan)
        # 1文字クリアボタン
        cb = tk.Button(self, text='1字消去', command=self.clear_char)
        # 提出ボタン
        sb = tk.Button(self, text='決定', command=submit_func)

        #
        # ウィジェットの配置
        #

        if lang == 'hiragana' or lang == 'katakana':
            # ひらがな・カタカナの場合
            for col_idx, line in enumerate(self.buttons):
                for row_idx, b in enumerate(line):
                    if col_idx != 7:
                        # や行以外の配置
                        b.grid(row=row_idx+1, column=9-col_idx, sticky=tk.N + tk.E + tk.S + tk.W)
                    else:
                        # や行の配置
                        b.grid(row=row_idx*2+1, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        else:
            # アルファベットの場合
            for row_idx, line in enumerate(self.buttons):
                for col_idx, b in enumerate(line):
                    b.grid(row=row_idx+1, column=col_idx, sticky=tk.N + tk.E + tk.S + tk.W)

        # 入力表示ラベルと枠の配置
        labelframe.grid(row=0, column=0, columnspan=10)
        self.label.pack()

        # 変換・1字クリア・提出ボタンの配置
        hb.grid(row=6, column=1, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        cb.grid(row=6, column=7, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        sb.grid(row=6, column=3, columnspan=4, sticky=tk.N + tk.E + tk.S + tk.W)

    def clear_label(self):
        """全消し"""
        self.txt.set('')
        self.inputted = []

    def clear_char(self):
        """末尾の1文字を消す"""
        if self.txt.get() != '':
            self.txt.set(self.txt.get()[:-1])
            del self.inputted[-1]

    def push_kana(self, kana_set):
        """かな入力 commandに引数付きで渡すために関数をネスト"""
        def x():
            if len(self.txt.get()) < TXT_MAX:
                self.txt.set(self.txt.get() + kana_set[0])
                self.inputted.append(kana_set)
        return x

    def henkan(self):
        """変換ボタン 拗音化・濁音半濁音への変換"""
        if self.txt.get() != '':
            # 末尾の文字を取得
            last_c = self.txt.get()[-1]

            # 末尾の文字の, 変換を含めたセット(String列)
            last_set = self.inputted[-1]

            # 末尾の文字の変換後の文字
            next_c = last_set[(last_set.index(last_c)+1) % len(last_set)]

            # 末尾までの文字の取得
            before_last = self.txt.get()[:-1]

            # 入力文字を検索し変換次の文字に変換したものに末尾を置き換える
            self.txt.set(before_last + next_c)
