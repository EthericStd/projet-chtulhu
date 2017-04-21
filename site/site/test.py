#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
app = Flask(__name__)


def connect():
    try:
        conn = psycopg2.connect(dbname="chtulhu")
        print("\nConnecté.\n")
        cur = conn.cursor()
        cur.execute("SET search_path TO chtulhu")
        return cur
    except:
        print("\n##### ERREUR DE CO #####\n")


@app.route('/')
def accueil():
    return render_template('index.html')


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
    cur = connect()
    app.run(debug=True)
