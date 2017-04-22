#! /usr/bin/python
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
    cur = conn.cursor()
    cur.execute("SET search_path TO chtulhu")
    return cur

@app.route('/')
def accueil():
    section = "acceuil.html"
    l_css = ["acceuil.css"]
    return render_template('layout_base.html', section=section, l_css=l_css)

@app.route('/articles/')
def articles():
    section = "articles.html"
    l_css = ["articles.css"]
    articles = [1,2,3]
    return render_template('layout_base.html', section=section,
                                               l_css=l_css
                                               ,articles=articles)

@app.errorhandler(404)
def err(error):
    return ("ERROR {} CHTULHU NOT FOUND (lol)".format(error.code), error.code)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        query = "INSERT INTO Client (numClient, nomClient) VALUES (20, 'Marc');"
        cur.execute(query)
        query = "SELECT * FROM Client;"
        cur.execute(query)
        cur.fetchall()
        return redirect(url_for('accueil'))
    else:
        return render_template('login.html')

if __name__ == '__main__':
    #cur = connect()
    app.run(debug=True)
