#encoding=utf-8
#读取词典模块
import xlrd
import os
class read_file_part:
    ##大连理工情感词典里的情感词类型简写
    positive = ['PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK']
    negative = ['NA', 'NB', 'NJ', 'NH', 'PF', 'NI', 'NC', 'NG', 'NE', 'ND', 'NN', 'NK', 'NL', 'PC']

    extreme = ""            ##极其|extreme / 最|most           2
    very    = ""            ##很|very                          1.25
    more    = ""            ##较|more                          1.2
    _ish    = ""            ##稍|-ish                          0.8
    insufficiently = ""     ##欠|insufficiently                0.5
    over    = ""            ##超|over
    dligemotion = []        ##大连理工情感词                          1.5
    noword  = ""            ##否定词
    emotionnum   = 0        ##情感词总数
    hownetposemotion = []   ##知网hownet正向情感词
    hownetnegemotion = []   ##知网hownet负向情感词
    tsingposemotion = []    ##TSing正向情感词
    tsingnegemotion = []    ##TSing负向情感词
    ntusdposemotion = []    ##ntusd正向情感词
    ntusdnegemotion = []    ##ntusd负向情感词


    ##路径

    HownetPath = 'SentimentAnalysisDic'+u'/知网Hownet情感词典'
    HownetPosEmoFile = u'/正面情感词语（中文）' + '.txt'
    HownetPosEvaFile = u'/正面评价词语（中文）' + '.txt'
    HownetNegEmoFile = u'/负面情感词语（中文）' + '.txt'
    HownetNegEvaFile = u'/负面评价词语（中文）' + '.txt'
    NegatePath = 'SentimentAnalysisDic' + u'/否定词典' + u'/否定' + '.txt'
    DLLGPath = 'SentimentAnalysisDic' + u'/大连理工情感词汇本体' + u'/情感词汇本体' + '.xlsx'

    ##读取文件函数
    def _read_file_(self, filename):
        file_object = open(filename,encoding="UTF-8")
        try:
            word = file_object.read().split()
        finally:
            file_object.close()
        return word

    ##读取大连理工情感词典
    def _read_dllg_emotion_file(self):
        path = os.getcwd()
        # 打开文件
        bk = xlrd.open_workbook(path+ '/Emotion_Manager/Modules/' + '/res/dic/dalianligong/SenDic.xlsx')
        # 打开工作表
        sh = bk.sheet_by_name("Sheet1")
        # 获取行数
        self.emotionnum = sh.nrows-1
        word = [[] for i in range(1, sh.nrows)]
        for i in range(1, sh.nrows):
            word[i-1] = sh.row_values(i)
        return word


    def __init__(self):
        path = os.getcwd()+'/Emotion_Manager/Modules/'
        self.extreme = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_6.txt')
        self.very = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_4.txt')
        self.more = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_3.txt')
        self._ish = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_2.txt')
        self.insufficiently = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_1.txt')
        self.over = self._read_file_(path + '/res/dic/zhiwang/extent_Lv_5.txt')
        self.noword = self._read_file_(path + '/res/dic/zhiwang/reversed.txt')
        self.dligemotion = self._read_dllg_emotion_file()