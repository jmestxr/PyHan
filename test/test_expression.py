import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

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
(((((1)))))\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(((((1)))))
"""
    assert actual == expected

def test_arithmetic():
    input = """\
1+1*1/1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
1+1*1/1
"""
    assert actual == expected

def test_arithmeticWithVariable():
    input = """\
数目 = 1
数目+1*数目/1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15=1
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15+1\
*shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15/1
"""
    assert actual == expected

def test_arithmeticWithBrackets1():
    input = """\
(1+(1)*1/((1)))\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(1+(1)*1/((1)))
"""
    assert actual == expected

def test_arithmeticWithBrackets2():
    input = """\
(1+1)*((1/1))\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(1+1)*((1/1))
"""
    assert actual == expected

def test_arithmeticWithBrackets3():
    input = """\
7 + 3 * (10 / (12 / (3 + 1) - 1))\
"""
    actual = mock_compiler.compile(input)
    expected = """\
7+3*(10/(12/(3+1)-1))
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

def test_greaterThan():
    input = """\
2>1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2>1
"""
    assert actual == expected

def test_lessThan():
    input = """\
2<1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2<1
"""
    assert actual == expected

def test_greaterThanEqual():
    input = """\
2>=1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2>=1
"""
    assert actual == expected

def test_lessThanEqual():
    input = """\
2<=1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2<=1
"""
    assert actual == expected

def test_equalEqual():
    input = """\
2==1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2==1
"""
    assert actual == expected

def test_notEqual():
    input = """\
2!=1\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2!=1
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

def test_logicalAnd():
    input = """\
2 与 3\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2 and 3
"""
    assert actual == expected

def test_logicalOr():
    input = """\
2 或 3\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2 or 3
"""
    assert actual == expected

def test_logicalNot():
    input = """\
非 2\
"""
    actual = mock_compiler.compile(input)
    expected = """\
not 2
"""
    assert actual == expected

def test_logicalMixed():
    input = """\
1 与 非 2\
"""
    actual = mock_compiler.compile(input)
    expected = """\
1 and not 2
"""
    assert actual == expected

def test_logicalAndWithVariable():
    input = """\
数目 = 1
数目 与 2\
"""
    actual = mock_compiler.compile(input)
    expected = """\
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15=1
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15 and 2
"""
    assert actual == expected

def test_logicalAndError():
    input = """\
与 3\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)

    assert output.type == SystemExit

def test_logicalMixedError():
    input = """\
1 与 或 3\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)

    assert output.type == SystemExit

def test_logicalWithBrackets():
    input = """\
(2 与 3)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
(2 and 3)
"""
    assert actual == expected

def test_arithmeticWithLogical():
    input = """\
2 + (非 3)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2+(not 3)
"""
    assert actual == expected

def test_arithmeticWithLogicalError():
    input = """\
2 + 非 3\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)

    assert output.type == SystemExit

def test_comparisonWithLogical():
    input = """\
2 > (非 3)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
2>(not 3)
"""
    assert actual == expected

def test_comparisonWithLogicalError():
    input = """\
2 > 非 3\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)

    assert output.type == SystemExit
