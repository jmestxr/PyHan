import enum
import sys
import re

class Lexer:
    def __init__(self, input: str):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

    def nextChar(self) -> None:
        """
        Process the next character.
        """
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    def peekForward(self) -> None:
        """
        Return the lookahead character.
        """
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]
    
    def peekBackward(self) -> None:
        """
        Return the lookbackward character.
        """
        if self.curPos <= 0 or self.curPos > len(self.source):
            return None
        return self.source[self.curPos - 1]

    def abort(self, message: str) -> None:
        """
        Display an error message and exit if an invalid token is found.
        
        Parameters:
        message (str): The error message to display.
        """
        sys.exit("Lexing error. " + message)
		
    def skipWhitespace(self) -> None:
        """
        Skip whitespace except newlines, which we will use to indicate the end of a statement.
        """
        while Lexer.isspace(self.curChar):
            self.nextChar()
		
    def skipComment(self) -> None:
        """
        Skip comments in the code.
        """
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self) -> None:
        """
        Return the next token.
        """
        if self.peekBackward() and self.peekBackward() != '\n':
            self.skipWhitespace()

        self.skipComment()

        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peekForward() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peekForward() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peekForward() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peekForward() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peekForward())
        elif Lexer.isquote(self.curChar):
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while not Lexer.isquote(self.curChar):
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peekForward().isdigit():
                self.nextChar()
            if self.peekForward() == '.': # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peekForward().isdigit(): 
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peekForward().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif Lexer.ischinese(self.curChar) or self.curChar.isalpha():
            # Leading character is an English or Chinese character, 
            # so this must be an identifier or a keyword.
            # Get all consecutive chinese/alpha/numeric characters.
            startPos = self.curPos
            while Lexer.ischinese(self.peekForward()) or self.peekForward().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            logicalOperator = Token.checkIfLogicalOperator(tokText)
            if keyword: # Keyword
                token = Token(tokText, keyword)
            elif logicalOperator: # Logical Operator
                token = Token(tokText, logicalOperator)
            else:   # Identifier
                token = Token(tokText, TokenType.IDENT)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)  
        elif Lexer.iscolon(self.curChar):
            token = Token(self.curChar, TokenType.COLON)
        elif Lexer.isspace(self.curChar):
            numSpaces = 1
            while Lexer.isspace(self.peekForward()):
                self.nextChar()
                numSpaces += 1
            token = Token(self.curChar, TokenType.SPACE, numSpaces)
        elif self.curChar == '(':
            token = Token(self.curChar, TokenType.OPEN_BRACKET)
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.CLOSE_BRACKET)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)
			
        self.nextChar()
        return token
    
    @staticmethod
    def ischinese(char) -> bool:
        """
        Check if a character is Chinese.
        """
        return len(re.findall(r'[\u4e00-\u9fff]+', char)) > 0
    
    @staticmethod
    def iscolon(char) -> bool:
        """
        Check if a character is colon.
        """
        return char == ':'
    
    @staticmethod
    def isquote(char) -> bool:
        """
        Check if a character is quote.
        """
        return char == '\"'
    
    @staticmethod
    def isspace(char) -> bool:
        """
        Check if a character is space.
        """
        return char == ' ' or char == '\t' or char == '\r'
    
    
class Token:
    """
    Token contains the original text, type of token and number of tokens.
    """   
    def __init__(self, tokenText, tokenKind, numTokens = 1):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.
        self.count = numTokens  # The number of this token

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.value >= 100 and kind.value < 200 and ChineseKeywords[kind.name] == tokenText:
                return kind
        return None
    
    @staticmethod
    def checkIfLogicalOperator(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 3XX.
            if kind.value >= 300 and ChineseLogicalOperators[kind.name] == tokenText:
                return kind
        return None


class TokenType(enum.Enum):
    """
    Enum for all the types of tokens.
    """
    EOF = -1
    NEWLINE = 0
    SPACE = 1
    COLON = 2
    OPEN_BRACKET = 3
    CLOSE_BRACKET = 4
    NUMBER = 5
    IDENT = 6
    STRING = 7
	# Keywords.
    PRINT = 101
    IF = 102
    ELIF = 103
    ELSE = 104
    WHILE = 105
    BREAK = 106
    CONTINUE = 107
	# Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    # Logical Operators.
    AND = 301
    OR = 302
    NOT = 303

ChineseKeywords = {
    "PRINT": "印出",
    "IF": "如果",
    "ELIF": "或则",
    "ELSE": "否则",
    "WHILE": "当",
    "BREAK": "中断",
    "CONTINUE": "继续"
}

ChineseLogicalOperators = {
    "AND": "与",
    "OR": "或",
    "NOT": "非"
}
