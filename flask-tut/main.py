from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

local_server = True
with open('config.json', 'r') as c:
    parameters = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters["gmail_user"],
    MAIL_PASSWORD=parameters["g_pass"]
)
mail = Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameters['prod_uri']
# below initializing db to flask app
db = SQLAlchemy(app)


# Models Below
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(25), nullable=True)


# Routes Below
@app.route('/')
def home():
    posts = Posts.query.all()
    return render_template('index.html', params=parameters, allposts=posts)


@app.route('/about')
def about():
    return render_template('about.html', params=parameters)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = request.form.get('msg')

        entry = Contacts(name=name, phone_num=phone, email=email, msg=msg, date=datetime.now())
        print(entry)
        db.session.add(entry)
        db.session.commit()

        mail.send_message('New Message from' + name,
                          sender=email,
                          recipients=[parameters['gmail_user']],
                          body=msg + "\n" + phone)
    return render_template('contact.html', params=parameters)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=parameters, post=post)



