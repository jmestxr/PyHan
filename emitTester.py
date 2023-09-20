from lex import *
from emit import *
from parse import *
import sys

def main():
    print("Teeny Tiny Compiler")

    source = ""

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        # Remove blank lines
        for line in inputFile:
            if not line.isspace():
                source += line

    # Initialize the lexer, emitter, and parser.
    lexer = Lexer(source)
    emitter = Emitter("out.py")
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    emitter.writeFile() # Write the output to file.
    print("Compiling completed.")

main()