import tkinter as tk
import Widgets.select as select


#
# GUIの設定
#

root = tk.Tk()
root.title('問題選択')
# root.geometry('800x450')

#
# GUIの末端
#

sf = select.SelectFrame(root)
sf.open_window()
sf.pack()
sf.mainloop()
