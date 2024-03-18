from flask import Flask, make_response, redirect, url_for, request, session, render_template_string
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'kfx7'


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    print(name)
    if name is None:
        name = request.cookies.get('name', default='Human')
        response = '<h1> Hello, %s!</h1>' % escape(name)
        print(response)
        if "login_in" in session:
            response += '[Authenticated]'
            print(response)
        else:
            response += '[Not Authenticated]'
        return response


@app.route("/set/<name>")
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    session['login_in'] = True
    return response


@app.route('/foo')
def foo():
    return '<h1> Foo page </h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1> Foo page </h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect('target')
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return render_template_string("""  # 返回一个字符串模板渲染后的结果
            <h1> A very long post </h1>  # 标题为 "A very long post"
            <div class="body">{{ post_body }}</div>  # 正文为 post_body 参数传入的值，被包裹在 div 标签中
            <button id="load">Load More</button>  # 按钮的 id 为 "load"，显示文本为 "Load More"
            <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>  # 引入 jQuery 库
            <script type="text/javascript">
                var page = 1;  # 定义变量 page，初始值为 1
                var maxPages = {{ max_pages }};  # 定义变量 maxPages，值为传入的 max_pages 参数（在 {{ }} 中）
                $('#load').click(function() {  # 为 id 为 "load" 的按钮绑定点击事件
                    if (page <= maxPages) {  # 如果当前页数小于等于最大页数
                        $.ajax({  # 发送 AJAX 请求
                            url: '/more?page=' + page,  # 请求 URL，带上当前页数作为参数
                            type: 'get',  # 请求类型为 "GET"
                            success: function(data){  # 请求成功后执行以下函数
                                $('.body').append(data);  # 将请求返回的内容添加到正文中
                                page++;  # 增加页数
                            }
                        });
                    } else {  # 如果当前页数大于最大页数
                        $('#load').hide();  # 隐藏按钮
                    }
                });
            </script>
        """, post_body=post_body, max_pages=10)  # 将 post_body 和 max_pages 参数传入字符串模板并渲染


@app.route("/more")
def load_post():
    return generate_lorem_ipsum(n=1)


if __name__ == '__main__':
    app.run(debug=True)
