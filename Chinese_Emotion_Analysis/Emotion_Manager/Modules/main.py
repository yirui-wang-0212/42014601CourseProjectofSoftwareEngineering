# -*- coding: utf-8 -*-
import re
import jieba.posseg
import Emotion_Manager.Modules.load_dic
import os
import os.path
import sqlite3
from Emotion_Manager.Modules.load_dic import load_multi_meaning_word_dic
from functools import reduce
from Emotion_Manager.Modules.use_dalianligong_dic import _text_processing_
from Emotion_Manager.Modules.extract_word_pair import getCommentPair
#DATA SEGMENT
__choose__ = 0
no_word_set = set()                            #否定词集

zhiwang_pos_sen_dic = {}                       #知网正面情感词词典
zhiwang_neg_sen_dic = {}                       #知网负面情感词词典
ext_dic = {}                                   #知网程度副词词典

tsinghua_pos_dic = {}                          #清华李建军正面情感词词典
tsinghua_neg_dic = {}                          #清华李建军负面情感词词典

ntusd_pos_dic = {}                             #NTUSD正面情感词词典
ntusd_neg_dic = {}                             #NTUSD负面情感词词典

word_extreme_dic = {}                          #情感词极值词典

dllg_dic_meta_list = []                        #大连理工情感词元组列表


dic_root_path = os.getcwd() + '/Emotion_Manager/Modules/res/dic/'         #情感词典的根目录

neg_corpus_root_path = os.getcwd() + '/Emotion_Manager/Modules/res/corpus/hotel/neg/'  #酒店评价负面情绪语料库目录
pos_corpus_root_path = os.getcwd() + '/Emotion_Manager/Modules/res/corpus/hotel/pos/' #酒店评价正面情绪语料库目录
sense_word_kind_set = {}                #具有情感的词性集合

conn = sqlite3.connect(':memory:')
conn.execute('create table polysemy(a,n,s)')
path = os.getcwd() + '/Emotion_Manager/Modules/res/dic/create_by_huzehao/'
file_name = 'word_pair.txt'
multi_dic = load_multi_meaning_word_dic(path, file_name)
conn.executemany('insert into polysemy values(?,?,?)', multi_dic)
#DATA INIT

#---------------------------------------
#初始化否定词集合
#---------------------------------------
def __init__no_word_list():
    with open(dic_root_path + "zhiwang/reversed.txt", encoding="utf-8") as f:
        for items in f:
             item = items.strip()
             no_word_set.add(item)


sense_word_kind_set = {"a", "ad", "an", "ag", "al", "d", "dg","n","l",'v','m','z','i','zg','nr'}    #有情感极性的词性目前包括形容词, 副词

#---------------------------------------
#初始化 知网情感词词典
#---------------------------------------
def __init_zhiwang_dic__():
    __path__ = dic_root_path + "zhiwang/"
    global zhiwang_neg_sen_dic
    global zhiwang_pos_sen_dic
    zhiwang_pos_sen_dic = Emotion_Manager.Modules.load_dic.load_dic(__path__, "pos_comment.txt", 1)  # 初始化正面情感词词典
    Emotion_Manager.Modules.load_dic.append_dic(zhiwang_pos_sen_dic, __path__, "pos_sentiment.txt", 1)
    zhiwang_neg_sen_dic = Emotion_Manager.Modules.load_dic.load_dic(__path__, "neg_sentiment.txt", -1)  # 初始化负面情感词词典
    Emotion_Manager.Modules.load_dic.append_dic(zhiwang_neg_sen_dic, __path__, "neg_comment.txt", -1)


#---------------------------------------
#初始化 清华李建军情感词词典
#---------------------------------------
def __init_tsinghua_dic__():
    global tsinghua_neg_dic
    global tsinghua_pos_dic
    __path__ = dic_root_path + "TS_lijianjun\\"
    tsinghua_pos_dic = Modules.load_dic.load_dic(__path__, "tsinghua.positive.gb.txt", 1)
    tsinghua_neg_dic = Modules.load_dic.load_dic(__path__, "tsinghua.negative.gb.txt", -1)

#---------------------------------------
#初始化 NTUSD 情感词词典
#---------------------------------------
def __init_ntusd_dic__():
	__path__ = dic_root_path + "NTUSD/"
	global ntusd_neg_dic
	global ntusd_pos_dic
	ntusd_pos_dic = Emotion_Manager.Modules.load_dic.load_dic(__path__, "ntusd-positive.txt", 1)
	ntusd_neg_dic = Emotion_Manager.Modules.load_dic.load_dic(__path__, "ntusd-negative.txt", 1)

#---------------------------------------
#初始化大连理工情感词词典
#---------------------------------------
def __init_dllg_dic__():
    __path__ = dic_root_path + "dalianligong/"
    global dllg_dic_meta_list
    dllg_dic_meta_list = Emotion_Manager.Modules.load_dic.read_xlsx_file(__path__, "SenDic.xlsx")

#---------------------------------------
#初始化情感词极值词典
#---------------------------------------
def __init_extreme_dic__():
    __path__ = dic_root_path + "extreme_of_word/"
    global word_extreme_dic
    word_extreme_dic = Emotion_Manager.Modules.load_dic.load_extreme_dic(__path__, "extreme.txt")


#-----------------------------------------------------------------------
#   初始化词典 , 加载自定义jieba词典
#   para_in : dic_kind 词典类型
#             1.    知网
#             2.    大连理工
#             3.    NTUSD
#             4.    清华李建军
#             5.    清华情感词极值词典
#             else  None
#   para_out: 无
#-----------------------------------------------------------------------
def __init_dic__(dic_kind):
    global ext_dic
    jieba.load_userdict(dic_root_path + 'create_by_huzehao/jieba_dic.txt')
    __path__ = dic_root_path + "zhiwang/"
    ext_dic = Emotion_Manager.Modules.load_dic.load_ext_dic(__path__, "extent_Lv_")  # 初始化程度副词词典
    __init__no_word_list()
    if dic_kind == 1:               #知网
        __init_zhiwang_dic__()
    elif dic_kind == 2:             #大连理工
        __init_dllg_dic__()
    elif dic_kind == 3:             #NTUSD
        __init_ntusd_dic__()
    elif dic_kind == 4:             #清华大学 李建军
        __init_tsinghua_dic__()
    elif dic_kind == 5:             #情感极值词典
        __init_extreme_dic__()
    else:
        return None





# 句子生成器:
#input:  字符串
#output: 生成器
#将其返回值传入next() 函数中, 调用一次next, 可得到一个非空的字符串
def get_paragraph(str):
    str = re.split('[。？！；.?!;“”．]', str)
    for s in str:
        if s != ''and s!= ' ':
            yield s.strip()

#-----------------------------------------------------------------------
# 意群生成器:
# input:字符串列表
# output: 生成器
# 使用next函数 一次返回一个非空非空格的字符串
#-----------------------------------------------------------------------
def get_group(gen):
    for s in gen:
       s = re.split('[,，、（）\s]',s)
       for str in s:
           if str != ' ' and str != '':
               yield str.strip()

#---------------------------------------
#private
#input: 词典, 字符串
#output: 情感词的得分
#---------------------------------------
def __getScore__(dic, word):
    return dic.get(word, 0)


#-----------------------------------------------------------------------
#给出一个中文词语, 及其词性, 返回一个字典, 里面包含 词语 词性 分数 情感词类型
#   eg: {'n': '恶劣', 'k': 'a', 's': -1, 'p': 'neg'}
#         n:词语名     k: 词性   s:分数    p: 属性
#   para_in :  word       词语
#   para_in :  kind       词性
#   para_in :  dic_kind   字典类型
#   para_in :  All        是否为全模式(默认为False)
#                         True   :对所有传入的词语均返回一个详细信息
#                         False  :只对词性在 sense_word_kind_set 里的词返回一个详细信息
#   para_out:  dic        描述一个词语的详细信息
#-----------------------------------------------------------------------
def find_word_info(word, kind, dic_kind, All = True):
    dic = {}
    def __setdic__(k, s, p = None):
        dic['n'] = word                   #word
        dic['k'] = k                      #kind
        dic['s'] = s                      #score
        dic['p'] = p                      #property

    def __common__(pos_dic, neg_dic):     #如果词语是正面情感词或负面情感词的时候, 进行该操作
        score = __getScore__(pos_dic, word)
        if score != 0:
            __setdic__(kind, score, 'pos')
        else:
            score = __getScore__(neg_dic, word)
            if score != 0:
                __setdic__(kind, score, 'neg')
            else:  # 有意义的词被遗漏了
                __setdic__(kind, score)
                ignoredWordList.write("{} {} {}\n".format(word, kind, score))

    if word in no_word_set:
        __setdic__('no', None, None)
    elif  kind in sense_word_kind_set:
        score =  __getScore__(ext_dic, word)
        if score != 0:
            __setdic__(kind, score, 'ext')
        else:
            if dic_kind == 1:       #知网
                __common__(zhiwang_pos_sen_dic, zhiwang_neg_sen_dic)

            elif dic_kind == 2:     #大连理工
                pass

            elif dic_kind == 3:     #ntusd
                __common__(ntusd_pos_dic,ntusd_neg_dic)

            elif dic_kind == 4:     #清华 李建军
                __common__(tsinghua_pos_dic, tsinghua_neg_dic)

            elif dic_kind == 5:     #情感极值词典
                score = __getScore__(word_extreme_dic, word)
                if score > 0:
                    __setdic__(kind, score, "pos")
                elif score < 0:
                    __setdic__(kind, score, "neg")
                else:              #情感词语遗漏了
                    ignoredWordList.write("{} {} {}\n".format(word, kind, score))

    if len(dic) > 0:
        return dic
    elif All:
        __setdic__(kind, 0, None)
        return dic
    else: return None


#-----------------------------------------------------------------------
#   传入一个意群(字符串)返回一个jieba分词系统分词后的词描述字典列表
#   para_in : tiny_sentence  eg : '房间通风不好'
#   para_in : dic_kind
#             1: 知网
#             2: 大连理工
#             3: ntusd
#             4:李建军
#             5:极值词典
#   para_out: 词语信息列表 eg :[{'n':'房间','k': 'n','s': 0,'p':None},
#                             {'n':'通风','k':'n','s':0,'p':None},
#                             {'n':'不好','k':'a','s':None,'p':None}]
#-----------------------------------------------------------------------
def splict_group_into_list(tiny_sentence, dic_kind):
    _word_list = []
    data = jieba.posseg.cut(tiny_sentence)
    for word, kind in data:
        tmp = find_word_info(word, kind, dic_kind)
        if tmp:
            _word_list.append(tmp)
    return _word_list


def __check__(word):
    dic = {}
    dic["pos"] = __getScore__(zhiwang_pos_sen_dic, word)
    dic["neg"] = __getScore__(zhiwang_neg_sen_dic, word)
    dic["ext"] = __getScore__(ext_dic, word)
    return dic


def __reduceOp__(item1, item2):
    return item1 * item2


def __CaculateScoreOfGroup__(stack = [], ExtInNoAndSen = False):
    if ExtInNoAndSen:
        return reduce(__reduceOp__, stack) * -0.5
    else:
        return reduce(__reduceOp__, stack)


def __meet_conj__(stack):
    pass

#-----------------------------------------------------------------------
#   para_in :
#   para_in :
#   para_out:
#-----------------------------------------------------------------------
def _get_group_score(tiny_sentence,group = [{}], stream = None):
    if len(group) > 0:
        stack = []
        score = None
        score_item = None
        pair = getCommentPair(tiny_sentence,group)
        if pair != None:
            score_item = conn.execute('select s from polysemy where a = ? and n = ?', pair).fetchone()
            if score_item != None:
                score = score_item[0]
                stack.append(score)
                for item in group:
                    if item.get('k') == 'no':
                        stack.append(-1)
                    elif item.get('k') == 'ext':
                        stack.append(item.get('s'))
                return  __CaculateScoreOfGroup__(stack, False), stack, pair
        #else:
        score, stack = get_group_score(group)
        return score, stack, pair
    return 0, None


#-----------------------------------------------------------------------
#传入一个由描述词的字典组成的列表, 得到一个意群的分值
#   para_in :
#   para_in :
#   para_out:
#-----------------------------------------------------------------------
def get_group_score(group = [{}], stream =None):
    if len(group) > 0:
        stack = []
        copystack = []
        GroupScore = 0
        NoWordFirst = False
        HaveSenWord = False
        ExtInNoAndSen = False
        if group[0].get("k") == 'no':
            NoWordFirst = True
            copystack.append('no')

        for item in group:
            if item.get('p') == 'pos' or item.get('p') == 'neg':
                HaveSenWord = True
                stack.append(item.get('s'))
            elif item.get('p') == 'ext':
                stack.append(item.get('s'))
                if NoWordFirst == True and HaveSenWord == False:
                    ExtInNoAndSen = True
            elif item.get('k') == 'c':
                __meet_conj__(stack)
                pass
            elif item.get('k') == 'no':
                stack.append(-1)
        copystack.append(stack)
        if HaveSenWord:
            GroupScore = __CaculateScoreOfGroup__(stack, ExtInNoAndSen)
        return GroupScore, copystack
    return 0, None


def fromPath(path,filename):
    with open(path + filename,'r',encoding='UTF-8') as f:
        document = f.read()

#-----------------------------------------------------------------------
#                            内部函数
#获取给定文件夹的目录, 返回文件夹下的文件名, 生成器类型
#   para_in : path: 可为文件路径, 也可为文件夹路径
#
#   para_out: filename 取决于 path 的值
#             1. 文件夹路径: 返回文件名
#             2. 文件路径  : 返回空字符串
#-----------------------------------------------------------------------
def __getFileNameInDir__(path):
    if path.endswith('.txt'):
        yield ''
    else:
        for parents, directorys, filenames in os.walk(path):
            for filename in filenames:
                yield filename


#-----------------------------------------------------------------------
#   错误处理函数                 未完成
#   para_in :
#   para_in :
#   para_out:
#-----------------------------------------------------------------------
def handleError(ErrorKind,*params):
    kinds = {1: "sense word ignored", 2: "wrong score"}
    kind =kinds.get(ErrorKind,0)
    stream = None
    if kind == 1:
        with open('ingored.txt', 'a', encoding='UTF-8') as f:
            stream = f
            pass
    elif kind == 2:
        with open('wrong_score_filename.txt','a',encoding='UTF-8') as f:
            stream = f


wrongFileList = open('wrong_score_filename.txt','a',encoding='UTF-8')
wrongSmallSentence =open('wrong_small_sentence.txt','a',encoding='UTF-8')
imp_word_pair = open('imp_word_pair.txt','a',encoding='UTF-8')
ignoredWordList = open('ignored_word.txt','a',encoding='UTF-8')



#-----------------------------------------------------------------------
#   测试语料用函数: 输入一个语料所在文件夹路径或文件路径, 在控制台中输出分析的详细结果
#
#   para_in :  path 语料文件的路径 or 语料文件夹的路径
#   para_in :  dic_kind 使用的词典类型
#   para_out:  不同文件直接以 '===...==='分开
#              同一文件中不同的短句子 以 '---...---' 分开
#              对每个短句子依次输出:
#
#-----------------------------------------------------------------------
def getScoreFromDir(path, dic_kind):
    __init_dic__(dic_kind)
    filenames = __getFileNameInDir__(path)
    plus = 0
    minus = 0
    zero = 0
    for filename in filenames:
         with open(path + filename, 'r', encoding='UTF-8') as f:
             doc = f.read()
             #doc = '我们定的是差不多260的特价房，我不想形容，通往房间的过程简直隧道，房间极小，窗户在是停车场位置，整晚被吵！真的不想别人和我一样感觉被忽悠，酒店分两边，应该另一边的还可以，但如果跟我一样要特价房，就要有心理准备！携程服务还可以，退了第二.三天的预定！'
             pgen = get_paragraph(doc)
             ggen = get_group(pgen)
             score_sum = 0
             print("=============================================")
             for group in ggen:
                 wordList = splict_group_into_list(group, dic_kind)
                 score, stack, pair = _get_group_score(group, wordList)
                 print('-----------------------------------')
                 #if pair!=None and score != 0:

                     #imp_word_pair.write(group+ "     ({} , {})".format(pair[0],pair[1]) +'\n\n')
                 if score < 0:
                     #i = 0
                     print("score < 0 : ",score, '\ngroup: ', group, '\nstack:', stack, '\nwordlist: ', wordList, "\npair: ", pair, '\n\n')
                 elif score > 0:
                     #i = 1
                   # wrongSmallSentence.write(group + '\n\n\n')
                     print("score > 0 : ",score, '\ngroup: ', group ,'\nstack:', stack, '\nwordlist: ', wordList, "\npair: ", pair, '\n\n')
                 elif score == 0:
                     #i = 0
                     print("score == 0 : ",score, '\ngroup: ', group, '\nstack:', stack, '\nwordlist: ', wordList, "\npair: ", pair, '\n\n')

                 score_sum += score
             if score_sum > 0:
                 plus += 1
               #  wrongFileList.write("{}\n".format(filename))
                 print("filename:",filename,"\nscore:", score_sum)
             if score_sum == 0:
                 zero += 1
                 print("filename:", filename, "\nscore:", score_sum)
             if score_sum < 0:
                 minus += 1
                 print("filename:", filename, "\nscore:", score_sum)
    print('=================================================')
    print("\n\n正向：{}\n 负向: {} \n为零：{}".format(plus, minus, zero))
    wrongFileList.close()
    wrongSmallSentence.close()
    imp_word_pair.close()





#-----------------------------------------------------------------------
#                               暴露接口
#   para_in : text      文件内容    字符串
#   para_in : dic_kind  词典类型    整数值
#             1: 知网
#             2: 大连理工
#             3: ntusd
#             4:李建军
#             5:极值词典
#   para_out: score     文本情感值
#-----------------------------------------------------------------------
def getScoreFromString(text, dic_kind):
    __init_dic__(dic_kind)
    pgen = get_paragraph(text)
    ggen = get_group(pgen)
    _score_sum_ = 0
    if dic_kind == 4:
        _score_sum_ = _text_processing_(text)
    else:
        for group in ggen:
            wordList = splict_group_into_list(group, dic_kind)
            score, stack = get_group_score(wordList)
            _score_sum_ += score
            #print(group, score, stack, wordList)
    return _score_sum_



#==================================================================================
# 测试数据参数定义区
#
teststr1 = "我很不开心"
teststr2 = "我不很开心"
teststr3 = '我难过而且悲伤'
teststr4 = '第一印象不好'
teststr5 = '这件事不好说'

str = '''服务态度极其差，前台接待好象没有受过培训，连基本的礼貌都不懂，竟然同时接待几个客人；    
大堂副理更差，跟客人辩解个没完，要总经理的电话投诉竟然都不敢给。要是没有作什么亏心事情，跟本不用这么怕。'''





#---------------------------------------------------------------------------------
'                           以下路径供测试用                                   '
corpus_root_path = os.getcwd() + '/res/corpus/'
neg1000_path = corpus_root_path + 'hotel/neg/'   #测1000个负向文本
pos1000_path = corpus_root_path + 'hotel/pos/'   #1000个正向文本
neg3000_path = corpus_root_path + 'hotel/neg3000/' #3000个负向文本
pos7000_path = corpus_root_path+ 'hotel/pos7000'   #7000个正向文本

test_100_path = corpus_root_path + 'hotel/n/0/'    #100个负向文本
test_file_path = corpus_root_path + 'hotel/n/7/neg.712.txt'  #某一个文本

#==================================================================================




if __name__ == '__main__':
    #word_info_list = splict_group_into_list("气味有点大",1)
    #score, stack = _get_group_score("气味有点大",word_info_list)
    #print(word_info_list)
    #print('score : ',score, '  stack: ', stack)
    #t = splict_group_into_list('床单陈旧',1)
    #print(t)
    #str1 = "你非常漂亮!"
    #print(getScoreFromString(str1, 1))

    #s, stack = _get_group_score('床单陈旧',[{'n': '床单', 'k': 'n', 's': 0, 'p': None}, {'n': '陈旧', 'k': 'a', 's': -1, 'p': 'neg'}])
    #print(s,"  " ,stack)

    #getScoreFromDir(test_total_path, 1)
    print(getScoreFromString('卫生状况也不太近人意',1))
    #getScoreFromDir(test_file_path,1)
    #__init_extreme_dic__()
    #print(word_extreme_dic)
