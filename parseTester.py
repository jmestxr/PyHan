from lex import *
from parse import *
import sys
import os

def main():
    print("Py汉 compiler")

    source = ""

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        # Remove blank lines
        for line in inputFile:
            if not line.isspace():
                source += line

    # Initialize the lexer and parser.
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() # Start the parser.
    print("Parsing completed.")

main()
