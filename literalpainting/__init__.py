# -*- coding: utf-8 -*-
import sys
import re
import gettext
import random

from nltk.data import load as data_load
from nltk.grammar import (Production, FeatureGrammar)
from nltk.parse.earleychart import FeatureEarleyChartParser

from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import route, post, get, run, redirect, request, Bottle
from bottle import Jinja2Template
from bottle import static_file

class Integer(object):
    """ A class that always returns true if it is compared to a number. """
    def __hash__(self):
        return hash(getattr(self, 'value', 0))

    def __eq__(self, other):
        try:
            assert int(other) > 1
            self.value = other
            return True
        except:
            return False

    def __ne__(self, other):
        try:
            assert int(other)
            self.value = other
            return False
        except:
            return True


class IntDict(dict):
    """ Dict which returns i for d[i] if i can be converted to an integer. """
    def __getitem__(self, key):
        try:
            return int(key)
        except:
            return super(IntDict, self).__getitem__(key)

    def get(self, key, value=None):
        try:
            int(key) 
            return key
        except:
            return super(IntDict, self).get(key, value)

# In order to accept all numbers, add a production to a terminal which
# accepts "all" objects which can be converted to an integer (eg '100').
grammar = data_load('file:commandParser.fcfg')
productions = grammar.productions()

# Trick production
# 'NUM -> <integer>'
production = Production(productions[-1].lhs(), [Integer()])
productions.append(production)

#print(type(grammar.start()))

# Rebuild grammar
grammar = FeatureGrammar(grammar.start(), productions)
grammar._lexical_index = IntDict(grammar._lexical_index)
parser = FeatureEarleyChartParser(grammar, trace=3)


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
            errors = ['I could not parse this sentence.']
        elif len(trees) > 1:
            for tree in trees:
                print tree
            errors = ['This sentence had multiple interpretations.']
        else:
            status = True
            data = {
                'tree': trees[0],
                # @TODO
                'actions': [(random.randint(10,790), random.randint(10,390), 10, 'circle')]
                }
    except ValueError as e:
        errors = ['I got the following error: <br /><pre>' + str(e) + '</pre>']
    return {'status':status, 'errors':errors, 'data':data}


@route('/static/<filepath:path>')
def server_static(filepath):
    """ Serve static files (css/js/images). """
    return static_file(filepath, root='./static')



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
