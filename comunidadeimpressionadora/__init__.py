# pip install flask
# {% %} eu consigo chamar códigos de python no html
# pip install email_validator
# pip install flask-sqlalchemy
# pip install flask-wtf
# pip install flask-bcrypt
# pip install flask-login
# pip install Pillow

# criar banco de dados com o python console
# from comunidadeimpressionadora import app, database
# with app.app_context():
    # database.create_all()
# fazer o cadastro de teste no site
# voltar no python console para ver se deu certo
# from comunidadeimpressionadora.models import Usuario
# with app.app_context():
#     print(Usuario.query.all())
#     usuario = Usuario.query.first()
#     print(usuario.email)

# ****** ARQUIVO DE CONFIGURAÇÃO DO SITE, ONDE CRIA O APP, O DATABASE E IMPORTA OS LINKS/CAMINHOS *******


from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # sqlalchemy é um banco de dados com integração com o flask e permite criar as tabelas em forma de classes
from flask_bcrypt import Bcrypt  # criptografar as senhas dos usuários
from flask_login import LoginManager # permite fazer o login


app = Flask(__name__)  # obrigatório para usar o flask

app.config['SECRET_KEY'] = '84ee98eeb0577079b429a4b66c5aa423'  # token gerado para garantir a segurança de formulários, como login
                                                               # no terminal, import secrets -> secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'  # uri é o meu local no meu computador onde será criado o banco de dados. as /// indicam que será criado no mesmo local do arquivo main

database = SQLAlchemy(app)

bcrypt = Bcrypt(app) # criptografar as senhas

login_manager = LoginManager(app)
login_manager.login_view = 'login' # quando a página que eu tento acessar precisa de login, eu redireciono para a função login que é da página de login
login_manager.login_message = 'Faça login para acessar a página'
login_manager.login_message_category = 'alert-info'  # classe do bootstrap para deixar a mensagem azulzinha

from comunidadeimpressionadora import routes  # permite que o arquivo __init__ rode os routes para colocar os caminhos do site no ar
                                              # fica aqui no final porque os routes dependem do app, e o app está sendo criado no começo desse arquivo aqui