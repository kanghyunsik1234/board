import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

db.create_all()


@app.route("/")
def index():
    # myapp.db에 있는 모든 레코드를 불러와
    # 보여준다
    # SELECT * FROM posts;
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/create")
def create():
    title = request.args.get('title')
    content = request.args.get('content')
    post = Post(title = title, content = content)
    db.session.add(post)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    #1. 수정하려고 하는 레코드를 선택해서
    post = Post.query.get(id)
    #2. 수정을 하고
    #post.title = "수정하셈"
    #3. 커밋한다.
    #post.content = "수정하셈"
    return render_template("edit.html", post=post)
    
@app.route("/update/<int:id>")
def update(id):
    #1. 수정하려고 하는 레코드를 선택해서
    post = Post.query.get(id)
    #2. 수정을 하고
    post.title = request.args.get('title')
    #3. 커밋한다.
    post.content = request.args.get('content')
    #return render_template("edit.html", post=post)
    
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):  
    #1. 지우려하고 하는 레코드를 선택
    post = Post.query.get(id)
    #2. 지우기
    db.session.delete(post)
    #3. 확정하고 db에 반영
    db.session.commit()
    return redirect("/")
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug = True)