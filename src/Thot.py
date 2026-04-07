#!/bin/python3

import sys
import errorUtils

from scanner.token import Token
from scanner.scanner import Scanner
from parser.parser import Parser
from parser.expr import Expr
from parser.ast_printer import Ast_printer 

def run(source: str):

    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()
    
    parser: Parser = Parser(tokens)
    expresion: Expr = parser.parse()
    
    if errorUtils.had_error:
       return 
    
    ast_printer = Ast_printer()

    sys.stderr.write(ast_printer.print_exp(expresion)) 
    
def run_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        source_code = file.read()

    run(source_code)    

    if errorUtils.had_error: 
        sys.exit(65) 
        
    
def run_prompt():
    while True:
        try:
           expresion = input("Thot [> ") 
           run(expresion)
           errorUtils.had_error = False
        except EOFError:
            print()
            break

def main() -> None:
    
    args = sys.argv[1:]
    if len(args) > 1:

        sys.stdout.write("Usage: Thot [script]")
        sys.exit(64)

    elif len(args) == 1:
        run_file(args[0])

    else:
        run_prompt()


if __name__ == "__main__":
    main()


