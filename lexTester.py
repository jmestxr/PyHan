from lex import *

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

    lexer = Lexer(source)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind, token.count)
        token = lexer.getToken()

main()
