import unittest

import bottle

from nltk.grammar import (FeatStructNonterminal, FeatureGrammar)
from nltk.parse.earleychart import FeatureEarleyChartParser
from nltk.data import load as data_load

from literalpainting import (num_production,
                             RE_INT,
                             grammar,
                             )


grammar = data_load('file:commandParser.fcfg')
parser = FeatureEarleyChartParser(grammar, trace=0)

class GrammarMixin:
    def parse(self, command):
        ints = set(filter(RE_INT.match, command.split()))
        lproductions = list(grammar.productions())
        # Add a production for every integer
        lproductions.extend(map(num_production, ints))

        # Make a local copy of the grammar with extra productions
        lgrammar = FeatureGrammar(type(self).start, lproductions)

        # Load grammar into a parser
        parser = FeatureEarleyChartParser(lgrammar, trace=0)
        return parser.nbest_parse(command.split())

class ShapeTestCase(unittest.TestCase, GrammarMixin):
    start = FeatStructNonterminal('NP')

    def test_circle_at(self):
        test = 'a circle at 200 200 with a radius of 20 pixels'
        self.assertTrue(self.parse(test))

    def test_and(self):
        test = 'a line from 100 100 to 200 200 and a rectangle from 100 100 to 200 200'
        self.assertTrue(self.parse(test))
        
class NPTestCase(unittest.TestCase, GrammarMixin):
    start = FeatStructNonterminal('NP')
    def test_location(self):
        test = '200 200'
        self.assertTrue(self.parse(test))

    def test_length(self):
        test = '200 pixels'
        self.assertTrue(self.parse(test))


class PPTestCase(unittest.TestCase, GrammarMixin):
    start = FeatStructNonterminal('PP')

    def test_at(self):
        test = 'at 200 200'
        self.assertTrue(self.parse(test))

    def test_with(self):
        test = 'with a radius of 20 pixels'
        self.assertTrue(self.parse(test))

    def test_of(self):
        test = 'of 20 pixels'
        self.assertTrue(self.parse(test))

