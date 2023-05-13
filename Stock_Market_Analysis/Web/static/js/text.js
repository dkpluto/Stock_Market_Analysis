/* 处理文本分析页面的数据与样式 */
var token = $('[name="csrfmiddlewaretoken"]').val() // 获取csrf的token值

// 提交按钮点击事件
$('#submit-button').click(function () {
  var text = $('#text-input').val()
  if (text.length > 2048) {
    alert('文本长度不能超过2048!') // 接口最多支持2048长度的文本分析
  } else {
    $.ajax({
      url: '/text', // 请求url
      type: 'POST', // 请求方法
      data: { text: text, csrfmiddlewaretoken: token },
      dataType: 'json', // 响应类型
    })
      .done(function (data) {
        $('#result').empty()

        // 添加情感分析
        if (data.senti == 0) {
          $('#result').append('<h4>情感倾向分析：<font class="text-success">' + '消极' + '</font></h4>')
        } else if (data.senti == 1) {
          $('#result').append('<h4>情感倾向分析：中立/无关</h4>')
        } else if (data.senti == 2) {
          $('#result').append('<h4>情感倾向分析：<font class="text-danger">' + '积极' + '</font></h4>')
        }

        // 添加分析条
        $('#result').append(
          '\
      <h6>积极</h6>\
      <div class="progress" style="height:20px;">\
          <div class="progress-bar progress-bar-striped bg-danger progress-bar-animated" role="progressbar" style="width:' +
            (data.posi * 100).toFixed(2) +
            '%">' +
            (data.posi * 100).toFixed(2) +
            '%</div>\
      </div>\
      <h6>消极</h6>\
      <div class="progress" style="height:20px;">\
          <div class="progress-bar progress-bar-striped bg-success progress-bar-animated" role="progressbar" style="width:' +
            (data.nega * 100).toFixed(2) +
            '%">' +
            (data.nega * 100).toFixed(2) +
            '%</div>\
      </div>\
      <h6>置信度</h6>\
      <div class="progress" style="height:20px;">\
          <div class="progress-bar progress-bar-striped bg-secondary progress-bar-animated" role="progressbar" style="width:' +
            (data.confi * 100).toFixed(2) +
            '%">' +
            (data.confi * 100).toFixed(2) +
            '%</div>\
      </div>\
      '
        )

        // 添加关键词
        if (data.word_list.length > 0) {
          $('#result').append('<hr><h4>TextRank关键词提取：</h4>')
          for (var i = 0; i < data.word_list.length; i++) {
            result.innerHTML += '<p>' + data.word_list[i][0] + ' ' + data.word_list[i][1].toFixed(2) + '</p>'
          }
        }
      })
      .fail(function (xhr, status, error) {
        alert(error)
      })
  }
})
