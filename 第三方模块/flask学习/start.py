from flask import Flask, render_template, redirect, url_for, request, make_response

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def hello():
    return "Hello Flask!"


@app.route("/string/<user>")
def param_string(user):
    return user


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # request.cookies.get("username") 获取cookie
        if request.form['username'] == 'admin' and request.form['password'] == '123456':
            # return render_template("index.html", admin="admin")
            resp = make_response(render_template("index.html", admin="admin"))
            resp.set_cookie('username', 'the username')  # 发送cookie给客户端
            return resp


@app.route("/index")
def index():
    # return redirect("/login")      # 重定向
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(port=9527, debug=True)
