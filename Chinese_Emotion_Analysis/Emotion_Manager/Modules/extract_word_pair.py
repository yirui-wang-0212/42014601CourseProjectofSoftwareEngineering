# encoding=utf-8
import jieba
import jieba.analyse
import jieba.posseg
import sqlite3
import os
from Emotion_Manager.Modules.load_dic import load_multi_meaning_word_dic



#----------------------------------------------------------------------------------
#   获取短句子中的描述对象和描述语
#   para_in : s_sentence = '房间通风不好'
#   para_in : word_info_dic_list = [{'n': '房间', 'k': 'n', 's': 0, 'p': None}, {'n': '通风', 'k': 'n', 's': 0, 'p': None}, {'n': '不好', 'k': 'a', 's': None, 'p': None}]
#   para_out: ('通风','不好')
#----------------------------------------------------------------------------------
def getCommentPair(s_sentence, word_info_dic_list):
    _comment_pair_ = []
    _find_n_ = True                  #找出短句子中的最关键的名词，即描述对象
    _find_a_ = True                  #找出形容短句子中的最关键的形容词，即评价语
    n = None
    a = None
    imp_word_list = jieba.analyse.extract_tags(s_sentence, topK=20, withWeight=False, allowPOS=())
    for word in imp_word_list:
        if _find_n_ or _find_a_:
            for word_info_dic in word_info_dic_list:
                tmp1 = word_info_dic['n']
                tmp2 = word_info_dic['k']
                if _find_n_ and tmp1 == word and (tmp2 == 'n' or tmp2 == 'v'):
                    n = word
                    _find_n_ = False
                    break
                if _find_a_ and tmp1 == word and (tmp2 == 'a' or tmp2 == 'd' or tmp2 == 'no'):
                    a = word
                    _find_a_ = False
                    break
        s_sentence = s_sentence.replace(word, '')
    if a == None and n == None:
        return None
    else:
        if a == None:
            a = s_sentence.strip(n)
        elif n == None:
            n = s_sentence.strip(n)
        _comment_pair_.append(a)
        _comment_pair_.append(n)
        return tuple(_comment_pair_)




def load_data_to_polysemy_db(collocation_list):
    conn = sqlite3.connect('sentiment.db')
    cursor = conn.cursor()
    createtb = '''
       create table polysemy(
       discription VARCHAR(10),
       object      VARCHAR(10),
       score       FLOAT,
       PRIMARY KEY (discription,object)
       )
       '''
    inserttb = 'insert into polysemy(discription,object,score) values (\'大\',\'气味\',-1)'
    querytb = 'select score from polysemy where discription = \'大\' and object =\'气味\' '

    try:
        cursor.execute(createtb)
    except Exception as e:
        pass
    for collocation in collocation_list:
        pass

    cursor.close()
    conn.commit()
    conn.close()




if __name__ == '__main__':

    conn = sqlite3.connect(':memory:')
    conn.execute('create table polysemy(a,n,s)')
    path = 'G:\PyCharm\SentimentNew\Modules/res\dic\create_by_huzehao/'
    file_name = 'word_pair.txt'
    multi_dic = load_multi_meaning_word_dic(path, file_name)
    conn.executemany('insert into polysemy values(?,?,?)',multi_dic)
    s =  conn.execute('select s from polysemy where a = ? and n = ?',('大','气味')).fetchone()
    #print(s)


    #print(multi_dic)
    s_sentence = "房间通风不好"
    word_info_dic_list = [{'n': '房间', 'k': 'n', 's': 0, 'p': None}, {'n': '通风', 'k': 'n', 's': 0, 'p': None}, {'n': '不好', 'k': 'a', 's': None, 'p': None}]
    s_sentence = '本来想让酒店再来打扫一下'
    word_info_dic_list = [{'n': '本来', 'k': 't', 's': None, 'p': None}, {'n': '想', 'k': 'v', 's': 1, 'p': 'pos'}, {'n': '让', 'k': 'v', 's': 0, 'p': None}, {'n': '酒店', 'k': 'n', 's': None, 'p': None}, {'n': '再', 'k': 'd', 's': 0, 'p': None}, {'n': '来', 'k': 'v', 's': 0, 'p': None}, {'n': '打扫', 'k': 'v', 's': 0, 'p': None}, {'n': '一下', 'k': 'm', 's': None, 'p': None}]
    s_sentence = '各位最好的办法就是不要去住'
    word_info_dic_list =  [{'n': '各位', 'k': 'r', 's': 0, 'p': None}, {'n': '最好', 'k': 'a', 's': 1, 'p': 'pos'}, {'n': '的', 'k': 'uj', 's': 0, 'p': None}, {'n': '办法', 'k': 'n', 's': 0, 'p': None}, {'n': '就是', 'k': 'd', 's': 0, 'p': None}, {'n': '不要', 'k': 'df', 's': 0, 'p': None}, {'n': '去', 'k': 'v', 's': 0, 'p': None}, {'n': '住', 'k': 'v', 's': 0, 'p': None}]
    s_sentence = '先是服务态度的恶劣程度就不适宜入住'
    word_info_dic_list = [{'n': '先是', 'k': 'd', 's': 0, 'p': None}, {'n': '服务态度', 'k': 'n', 's': 0, 'p': None}, {'n': '的', 'k': 'uj', 's': 0, 'p': None}, {'n': '恶劣', 'k': 'a', 's': -1, 'p': 'neg'}, {'n': '程度', 'k': 'n', 's': 0, 'p': None}, {'n': '就', 'k': 'd', 's': 0, 'p': None}, {'n': '不', 'k': 'no', 's': None, 'p': None}, {'n': '适宜', 'k': 'a', 's': 1, 'p': 'pos'}, {'n': '入住', 'k': 'v', 's': 0, 'p': None}]
    s_sentence = '该酒店就显得不够气派'
    word_info_dic_list = [{'n': '该', 'k': 'r', 's': 0, 'p': None}, {'n': '酒店', 'k': 'n', 's': 0, 'p': None}, {'n': '就', 'k': 'd', 's': 0, 'p': None}, {'n': '显得', 'k': 'v', 's': 0, 'p': None}, {'n': '不够', 'k': 'v', 's': 0, 'p': None}, {'n': '气派', 'k': 'n', 's': 1, 'p': 'pos'}]
    #s_sentence = '真后悔没住那儿只不过贵100元'
    #word_info_dic_list = [{'n': '真', 'k': 'd', 's': 1, 'p': 'pos'}, {'n': '后悔', 'k': 'v', 's': 0, 'p': None}, {'n': '没住', 'k': 'v', 's': 0, 'p': None}, {'n': '那儿', 'k': 'r', 's': 0, 'p': None}, {'n': '只不过', 'k': 'c', 's': 0, 'p': None}, {'n': '贵', 'k': 'ns', 's': 0, 'p': None}, {'n': '100', 'k': 'm', 's': 0, 'p': None}, {'n': '元', 'k': 'm', 's': 0, 'p': None}]
    s_sentence = '我不能上网'
    word_info_dic_list = [{'n': '我', 'k': 'r', 's': 0, 'p': None}, {'n': '不能', 'k': 'no', 's': None, 'p': None}, {'n': '上网', 'k': 'v', 's': 0, 'p': None}]
    s_sentence = '不能用'
    word_info_dic_list = [{'n': '不能', 'k': 'no', 's': None, 'p': None}, {'n': '用', 'k': 'p', 's': 0, 'p': None}]
    s_sentence = '不能回复邮件'
    word_info_dic_list =  [{'n': '不能', 'k': 'no', 's': None, 'p': None}, {'n': '回复', 'k': 'v', 's': 0, 'p': None}, {'n': '邮件', 'k': 'n', 's': 0, 'p': None}]
    s_sentence =  '性价比低'

    s_sentence = '气味有点大'
    word_info_dic_list = [{'n': '气味', 'k': 'n', 's': 0, 'p': None}, {'n': '有点', 'k': 'n', 's': 0, 'p': None},{'n': '大', 'k': 'a', 's': 0, 'p': None}]

    s_sentence = u'房间总是能听得很响的水声'
    word_info_dic_list = [{'n': '房间', 'k': 'n', 's': 0, 'p': None}, {'n': '总是', 'k': 'c', 's': 0, 'p': None}, {'n': '能', 'k': 'v', 's': 1, 'p': 'pos'}, {'n': '听', 'k': 'v', 's': 0, 'p': None}, {'n': '得', 'k': 'ud', 's': 0, 'p': None}, {'n': '很响', 'k': 'a', 's': 0, 'p': None}, {'n': '的', 'k': 'uj', 's': 0, 'p': None}, {'n': '水声', 'k': 'n', 's': 0, 'p': None}]
    word = u'总是'
    #s_sentence = s_sentence.replace(word,'')
    pair =getCommentPair(s_sentence, word_info_dic_list)
    #print(pair)

    s_sentence = '希望京东改进'
    s_sentence = '住他们酒店还得不到应有的服务'
    s_sentence = '出于价格么'
    imp_word_list = jieba.analyse.extract_tags(s_sentence, topK=20, withWeight=False, allowPOS=())
    print(imp_word_list)

    #t = jieba.posseg.lcut('床单陈旧')
    #test =getCommentPair(s_sentence, word_info_dic_list)
    #print (test)



