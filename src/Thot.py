#!/bin/python3

import sys
from scanner import Scanner
from errorUtils import had_error 


def run(source: str):
    scanner: Scanner = Scanner(source)
    tokens: list[str] = scanner.scan_tokens()
    
    for token in tokens:
        print(token)

def run_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        source_code = file.read()

    run(source_code)    

    if had_error: 
        sys.exit(65) 
        
    
def run_prompt():
    global had_error
    while True:
        try:
           expresion = input("Thot [> ") 
           run(expresion)
           had_error = False
        except EOFError:
            print()
            break

def main() -> None:
    
    args = sys.argv[1:]
    if len(args) > 1:

        print("Usage: Thot [script]")
        sys.exit(64)

    elif len(args) == 1:
        run_file(args[0])

    else:
        run_prompt()


if __name__ == "__main__":
    main()


