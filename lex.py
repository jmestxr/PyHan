import enum
import sys
import re

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

        # Check for unexpected indentation at beginning of file
        if self.curChar.isspace():
            self.abort("IndentationError: unexpected indent")

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peekForward(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]
    
    # Return the lookbackward character.
    def peekBackward(self):
        if self.curPos <= 0:
            return None
        return self.source[self.curPos - 1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token.
    def getToken(self):
        if self.peekBackward() != '\n':
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
        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
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
            if keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)  
        elif Lexer.iscolon(self.curChar):
            token = Token(self.curChar, TokenType.COLON)
        elif self.curChar.isspace():
            numSpaces = 1
            while self.peekForward().isspace():
                self.nextChar()
                numSpaces += 1
            token = Token(self.curChar, TokenType.SPACE, numSpaces)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)
			
        self.nextChar()
        return token
    
    @staticmethod
    def ischinese(char):
        return len(re.findall(r'[\u4e00-\u9fff]+', char)) > 0
    
    @staticmethod
    def iscolon(char):
        return char == '：' or char == ':'


# Token contains the original text, type of token and number of tokens.
class Token:   
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


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	SPACE = 1
	COLON = 2
	NUMBER = 3
	IDENT = 4
	STRING = 5
	# Keywords.
	PRINT = 101
	IF = 102
	WHILE = 103
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

ChineseKeywords = {
    "PRINT": "印出",
    "IF": "如果",
    "WHILE": "当"
}
