from email import message
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, HiddenField, StringField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from datetime import datetime
import pymysql



app = Flask(__name__)


# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY']='mykey'

# Flask-Bootstrap requires this line
Bootstrap(app)

# the name of the database; add path if necessary
# db_name = 'sqlite.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:008488@35.192.97.51/project'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class reserve(db.Model):
    __tablename__ = 'reserve'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ph_number = db.Column(db.String)
    people = db.Column(db.String)
    date = db.Column(db.String)
    time = db.Column(db.String)
    option = db.Column(db.String)
    plus = db.Column(db.String)
    updated = db.Column(db.String)

    def __init__(self, name, ph_number, people, date, time, option, plus, updated):
        self.name = name
        self.ph_number = ph_number
        self.people = people
        self.date = date
        self.time = time
        self.option = option
        self.plus = plus
        self.updated = updated

# !/usr/bin/python
# vim: set fileencoding:utf-8
#create form
class MyForm(FlaskForm):
    name = StringField('預約姓名', validators=[DataRequired()])
    ph_number = StringField('預約電話', validators=[DataRequired()])
    people = SelectField('預約人數', choices=[(r'1', r'1'), (r'2', r'2'), (r'3', r'3'), (r'4', r'4'), (r'5', r'5'), (r'5人以上', r'5人以上')])
    date =  DateField('預約日期', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('預約時間', choices=[('上午'), ('下午')])
    option = SelectField('兒童寫真方案選擇', choices=[(r'純數位檔方案 $4,999'),(r'紀念方案 ＄8,888'),
    (r'典藏方案 $13,500'),(r'全檔精緻方案 $18,500'),(r'成長方案-2年內拍攝3次（可包含新生兒寫真）$19,999')])
    plus = SelectField('加購項目', choices=[(r'無',r'無'),(r'外加入鏡 $500/人(爸媽以外成員)',r'外加入鏡 $500/人(爸媽以外成員)'),
    (r'媽媽另加妝髮造型 $1,000/套',r'媽媽另加妝髮造型 $1,000/套'),(r'兒童造型服 $500/套',r'兒童造型服 $500/套'),(r'新生兒造型 $1,000/套',r'新生兒造型 $1,000/套'),(r'外景拍攝另加 $500-3,000（依地點報價）',r'外景拍攝另加 $500-3,000（依地點報價）')])
    updated = HiddenField()
    submit = SubmitField("確認")

# home pag
@app.route('/',methods=['GET','POST'])
def index():
    """首頁"""
    form = MyForm()
    if form.validate_on_submit():
        session['name'] =form.name.data
        session['ph_number'] = form.ph_number.data
        session['people'] = form.people.data
        session['date'] = form.date.data
        session['time'] = form.time.data
        session['option'] = form.option.data
        session['plus'] = form.plus.data
        
        name = request.form['name']
        ph_number = request.form['ph_number']
        people = request.form['people']
        date = request.form['date']
        time = request.form['time']
        option = request.form['option']
        plus = request.form['plus']
        
        # get today's date from function, above all the routes
        updated = datetime.now()
        # the data to be inserted into Sock model - the table, socks
        print('name:\t', name)
        record = reserve(name, ph_number, people, date, time, option, plus, updated)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        
        return redirect(url_for('thankyou'))
    return render_template('reserve.html', form=form)

@app.route('/thankyou')
def thankyou():
    """thankyou頁"""
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# debug=True

