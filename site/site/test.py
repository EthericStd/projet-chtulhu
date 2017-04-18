#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
import psycopg2
app = Flask(__name__)

try:
    conn = psycopg2.connect(dbname="chtulhu")
except:
    print("\n##### ERREUR DE CO #####\n")


@app.route('/')
def accueil():
    return render_template('index.html')


@app.errorhandler(404)
@app.errorhandler(500)
def err(error):
    return ("ERROR {} CHTULHU NOT FOUND (lol)".format(error.code), error.code)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
