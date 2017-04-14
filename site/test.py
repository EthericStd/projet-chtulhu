#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import *
app = Flask(__name__)


@app.route('/')
def test():
    return render_template('index.html')


@app.errorhandler(404)
def lol(error):
    return ("ERROR CHTULHU NOT FOUND (lol)", 404)

if __name__ == '__main__':
    app.run(debug=True)
