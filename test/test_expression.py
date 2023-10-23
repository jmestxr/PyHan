import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

# ======================================================================
# NUMBER
# ======================================================================
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

def test_equalequal():
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

# ======================================================================
# STRING
# ======================================================================

def test_string():
    input = """\
"你好"\
"""
    actual = mock_compiler.compile(input)
    expected = """\
"你好"
"""
    assert actual == expected

def test_arithmeticWithString():
    input = """\
"你好" + "hello"\
"""
    actual = mock_compiler.compile(input)
    expected = """\
"你好"+"hello"
"""
    assert actual == expected

def test_comparisonWithString():
    input = """\
"你好" > "hello"\
"""
    actual = mock_compiler.compile(input)
    expected = """\
"你好">"hello"
"""
    assert actual == expected

def test_logicalWithString():
    input = """\
"你好" 与 "hello"\
"""
    actual = mock_compiler.compile(input)
    expected = """\
"你好" and "hello"
"""
    assert actual == expected


# ======================================================================
# BOOLEAN
# ======================================================================

def test_true():
    input = """\
真\
"""
    actual = mock_compiler.compile(input)
    expected = """\
True
"""
    assert actual == expected

def test_false():
    input = """\
假\
"""
    actual = mock_compiler.compile(input)
    expected = """\
False
"""
    assert actual == expected

def test_arithmeticWithBoolean():
    input = """\
真 + 假\
"""
    actual = mock_compiler.compile(input)
    expected = """\
True+False
"""
    assert actual == expected

def test_comparisonWithBoolean():
    input = """\
真 > 假\
"""
    actual = mock_compiler.compile(input)
    expected = """\
True>False
"""
    assert actual == expected

def test_logicalWithBoolean():
    input = """\
真 与 假\
"""
    actual = mock_compiler.compile(input)
    expected = """\
True and False
"""
    assert actual == expected


# ======================================================================
# IDENTIFIER / VARIABLE
# ======================================================================

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

def test_comparisonWithVariable():
    input = """\
阳 = 5
洋 = 5
洋 == 阳\
"""
    actual = mock_compiler.compile(input)
    expected = """\
yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17=5
yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b=5
yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b==yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17
"""
    assert actual == expected

def test_logicalWithVariable():
    input = """\
阳 = 5
洋 = 5
阳 与 洋\
"""
    actual = mock_compiler.compile(input)
    expected = """\
yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17=5
yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b=5
yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17 and yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b
"""
    assert actual == expected
    