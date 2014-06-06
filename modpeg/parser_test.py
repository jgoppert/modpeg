import unittest
from .parser import modelica_parser


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_class(self):
        modelica_parser.parse(empty_class_src)

    @unittest.skip('not working yet')
    def test_hello_world(self):
        modelica_parser.parse(hello_world_src)

empty_class_src = """
class test "hello world"
end test;
"""

hello_world_src = """
model HelloWorld "A differrential equation"
Real x(start=1);
equation
der(x) = -x;
end HelloWorld;
"""
