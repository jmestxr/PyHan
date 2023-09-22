import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

import pytest

def test_correctIndent():
    input = """\
如果 1 > 2:
    印出("1>2")
    如果 2 >= 3:
        印出("2>=3")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
    print("1>2")
    if 2>=3:
        print("2>=3")
"""

    assert actual == expected

def test_diffIndentSize():
    input = """\
如果 1 > 2:
  印出("1>2")
  如果 2 >= 3:
   印出("2>=3")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
if 1>2:
  print("1>2")
  if 2>=3:
   print("2>=3")
"""

    assert actual == expected


def test_unexpectedIndentError():
    input = """\
  印出("1>2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

def test_noIndentError():
    input = """\
如果 1 > 2:
印出("1>2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit
    
def test_incorrectIndentError():
    input = """\
当 1 > 2:
    印出("1>2")
     印出("1>2")\
"""
    with pytest.raises(SystemExit) as output:
        mock_compiler.compile(input)
    
    assert output.type == SystemExit

