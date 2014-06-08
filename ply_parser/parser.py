#!/usr/bin/env python

import os
import string
import sys

import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.classes = {}
        try:
            modname = os.path.split(
                os.path.splitext(__file__)[0])[1] \
                + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        # print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('modelica > ')
            except EOFError:
                break
            if not s:
                continue
            yacc.parse(s)
            print self.classes

    def dump(self, obj, nested_level=0, output=sys.stdout):
        spacing = '   '
        if type(obj) == dict:
            print >> output, '%s{' % ((nested_level) * spacing)
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    print >> output, '%s%s:' % \
                        ((nested_level + 1) * spacing, k)
                    self.dump(v, nested_level + 1, output)
                else:
                    print >> output, '%s%s: %s' % \
                        ((nested_level + 1) * spacing, k, v)
            print >> output, '%s}' % (nested_level * spacing)
        elif type(obj) == list:
            print >> output, '%s[' % ((nested_level) * spacing)
            for v in obj:
                if hasattr(v, '__iter__'):
                    self.dump(v, nested_level + 1, output)
                else:
                    print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
            print >> output, '%s]' % ((nested_level) * spacing)
        else:
            print >> output, '%s%s' % (nested_level * spacing, obj)

    def parse(self, s):
        res = yacc.parse(s)
        self.dump(res)


class ModelicaParser(Parser):

    keywords = (
        'algorithm', 'and', 'annotation', 'assert', 'block',
        'break', 'class', 'connect', 'connector', 'constant',
        'constrainedby', 'der', 'discrete', 'each', 'else',
        'elseif', 'elsewhen', 'encapsulated', 'end', 'enumeration',
        'equation', 'expandable', 'extends', 'external', 'false',
        'final', 'flow', 'for', 'function', 'if', 'import', 'impure',
        'in', 'initial', 'inner', 'input', 'loop', 'model', 'not',
        'operator', 'or', 'outer', 'output', 'package', 'parameter',
        'partial', 'protected', 'public', 'pure', 'record',
        'redeclare', 'return', 'stream', 'then',
        'true', 'type', 'when', 'while', 'within')

    reserved = {key: key.upper() for key in keywords}

    tokens = reserved.values() + [
        'IDENT', 'SEMI', 'STRING_COMMENT', 'EQUALS',
        'COMMA', 'UNSIGNED_NUMBER', 'STRING'
        ]

    t_ignore = ' \t'
    t_SEMI = r';'
    t_EQUALS = r'='
    t_COMMA = r','

    re_dict = {
        'digit': r'[0-9]',
        'nondigit': r'[_a-zA-Z]',
        's_escape': r'([\\][\']|[\\]["])',
        's_char': r'[^\\"]',
    }
    re_process_list = [
        ('q_char', r'{nondigit}|{digit}|\!|\#'),
        ('q_ident', r"'({q_char}|{s_escape})+'"),
        ('ident', r'({nondigit} ({digit}|{nondigit})*) | {q_ident}'),
        ('string', r'\"({s_char}|{s_escape})*\"'),
        # ('string', r'\"({s_char})*\"'),
        ('unsigned_integer', r'{digit}+'),
        ('unsigned_number', r'{unsigned_integer}([\.]{unsigned_integer}?)?'),
    ]
    for key, val in re_process_list:
        re_dict[key] = val.format(**re_dict)

    @TOKEN(re_dict['ident'])
    def t_IDENT(self, t):
        t.type = self.reserved.get(t.value, 'IDENT')
        return t

    @TOKEN(re_dict['unsigned_number'])
    def t_UNSIGNED_NUMBER(self, t):
        return t

    @TOKEN(re_dict['string'])
    def t_STRING(self, t):
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return None

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
        return None

    # Parsing rules

    # EBNF to BNF
    # {E} -> X = empty | X E
    # [E] -> X = empty | E
    # (E) -> X = E

    precedence = ()

    start = 'stored_definition'

    @staticmethod
    def list_extend(p):
        p[0] = p[1]
        if p[0] is None:
            p[0] = []
        if len(p) > 2:
            p[0].extend([p[2]])

    @staticmethod
    def store_as_list(p):
        p[0] = p[1:]

    def p_stored_definition(self, p):
        'stored_definition : within_opt class_definitions'
        p[0] = {'within': p[1], 'classes': p[2]}

    def p_class_definitions(self, p):
        '''class_definitions : class_definitions class_definition SEMI
            | empty'''
        if len(p) > 2:
            if p[1] is None:
                p[0] = {}
            else:
                p[0] = p[1]
            p[0][p[2]['name']] = p[2]

    def p_within_opt(self, p):
        '''within_opt : WITHIN name_opt SEMI
            | empty'''
        p[0] = {'name': p[1]}

    # TODO
    def p_name(self, p):
        '''name : IDENT'''
        self.store_as_list(p)

    # TODO
    def p_names(self, p):
        '''names : names '.' IDENT
            | empty'''
        self.store_as_list(p)

    def p_name_opt(self, p):
        '''name_opt : name
            | empty'''
        p[0] = '' if p[1] is None else True

    def p_class_definition(self, p):
        'class_definition : encapsulated_opt '\
            'class_prefixes class_specifier'
        encapsulated = p[1]
        prefixes = p[2]
        specifier = p[3]
        p[0] = {
            'encapsulated': encapsulated,
            'class_prefixes': prefixes,
            'name': specifier['name'],
            'comment': specifier['comment'],
            'composition': specifier['composition'],
        }

    def p_class_prefixes(self, p):
        'class_prefixes : partial_opt class_type_opt'
        p[0] = {
            'partial': p[1],
            'type': p[2]
        }

    def print_p(self, p):
        for i in range(len(p)):
            print(i, p[i])

    def p_class_specifier(self, p):
        'class_specifier : IDENT string_comment_opt composition END IDENT'
        name = p[1]
        comment = p[2]
        composition = p[3]
        name_end = p[5]
        if name != name_end:
            raise IOError(
                "Syntax error at line {:d}, "
                "class names don't match at beginning and end: "
                "{:s} {:s}".
                format(p.lineno(6), name, name_end))
        p[0] = {
            'name': name,
            'comment': comment,
            'composition': composition,
        }

    def p_composition(self, p):
        '''composition : element_list composition_list'''
        self.list_extend(p)

    def p_composition_or(self, p):
        '''composition_or : PUBLIC element_list
            | PROTECTED element_list
            | equation_section
            | algorithm_section'''
        self.store_as_list(p)

    def p_composition_list(self, p):
        '''composition_list : composition_list composition_or
            | empty'''
        self.list_extend(p)

    def p_language_specification(self, p):
        'language_specification : STRING'
        self.store_as_list(p)

    # def p_external_function_call(self, p):
    #     'external_function_call : component_reference_opt '\
    #         ' IDENT "(" expression_list ")"'
    #     self.store_as_list(p)

    def p_component_reference_opt(self, p):
        '''component_refefrence_opt : component_reference EQUALS
            | empty'''
        self.store_as_list(p)

    # TODO
    def p_component_reference(self, p):
        '''component_reference : IDENT'''
        self.store_as_list(p)

    def p_equation_section(self, p):
        'equation_section : EQUATION'
        self.store_as_list(p)

    def p_algorithm_section(self, p):
        'algorithm_section : ALGORITHM'
        self.store_as_list(p)

    def p_element_list(self, p):
        '''element_list : element_list element SEMI
            | empty'''
        if len(p) > 2:
            if p[1] is None:
                p[0] = []
            else:
                p[0] = p[1]
            p[0] += [p[2]]

    def p_element(self, p):
        'element : component_clause'
        p[0] = p[1]

    def p_component_clause(self, p):
        'component_clause : type_prefix type_specifier '\
            'array_subscripts_opt component_list'
        p[0] = {
            'prefix': p[1],
            'specifier': p[2],
            'array_subscripts': p[3],
            'component_list': p[4],
        }

    def p_type_prefix(self, p):
        'type_prefix : type_prefix_1 type_prefix_2 type_prefix_3'
        p[0] = [p[1], p[2], p[3]]

    def p_type_prefix1(self, p):
        '''type_prefix_1 : FLOW
            | STREAM
            | empty'''
        p[0] = p[1]

    def p_type_prefix2(self, p):
        '''type_prefix_2 : DISCRETE
            | PARAMETER
            | CONSTANT
            | empty'''
        p[0] = p[1]

    def p_type_prefix3(self, p):
        '''type_prefix_3 : INPUT
            | OUTPUT
            | empty'''
        p[0] = p[1]

    def p_type_specifier(self, p):
        'type_specifier : name'
        p[0] = p[1]

    # TODO
    def p_array_subscripts_opt(self, p):
        '''array_subscripts_opt : empty'''
        p[0] = p[1]

    def p_component_list(self, p):
        '''component_list : component
            | component_list COMMA component
            | empty
        '''
        if len(p) > 2:
            if p[1] is None:
                p[0] = []
            else:
                p[0] = p[1]
            p[0].extend([p[3]])
        elif p[1] is not None:
            p[0] = [p[1]]

    def p_component(self, p):
        '''component : IDENT EQUALS UNSIGNED_NUMBER'''
        p[0] = [p[1], p[2], p[3]]

    def p_class_type_opt(self, p):
        '''class_type_opt : CLASS
            | MODEL
            | RECORD
            | OPERATOR RECORD
            | BLOCK
            | CONNECTOR
            | EXPANDABLE CONNECTOR
            | TYPE
            | PACKAGE
            | PURE FUNCTION
            | IMPURE FUNCTION
            | PURE OPERATOR FUNCTION
            | IMPURE OPERATOR FUNCTION
            | OPERATOR'''
        p[0] = string.join(p[1:len(p)])

    def p_partial_opt(self, p):
        '''partial_opt : PARTIAL
            | empty'''
        p[0] = False if p[1] is None else True

    def p_encapsulated_opt(self, p):
        '''encapsulated_opt : ENCAPSULATED
            | empty'''
        p[0] = False if p[1] is None else True

    def p_string_comment_opt(self, p):
        '''string_comment_opt : STRING
            | empty'''
        p[0] = p[1] if p[1] is None else p[1]

    def p_empty(self, p):
        'empty : '
        pass

    def p_error(self, p):
        if p is None:
            print("Syntax error at root definition.")
        else:
            print("Syntax error at line {:d}, {:s}".
                  format(p.lineno, p.value))

if __name__ == '__main__':
    parser = ModelicaParser()
    parser.parse('''
    class hello1 "hello"
    end hello1;
    class hello2 "I like modelica"
        flow discrete input Real a=1, b=2;
    public
        Real c=3;
        Real d=3;
    equation
    algorithm
    end hello2;
    ''')
