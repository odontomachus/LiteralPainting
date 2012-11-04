# -*- coding: utf-8 -*-
import sys
import re
import gettext

from nltk import load_parser

from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import route, post, get, run, redirect, request, Bottle
from bottle import Jinja2Template
from bottle import static_file

parser = load_parser('file:commandParser.fcfg', trace=0)

@get('/')
@view('templates/base.jinja2')
def home():
    """ Displays the home view. """
    return {}

@post('/ajax/parse')
def ajax_parse():
    return parse()

@post('/parse')
@view('templates/base.jinja2')
def std_parse():
    return parse()

def parse():
    """ Parse a command and return a json string.
    If parse is successful, returns a tuple (true, [instructions]).
    If parse is not successful, returns a tuple (false, [errors]).
    """
    status = False
    data = {}
    errors = []

    command = request.forms.get('command')
    # preprocess
    command.strip(' .')
    try:
        trees = parser.nbest_parse(command.split())
        if not trees:
            errors = ['I could not parse this sentence']
        elif len(trees) > 1:
            errors = ['This sentence had multiple interpretations.']
        else:
            status = True
            data = {'tree': trees[0]}
    except ValueError as e:
        errors = ['I got the following error: <br /><pre>' + str(e) + '</pre>']
    return {'status':status, 'errors':errors, 'data':data}


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
