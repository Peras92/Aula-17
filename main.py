from flask import Flask, render_template, request, make_response, redirect, url_for
from sqla_wrapper import SQLAlchemy
import os
from sqlalchemy_pagination import paginate
import random
from funcoes import utilizador
from datetime import datetime

app = Flask(__name__)

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilizador = db.Column(db.String, unique=False)
    texto = db.Column(db.String, unique=False)

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aboutme/")
def about_me():
    return render_template("about_me.html", page = "aboutme")

@app.route("/portefolio/")
def portfolio():
    return render_template("portefolio.html")

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
    if request.method == "GET":
        segredo = request.cookies.get("segredo")

        pagina = make_response(render_template("numero.html"))

        if not segredo:
            novo_segredo = random.randint(1, 10)
            pagina.set_cookie("segredo", str(novo_segredo))

        return pagina

    elif request.method == "POST":
        adivinha = int(request.form.get("tentativa"))
        segredo = int(request.cookies.get("segredo"))

        if adivinha == segredo:
            mensagem = "Parabens! Conseguiste adivinhar que o número secreto era o {0}!".format(str(segredo))

            pagina = make_response(render_template("sucesso.html", mensagem = mensagem))
            pagina.set_cookie("segredo", str(random.randint(1, 10)))

            return pagina

        elif adivinha > segredo:
            mensagem = "O {0} não é o número certo. Tenta um número menor.".format(str(adivinha))

            return render_template("sucesso.html", mensagem=mensagem)

        elif adivinha < segredo:
            mensagem = "O {0} não é o número certo. Tenta um número maior.".format(str(adivinha))

            return render_template("sucesso.html", mensagem=mensagem)
   
@app.route("/mural/", methods=["GET"])
def mural():
    page = request.args.get("page")

    if not page:
        page=1

    mensagem_filtrada = db.query(Mensagem)

    mensagem = paginate(query=mensagem_filtrada, page=int(page), page_size=5)

    return render_template("mural.html", mensagem=mensagem)

@app.route("/add-message", methods=["POST"])
def add_message():
    utilizador = request.form.get("utilizador")
    texto = request.form.get("texto")

    mensagem = Mensagem(utilizador=utilizador, texto=texto)
    mensagem.save()

    return redirect("/mural")

@app.route("/registo/", methods=["GET", "POST"])
def registo():
    if request.methods=="GET":
        return render_template("registo.html")

    else:
        name = request.form.get("user-name")
        email = request.form.get("user-email")

        # create a User object
        user = User(name=name, email=email)

        # save the user object into a database
        db.add(user)
        db.commit()

        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('404.html'), 500

if __name__ == '__main__':
    app.run()  # if you use the port parameter, delete it before deploying to Heroku