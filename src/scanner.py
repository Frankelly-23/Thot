
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

    def _scan_token(self):
        
       c = self._advance() 
       match c:
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
        case _:
            error(self.line, "Unexpected character.")
            
        

    def scan_tokens(self) -> list[Token]:

        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

