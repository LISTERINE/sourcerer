#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sourcerer
----------------------------------

Tests for `sourcerer` module.
"""

from sourcerer import Statement, Name
from inspect import isgenerator
import pytest

# Test Base


class TestStatment():

    def test_defaults(self):
        s = Statement()
        assert s.code == ''
        assert s.scope == []
        assert s.whitespace == '    '
        assert s.line_ending == ''

    def test_add_child(self):
        s = Statement()
        s2 = Statement()
        s.add_child(s2)
        assert s2 in s.scope

    def test_add_children(self):
        s = Statement()
        s21 = Statement()
        s22 = Statement()
        s2 = [s21, s22]
        s3 = Statement()
        s.add_children([s2, s3])
        assert s.scope[0] is s21
        assert s.scope[1] is s22
        assert s.scope[2] is s3

    def test_create_lineage(self):
        s = Statement()
        s21 = Statement()
        s22 = Statement()
        s2 = [s21, s22]
        s3 = Statement()
        s.create_lineage([s2, s3])
        assert s.scope[0] is s21
        assert s.scope[1] is s22
        child = s.scope[1]
        assert child.scope[0] is s3

    def test_from_parent(self):
        s = Statement()
        s2 = Statement()
        s2.from_parent(s)
        assert s2 in s.scope

    def test_from_lineage(self):
        s = Statement()
        s2 = Statement()
        s3 = Statement()
        s3.from_lineage([s, s2])
        assert s.scope[0] is s2
        child = s.scope[0]
        assert child.scope[0] is s3

    def test_build_renderer(self):
        s = Statement()
        renderer = s.build_renderer()
        print type(renderer)
        assert isgenerator(renderer)

    def test_render(self):
        s_base = Statement()
        s = Statement(code='for i in range(10):')
        s2 = Statement(code='print i')
        s3 = Statement(code='print "done"')
        s_base.create_lineage([s,s2])
        s_base.add_child(s3)
        test_code = '\n'.join(s_base) # join with \n to replicate a document output
        train_code = '\nfor i in range(10):\n    print i\nprint "done"'
        assert test_code == train_code

    def test_to_statement(self):
        init = Statement("TESTING")
        from_string = Statement.to_statement("TESTING")
        from_state = Statement.to_statement(init)
        from_int = Statement.to_statement(4)
        assert isinstance(from_string, Statement)
        assert from_state is init
        assert isinstance(from_int, Statement)


class TestName():

    valid_function_names = ['_func', '_Func', 'func_', 'Func_']

    invalid_int_function_names = ['1_func', '1_Func', '1func_', '1Func_']
    valid_int_function_names = valid_function_names

    invalid_punc_function_names = ['(_func', '(_Func', '(func_', '(Func_',
                                   '_func(', '_Func(', 'func_(', 'Func_(',
                                   '_(func', '_(Func', 'func(_', 'Func(_']
    valid_punc_function_names = ['_func', '_Func', 'func_', 'Func_',
                                 '_func', '_Func', 'func_', 'Func_',
                                 '_func', '_Func', 'func_', 'Func_']

    invalid_mixed_function_names = ['(1_1func', '1(_1Func', '1(1func_', '1(1Func_',
                                   '1_func(1', '_1Func1(', 'func1_(1', 'Func_1(1',
                                   '1_(1func', '_1(Func1', 'func1(1_', '1Func(_1']
    valid_mixed_function_names = ['_1func', '_1Func', 'func_', 'Func_',
                                   '_func1', '_1Func1', 'func1_1', 'Func_11',
                                   '_1func', '_1Func1', 'func11_', 'Func_1']

    def test_format(self):
        # Make sure we are getting rid of those quotes so we get name and not 'name'
        for valid in self.valid_function_names:
            assert Name(valid).__str__() == valid
            assert Name(valid) != valid

    def test_invalid_int(self):
        for invalid, valid in zip(self.invalid_int_function_names, self.valid_int_function_names):
            assert Name(invalid).__str__() == valid

    def test_invalid_punc(self):
        for invalid, valid in zip(self.invalid_punc_function_names, self.valid_punc_function_names):
            assert Name(invalid).__str__() == valid

    def test_invalid_mixed(self):
        for invalid, valid in zip(self.invalid_mixed_function_names, self.valid_mixed_function_names):
            assert Name(invalid).__str__() == valid

    def test_dont_validate(self):
        for invalid in self.invalid_mixed_function_names:
            assert Name(invalid, validate=False).__str__() == invalid


class TestStr():
    pass


class TestNum():
    pass




# Test Callables
class TestFunctionDef():
    pass


class TestDecoratorDef():
    pass


class TestClassDef():
    pass


class TestAttribute():
    pass


class TestCall():
    pass


# Test Modules


class TestDocument():
    pass

# Test Simple Statements


class TestReturn():
    pass


class TestDocString():
    pass


class TestAssignment():
    pass