from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "movie.db")


def connect_db():
    pass


@app.route('/')
def home():
    return redirect(url_for('index'))  # code= 301永久性重定向 302暂时性重定向


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/movie')
def movie():
    data_list = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        data_list.append(item)
    cur.close()
    conn.close()
    return render_template("movie.html", movies=data_list)


@app.route('/score')
def score():
    score_list, score_num = [], []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score_list.append(str(item[0]))
        score_num.append(item[1])
    cur.close()
    conn.close()
    return render_template("score.html", score=score_list, num=score_num)


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return redirect("http://www.baidu.com")


if __name__ == '__main__':
    app.run()
