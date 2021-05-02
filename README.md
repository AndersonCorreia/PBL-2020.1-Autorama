# PBL-2020.1-Autorama

### Pré-requisitos

Para rodar a aplicação web, você vai precisar ter instalado em sua máquina as seguintes ferramentas 🛠:
[Python 3.5 ou superior](https://www.python.org/downloads/) - 
[Pip](https://pypi.org/project/pip/) - 
[Flask](https://flask.palletsprojects.com/en/1.1.x/installation/)

```bash
# Clone este repositório
$ git clone https://github.com/AndersonCorreia/PBL-2020.1-Autorama.git

# Crie um ambiente virtual dentro da pasta do projeto
$ python3 -m venv venv

# Ative o ambiente
$ source venv/bin/activate

# No Windows
>> py -3 -m venv venv
>> venv\Scripts\activate

# Instale o Flask
$ pip install Flask
```

### Para executar a aplicação web dentro do ambiente virtual
```bash
# Definir as variáveis de ambiente no Linux:
$ export FLASK_APP=app
$ export FLASK_ENV=development

# No PowerShell do Windows
>> $env:FLASK_APP = "app.py"
>> $env:FLASK_ENV = "development"

# No Prompt de Comando do Windows
>> set FLASK_APP=app.py
>> set FLASK_ENV=development

# Execute o comando para iniciar o servidor:
$ flask run

# Ou então
$ py -m flask run

Ao acessar a URL <http://127.0.0.1:5000/>, que será exibida no terminal, a aplicação já poderá ser usada. 
```