import pickle

# 2.3 把选出的这些词作为特征（这就是选择了信息量丰富的特征）
def best_word_features(words, best_words):
    return dict([(word, True) for word in words if word in best_words])


best_words = []


def transfer_text_to_moto(data):
    best_words = pickle.load(open('Emotion_Manager/CEA_LIB/best_words.pkl', 'rb'))
    # def extract_features(data):
    #     feat = []
    #     for i in data:
    #         feat.append(best_word_features(i, best_words))
    #     return feat
    #
    # moto_features = extract_features(data)  # 把文本转化为特征表示的形式
    moto_features = best_word_features(data, best_words)

    return moto_features


# 6.2 对文本进行分类，给出概率值
def application(moto_features):
    global result
    clf = pickle.load(open('Emotion_Manager/CEA_LIB/classifier.pkl', 'rb'))  # 载入分类器
    pred = clf.prob_classify_many(moto_features)  # 该方法是计算分类概率值的
    for i in pred:
        result =i.prob('pos')
    return round(result * 100, 2)


if __name__ == '__main__':
    pass
    # best_words = pickle.load(open('best_words.pkl', 'rb'))
    # moto_features = transfer_text_to_moto()
    # application(moto_features)