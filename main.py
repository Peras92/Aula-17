from flask import Flask, render_template, request, make_response, redirect, url_for
from sqla_wrapper import SQLAlchemy
import os
from sqlalchemy_pagination import paginate
import random
#from datetime import datetime
import uuid
import hashlib

app = Flask(__name__)

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilizador = db.Column(db.String, unique=False)
    texto = db.Column(db.String, unique=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)
    segredo = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default = True)

db.create_all()

#função para validar se o utilizar está logado
def utilizador_reg():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token, activo=True).first()
    else:
        user = None
    return user

@app.route("/")
def index():
    user = utilizador_reg()
    
    return render_template("index.html", user=user)

@app.route("/aboutme/")
def about_me():
    user = utilizador_reg()

    return render_template("about_me.html", user=user)

@app.route("/portefolio/")
def portfolio():
    user = utilizador_reg()
    return render_template("portefolio.html", user=user)

@app.route("/portefolio/fakebook/")
def fakebook():
    return render_template("Fakebook.html")

@app.route("/portefolio/boogle/")
def boogle():
    return render_template("Boogle.html")

@app.route("/portefolio/boogle/login/")
def login():
    return render_template("Login.html")

@app.route("/portefolio/cabeleireiro/")
def cabeleireiro():
    return render_template("cabeleireiro.html")

@app.route("/numero/", methods=["Get", "POST"])
def numero():
    user = utilizador_reg()

    if request.method == "GET":
        pagina = make_response(render_template("numero.html", user=user))

        return pagina

    elif request.method == "POST":
        adivinha = int(request.form.get("tentativa"))
        segredo = user.segredo

        if adivinha == segredo:
            mensagem = "Parabens! Conseguiste adivinhar que o número secreto era o {0}!".format(str(segredo))

            pagina = make_response(render_template("sucesso.html", mensagem = mensagem))
            user.segredo = str(random.randint(1, 10))

            user.save()

            return pagina

        elif adivinha > segredo:
            mensagem = "O {0} não é o número certo. Tenta um número menor.".format(str(adivinha))

            return render_template("sucesso.html", mensagem=mensagem)

        elif adivinha < segredo:
            mensagem = "O {0} não é o número certo. Tenta um número maior.".format(str(adivinha))

            return render_template("sucesso.html", mensagem=mensagem, user=user)
   
@app.route("/mural/", methods=["GET"])
def mural():
    user = utilizador_reg()

    page = request.args.get("page")

    if not page:
        page=1

    mensagem_filtrada = db.query(Mensagem)

    mensagem = paginate(query=mensagem_filtrada, page=int(page), page_size=5)

    return render_template("mural.html", mensagem=mensagem, user=user)

@app.route("/add-message", methods=["POST"])
def add_message():
    user = utilizador_reg()

    utilizador = user.nome
    texto = request.form.get("texto")

    mensagem = Mensagem(utilizador=utilizador, texto=texto)
    mensagem.save()

    return redirect("/mural")

@app.route("/registo/", methods=["GET", "POST"])
def registo():
    if request.method == "GET":
        return render_template("registo.html")

    else:
        utilizador = request.form.get("utilizador")
        email = request.form.get("email")
        password = request.form.get("password_user")

        # hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = db.query(User).filter_by(email=email).first()

        if not user:
        # create a User object
            user = User(nome=utilizador, email=email, password=hashed_password, segredo = str(random.randint(1, 10)), activo = True)

        # save the user object into a database
        user.save()

        if hashed_password != user.password:
            return "WRONG PASSWORD! Go back and try again."

        elif hashed_password == user.password:
            # create a random session token for this user
            session_token = str(uuid.uuid4())

            # save the session token in a database
            user.session_token = session_token
            user.save()
            
            # save user's email into a cookie
            response = make_response(redirect(url_for("index")))
            response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

            return response

@app.route("/profile/", methods=["GET"])
def profile():
    user = utilizador_reg()

    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("/index"))

@app.route("/profile/edit/", methods=["GET", "POST"])
def profile_edit():
    user = utilizador_reg()

    if request.method == "GET":
        if user:  # if user is found
            return render_template("profile_edit.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":
        utilizador = request.form.get("utilizador")
        email = request.form.get("email")
        password = request.form.get("password_user")

        # hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user.nome = utilizador
        user.email = email
        user.password = hashed_password
        
        # save the user object into a database
        user.save()

        return redirect(url_for("profile"))

@app.route("/profile/delete/", methods=["GET", "POST"])
def profile_delete():
    user = utilizador_reg()

    if request.method == "GET":
        if user:  # if user is found
            return render_template("profile_delete.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":
        user.activo = False
        user.save()
        return redirect(url_for("index"))

@app.route("/logout/")
def logout():
    response = redirect(url_for("index"))
    response.delete_cookie("session_token")

    return response


@app.route("/utilizadores/", methods=["GET"])
def utilizadores():
    user = utilizador_reg()
    utilizadores = db.query(User).all()

    return render_template("utilizadores.html", utilizadores=utilizadores, user=user)

@app.route("/utilizadores/<user_id>",  methods=["GET"])
def detalhe_utilizador(user_id):
    user = utilizador_reg()
    detalhe = db.query(User).get(int(user_id))

    return render_template("detalhe_utilizador.html", user=user, detalhe=detalhe)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

#@app.errorhandler(500)
#def page_not_found(e):
    # note that we set the 500 status explicitly
#    return render_template('404.html'), 500

if __name__ == '__main__':
    app.run()  # if you use the port parameter, delete it before deploying to Heroku