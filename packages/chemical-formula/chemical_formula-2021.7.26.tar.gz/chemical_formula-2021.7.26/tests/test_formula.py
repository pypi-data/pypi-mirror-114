#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chemical-formula` package, formula module."""

from chemical_formula import Formula


def test_simple():
    """Testing that we can handle a simple formula."""
    f = Formula("H4C")
    assert f.formula == "CH4"


def test_parentheses():
    """Testing that we can handle simple parentheses."""
    f = Formula("(H2SO4)4")
    assert f.formula == "H8O16S4"


def test_complex_parentheses():
    """Testing that we can handle simple parentheses."""
    f = Formula("CH3C(CH3)(CH3)CH2(CH(CH3)2)")
    assert f.formula == "C8H18"
