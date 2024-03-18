function bindEmailCaptchaClick(){
  $("#captcha-btn").click(function (event){
    // $this：代表的是当前按钮的jquery对象
    // captcha-btn 与 register。html文件一个id名为captcha-btn按钮绑定
    // 绑定 captcha-btn 按钮的点击事件。$("#captcha-btn") 使用 jQuery 选择器选中 ID 为 captcha-btn 的元素。
    var $this = $(this);

    /*将当前点击的按钮对象存储到 $this 变量中。$(this) 是 jQuery 提供的技巧，
    它将原生的 DOM 元素转化为 jQuery 对象，以便在后续操作中使用 jQuery 方法。*/
    event.preventDefault();
     // 阻止默认的事件
    var email = $("input[name='email']").val();
    //获取 name=email 的输入框的值。

    /*$.ajax({ ... }) 发起一个 Ajax 请求，使用 jQuery 的 ajax 方法。
  url: "/auth/captcha/email?email="+email, 设置请求的 URL，将用户输入的邮箱地址作为参数添加到 URL 中。
  method: "GET", 设置请求的 HTTP 方法为 GET。
  success: function (result){ ... }, 请求成功后执行的回调函数，接收返回的结果作为参数。
  fail: function (error){ ... } 请求失败后执行的回调函数，接收错误信息作为参数。
 */
    $.ajax({
      // http://127.0.0.1:500
      // /auth/captcha/email?email=xx@qq.com
      url: "/auth/captcha/email?email="+email,
      method: "GET",
      success: function (result){
        var code = result['code'];
        // auth.py中jsonify # RESTful API
        //   {code: 200/400/500, message: "", data: {}}
        if(code === 200){
          // code==200表示成功，无错误
          var countdown = 5;
          // 开始倒计时之前，就取消按钮的点击事件，即按钮不可点击
          $this.off("click");
          var timer = setInterval(function (){
            $this.text(countdown);
            countdown -= 1;
            // 倒计时结束的时候执行
            if(countdown <= 0){
              // 清掉定时器
              clearInterval(timer);
              // 将按钮的文字重新修改回来
              $this.text("获取验证码");
              // 重新绑定点击事件，为了让按钮再次可以点击
              bindEmailCaptchaClick();
            }
          }, 1000);
          // alert("邮箱验证码发送成功！");
        }else{
          alert(result['message']);
        }
      },
      fail: function (error){
        console.log(error);
      }
    })
  });
}


// 整个网页都加载完毕后再执行的
$(function (){
  bindEmailCaptchaClick();
});