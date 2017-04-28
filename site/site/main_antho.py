#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
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
    if ('user' in session):
        section = "accueil.html"
        l_css = []
        return render_template('layout_base.html', section=section,
                               l_css=l_css, user=session['user'])
    section = "accueil.html"
    l_css = []
    return render_template('layout_base.html', section=section, l_css=l_css)


@app.route('/articles/')
def articles():
    if ('user' in session):
        section = "articles.html"
        l_css = ["articles.css"]
        articles = [1, 2, 3]
        return render_template('layout_base.html', section=section,
                               l_css=l_css, articles=articles,
                               user=session['user'])
    section = "articles.html"
    l_css = ["articles.css"]
    articles = [1, 2, 3]
    return render_template('layout_base.html', section=section,
                           l_css=l_css, articles=articles)


@app.route('/compte/<int:page>/')
def compte(page):
    if "user" in session:
        page = page
        # cur.execute("select * from get_infos_client(" + str(session["user"]) + ")")
        cur.execute("SELECT * FROM Client WHERE\
                    numClient='"+str(session['user'])+"'")
        infos = cur.fetchall()
        section = "mes_informations.html"
        l_css = ["mes_informations.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css, infos=infos,
                               user=session['user'])
    else:
        section = "non_connecte.html"
        l_css = "non_connecte.css"
        return render_template("layout_base.html",
                               section=section, l_css=l_css)


@app.route('/compte/')
def redir_compte():
    return redirect('/compte/1/')


@app.errorhandler(404)
def err(error):
    return ("ERROR {} CHTULHU NOT FOUND (lol)".format(error.code), error.code)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur.execute("SELECT mailClient, mdpClient, prenomClient, numClient\
                    FROM Client;")
        l_client = cur.fetchall()
        mailC = request.form["mail"]
        mdpC = request.form["mdp"]
        if (len(l_client) != 0):
            i = 0
            while (i < len(l_client)):
                if (l_client[i][0] == mailC) and (l_client[i][1] == mdpC):
                    flash(u"Vous êtes connecté. Bonjour "+l_client[i][2]+" :)")
                    session['user'] = l_client[i][3]
                    return redirect(url_for('articles'))
                i += 1
        flash("Informations incorrectes :(")
        return redirect(url_for('login'))
    elif (request.method == 'GET') and ('user' in session):
        return redirect(url_for('compte'))
    else:
        section = "login.html"
        l_css = ["login.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css)


@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('accueil'))


@app.route('/subscription/', methods=['GET', 'POST'])
def subscription():
    if request.method == 'POST':
        cur.execute("SELECT mailClient FROM Client;")
        l_client = cur.fetchall()
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        datena = request.form["date_naissance"]
        mailC = request.form["mail"]
        mdpC = request.form["mdp"]
        mdpConfC = request.form["mdpconfirm"]
        if (mdpC == mdpConfC):
            if (len(l_client) != 0):
                i = 0
                while (i < len(l_client)):
                    if (l_client[i][0] == mailC):
                        section = "accueil.html"
                        l_css = []
                        return render_template('layout_base.html',
                                               section=section, l_css=l_css)
                    i += 1
            query = "INSERT INTO Client (nomClient, prenomClient, DateNaissance,\
                     mailClient, MdpClient) VALUES ('"+nom+"', '"+prenom+"',\
                     '"+datena+"', '"+mailC+"', '"+mdpC+"');"
            cur.execute(query)
            conn.commit()
            return redirect(url_for('articles'))
        flash("Les mots de passe ne sont pas identiques.")
        return redirect(url_for('login'))
    else:
        abort(404)

if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()
    cur.execute("SET search_path TO chtulhu")
    app.debug = True
    app.secret_key = "lolololololol"
    app.run()
