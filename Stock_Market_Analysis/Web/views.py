from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from Web import models, data_update, text_analysis


def home(request):
    """主页视图"""
    if request.method == "GET":
        # 三个榜单数据
        baidu_list = models.baidu_search.objects.all()
        em_list = models.em_rank.objects.all()
        xq_tweet = models.xq_tweet.objects.all()
        return render(request, "home.html", {"em_list": em_list[:10], "baidu_list": baidu_list[:10], "xq_tweet": xq_tweet[:10]})
    else:
        # 热力图数据返回
        if request.POST.get("type") == "heatmap":
            data_list = serializers.serialize("json", models.weibo_report.objects.all())
            return JsonResponse(data=data_list, safe=False)


def detail(request):
    """个股详情视图"""
    if request.method == "GET":
        target = request.GET.get("target")
        # 没有数据跳转到搜索界面
        if not target:
            return render(request, "detail_search.html")
        # 根据数据库中的现存股票代码和名称判断搜索是否合法
        try:
            res = models.stock_list.objects.get(Q(code=target) | Q(name=target))
            code = res.code  # 股票代码
            abbr = res.abbr  # 交易所缩写
        except:
            return render(request, "404.html", {"target": target})
        # 更新新闻数据
        data_update.update_stock_news(symbol=code)
        stock_spot = models.stock_spot.objects.get(code=code)
        # 信息面板数据
        stock_news = models.stock_news.objects.filter(code=code)
        return render(request, "detail.html", {"code": code, "abbr": abbr, "stock_spot": stock_spot, "stock_news": stock_news})
    else:
        # 请求K线图数据
        code = request.POST.get("code")
        if request.POST.get("type") == "kchart":
            data_update.update_stock_data(symbol=code)
            data_list = serializers.serialize("json", models.stock_data.objects.filter(code=code))
        # 请求百度股评数据
        elif request.POST.get("type") == "vote":
            data_update.update_baidu_vote(symbol=code)
            data_list = serializers.serialize("json", models.baidu_vote.objects.filter(code=code))
        # 请求折线图数据
        elif request.POST.get("type") == "lchart":
            data_update.update_rank_detail(symbol=code)
            data_list = serializers.serialize("json", models.rank_detail.objects.filter(code=code))
        return JsonResponse(data=data_list, safe=False)


def text(request):
    """文本分析视图"""
    if request.method == "GET":
        return render(request, "text.html")
    else:
        # 对传入文本进行情感分析并返回数据
        text = request.POST.get("text")
        text_ana = text_analysis.TextModel()
        senti, confi, posi, nega = text_ana.analyze(text)
        word_list = text_ana.textrank(text)
        data_list = {"senti": senti, "confi": confi, "posi": posi, "nega": nega, "word_list": word_list}
        return JsonResponse(data=data_list, safe=False)
