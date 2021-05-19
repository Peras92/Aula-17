from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/aboutme/")
def about_me():
    return render_template("about_me.html")

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

@app.route("/numero/", methods=["Get"])
def numero():

    segredo = request.cookies.get("segredo")

    pagina = make_response(render_template("numero.html"))

    if not segredo:
        novo_segredo = random.randint(1, 10)
        pagina.set_cookie("segredo", str(novo_segredo))

    return pagina

    #elif request.method == "POST":
        #adivinha = request.form.get("tentativa")

        #if adivinha == "segredo":
            #mensagem = "Parabens! Conseguiste adivinhar que o número secreto era o {0}!".format(str("segredo"))

            #pagina = make_response(render_template("sucesso.html", mensagem = mensagem))
            #pagina.set_cookie("segredo", str(random.randint(1, 10)))

            #return pagina
            #render_template("sucesso.html")

@app.route("/sucesso", methods=["POST"])
def sucesso():
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


    
       



if __name__ == '__main__':
    app.run()  # if you use the port parameter, delete it before deploying to Heroku