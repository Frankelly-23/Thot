
import sys
from scanner.token import Token
from scanner.tokenType import TokenType 

had_error = False

def report(line: int, where: str, message: str):
    global had_error
    print(f"[+] Error at line: {line}, Issue {where}: {message}", file=sys.stderr)
    had_error = True 

def error(token: Token, message: str):

    if token.type == TokenType.EOF: 
        report(token.line, "At end", message)

    else:
        report(token.line, f"At '{token.lexeme}' " , message)
