#encoding=utf-8
from __future__ import print_function, unicode_literals
from Emotion_Manager.Modules.read_file import read_file_part
import jieba
import jieba.posseg
import jieba.analyse
import re
import sys
import os
#sys.setdefaultencoding('utf8')
sys.path.append("../")

##载入读取词典模块
rf = read_file_part()

##路径
posPath = 'SentimentAnalysisDic/pos/'
negPath = 'SentimentAnalysisDic/neg/'
testPath = 'SentimentAnalysisDic/test/'

##分段函数，用于将大文章片段分割为小文章片段
##输入  待分割文章片段 text
##      分割符号      symblo
##输出  分割结果      result
def _divide_(text, symbol):
    result = re.split(symbol, text)
    while '' in result:
        result.remove('')
    return result

##程度词判断函数，共有6个等级的程度词，对应不同的程度系数
##输入  待判断词      word
##输出  程度系数      dword_weight
def _degree_word_judgement_(word):
    if (word in rf.extreme):
        dword_weight = 2.0
    elif (word in rf.very):
        dword_weight = 1.25
    elif (word in rf.more):
        dword_weight = 1.2
    elif (word in rf._ish):
        dword_weight = 0.8
    elif (word in rf.insufficiently):
        dword_weight = 0.5
    elif (word in rf.over):
        dword_weight = 1.5
    else:
        dword_weight = 1.0
    return dword_weight

##情感词判断函数，在情感词典中查找情感词的极性与幅度
##输入  待判断词      word
##输出  幅度与极性    list
def _dlig_emotion_word_judgement_(word):
    list = [0,1]
    for i in range(0, rf.emotionnum):
        if (word == rf.dligemotion[i][0]):
            list[0] = rf.dligemotion[i][5]
            if (rf.dligemotion[i][6] == 1):
                list[1] = 1.0
            elif (rf.dligemotion[i][6] == 2):
                list[1] = -1.0
            elif (rf.dligemotion[i][6] == 0):
                list[1] = 0.0
            else:
                char = rf.dligemotion[i][4]
                if (char in rf.positive):
                    list[1] = 1.0
                elif (char in rf.negative):
                    list[1] = -1.0
                else:
                    list[1] = 0.0
            break
    return list

##意群情感计算函数
##输入  意群          group
##输出  意群情感值    group_value
def _group_emotion_(group):
    result = jieba.posseg.cut(group)
    #print(result)
    order = 1
    W = 1.0
    dword_weight = 1.0
    dword_point = -1.0
    nword_point = []
    eword_weight = 0.0
    eword_Polar = 1.0
    for w in result:
        eword_Polar
        dword_weight = _degree_word_judgement_(w.word)
        elist = _dlig_emotion_word_judgement_(w.word)
        if(elist[0]!=0 and w.flag != 'v'):
            eword_weight = elist[0]
            eword_Polar = elist[1]
            #print(w.word, eword_weight, eword_Polar)
        elif (dword_weight != 1):
            dword_point = order
        elif (w.word in rf.noword):
            nword_point.append(order)
        order = order + 1
    for point in nword_point:
        if (point > dword_point):
            W = W * -1.0
        else:
            W = W * 0.5
    group_value = W * dword_weight * eword_Polar * eword_weight
    #print("group_value:", group_value)
    #print(W, dword_weight, eword_Polar, eword_weight)
    return group_value

##文章情感分析接口
##输入  文件路径      filepath
##输出  文章情感值    1（积极） -1（消极） 0（无极性）
def _text_processing_(Document):
    Paragraphs = Document.split("\n")
    document_value_list = []
    document_value = 0.0
    while '' in Paragraphs:
        Paragraphs.remove('')
    for paragraph in Paragraphs:
        Sentences = _divide_(paragraph, r'[。；！？．.;!?~]')
        paragraph_value_list = []
        paragraph_value = 0.0
        for sentence in Sentences:
            Groups = _divide_(sentence, r'[,，]')
            sentence_value_list = []
            sentence_value = 0.0
            for group in Groups:
                group_value = _group_emotion_(group)
                sentence_value_list.append(group_value)
                #print("group_value:", group_value)
            for gvalue in sentence_value_list:
                sentence_value = sentence_value + gvalue
            #print("sentence_value:", sentence_value)
            paragraph_value_list.append(sentence_value)
        for svalue in paragraph_value_list:
            paragraph_value = paragraph_value + svalue
        paragraph_value = paragraph_value / (len(paragraph_value_list))
        #print("paragraph_value:", paragraph_value)
        document_value_list.append(paragraph_value)
    for pvalue in document_value_list:
        document_value = document_value + pvalue
    document_value = document_value / len(document_value_list)
    #print("document_value:", document_value)
    if (document_value > 0):
        return document_value
    elif (document_value < 0):
        #print(document_value)
        return document_value
    else:
        return 0

##测试成功率接口
##输入  文件路径      filepath
##      测试类型      type1（测试正向结果：pos, 测试负向结果：neg）
##      词典类型      type2（0：大连理工:， 1：知网Hownet， 2：清华大学）
##输出  成功率        Percentage
'''
def _success_rate_(filepath, type1, type2):
    Percentage = 0
    Base = 0
    FindPath = filepath
    FileNames = os.listdir(FindPath)
    for file_name in FileNames:
        filename = os.path.join(FindPath, file_name)
        print(filename)
        if (type1 == 'pos' and _text_processing_(filename, type2) == 1):
            Percentage += 1
        elif (type1 == 'neg' and _text_processing_(filename, type2) == -1):
            Percentage += 1
        Base += 1.0
    Percentage = 100 * Percentage / Base
    return Percentage
'''
##测试函数
#print(_success_rate_('G:\\PyCharm\\SentimentNew\\res\\corpus\\hotel\\neg', "neg", 0))

_text_processing_("标准间太差,房间还不如3星的,而且设施非常陈旧.建议酒店把老的标准间从新改善.")