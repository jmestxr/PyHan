from lex import *
from emit import *
from parse import *
import sys
import io
import tempfile

def compile(inputString: str) -> str:
    """
    Compiles the input pyhan code into python code.
    
    Parameters:
        inputString (str): The input pyhan code.
    Returns:
        str: The compiled python code.
    """
    inputFile = io.StringIO(inputString)
    outputFile = tempfile.NamedTemporaryFile()
    source = ""

    # Remove blank lines
    for line in inputFile:
        if not line.isspace():
            source += line
            
    # Initialize the lexer, emitter, and parser.
    lexer = Lexer(source)
    emitter = Emitter(outputFile.name)
    
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    emitter.writeFile() # Write the output to file.

    return outputFile.read().decode('utf-8')
