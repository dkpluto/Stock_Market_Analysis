/* 处理主页的数据与样式 */
// 榜单涨跌幅样式调整
$(function () {
  $('.set_color').each(function () {
    var n = $(this).html()
    var formatted = Number(n).toFixed(2) // 格式化数字
    var colorStr = n > 0 ? 'red' : 'green'
    var sign = n > 0 ? '+' : ''
    $(this)
      .css('color', colorStr)
      .html(sign + formatted + '%')
  })
})

var token = $('[name="csrfmiddlewaretoken"]').val() // 获取csrf的token值
var heatmap = echarts.init(document.getElementById('heatmap')) // 微博舆情报告热力图

$.ajax({
  url: '/', // 请求url
  type: 'POST', // 请求方法
  data: { type: 'heatmap', csrfmiddlewaretoken: token },
  dataType: 'json', // 响应类型
})
  .done(function (data) {
    data = JSON.parse(data)
    var source = []
    for (var i = 0; i < data.length; i++) {
      source.push({
        name: data[i].fields.name,
        value: [(data[i].pk - 1) % 10, Math.floor((data[i].pk - 1) / 10), data[i].fields.rate],
      })
    }
    var option = {
      title: {
        text: '微博舆情报告',
        left: 'center',
        triggerEvent: true,
        textStyle: {
          fontSize: 25, // 设置热力图标题的文字大小为18像素
        },
      },
      responsive: true, // 自适应容器
      grid: {
        left: '0%',
        right: '0%',
        height: '50%',
      },
      xAxis: {
        show: false,
        type: 'category',
      },
      yAxis: {
        show: false,
        type: 'category',
      },
      visualMap: {
        min: -5,
        max: 5,
        show: false,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '10%',
        type: 'piecewise', // 分段视觉映射
        pieces: [
          { lte: -3, color: '#de2623' }, // (-∞,-3]
          { gt: -3, lte: -1, color: '#e34b4a' }, // (-3,-1]
          { gt: -1, lt: 0, color: '#e77675' }, // (-1,0)
          { gte: 0, lte: 0, color: '#e9a4a3' }, // [0,0]
          { gt: 0, lt: 1, color: '#8ebe87' }, // (0,1)
          { gte: 1, lt: 3, color: '#62aa54' }, // [1,3)
          { gte: 3, color: '#3e9423' }, // [3,+∞)
        ],
      },
      series: [
        {
          name: '股票涨跌幅',
          type: 'heatmap',
          data: source.map(function (item) {
            return item.value
          }),
          label: {
            show: true,
            fontSize: 16, // 设置文字的大小为12像素
            formatter: function (params) {
              var index = params.dataIndex // 获取数据索引
              var name = source[index].name // 获取股票名称
              var value = source[index].value[2] // 获取涨跌幅
              var sign = value > 0 ? '+' : ''
              return name + '\n' + sign + value + '%' // 返回文本内容
            },
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    }
    // 使用配置项和数据显示图表
    heatmap.setOption(option)
  })
  .fail(function (xhr, status, error) {
    alert(error)
  })

// 绑定点击事件
heatmap.on('click', function (params) {
  if (params.componentType === 'title') {
    alert(
      '该表格展示的是在对应的时间期限内，个股在微博讨论中的人气排行指数。红色颜色越深，表明该股票讨论热度越高，其当前的涨幅更大。绿色颜色越深，表明该股票讨论的热度越低，其当前的跌幅更大。'
    )
  }
})
