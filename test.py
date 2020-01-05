import tkinter as tk
import numpy as np


if __name__ == '__main__':
    root = tk.Tk()
    f = tk.Frame(root)

    cvs = tk.Canvas(f, width=400, height=400, scrollregion=(0, 0, 800, 800))
    bar = tk.Scrollbar(f, orient=tk.VERTICAL, command=cvs.yview)
    bar.grid(row=0, column=1, sticky=tk.N+tk.S)
    cvs.config(yscrollcommand=bar.set)
    cvs.create_text(50, 50, text="hoge")
    cvs.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W+tk.S)

    cvs.bind("<ButtonPress-1>", lambda e: cvs.scan_mark(e.x, e.y))
    cvs.bind("<B1-Motion>", lambda e: cvs.scan_dragto(e.x, e.y, gain=1))

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
