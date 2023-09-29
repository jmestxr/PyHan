# Py汉 (PyHan), a.k.a. Chinese Python

(This project is still Work in Progress)

Write and execute Python code in Simplified Chinese syntax!

```
 :::::::;,                
::        ;:                      
::        ::               ';,           
::       ,;'                 ';,    ,;::::::::::;,      
::::::::;'    ::      ::             ;;        ;; 
::             ::    ::     ';,       ;;      ;;    
::              ;;  ;;        ';       ':,  ,:'     
::               '::'            .:      '::'
::                ;;            ;'      .:'':.
                 ;;          ,;'      ,;'    ';,                 
             ,:;''        :;'      ,:;'        ';:,

```

## Credits

Starter code is obtained from [this tutorial](https://austinhenley.com/blog/teenytinycompiler1.html). Special thanks 🎉


## Syntax

Here are the list of syntax currently supported:

- `print` statement - `印出`
- `if` statement - `如果`
- `while` loop - `当`
- Logical operators (`and`, `or`, `not`) - `与`, `或`, `非`
- Variable assignment
- Declaring variables in Chinese characters
- Basic arithmetic (`+`, `-`, `*`, `/`)
- Parenthesis

## Example

#### **`example.pyhan`**
```
x = 1
当 x < 5:
  印出("Hello，世界！")
  x = x + 1
```
compiles to

#### **`example.py`**
```
x = 1
while x < 5:
  print("Hello，世界！")
  x = x + 1
```

### Usage

1. Clone this repo.
1. Run `python setup.py sdist` in the root directory.
1. Confirm that the package is installed correctly by running `pyhan` command:
   
<img width="688" alt="Screenshot 2023-09-29 at 6 31 36 PM" src="https://github.com/jmestxr/PyHan/assets/87931905/0b4afc19-e090-40c7-ac1a-7da2059418b4">

#### Example:
To execute the above `example.pyhan` script directly, run

```
pyhan example.pyhan
```

To compile .pyhan script without executing, use the `--compile` or `-c` option. The compiled .py script will be saved to `./out.py` by default.

```
pyhan example.pyhan -c
```

You can specify the desired file path of the compiled .py script using the `--output` or `-o` option.

```
pyhan example.pyhan -c -o example.py
```


## Dev Guide

### Testing
Unit test cases are written with pytest. All test files are stored in `/test` directory. 

Run `pytest` to run all tests.
