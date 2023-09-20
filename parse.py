import sys
from lex import *
from utils import getAlphaNumericVar

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()    # All variables we have declared so far.

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.
    
    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def checkIndentation(self, indentationSize):
        if indentationSize == 0:
            if self.checkToken(TokenType.SPACE):
                self.abort("Unexpected indentation at " + self.curToken.text)
            return

        if not self.checkToken(TokenType.SPACE):
            self.abort("Expected indentation at " + self.curToken.text) 
        if self.curToken.count != indentationSize:
            self.abort("Wrong amount of indentation given at " + self.curToken.text)

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def abort(self, message):
        sys.exit("Error. " + message)
        

    # Production rules.

    # program ::= {statement}
    def program(self):
        print("程序 (PROGRAM)")

        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    # One of the following statements...
    def statement(self, indentationSize = 0):
        # Check that the number of spaces at beginning of statement
        # corresponds to expected indentation size
        self.checkIndentation(indentationSize)

        if indentationSize > 0:
            self.nextToken()

        # Check the first token to see what kind of statement this is.

        # “印出”（ expression | string ）+ nl
        if self.checkToken(TokenType.PRINT):
            print("陈述-印出 (STATEMENT-PRINT)")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # Simple string.
                self.emitter.emit("print(\"" + self.curToken.text + "\")")
                self.nextToken()

            else:
                # Expect an expression.
                self.emitter.emit("print(\"")
                self.expression()
                self.emitter.emit("\")")
            
            # Expect one or more newlines at the end
            self.nl()

        # “如果” comparison：nl {statement}
        elif self.checkToken(TokenType.IF):
            print("陈述-如果 (STATEMENT-IF)")
            self.nextToken()
            self.emitter.emit("if ")
            self.comparison()

            self.match(TokenType.COLON)
            self.emitter.emit(":")

            self.nl()
        
            if self.checkToken(TokenType.SPACE) and self.curToken.count > indentationSize:
                statementIndentSize = self.curToken.count

                # Zero or more statements in the body.
                while self.checkToken(TokenType.SPACE) and self.curToken.count == statementIndentSize:
                    self.emitter.emit(" " * statementIndentSize)
                    self.statement(statementIndentSize)
            else:
                self.abort('缩进错误：在\'如果\'语句后需要一个缩进块 (IndentationError: expected an indented block after \'if\' statement)')

        # “当” comparison：nl {statement}
        elif self.checkToken(TokenType.WHILE):
            print("陈述-当 (STATEMENT-WHILE)")
            self.nextToken()
            self.emitter.emit("while ")
            self.comparison()

            self.match(TokenType.COLON)
            self.emitter.emit(":")

            self.nl()

            if self.checkToken(TokenType.SPACE) and self.curToken.count > indentationSize:
                statementIndentSize = self.curToken.count

                # Zero or more statements in the loop body.
                while self.checkToken(TokenType.SPACE) and self.curToken.count == statementIndentSize:
                    self.emitter.emit(" " * statementIndentSize)
                    self.statement(statementIndentSize)
            else:
                self.abort('缩进错误：在\'当\'语句后需要一个缩进块 (IndentationError: expected an indented block after \'while\' statement)')

        # Variable Assignment; ident "=" expression + nl
        elif self.checkToken(TokenType.IDENT):
            print("陈述-变量赋值 (STATEMENT-VARIABLE ASSIGNMENT)")

            variable = getAlphaNumericVar(self.curToken.text)
            #  Check if ident exists in symbol table. If not, declare it.
            if variable not in self.symbols:
                self.symbols.add(variable)
                self.emitter.emit(variable + " = ")

            self.nextToken()
            self.match(TokenType.EQ)

            self.expression()

            self.nl()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()


    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()        
        self.primary()

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER): 
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists.
            variable = getAlphaNumericVar(self.curToken.text)
            if variable not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)

            self.emitter.emit(variable)
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)
    
    # nl ::= '\n'+
    def nl(self):
        print("换行 (NEWLINE)")
		
        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        self.emitter.emitLine("")

        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
