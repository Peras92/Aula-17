from flask import Flask, render_template

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

@app.route("/numero/", methods=["Get", "Post"])
def numero():

    return render_template("numero.html")

if __name__ == '__main__':
    app.run()  # if you use the port parameter, delete it before deploying to Heroku