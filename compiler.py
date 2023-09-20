from lex import *
from emit import *
from parse import *
import sys

def main():
    print("Py汉 compiler")

    if len(sys.argv) != 3:
        sys.exit("Error: Compiler needs both source file and output file as argument.")
    
    sourceFile, outputFile = sys.argv[1:]

    source = ""
    with open(sourceFile, 'r') as inputFile:
        # Remove blank lines
        for line in inputFile:
            if not line.isspace():
                source += line

    # Initialize the lexer, emitter, and parser.
    lexer = Lexer(source)
    emitter = Emitter(outputFile)
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    emitter.writeFile() # Write the output to file.
    print("Compiling completed.")

main()
