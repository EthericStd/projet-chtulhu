#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
import time
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
    if 'user' in session:
        section = "accueil.html"
        l_css = ["accueil.css"]
        return render_template('layout_base.html', section=section,
                               l_css=l_css, user=session['user'])
    section = "accueil.html"
    l_css = ["accueil.css"]
    return render_template("layout_base.html", section=section, l_css=l_css)


@app.route('/articles/')
def articles():
    section = "articles.html"
    l_css = ["articles.css"]
    cur.execute("SELECT numArticle, LibelléArticle, DescriptionArticle FROM Article")
    l_articles = cur.fetchall()

    N = len(l_articles)
    for i in range(N):
        cur.execute("SELECT ValeurTags FROM Tags\
                    WHERE NumArticle = '"+ str(l_articles[i][0]) + "'\
                    AND NomTags =  'type composant'; ")
        nom_img = cur.fetchall()[0][0]
        l_articles[i] = list(l_articles[i]) + [nom_img]
    print(l_articles)
    if ('user' in session):
        return render_template('layout_base.html', section=section,
                               l_css=l_css, articles=l_articles,
                               user=session['user'])
    return render_template('layout_base.html', section=section,
                           l_css=l_css, articles=l_articles)


@app.route('/article/<int:id_article>/', methods=['GET', 'POST'])
def article(id_article):
    id_article = id_article
    section = "article.html"
    l_css = ["articles.css"]
    cur.execute("SELECT LibelléArticle, DescriptionArticle FROM Article\
                WHERE numArticle='"+str(id_article)+"';")
    article = [id_article] + [cur.fetchone()]
    cur.execute("SELECT valeurTags FROM Tags\
                WHERE numArticle='"+str(id_article)+"'\
                AND nomTags <> 'type composants';")
    l_tags = cur.fetchall()
    cur.execute("SELECT valeurTags FROM Tags\
                WHERE numArticle='"+str(id_article)+"'\
                AND nomTags = 'type composants';")
    image = cur.fetchone()[0]
    if ('user' in session):
        return render_template('layout_base.html', section=section,
                               l_css=l_css, tags=l_tags, article=article,
                               user=session['user'], image=image)
    return render_template('layout_base.html', section=section,
                           l_css=l_css, article=article, tags=l_tags)


@app.route('/compte/mes_informations/', methods=['GET'])
def mes_informations():
    if "user" in session:
        cur.execute("select * from get_infos_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        cur.execute("select * from get_infos_vendeur(" + str(session["vendeur"]) + ")")
        infosv = cur.fetchall()
        section = "mes_informations.html"
        l_css = ["mes_informations.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css, infos=infos[0],
                               user=session['user'],
                               vendeur=session["vendeur"], infosv=infosv)
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
                               user=session['user'], vendeur=session["vendeur"])
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


@app.route('/compte/moyens_paiement/<int:index>/')
def moyens_paiement(index):
    index = index
    if "user" in session:
        cur.execute("select * from get_moyens_paiement_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        if index < len(infos) and index >= 0:

            nb_obj = len(infos)
            infos = list(infos[index])
            infos[1] = "**** **** **** " + str(infos[1]//10**11)

            section = "moyens_paiement.html"
            l_css = ["moyens_paiement.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        elif len(infos) == 0:
            nb_obj = len(infos)
            section = "moyens_paiement.html"
            l_css = ["moyens_paiement.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        else:
            abort(404)
    else:
        return redirect('/non_connecte/')


@app.route('/compte/adresse_facturation/<int:index>/')
def adr_facturation(index):
    index = index
    if "user" in session:
        cur.execute("select * from get_adr_facturation_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        if index < len(infos):

            nb_obj = len(infos)
            infos = list(infos[index])

            section = "adresse_facturation.html"
            l_css = ["adresse_facturation.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        elif len(infos) == 0:
            nb_obj = len(infos)
            section = "adresse_facturation.html"
            l_css = ["adresse_facturation.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        else:
            abort(404)
    else:
        return redirect('/non_connecte/')

@app.route('/compte/adresse_livraison/<int:index>/')
def adr_livraison(index):
    index = index
    if "user" in session:
        cur.execute("select * from get_adr_livraison_client(" + str(session["user"]) + ")")
        infos = cur.fetchall()
        if index < len(infos):

            nb_obj = len(infos)
            infos = list(infos[index])

            section = "adresse_livraison.html"
            l_css = ["adresse_livraison.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        elif len(infos) == 0:
            nb_obj = len(infos)
            section = "adresse_livraison.html"
            l_css = ["adresse_livraison.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   infos=infos,
                                   index=index,
                                   nb_obj=nb_obj,
                                   vendeur=session["vendeur"])
        else:
            abort(404)
    else:
        return redirect('/non_connecte/')


@app.route('/compte/ajout_moyens_paiement/', methods=['GET'])
def ajout_moyens_paiement():
    if "user" in session:
        section = "ajout_moyens_paiement.html"
        l_css = ["ajout_moyens_paiement.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css,
                               user=session['user'], vendeur=session["vendeur"])
    else:
        return redirect('/non_connecte/')


@app.route('/compte/ajout_moyens_paiement/', methods=['POST'])
def ajout_moyens_paiement_():
    if "user" in session:
        type_cb = request.form["type_cb"]
        numero = request.form["numero1"] + request.form["numero2"] +\
                 request.form["numero3"] + request.form["numero4"]
        nom = request.form["nom"]
        date_cb = request.form["date_cb1"] + request.form["date_cb2"]
        crypto = request.form["crypto"]

        cur.execute("select ajout_moyens_paiement(" + str(session["user"]) +
                                                  ", '" + type_cb + "'" +
                                                  "," + numero +
                                                  ", '" + nom + "'" +
                                                  "," + date_cb +
                                                  "," + crypto +
                                                  ")" )
        conn.commit()
        return redirect("/compte/moyens_paiement/")
    else:
        return redirect("/non_connecte/")


@app.route('/compte/ajout_adresse_facturation/', methods=['GET'])
def ajout_adresse_facturation():
    if "user" in session:
        section = "ajout_adresse_facturation.html"
        l_css = ["ajout_adresse_facturation.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css,
                               user=session['user'], vendeur=session["vendeur"])
    else:
        return redirect('/non_connecte/')


@app.route('/compte/ajout_adresse_facturation/', methods=['POST'])
def ajout_adresse_facturation_():
    if "user" in session:
        nom_prenom = request.form["nom_prenom"]
        adr1 = request.form["adr1"]
        adr2 = request.form["adr2"]
        ville = request.form["ville"]
        pays = request.form["pays"]
        cp = request.form["cp"]

        cur.execute("select ajout_adresse_facturation(" + str(session["user"]) +
                                                      ", '" + nom_prenom + "'" +
                                                      ", '" + adr1 + "'" +
                                                      ", '" + adr2 + "'" +
                                                      ", '" + ville + "'" +
                                                      ", '" + pays + "'" +
                                                      "," + cp +
                                                      ")" )
        conn.commit()
        return redirect("/compte/adresse_facturation/")
    else:
        return redirect("/non_connecte/")


@app.route('/compte/ajout_adresse_livraison/', methods=['GET'])
def ajout_adresse_livraison():
    if "user" in session:
        section = "ajout_adresse_livraison.html"
        l_css = ["ajout_adresse_livraison.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css,
                               user=session['user'], vendeur=session["vendeur"])
    else:
        return redirect('/non_connecte/')


@app.route('/compte/ajout_adresse_livraison/', methods=['POST'])
def ajout_adresse_livraison_():
    if "user" in session:
        nom_prenom = request.form["nom_prenom"]
        adr1 = request.form["adr1"]
        adr2 = request.form["adr2"]
        ville = request.form["ville"]
        pays = request.form["pays"]
        cp = request.form["cp"]

        cur.execute("select ajout_adresse_livraison(" + str(session["user"]) +
                                                      ", '" + nom_prenom + "'" +
                                                      ", '" + adr1 + "'" +
                                                      ", '" + adr2 + "'" +
                                                      ", '" + ville + "'" +
                                                      ", '" + pays + "'" +
                                                      "," + cp +
                                                      ")" )
        conn.commit()
        return redirect("/compte/adresse_livraison/")
    else:
        return redirect("/non_connecte/")


@app.route('/compte/ameliorer_vendeur/', methods=['GET'])
def ameliorer_vendeur():
    if "user" in session:
        section = "ameliorer_vendeur.html"
        l_css = ["ameliorer_vendeur.css"]
        return render_template('layout_base.html',
                               section=section, l_css=l_css,
                               user=session['user'], vendeur=session["vendeur"])
    else:
        return redirect('/non_connecte/')


@app.route('/compte/ameliorer_vendeur/', methods=['POST'])
def ameliorer_vendeur_():
    if "user" in session:
        nom = request.form["nom"]
        adr = request.form["adr"]
        mail_c = request.form["mail_c"]
        mail_d = request.form["mail_d"]
        desc = request.form["desc"]

        cur.execute("select * from ameliorer_vendeur(" +  "'" + nom + "'" +
                                                      ", '" + adr + "'" +
                                                      ", '" + mail_c + "'" +
                                                      ", '" + mail_d + "'" +
                                                      ", '" + desc + "'" +
                                                      ", " + str(session["user"]) +
                                                      ")" )
        vendeur = cur.fetchall()
        session["vendeur"] = vendeur[0][0]
        conn.commit()
        return redirect("/compte/mes_informations/")
    else:
        return redirect("/non_connecte/")


def check_vendeur(pnum):
    cur.execute("select * from check_vendeur( "+ str(pnum) +" )" )
    vendeur = cur.fetchall()
    if vendeur[0][0]:
        return vendeur[0][0]
    else:
        return -1

@app.route("/compte/sup_moyens_paiement/", methods=["POST"])
def sup_moyens_paiement():
    if "user" in session:
        num = request.form["num"]
        cur.execute("select sup_moyens_paiement(" + str(num) + ")")
        conn.commit()
        return redirect("/compte/moyens_paiement")
    else:
        return redirect("/non_connecte")

@app.route("/compte/sup_adr_facturation/", methods=["POST"])
def sup_adr_facturation():
    if "user" in session:
        num = request.form["num"]
        cur.execute("select sup_adr_facturation(" + str(num) + ")")
        conn.commit()
        return redirect("/compte/adresse_facturation")
    else:
        return redirect("/non_connecte")

@app.route("/compte/sup_adr_livraison/", methods=["POST"])
def sup_adr_livraison():
    if "user" in session:
        num = request.form["num"]
        cur.execute("select sup_adr_livraison(" + str(num) + ")")
        conn.commit()
        return redirect("/compte/adresse_livraison")
    else:
        return redirect("/non_connecte")


@app.route("/compte/ajout_article/", methods=["GET"])
def ajout_article():
    if "user" in session:
        if session["vendeur"] != -1:
            section = "ajout_article.html"
            l_css = ["ajout_article.css"]
            return render_template('layout_base.html',
                                   section=section, l_css=l_css,
                                   user=session['user'],
                                   vendeur=session["vendeur"])
        else:
            abort(404)
    else:
        return redirect("/non_connecte")

@app.route("/compte/ajout_article/", methods=["POST"])
def ajout_article_():
    if "user" in session:
        if session["vendeur"] != -1:

            libelle = request.form["libelle"]
            desc = request.form["desc"]
            point = 0
            prix = request.form["prix"]
            qte = request.form["qte"]
            date_mise = time.strftime("%d/%m/%y", time.localtime())

            cur.execute("select * from ajout_article('" + libelle + "'" +
                                                      ", '" + desc + "'" +
                                                      "," + str(point) +
                                                      "," + str(prix) +
                                                      "," + str(qte) +
                                                      ", '" + date_mise + "'" +
                                                      "," + str(session["vendeur"]) +
                                                      ")" )
            num_a = cur.fetchall()[0][0]
            conn.commit()

            type_a = request.form["type_a"]
            cur.execute("select ajout_tag('type composant'" +
                                          ", '" + str(type_a) + "'" +
                                          "," + str(num_a) +
                                          ")")
            conn.commit()
            flash("L'article a bien été ajouté")
            return redirect("/compte/ajout_article")
        else:
            abort(404)
    else:
        return redirect("/non_connecte")









@app.route('/compte/moyens_paiement/')
def redir_moyens_paiement():
    return redirect('/compte/moyens_paiement/0')

@app.route('/compte/adresse_facturation/')
def redir_adr_facturation():
    return redirect('/compte/adresse_facturation/0')

@app.route('/compte/adresse_livraison/')
def redir_adr_livraison():
    return redirect('/compte/adresse_livraison/0')

@app.route('/compte/')
def redir_compte():
    return redirect('/compte/mes_informations/')

@app.route('/non_connecte/')
def non_connecte():
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




@app.route('/panier/')
def panier():
    if ('user' in session):
        query = "SELECT numArticle, nbArticlePanier FROM ArticlePanier\
                WHERE numPanier=\
                (SELECT numPanier FROM Panier\
                WHERE numClient='"+str(session['user'])+"'\
                AND dateCommandePanier is null);"
        cur.execute(query)
        panier = cur.fetchall()
        i = 0
        for article in panier:
            query = "SELECT LibelléArticle FROM Article\
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
                     WHERE numClient='"+str(session['user'])+"'\
                     AND dateCommandePanier is null;"
            cur.execute(query)
            numP = cur.fetchone()[0]
            nbA = request.form['nbArticle']
            cur.execute("INSERT INTO ArticlePanier\
                        VALUES ('"+str(numP)+"',\
                        '"+str(id_article)+"', '"+str(nbA)+"')")
            conn.commit()
            derniere_modif_panier()
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
                infos = recup_infos()
                section = "commande_panier.html"
                l_css = ["panier.css"]
                return render_template("layout_base.html", section=section,
                                       l_css=l_css, user=session['user'],
                                       infos=infos)
            flash(u"Veuillez remplir toutes vos informations\
                  de paiement et de livraison.")
            return redirect(url_for("redir_compte"))
        else:
            return redirect(url_for('non_connecte'))
    else:
        abort(404)


@app.route('/paiement_effectue/', methods=['GET'])
def paiement_effectue():
    flash(u"Votre commande a bien été effectuée :)")
    cur.execute("UPDATE Panier\
                SET dateCommandePanier=\
                '"+time.strftime('%d/%m/%y', time.localtime())+"'\
                WHERE numClient='"+str(session['user'])+"'\
                AND dateCommandePanier is null;")
    set_panier()
    return redirect(url_for('redir_compte'))


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
                session["vendeur"] = check_vendeur(session["user"])
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
    cur.execute("INSERT INTO CartePaiement (numClient)\
                VALUES ('"+str(session['user'])+"');")
    conn.commit()


def set_panier():
    cur.execute("SELECT numAdresseFacturation FROM AdresseFacturation\
                where NumAdresseFacturation IN (select NumAdresseFacturation\
                                              from PossedeAdrFacturation\
                                              where NumClient = '"+str(session['user'])+"');")
    numFact = cur.fetchone()[0]

    cur.execute("SELECT numAdresseLivraison FROM AdresseLivraison\
                where NumAdresseLivraison IN (select NumAdresseLivraison\
                                              from PossedeAdrLivraison\
                                              where NumClient = '"+str(session['user'])+"');")
    numLivr = cur.fetchone()[0]

    cur.execute("SELECT numCartePaiement FROM CartePaiement\
                where NumCartePaiement IN (select NumCartePaiement\
                                              from PossedeCartePaiement\
                                              where NumClient = '"+str(session['user'])+"');")
    numCarte = cur.fetchone()[0]

    cur.execute("INSERT INTO Panier (numClient, dateCréationPanier,\
                numAdresseFacturation, numAdresseLivraison, numCartePaiement)\
                VALUES ('"+str(session['user'])+"',\
                '"+time.strftime('%d/%m/%y', time.localtime())+"',\
                '"+str(numFact)+"', '"+str(numLivr)+"', '"+str(numCarte)+"');")
    conn.commit()


def derniere_modif_panier():
    cur.execute("UPDATE Panier SET dateDernièreModifPanier=\
                '"+time.strftime('%d/%m/%y', time.localtime())+"'\
                WHERE numClient='"+str(session['user'])+"'\
                AND dateCommandePanier is null;")
    conn.commit()


def verif_info():
    cur.execute("SELECT * FROM AdresseLivraison\
                where NumAdresseLivraison IN (select NumAdresseLivraison\
                                              from PossedeAdrLivraison\
                                              where NumClient = '"+str(session['user'])+"');")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    cur.execute("SELECT * FROM AdresseFacturation\
                where NumAdresseFacturation IN (select NumAdresseFacturation\
                                              from PossedeAdrFacturation\
                                              where NumClient = '"+str(session['user'])+"');")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    cur.execute("SELECT * FROM CartePaiement\
                where NumCartePaiement IN (select NumCartePaiement\
                                              from PossedeCartePaiement\
                                              where NumClient = '"+str(session['user'])+"');")
    l_infos = cur.fetchall()
    for info in l_infos:
        if (None in info):
            return False
    return True


def recup_infos():
    cur.execute("SELECT nomprénomadresselivraison,\
                adresseligne1adresselivraison,\
                adresseligne2adresselivraison, villeadresselivraison,\
                paysadresselivraison, codepostaladresselivraison\
                FROM AdresseLivraison\
                where NumAdresseLivraison IN (select NumAdresseLivraison\
                                              from PossedeAdrLivraison\
                                              where NumClient = '"+str(session['user'])+"');")
    infos = cur.fetchall()
    cur.execute("SELECT nomprénomadressefacturation,\
                adresseligne1adressefacturation,\
                adresseligne2adressefacturation, villeadressefacturation,\
                paysadressefacturation, codepostaladressefacturation\
                FROM AdresseFacturation\
                where NumAdresseFacturation IN (select NumAdresseFacturation\
                                              from PossedeAdrFacturation\
                                              where NumClient = '"+str(session['user'])+"');")
    infos.append(cur.fetchone())
    cur.execute("SELECT numéroCartePaiement FROM CartePaiement\
                where NumCartePaiement IN (select NumCartePaiement\
                                              from PossedeCartePaiement\
                                              where NumClient = '"+str(session['user'])+"');")
    infos.append(cur.fetchone())
    return infos

if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()
    cur.execute("SET search_path TO chtulhu")
    app.debug = True
    app.secret_key = "lolololololol"
    app.run()
