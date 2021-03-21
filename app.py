from flask import Flask, render_template, request
from models.Leitor import Leitor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configuração')
def config():
    return render_template('config/config.html')

@app.route('/configuração/leitor', methods=['GET', 'POST'])
def configLeitor():
    if (request.method == "GET"):
        leitor = Leitor()
        return render_template('config/leitor.html', leitor = leitor.dados)
    if (request.method == "POST"):
        leitor = Leitor()
        leitor.save(request.form)
        return render_template('config/leitor.html', leitor = leitor.dados, saved=True)

@app.route('/sobre')
def about():
    return render_template('about.html')
