from django.db import models


class stock_list(models.Model):
    """A股股票基础信息"""

    code = models.CharField(verbose_name="股票代码", primary_key=True, max_length=8)
    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    area = models.CharField(verbose_name="地区", max_length=32, blank=True, null=True)
    industry = models.CharField(verbose_name="所属板块", max_length=32, blank=True, null=True)
    abbr = models.CharField(verbose_name="市场缩写", max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stock_list"


class stock_spot(models.Model):
    """东财A股实时行情数据"""

    code = models.CharField(verbose_name="股票代码", primary_key=True, max_length=8)
    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    latest_price = models.FloatField(verbose_name="最新价", blank=True, null=True)
    change_rate = models.FloatField(verbose_name="涨跌幅", blank=True, null=True)
    change_amount = models.FloatField(verbose_name="涨跌额", blank=True, null=True)
    volume = models.FloatField(verbose_name="成交量", blank=True, null=True)
    turnover = models.FloatField(verbose_name="成交额", blank=True, null=True)
    amplitude = models.FloatField(verbose_name="振幅", blank=True, null=True)
    highest = models.FloatField(verbose_name="最高价", blank=True, null=True)
    lowest = models.FloatField(verbose_name="最低价", blank=True, null=True)
    today_open = models.FloatField(verbose_name="今开", blank=True, null=True)
    prev_close = models.FloatField(verbose_name="昨收", blank=True, null=True)
    volume_ratio = models.FloatField(verbose_name="量比", blank=True, null=True)
    turnover_ratio = models.FloatField(verbose_name="换手率", blank=True, null=True)
    price_earnings = models.FloatField(verbose_name="市盈率", blank=True, null=True)
    price_book = models.FloatField(verbose_name="市净率", blank=True, null=True)
    total_value = models.FloatField(verbose_name="总市值", blank=True, null=True)
    circulation_value = models.FloatField(verbose_name="流通市值", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stock_spot"


class stock_data(models.Model):
    """A股日频率数据-东方财富"""

    date = models.DateField(verbose_name="日期", blank=True, null=True)
    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    open = models.FloatField(verbose_name="开盘价", blank=True, null=True)
    close = models.FloatField(verbose_name="收盘价", blank=True, null=True)
    highest = models.FloatField(verbose_name="最高价", blank=True, null=True)
    lowest = models.FloatField(verbose_name="最低价", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stock_data"
        unique_together = (("date", "code"),)


class weibo_report(models.Model):
    """微博舆情报告"""

    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    rate = models.FloatField(verbose_name="指数", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "weibo_report"


class baidu_search(models.Model):
    """百度股市通-热搜股票"""

    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    state = models.FloatField(verbose_name="涨跌幅", blank=True, null=True)
    industry = models.CharField(verbose_name="所属板块", max_length=32, blank=True, null=True)
    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    price = models.FloatField(verbose_name="现价", blank=True, null=True)
    abbr = models.CharField(verbose_name="市场缩写", max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "baidu_search"


class em_rank(models.Model):
    """东方财富-个股人气榜"""

    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    price = models.FloatField(verbose_name="最新价", blank=True, null=True)
    state = models.FloatField(verbose_name="涨跌幅", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "em_rank"


class xq_tweet(models.Model):
    """雪球-沪深股市-热度排行榜-讨论排行榜"""

    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    name = models.CharField(verbose_name="股票名称", max_length=32, blank=True, null=True)
    follow = models.IntegerField(verbose_name="关注", blank=True, null=True)
    price = models.FloatField(verbose_name="最新价", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "xq_tweet"


class baidu_vote(models.Model):
    """百度股市通-A股或指数-股评-投票"""

    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    period = models.CharField(verbose_name="周期", max_length=8, blank=True, null=True)
    bullish = models.IntegerField(verbose_name="看涨", blank=True, null=True)
    bearish = models.IntegerField(verbose_name="看跌", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "baidu_vote"


class rank_detail(models.Model):
    """东方财富-个股人气榜-历史趋势及粉丝特征"""

    date = models.DateField(verbose_name="日期", blank=True, null=True)
    rank = models.IntegerField(verbose_name="排名", blank=True, null=True)
    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    new_fans = models.FloatField(verbose_name="新晋粉丝", blank=True, null=True)
    loyal_fans = models.FloatField(verbose_name="铁杆粉丝", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rank_detail"


class stock_news(models.Model):
    """新闻-个股新闻"""

    code = models.CharField(verbose_name="股票代码", max_length=8, blank=True, null=True)
    title = models.CharField(verbose_name="新闻标题", max_length=128, blank=True, null=True)
    source = models.CharField(verbose_name="文章来源", max_length=32, blank=True, null=True)
    link = models.URLField(verbose_name="新闻链接", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stock_news"
