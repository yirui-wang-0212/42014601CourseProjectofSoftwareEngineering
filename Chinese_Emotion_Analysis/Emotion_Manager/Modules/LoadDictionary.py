import xlrd

#通用 读取一个文本词典 返回一个内存词典, 其中所有词的 score 一样
#针对文本词典只含有词语没有分数的情况
###########################################################
def load_dic(path, fileName, score):                       #
	wordDict = {}                                         #
	with open(path+fileName,encoding="utf-8") as fin:    #
		for line in fin:
			word = line.strip()
			wordDict[word] = score
	return wordDict


#传入 上面 函数构造的词典, 向其中附加 另一 score 的 词语
def append_dic(wordDict, path, fileName, score):
	with open(path+fileName,encoding="utf-8") as fin:
		for line in fin:
			word = line.strip()
			wordDict[word] = score
###########################################################


#知网词典 程度副词 词典的读取与构造
###########################################################
def __get_score__(x):
	return {0:0.5, 1:0.8 , 2:1.2, 3:1.25, 4:1.5, 5:2}.get(x,0)

def load_ext_dic(path, fileName):
	extent_dic = {}
	for i in range(6):
		score = __get_score__(i)
		with open(path+fileName + str(i + 1) + ".txt",encoding='utf-8') as fin :
			for line in fin:
				word = line.strip()
				extent_dic[word]= score
	return extent_dic

############################################################

#读取 txt 文件, 每一行包含两项 , 一项是词语, 一项是词语的极值
############################################################
def load_extreme_dic(path, fileName):
	__dic__ = {}
	with open(path + fileName,'r',encoding="UTF-8") as f:
		line = f.readline()
		while len(line) > 0:
			l = line.split()
			__dic__[l[0]] = float(l[1])
			line = f.readline()
		return __dic__



#读取 excel 文件 : xlsx 文件, 构建情感词词典
############################################################
def read_xlsx_file(path, fileName):
	book = xlrd.open_workbook(path + fileName)
	sh = book.sheet_by_name("Sheet1")
	list = []
	for i in range(1, sh.nrows):
		list.append(sh.row_values(i))
	return list

