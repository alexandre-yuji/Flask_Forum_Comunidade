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
# with app.app_context():
#     usuario = Usuario.query.filter_by(email='lirateste@gmail.com').first()
#     print(usuario.cursos)


from flask_wtf import FlaskForm  # importa os formulários do flask
from flask_wtf.file import FileField, FileAllowed  # permite escolher um arquivo do computador, permite escolher determinado tipo de arquivo (png, jpg)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # importa os campos de tipo texto, senha e confirmar, lembrar senha
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # permite validar informações. senha igual, email existente...
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm): # herança da classe flaskform (biblioteca), já contém o __init___
    username = StringField('Nome de Usuário', validators=[DataRequired()])  # campo obrigatório
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # campo obrigatório e de email
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)]) # campo obrigatório entre 6 e 20 caracteres
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')]) # campo obrigatório igual à variável senha
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):  # o validate_on_submit() do arquivo routes, além de validar os validators desse arquivo, também roda automaticamente qualquer função que comece com o nome validate_
        usuario = Usuario.query.filter_by(email=email.data).first()  # não preciso do form_criar_conta.email porque eu já estou dentro do forms com o self
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email ou faça login para continuar.')

    def validate_username(self, username):  # o validate_on_submit() do arquivo routes, além de validar os validators desse arquivo, também roda automaticamente qualquer função que comece com o nome validate_
        usuario = Usuario.query.filter_by(username=username.data).first()  # não preciso do form_criar_conta.email porque eu já estou dentro do forms com o self
        if usuario:
            raise ValidationError('Username já cadastrado. Cadastre-se com outro username ou faça login para continuar.')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')  # checkbox de verdadeiro ou falso
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarPerfil(FlaskForm): # herança da classe flaskform (biblioteca), já contém o __init___
    username = StringField('Nome de Usuário', validators=[DataRequired()])  # campo obrigatório
    email = StringField('E-mail', validators=[DataRequired(), Email()])  # campo obrigatório e de email
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])  # mensagem quando for escolher arquivo do computador, validators com as extensões permitidas

    curso_excel = BooleanField('Excel Impressionador')  # crio os checkbox na página de editarperfil
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('PowerPoint Impressionador')
    curso_sql = BooleanField('SQL Impressionador')

    botao_submit_editar_perfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):  # o validate_on_submit() do arquivo routes, além de validar os validators desse arquivo, também roda automaticamente qualquer função que comece com o nome validate_
        if current_user.email != email.data: # se o email atual é diferente do email inserido no campo de alterar email
            usuario = Usuario.query.filter_by(email=email.data).first()  # não preciso do form_criar_conta.email porque eu já estou dentro do forms com o self
            if usuario:
                raise ValidationError('Já existe um usuário com esse email.')

    def validate_username(self, username):  # o validate_on_submit() do arquivo routes, além de validar os validators desse arquivo, também roda automaticamente qualquer função que comece com o nome validate_
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()  # não preciso do form_criar_conta.email porque eu já estou dentro do forms com o self
            if usuario:
                raise ValidationError('Já existe um usuário com esse username.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva Seu Post Aqui', validators=[DataRequired()])
    botao_submit_criar_post = SubmitField('Criar Post')