from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configuração')
def config():
    return render_template('config.html')

@app.route('/sobre')
def about():
    return render_template('about.html')
