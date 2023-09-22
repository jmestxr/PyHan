import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

def test_basicComparison():
    input = """\
如果 1 > 2:
    印出("1 > 2")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1 > 2")
"""

    assert actual == expected

def test_variableComparison():
    input = """\
阳 = 5
洋 = 5
如果 洋 == 阳:
    印出(洋)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17=5
yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b=5
if yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b==yang_65e20c27a154dfe12117f65b731513990bddf795faeb56db0a733734373aef17:
    print(yang_49a1fcbe2bc4c581f3726bbddea023f53ba4023239e28e3ec7328bd59a79893b)
"""

    assert actual == expected

def test_missingStatementError():
    input = """\
如果 1 > 2:\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_noColonError():
    input = """\
如果 1 > 2
    印出("1>2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit
