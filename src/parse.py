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
    
    def isCurTokenOfKind(self, kind):
        """
        Return true if the current token matches.
        """
        return kind == self.curToken.kind

    def isPeekTokenOfKind(self, kind):
        """
        Return true if the next token matches.
        """
        return kind == self.peekToken.kind

    def match(self, kind):
        """
        Try to match current token. If not, error. Advances the current token.
        """
        if not self.isCurTokenOfKind(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def hasIndentation(self, indentationSize):
        if indentationSize == 0:
            if self.isCurTokenOfKind(TokenType.SPACE):
                return False
            return True

        if not self.isCurTokenOfKind(TokenType.SPACE) or self.curToken.count != indentationSize:
            return False
        return True

    def hasIndentationOrAbort(self, indentationSize):
        if indentationSize == 0:
            if self.isCurTokenOfKind(TokenType.SPACE):
                self.abort("Unexpected indentation at " + self.curToken.text)
            return

        if not self.isCurTokenOfKind(TokenType.SPACE):
            self.abort("Expected indentation at " + self.curToken.text) 
        if self.curToken.count != indentationSize:
            self.abort("Wrong amount of indentation given at " + self.curToken.text)
        self.nextToken()

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
        return self.isCurTokenOfKind(TokenType.GT) or self.isCurTokenOfKind(TokenType.GTEQ) or self.isCurTokenOfKind(TokenType.LT) or self.isCurTokenOfKind(TokenType.LTEQ) or self.isCurTokenOfKind(TokenType.EQEQ) or self.isCurTokenOfKind(TokenType.NOTEQ)

    def isArithmeticOperator(self):
        """
        Return true if the current token is a arithmetic operator.
        """
        return self.isCurTokenOfKind(TokenType.PLUS) or self.isCurTokenOfKind(TokenType.MINUS) or self.isCurTokenOfKind(TokenType.ASTERISK) or self.isCurTokenOfKind(TokenType.SLASH)

    def isLogicalOperator(self, token):
        """
        Return true if the specified token is a logical operator.
        """
        return token.kind == TokenType.AND or token.kind == TokenType.OR or token.kind == TokenType.NOT

    def parseStatementsInBlock(self, indentationSize: int) -> None:
        """Get statements in a block.

        Parameters:
        indentationSize (int): The minimum indentation size of each statement.
        """
        if self.isCurTokenOfKind(TokenType.SPACE) and self.curToken.count >= indentationSize:
                statementIndentSize = self.curToken.count

                # One or more statements in the body.
                while self.isCurTokenOfKind(TokenType.SPACE) and self.curToken.count == statementIndentSize:
                    self.statement(statementIndentSize)
        else:
            self.abort("IndentationError: expected an indented block")

    def abort(self, message):
        sys.exit("Error. " + message)
        

    # Production rules.

    def program(self):
        """
        program ::= {statement}
        """
        parseLogger.info("程序 (PROGRAM)")

        # Since some newlines are required in our grammar, need to skip the excess.
        while self.isCurTokenOfKind(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.isCurTokenOfKind(TokenType.EOF):
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
        self.hasIndentationOrAbort(indentationSize)
        self.emitter.emit(" " * indentationSize)

        # Check the first token to see what kind of statement this is.

        # “印出”（ expression | string ）+ nl
        if self.isCurTokenOfKind(TokenType.PRINT):
            parseLogger.info("STATEMENT-PRINT")

            self.nextToken()
            self.match(TokenType.OPEN_BRACKET)

            if self.isCurTokenOfKind(TokenType.STRING):
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
        elif self.isCurTokenOfKind(TokenType.IF):
            parseLogger.info("STATEMENT-IF")

            self.emitter.emit("if ")
            self.nextToken()
            self.expression()

            self.match(TokenType.COLON)
            self.emitter.emit(":")

            self.nl()

            self.parseStatementsInBlock(indentationSize + 1)

            # One or more optional 'elif' blocks
            while self.hasIndentation(indentationSize) and\
                ((indentationSize == 0 and self.isCurTokenOfKind(TokenType.ELIF))\
                 or (indentationSize > 0 and self.isPeekTokenOfKind(TokenType.ELIF))):
                parseLogger.info("STATEMENT-ELIF")

                if indentationSize > 0:
                    self.nextToken()
                self.emitter.emit(" " * indentationSize + "elif ")
                self.nextToken()
                self.expression()

                self.match(TokenType.COLON)
                self.emitter.emit(":")

                self.nl()

                self.parseStatementsInBlock(indentationSize + 1)

            # Optional 'else' block
            if self.hasIndentation(indentationSize) and\
                ((indentationSize == 0 and self.isCurTokenOfKind(TokenType.ELSE))\
                 or (indentationSize > 0 and self.isPeekTokenOfKind(TokenType.ELSE))):
                parseLogger.info("STATEMENT-ELSE")
                
                if indentationSize > 0:
                    self.nextToken()
                self.emitter.emit(" " * indentationSize + "else")
                self.nextToken()

                self.match(TokenType.COLON)
                self.emitter.emit(":")

                self.nl()

                self.parseStatementsInBlock(indentationSize + 1)

        # “当” comparison：nl {statement}
        elif self.isCurTokenOfKind(TokenType.WHILE):
            parseLogger.info("陈述-当 (STATEMENT-WHILE)")

            self.nextToken()
            self.emitter.emit("while ")
            self.expression()

            self.match(TokenType.COLON)
            self.emitter.emit(":")

            self.nl()

            if self.isCurTokenOfKind(TokenType.SPACE) and self.curToken.count > indentationSize:
                statementIndentSize = self.curToken.count

                # Zero or more statements in the loop body.
                while self.isCurTokenOfKind(TokenType.SPACE) and self.curToken.count == statementIndentSize:
                    self.emitter.emit(" " * statementIndentSize)
                    self.statement(statementIndentSize)
            else:
                self.abort('缩进错误：在\'当\'语句后需要一个缩进块 (IndentationError: expected an indented block after \'while\' statement)')

        # Variable Assignment: ident "=" expression + nl
        elif self.isCurTokenOfKind(TokenType.IDENT) and self.peekToken.kind == TokenType.EQ:
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

        # Missing 'if' statement
        elif self.isCurTokenOfKind(TokenType.ELSE):
            self.abort("SyntaxError: invalid syntax")

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
        while self.isCurTokenOfKind(TokenType.PLUS)\
                or self.isCurTokenOfKind(TokenType.MINUS)\
                or self.isComparisonOperator()\
                or self.isCurTokenOfKind(TokenType.AND) or self.isCurTokenOfKind(TokenType.OR):
            if self.isCurTokenOfKind(TokenType.AND):
                self.emitter.emit(" and ")
            elif self.isCurTokenOfKind(TokenType.OR):
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
        while self.isCurTokenOfKind(TokenType.ASTERISK) or self.isCurTokenOfKind(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()


    def unary(self):
        """
        unary ::= ["+" | "-" | "非"] primary
        """
        parseLogger.info("UNARY")

        # Optional unary +/-/非
        if self.isCurTokenOfKind(TokenType.PLUS)\
            or self.isCurTokenOfKind(TokenType.MINUS)\
            or self.isCurTokenOfKind(TokenType.NOT):
            if self.isCurTokenOfKind(TokenType.NOT):
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

        if self.isCurTokenOfKind(TokenType.NUMBER): 
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.isCurTokenOfKind(TokenType.IDENT):
            # Ensure the variable already exists.
            variable = getAlphaNumericVar(self.curToken.text)
            if variable not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)

            self.emitter.emit(variable)
            self.nextToken()
        elif self.isCurTokenOfKind(TokenType.OPEN_BRACKET):
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
        while self.isCurTokenOfKind(TokenType.NEWLINE):
            self.nextToken()
