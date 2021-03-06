import numpy as np
import signal
import pickle
from math import floor
from myerrors import *

"""
----update-----
> 'あとnマス'の表示
> マス指定を2整数(1文字は1整数)で入力できるように変更する
"""


#
# ファイル操作
#

def question_list():
    """保存されている問題の(author, tag)一覧"""

    # binファイルの読み込み
    with open('questions_data.bin', 'rb') as f:
        keshimasu_list = pickle.load(f)

    # 表示を揃えるために文字列の最大長を調べる
    max_author_len = 0
    max_tag_len = 0
    for k in keshimasu_list:
        max_author_len = max(max_author_len, len(k.author))
        max_tag_len = max(max_tag_len, len(k.tag))

    # 一覧表示
    print('author'.center(max_author_len), 'tag'.center(max_tag_len))
    print(''.rjust(max_author_len, '-'), ''.rjust(max_tag_len, '-'))
    for k in keshimasu_list:
        print(k.author.rjust(max_author_len), k.tag.rjust(max_tag_len))
    print()  # 改行

'''
def resister_question(keshimasu: ksms.Keshimasu):
    """新しい消しマス問題を問題集ファイルへ登録"""

    author = keshimasu.author
    tag = keshimasu.tag
    theme = keshimasu.theme
    question = keshimasu.question_table
    answer = keshimasu.answer_set

    try:
        # binファイルの読み込み
        with open('questions_data.bin', 'rb') as f:
            questions = pickle.load(f)
    except FileNotFoundError:
        # 初回は初期化
            questions = []

    # すでに同じ(author, tag)で登録されたものがなければ追加する.
    author_tags = [(q['author'], q['tag']) for q in questions]
    if (author, tag) in author_tags:
        print(f'author: {author}, tag: {tag} の問題はすでに登録されています.')
    else:
        questions.append({'author': author,
                          'tag': tag,
                          'theme': theme,
                          'question': question,
                          'answer': answer})

        # binファイルへの書き込み
        with open('questions_data.bin', 'wb') as f:
            pickle.dump(questions, f)
'''

'''
def update_question(keshimasu: ksms.Keshimasu):
    """すでに登録されている同じ(author, tag)の問題を登録し直す"""
    author = keshimasu.author
    tag = keshimasu.tag
    theme = keshimasu.theme
    question = keshimasu.question_table
    answer = keshimasu.answer_set

    try:
        # binファイルの読み込み
        with open('questions_data.bin', 'rb') as f:
            keshimasu_list = pickle.load(f)

        # 問題集の(作者, タグ)リスト
        author_tags = [(q['author'], q['tag']) for q in keshimasu_list]

        # 同じ(author, tag)の問題を探す
        if (author, tag) in author_tags:
            # 対応する問題辞書を書き換え
            idx = author_tags.index((author, tag))
            questions[idx]['theme'] = theme
            questions[idx]['question'] = question
            questions[idx]['answer'] = answer
        else:
            # 同じ(author, tag)の問題が見つからない場合
            print(f"{author} {tag} の問題が見つかりません")

    except FileNotFoundError:
        print("questions_data.bin が開けません.")
'''


def play():
    """消しマスをコマンドライン上でプレイ"""
    print("問題のリストを表示します.")
    question_list()

    while True:
        try:
            inputs = tuple(input("作者とタグを入力し問題を選択してください. >>\n").split(' '))

            # 書式は "作者名 問題タグ"
            if len(inputs) != 2:
                raise InputError("不適切な入力です. '[作者] [タグ]'の形式で入力してください.")

            # ファイルを開く
            with open('questions_data.bin', 'rb') as f:
                keshimasu_list = pickle.load(f)

            # 問題集の(作者, タグ)リスト
            author_tags = [(k.author, k.tag) for k in keshimasu_list]

            if inputs in author_tags:
                # 該当問題がリストにある場合 -> 該当問題が何問目かを検索し取得
                idx = author_tags.index(inputs)
                keshimasu = keshimasu_list[idx]
                print("問題を読み込みました.")
                break
            else:
                print("該当する問題が見つかりませんでした.")
        except InputError as e:
            print(e)

    ################
    # ゲーム開始準備 #
    ################

    #
    # よく使う変数のリネーム
    #

    hei = keshimasu.hei        # 盤面を表示する高さ
    tate = keshimasu.shape[0]  # 盤面の縦の長さ
    yoko = keshimasu.shape[1]  # 盤面の横の長さ

    #
    # コマンドライン表示
    #

    print("お題: " + keshimasu.theme)
    # 盤面の表示 番号付き
    keshimasu.display(number_is=True)

    input("エンターキーを押すと始まります.")
    print("制限時間は " + str(keshimasu.time) + "s です")

    #
    # タイマーの設定
    #

    signal.signal(signal.SIGALRM, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, keshimasu.time)  # 100秒後に例外を起こす

    #############
    # ゲーム開始 #
    #############

    try:
        # 1ターンの処理
        while True:
            while True:
                try:
                    # 回答マスの選択
                    input_str = input("番号を指定してください. >>").split(' ')

                    # 数値以外を入力していないかチェック
                    if not np.all([i.isdecimal() for i in input_str]):
                        raise InputError("非負整数を入力してください.")
                    in_num = [int(e) for e in input_str]

                    # 有効な選択か否かのチェック
                    if not np.all(0 < np.all(np.array(in_num) < hei*yoko)):
                        raise InputError(f"0から{hei*yoko-1}の数値を入力してください.")

                    # 選択が2つ以上の場合更に間隔をチェック
                    if len(in_num) > 1:
                        # 各隣り合う要素の差分からなる階差列
                        check_list = np.array([])
                        for i in range(len(in_num)-1):
                            check_list = np.append(check_list, in_num[i+1]-in_num[i])

                        # 横: 間隔がすべて1 縦: 間隔がすべて横幅
                        if np.all(check_list == 1) or np.all(check_list == yoko):
                            break

                        # ここを通る場合, 入力が不適
                        raise InputError("隣り合ったマスを左からもしくは上から指定してください.")
                    else:
                        break
                except ValueError:
                    print("数値を入力してください.")
                except InputError as e:
                    print(e)

            # 選択した番号をnumpy式のindexに変換
            in_num_f = (np.array(in_num)//yoko + tate - hei, np.array(in_num) % yoko)

            # 選択した番号から熟語を構成
            choice = keshimasu.construct_word(in_num_f)

            # 選択した熟語を表示
            print("'" + choice + "'が選択されました.")

            # 回答の入力
            in_ans = input("この選択に対し, お題に合うように答えを入力してください. >>")

            # 正解判定
            if keshimasu.check_answer(choice, in_ans):
                # 正解の場合
                print(choice + ': ' + in_ans + " 正解です.")
                # 盤面の更新
                keshimasu.delete_word(in_num_f)
                print("盤面が更新されました.")

                # 全消しの場合ループを抜けてクリア
                if np.all(keshimasu.playing_table == '　'):  # 全角スペース
                    print("全消しが達成されました. おめでとうございます.")
                    break
                # ターンの終了
            else:
                # 不正解の場合
                print(choice + ': ' + in_ans + " 不正解です.")
            r_time = floor(signal.getitimer(signal.ITIMER_REAL)[0])
            print("残り時間は " + str(r_time) + "s です")

            # お題の表示
            print("お題: " + keshimasu.theme)
            # 盤面の表示 番号付き
            keshimasu.display(number_is=True)

    except TimeUpException as e:
        print(e.args[0])


if __name__ == '__main__':
    play()
