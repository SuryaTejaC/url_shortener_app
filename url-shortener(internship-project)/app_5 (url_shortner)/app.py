from flask import Flask, render_template, request,redirect,session
import random
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import validators

app = Flask(__name__)



###########sqlalchemy configuration#################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
####################################################

################create model########################

class Url(db.Model):
    __tablename__='URL-shortener'
    id = db.Column(db.Integer, primary_key = True)
    original_url = db.Column(db.String(128))
    shorten_url = db.Column(db.String(128))

    def __init__(self,original_url,shorten_url):
        self.original_url=original_url
        self.shorten_url=shorten_url
    def __repr__(self):
        return "{}".format(self.shorten_url)


####################################################
@app.route('/')
def home_get():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def home_post():
    if request.method == 'POST':
        original_url = request.form.get('in_1')
        shorten_url = random.randint(1000, 9999)

        new_url=Url(original_url,shorten_url)# created a object for class 'Url' to which we passed original url, shorten url.
        db.session.add(new_url)
        db.session.commit()

        urls=Url.query.all()

    return render_template('index.html', urls=new_url.shorten_url)
    

@app.route('/history')
def history_get():
    history=Url.query.all()
    return render_template('history.html',history=history)

@app.route('/sh/<urls>')
def redirect_to_url(urls):
        new_url=Url.query.filter(urls == urls).first_or_404()
        return redirect(new_url.original_url)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Url.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/history')
    except:
        return 'There was an error while deleting that task'




if __name__ == "__main__":
    app.run(debug=True)