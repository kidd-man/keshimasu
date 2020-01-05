import tkinter as tk
import Widgets.play as play
import keshimasu as ksms

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
                 '何処': {'いずこ', 'いずく', 'いづく', 'いずく', 'いどこ'},
                 '地名': {'ちめい'}}

kesimasu1 = ksms.Keshimasu()
kesimasu1.set_question(test1_question)
kesimasu1.set_answers(test1_answers)
kesimasu1.set_theme(test1_theme)


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
f1 = play.PlayFrame(kesimasu1, master=root)
f1.pack()
f1.mainloop()
