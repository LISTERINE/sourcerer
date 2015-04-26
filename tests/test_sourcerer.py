#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_sourcerer
----------------------------------

Tests for `sourcerer` module.
"""

from sourcerer import Statement
from inspect import isgenerator
import pytest


class TestStatment():

    def test_defaults(self):
        s = Statement()
        assert s.code == ''
        assert s.scope == []
        assert s.whitespace == '    '
        assert s.line_ending == '\n'

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
        test_code = ''.join(s_base)
        train_code = '\nfor i in range(10):\n    print i\nprint "done"\n'
        assert test_code == train_code

    def test_to_statement(self):
        init = Statement("TESTING")
        from_string = Statement.to_statement("TESTING")
        from_state = Statement.to_statement(init)
        from_int = Statement.to_statement(4)
        assert isinstance(from_string, Statement)
        assert from_state is init
        assert isinstance(from_int, Statement)
