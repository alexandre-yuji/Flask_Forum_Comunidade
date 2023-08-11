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


# ******* ARQUIVO DE CAMINHOS DAS PÁGINAS *******

from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost  # importa as classes do arquivo de forms
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required  # permite fazer login, sair do login, verifica se o usuário atual é o que fez login, só pode visualizar a página se estiver logado
import secrets  # para gerar chaves aleatórias
import os
from PIL import Image  # permite mexer com imagem. ex: compactar a imagem


@app.route('/')  # caminho da página inicial
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)  # render_template importa o nome do arquivo que estou importando

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required  # só acessa a página se estiver logado
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios) # o parâmetro pode ter qualquer nome e vai ser usado dentro do template, mas por padrão é recomendado usar o mesmo nome da variável

@app.route('/login', methods=['GET', 'POST'])  # indico que quero usar os métodos get e post
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
                                                                        # validate_on_submit() valida os validators do arquivo forms
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:  # preciso ter as duas validações porque os botões de login e criar conta estão na mesma página

        usuario = Usuario.query.filter_by(email=form_criar_conta.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data): # se o email está cadastrado e comparo a criptografia da senha cadastrada com a senha que colocou no campo de login
            login_user(usuario, remember=form_login.lembrar_dados.data)  # usuario é a validação de email e senha. remember é a marcação da caixa lembrar_dados do arquivo forms
            flash(f'Login realizado com sucesso para o email {form_login.email.data}', 'alert-success')  # .data é o conteúdo do campo. alert-success é classe do bootstrap que exibe mensagem verdinha

            parametro_next = request.args.get('next') # next é parâmetro da url condizente à página que eu tentei acessar mas pediu login primeiro
            if parametro_next:
                return redirect(parametro_next) # quando eu fizer o login, redireciono para a página que eu estava tentando entrar antes do login
            else:
                return redirect(url_for('home')) # senão eu redireciono para a home

            return redirect(url_for('home')) # redireciona para a página da função home
        else:
            flash(f'Email ou senha incorretos.', 'alert-danger') # alert-danger é classe do bootstrap vermelhinha

    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:

        # criar usuário
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data) # criptografar a senha
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)  # crio uma instância pegando os valores inseridos em cada campo
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso para o email {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)  # posso acessar o form_login e form_criar_conta dentro da página login.html

@app.route('/sair')
@login_required  # só acessa a página se estiver logado
def sair():
    logout_user()
    flash('Logout feito com sucesso.', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required  # só acessa a página se estiver logado
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')  # procuro pelo caminho da foto_perfil do usuário
    return render_template('perfil.html', foto_perfil=foto_perfil) # passo para a página html a foto_perfil

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required  # só acessa a página se estiver logado
def criar_post():
    form = FormCriarPost()

    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso.', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)  # gero código aleatório para o nome da foto inserida não ser igual a outra foto no banco de dados
    nome, extensao = os.path.splitext(imagem.filename) # separo o arquivo inserido em nome e extensao
    nome_arquivo = nome + codigo + extensao # junto novamente o que separei + codigo aleatório para ter um nome de arquivo único

    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo) # caminho completo onde eu vou salvar a foto, desde a pasta comunidadeimpressionadora

    tamanho = (200,200) # mesmo tamanho que coloquei no width da imagem de perfil no arquivo perfil.html
    imagem_reduzida = Image.open(imagem) # abro a imagem com a biblioteca do pillow e salvo em uma variável
    imagem_reduzida.thumbnail(tamanho) # passo o tamanho para a imagem
    imagem_reduzida.save(caminho_completo)  # salvo a imagem com o tamanho novo no caminho que escolhi na variável caminho_completo

    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:  # se a checkbox estiver selecionada
                lista_cursos.append(campo.label.text)  # adiciono o texto da variável que comemça com curso_. ex: curso_excel pego o texto Excel Impressionador
    return ';'.join(lista_cursos) # com o append de cima, os cursos estavam em uma lista. com o join, eu transformo tudo em um texto só, porque no arquivo models, os cursos são uma StringField


@app.route('/perfil/editar', methods=['GET', 'POST'])  # indico que quero usar os métodos get e post
@login_required  # só acessa a página se estiver logado
def editar_perfil():
    form = FormEditarPerfil()

    if form.validate_on_submit():  # se as validações no form de editar perfil estiverem ok
        current_user.email = form.email.data  # o email atual troca para o que foi inserido no campo de alterar email
        current_user.username = form.username.data  # o username atual troca para o que foi inserido no campo de alterar username

        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)  # chamo a função salvar_imagem passando a informação do campo foto_perfil
            current_user.foto_perfil = nome_imagem  # a foto de perfil passa a ser o que foi passado na variável nome_imagem quando chamou a função salvar_imagem

        current_user.cursos = atualizar_cursos(form)  # chamo a função atualizar_cursos

        database.session.commit()
        flash('Perfil atualizado com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":  # quando eu quiser que alguma coisa já venha preenchida
        form.email.data = current_user.email
        form.username.data = current_user.username

    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')  # procuro pelo caminho da foto_perfil do usuário
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)  # passo para a página html a foto_perfil e o formulário de editar perfil


@app.route('/post/<post_id>', methods=['GET', 'POST']) # <> é uma variável dentro da url
@login_required
def exibir_post(post_id):  # permite entrar em cada post individualmente, cada post tem a sua página
    post = Post.query.get(post_id) # por ser chave primária eu posso usar o método get

    if current_user == post.autor:  # se o usuário logado for o dono do post
        form = FormCriarPost()  # aparece o formulário de editar o post (mesmo form usado para criar post)
        if request.method == 'GET':
            form.titulo.data = post.titulo  # já vem preenchido o campo de editar título
            form.corpo.data = post.corpo  # já vem preenchido o campo de editar corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data  # post.titulo é atributo de post no arquivo models
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None

    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)

    if current_user == post.autor:  # se eu for o dono do post
        database.session.delete(post)  # posso deletar o post
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)  # erro de proibição. se eu não sou o dono do post eu não tenho permissão para excluir