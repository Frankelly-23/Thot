
import sys
had_error = False

def report(line: int, where: str, message: str):
    global had_error
    print(f"[+] Error at line: {line}, Issue {where}: {message}", file=sys.stderr)
    had_error = True 

def error(line: int, message: str):
    report(line, "", message)
