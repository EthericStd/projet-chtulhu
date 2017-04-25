#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
from random import randrange
app = Flask(__name__)


def connect():
    try:
        conn = psycopg2.connect(dbname="chtulhu")
        print("\nConnecté.\n")
    except:
        print("\n##### ERREUR DE CO #####\n")
    return conn


@app.route('/')
def accueil():
    session["user"] = 1
    section = "acceuil.html"
    l_css = ["acceuil.css"]
    return render_template('layout_base.html', section=section, l_css=l_css)


@app.route('/articles/')
def articles():
    section = "articles.html"
    l_css = ["articles.css"]
    articles = [1, 2, 3]
    return render_template('layout_base.html', section=section,
                           l_css=l_css, articles=articles)

@app.route('/compte/<page>/')
def compte(page):
    if "user" in session:
        page = page
        cur.execute("select * from get_infos_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        section = "mes_informations.html"
        l_css = ["mes_informations.css"]
        return render_template('layout_base.html', section=section,
                                                   l_css=l_css,
                                                   infos=infos[0])
    else:
        section = "non_connecte.html"
        l_css = "non_connecte.css"
        return render_template("layout_base.html", section=section,
                                                   l_css=l_css)

@app.errorhandler(404)
def err(error):
    return ("ERROR {} CHTULHU NOT FOUND (lol)".format(error.code), error.code)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur.execute("SELECT mailClient FROM Client;")
        l_client = cur.fetchall()
        print(l_client)
        mailC = request.form["mail"]
        if (len(l_client) != 0):
            i = 0
            while (i < len(l_client)):
                if (l_client[i][0] == mailC):
                    return redirect(url_for('articles'))
                i += 1
        return render_template('acceuil.html')
    else:
        section = "login.html"
        l_css = ["acceuil.html"]
        return render_template('layout_base.html', section=section, l_css=l_css)


@app.route('/subscription/', methods=['POST'])
def subscription():
    cur.execute("SELECT * FROM Client;")
    l_client = cur.fetchall()
    print(l_client)
    numC = randrange(20, 30)
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    mailC = request.form["mail"]
    if (len(l_client) != 0):
        i = 0
        while (i < len(l_client)):
            if (l_client[i][4] == mailC):
                return render_template('acceuil.html')
            if (l_client[i][0] == numC):
                numC = randrange(20, 30)
                i = -1
            i += 1
    query = "INSERT INTO Client (numClient, nomClient, prenomClient, mailClient) \
             VALUES ('"+str(numC)+"', '"+nom+"', '"+prenom+"', '"+mailC+"');"
    cur.execute(query)
    conn.commit()
    return redirect(url_for('articles'))

if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()
    cur.execute("SET search_path TO chtulhu")
    app.debug = True
    app.secret_key = "lolololololol"
    app.run()
