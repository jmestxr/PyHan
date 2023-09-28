import sys
import os
from tokenize import TokenError

# appending the directory of parseLogger.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../log")   

from lex import *
from utils import getAlphaNumericVar
from parseLogger import parseLogger

class Parser:
    """
    Parser object keeps track of current token and checks if the code matches the grammar.
    """
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()    # All variables we have declared so far.

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.
    
    def checkToken(self, kind):
        """
        Return true if the current token matches.
        """
        return kind == self.curToken.kind

    def checkPeek(self, kind):
        """
        Return true if the next token matches.
        """
        return kind == self.peekToken.kind

    def match(self, kind):
        """
        Try to match current token. If not, error. Advances the current token.
        """
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

    def nextToken(self):
        """
        Advances the current token.
        """
         # No need to worry about passing the EOF, lexer handles that.
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        if self.curToken and self.peekToken\
            and (self.isComparisonOperator() or self.isArithmeticOperator())\
            and self.isLogicalOperator(self.peekToken):
            self.abort("SyntaxError: invalid syntax")

    def isComparisonOperator(self):
        """
        Return true if the current token is a comparison operator.
        """
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def isArithmeticOperator(self):
        """
        Return true if the current token is a arithmetic operator.
        """
        return self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS) or self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH)

    def isLogicalOperator(self, token):
        """
        Return true if the specified token is a logical operator.
        """
        return token.kind == TokenType.AND or token.kind == TokenType.OR or token.kind == TokenType.NOT


    def abort(self, message):
        sys.exit("Error. " + message)
        

    # Production rules.

    def program(self):
        """
        program ::= {statement}
        """
        parseLogger.info("程序 (PROGRAM)")

        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()


    def statement(self, indentationSize = 0):
        """
        One of the following statements...
        - PRINT: “印出”（ expression | string ）+ nl
        - IF: “如果” comparison：nl {statement}
        - WHILE: “当” comparison：nl {statement}
        - VARIABLE ASSIGNMENT: ident "=" expression + nl
        - EXPRESSION
        """
        # Check that the number of spaces at beginning of statement
        # corresponds to expected indentation size
        self.checkIndentation(indentationSize)

        if indentationSize > 0:
            self.nextToken()

        # Check the first token to see what kind of statement this is.

        # “印出”（ expression | string ）+ nl
        if self.checkToken(TokenType.PRINT):
            parseLogger.info("陈述-印出 (STATEMENT-PRINT)")

            self.nextToken()
            self.match(TokenType.OPEN_BRACKET)

            if self.checkToken(TokenType.STRING):
                # Simple string.
                self.emitter.emit("print(\"" + self.curToken.text + "\")")
                self.nextToken()
            else:
                # Expect an expression.
                self.emitter.emit("print(")
                self.expression()
                self.emitter.emit(")")
            
            self.match(TokenType.CLOSE_BRACKET)
            
            # Expect one or more newlines at the end
            self.nl()

        # “如果” comparison：nl {statement}
        elif self.checkToken(TokenType.IF):
            parseLogger.info("陈述-如果 (STATEMENT-IF)")
            self.nextToken()
            self.emitter.emit("if ")
            self.expression()

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
                self.abort('缩进错误：在\'如果\'语句后需要一个缩进块 (IndentatilonError: expected an indented block after \'if\' statement)')

        # “当” comparison：nl {statement}
        elif self.checkToken(TokenType.WHILE):
            parseLogger.info("陈述-当 (STATEMENT-WHILE)")

            self.nextToken()
            self.emitter.emit("while ")
            self.expression()

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

        # Variable Assignment: ident "=" expression + nl
        elif self.checkToken(TokenType.IDENT) and self.peekToken.kind == TokenType.EQ:
            parseLogger.info("陈述-变量赋值 (STATEMENT-VARIABLE ASSIGNMENT)")

            variable = getAlphaNumericVar(self.curToken.text)
            self.emitter.emit(variable)

            self.nextToken()
            self.match(TokenType.EQ)

            self.emitter.emit("=")

            self.expression()

            #  Check if ident exists in symbol table. If not, declare it.
            if variable not in self.symbols:
                self.symbols.add(variable)

            self.nl()

        else:
            self.expression()
            self.nl()


    def expression(self):
        """
        Any of the following:
        - expression ::= term {( "-" | "+" ) term}
        - comparison (special kind of expression) ::= 
            term (("==" | "!=" | ">" | ">=" | "<" | "<=") term)
        - logical (special kind of expression) ::=
            term(("与" | "或") term)
        """
        parseLogger.info("EXPRESSION/COMPARISON")

        self.term()
        # Can have 0 or more +,-,==,!=,>,>=,<,<=,与,或 expressions.
        while self.checkToken(TokenType.PLUS)\
                or self.checkToken(TokenType.MINUS)\
                or self.isComparisonOperator()\
                or self.checkToken(TokenType.AND) or self.checkToken(TokenType.OR):
            if self.checkToken(TokenType.AND):
                self.emitter.emit(" and ")
            elif self.checkToken(TokenType.OR):
                self.emitter.emit(" or ")
            else:
                self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()


    def term(self):
        """
        term ::= unary {( "/" | "*" ) unary}
        """
        parseLogger.info("TERM")

        self.unary()
        # Can have 0 or more *// expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()


    def unary(self):
        """
        unary ::= ["+" | "-" | "非"] primary
        """
        parseLogger.info("UNARY")

        # Optional unary +/-/非
        if self.checkToken(TokenType.PLUS)\
            or self.checkToken(TokenType.MINUS)\
            or self.checkToken(TokenType.NOT):
            if self.checkToken(TokenType.NOT):
                self.emitter.emit("not ")
            else:
                self.emitter.emit(self.curToken.text)
            self.nextToken()       
        self.primary()


    def primary(self):
        """
        primary ::= number | ident | LPAREN expr RPAREN
        """
        parseLogger.info("PRIMARY")

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
        elif self.checkToken(TokenType.OPEN_BRACKET):
            self.emitter.emit(self.curToken.text)
            self.nextToken()

            self.expression()

            self.match(TokenType.CLOSE_BRACKET)
            self.emitter.emit(")")
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)


    def nl(self):
        """
        nl ::= '\n'+
        """
        parseLogger.info("换行 (NEWLINE)")
		
        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        self.emitter.emitLine("")

        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
