request对象
    method：当前请求方法（POST，GET等）
    url：当前链接地址
    path：当前链接的路径
    environ：潜在的WSGI环境
    headers：传入的请求头作为字典类对象
    data：包含传入的请求数据作为
    args：请求链接中的参数（GET参数），解析后
    form：form提交中的参数，解析后
    values：args和forms的集合
    json：json格式的body数据，解析后
    cookies：cookie读取

response = make_response(render_template(index.html))
方法
    status：响应状态
    headers：响应头，设置http字段
    set_cookie：设置一个cookie