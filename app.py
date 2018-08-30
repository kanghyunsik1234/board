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


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug = True)