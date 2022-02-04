import os
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate
import random  
import string


app=Flask(__name__)

################### SQL Alchemy Configuration #####################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db) 

@app.before_first_request
def create_table():
    db.create_all()

###################################################################

##################### Create a Model ##############################

class Project(db.Model):
    __tablename__='url_shortner'
    id = db.Column(db.Integer, primary_key = True)
    org = db.Column(db.Text)
    short=db.Column(db.Text)
    

    def __init__(self,org,short):
        self.org = org
        self.short = short
    def __repr__(self):
        return f"{self.org} - {self.short}"

 #################################################################       

data={}

@app.route('/')
def home_get():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def home_post():
    n=5
    original_url = request.form.get('in_1')
    short_url = ''.join(random.choices(string.ascii_letters+string.digits,k=n))
    data[short_url] = original_url
    new_original=Project(original_url,short_url)
    db.session.add(new_original)
    db.session.commit()
    return render_template('index.html',k=short_url,data=original_url)

@app.route('/history')
def history_get():
    all_url=Project.query.all()
    return render_template('history.html', data=data,all_url=all_url)

@app.route('/sh/<short>')
def fun(short):
    if (short) in data:
        return redirect(data[(short)])
    return "incorrect URL"


if __name__=="__main__":
    app.run(debug=True)

