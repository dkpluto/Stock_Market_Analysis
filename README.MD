# 量化舆情交易平台

本项目基于Django框架开发。使用akshare和tushare获取股票数据。使用jieba分词和百度智能云进行情感分析。使用MySQL存储数据，ECharts进行可视化展示。

## 文件目录

```
Stock_Market_Analysis
│  manage.py
│  
├─data
│      stop_words.txt                 	#停用词词典
│      user_dict.txt					#用户词典
│      
├─Stock_Market_Analysis
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │  
│  └─__pycache__
|
│          
└─Web
    │  admin.py
    │  apps.py							#app注册
    │  data_update.py					#数据获取与数据库更新
    │  models.py						#数据库配置
    │  tests.py
    │  text_analysis.py					#股评文本分析
    │  views.py							#视图
    │  __init__.py
    │  
    ├─migrations
    │  │  0001_initial.py
    │  │  __init__.py
    │  │  
    │  └─__pycache__
	|
    │          
    ├─static
    │  ├─css
    │  │      detail.css				#详情页面css
    │  │      global.css				#全局css
    │  │      home.css					#主页css
    │  │      
    │  ├─ico
    │  │      baidu.png					#百度图片
    │  │      eastmoney.png				#东方财富图片
    │  │      favicon.ico				#网站图标
    │  │      xq.png					#雪球图片
    │  │      
    │  └─js
    │          detail.js				#详情页面js
    │          home.js					#主页js
    │          text.js					#文本分析页面js
    │          
    ├─templates
    │      404.html						#404页面
    │      detail.html					#详情页面
    │      detail_search.html			#搜索页面
    │      home.html					#主页
    │      layout.html					#模板页面
    │      text.html					#文本分析页面
    │      
    └─__pycache__
```

