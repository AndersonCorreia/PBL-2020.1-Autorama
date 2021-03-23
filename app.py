from flask import Flask, render_template, request
from models.Leitor import Leitor
from models.Carro import Carro

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

@app.route('/configuração/carro', methods=['GET', 'POST'])
def configCarro():
    if (request.method == "GET"):
        return render_template('config/carro.html')
    if (request.method == "POST"):
        carro = Carro()
        carro.save(request.form)
        return render_template('config/carro.html', carro = carro.dados, saved=True)

@app.route('/configuração/pistas', methods=['GET', 'POST'])
def configLeitor():
    if (request.method == "GET"):
        leitor = Leitor()
        return render_template('config/leitor.html', leitor = leitor.dados.pista)
    if (request.method == "POST"):
        leitor = Leitor()
        leitor.save(request.form)
        return render_template('config/leitor.html', leitor = leitor.dados, saved=True)

@app.route('/sobre')
def about():
    return render_template('about.html')
