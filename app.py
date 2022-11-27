from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertisements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())


    def __repr__(self):
        return '<Advertisement %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    adv = Advertisement.query.order_by(Advertisement.date.desc()).all()
    return render_template("posts.html", adv=adv)


@app.route('/posts/<int:id>')
def post_detail(id):
    adv = Advertisement.query.get(id)
    return render_template("post_detail.html", adv=adv)


@app.route("/posts/<int:id>/delete")
def post_delete(id):
    adv = Advertisement.query.get_or_404(id)

    try:
        db.session.delete(adv)
        db.session.commit()
        return redirect('/posts')
    except:
        "При удалении статьи произошла ошибка"



@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_advertisement(id):
    adv = Advertisement.query.get(id)
    if request.method == "POST":
        adv.name = request.form['name']
        adv.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при редактировании объявления"
    else:

        return render_template("post_update.html", adv=adv)


@app.route('/create', methods=['POST', 'GET'])
def create_advertisement():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']

        adv = Advertisement(name=name, description=description)

        try:
            db.session.add(adv)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при добавлении объявления"
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
