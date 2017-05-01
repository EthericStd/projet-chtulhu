#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
from liste_article import *
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
        cur.execute("SELECT numArticle, nomArticle, descriptionArticle FROM Article")
        l_articles = cur.fetchall()
        # articles = [carte_mere, carte_graphique]
        return render_template('layout_base.html', section=section,
                               l_css=l_css, articles=l_articles,
                               user=session['user'])
    section = "articles.html"
    l_css = ["articles.css"]
    articles = [carte_graphique, carte_mere]
    return render_template('layout_base.html', section=section,
                           l_css=l_css, articles=articles)


@app.route('/compte/mes_informations/')
def compte():
    if "user" in session:
        cur.execute("select *\
                    from get_infos_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        section = "mes_informations.html"
        l_css = ["mes_informations.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css, infos=infos[0],
                               user=session['user'])
    else:
        section = "non_connecte.html"
        l_css = "non_connecte.css"
        return render_template("layout_base.html",
                               section=section, l_css=l_css)


@app.route('/compte/')
def redir_compte():
    return redirect('/compte/mes_informations/')


@app.errorhandler(404)
def err(error):
    return ("ERROR {} CHTULHU NOT FOUND (lol)".format(error.code), error.code)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mailC = request.form["mail"]
        mdpC = request.form["mdp"]
        return log(mailC, mdpC)
    elif (request.method == 'GET') and ('user' in session):
        return redirect(url_for('redir_compte'))
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
                        flash(u"Adresse mail déjà utilisée :(")
                        return redirect(url_for("login"))
                    i += 1
            query = "INSERT INTO Client (nomClient, prenomClient,\
                     DateNaissanceClient, mailClient, MdpClient)\
                     VALUES ('"+nom+"', '"+prenom+"',\
                     '"+datena+"', '"+mailC+"', '"+mdpC+"');"
            cur.execute(query)
            conn.commit()
            url = log(mailC, mdpC)
            set_adresse_livraison()
            set_adresse_facturation()
            set_carte_paiement()
            set_panier()
            return url
        flash("Les mots de passe ne sont pas identiques.")
        return redirect(url_for('login'))
    else:
        abort(404)


@app.route('/non_connecte/')
def non_connect():
    section = "non_connecte.html"
    l_css = ["non_connecte.css"]
    return render_template("layout_base.html",
                           section=section, l_css=l_css)


@app.route('/panier/')
def panier():
    if ('user' in session):
        query = "SELECT numArticle, nbArticlePanier FROM ArticlePanier\
                WHERE numPanier=\
                (SELECT numPanier FROM Panier\
                WHERE numClient='"+str(session['user'])+"');"
        cur.execute(query)
        panier = cur.fetchall()
        i = 0
        for article in panier:
            query = "SELECT nomArticle FROM Article\
                     WHERE numArticle='"+str(article[0])+"';"
            cur.execute(query)
            article = article + (cur.fetchone()[0],)
            panier[i] = article
            i += 1
        section = "panier.html"
        l_css = ["panier.css"]
        return render_template("layout_base.html",
                               section=section, l_css=l_css,
                               panier=panier, user=session['user'])
    else:
        return redirect(url_for('non_connecte'))


@app.route('/ajout_panier/<int:id_article>/', methods=['GET', 'POST'])
def ajout_panier(id_article):
    if request.method == 'POST':
        id_article = id_article
        if ('user' in session):
            query = "SELECT numPanier FROM Panier\
                     WHERE numClient='"+str(session['user'])+"';"
            cur.execute(query)
            numP = cur.fetchone()[0]
            nbA = request.form['nbArticle']
            cur.execute("INSERT INTO ArticlePanier\
                        VALUES ('"+str(numP)+"',\
                        '"+str(id_article)+"', '"+str(nbA)+"')")
            conn.commit()
            return redirect(url_for('panier'))
        else:
            return redirect(url_for('non_connecte'))
    else:
        abort(404)


@app.route('/commande_panier/', methods=['GET', 'POST'])
def commande_panier():
    if request.method == "POST":
        if ('user' in session):
            if verif_info():
                section = "commande_panier.html"
                l_css = ["panier.css"]
            return render_template("layout_base.html", section=section,
                                   l_css=l_css, user=session['user'])
            flash(u"Veuillez remplir vos informations de paiement et de livraison.")
            return redirect(url_for("compte"))
        else:
            return redirect(url_for('non_connecte'))
    else:
        abort(404)


def log(mailC, mdpC):
    cur.execute("SELECT mailClient, mdpClient, prenomClient, numClient\
                FROM Client;")
    l_client = cur.fetchall()
    if (len(l_client) != 0):
        i = 0
        while (i < len(l_client)):
            if (l_client[i][0] == mailC) and (l_client[i][1] == mdpC):
                flash(u"Vous êtes connecté.\
                      Bonjour {} :)".format(l_client[i][2]))
                session['user'] = l_client[i][3]
                return redirect(url_for('articles'))
            i += 1
    flash("Informations incorrectes :(")
    return redirect(url_for('login'))


def set_adresse_facturation():
    cur.execute("INSERT INTO AdresseFacturation (numClient)\
                VALUES ('"+str(session['user'])+"');")
    conn.commit()


def set_adresse_livraison():
    cur.execute("INSERT INTO AdresseLivraison (numClient)\
                VALUES ('"+str(session['user'])+"');")
    conn.commit()


def set_carte_paiement():
    cur.execute("INSERT INTO CartePaienment (numClient)\
                VALUES ('"+str(session['user'])+"');")
    conn.commit()


def set_panier():
    cur.execute("INSERT INTO Panier (numClient)\
                VALUES ('"+str(session['user'])+"');")
    conn.commit()


def verif_info():
    cur.execute("SELECT * FROM AdresseLivraison\
                WHERE numClient='"+str(session['user'])+"';")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    cur.execute("SELECT * FROM AdresseFacturation\
                WHERE numClient='"+str(session['user'])+"';")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    cur.execute("SELECT * FROM CartePaienment\
                WHERE numClient='"+str(session['user'])+"';")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    return True


if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()
    cur.execute("SET search_path TO chtulhu")
    app.debug = True
    app.secret_key = "lolololololol"
    app.run()
