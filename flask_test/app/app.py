from flask import Flask, render_template, request, url_for ,Response ,abort # クエストリングを受け取るモジュール
from werkzeug.utils import redirect

from flask_test.model.models import main
from flask_test.model.database import db_session
from datetime import datetime
from flask_login import login_user, logout_user, LoginManager, UserMixin, login_required
from collections import defaultdict
#Flaskオブジェクトの生成
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cfb33786023cc152019e747a051f73c6'
login_manager = LoginManager()
login_manager.init_app(app)

app_list = ['todo','dentaku','vending_machine']
#Todoリストの最初の画面
# @app.route("/")
# def hello():
#     return render_template("selection_app.html")

#Todoリストの実際の行う画面
@app.route("/todo")
@app.route("/todo",methods=["post"])
@login_required
def todo():
    all_todo = main.query.all()
    return render_template("todo.html", name='岩本海斗', all_todo=all_todo)

@app.route("/add",methods=["post"])
@login_required
def add():
    title = request.form["title"]
    deadline = request.form["deadline"]
    content = main(title, deadline=deadline)
    db_session.add(content)
    db_session.commit()
    return todo()


@app.route("/delete",methods=["post"])
@login_required
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = main.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return todo()

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password"),
    3: User(3, "awamuramasakazu", "sensei")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/home')
def home():
    return Response("home: <a href='/login/'>Login</a> <a href='/protected/'>Protected</a> <a href='/logout/'>Logout</a>")

# ログインしないと表示されないパス
@app.route('/protected/')
@login_required
def protected():
    return Response('''
    protected<br />
    <a href="/logout/">logout</a>
    ''')

# ログインパス
#@app.route('/')
@app.route('/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):

        
        # ユーザーチェック
        while True :
            if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
                # ユーザーが存在した場合はログイン
                login_user(users.get(user_check[request.form["username"]]["id"]))
                if request.form["username"] != 'awamuramasakazu':
                     return todo()
                else:
                    return render_template("Thankyou.html")

    else:
        return render_template("login.html")

# ログアウトパス
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return Response('''
    logout success!<br />
    <a href="/login/">login</a>
    ''')
if __name__ == "__main__":
    app.run(debug=True)
