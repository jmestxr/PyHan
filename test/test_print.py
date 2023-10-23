import os
import sys

# appending the directory of mock_compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
from mocks import mock_compiler

def test_printNumber():
    input = """\
印出(-1)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
print(-1)
"""
    assert actual == expected

def test_printArithmetic():
    input = """\
印出((5+2-3))\
"""
    actual = mock_compiler.compile(input)
    expected = """\
print((5+2-3))
"""
    assert actual == expected

def test_printEnglishString():
    input = """\
印出("hello world!")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
print("hello world!")
"""
    assert actual == expected

def test_printChineseString():
    input = """\
印出("你好世界！")\
"""
    actual = mock_compiler.compile(input)
    expected = """\
print("你好世界！")
"""
    assert actual == expected

def test_printBoolean():
    input = """\
印出(真)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
print(True)
"""
    assert actual == expected

def test_printEnglishVariable():
    input = """\
number = 1
印出(number)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
number=1
print(number)
"""
    assert actual == expected

def test_printChineseVariable():
    input = """\
数目 = 1
印出(数目)\
"""
    actual = mock_compiler.compile(input)
    expected = """\
shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15=1
print(shumu_2587044c9663e086a82fb5ad144e94493ee7e879169936b5a615c0ae047e7d15)
"""
    assert actual == expected
