/* 处理个股详情页面的数据与样式 */
var code = $('#kchart').attr('code') // 请求的股票代码
var abbr = $('#kchart').attr('abbr') // 请求的交易所缩写
var token = $('[name="csrfmiddlewaretoken"]').val() // 获取csrf的token值

// 信息面板样式调整
var change_amount = $('#change_amount').html()
var colorStr = Number(change_amount) > 0 ? 'red' : 'green'
Number(change_amount) > 0 ? $('#chevron-down').hide() : $('#chevron-up').hide()
$('#latest_price').css('color', colorStr)
$('#change_rate').css('color', colorStr)
$('#change_amount').css('color', colorStr)
var volume = $('#volume').html()
$('#volume').html((Number(volume) / 10000).toFixed(2) + '万')
var turnover = $('#turnover').html()
$('#turnover').html((Number(turnover) / 100000000).toFixed(2) + '亿')
var total_value = $('#total_value').html()
$('#total_value').html((Number(total_value) / 100000000).toFixed(2) + '亿')
var circulation_value = $('#circulation_value').html()
$('#circulation_value').html((Number(circulation_value) / 100000000).toFixed(2) + '亿')

// 获取百度股评投票数据
$.ajax({
  url: '/detail',
  type: 'POST',
  data: { code: code, type: 'vote', csrfmiddlewaretoken: token },
  dataType: 'json',
})
  .done(function (data) {
    data = JSON.parse(data)
    title = document.getElementById('titledom')
    bullish = data[0].fields.bullish
    bearish = data[0].fields.bearish
    // 标题修改
    if (bullish >= bearish) title.innerHTML += '：<font class="text-danger">看涨📈</font>'
    else title.innerHTML += '：<font class="text-success">看跌📉</font>'

    //看涨看跌比例
    up_prog = document.getElementById('up_prog')
    up_rate = ((bullish / (bullish + bearish)) * 100).toFixed(2)
    up_prog.innerText = String(up_rate) + '%'
    up_prog.style.width = String(up_rate) + '%'

    down_prog = document.getElementById('down_prog')
    down_rate = ((bearish / (bullish + bearish)) * 100).toFixed(2)
    down_prog.innerText = String(down_rate) + '%'
    down_prog.style.width = String(down_rate) + '%'
  })
  .fail(function (xhr, status, error) {
    alert(error)
  })

// K线图样式
var chart = echarts.init(document.getElementById('kchart'))
option = {
  title: {
    text: '行情数据',
    left: '2%',
    textStyle: {
      fontSize: 20,
    },
  },
  xAxis: {
    type: 'category',
    data: [],
  },
  yAxis: [
    {
      name: '价格',
      type: 'value',
      scale: true,
    },
    {
      name: '排名',
      type: 'value',
      scale: true,
      inverse: true,
      nameLocation: 'start',
    },
  ],
  series: [
    {
      name: '日K线图',
      type: 'candlestick',
      data: [],
      yAxisIndex: 0,
    },
    {
      name: '人气排名',
      type: 'line',
      data: [],
      yAxisIndex: 1,
      // smooth: true,
    },
  ],
  legend: {
    data: ['日K线图', '人气排名'],
    selected: {
      日K线图: true, // 设置K线图默认显示
      人气排名: true, // 设置折线图默认显示
    },
  },
  tooltip: {
    trigger: 'axis',
    formatter: function (params) {
      var res = params[0].name + '<br/>'
      if (params[0] && params[1]) {
        res += '开盘 : ' + params[0].data[1] + '<br/>'
        res += '收盘 : ' + params[0].data[2] + '<br/>'
        res += '最低 : ' + params[0].data[3] + '<br/>'
        res += '最高 : ' + params[0].data[4] + '<br/>'
        res += '排名 : ' + params[1].data + '<br/>'
      } else if (params[0].seriesName == '日K线图') {
        res += '开盘 : ' + params[0].data[1] + '<br/>'
        res += '收盘 : ' + params[0].data[2] + '<br/>'
        res += '最低 : ' + params[0].data[3] + '<br/>'
        res += '最高 : ' + params[0].data[4] + '<br/>'
      } else if (params[0].seriesName == '人气排名') {
        res += '排名 : ' + params[0].data + '<br/>'
      }
      return res
    },
  },
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 100,
    },
    {
      show: true,
      type: 'slider',
      y: '90%',
      start: 50,
      end: 100,
    },
  ],
}
chart.setOption(option)
window.addEventListener('resize', function () {
  chart.resize()
})
chart.showLoading()

// K线图数据获取
$.ajax({
  url: '/detail',
  type: 'POST',
  data: { code: code, type: 'kchart', csrfmiddlewaretoken: token },
  dataType: 'json',
})
  .done(function (data) {
    data = JSON.parse(data)
    var dates = []
    var prices = []
    for (var i = 0; i < data.length; i++) {
      dates.push(data[i].fields.date)
      prices.push([data[i].fields.open, data[i].fields.close, data[i].fields.lowest, data[i].fields.highest])
    }
    // 将提取的数据赋值给配置项
    option.xAxis.data = dates
    option.series[0].data = prices
    chart.hideLoading()
    chart.setOption(option)
    // 进行折线图数据更新
    lchart(dates)
  })
  .fail(function (xhr, status, error) {
    alert(error)
  })

// 折线图数据获取,当K线图更新完后再更新折线图
function lchart(k_dates) {
  $.ajax({
    url: '/detail',
    type: 'POST',
    data: { code: abbr + code, type: 'lchart', csrfmiddlewaretoken: token },
    dataType: 'json',
  })
    .done(function (data) {
      data = JSON.parse(data)
      var rank = []
      var dates = []
      var k_dates_obj = {}
      for (var i = 0; i < k_dates.length; i++) {
        k_dates_obj[k_dates[i]] = i // 将日期作为键，索引作为值
      }
      for (var i = 0; i < data.length; i++) {
        if (k_dates_obj.hasOwnProperty(data[i].fields.date)) {
          rank.push(data[i].fields.rank)
          dates.push(data[i].fields.date)
        }
      }
      option.series[1].data = rank
      chart.setOption(option)
    })
    .fail(function (xhr, status, error) {
      alert(error)
    })
}
