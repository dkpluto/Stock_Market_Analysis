import pymysql
import akshare as ak
import tushare as ts
from datetime import datetime, timedelta

today = datetime.today().strftime("%Y%m%d")
prev_month = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")


class DataBase(object):
    """数据库类"""

    def __init__(
        self,
        host="",
        port=3306,
        user="",
        password="",
        database="",
    ):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset="utf8")
        self.cursor = self.conn.cursor()

    # insert delete update
    def execute(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # select fetchall
    def queryAll(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    # select fetchone
    def queryOne(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


def update_stock_list():
    """更新A股股票基础信息"""
    with DataBase() as db:
        db.execute("truncate table stock_list", None)
        pro = ts.pro_api("")  # 使用tushare更新
        data_list = pro.stock_basic(exchange="", list_status="L", fields="ts_code,symbol,name,area,industry,list_date").values
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into stock_list(code,name,area,industry,abbr) values(%s,%s,%s,%s,%s)",
                [data[1], data[2], data[3], data[4], data[0][-2:]],
            )
    print("更新完成")


def update_stock_spot():
    """东财A股实时行情数据 定时更新"""
    with DataBase() as db:
        db.execute("truncate table stock_spot", None)
        data_list = ak.stock_zh_a_spot_em()
        data_list = data_list.dropna(axis=0, how="any").values  # 删除有空值的行,有空值代表可能已退市
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into stock_spot(code,name,latest_price,change_rate,change_amount,volume,turnover,amplitude,highest,lowest,today_open,prev_close,volume_ratio,turnover_ratio,price_earnings,price_book,total_value,circulation_value) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                [data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18]],
            )
    print("更新完成")


def update_stock_data(symbol: str = "000001"):
    """更新A股日频率数据-东方财富 仅更新代码为symbol的股票 更新三个月之内的数据 数据为后复权"""
    with DataBase() as db:
        # db.execute("truncate table stock_data", None)
        res = db.queryOne("select count(*) from stock_data where code=%s", [symbol])[0]  # 查询数据库中是否存在,动态更新
        if res == 0:
            data_list = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=prev_month, end_date=today, adjust="hfq").values
            print("数据长度:", len(data_list))
            for data in data_list:
                db.execute(
                    "insert into stock_data(date,code,open,close,highest,lowest) values(%s,%s,%s,%s,%s,%s)",
                    [data[0], symbol, data[1], data[2], data[3], data[4]],
                )
    print("更新完成")


def update_weibo_report(time_period="CNHOUR24"):
    """更新微博舆情报告 1天"""
    with DataBase() as db:
        db.execute("truncate table weibo_report", None)
        data_list = ak.stock_js_weibo_report(time_period=time_period).values
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into weibo_report(name,rate) values(%s,%s)",
                [data[0], data[1]],
            )
    print("更新完成")


def update_baidu_search(time="今日"):
    """更新百度股市通-热搜股票"""
    with DataBase() as db:
        db.execute("truncate table baidu_search", None)
        data_list = ak.stock_hot_search_baidu(symbol="A股", date=today, time=time).values
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into baidu_search(name,state,industry,code,price,abbr) values(%s,%s,%s,%s,%s,%s)",
                [data[0], data[1], data[2], data[3], data[4], data[5]],
            )
    print("更新完成")


def update_em_rank():
    """更新东方财富-个股人气榜"""
    with DataBase() as db:
        db.execute("truncate table em_rank", None)
        data_list = ak.stock_hot_rank_em().values
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into em_rank(code,name,price,state) values(%s,%s,%s,%s)",
                [data[1], data[2], data[3], data[4]],
            )
    print("更新完成")


def update_xq_tweet():
    """更新雪球-沪深股市-热度排行榜-讨论排行榜"""
    with DataBase() as db:
        db.execute("truncate table xq_tweet", None)
        data_list = ak.stock_hot_tweet_xq("最热门").values
        print("数据长度:", len(data_list))
        for data in data_list:
            db.execute(
                "insert into xq_tweet(code,name,follow,price) values(%s,%s,%s,%s)",
                [data[0], data[1], data[2], data[3]],
            )
    print("更新完成")


def update_baidu_vote(symbol: str = "000001"):
    """更新百度股市通-A股或指数-股评-投票 仅更新代码为symbol的股票"""
    with DataBase() as db:
        # db.execute("truncate table baidu_vote", None)
        res = db.queryOne("select count(*) from baidu_vote where code=%s", [symbol])[0]  # 查询数据库中是否存在,动态更新
        if res == 0:
            data_list = ak.stock_zh_vote_baidu(symbol=symbol, indicator="股票").values
            print("数据长度:", len(data_list))
            for data in data_list:
                db.execute(
                    "insert into baidu_vote(code,period,bullish,bearish) values(%s,%s,%s,%s)",
                    [symbol, data[0], data[1], data[2]],
                )
    print("更新完成")


def update_rank_detail(symbol: str = "SZ000001"):
    """更新东方财富-个股人气榜-历史趋势及粉丝特征 仅更新代码为symbol的股票 更新三个月之内的数据"""
    with DataBase() as db:
        # db.execute("truncate table rank_detail", None)
        res = db.queryOne("select count(*) from rank_detail where code=%s", [symbol])[0]  # 查询数据库中是否存在,动态更新
        if res == 0:
            data_list = ak.stock_hot_rank_detail_em(symbol=symbol).values
            print("数据长度:", len(data_list))
            for data in data_list:
                db.execute(
                    "insert into rank_detail(date,rank,code,new_fans,loyal_fans) values(%s,%s,%s,%s,%s)",
                    [data[0], data[1], data[2], data[3], data[4]],
                )
    print("更新完成")


def update_stock_news(symbol: str = "000001"):
    """更新新闻-个股新闻 最多10条"""
    with DataBase() as db:
        # db.execute("truncate table stock_news", None)
        res = db.queryOne("select count(*) from stock_news where code=%s", [symbol])[0]  # 查询数据库中是否存在,动态更新
        if res == 0:
            data_list = ak.stock_news_em(symbol=symbol).values
            print("数据长度:", len(data_list))
            for data in data_list[:10]:
                db.execute(
                    "insert into stock_news(code,title,source,link) values(%s,%s,%s,%s)",
                    [symbol, data[1], data[4], data[5]],
                )
    print("更新完成")


def update_database():
    """需要定期向数据库更新"""
    update_em_rank()
    update_baidu_search()
    update_xq_tweet()
    update_weibo_report()
    update_stock_spot()

    # 清理数据库过期数据
    with DataBase() as db:
        db.execute("truncate table stock_data", None)
        db.execute("truncate table rank_detail", None)
        db.execute("truncate table stock_news", None)
        db.execute("truncate table baidu_vote", None)


if __name__ == "__main__":
    update_database()
    print("welcome")
