from lex import *
from emit import *
from parse import *
import sys

def compile(inputFile: str, outputFile: str) -> None:
    """
    Compiles the source file into the target file.
    
    Parameters:
        inputFile (str): The path to the source file.
        outputFile (str): The path to the target file.
    """
    if not inputFile or not outputFile:
        sys.exit("Error: Compiler needs both source file and output file as argument.")

    source = ""
    with open(inputFile, 'r') as sourceFile:
        # Remove blank lines
        for line in sourceFile:
            if not line.isspace():
                source += line

    # Initialize the lexer, emitter, and parser.
    lexer = Lexer(source)
    emitter = Emitter(outputFile)
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    emitter.writeFile() # Write the output to file.
