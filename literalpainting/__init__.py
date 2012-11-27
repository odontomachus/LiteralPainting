# -*- coding: utf-8 -*-
import sys
import re

from nltk.data import load as data_load
from nltk.grammar import (Production, FeatureGrammar, FeatStructNonterminal)
from nltk.parse.earleychart import FeatureEarleyChartParser
from nltk.featstruct import FeatStructParser

import bottle
from bottle import jinja2_view as view
from bottle import route, post, get, run, request
from bottle import static_file

from beaker.middleware import SessionMiddleware

import history

import draw
from draw import Drawable

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './tmp/sessions',
    'session.auto': True,
}

app = SessionMiddleware(bottle.app(), session_opts)

grammar = data_load('file:commandParser.fcfg')
productions = grammar.productions()

RE_INT = re.compile(r'\d+$')

feature_parser = FeatStructParser()

def preprocess(command):
    """ Decapitalize first letter of sentence. """
    tokens = command.strip(' .?!').split()
    if tokens[0] not in ('I'):
        tokens[0] = tokens[0].lower()
    return tokens

def num_production(n):
    """ Return a production NUM -> n """
    lhs = FeatStructNonterminal('NUM')
    pl = 'sg' if n == '1' else 'pl'
    lhs.update(feature_parser.parse('[NUM={pl}, SEM=<\V.V({num})(identity)>]'.format(pl=pl, num=n)))
    return Production(lhs, [n])

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
    tokens = preprocess(command)

    # Make a local copy of productions
    lproductions = list(productions)

    # find all integers
    ints = set(filter(RE_INT.match, tokens))
    # Add a production for every integer
    lproductions.extend(map(num_production, ints))

    # Make a local copy of the grammar with extra productions
    lgrammar = FeatureGrammar(grammar.start(), lproductions)

    # Load grammar into a parser
    parser = FeatureEarleyChartParser(lgrammar, trace=0)

    try:
        trees = parser.nbest_parse(tokens)
        if not trees:
            errors = ['I could not parse this sentence.']
        elif len(trees) > 1:
            errors = ['This sentence had multiple interpretations.']
        else:
            status = True
            try:
                # Setup session for history
                session = bottle.request.environ.get('beaker.session')
                history.history = session.get('history', [])
                session['history'] = history.history

                commands = eval(str(trees[0].node['SEM']), draw.functions)
                data = {
                    'sentence': request.forms.get('command'),
                    'tree': trees[0],
                    # Eval semantics in draw namespace
                    'actions': commands,
                    }

            except AssertionError as e:
                status = False
                errors = ['I got the following semantic error: <br /><pre>' + str(e) + '</pre>']

    except ValueError as e:
        status = False
        errors = ['I got the following error: <br /><pre>' + str(e) + '</pre>']
    return {'status':status, 'errors':errors, 'data':data}



@route('/static/<filepath:path>')
def server_static(filepath):
    """ Serve static files (css/js/images). """
    return static_file(filepath, root='./static')

if __name__ == '__main__':
    run(app=app, host='localhost', port=8080, debug=True, reloader=True)
