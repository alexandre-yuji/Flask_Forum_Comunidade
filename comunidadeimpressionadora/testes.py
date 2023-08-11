from comunidadeimpressionadora import app, database  # importar o app do flask e a integração com o sqlalchemy

# with app.app_context():  # atualização do flask para poder rodar a aplicação do banco de dados fora do app
#     database.create_all()  # cria o arquivo do banco de dados


# with app.app_context():
#     usuario = Usuario(username='Lira', email='lira@gmail.com', senha='123456')  # criando uma instância da tabela Usuario. os atributos que faltam ou são auto increment ou tem default
#     usuario2 = Usuario(username='João', email='joao@gmail.com', senha='123456')
#
#     database.session.add(usuario)
#     database.session.add(usuario2)
#
#     database.session.commit()


# with app.app_context():
#     meus_usuarios = Usuario.query.all()  # busca por todos os usuários
#     print(meus_usuarios)
#
#     primeiro_usuario = Usuario.query.first()  # busca pelo primeiro usuário e seus atributos
#     print(primeiro_usuario.id)
#     print(primeiro_usuario.email)
#     print(primeiro_usuario.posts)
#
#     usuario_teste = Usuario.query.filter_by(id=2).first()  # busco usando filtro
#     print(usuario_teste)
#     print(usuario_teste.email)
#
#     usuario_teste2 = Usuario.query.filter_by(email='lira@gmail.com').first()
#     print(usuario_teste2)
#     print(usuario_teste2.username)


# with app.app_context():
#     meu_post = Post(titulo='Primeiro Post do Lira', corpo='Lira Voando', id_usuario=1)  # criando uma instância de Post
#
#     database.session.add(meu_post)
#
#     database.session.commit()


# with app.app_context():
#     post = Post.query.all()
#     print(post)
#
#     post2 = Post.query.first()
#     print(post2.titulo)
#     print(post2.autor.email)  # utilizo a relação criada com o backref


with app.app_context():
    database.drop_all()   # deletei os testes e criei o banco de dados novamente
    #database.create_all()