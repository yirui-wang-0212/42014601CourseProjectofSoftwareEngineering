import xlrd

#----------------------------------------------------------------------
#	通用 读取一个文本词典 返回一个内存词典, 其中所有词的 score 一样
#	针对文本词典只含有词语没有分数的情况
#----------------------------------------------------------------------
def load_dic(path, file_name, score):
	wordDict = {}
	with open(path+file_name, encoding="utf-8") as fin:
		for line in fin:
			word = line.strip()
			wordDict[word] = score
	return wordDict

#----------------------------------------------------------------------
#传入 上面 函数构造的词典, 向其中附加 另一 score 的 词语
#----------------------------------------------------------------------
def append_dic(wordDict, path, file_name, score):
	with open(path+file_name, encoding="utf-8") as fin:
		for line in fin:
			word = line.strip()
			wordDict[word] = score


#-----------------------------------------------------------------------
#   知网词典 程度副词 词典的读取与构造
#   para_in  :
#   para_in  :
#   para_out :
#-----------------------------------------------------------------------
def __get_score__(x):
	return {0:0.5, 1:0.8 , 2:1.2, 3:1.25, 4:1.5, 5:2}.get(x,0)

def load_ext_dic(path, file_name):
	extent_dic = {}
	for i in range(6):
		score = __get_score__(i)
		with open(path + file_name + str(i + 1) + ".txt", encoding='utf-8') as fin :
			for line in fin:
				word = line.strip()
				extent_dic[word]= score
	return extent_dic


#--------------------------------------------------------------------------------------
#   读取 txt 文件, 每一行包含两项 , 一项是词语, 一项是词语的极值
#   para_in: path = 'G:/PyCharm/SentimentNew/Modules/res/dic/extreme_of_word/'
#   para_in: file_name = 'extreme.txt'
#   para_out:{'沉醉于': -0.4, '要': 0.48549295774647866, '暗查': -0.4, '陶醉在': 1.95,...}
#---------------------------------------------------------------------------------------
def load_extreme_dic(path, file_name):
	__dic__ = {}
	with open(path + file_name, 'r', encoding="UTF-8") as f:
		line = f.readline()
		while len(line) > 0:
			li = line.split()
			__dic__[li[0]] = float(li[1])
			line = f.readline()
		return __dic__


#----------------------------------------------------------------
#   读取 excel 文件 : xlsx 文件, 构建情感词词典
#   para_in  : path
#   para_in  : file_name
#   para_out :
#----------------------------------------------------------------
def read_xlsx_file(path, file_name):
	book = xlrd.open_workbook(path + file_name)
	sh = book.sheet_by_name("Sheet1")
	list = []
	for i in range(1, sh.nrows):
		list.append(sh.row_values(i))
	return list

#------------------------------------------------------------------
# time:   2018-1-12
# author: hao
#    读取多义词搭配词典， 词典每行3词， 分别为， 形容词， 名词， 分数
#    	eg:  小 房间 -1
#            大 气味 -1
#            ...
#
#    para_in : path
#    para_in : file_name
#    para_out: [('小', '房间', -1.0), ('大', '气味', -1.0), ('不好', '通风', -1.0)]
#-------------------------------------------------------------------
def load_multi_meaning_word_dic(path, file_name):
	def __get_dic__():
		__dic__ = []
		return __dic__

	dic_list = []
	dic = __get_dic__()
	with open(path + file_name, 'r', encoding='UTF-8') as f:
		line = f.readline()
		while len(line) > 0:
			li = line.split()
			dic.append(li[0])
			dic.append(li[1])
			dic.append(float(li[2]))
			tmp = tuple(dic)
			dic_list.append(tmp)
			line = f.readline()
			dic = __get_dic__()
	return dic_list
