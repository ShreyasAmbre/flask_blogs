from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    name = "Shreyas"
    return render_template('index.html', name=name)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')


app.run()
