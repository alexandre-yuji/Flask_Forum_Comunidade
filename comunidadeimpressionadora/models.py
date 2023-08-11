
# ******* ARQUIVO PARA CRIAÇÃO DO BANCO DE DADOS (TABELAS E RELAÇÕES) ********

from comunidadeimpressionadora import database, login_manager  # encontra usuário
from datetime import datetime
from flask_login import UserMixin  # parâmetro que eu passo para a classe que vai atribuir para a classe todas as características que o login_manager precisa


@login_manager.user_loader
def load_usuario(id_usuario):  # função para carregar um usuário cadastrado através do login_manager
    return Usuario.query.get(int(id_usuario))  # encontra o usuario através do id_usuario que é a chave primária

class Usuario(database.Model, UserMixin):  #.Model é uma herança do sqlalchemy
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default='Não Informado')
    posts = database.relationship('Post', backref='autor', lazy=True)  # criando a relação entre as tabelas Usuario e Post. backref é o nome que vai me permitir acessar quem criou o post

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):  #.Model é uma herança do sqlalchemy
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)  # id da tabela usuário é minha chave estrangeira aqui