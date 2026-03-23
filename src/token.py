from tokenType import TokenType

class Token:
    def __init__(self, t_type: TokenType, lexeme: str, literal, line: int) -> None:
        self.type: TokenType = t_type
        self.lexeme: str = lexeme
        self.literal = literal
        self.line: int = line
    
    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"  
        
        
