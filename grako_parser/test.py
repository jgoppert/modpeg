import unittest

from .parser import ModelicaParser


class Test(unittest.TestCase):

    def setUp(self):
        self.parser = ModelicaParser()
        pass

    def test_basic(self):
        res = self.parser.parse('''
            within mypackage;
        ''', rule_name='stored_definition')
        print res
