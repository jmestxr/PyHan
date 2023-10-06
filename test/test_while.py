import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

def test_while():
    input = """\
当 1 > 2:
    印出("1 > 2")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
while 1>2:
    print("1 > 2")
"""
    assert actual == expected


def test_nestedWhile():
    input = """\
当 1 > 2:
    当 1 > 2:
        印出("1 > 2")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
while 1>2:
    while 1>2:
        print("1 > 2")
"""
    assert actual == expected

def test_break():
    input = """\
当 1 > 2:
    印出("1 > 2")
    中断\
"""
    actual = mock_compiler.compile(input)
    expected = """\
while 1>2:
    print("1 > 2")
    break
"""
    assert actual == expected

def test_continue():
    input = """\
当 1 > 2:
    印出("1 > 2")
    继续\
"""
    actual = mock_compiler.compile(input)
    expected = """\
while 1>2:
    print("1 > 2")
    continue
"""
    assert actual == expected

def test_missingStatementError():
    input = """\
当 1 > 2:\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_noColonError():
    input = """\
当 1 > 2
    印出("1>2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_emptyStatementInWhileError():
    input = """\
当 1 > 2
    \
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_breakOutsideLoopError():
    input = """\
中断\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_continueOutsideLoopError():
    input = """\
继续\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit
    