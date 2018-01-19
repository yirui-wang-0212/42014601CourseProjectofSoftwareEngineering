# -*- coding: utf-8 -*-
import re
import jieba.posseg
import Emotion_Manager.Modules.LoadDictionary as LoadDictionary
import os
import os.path
from functools import reduce
from Emotion_Manager.Modules.use_dalianligong_dic import _text_processing_

#DATA SEGMENT
__choose__ = 0
no_word_set = set()                              #否定词集

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


#DATA INIT
#初始化否定词集合
def __init__no_word_list():
    with open(dic_root_path + "zhiwang/reversed.txt", encoding="utf-8") as f:
        for items in f:
             item = items.strip()
             no_word_set.add(item)


sense_word_kind_set = {"a", "ad", "an", "ag", "al", "d", "dg","n","l"}    #有情感极性的词性目前包括形容词, 副词


#初始化 知网情感词词典
def __init_zhiwang_dic__():
    __path__ = dic_root_path + "zhiwang/"
    global zhiwang_neg_sen_dic
    global zhiwang_pos_sen_dic
    zhiwang_pos_sen_dic = LoadDictionary.load_dic(__path__, "pos_comment.txt", 1)  # 初始化正面情感词词典
    LoadDictionary.append_dic(zhiwang_pos_sen_dic, __path__, "pos_sentiment.txt", 1)
    zhiwang_neg_sen_dic = LoadDictionary.load_dic(__path__, "neg_sentiment.txt", -1)  # 初始化负面情感词词典
    LoadDictionary.append_dic(zhiwang_neg_sen_dic, __path__, "neg_comment.txt", -1)



#初始化 清华李建军情感词词典
def __init_tsinghua_dic__():
    global tsinghua_neg_dic
    global tsinghua_pos_dic
    __path__ = dic_root_path + "TS_lijianjun/"
    tsinghua_pos_dic = LoadDictionary.load_dic(__path__,"tsinghua.positive.gb.txt",1)
    tsinghua_neg_dic = LoadDictionary.load_dic(__path__,"tsinghua.negative.gb.txt",-1)


#初始化 NTUSD 情感词词典
def __init_ntusd_dic__():
	__path__ = dic_root_path + "NTUSD/"
	global ntusd_neg_dic
	global ntusd_pos_dic
	ntusd_pos_dic = LoadDictionary.load_dic(__path__,"ntusd-positive.txt",1)
	ntusd_neg_dic = LoadDictionary.load_dic(__path__,"ntusd-negative.txt",1)


#初始化大连理工情感词词典
def __init_dllg_dic__():
    __path__ = dic_root_path + "dalianligong/"
    global dllg_dic_meta_list
    dllg_dic_meta_list = LoadDictionary.read_xlsx_file(__path__,"SenDic.xlsx")

#初始化情感词极值词典
def __init_extreme_dic__():
    __path__ = dic_root_path + "extreme_of_word/"
    global word_extreme_dic
    word_extreme_dic = LoadDictionary.load_extreme_dic(__path__, "extreme.txt")

'''
choose == 1     初始化 知网     情感词词典
choose == 2     初始化 大连理工 情感词词典
choose == 3     初始化 NTUSD   情感词词典
choose == 4     初始化 清华    情感词词典 
choose == 5     初始化 情感词极值    词典 
'''
def __init_dic__(dictory_kind):
    global ext_dic
    __path__ = dic_root_path + "zhiwang/"
    ext_dic = LoadDictionary.load_ext_dic(__path__, "extent_Lv_")  # 初始化程度副词词典
    __init__no_word_list()
    if dictory_kind == 1:               #知网
        __init_zhiwang_dic__()
    elif dictory_kind == 2:             #大连理工
        __init_dllg_dic__()
    elif dictory_kind == 3:             #NTUSD
        __init_ntusd_dic__()
    elif dictory_kind == 4:             #清华大学 李建军
        __init_tsinghua_dic__()
    elif dictory_kind == 5:             #情感极值词典
        __init_extreme_dic__()
    else:
        return None





# 句子生成器:
#input:  字符串
#output: 生成器
#将其返回值传入next() 函数中, 调用一次next, 可得到一个非空的字符串
def get_paragraph(str):
    str = re.split('[。？！；.?!;“”]', str)
    for s in str:
        if s != ''and s!= ' ':
            yield s.strip()


# 意群生成器:
# input:字符串列表
# output: 生成器
# 使用next函数 一次返回一个非空非空格的字符串
def get_group(gen):
    for s in gen:
       s = re.split('[,，]',s)
       for str in s:
           if str != ' ' and str != '':
               yield str.strip()


#private
#input: 词典, 字符串
#output: 情感词的得分
def __getScore__(dic, word):
    return dic.get(word, 0)

'''
def __find_word_info_zhiwang__(word, kind):
    dic = {}
    def __setdic__(k, s, p=None):
        dic['n'] = word  # word
        dic['k'] = k  # kind
        dic['s'] = s  # score
        dic['p'] = p  # property

    if word in no_word_set:
        __setdic__('no', None, None)
    elif kind in sense_word_kind_set:
        score = __getScore__(ext_dic, word)
        if score != 0:
            __setdic__(kind, score, 'ext')
        else:
            score = __getScore__(zhiwang_pos_sen_dic, word)
            if score != 0:
                __setdic__(kind, score, 'pos')
            else:
                score = __getScore__(zhiwang_neg_sen_dic, word)
                if score != 0:
                    __setdic__(kind, score, 'neg')
                else:  # 有意义的词被遗漏了
                    __setdic__(kind, score)
                    ignoredWordList.write("{} {} {}\n".format(word, kind, score))
                    pass
    elif kind == 'c':
        __setdic__(kind, None, None)
    if len(dic) > 0:
        return dic
    else:
        return None


def __find_word_info_ntusd__(word,kind):

    pass

def __find_word_info_dllg__(word, kind):
    pass

def __find_word_info_tsinghua(word,kind):
    pass

def __find_word_info_extreme(word, kind):
    pass
'''

#input:    string, char, boolean , 分别表示词语, 词性, 是否为全模式
#output:
def find_word_info(word, kind, dictory_kind, All = True):
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
    elif kind in sense_word_kind_set:
        score =  __getScore__(ext_dic, word)
        if score != 0:
            __setdic__(kind, score, 'ext')
        else:
            if dictory_kind == 1:       #知网
                __common__(zhiwang_pos_sen_dic, zhiwang_neg_sen_dic)

            elif dictory_kind == 2:     #大连理工
                pass

            elif dictory_kind == 3:     #ntusd
                __common__(ntusd_pos_dic,ntusd_neg_dic)

            elif dictory_kind == 4:     #清华 李建军
                __common__(tsinghua_pos_dic, tsinghua_neg_dic)

            elif dictory_kind == 5:     #情感极值词典
                score = __getScore__(word_extreme_dic, word)
                if score > 0:
                    __setdic__(kind, score, "pos")
                elif score < 0:
                    __setdic__(kind, score, "neg")
                else:              #情感词语遗漏了
                    ignoredWordList.write("{} {} {}\n".format(word, kind, score))

    if len(dic) > 0:
        return dic
    elif All == True:
        __setdic__(kind,word,0)
    else: return None


def splict_group_into_list(str, dictory_kind):                #传入一个意群(字符串)返回一个jieba分词系统分词后的词描述字典列表
    _word_list = []
    data = jieba.posseg.cut(str)
    for word, kind in data:
        tmp = find_word_info(word, kind, dictory_kind)
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


def get_group_score(group = [{}], stream =None):#传入一个由描述词的字典组成的列表, 得到一个意群的分值
    if len(group) > 0:
        stack = []
        copystack = []
        GroupScore = 0
        NoWordFirst = False
        HaveSenWord = False
        ExtInNoAndSen = False
        if group[0].get("k") == 'no':
            NoWordFirst = True
            group.pop(0)
            stack.append(-1)
            copystack.append(-1)
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
    with open(path+filename,'r',encoding='UTF-8') as f:
        document = f.read()

teststr1 = "我很不开心"
teststr2 = "我不很开心"
teststr3 = '我难过而且悲伤'
teststr4 = '第一印象不好'
teststr5 = '这件事不好说'

str = '''服务态度极其差，前台接待好象没有受过培训，连基本的礼貌都不懂，竟然同时接待几个客人；    
大堂副理更差，跟客人辩解个没完，要总经理的电话投诉竟然都不敢给。要是没有作什么亏心事情，跟本不用这么怕。'''

def __getFileNameInDir__(path):
    if path.endswith('.txt'):
        yield ''
    else:
        for parents, directorys, filenames in os.walk(path):
            for filename in filenames:
                yield filename

def handleError(ErrorKind,*params):
    kinds = {1: "sense word ignored", 2: "wrong score"}
    kind =kinds.get(ErrorKind,0)
    stream = None
    if kind == 1:
        with open('ingored.txt', 'a', encoding='UTF-8') as f:
            stream = f
            pass
    elif kind == 2:
        with open('wrongScore.txt','a',encoding='UTF-8') as f:
            stream = f


wrongFileList = open('wrongScore.txt','a',encoding='UTF-8')
ignoredWordList = open('ignoredWord.txt','a',encoding='UTF-8')

'''
def getScoreFromDir(path, dictory_kind):   #传入一个路径, 可以是一个文件夹的路径(以'//'结尾, 也可以是一个txt文件的路径
    __init_dic__(dictory_kind)
    filenames = __getFileNameInDir__(path)
    cx = 0
    dx = 0
    for filename in filenames:
         with open(path + filename, 'r', encoding='UTF-8') as f:
             doc = f.read()
             # doc = '老的, , ,标准间改善.  '
             pgen = get_paragraph(doc)
             ggen = get_group(pgen)
             score_sum = 0
             for group in ggen:
                 wordList = splict_group_into_list(group,dictory_kind)
                 score, stack = get_group_score(wordList)
                 #本段是测试用,以后要写一个专门的侧屋处理函数, 待完成
                 if score < 0:
                     print(group, score, stack)
                 elif score > 0:
                     print(group, stack, wordList)
                 else:
                     print(group, wordList)
                 score_sum += score
             if score_sum > 0:
                 cx += 1
                 wrongFileList.write("{}\n".format(filename))
                 print(filename, score_sum)
             if score_sum == 0:
                 dx += 1
                 print(filename)
    print("total:\t{} \t{}".format(cx,dx))
    wrongFileList.close()
'''

# testFilePath = 'G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\neg\\neg.108.txt'


def getScoreFromString(text, dictory_kind):
    __init_dic__(dictory_kind)
    pgen = get_paragraph(text)
    ggen = get_group(pgen)
    _score_sum_ = 0
    if dictory_kind == 4:
        _score_sum_ = _text_processing_(text)
    else:
        for group in ggen:
            wordList = splict_group_into_list(group, dictory_kind)
            score, stack = get_group_score(wordList)
            _score_sum_ += score
            # print(group, score, stack, wordList)
    return _score_sum_

if __name__ == '__main__':
    str1 = "你非常漂亮!"
    print(getScoreFromString(str1, 1))
    # print(1)
    #getScoreFromDir(neg_corpus_root_path, 1)
    #print(getScoreFromString('标准间太差,房间还不如3星的,而且设施非常陈旧.建议酒店把老的标准间从新改善.',4))






