import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

def test_if():
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

def test_ifElif():
    input = """\
如果 1 > 2:
    印出("1 > 2")
或则 3 > 4:
    印出("3 > 4")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1 > 2")
elif 3>4:
    print("3 > 4")
"""
    assert actual == expected

def test_ifElse():
    input = """\
如果 1 > 2:
    印出("1 > 2")
否则:
    印出("1 <= 2")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1 > 2")
else:
    print("1 <= 2")
"""
    assert actual == expected

def test_ifElifElse():
    input = """\
如果 1 > 2:
    印出("1 > 2")
或则 3 > 4:
    印出("3 > 4")
否则:
    印出("boop")
\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1 > 2")
elif 3>4:
    print("3 > 4")
else:
    print("boop")
"""
    assert actual == expected

def test_nestedIfElifElse():
    input = """\
如果 1 > 2:
    印出("1 > 2")
    如果 1 > 2:
        印出("1 > 2")
    或则 3 > 4:
        印出("3 > 4")
    否则:
        印出("boop")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1 > 2")
    if 1>2:
        print("1 > 2")
    elif 3>4:
        print("3 > 4")
    else:
        print("boop")
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

def test_emptyStatementInIfError():
    input = """\
如果 1 > 2
    \
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_elifWithmissingIfError():
    input = """\
或则 1 > 2:
    印出("1 > 2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_elseWithmissingIfError():
    input = """\
否则:
    印出("1 > 2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit
