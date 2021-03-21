from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configuração')
def config():
    return render_template('config/config.html')

@app.route('/configuração/leitor')
def configLeitor():
    return render_template('config/leitor.html')

@app.route('/sobre')
def about():
    return render_template('about.html')
