from flask import Flask, render_template, request, redirect, url_for, session
from models.Leitor import Leitor
from models.Carro import Carro
from models.Qualificatoria import Qualificatoria
from models.Classificacao import Classificacao
from models.Autorama import Autorama
from threads.QualificatoriaThread import QualificatoriaThread
from threads.ClassificacaoThread import ClassificacaoThread
from threads.InterromperCorridaThread import InterromperCorridaThread

app = Flask(__name__)
app.secret_key = "pbl"

@app.route('/', methods=['GET'])
def index():
    if (request.method == "GET"):
        autorama = Autorama()
        
        if autorama.dados['corrida_ativa'] > 0: 
            corrida = autorama.getCorridaAtual()
            return render_template('index.html', ativo=True, corrida = corrida, circuito = autorama.getPista(corrida['circuito_id']))

        return render_template('index.html', ativo=False)

@app.route('/teste')
def test():
    leitor = Leitor()
    success = leitor.testConnection()['success']
    error = not success
    autorama = Autorama()
    if autorama.dados['corrida_ativa'] > 0 and success:
        corrida = autorama.getCorridaAtual()
        return render_template('index.html', success=success, error=error, ativo=True, corrida = corrida, circuito = autorama.getPista(corrida['circuito_id']))
    
    return render_template('index.html', success=success, error=error)

@app.route('/qualificatoria/<int:id>', methods=['GET'])
def qualificatoriaHistorico(id):
    if (request.method == "GET"):
        autorama = Autorama()
        qualificatoria = Qualificatoria(id)
        corrida = qualificatoria.corrida
        qualificatoriaDados = qualificatoria.getDadosQualificatoria()
        return render_template('qualificatoria/qualificatoria.html', status = corrida['qualificatoriaCompleta'], qualificatoria=qualificatoriaDados, circuito = autorama.getPista(corrida['circuito_id']))

@app.route('/qualificatoria', methods=['GET'])
def qualificatoria():
    if (request.method == "GET"):
        autorama = Autorama()
        qualificatoria = Qualificatoria()
        corrida = qualificatoria.corrida
        qualificatoriaDados = qualificatoria.getDadosQualificatoria()
        return render_template('qualificatoria/qualificatoria.html', tempo = corrida['qualificatoriaDuracao'], status = corrida['qualificatoriaCompleta'], qualificatoria=qualificatoriaDados, circuito = autorama.getPista(corrida['circuito_id']))

@app.route('/qualificatoria/atualizar', methods=['GET'])
def updateQualificatoria():
    if (request.method == "GET"):
        autorama = Autorama()
        qualificatoria = Qualificatoria()
        qualificatoriaDados = qualificatoria.getDadosQualificatoria()
        return {'data': qualificatoriaDados, 'status': qualificatoria.corrida['qualificatoriaCompleta'] }

@app.route("/rest/qualificatoria")
def rest():
    session["rest"] = 5
    session["set_counter"] = 0
    qualificatoria = Qualificatoria()
    qualificatoria.resetQualificatoria()
    return render_template("qualificatoria/timer.html", rest=session["rest"])

@app.route('/classificacao/<int:id>', methods=['GET'])
def classificacaoHistorico(id):
    if (request.method == "GET"):
        autorama = Autorama()
        classificacao = Classificacao(id)
        corrida = classificacao.corrida
        classificacaoDados = classificacao.getDadosClassificacao()
        return render_template('classificacao/classificacao.html', status = corrida['corridaCompleta'], classificacao=classificacaoDados, circuito = autorama.getPista(corrida['circuito_id']), contentLarge=True)

@app.route('/classificacao', methods=['GET'])
def classificacao():
    if (request.method == "GET"):
        autorama = Autorama()
        classificacao = Classificacao()
        corrida = classificacao.corrida
        classificacaoDados = classificacao.getDadosClassificacao()
        return render_template('classificacao/classificacao.html', tempo = corrida['classificacaoDuracao'], status = corrida['corridaCompleta'], classificacao=classificacaoDados, circuito = autorama.getPista(corrida['circuito_id']), contentLarge=True)

@app.route('/classificacao/atualizar', methods=['GET', 'POST'])
def updateClassificacao():
    classificacao = Classificacao()
    if (request.method == "GET"):
        autorama = Autorama()
        classificacaoDados = classificacao.getDadosClassificacao()
        return {'data': classificacaoDados, 'status': classificacao.corrida['corridaCompleta'] }
    if (request.method == "POST"):
        classificacao.setTime(request.form['time'])
        return redirect(url_for('classificacao'))

@app.route("/rest/classificacao")
def restClassificacao():
    session["rest"] = 5
    session["set_counter"] = 0
    classificacao = Classificacao()
    classificacao.resetClassificacao()
    return render_template("classificacao/timer.html", rest=session["rest"])

@app.route("/button/pres")
def buttonPres():
    if (request.method == "GET"):
        leitor = Leitor()
        return leitor.getButton()

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
        dado = carro.getTags()
        if dado['success']:
            tags = dado['response'] 
        else:
            tags = None
        return render_template('config/carro.html', success = dado['success'], EPCs = tags)
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
    
@app.route('/thread/corrida/qualificatoria', methods=['GET'])
def qualificatoriaThread():
    if (request.method == "GET"):
        qualificatoriaT = QualificatoriaThread()
        qualificatoriaT.start()
        interromperCorridaT = InterromperCorridaThread(qualificatoriaT.corrida)
        interromperCorridaT.start()
        return {'success': True}
    
@app.route('/thread/corrida/classificacao', methods=['GET'])
def classificacaoThread():
    if (request.method == "GET"):
        classificacaoT = ClassificacaoThread()
        classificacaoT.start()
        interromperCorridaT = InterromperCorridaThread(classificacaoT.corrida)
        interromperCorridaT.start()
        return {'success': True}

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

@app.route('/sobre')
def about():
    return render_template('about.html')
