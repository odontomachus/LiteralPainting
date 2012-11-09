# -*- coding: utf-8 -*-
import sys
import re
import gettext
import random

from nltk.data import load as data_load
from nltk.grammar import (Production, FeatureGrammar, FeatStructNonterminal)
from nltk.parse.earleychart import FeatureEarleyChartParser
from nltk.featstruct import FeatStructParser
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

RE_INT = re.compile(r'\d+$')

feature_parser = FeatStructParser()

def num_production(n):
    """ Return a production NUM -> n """
    lhs = FeatStructNonterminal('NUM')
    lhs.update(feature_parser.parse('[NUM=pl, SEM=<\V.V({num})(identity)>]'.format(num=n)))
    return Production(lhs, [n])

def rectangle(start, end):
    return start + end + ('rectangle',)

def line(start, end):
    return start + end + ('line',)

def draw(x):
    return x

def circle(at, rad):
    return at + rad + ('circle',)

def radius(rad):
    return (rad,)

def diameter(rad):
    return (int(rad)//2,)

def pixel(p):
    return p

def loc(x,y):
    return (x,y)

def identity(x):
    return x

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

    # preprocess
    command = request.forms.get('command').strip(' .?!')
    tokens = command.split()

    lproductions = list(productions)

    # find all integers
    ints = set(filter(RE_INT.match, command.split()))
    # Add a production for every integer
    lproductions.extend(map(num_production, ints))

    lgrammar = FeatureGrammar(grammar.start(), lproductions)

    lgrammar._lexical_index = IntDict(lgrammar._lexical_index)
    parser = FeatureEarleyChartParser(lgrammar, trace=0)

    try:
        trees = parser.nbest_parse(command.split())
        if not trees:
            errors = ['I could not parse this sentence.']
        elif len(trees) > 1:
            errors = ['This sentence had multiple interpretations.']
        else:
            status = True
            data = {
                'tree': trees[0],
                # @TODO
                'actions': [eval(str(trees[0].node['SEM']))]
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
