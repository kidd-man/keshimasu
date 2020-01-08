import numpy as np
import keshimasu as ksms

##############
# テスト用問題 #
##############

tests = []

#
# テスト1
#

test1_author = "qsama"
test1_tag = "test1"
test1_theme = "かな３文字で漢字を読め"
test1_question = np.array([['御', '神', '酒', '洋'],
                           ['渾', '名', '息', '墨'],
                           ['意', '稲', '吹', '何'],
                           ['気', '桜', '荷', '処'],
                           ['地', '深', '合', '扉'],
                           ['大', '人', '傷', '図']
                           ])
test1_answers = {'大人': {'おとな'},
                 '桜': {'さくら'},
                 '深傷': {'ふかで'},
                 '傷': {'しょう'},
                 '意気地': {'いくじ', 'いきじ'},
                 '意': {'こころ'},
                 '地': {'ところ'},
                 '合図': {'あいず'},
                 '扉': {'とびら'},
                 '稲荷': {'いなり'},
                 '息吹': {'いぶき'},
                 '渾名': {'あだな'},
                 '名': {'みょう'},
                 '御神酒': {'おみき'},
                 '洋墨': {'いんく'},
                 '何処': {'いずこ', 'いずく', 'いづく', 'いずく', 'いどこ'},
                 '地名': {'ちめい'}
                 }
test1_lang = 'hiragana'
test1_height = 4
test1_time = 150

tests.append({'aut': test1_author,
              'tag': test1_tag,
              'thm': test1_theme,
              'que': test1_question,
              'ans': test1_answers,
              'lng': test1_lang,
              'hei': test1_height,
              'tim': test1_time
              })

#
# テスト2
#

test2_author = "qsama"
test2_tag = "test2"
test2_theme = "かな3文字で漢字を読め"
test2_question = np.array([['海', '案', '山', '麒'],
                           ['星', '萄', '酒', '麟'],
                           ['葡', '冬', '至', '子'],
                           ['印', '絵', '達', '磨'],
                           ['度', '族', '蜜', '柑'],
                           ['家', '暦', '文', '字']
                           ])
test2_answers = {'暦': {'こよみ', 'りゃく'},
                 '字': {'あざな'},
                 '家族': {'かぞく'},
                 '印度': {'いんど'},
                 '印': {'しるし'},
                 '度': {'めもり'},
                 '蜜柑': {'みかん'},
                 '達磨': {'だるま'},
                 '絵文字': {'えもじ'},
                 '葡萄': {'ぶどう'},
                 '葡萄酒': {'わいん'},
                 '海星': {'ひとで'},
                 '案山子': {'かかし'},
                 '案': {'つくえ'},
                 '子': {'おとこ'},
                 '麒麟': {'きりん'},
                 '冬至': {'とうじ'}
                 }
test2_lang = 'hiragana'
test2_height = 4
test2_time = 200

tests.append({'aut': test2_author,
              'tag': test2_tag,
              'thm': test2_theme,
              'que': test2_question,
              'ans': test2_answers,
              'lng': test2_lang,
              'hei': test2_height,
              'tim': test2_time
              })

#
# テスト3
#

test3_author = "qsama"
test3_tag = "test3"
test3_theme = "ウで始まる英語に直せ"
test3_question = np.array([['せ', 'お', 'さ', 'い', 'ふ'],
                           ['じ', 'ん', 'お', 'か', 'み'],
                           ['ょ', 'す', 'そ', 'う', 'な'],
                           ['せ', 'い', 'ま', 'う', 'み'],
                           ['い', 'か', 'ど', 'つ', 'び'],
                           ['て', 'ん', 'き', 'ば', 'と'],
                           ['す', 'い', 'よ', 'さ', 'け'],
                           ['け', 'っ', 'こ', 'ん', 'い']
                           ])
test3_answers = {'けっこん': {'ウェディング'},
                 'とけい': {'ウォッチ'},
                 'つばさ': {'ウイング', 'ウィング'},
                 'すいようび': {'ウェンズデー', 'ウェンズデイ'},
                 'まど': {'ウィンドウ', 'ウインドウ', 'ウィンドー', 'ウインドー'},
                 'てんき': {'ウェザー'},
                 'すいか': {'ウォーターメロン'},
                 'なみ': {'ウェーブ', 'ウェイブ', 'ウェーヴ', 'ウェイヴ'},
                 'じょせい': {'ウーマン'},
                 'せんそう': {'ウォー'},
                 'さいふ': {'ウォレット'},
                 'おおかみ': {'ウルフ'}
                 }
test3_lang = 'katakana'
test3_height = 5
test3_time = 200

tests.append({'aut': test3_author,
              'tag': test3_tag,
              'thm': test3_theme,
              'que': test3_question,
              'ans': test3_answers,
              'lng': test3_lang,
              'hei': test3_height,
              'tim': test3_time
              })

#########
# メイン #
#########
if __name__ == '__main__':
    for test in tests:
        # 消しマスインスタンスの生成
        keshimasu = ksms.Keshimasu(ques=test['que'], ans=test['ans'], author=test['aut'],
                                   tag=test['tag'], theme=test['thm'], lang=test['lng'],
                                   height=test['hei'], time=test['tim'])

        # 外部ファイルへの上書き保存
        keshimasu.save(overwrite=True)
