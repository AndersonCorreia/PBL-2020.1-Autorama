from flask import Flask, render_template, request, redirect, url_for
from models.Leitor import Leitor
from models.Carro import Carro
from models.Autorama import Autorama

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
        leitor.save(request.form.to_dict())
        return render_template('config/leitor.html', leitor = leitor.dados, saved=True)

@app.route('/configuração/carro', methods=['GET', 'POST'])
def configCarro():
    if (request.method == "GET"):
        carro = Carro()
        tag = carro.getTag()
        return render_template('config/carro.html', epc = tag)
    if (request.method == "POST"):
        carro = Carro()
        carro.save(request.form.to_dict())
        return render_template('config/carro.html', carro = carro.dados, saved=True)

@app.route('/configuração/pistas/create', methods=['GET', 'POST'])
def createCircuito():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/pistas.html', autorama = autorama.dados)
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addCircuito(request.form.to_dict())
        return redirect(url_for('config'))

@app.route('/configuração/corrida/create', methods=['GET', 'POST'])
def createCorrida():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/corridas.html', autorama = autorama.dados)
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addCorrida(request.form.to_dict())
        return redirect(url_for('config'))

@app.route('/sobre')
def about():
    return render_template('about.html')
