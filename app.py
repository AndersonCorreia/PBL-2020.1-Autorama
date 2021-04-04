from flask import Flask, render_template, request, redirect, url_for
from models.Leitor import Leitor
from models.Carro import Carro
from models.Corrida import Corrida
from models.Autorama import Autorama

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if (request.method == "GET"):
        leitor = Leitor()
        status = leitor.getButton()['success']
        autorama = Autorama()
        if autorama.dados['corrida_ativa'] > 0:
            corrida = autorama.getCorridaAtual()
            return render_template('index.html', ativo=True, status=status, corrida = corrida, circuito = autorama.getPista(corrida['circuito_id']))
        
        return render_template('index.html', ativo=False, status=False)

@app.route('/teste')
def test():
    leitor = Leitor()
    success = leitor.testConnection()['success']
    error = not success
    autorama = Autorama()
    if autorama.dados['corrida_ativa'] > 0 and success:
        corrida = autorama.getCorridaAtual()
        return render_template('index.html', success=success, error=error)
    
    return render_template('index.html', success=success, error=error)

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
        result = leitor.save(request.form.to_dict())
        return render_template('config/leitor.html', leitor = leitor.dados, saved=result['success'], error= not result['success'])

@app.route('/configuração/carro', methods=['GET', 'POST'])
def configCarro():
    if (request.method == "GET"):
        carro = Carro()
        dado = carro.getTag()
        if dado['success']:
            tag = dado['response']['tag'] 
        else:
            tag = 0
        return render_template('config/carro.html', success = dado['success'], EPC = tag)
    if (request.method == "POST"):
        carro = Carro()
        carro.save(request.form.to_dict())
        return render_template('config/carro.html', saved=True)

@app.route('/configuração/equipe', methods=['GET', 'POST'])
def configEquipe():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/equipe.html')
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addEquipe(request.form.to_dict())
        return render_template('config/equipe.html', saved=True)

@app.route('/configuração/pista/create', methods=['GET', 'POST'])
def createCircuito():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/pista_create.html', autorama = autorama.dados)
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addCircuito(request.form.to_dict())
        return redirect(url_for('listCircuito'))

@app.route('/configuração/pistas', methods=['GET'])
def listCircuito():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/pistas.html', autorama = autorama.dados)

@app.route('/configuração/corrida/create', methods=['GET', 'POST'])
def createCorrida():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/corrida_create.html', autorama = autorama.dados)
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addCorrida(request.form.to_dict(), request.form.getlist('piloto_id[]'))
        return redirect(url_for('listCorrida'))

@app.route('/configuração/corrida/ativa', methods=['POST'])
def setCorridaAtiva():
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.setCorridaAtiva(request.form.to_dict())
        return redirect(url_for('listCorrida'))

@app.route('/configuração/corridas', methods=['GET'])
def listCorrida():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/corridas.html',corridas = autorama.getCorridas(), corridaAtiva = autorama.dados['corrida_ativa'] )

@app.route('/configuração/piloto/cadastrar', methods=['GET', 'POST'])
def createPiloto():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/piloto_create.html', autorama = autorama.dados)
    if (request.method == "POST"):
        autorama = Autorama()
        autorama.addPiloto(request.form.to_dict())
        return redirect(url_for('listPilotos'))

@app.route('/configuração/piloto', methods=['GET'])
def listPilotos():
    if (request.method == "GET"):
        autorama = Autorama()
        return render_template('config/piloto.html', autorama = autorama.dados)

@app.route('/qualificatoria', methods=['GET'])
def qualificatoria():
    if (request.method == "GET"):
        corrida = Corrida(request.get('corrida_id'))
        corrida.qualificatoria()

@app.route('/sobre')
def about():
    return render_template('about.html')
