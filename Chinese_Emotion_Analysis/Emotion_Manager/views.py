import re
import jieba
from django.http import HttpResponse
from django.shortcuts import render
import Emotion_Manager.CEA_LIB.chinese_emotion_analysis as CEA
# Create your views here.


def index(request):
    return render(request, 'Emotion_Manager/index.html', {})


def calculate_accuracy(request):
    # CEA.compare_test()
    print(request.GET['query'])
    text = request.GET['query']
    text = ''.join(text.split())
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）～-]+", "", text)
    pos_list = jieba.cut(text, cut_all=False)
    res = CEA.application(CEA.transfer_text_to_moto(list(pos_list)))

    return HttpResponse(res)


def dict_result(request):
    pass