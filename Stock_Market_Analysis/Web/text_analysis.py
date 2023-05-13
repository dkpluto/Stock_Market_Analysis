import jieba
import jieba.analyse
import json
import requests

# from snownlp import SnowNLP


class TextModel:
    """文本情感分析"""

    def __init__(self, path="Stock_Market_Analysis/data/"):
        jieba.load_userdict(path + "user_dict.txt")  # 加载用户词典
        self.stopwords = set(open(path + "stop_words.txt", encoding="utf-8").read().split())  # 加载停用词词典

    # 使用SnowNLP进行情感分析
    # def analyze(self, text):
    #     text_analyze = " ".join([w for w in jieba.lcut(text) if w not in self.stopwords])  # 去除停用词
    #     senti = SnowNLP(text_analyze).sentiments  # 情感分析
    #     print(senti, text_analyze)
    #     senti = (senti > 0.6) - (senti < 0.4)  # (0,0.4)消极 [0.4,0.6]中性 (0.6,1)积极
    #     return senti

    # 使用百度智能云-情感倾向分析
    def analyze(self, text):
        url = ""

        payload = json.dumps({"text": text})
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload).json()
        # 情感极性分类结果(0:负向，1:中性，2:正向),分类的置信度(取值范围[0,1]),属于积极类别的概率(取值范围[0,1]),属于消极类别的概率(取值范围[0,1])
        return response["items"][0]["sentiment"], response["items"][0]["confidence"], response["items"][0]["positive_prob"], response["items"][0]["negative_prob"]

    # 基于TextRank算法的关键词抽取
    def textrank(self, text):
        stop_n = set(["市场", "板块", "公司", "大盘", "股票", "个股"])
        arr = jieba.analyse.textrank(text, topK=10, withWeight=True)
        arr = [[*x] for x in arr if x[0] not in stop_n]
        return sorted(arr, key=lambda x: x[1], reverse=1)
