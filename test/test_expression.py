import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

def test_numberWithoutBrackets():
    input = """\
1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
1
"""

    assert actual == expected

def test_numberWithBrackets():
    input = """\
(1)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(1)
"""

    assert actual == expected

def test_arithmeticWithoutBrackets():
    input = """\
1+1*1/1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
1+1*1/1
"""

    assert actual == expected

def test_arithmeticWithBrackets():
    input = """\
(1+1*1/1)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(1+1*1/1)
"""

    assert actual == expected

def test_variableWithoutBrackets():
    input = """\
数目 = 1
数目\
"""
    actual = mock_compiler.compile(input)
    expected = """\
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15=1
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15
"""

    assert actual == expected

def test_variableWithBrackets():
    input = """\
数目 = 1
(数目)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15=1
(shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15)
"""

    assert actual == expected

def test_comparisonWithoutBrackets():
    input = """\
2>1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2>1
"""

    assert actual == expected

def test_comparisonWithBrackets():
    input = """\
(2>1)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(2>1)
"""

    assert actual == expected