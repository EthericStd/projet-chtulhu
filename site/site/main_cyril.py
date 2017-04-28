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
    l_css = ["accueil.css"]
    return render_template("layout_base.html", section=section, l_css=l_css)


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


@app.route('/compte/mes_informations/', methods=['GET'])
def compte():
    if "user" in session:
        cur.execute("select * from get_infos_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        section = "mes_informations.html"
        l_css = ["mes_informations.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css, infos=infos[0],
                               user=session['user'])
    else:
        section = "non_connecte.html"
        l_css = ["non_connecte.css"]
        return render_template("layout_base.html",
                               section=section, l_css=l_css)


@app.route('/compte/changer_mdp/', methods=['GET'])
def changer_mdp():
    if "user" in session:
        section = "changer_mdp.html"
        l_css = ["changer_mdp.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css,
                               user=session['user'])
    else:
        return redirect('/non_connecte/')


@app.route('/compte/changer_mdp/', methods=['POST'])
def changer_mdp_():
    if "user" in session:
        ancien_mdp = request.form["ancien_mdp"]
        new_mdp = request.form["new_mdp"]
        new_mdp_confirm = request.form["new_mdp_confirm"]
        cur.execute("select * from get_infos_client(" + str(session["user"]) + ")")
        mdp = cur.fetchall()[0][4]
        if mdp != ancien_mdp:
            flash("L'ancien mot de passe n'est pas identique.")
            return redirect("compte/changer_mdp/")
        elif new_mdp != new_mdp_confirm:
            flash("Les nouveaux mots de passe ne sont pas identiques.")
            return redirect("compte/changer_mdp/")
        else:
            cur.execute("select changer_mdp(" + str(session["user"]) + ", '" + str(new_mdp) + "')")
            conn.commit()
            return redirect("/compte/mes_informations/")
    else:
        return redirect("/non_connecte/")


@app.route('/compte/')
def redir_compte():
    return redirect('/compte/mes_informations/')

@app.route('/non_connecte/')
def non_connect():
    section = "non_connecte.html"
    l_css = ["non_connecte.css"]
    return render_template("layout_base.html",
                            section=section, l_css=l_css)

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
                        section = "accueil.html"
                        l_css = ["accueil.css"]
                        return render_template('layout_base.html',
                                               section=section, l_css=l_css)
                    i += 1
            query = "INSERT INTO Client (nomClient, prenomClient, DateNaissanceClient,\
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
