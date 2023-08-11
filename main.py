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

# ******* ARQUIVO APENAS PARA RODAR O CÓDIGO *********

from comunidadeimpressionadora import app


if __name__ == '__main__':
    app.run(debug=True)  # as mudanças são atualizadas automaticamente no site