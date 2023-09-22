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
- Variable assignment
- Declaring variables in Chinese characters
- Basic arithmetic (`+`, `-`, `*`, `/`)

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

## Dev Guide

### Testing
Unit test cases are written with pytest. All test files are stored in `/test` directory. 

Run `pytest` to run all tests.
