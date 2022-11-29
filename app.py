from flask import Flask, render_template, url_for, request, redirect, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertisements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f5a2b4f9c5cb15099b91a4252cbe8865fbb67df5'
db = SQLAlchemy(app)


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    session_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Advertisement %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template("index.html")




@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM advertisement"))
        for row in result:
            date_db = datetime.strptime(row["date"], '%Y-%m-%d %H:%M:%S.%f')
            date_system = datetime.utcnow() - timedelta(minutes=5)
            if date_system > date_db:
                row_id = row["id"]
                Advertisement.query.filter_by(id=row_id).delete()
    db.session.commit()

    adv = Advertisement.query.filter_by(session_number = session['visits'])
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
        session_number = session['visits']
        adv = Advertisement(name=name, description=description, session_number=session_number)

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
