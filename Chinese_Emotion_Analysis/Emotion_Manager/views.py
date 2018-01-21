# -*- encoding: utf-8 -*-
import re
import jieba
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import Emotion_Manager.CEA_LIB.chinese_emotion_analysis as CEA
from Emotion_Manager.Modules.main import getScoreFromString
# Create your views here.


def redirect_to_index(request):
    return HttpResponseRedirect('/index')


def index(request):
    return render(request, 'Emotion_Manager/index.html', {})


def calculate_accuracy(request):
    # CEA.compare_test()
    print(request.GET['query'])
    print(request.GET['type'])
    text = request.GET['query']
    type = request.GET['type']

    if type == 'NLP':
        text = ''.join(text.split())
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）～-]+", "", text)
        pos_list = jieba.cut(text, cut_all=False)
        res = CEA.application(CEA.transfer_text_to_moto(list(pos_list)))

        return HttpResponse(res)
    elif type == 'DIC':
        print(request.GET['dic'])
        dicType = request.GET['dic']
        score = getScoreFromString(text, int(dicType))
        return HttpResponse(score)


def dict_result(request):
    pass
