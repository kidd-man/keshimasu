import tkinter as tk
import pickle as pk
import Widgets.play as play


class SelectFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 問題ファイルの読み込み
        with open('questions_data.bin', 'rb') as f:
            self.k_list = pk.load(f)

    def open_window(self):
        # 問題選択用テーブルの作成
        table = [['盤面形', 'テーマ', '作者', '問題タグ']]

        for k in self.k_list:
            table.append([f'{k.shape[0]}x{k.shape[1]}', k.theme, k.author, k.tag])

        # 選択用リストの作成
        for row_idx, row_dat in enumerate(table):
            for col_idx, col_dat in enumerate(row_dat):
                if row_idx == 0:
                    bg_color = '#ccc'
                else:
                    bg_color = '#fff'

                lbl = tk.Label(self, bg=bg_color, borderwidth=1, relief=tk.RAISED, text=col_dat)
                lbl.grid(row=row_idx, column=col_idx, sticky=tk.N + tk.E + tk.S + tk.W)

            # 選択ボタンを配置
            if row_idx > 0:
                keshimasu = self.k_list[row_idx-1]
                btn = tk.Button(self, text='try', command=self.open_play_window(keshimasu))
                btn.grid(row=row_idx, column=4)

    def open_play_window(self, keshimasu):
        def x():
            """問題選択ウインドウを閉じてプレイ画面を開く"""
            # 選択ウインドウの削除
            self.master.destroy()

            playroot = tk.Tk()
            playroot.title('消しマス')
            pf = play.PlayFrame(keshimasu, master=playroot)
            pf.pack()
            pf.mainloop()
        return x
