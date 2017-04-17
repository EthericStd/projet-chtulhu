#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
app = Flask(__name__)


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
