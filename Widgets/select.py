import tkinter as tk
import pickle as pk
import numpy as np
import keshimasu as ksms

HEI = 4


class QList(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, width=500, height=200)

        # 問題集の読み込み
        with open('../questions_data.bin', 'rb') as f:
            questions = pk.load(f)

        brd_list = []  # 盤面形表示のリスト
        frm_list = []  # 枠のリスト
        thm_list = []  # テーマのリスト
        aut_list = []  # 作者のリスト
        tag_list = []  # 問題タグのリスト

        # スクロールバー用のキャンバス
        cvs = tk.Canvas(self)

        # スクロールバーの作成と配置
        bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        bar.config(command=cvs.yview)

        cvs.config(yscrollcommand=bar.set)
        cvs.config(scrollregion=(0, 0, 500, 500))
        cvs.pack()

        # 問題ごとに見出しを作成
        for i, q in enumerate(questions):
            # 盤面の形
            shape = np.array(q['question']).shape

            # テーブルをテキスト化
            tbl_txt = '\n'.join([' '.join(i) for i in [['□']*shape[1]]*(shape[0]-HEI) + [['■']*shape[1]]*HEI])
            frm_list.append(tk.LabelFrame(cvs))
            brd_list.append(tk.Label(frm_list[i], text=tbl_txt))
            thm_list.append(tk.Label(frm_list[i], text="テーマ: " + q['theme']))
            aut_list.append(tk.Label(frm_list[i], text="作者: " + q['author']))
            tag_list.append(tk.Label(frm_list[i], text="問題タグ: " + q['tag']))

            # 配置
            frm_list[i].propagate(False)  # 自動サイズ変更を無効
            frm_list[i].grid(row=i, column=0)
            brd_list[i].grid(row=0, column=0, rowspan=3)
            thm_list[i].grid(row=0, column=1, sticky=tk.W)
            aut_list[i].grid(row=1, column=1, sticky=tk.W)
            tag_list[i].grid(row=2, column=1, sticky=tk.W)


root = tk.Tk()
root.geometry('400x200')
f = QList(master=root)
# root.pack()
root.mainloop()
