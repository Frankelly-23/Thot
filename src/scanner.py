
from token import Token
from tokenType import TokenType
from errorUtils import error

class Scanner:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []  
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        pass 

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _add_token(self, type: TokenType, literal = None):

        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _match(self, expected: str):

        if self._is_at_end(): 
            return False 
        if self.source[self.current] != expected: 
            return False 

        self.current += 1
        return True 

    def _peek(self):
        if self._is_at_end():  
            return "/0"
        return self.source[self.current]

    def _nextpeek(self):
        if self.current + 1 >= len(self.source):  
            return "/0"
        return self.source[self.current + 1]

    def _string(self):

        while self._peek() != "'" and not self._is_at_end(): 
            if self._peek() == "\n": 
                self.line += 1
            self._advance()

        if self._is_at_end():
            error(self.line, "Unterminated str")
            return

        self._advance()
        value: str = self.source[(self.start + 1): (self.current - 1)] 
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._peek().isdigit() and not self._is_at_end():
           self._advance() 
        
        if self._peek() == "." and self._nextpeek().isdigit():
            self._advance()
            while self._peek().isdigit() and not self._is_at_end():
                self._advance() 

        value = self.source[self.start:self.current]
        self._add_token(TokenType.NUMBER, value)

    def _scan_token(self):
        
       c = self._advance() 
       match c:
    # Single-character tokens.
        case ")":
            self._add_token(TokenType.LEFT_PAREN)
        case "(":
            self._add_token(TokenType.RIGHT_PAREN)
        case "}":
            self._add_token(TokenType.LEFT_BRACE)
        case "{":
            self._add_token(TokenType.RIGHT_BRACE)
        case ",":
            self._add_token(TokenType.COMMA)
        case ".":
            self._add_token(TokenType.DOT)
        case "-":
            self._add_token(TokenType.MINUS)
        case "+":
            self._add_token(TokenType.PLUS)
        case "*":
            self._add_token(TokenType.STAR)
        case ";":
            self._add_token(TokenType.SEMICOLON)
    # One or two character tokens.
        case "!":
            self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
        case "=":
            self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
        case "<":
            self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
        case ">":
            self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
        case "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        # Literals.
        case "'":
            self._string() 
        # garbage
        case " ":
            pass
        case "\t":
            pass
        case "\r":
            pass
        case "\n":
            self.line += 1
        case _:
            if c.isdigit():
                self._number()
            else:
                error(self.line, "Unexpected character.")
        
    # entry point
    def scan_tokens(self) -> list[Token]:

        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

